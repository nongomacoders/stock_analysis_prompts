"""Offline completion accounting and preliminary checks; no paid calls."""
from pathlib import Path
import importlib.util
import json
import shutil
import sqlite3
import sys

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('comparison',HERE/'stage2_300k.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
m=t.m
def offline(event,args):
    if event in {'socket.connect','socket.getaddrinfo','socket.sendto'}:
        raise RuntimeError('Offline review: network disabled')
sys.addaudithook(offline)
run=Path(t.POINTER.read_text(encoding='utf-8').strip())
r=m.read(run/'receipts/stage2.json')
assert r.get('completed_utc'), 'Generation still running; no review yet'
assert r['max_tokens']==300000 and not r['reasoning_controls_sent']
assert m.read(run/'requests/stage2.json')==dict(m.read(t.OLD/'requests/stage2.json'),max_tokens=300000)
original=m.read(t.OLD/'receipts/stage2.json')
metrics=m.read(run/'metrics.json')
assert metrics['calls']==1
u=r.get('usage',{});g=r.get('generation_metadata',{})
cost=r.get('cost_usd')
if cost is not None and g.get('total_cost') is not None:
    assert abs(cost-g['total_cost'])<1e-9
c=m.ro(t.ROOT/'documents/analysis.sqlite'); dest=sqlite3.connect(run/'inputs/evaluator_snapshot.sqlite')
c.backup(dest);c.close();dest.close()
from evaluate_stock import StockEvaluator
e=StockEvaluator('NTU',period='1H26',db_path=run/'inputs/evaluator_snapshot.sqlite')
e.fetch_market_quote=lambda:dict(price_zar=None,source='No current quote requested; frozen R0.89 reference only')
note=run/'outputs/stage2.md'
result=e.audit(note_path=note)
m.save(run/'outputs/preliminary_evaluator.json',dict(result=result,network_disabled=True,scope='Script checks only; no independent financial validation'))
arithmetic=dict(principal_close=3975+382-728+383-167,other_close=702+28-116+30,
    net_portfolio_cash=728+116-382-28,portfolio_income=383-167+30,
    carrying_decline=4677-4489,statutory_movement=182)
arithmetic['unexplained_residual']=arithmetic['net_portfolio_cash']-arithmetic['portfolio_income']-182
assert arithmetic['unexplained_residual']==6
m.save(run/'outputs/independent_calculations.json',dict(values=arithmetic,
    basis='Inputs independently checked against identical-hash PDF pp12–13 in prior versioned Codex audit; reused here. No new PDF inspection. Forecast/valuation not verified.'))
comparison=dict(old={k:original.get(k) for k in ['id','finish_reason','elapsed_seconds','cost_usd','provider','max_tokens']},
    new={k:r.get(k) for k in ['id','finish_reason','elapsed_seconds','cost_usd','provider','max_tokens']},
    previous_completion_tokens=original['usage']['completion_tokens'],new_usage=u,
    identical_prompt=True,only_request_change='max_tokens=300000',
    conclusion='Generation completion is not financial validation; account/provider effective internal limits remain unverified.')
m.save(run/'comparison.json',comparison)
if note.exists():
    shutil.copy2(note,run/'inputs/stage2_review_subject.md')
    m.save(run/'inputs/output_manifest.json',dict(path=str(note),sha256=m.sha(note)))
    answer=note.read_text(encoding='utf-8')
    print('ANSWER_PREVIEW\n'+answer[:2200])
m.preserve(run)
with (run/'audit.md').open('a',encoding='utf-8',newline='') as f:
    f.write('\nOffline review: request equality/one-call accounting/source and production preservation checks passed. Preliminary StockEvaluator ran against explicit new note on a copied database with network disabled; see outputs/preliminary_evaluator.json. Historical bridge independently re-executed from prior verified inputs: net portfolio cash434 minus income246 equals carrying decline188; statutory182 leaves6 unexplained. See outputs/independent_calculations.json. No financial validation of Stage2 forecasts/valuation; Gemini review pending.\n')
print(json.dumps(dict(comparison=comparison,preliminary=result,preservation=m.read(run/'preservation.json')),ensure_ascii=False,indent=2))
