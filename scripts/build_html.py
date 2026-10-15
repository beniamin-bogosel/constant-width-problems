#!/usr/bin/env python3
"""Build an offline HTML reader from the canonical chapter JSON files."""
import argparse
import html
import json
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import urlparse
import markdown
from validate import ROOT, validate, safe_path

def esc(value): return html.escape(str(value), quote=True)
MATH = re.compile(r'\$\$([\s\S]+?)\$\$|(?<!\\)\$([^$\n]+?)(?<!\\)\$')

class Renderer:
    def __init__(self): self.fragments=[]
    def md(self, text):
        # Protect TeX from Markdown's underscore and backslash interpretation.
        stash=[]
        def protect(match):
            display=match.group(1) is not None
            token=f'CWMATHFRAGMENT{len(self.fragments)}END'
            self.fragments.append(dict(text=match.group(1) if display else match.group(2),display=display))
            stash.append((token,display));return token
        protected=MATH.sub(protect,text)
        # Raw HTML in source text is text, not executable markup.
        result=markdown.markdown(html.escape(protected,quote=False),extensions=['tables','sane_lists'])
        return result
    def finish(self, document):
        process=subprocess.run(['node',str(ROOT/'web/render_math.cjs')],input=json.dumps(self.fragments),text=True,capture_output=True)
        if process.returncode: raise RuntimeError('Math rendering failed: '+process.stderr)
        rendered=json.loads(process.stdout)
        return re.sub(r'CWMATHFRAGMENT(\d+)END',lambda m:rendered[int(m[1])],document)

