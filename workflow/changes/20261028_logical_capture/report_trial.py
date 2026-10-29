"""Finalize existing paid-trial receipts; run only offline preliminary financial checks."""
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sqlite3
import sys

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('trial',HERE/'trial.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
m=t.m;run=Path(t.POINTER.read_text(encoding='utf-8').strip());pilot=run/'pilot'
status=m.read(run/'status.json')
assert status['status'] in {'completed_awaiting_independent_review','stopped'},'Never finalize an active run'
from section_capture.openrouter import get_openrouter_api_key
key=get_openrouter_api_key()
for folder in [pilot,run]:
    for path in sorted((folder/'receipts').glob('*.json')):
        r=m.read(path)
        if r.get('completed_utc') and r.get('metadata_status')!='retrieved':
            m.metadata(folder,r['label'],r,key);m.save(path,r)
    m.summarize(folder);m.preserve(folder)
full=m.read(run/'metrics.json');small=m.read(pilot/'metrics.json')
all_rows=[dict(phase=phase,**r) for phase,metrics in [('pilot',small),('full',full)] for r in metrics['rows']]
known=sum(Decimal(str(r['cost_usd'])) for r in all_rows if r['cost_usd'] is not None)
receipt_checks=[]
for folder in [pilot,run]:
    for p in (folder/'receipts').glob('*.json'):
        r=m.read(p);payload=m.read(folder/'requests'/f'{r["label"]}.json')
        assert payload['model']==m.MODEL
        assert not {'max_tokens','max_completion_tokens','reasoning','reasoning_effort','provider','service_tier'} & payload.keys()
        g=r.get('generation_metadata') or {}
        if g.get('total_cost') is not None and r.get('cost_usd') is not None:
            assert abs(r['cost_usd']-g['total_cost'])<1e-9
        receipt_checks.append(dict(phase=folder.name,label=r['label'],cost_metadata_available=g.get('total_cost') is not None,
           cost_usd=r.get('cost_usd'),finish_reason=r.get('finish_reason')))
conn=m.ro(run/'experiment.sqlite')
rows=conn.execute('SELECT manifest_json,llm_response FROM sections ORDER BY section_number').fetchall()
manifests=[json.loads(r[0]) for r in rows]
assert [s['physical_page'] for x in manifests for s in x['selections']]==list(range(1,39))
assert sum(x.get('analysis_role')=='navigation_only' for x in manifests)==2
analyzed=sum(bool(r[1]) for r in rows)
questions=[json.loads(r[0]) for r in conn.execute('SELECT question_json FROM ledger_questions')]
validation=dict(conn.execute('SELECT validation_status,count(*) FROM section_response_attempts GROUP BY validation_status'))
conn.close()
m.save(run/'combined_metrics.json',dict(full=full,pilot=small,combined_known_cost_usd=str(known),
 missing_cost_calls=sum(r['cost_usd'] is None for r in all_rows),rows=all_rows,receipt_checks=receipt_checks,
 source_pages=38,capture_units=24,financial_capture_units=22,navigation_units=2,financial_analyses_saved=analyzed,
 ledger=dict(records=len(questions),statuses=dict(Counter(q['status'] for q in questions)),validation_attempts=validation)))

# From this point onward, prevent any accidental network request during evaluation.
def offline(event,args):
    if event in {'socket.connect','socket.getaddrinfo','socket.sendto'}:raise RuntimeError('Offline preliminary audit; no quote/model requests')
sys.addaudithook(offline)
if (run/'outputs/stage2_publication.md').exists() or status.get('stage')=='stage2':
    copy=m.ro(run/'experiment.sqlite');auditdb=sqlite3.connect(run/'inputs/evaluator_snapshot.sqlite')
    copy.backup(auditdb);copy.close();auditdb.close()
    from evaluate_stock import StockEvaluator
    evaluator=StockEvaluator('NTU',period='1H26',db_path=run/'inputs/evaluator_snapshot.sqlite')
    evaluator.s2_note_file=run/'outputs/stage2_publication.md'
    evaluator.fetch_market_quote=lambda:dict(price_zar=None,source='No live quote requested;0.89 is frozen reference only')
    result=evaluator.audit(note_path=run/'outputs/stage2_publication.md')
    m.save(run/'outputs/preliminary_evaluator.json',dict(result=result,method='StockEvaluator.audit(explicit experimental note)',
      network_disabled=True,live_quote_available=False,scope='Script checks, not independent financial validation'))

arithmetic=dict(poci_net=3414+431,principal_close=3975+382-728+383-167,other_close=702+28-116+30,
  portfolio_net_cash=728+116-382-28,portfolio_income=383-167+30,portfolio_decline=(3975+702)-(3845+644),
  residual_to_statutory=((728+116-382-28)-(383-167+30))-182,nonfinancial_receivables=497-(395-5),
  conventional_etr=(-29)/(-92)*100,fy25_historical_book_loss=77+182,amortisation=728-383+167+116-30,
  nav=1329/(780651033/1e6),cash_close=107-111-61+178)
assert arithmetic['portfolio_net_cash']-arithmetic['portfolio_income']==arithmetic['portfolio_decline']==188
assert arithmetic['residual_to_statutory']==6 and arithmetic['nonfinancial_receivables']==107
assert arithmetic['fy25_historical_book_loss']==259 and arithmetic['cash_close']==113
m.save(run/'outputs/independent_calculations.json',dict(source_basis='Original identical-hash NTU PDF,physical pp.8,9,12,13,16,22,24,31; source-transcribed inputs independently checked in prior Codex audit.',
 calculations=arithmetic,limits='Historical arithmetic only; no automatic validation of forecast assumptions or price.'))

review=run/'inputs/review_subject';review.mkdir(exist_ok=True)
subjects=[]
for folder in [run/'outputs',pilot/'outputs']:
    for path in sorted(folder.glob('*')):
        if path.suffix not in {'.md','.json'}:continue
        name=('pilot_' if folder.parent==pilot else 'full_')+path.name
        target=review/name
        if not target.exists():shutil.copy2(path,target)
        assert m.sha(target)==m.sha(path)
        subjects.append(dict(original=str(path.relative_to(run)),preserved=str(target.relative_to(run)),sha256=m.sha(path)))
m.save(run/'inputs/review_subject_manifest.json',dict(created_utc=m.utc(),files=subjects,source_documents=m.read(run/'plan.json')['documents']))
m.preserve(run);m.preserve(pilot)
outcome=m.read(run/'outputs/publication_assessment.json') if (run/'outputs/publication_assessment.json').exists() else dict(valuation_status='NOT_PUBLISHED_PROCESS_INCOMPLETE')
lines=['# NTU reviewed logical-capture trial','',f'Execution status: **{status["status"]}**. Stage2 publication status: **{outcome["valuation_status"]}**. Independent financial review remains pending.','',
 '24 captured units cover38 pages exactly once.22 financial units are analyzed in chronological order;2 navigation/contact units remain captured without standalone calls. Pilot and full ledgers are separate.',
 '', '| Phase | Generations | Successful | Cost USD | Input tokens | Completion tokens | Reasoning subset | First dispatch to last accounting | Summed request time |',
 '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for name,data in [('Pilot + scope recheck',small),('Full chronological run',full)]:
    a=data['totals'];lines.append(f'| {name} | {data["calls"]} | {data["successful_generations"]} | {a["cost_usd"]:.8f} | {a["prompt_tokens"]:,} | {a["completion_tokens"]:,} | {a["reasoning_tokens"]:,} | {data["observed_first_dispatch_to_last_accounting_seconds"]:.2f}s | {a["elapsed_seconds"]:.2f}s |')
lines += ['',f'**Combined known cost: USD{known}**; missing-cost calls:{sum(r["cost_usd"] is None for r in all_rows)}. Reasoning is already included in completion tokens.',
 '', 'The first pilot needed one quote repair and missed a secondary note on page25. One revised scope check then correctly included currency risk and continuation to26. All earlier outputs/charges remain preserved. The full run starts with a fresh ledger; pilot responses are intentionally not imported.',
 'Run-only prompt improvements: explicit secondary note headings, short literal evidence locators and a compact resolved-question index. Production guardrails/prompts/valuations were not rewritten.',
 '', 'Model: DeepSeek base snapshot,default thinking,normal routing; no requested token cap. Actual providers,finish reasons,usage,cost,cache and timing are in per-call receipts/CSV. Variable providers and multiple prompt/partition changes prevent isolated causal conclusions.',
 f'Full ledger: {len(questions)} records;{dict(Counter(q["status"] for q in questions))};validation attempts:{validation}. A literal quote does not by itself prove closure.',
 '', 'Prior versions used different evidence groupings and mixed retries; lower cost or better financial accuracy is not assumed from completion. Source PDF,all production tables and enumerated original outputs remain unchanged.',
 '', 'Artifacts: `REVIEWED_PLAN.md`, `combined_metrics.json`, `calls.csv`, `pilot/calls.csv`, exact `requests/outputs/receipts`, `inputs/review_subject_manifest.json`, `preservation.json`, and `gemini/PROMPT.md`.']
m.text(run/'RUN_SUMMARY.md','\n'.join(lines)+'\n')
m.text(run/'gemini/PROMPT.md',f'''Review the NTU1H26 logical-capture trial in Antigravity. Subject directory:{run}
ACTUAL OUTCOME:22 financial section analyses and Stage1 completed,with no full-run repairs. Stage2 failed at131072 reported completion tokens,all reasoning,with no final answer despite no caller-set cap. No new valuation/recovery brief exists. Do not confuse this process failure with a completed financial WITHHELD decision. Grade absent Stage2 schedules NOT APPLICABLE/NOT VERIFIED,not PASS. Inspect outputs/codex_stage1_findings.json:Stage1 introduces an unsupportedR370m cash difference; source decline188 versus statutory182 leaves6. Test this independently and do not infer it caused token exhaustion.
Read AGENTS.md,workflow/STATE.md,workflow/WORKFLOW.md,TOOL_CHEATSHEET.md and docs/STOCK_EVALUATION_FORMAT.md section1A. Save your audit,exact inputs/hashes,independent executable calculations/results,C/F register,coverage and limitations under a NEW UTC-versioned Gemini evaluation directory. No paid model calls,production writes or automatic guardrail codification.
Start with REVIEWED_PLAN.md,RUN_SUMMARY.md,plan.json,combined_metrics.json,per-call CSV/receipts,pilot semantic reviews and preservation.json.24 capture units cover38 pages;22 financial units are analyzed and2 navigation/contact units captured without standalone calls. Full ledger starts fresh in source order. Pilot initial page25 response omitted currency risk; the revised scope check fixed this. All original failures/repairs and cost are preserved. Do not treat repaired-only output as the original answer.
Inspect exact full section answers,ledger,Stage1,raw Stage2,publication assessment and preliminary evaluator output. Script success and literal quote matching do not validate financial truth or closure. Source PDF:{m.read(run/'plan.json')['documents'][0]['path']};SHA256:{m.SHA};38 physical pages. Reopen actual PDF tables/images; raw text ingestion does not count as independent image inspection. R0.89 is frozen,not current.
Check captured financial coverage,secondary shared-page note starts/continuations,POCI signed gain,FVTPL classification,both portfolio rollforwards and net-cash/accounting-income bridge,remaining6 residual,gross/net receivables107,ETR signs,closing/weighted-average shares,FY25 historical loss259,facility/covenant/renewal scope,conditional simplified ECL and NCA/ABS applicability. Test ledger semantic closures and duplicate/reopened questions. Reconcile any actual forecasts/DCF/sensitivity/terminal financing; unperformed checks are NOT APPLICABLE,not repaired/PASS. Review blocker materiality and permissible supported analyst assumptions rather than requiring management forecasts categorically.
Compare with preserved prior NTU evaluations,including 20261028T114521Z_deepseek_default_no_requested_cap. Discuss generation completeness,financial quality,coverage,cost and time separately. Models/providers/prompts/groupings changed; no isolated causal speed/quality claim. Do not publish an unsupported replacement target/rating. Record fixed,remaining and new errors,plus prioritized prompts/ledger improvements and conditional guardrails for user approval. Codex will independently review your saved Gemini audit.
''')
m.save(run/'completion_record.json',dict(recorded_utc=m.utc(),execution_status=status,publication_status=outcome['valuation_status'],
 full_cost_usd=str(full['totals']['cost_usd']),pilot_cost_usd=str(small['totals']['cost_usd']),combined_known_cost_usd=str(known),
 accepted_financial_captures=analyzed,financial_captures=22,navigation_captures=2,source_pages=38,
 paid_gemini_calls=0,preservation=m.read(run/'preservation.json'),independent_review='Preliminary Codex audit and manual Gemini review pending'))
print(json.dumps(dict(full_calls=full['calls'],pilot_calls=small['calls'],full_totals=full['totals'],pilot_totals=small['totals'],combined_cost_usd=str(known),full_wall_seconds=full['observed_first_dispatch_to_last_accounting_seconds'],publication=outcome['valuation_status'],execution=status['status'])))
