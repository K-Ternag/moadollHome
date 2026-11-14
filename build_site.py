"""Generate a buildless, bilingual GitHub Pages site. Python standard library only."""
from pathlib import Path
from html import escape
from urllib.parse import quote, urlsplit
from datetime import date
import argparse
import json
import re
import shutil
from site_content import COPY, FEATURES, LEGAL

ROOT = Path(__file__).resolve().parent
PAGES = ['index', 'guide', 'support', 'privacy', 'delete-account', 'terms']


def filename(page, lang):
    return page + ('.en' if lang == 'en' else '') + '.html'


def asset(slug, lang):
    return f'assets/{lang}/{slug}.jpg'


def valid_email(value):
    return isinstance(value, str) and bool(re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", value))


def validate_config(c):
    for key in ['developerName', 'supportEmail', 'playStoreUrl', 'siteUrl', 'policyEffectiveDate']:
        if not isinstance(c.get(key), str):
            raise ValueError(f'{key} must be a string')
        c[key] = c[key].strip()
    if c['supportEmail'] and not valid_email(c['supportEmail']):
        raise ValueError('supportEmail must be a valid email address')
    if c['siteUrl']:
        url = urlsplit(c['siteUrl'])
        if url.scheme != 'https' or not url.netloc or url.query or url.fragment or url.username:
            raise ValueError('siteUrl must be an HTTPS base URL without query or fragment')
        c['siteUrl'] = c['siteUrl'].rstrip('/') + '/'
    if c['playStoreUrl']:
        url = urlsplit(c['playStoreUrl'])
        if url.scheme != 'https' or url.netloc != 'play.google.com' or url.path != '/store/apps/details':
            raise ValueError('playStoreUrl must be an HTTPS Google Play app listing')
        from urllib.parse import parse_qs
        if parse_qs(url.query).get('id') != ['com.moadoll']:
            raise ValueError('playStoreUrl must identify com.moadoll')
    if c['policyEffectiveDate']:
        date.fromisoformat(c['policyEffectiveDate'])
    days = c.get('supportRetentionDays')
    if days is not None and (type(days) is not int or not 1 <= days <= 3650):
        raise ValueError('supportRetentionDays must be an integer between 1 and 3650, or null')
    if type(c.get('policiesApproved')) is not bool:
        raise ValueError('policiesApproved must be a boolean')
    if c['policiesApproved'] and not policy_ready(c):
        raise ValueError('Approved policies require developerName, supportEmail, policyEffectiveDate, and supportRetentionDays')
    return c


def policy_ready(c):
    return bool(c.get('policiesApproved') and all(c.get(k) for k in ['developerName', 'supportEmail', 'policyEffectiveDate', 'supportRetentionDays']))


def mail_link(c, text=None, subject='MoaDoll'):
    target = 'mailto:' + quote(c['supportEmail'], safe='@.') + '?subject=' + quote(subject)
    return f'<a href="{escape(target, quote=True)}">{escape(text or c["supportEmail"])}</a>'


def store(c, t, large=False):
    if c['playStoreUrl']:
        return f'<a class="button store-button" href="{escape(c["playStoreUrl"], quote=True)}"><span aria-hidden="true">▷</span>{t["download"]}<span aria-hidden="true">↗</span></a>'
    return f'<span class="store-status"><span class="status-dot" aria-hidden="true"></span>{t["coming"]}</span>'


def brand(lang):
    return f'<a class="brand" href="{filename("index",lang)}" aria-label="MoaDoll"><img src="assets/favicon.svg" width="38" height="38" alt=""><span>MoaDoll<small>모아돌</small></span></a>'


def layout(page, lang, content, c):
    t = COPY[lang]
    title = t['title'] if page == 'index' else (t['notFoundTitle'] if page == '404' else t['pages'][page]) + ' · MoaDoll'
    description = t['description'] if page in ['index','404'] else t['pageDescriptions'][page]
    base = c['siteUrl']
    pageurl = base + filename(page, lang)
    meta = f'<meta name="robots" content="noindex">' if page == '404' else ''
    if base:
        meta += f'<link rel="canonical" href="{escape(pageurl)}"><meta property="og:url" content="{escape(pageurl)}"><meta property="og:image" content="{escape(base + asset("03-photocard",lang))}">'
    else:
        meta += f'<meta property="og:image" content="{asset("03-photocard",lang)}">'
    for code in ['ko','en','x-default']:
        target_lang = 'en' if code == 'x-default' else code
        meta += f'<link rel="alternate" hreflang="{code}" href="{escape(base + filename(page,target_lang))}">'
    navlinks = [filename('index',lang)+'#story', filename('index',lang)+'#gallery', filename('guide',lang), filename('support',lang)]
    nav = ''.join(f'<a href="{url}"'+(' aria-current="page"' if url == filename(page,lang) else '')+f'>{label}</a>' for url,label in zip(navlinks,t['nav']))
    languages = ''.join(f'<a class="language-link" href="{filename(page,code)}" lang="{code}" hreflang="{code}"'+(' aria-current="page"' if lang==code else '')+f'>{label}</a>' for code,label in [('ko','KO'),('en','EN')])
    footer = ''.join(f'<a href="{filename(p,lang)}">{label}</a>' for p,label in zip(['privacy','delete-account','terms','support'],t['footerLinks']))
    return f'''<!doctype html>
<html lang="{lang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(description,quote=True)}">
<meta name="theme-color" content="#faf8f3"><meta name="referrer" content="strict-origin-when-cross-origin">
<meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}">
<meta property="og:type" content="website"><meta property="og:site_name" content="MoaDoll"><meta property="og:locale" content="{'ko_KR' if lang=='ko' else 'en_US'}">
<meta name="twitter:card" content="summary_large_image">{meta}
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg"><link rel="stylesheet" href="styles.css">
<script src="app.js" defer></script></head>
<body><a class="skip" href="#main">{t['skip']}</a>
<header class="site-header"><div class="wrap header-inner">{brand(lang)}
<button class="menu-toggle" aria-expanded="false" aria-controls="navigation" hidden>{t['menu']} <span aria-hidden="true">☰</span></button>
<nav id="navigation" aria-label="{'주 메뉴' if lang=='ko' else 'Main navigation'}">{nav}<div class="languages" aria-label="Language">{languages}</div></nav></div></header>
<main id="main">{content}</main>
<footer class="site-footer"><div class="wrap footer-top"><div>{brand(lang)}<p>{t['footerLine']}</p></div><div class="footer-links">{footer}</div></div><div class="wrap footer-bottom"><span>© {date.today().year} {escape(c['developerName'] or 'MoaDoll')}</span><span>MADE FOR YOUR LITTLE WORLD</span></div></footer>
<dialog id="lightbox" aria-labelledby="lightbox-title"><div class="dialog-bar"><span id="lightbox-title">{t['zoom']}</span><button type="button" class="close-dialog">{t['close']} <span aria-hidden="true">×</span></button></div><img id="lightbox-image" alt=""><p id="lightbox-caption"></p></dialog>
</body></html>'''


def home(lang,c):
    t=COPY[lang]
    stats=''.join(f'<div><strong>{v}</strong><span>{label}</span></div>' for v,label in t['stats'])
    ribbon=''.join(f'<span>{label}</span><i aria-hidden="true">✧</i>' for label in t['ribbon'])
    tabs=''.join(f'<a id="tab-{i}" href="#feature-{i}" class="feature-tab"><span>0{i+1}</span>{f[1]}</a>' for i,f in enumerate(FEATURES[lang]))
    panels=''.join(f'''<section id="feature-{i}" class="feature-panel" aria-labelledby="feature-title-{i}"><a href="{asset(f[0],lang)}" class="zoom-link" data-zoom data-caption="{escape(f[4],quote=True)}"><img src="{asset(f[0],lang)}" alt="{f[4]}" width="1920" height="1080" loading="lazy"><span class="zoom-hint"><span aria-hidden="true">↗</span> {t['zoom']}</span></a><div class="feature-caption"><h3 id="feature-title-{i}">{f[2]}</h3><p>{f[3]}</p></div></section>''' for i,f in enumerate(FEATURES[lang]))
    steps=''.join(f'<li><span class="step-number">0{i+1}</span><h3>{heading}</h3><p>{body}</p></li>' for i,(heading,body) in enumerate(t['steps']))
    return f'''<section class="hero wrap" id="story"><div class="hero-copy"><p class="eyebrow"><span aria-hidden="true">✳</span> A LITTLE WORLD, ALL YOURS</p><h1>{t['hero']}</h1><p class="hero-intro">{t['intro']}</p><a class="button primary" href="#gallery">{t['explore']} <span aria-hidden="true">↗</span></a><div class="hero-availability">{store(c,t)}<small>{t['android']}</small></div></div>
<div class="hero-art"><span class="handwritten art-note" aria-hidden="true">made of little happy things</span><div class="paper-back" aria-hidden="true"></div><a class="hero-card" href="{asset('03-photocard',lang)}" data-zoom data-caption="{FEATURES[lang][2][4]}" aria-label="{t['zoom']}"><div class="hero-crop"><img src="{asset('03-photocard',lang)}" alt="{FEATURES[lang][2][4]}" width="1920" height="1080" fetchpriority="high"></div><span class="card-bottom">a little moment, forever.</span></a><span class="floating-flower" aria-hidden="true">✿</span><span class="floating-spark" aria-hidden="true">✧</span><span class="paper-label">{t['heroNote']}</span></div></section>
<div class="ribbon"><div class="wrap">{ribbon}</div></div>
<section class="gallery-section section-space" id="gallery"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">{t['galleryEyebrow']}</p><h2>{t['galleryTitle']}</h2></div><p>{t['galleryIntro']}</p></div><div class="feature-tabs" aria-label="{'앱 기능' if lang=='ko' else 'App features'}">{tabs}</div><div class="feature-stage">{panels}</div><p class="caption-note">{t['galleryNote']}</p><div class="stats">{stats}</div></div></section>
<section class="making-section section-space"><div class="wrap making-grid"><div><p class="eyebrow">FROM A DOLL TO A MEMORY</p><h2>{t['stepsTitle']}</h2><a class="text-link" href="{filename('guide',lang)}">{t['guideLink']} <span aria-hidden="true">↗</span></a><div class="little-colors" aria-hidden="true"><i></i><i></i><i></i><i></i><span>your colors, your story.</span></div></div><ol class="steps">{steps}</ol></div></section>
<section class="privacy-strip wrap"><span class="privacy-flower" aria-hidden="true">✳</span><div><p class="eyebrow">JUST YOU & YOUR LITTLE WORLD</p><h2>{t['privacyTitle']}</h2></div><div><p>{t['privacyIntro']}</p><small>{t['privacyNote']}</small><a class="text-link" href="{filename('privacy',lang)}">{t['privacyLink']} <span aria-hidden="true">↗</span></a></div></section>
<section class="closing section-space"><div class="wrap"><span class="closing-star" aria-hidden="true">✧</span><h2>{t['ctaTitle']}</h2><p>{t['ctaIntro']}</p>{store(c,t,True)}</div></section>'''


def faq(lang):
    t=COPY[lang]
    return '<section class="faq-section"><h2>'+t['faqTitle']+'</h2>'+''.join(f'<details><summary>{q}<span aria-hidden="true">+</span></summary><p>{a}</p></details>' for q,a in t['faqs'])+'</section>'


def contact(lang,c):
    t=COPY[lang]
    link=mail_link(c,t['emailAction']+' ↗','[MoaDoll] '+t['pages']['support']) if c['supportEmail'] else f'<p class="contact-pending">{t["noEmail"]}</p>'
    return f'<section class="contact-box" id="contact"><p class="eyebrow">HERE TO HELP</p><h2>{t["contactTitle"]}</h2><p>{t["contactIntro"]}</p>{link}<p class="small">{t["mailNote"]}</p></section>'


def guide(lang,c):
    t=COPY[lang]
    rows=''.join(f'''<section class="guide-row"><div><p class="eyebrow">STEP 0{i+1}</p><h2>{title}</h2><p>{body}</p></div><a href="{asset(FEATURES[lang][i][0],lang)}" data-zoom data-caption="{FEATURES[lang][i][4]}" aria-label="{t['zoom']}: {title}"><img src="{asset(FEATURES[lang][i][0],lang)}" alt="{FEATURES[lang][i][4]}" width="1920" height="1080" loading="lazy"></a></section>''' for i,(title,body) in enumerate(t['guideSteps']))
    return f'<div class="wrap page-content"><div class="page-heading"><p class="eyebrow">A SMALL GUIDE TO YOUR WORLD</p><h1>{t["pages"]["guide"]}</h1><p>{t["guideIntro"]}</p></div>{rows}<aside class="tip">{t["guideTip"]}</aside>{faq(lang)}</div>'


def support(lang,c):
    t=COPY[lang]
    return f'<div class="wrap narrow page-content"><div class="page-heading"><p class="eyebrow">A LITTLE HELP</p><h1>{t["pages"]["support"]}</h1><p>{t["supportIntro"]}</p></div>{faq(lang)}{contact(lang,c)}<p class="related-links"><a href="{filename("guide",lang)}">{t["pages"]["guide"]} ↗</a><a href="{filename("delete-account",lang)}">{t["pages"]["delete-account"]} ↗</a></p></div>'


def legal(page,lang,c):
    t=COPY[lang]
    notice='' if policy_ready(c) else f'<aside class="notice"><strong>{t["draftTitle"]}</strong><p>{t["draftText"]}</p></aside>'
    email=mail_link(c) if c['supportEmail'] else t['noEmail']
    identity=f'<dl class="identity"><div><dt>APP</dt><dd>MoaDoll · 모아돌 <small>com.moadoll</small></dd></div><div><dt>{t["operator"]}</dt><dd>{escape(c["developerName"] or t["pending"])}</dd></div><div><dt>{t["email"]}</dt><dd>{email}</dd></div><div><dt>{t["effective"]}</dt><dd>{escape(c["policyEffectiveDate"] or t["pending"])}</dd></div></dl>'
    if c['supportRetentionDays']:
        days=c['supportRetentionDays']
        retention=f'문의 처리가 끝난 날부터 {days}일 보관 후 삭제합니다' if lang=='ko' else f'deleted {days} days after the request is resolved'
    else:
        retention=t['pending']
    entries=LEGAL[lang][page]
    toc=''.join(f'<a href="#section-{i+1}"><span>{i+1:02d}</span>{heading}</a>' for i,(heading,_) in enumerate(entries))
    sections=''.join(f'<section id="section-{i+1}"><h2><span>{i+1:02d}</span>{heading}</h2><p>{escape(body.replace("{retention}",retention))}</p></section>' for i,(heading,body) in enumerate(entries))
    related=''.join(f'<a href="{filename(p,lang)}">{t["pages"][p]} ↗</a>' for p in ['privacy','delete-account','support'] if p!=page)
    refs=''
    if page=='privacy':
        refs='<p class="external-policies"><a href="https://policies.google.com/privacy">Google '+('개인정보처리방침' if lang=='ko' else 'Privacy Policy')+'</a><a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub '+('개인정보처리방침' if lang=='ko' else 'Privacy Statement')+'</a></p>'
    return f'<div class="wrap page-content"><div class="page-heading"><p class="eyebrow">YOUR WORLD, YOUR CHOICE</p><h1>{t["pages"][page]}</h1><p>MoaDoll · 모아돌</p></div><div class="legal-layout"><nav class="legal-toc" aria-label="{"목차" if lang=="ko" else "On this page"}">{toc}</nav><article class="legal-body">{notice}{identity}{sections}{refs}<div class="related-links">{related}</div></article></div></div>'


def build(output,config):
    output.mkdir(parents=True,exist_ok=True)
    if output.resolve()!=ROOT:
        for name in ['assets','styles.css','app.js','.nojekyll']:
            source=ROOT/name
            if source.is_dir(): shutil.copytree(source,output/name,dirs_exist_ok=True)
            else: shutil.copy2(source,output/name)
    for lang in ['ko','en']:
        for page in PAGES:
            content=home(lang,config) if page=='index' else guide(lang,config) if page=='guide' else support(lang,config) if page=='support' else legal(page,lang,config)
            (output/filename(page,lang)).write_text(layout(page,lang,content,config),encoding='utf-8')
        t=COPY[lang]
        content=f'<section class="not-found wrap"><p class="eyebrow">404 · LOST IN OUR LITTLE WORLD</p><h1>{t["notFoundTitle"]}</h1><p>{t["notFoundText"]}</p><a class="button primary" href="{escape(config["siteUrl"] or "./")}{filename("index",lang)}">{t["back"]} ↗</a></section>'
        html=layout('404',lang,content,config)
        if config['siteUrl']:
            html=html.replace('<head>','<head><base href="'+escape(config['siteUrl'],quote=True)+'">',1)
        (output/filename('404',lang)).write_text(html,encoding='utf-8')
    base=config['siteUrl']
    robots='User-agent: *\nAllow: /\n'+(f'Sitemap: {base}sitemap.xml\n' if base else '')
    (output/'robots.txt').write_text(robots,encoding='utf-8')
    urls=''.join(f'<url><loc>{escape(base+filename(p,lang))}</loc></url>' for p in PAGES for lang in ['ko','en']) if base else ''
    (output/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+urls+'</urlset>',encoding='utf-8')
    print(f'Built 14 pages in {output}. Policy status: '+('finalized' if policy_ready(config) else 'pre-release review'))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default=str(ROOT))
    parser.add_argument('--base-url',default=None)
    args=parser.parse_args()
    config=json.loads((ROOT/'site-config.json').read_text(encoding='utf-8'))
    if args.base_url is not None: config['siteUrl']=args.base_url
    build(Path(args.output).resolve(),validate_config(config))