def load_collection():
    catalog=json.loads((ROOT/'data/catalog.json').read_text())
    sources={s['id']:s for s in json.loads((ROOT/'data/sources.json').read_text())['sources']}
    chapters=[]
    for chapter in sorted(catalog['chapters'],key=lambda c:c['order']):
        problems=json.loads((ROOT/'data'/chapter['problems']).read_text())['problems']
        solutions=json.loads((ROOT/'data'/chapter['solutions']).read_text())['solutions']
        chapters.append(dict(chapter,problems=sorted([p for p in problems if p['editorial_status']!='draft'],key=lambda p:p['order']),solutions={s['problem_id']:s for s in solutions}))
    return catalog,sources,chapters

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'html')
    args=parser.parse_args();output=args.output.resolve()
    errors,stats=validate()
    if errors:raise SystemExit('\n'.join(errors))
    if output==ROOT or any(output.is_relative_to(ROOT/d) for d in ('data','web','scripts','figures','schemas','skills','sources','docs','Doc')):
        parser.error('choose a dedicated output directory, not a source directory')
    marker=output/'.cwdata-html.json'
    if output.exists() and any(output.iterdir()) and not marker.exists():parser.error('output is nonempty and not owned by this HTML builder')
    catalog,sources,chapters=load_collection();r=Renderer()
    all_problems={p['id']:p for c in chapters for p in c['problems']}
    total=len(all_problems);open_count=sum(p['status']=='open' for p in all_problems.values())
    nav=[];cards=[];routes=[];figure_paths=set()
    def source_links(refs):
        parts=[]
        for sr in refs:
            source=sources[sr['source_id']];title=esc(source['title'])
            url=source['url']
            if url and urlparse(url).scheme in ('http','https'):title=f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{title}</a>'
            parts.append(f'<li>{title} ({source["year"]}) — {esc(sr["locator"])}</li>')
        return '<ul>'+''.join(parts)+'</ul>'
    def reveal(pid,kind,closed_label,open_label,content):
        control=f'{pid}-{kind}'
        return f'''<section class="reveal {kind}"><button type="button" class="reveal-button" aria-expanded="false" aria-controls="{control}" data-closed-label="{closed_label}" data-open-label="{open_label}"><span class="toggle-label">{closed_label}</span><span class="symbol" aria-hidden="true">+</span></button><div class="reveal-body {kind}-body" id="{control}" hidden>{content}</div></section>'''
    for c in chapters:
        cid=c['id'];number=c['order'];title=esc(c['title']);problems=c['problems']
        nav_items=[];problem_list=[]
        for i,p in enumerate(problems):
            pid=p['id'];pnum=f'{number}.{p["order"]}';ptitle=esc(p['title']);is_open=p['status']=='open'
            badge='<span class="badge open">Open question</span>' if is_open else '<span class="badge">Exercise</span>'
            search=' '.join([p['title'],pid,c['title'],*p['tags']])
            nav_items.append(f'<li class="problem-nav-item" data-search="{esc(search)}"><a href="#{pid}" data-route-link>{pnum} &nbsp;{ptitle}</a></li>')
            level=p['level'].replace('-',' ')
            problem_list.append(f'<li><a href="#{pid}"><span class="number">{pnum}</span><span class="problem-title">{ptitle}<span class="list-meta">{esc(level.capitalize())}{" · Open question" if is_open else ""}</span></span><span class="forward" aria-hidden="true">↗</span></a></li>')
            figures=[]
            for f in p['figures']:
                figure_paths.add(f['path'])
                figures.append(f'<figure><img src="{esc(f["path"])}" alt="{esc(f["alt"])}" loading="lazy"><figcaption>{r.md(f["caption_md"])}</figcaption></figure>')
            hint=p['hint_md'] or 'No hint has been added for this problem yet.'
            hint_title='Show starting point' if is_open else 'Show hint'
            hint_hide='Hide starting point' if is_open else 'Hide hint'
            s=c['solutions'][pid]
            solution_title='Show background / partial results' if is_open else 'Show solution'
            solution_hide='Hide background / partial results' if is_open else 'Hide solution'
            proof_note='' if is_open else f'<p class="proof-status">{esc(s["proof_status"].replace("-"," ").capitalize())}. {esc(s["checked_by"])}</p>'
            prerequisites=''
            if p['prerequisites']:
                prerequisites='<h2>Before this problem</h2><ul>'+''.join(f'<li><a href="#{dep}">{esc(all_problems[dep]["title"])}</a></li>' if dep in all_problems else f'<li>{esc(dep)} (not in this edition)</li>' for dep in p['prerequisites'])+'</ul>'
            status=''
            if is_open:
                o=p['open_status']
                status=f'<aside class="open-status"><strong>{"Local research question" if o["scope"]=="local-research" else "Literature conjecture"}</strong> · Checked {esc(o["last_checked"])}<br>{esc(o["evidence"])} {esc(o["qualification"])}</aside>'
            previous=f'<a href="#{problems[i-1]["id"]}"><small>← Previous problem</small>{esc(problems[i-1]["title"])}</a>' if i else f'<a href="#{cid}"><small>← Chapter overview</small>{title}</a>'
            following=f'<a href="#{problems[i+1]["id"]}"><small>Next problem →</small>{esc(problems[i+1]["title"])}</a>' if i+1<len(problems) else f'<a href="#{cid}"><small>Back to chapter →</small>{title}</a>'
            routes.append(f'''<article class="route problem" id="{pid}" data-title="{ptitle}" data-chapter="{cid}" data-chapter-number="{number}" data-problem-number="{pnum}" hidden>
<header class="problem-header"><div class="eyebrow">Chapter {number} · Problem {pnum}</div><h1>{ptitle}</h1><div class="meta">{badge}<span>{esc(level.capitalize())}</span><span>·</span><span>{esc(p['editorial_status'].replace('-',' ').capitalize())}</span></div></header>
<div class="statement">{r.md(p['statement_md'])}</div>{status}<div class="problem-figures">{''.join(figures)}</div>
{reveal(pid,'hint',hint_title,hint_hide,r.md(hint))}
{reveal(pid,'solution',solution_title,solution_hide,r.md(s['body_md'])+proof_note)}
<div class="supporting">{prerequisites}<h2>Sources</h2>{source_links(p['sources'])}<h2>Topics</h2><p>{' · '.join(esc(t.replace('-',' ')) for t in p['tags'])}</p></div><nav class="pager" aria-label="Adjacent problems">{previous}{following}</nav></article>''')
        nav.append(f'''<details class="tree-chapter" id="tree-{cid}"><summary><span class="chapter-number">{number:02}</span><span>{title}</span></summary><ol><li class="chapter-overview"><a href="#{cid}" data-route-link>Chapter overview</a></li>{''.join(nav_items)}</ol></details>''')
        cards.append(f'<a class="chapter-card" href="#{cid}"><span class="number">{number:02}</span><div><h3>{title}</h3><p>{len(problems)} {"open questions" if number==8 else "problems"} <span aria-hidden="true">↗</span></p></div></a>')
        routes.append(f'''<section class="route chapter" id="{cid}" data-title="{title}" data-chapter="{cid}" data-chapter-number="{number}" hidden><div class="eyebrow">Chapter {number:02}</div><h1>{title}</h1><p class="lede">{len(problems)} {"open questions. Explore starting points and background without implying a known solution." if number==8 else "problems. Open an exercise, try it yourself, then reveal a hint or solution when you choose."}</p><ol class="problem-list">{''.join(problem_list)}</ol><a href="#overview">← All chapters</a></section>''')
    # Reuse an existing exact geometry figure for the collection's identity.
    hero='figures/smooth-support.svg';figure_paths.add(hero)
    document=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="A chapter-based collection of constant-width geometry problems, with optional hints and solutions."><title>Shapes of constant width</title><link rel="stylesheet" href="assets/katex/katex.min.css"><link rel="stylesheet" href="assets/reader.css"><script defer src="assets/reader.js"></script></head><body>
