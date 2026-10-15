#!/usr/bin/env python3
"""Export a validated reading copy and portable website data; no hosting or build framework."""
import argparse
import json
import shutil
from pathlib import Path
from validate import ROOT,validate

def dump(path,data):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/'build/reading');parser.add_argument('--include-solutions',action='store_true');args=parser.parse_args()
 errors,stats=validate()
 if errors:raise SystemExit('\n'.join(errors))
 out=args.output.resolve()
 # Never delete or overwrite the authoritative data through a mistaken output path.
 if out==ROOT or out==ROOT/'data' or out.is_relative_to(ROOT/'data'):parser.error('output must not be the repository root or authoritative data directory')
 if out.exists() and any(out.iterdir()) and not (out/'.cwdata-export.json').exists():parser.error('output is nonempty and was not created by this exporter; choose an empty directory')
 out.mkdir(parents=True,exist_ok=True)
 dump(out/'.cwdata-export.json',dict(format='cwdata-reading-export',version=1))
 catalog=json.loads((ROOT/'data/catalog.json').read_text());sources=json.loads((ROOT/'data/sources.json').read_text());bib={s['id']:s for s in sources['sources']}
 index=['# '+catalog['title'],'',catalog['notation_md'],'','All proofs are checked drafts awaiting human mathematical review. Open entries contain background discussion.','']
 if catalog.get('credits_md'):index += [catalog['credits_md'],'']
 public_catalog=json.loads(json.dumps(catalog));search=[]
 for ch,public_ch in zip(catalog['chapters'],public_catalog['chapters']):
  pd=json.loads((ROOT/'data'/ch['problems']).read_text());sd=json.loads((ROOT/'data'/ch['solutions']).read_text());solutions={s['problem_id']:s for s in sd['solutions']}
  pd['problems']=[p for p in pd['problems'] if p['editorial_status']!='draft']
  lines=['# '+ch['title'],''];answer=['# '+ch['title']+' — solutions and background','']
  for p in pd['problems']:
   lines += [f'## {p["order"]}. {p["title"]}',f'<a id="{p["id"]}"></a>','',f'`{p["id"]}` · {p["status"]} · {p["level"]} · {p["editorial_status"]}','',p['statement_md'],'']
   if p['prerequisites']:lines+=['Prerequisites: '+', '.join('`'+x+'`' for x in p['prerequisites'])+'.','']
   for f in p['figures']:lines += [f'![{f["alt"]}](../{f["path"]})','',f['caption_md'],'']
   if p['hint_md']:lines+=['Hint: '+p['hint_md'],'']
   if p['status']=='open':
    st=p['open_status'];lines += [f'Status checked {st["last_checked"]} ({st["scope"]}): {st["evidence"]} {st["qualification"]}','']
   refs=[]
   for sr in p['sources']:
    s=bib[sr['source_id']];label=f'{s["title"]} ({s["year"]})';refs.append((f'[{label}]({s["url"]})' if s['url'] else label)+' — '+sr['locator'])
   lines+=['Sources: '+'; '.join(refs)+'.','']
   if args.include_solutions:lines += [f'[Proof / background](../solutions/{ch["id"]}.md#{p["id"]})','']
   s=solutions[p['id']];answer += [f'## {p["order"]}. {p["title"]}',f'<a id="{p["id"]}"></a>','',s['body_md'],'',f'Proof status: {s["proof_status"]}.','']
   search.append(dict(id=p['id'],chapter_id=p['chapter_id'],title=p['title'],status=p['status'],tags=p['tags'],level=p['level']))
  md=out/'problems'/f'{ch["id"]}.md';md.parent.mkdir(exist_ok=True);md.write_text('\n'.join(lines)+'\n')
  solution_link=f' · [Solutions / background](solutions/{ch["id"]}.md)' if args.include_solutions else ''
  index += [f'- [{ch["order"]}. {ch["title"]}](problems/{ch["id"]}.md) ({len(pd["problems"])} entries){solution_link}']
  dump(out/'site-data/data'/ch['problems'],pd)
  if args.include_solutions:
   path=out/'solutions'/f'{ch["id"]}.md';path.parent.mkdir(exist_ok=True);path.write_text('\n'.join(answer)+'\n')
   sd['solutions']=[solutions[p['id']] for p in pd['problems']];dump(out/'site-data/data'/ch['solutions'],sd)
  else:public_ch.pop('solutions',None)
 # A dedicated exported directory can be refreshed without stale spoiler files.
 if not args.include_solutions:
  if (out/'solutions').is_dir():shutil.rmtree(out/'solutions')
  for stale in (out/'site-data/data/chapters').glob('*/solutions.json'):stale.unlink()
 (out/'INDEX.md').write_text('\n'.join(index)+'\n')
 dump(out/'site-data/data/catalog.json',public_catalog);dump(out/'site-data/data/sources.json',sources);dump(out/'site-data/data/search-index.json',dict(schema_version='1.0',problems=search))
 for target in (out/'figures',out/'site-data/figures'):
  target.mkdir(parents=True,exist_ok=True)
  for path in (ROOT/'figures').iterdir():
   if path.suffix in ('.svg','.png'):shutil.copy2(path,target/path.name)
 print(f'Exported {len(search)} entries to {out}; solutions included: {args.include_solutions}')
if __name__=='__main__':main()
