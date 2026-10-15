#!/usr/bin/env python3
"""Validate schemas, references, proof/open status, prerequisite graph, and assets."""
import argparse
import json
from pathlib import Path
from collections import Counter
from datetime import date
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from review_status import FINGERPRINT_VERSION,build_snapshot,relative_path
ROOT=Path(__file__).resolve().parents[1]

def read(path):return json.loads(path.read_text())
def safe_path(root,relative):
 p=(root/relative).resolve()
 if not p.is_relative_to(root.resolve()):raise ValueError(f'path escapes root: {relative}')
 return p

def validate(root=ROOT,strict=False):
 errors=[];registry=Registry()
 schemas={}
 for p in (root/'schemas').glob('*.schema.json'):
  schema=read(p);Draft202012Validator.check_schema(schema)
  registry=registry.with_resource(schema['$id'],Resource.from_contents(schema));schemas[p.stem.split('.')[0]]=schema
 def check(kind,path):
  try:
   data=read(path)
   schema_errors=list(Draft202012Validator(schemas[kind],registry=registry,format_checker=FormatChecker()).iter_errors(data))
   for e in schema_errors:
    errors.append(f'{path.relative_to(root)} {list(e.absolute_path)}: {e.message}')
   if schema_errors:return {}
   return data
  except (OSError,ValueError) as e:errors.append(str(e));return {}
 catalog=check('catalog',root/'data/catalog.json');sources=check('sources',root/'data/sources.json').get('sources',[])
 source_ids=[s['id'] for s in sources]
 if len(source_ids)!=len(set(source_ids)):errors.append('duplicate source IDs')
 problems={};solutions={};all_orders=[];chapter_ids=[]
 for ch in catalog.get('chapters',[]):
  chapter_ids.append(ch['id']);all_orders.append(ch['order'])
  try:pp=safe_path(root/'data',ch['problems']);sp=safe_path(root/'data',ch['solutions'])
  except ValueError as e:errors.append(str(e));continue
  pd=check('problems',pp);sd=check('solutions',sp)
  if pd.get('chapter_id')!=ch['id'] or sd.get('chapter_id')!=ch['id']:errors.append(f'chapter envelope mismatch {ch["id"]}')
  orders=[]
  for p in pd.get('problems',[]):
   pid=p['id'];orders.append(p['order'])
   if pid in problems:errors.append(f'duplicate problem {pid}')
   problems[pid]=p
   if p.get('chapter_id')!=ch['id']:errors.append(f'wrong chapter for {pid}')
   for f in p.get('figures',[]):
    try:
     if not safe_path(root,f['path']).is_file():errors.append(f'missing figure {f["path"]}')
    except ValueError as e:errors.append(str(e))
   if strict and p.get('editorial_status')!='reviewed':errors.append(f'{pid}: human editorial review required by --strict')
   if p.get('status')=='open':
    try:
     if date.fromisoformat(p['open_status']['last_checked'])>date.fromisoformat(catalog['updated']):errors.append(f'{pid}: status date exceeds catalog date')
    except (ValueError,KeyError):pass # schema error already records this
  if len(orders)!=len(set(orders)):errors.append(f'duplicate problem order in {ch["id"]}')
  for s in sd.get('solutions',[]):
   pid=s['problem_id']
   if pid in solutions:errors.append(f'duplicate solution {pid}')
   solutions[pid]=s
   if pid not in {p['id'] for p in pd.get('problems',[])}:errors.append(f'{pid}: solution is in wrong chapter')
 if len(chapter_ids)!=len(set(chapter_ids)) or len(all_orders)!=len(set(all_orders)):errors.append('duplicate chapter IDs or ordering')
 if set(problems)!=set(solutions):errors.append(f'problem/solution mismatch: {set(problems)^set(solutions)}')
 for pid,p in problems.items():
  for d in p.get('prerequisites',[]):
   if d not in problems:errors.append(f'{pid}: missing prerequisite {d}')
   elif problems[d]['status']=='open':errors.append(f'{pid}: cannot assume an open question as a prerequisite')
  s=solutions.get(pid,{})
  if p['status']=='open' and (s.get('kind')!='discussion' or s.get('proof_status')!='not-applicable'):errors.append(f'{pid}: open problem must have background discussion, not a proof')
  if p['status']=='solved' and (s.get('kind')!='proof' or s.get('proof_status') not in ('checked-draft','human-reviewed')):errors.append(f'{pid}: solved status requires a checked proof draft')
  for sr in p.get('sources',[])+s.get('sources',[]):
   if sr['source_id'] not in source_ids:errors.append(f'{pid}: missing source {sr["source_id"]}')
 state={}
 def visit(pid,chain):
  if state.get(pid)==1:errors.append('prerequisite cycle: '+' -> '.join(chain+[pid]));return
  if state.get(pid)==2 or pid not in problems:return
  state[pid]=1
  for dep in problems[pid].get('prerequisites',[]):visit(dep,chain+[pid])
  state[pid]=2
 for pid in problems:visit(pid,[])
 # Reviews describe content versions, not an authoring or human-approval gate.
 # Missing records and changed content are valid, pending-review states.
 ledger={'schema_version':'1.0','fingerprint_version':FINGERPRINT_VERSION,'reviews':{}}
 if (root/'data/reviews.json').exists():
  checked=check('reviews',root/'data/reviews.json')
  if checked:ledger=checked
 for pid,record in ledger['reviews'].items():
  try:relative_path(root,record['report'])
  except ValueError as e:errors.append(f'{pid}: {e}')
 review_stats=build_snapshot(problems,solutions,ledger)['summary']
 return errors,dict(problems=len(problems),solutions=len(solutions),chapters=len(chapter_ids),sources=len(sources),statuses=dict(Counter(p['status'] for p in problems.values())),illustrated=sum(bool(p.get('figures')) for p in problems.values()),reviews=review_stats)
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--strict',action='store_true');parser.add_argument('--root',type=Path,default=ROOT);args=parser.parse_args()
 errors,stats=validate(args.root,args.strict)
 print(json.dumps(stats,indent=2))
 if errors:
  print('\n'.join(errors));raise SystemExit(1)
 print('Validation passed. Schema validation does not establish mathematical correctness.')
