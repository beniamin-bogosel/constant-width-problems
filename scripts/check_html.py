#!/usr/bin/env python3
"""Check generated HTML structure, links, assets, and spoiler defaults."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse,unquote
from collections import Counter
import argparse
import json

class Document(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.attrs={};self.links=[];self.assets=[];self.buttons=[];self.problems=[];self.math_count=0
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs);classes=attrs.get('class','').split()
        if 'id' in attrs:self.ids.append(attrs['id']);self.attrs[attrs['id']]=attrs
        if tag=='a' and 'href' in attrs:self.links.append(attrs['href'])
        if tag in ('script','img') and 'src' in attrs:self.assets.append(attrs['src'])
        if tag=='link' and attrs.get('rel')=='stylesheet':self.assets.append(attrs['href'])
        if tag=='button' and 'reveal-button' in classes:self.buttons.append(attrs)
        if 'problem' in classes:self.problems.append(attrs)
        if tag=='math':self.math_count+=1

def check(path):
    doc=Document();doc.feed(path.read_text())
    manifest=json.loads((path.parent/'.cwdata-html.json').read_text())
    assert all(count==1 for count in Counter(doc.ids).values()),'Duplicate HTML IDs'
    assert len(doc.problems)==manifest['problems'],'HTML problem count differs from export manifest'
    assert len(doc.buttons)==2*len(doc.problems),'Each problem needs independent hint and solution controls'
    for button in doc.buttons:
        assert button['aria-expanded']=='false'
        target=doc.attrs[button['aria-controls']];assert 'hidden' in target,'Reveal content is visible on initial load'
    for href in doc.links:
        if href.startswith('#'):assert unquote(href[1:]) in doc.attrs,href
    for relative in doc.assets:
        assert not urlparse(relative).scheme,'Unexpected remote asset: '+relative
        assert (path.parent/relative).is_file(),relative
    assert doc.math_count==manifest['math_fragments'],'Some mathematical fragments were not rendered'
    assert 'CWMATHFRAGMENT' not in path.read_text(),'Unrendered math placeholder'
    print(f'HTML structure passed: {len(doc.problems)} problems, {len(doc.buttons)} initially closed controls, {doc.math_count} rendered formulas.')
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('path',type=Path,nargs='?',default=Path(__file__).resolve().parents[1]/'html/index.html');args=parser.parse_args();check(args.path)
