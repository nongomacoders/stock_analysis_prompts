"""Offline checks for accounting/default settings and failure preservation."""
import importlib.util
import io
import json
from pathlib import Path
import sqlite3
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('ntu_runner',HERE/'rerun.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

payload=m.request_payload('Evidence',32768)
assert payload['model']=='deepseek/deepseek-v4.1-flash-1017'
assert not {'reasoning','reasoning_effort','provider','service_tier'} & payload.keys()
assert payload['stream'] is True

def sse(finish):
    events=[dict(id='gen-offline',model=m.MODEL,choices=[dict(delta=dict(reasoning='DO NOT SAVE THIS',content='Visible answer'))]),
            dict(id='gen-offline',choices=[dict(delta={},finish_reason=finish)],usage=dict(prompt_tokens=10,completion_tokens=8,total_tokens=18,cost=0.001,completion_tokens_details=dict(reasoning_tokens=3)))]
    return io.BytesIO(('\n'.join('data: '+json.dumps(x)+'\n' for x in events)+'data: [DONE]\n').encode())
r={};assert m.parse_stream(sse('stop'),r)=='Visible answer'
assert r['usage']['cost']==0.001 and r['id']=='gen-offline' and r['stream_done']
assert 'DO NOT SAVE THIS' not in json.dumps(r)

# Exercise the actual call/finally path on an incomplete response; no real API key/request.
case=HERE/'offline_check'
case.mkdir(exist_ok=True)
for folder in ['requests','outputs','receipts']: (case/folder).mkdir(exist_ok=True)
assert not (case/'receipts/failure.json').exists(),'Use a fresh offline-check case'
m.save(case/'status.json',dict(status='prepared',calls=0))
class Response:
    status=200
    def __enter__(self): return self
    def __exit__(self,*args): pass
    def __iter__(self): return iter(sse('length'))
def stats(run,label,receipt,key):
    receipt['metadata_status']='retrieved'
    receipt['generation_metadata']=dict(total_cost=0.001,native_tokens_prompt=10,native_tokens_completion=8,native_tokens_reasoning=3)
with patch('section_capture.openrouter.get_openrouter_api_key',return_value='offline-dummy'),patch.object(m.urllib.request,'urlopen',return_value=Response()),patch.object(m,'metadata',side_effect=stats):
    try: m.call(case,'failure','Evidence',32768)
    except m.Incomplete: pass
    else: raise AssertionError('Truncated response accepted')
receipt=m.read(case/'receipts/failure.json')
assert not receipt['success'] and receipt['finish_reason']=='length'
assert receipt['id']=='gen-offline' and receipt['cost_usd']==0.001
assert (case/'outputs/failure.partial.md').exists() and not (case/'outputs/failure.md').exists()
metrics=m.read(case/'metrics.json')
assert metrics['totals']['completion_tokens']==8 and metrics['totals']['reasoning_tokens']==3
assert metrics['rows'][0]['estimated_nonreasoning_completion_tokens']==5
assert 'DO NOT SAVE THIS' not in (case/'receipts/failure.json').read_text(encoding='utf-8')

c=sqlite3.connect(':memory:');c.execute('create table t(a)');c.execute('insert into t values(1)')
first=m.snap(c);c.row_factory=sqlite3.Row;assert first==m.snap(c);c.close()
m.save(HERE/'offline_checks.json',dict(passed=True,checks=['base model/default controls','stream usage/ID capture','raw reasoning omitted','incomplete call persisted before failure','failed-call cost counted','reasoning subset not double counted','logical snapshot stable across row factories'],network_calls=0))
print('Seven offline runner checks passed; no network requests.')
