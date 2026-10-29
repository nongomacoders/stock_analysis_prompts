from pathlib import Path
import ast

for name in ['test_portfolio_valuation.py','test_capture.py','test_one_shot_pipeline.py']:
 p=Path('tests')/name
 raw=p.read_bytes();text=raw.decode('utf-8-sig');raw=text.encode('utf-8')
 lines=raw.splitlines(keepends=True); offsets=[];total=0
 for line in lines:offsets.append(total);total+=len(line)
 replacements=[]
 tree=ast.parse(text)
 for node in ast.walk(tree):
  if not isinstance(node,ast.Call) or not isinstance(node.func,ast.Name) or node.func.id!='save_stage2_report':continue
  value=next((x.value for x in node.keywords if x.arg=='response'),None)
  if value is None and len(node.args)>2:value=node.args[2]
  if value is None:continue
  a=offsets[value.lineno-1]+value.col_offset;b=offsets[value.end_lineno-1]+value.end_col_offset
  suffix=b')'
  if name=='test_capture.py' and isinstance(value,ast.Name) and value.id=='baseline_note':suffix=b", target_price_zar=.21, recommendation='SELL')"
  elif name=='test_capture.py' and isinstance(value,ast.Constant) and '112' in str(value.value):suffix=b", target_price_zar=112, recommendation='BUY')"
  replacements.append((a,b,b'ready_note('+raw[a:b]+suffix))
 for a,b,value in sorted(replacements,reverse=True):raw=raw[:a]+value+raw[b:]
 text=raw.decode('utf-8')
 marker='from __future__ import annotations\n'
 if marker in text:text=text.replace(marker,marker+'\nfrom valuation_examples import ready_note\n',1)
 else:text='from valuation_examples import ready_note\n'+text
 if name=='test_portfolio_valuation.py':text=text.replace('assert \'"target_price_zar": 0.00\' in prompt','assert \'"target_price_zar": null\' in prompt',1)
 if name=='test_one_shot_pipeline.py':
  text=text.replace('self.finished_query.emit(resp,', "self.finished_query.emit(ready_note(resp) if 'target_price_zar' in resp else resp,")
  text=text.replace('fixed = sanitize_stage2_valuation_markdown(bad_note,','fixed = sanitize_stage2_valuation_markdown(ready_note(bad_note),',1)
 p.write_text(text,encoding='utf-8')
print('Positive synthetic fixtures now supply explicit readiness checks; legacy-read tests retained.')
