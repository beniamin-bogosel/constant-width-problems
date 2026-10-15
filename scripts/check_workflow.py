#!/usr/bin/env python3
"""Exercise schema failures and the authoring workflow in temporary copies."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from validate import ROOT,validate

def main():
 with tempfile.TemporaryDirectory(prefix='cwdata-check-') as temp:
  root=Path(temp)
  for name in ('data','schemas','figures'):shutil.copytree(ROOT/name,root/name)
  errors, initial_stats = validate(root)
  assert not errors
  p=root/'data/chapters/01-generalities/problems.json';original=p.read_text()
  def mutated(change,needle):
   data=json.loads(original);change(data);p.write_text(json.dumps(data));errors,_=validate(root)
   assert any(needle in e for e in errors),(needle,errors)
   p.write_text(original)
  mutated(lambda d:d['problems'][0].pop('title'),'title')
  mutated(lambda d:d['problems'][0]['prerequisites'].append('cw-missing'),'missing prerequisite')
  mutated(lambda d:d['problems'][0]['prerequisites'].append(d['problems'][0]['id']),'prerequisite cycle')
  mutated(lambda d:d['problems'][0]['sources'][0].update(source_id='missing'),'missing source')
  mutated(lambda d:d['problems'][0].update(figures=[dict(figure_id='missing',path='../escape.svg',caption_md='Test',alt='Test')]),'path escapes root')
  statement=root/'statement.md';statement.write_text(r'Show $h(\theta)+h(\theta+\pi)=1$.')
  solution=root/'solution.md';solution.write_text('A test draft; no proof is asserted.')
  command=[sys.executable,str(ROOT/'scripts/new_problem.py'),'--root',str(root),'--chapter','01-generalities','--slug','workflow-example','--title','Workflow example','--statement-file',str(statement),'--solution-file',str(solution)]
  subprocess.run(command,check=True,capture_output=True,text=True)
  errors,stats=validate(root);assert not errors,errors;assert stats['problems']==initial_stats['problems']+1
  data=json.loads(p.read_text());assert data['problems'][-1]['statement_md']==statement.read_text()
  assert subprocess.run(command,capture_output=True).returncode!=0
  assert any('review required' in x for x in validate(root,strict=True)[0])
 print('Workflow checks passed: malformed input, references, cycles, asset paths, safe LaTeX import, duplicate ID rejection, review gate.')
if __name__=='__main__':main()