<a class="skip-link" href="#content">Skip to reading area</a>
<aside class="sidebar" id="sidebar"><a class="brand" href="#overview"><svg class="brand-mark" viewBox="0 0 60 66" aria-hidden="true"><path d="M30 5 A52 52 0 0 1 56 50 A52 52 0 0 1 4 50 A52 52 0 0 1 30 5Z" fill="none" stroke="#286c59" stroke-width="2"/><path d="M30 5L56 50H4Z" fill="none" stroke="#9cae92" stroke-dasharray="3 4"/></svg><span><strong>Shapes of<br>constant width</strong><small>Problems &amp; ideas</small></span></a>
<div class="search"><label for="search">Find a problem</label><input id="search" type="search" placeholder="Title, chapter, or topic…" autocomplete="off" aria-controls="chapter-tree"><span id="search-status" role="status" class="list-meta"></span></div><nav class="chapter-tree" id="chapter-tree" aria-label="Chapters and problems">{''.join(nav)}<p id="no-results" class="empty-search" hidden>No matching problems. Try another topic.</p></nav><div class="sidebar-footer">{len(chapters)} chapters · {total} entries<br>Hints and solutions stay hidden until opened.</div></aside>
<div class="main"><header class="topbar"><button class="menu-button" type="button" id="menu-button" aria-controls="sidebar" aria-expanded="false">Chapters</button><nav class="breadcrumb" id="breadcrumb" aria-label="Breadcrumb"><span aria-current="page">Collection</span></nav><span class="edition">An introduction through exercises</span></header><main class="content" id="content" tabindex="-1">
<noscript><p>Please enable JavaScript for chapter navigation and the hint and solution buttons.</p></noscript>
<section class="route" id="overview" data-title="Collection"><div class="hero"><div><div class="eyebrow">The geometry of equal width</div><h1>One constraint.<br>A world of shapes.</h1><p class="lede">Explore constant-width geometry through short proofs, constructions, and open questions. Choose a chapter, work through a problem, and reveal just the help you need.</p><div class="stats"><span><strong>{len(chapters)}</strong>chapters</span><span><strong>{total-open_count}</strong>exercises</span><span><strong>{open_count}</strong>open questions</span></div></div><img src="{hero}" alt="A smooth noncircular constant-width curve between supporting lines."></div><div class="section-header"><h2>Explore the chapters</h2><span>From first principles to open problems</span></div><div class="chapter-grid">{''.join(cards)}</div><p class="review-note">A working collection based on Beniamin Bogosel’s book outline. Proofs are checked drafts awaiting human mathematical review. Open questions include dated status notes.</p></section>
{''.join(routes)}<section class="route" id="not-found" data-title="Page not found" hidden><div class="eyebrow">Unknown link</div><h1>This problem is not in the current edition.</h1><p>It may have been renamed or omitted as a draft.</p><a href="#overview">Return to the chapter index</a></section>
</main><footer class="page-footer">Shapes of constant width · {esc(catalog['updated'])} · An offline reading edition with optional hints and solutions.<br>{esc(catalog.get('credits_md', ''))}</footer></div></body></html>'''
    document=r.finish(document)
    output.mkdir(parents=True,exist_ok=True);(output/'assets').mkdir(exist_ok=True)
    for name in ('reader.css','reader.js'):shutil.copy2(ROOT/'web'/name,output/'assets'/name)
    shutil.copytree(ROOT/'web/vendor/katex',output/'assets/katex',dirs_exist_ok=True)
    for relative in figure_paths:
        source=safe_path(ROOT,relative);dest=safe_path(output,relative);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
    (output/'index.html').write_text(document)
    marker.write_text(json.dumps(dict(format='cwdata-html',version=1,problems=total,chapters=len(chapters),math_fragments=len(r.fragments)),indent=2)+'\n')
    print(f'Built {output / "index.html"}: {len(chapters)} chapters, {total} entries, {len(r.fragments)} rendered equations. Hints and solutions are hidden by default.')
if __name__=='__main__':main()
