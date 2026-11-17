"""Check static navigation, assets, language parity, and optional release readiness."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import argparse
import json
from build_site import PAGES, ROOT, filename, missing_policy_fields, validate_config


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids=[]; self.refs=[]; self.tags=[]; self.lang=''; self.h1=0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        self.tags.append((tag,a))
        if 'id' in a: self.ids.append(a['id'])
        if tag=='html': self.lang=a.get('lang')
        if tag=='h1': self.h1+=1
        if tag=='img':
            assert 'alt' in a, 'Images need an alt attribute'
            if a.get('src') and a.get('src')!='assets/favicon.svg':
                assert a['alt'], 'Content images need descriptive alt text'
        if 'href' in a: self.refs.append((tag,a['href']))
        if 'src' in a: self.refs.append((tag,a['src']))


def verify(root):
    documents={p.name: Document(p.read_text(encoding='utf-8')) for p in root.glob('*.html')}
    assert len(documents)==14, f'Expected 14 pages, found {len(documents)}'
    count=0
    for name,d in documents.items():
        assert d.h1==1,(name,'one H1 required')
        assert len(d.ids)==len(set(d.ids)),(name,'duplicate IDs')
        lang='en' if '.en.' in name else 'ko'
        assert d.lang==lang,(name,'wrong language')
        for tag,a in d.tags:
            if tag=='img' and a.get('src') and a['src']!='assets/favicon.svg':
                assert a['src'].startswith('assets/'+lang+'/'),(name,'wrong image language',a['src'])
            if tag=='script': assert not a.get('src','').startswith('http'),(name,'external script')
        for tag,ref in d.refs:
            url=urlsplit(ref)
            assert url.scheme not in ['javascript','data'],(name,ref)
            if url.scheme or url.netloc: continue
            target=unquote(url.path) or name
            assert not target.startswith('/'),(name,'root-relative path breaks project Pages',ref)
            assert (root/target).is_file(),(name,'missing target',target)
            if url.fragment and target in documents:
                assert unquote(url.fragment) in documents[target].ids,(name,'missing anchor',ref)
            count+=1
        other=filename(name.split('.')[0],'ko' if lang=='en' else 'en')
        assert any(urlsplit(ref).path.endswith(other) for _,ref in d.refs),(name,'missing alternate language')
    print(f'PASS: {len(documents)} pages, {count} local references, image languages, IDs, headings and anchors.')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',default=str(ROOT))
    parser.add_argument('--release',action='store_true')
    args=parser.parse_args()
    verify(Path(args.root))
    if args.release:
        config=validate_config(json.loads((ROOT/'site-config.json').read_text(encoding='utf-8')))
        missing=missing_policy_fields(config)
        if missing: raise SystemExit('NOT READY FOR PLAY SUBMISSION: '+', '.join(missing))
        print('PASS: required policy configuration is complete. Confirm published URLs and the release app before submission.')
