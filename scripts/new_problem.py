#!/usr/bin/env python3
"""Add a draft problem and paired solution without hand-escaping LaTeX in JSON."""
import argparse
import json
import re
from pathlib import Path
from datetime import date
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--chapter',required=True);p.add_argument('--slug',required=True);p.add_argument('--title',required=True)
 p.add_argument('--source',default='editorial');p.add_argument('--locator',default='New exercise; add precise provenance before review.')
 p.add_argument('--statement-file',type=Path);p.add_argument('--solution-file',type=Path);p.add_argument('--open',action='store_true');p.add_argument('--root',type=Path,default=ROOT)
 args=p.parse_args();root=args.root
 if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',args.slug):p.error('slug must use lowercase letters, numbers, and single hyphens')
 catalog=json.loads((root/'data/catalog.json').read_text());matches=[c for c in catalog['chapters'] if c['id']==args.chapter]
 if not matches:p.error('unknown chapter; use its full ID from data/catalog.json')
 source_ids={s['id'] for s in json.loads((root/'data/sources.json').read_text())['sources']}
 if args.source not in source_ids:p.error('register the source in data/sources.json first')
 pid='cw-'+args.slug
 for c in catalog['chapters']:
  if any(x['id']==pid for x in json.loads((root/'data'/c['problems']).read_text())['problems']):p.error('problem ID already exists')
 ch=matches[0];pp=root/'data'/ch['problems'];sp=root/'data'/ch['solutions'];pd=json.loads(pp.read_text());sd=json.loads(sp.read_text())
 sr=[dict(source_id=args.source,locator=args.locator,relationship='original-exercise' if args.source=='editorial' else 'adapted')]
 problem=dict(id=pid,title=args.title,chapter_id=args.chapter,order=max([x['order'] for x in pd['problems']],default=0)+1,status='open' if args.open else 'exercise',editorial_status='draft',level='undergraduate',tags=['unclassified'],statement_md=args.statement_file.read_text().strip() if args.statement_file else 'Write the standalone statement, including hypotheses.',hint_md='',prerequisites=[],sources=sr,figures=[])
 if args.open:problem['open_status']=dict(scope='local-research',last_checked=catalog['updated'],evidence='Draft: supply a dated source and actual status check.',qualification='Unverified draft; do not present as a confirmed open problem.')
 solution=dict(problem_id=pid,kind='discussion' if args.open else 'proof',body_md=args.solution_file.read_text().strip() if args.solution_file else 'Write the proof or background discussion; identify any assumed theorem.',proof_status='not-applicable' if args.open else 'incomplete',checked_by='Not yet checked',sources=sr)
 pd['problems'].append(problem);sd['solutions'].append(solution)
 # Serialize both before either write; no evaluation of supplied Markdown.
 payloads=[(pp,json.dumps(pd,ensure_ascii=False,indent=2)+'\n'),(sp,json.dumps(sd,ensure_ascii=False,indent=2)+'\n')]
 for path,text in payloads:path.with_suffix('.json.tmp').write_text(text)
 for path,_ in payloads:path.with_suffix('.json.tmp').replace(path)
 print(f'Created {pid}\n{pp}\n{sp}\nComplete the draft, then run scripts/validate.py.')
if __name__=='__main__':main()
