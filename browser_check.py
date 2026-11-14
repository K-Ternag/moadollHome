"""Browser QA uses a real HTTP project subpath, not only file URLs."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urlsplit
import json
import time
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'.qa'
OUT.mkdir(exist_ok=True)
PREFIX='/characterGameHome'


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith(PREFIX+'/'):
            self.path=self.path[len(PREFIX):]
            super().do_GET()
        else:
            self.send_error(404)
    def log_message(self,*args): pass


server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT)))
thread=Thread(target=server.serve_forever,daemon=True)
thread.start()
base=f'http://127.0.0.1:{server.server_port}{PREFIX}/'
report={'basePath':PREFIX,'checks':[],'screenshots':[],'status':'running'}
config=json.loads((ROOT/'site-config.json').read_text(encoding='utf-8'))
errors=[]
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        context=browser.new_context(device_scale_factor=1)
        page=context.new_page()
        page.on('pageerror',lambda error: errors.append(str(error)))
        page.on('response',lambda response: errors.append(f'{response.status} {response.url}') if response.status>=400 else None)
        page.on('request',lambda request: errors.append('Unexpected external request: '+request.url) if urlsplit(request.url).hostname!='127.0.0.1' else None)
        for lang in ['ko','en']:
            suffix='.en' if lang=='en' else ''
            for name in ['index','guide','support','privacy','delete-account','terms','404']:
                page.goto(base+name+suffix+'.html',wait_until='networkidle')
                for width in [320,390,768,1440,1920]:
                    page.set_viewport_size({'width':width,'height':1000})
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),(name,lang,width,'horizontal overflow')
                assert page.locator('h1').count()==1
                assert page.locator('html').get_attribute('lang')==lang
            report['checks'].append(f'{lang}: all 7 pages fit 320, 390, 768, 1440 and 1920 px')
            page.goto(base+'index'+suffix+'.html')
            for index in range(4):
                page.locator('.feature-tab').nth(index).click()
                panel=page.locator('.feature-panel').nth(index)
                assert panel.is_visible()
                assert page.locator('.feature-panel:visible').count()==1
                panel.locator('img').scroll_into_view_if_needed()
                panel.locator('img').evaluate('(img) => img.decode()')
                assert '/'+lang+'/' in panel.locator('img').get_attribute('src')
                panel.locator('[data-zoom]').click()
                assert page.locator('#lightbox').evaluate('(el) => el.open')
                page.locator('#lightbox-image').evaluate('(img) => img.decode()')
                page.keyboard.press('Escape')
                assert not page.locator('#lightbox').evaluate('(el) => el.open')
                assert panel.locator('[data-zoom]').evaluate('(el) => el === document.activeElement')
            tabs=page.locator('.feature-tab')
            tabs.first.focus()
            page.keyboard.press('End')
            assert tabs.last.get_attribute('aria-selected')=='true'
            page.keyboard.press('ArrowRight')
            assert tabs.first.get_attribute('aria-selected')=='true'
            report['checks'].append(f'{lang}: 4 gallery tabs, correct localized assets, image dialogs, Escape/focus return, keyboard navigation')
            page.goto(base+'index'+suffix+'.html')
            page.set_viewport_size({'width':1440,'height':1000})
            page.locator('.hero img').evaluate('(img) => img.decode()')
            page.screenshot(path=str(OUT/f'home-{lang}-desktop.png'),full_page=True)
            page.screenshot(path=str(OUT/f'hero-{lang}-desktop.png'))
            page.set_viewport_size({'width':390,'height':844})
            page.locator('.menu-toggle').click()
            assert page.locator('#navigation').is_visible()
            page.keyboard.press('Escape')
            assert not page.locator('#navigation').is_visible()
            page.screenshot(path=str(OUT/f'home-{lang}-mobile.png'),full_page=True)
            report['screenshots'] += [f'home-{lang}-desktop.png',f'home-{lang}-mobile.png']
            page.goto(base+'support'+suffix+'.html')
            page.locator('summary').first.click()
            assert page.locator('details').first.get_attribute('open') is not None
            if config.get('supportEmail'):
                assert page.locator('a[href^="mailto:"]').count()>0
                assert page.locator('.contact-pending').count()==0
            else:
                assert page.locator('.contact-pending').is_visible()
                assert page.locator('a[href^="mailto:"]').count()==0
            report['checks'].append(f'{lang}: mobile menu, FAQ and configured contact state')
        page.set_viewport_size({'width':1440,'height':1000})
        page.goto(base+'index.html#feature-2')
        assert page.locator('#feature-2').is_visible()
        page.locator('.language-link[lang="en"]').click()
        assert page.url.endswith('index.en.html#feature-2')
        assert page.locator('#feature-2').is_visible()
        assert '/en/' in page.locator('#feature-2 img').get_attribute('src')
        page.goto(base+'privacy.en.html#section-4')
        page.locator('.language-link[lang="ko"]').click()
        assert page.url.endswith('privacy.html#section-4')
        report['checks'].append('Language switching preserves page and section')
        plain=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
        nojs=plain.new_page()
        nojs.goto(base+'index.html')
        assert nojs.locator('.feature-panel:visible').count()==4
        assert nojs.locator('#navigation').is_visible()
        for lang in ['ko','en']:
            suffix='.en' if lang=='en' else ''
            for name in ['privacy','delete-account','terms','support']:
                nojs.goto(base+name+suffix+'.html')
                assert len(nojs.locator('main').inner_text())>700
                assert nojs.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
        report['checks'].append('Without JavaScript: complete legal/support text, navigation and all 4 gallery images')
        assert not errors,errors
        report['checks'].append('No JavaScript errors, failed HTTP responses or external runtime requests')
        report['status']='passed'
        browser.close()
except Exception as error:
    report['status']='blocked' if isinstance(error,PermissionError) else 'failed'
    report['reason']=str(error)
    raise
finally:
    server.shutdown()
    server.server_close()
    report['errors']=errors
    (OUT/'browser-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
