"""Save measured outcomes and a bounded independent audit; never submit models."""
from pathlib import Path
import json, hashlib, shutil, importlib.util, sys
from datetime import datetime, timezone
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
run=Path((HERE/'pilot_run.txt').read_text().strip())
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(v,encoding='utf-8')
plan=read(run/'plan.json');metrics=read(run/'metrics.json');validations=read(run/'validations.json')
assert metrics['calls']==metrics['successful_generations']==5
assert len(validations)==5 and all(v['ledger_valid'] for v in validations)
ids=[r['generation_id'] for r in metrics['rows']];assert len(set(ids))==5
assert all('fireworks' in r['provider'].lower() and r['finish_reason']=='stop' for r in metrics['rows'])
assert all(r['metadata_status']=='retrieved' for r in metrics['rows'])
old=(HERE/'before_question_ledger.py').read_text(encoding='utf-8')
new=(ROOT/'section_capture/question_ledger.py').read_text(encoding='utf-8')
assert old.split('\ndef apply_delta',1)[1]==new.split('\ndef apply_delta',1)[1]
for name in ['initial','target','target2','full']:
    source=ROOT/'tmp'/f'table_extraction_{name}_20261028-result.json'
    destination=HERE/f'{name}_test_result.json'
    if source.exists():shutil.copy2(source,destination)
    else:assert destination.exists()
calculations={
 'ntu_financial_assets':dict(expression='5 + 390 + 3845 + 644',calculated=5+390+3845+644,reported=4884),
 'ntu_principal_book':dict(expression='3975 + 382 - 728 + 383 - 167',calculated=3975+382-728+383-167,reported=3845),
 'ntu_other_assets':dict(expression='702 + 28 - 116 + 30',calculated=702+28-116+30,reported=644),
 'ntu_impairment_movement':dict(expression='-241 + 69 + 4 + 1',calculated=-241+69+4+1,reported=-167),
 'ntu_impairment_balance':dict(expression='598 - 167',calculated=598-167,reported=431),
 'ntu_ebitda_offline_only':dict(expression='-63 - 29 + 68 + 597 + 1 + 216',calculated=-63-29+68+597+1+216,reported=790),
 'pan_fy25_disjoint_production':dict(expression='92643 + 2654 + 98636 + 1081 + 1513',calculated=92643+2654+98636+1081+1513,reported=196527),
 'pan_fy25_model_overlap':dict(expression='93724 + 2654 + 98636 + 1081 + 1513',calculated=93724+2654+98636+1081+1513,reported=196527),
 'pan_fy26_group_production':dict(expression='105478 + 2428 + 113613 + 18667 + 32124',calculated=105478+2428+113613+18667+32124,reported=272310),
}
for c in calculations.values():c['residual']=c['calculated']-c['reported']
save(run/'calculations.json',calculations)
findings=[
 dict(id='F001',verdict='SUPPORTED WITHIN SAMPLE',origin='native PDF extraction',evidence='NTU physical22 and 24, exact re-extracted capture inputs',finding='5 and 390 remain separate; wrapped Unsecured/Debt review/Retail/Secured headings align. Asset sample reads 4884 and distinct 5/390; prior false 9879 allegation absent.',limit='Five selected captures; no general arbitrary-table guarantee.'),
 dict(id='F002',verdict='SUPPORTED WITHIN SAMPLE',origin='native PDF extraction/model interpretation',evidence='NTU physical25 and outputs/ntu_fx.md',finding='Closing USD 17.2/18.4/17.3 and GBP 22.7/23.9/23.2 assigned to March26/March25/September25 respectively. Secondary currency topic retained.',limit='No continuation26 or hedge valuation review.'),
 dict(id='F003',verdict='SUPPORTED WITHIN SAMPLE',origin='extraction and evidence-anchor prompt',evidence='outputs/*.validation.json',finding='Five complete generations and five valid deltas. Prose baseline section13 previously rejected; new prose delta validates and retains partial PBD question rather than premature full resolution.',limit='Extraction plus anchor wording changed; no causal isolation, retries or complete chronological ledger run. Literal validation does not prove answers or closure.'),
 dict(id='F004',verdict='CORRECTIONS REQUIRED',origin='section model output',evidence='NTU physical24 and outputs/ntu_headers.md',finding='Still calls 167 impairment loss a release and asks about sustainability of that release; 598-167=431 is a reduction in cumulative gain. Calling +69 Debt review directionally consistent with payer drop-offs is unsupported; management describes aggregate historical-book deterioration.',correction='Retain signed loss/gain meaning, distinguish overall loss from +24 acquired-book gain and -191 historical-book loss. Do not infer portfolio driver attribution.'),
 dict(id='F005',verdict='CORRECTIONS REQUIRED',origin='native grouped header extraction and model scope selection',evidence='PAN physical48/49 and outputs/pan_dense.md',finding='Adjacent tailings tonne cells now distinct, but multi-level parent labels remain imperfect. Model adds FY25 group underground93724 (already includes1081 buy-in) and buy-in1081 again, producing197608 versus196527. Disjoint mining underground92643 reconciles exactly.',correction='Use disjoint scopes or show alternatives; no issuer-error conclusion from this model overlap. Preserve genuine FY26 one-ounce subtotal difference.'),
 dict(id='F006',verdict='NOT VERIFIED',origin='section model inference',evidence='PAN physical49 and outputs/pan_dense.md',finding='Model speculates Tennant FY25 A$ all-in cost is a printing/scale error and cost-conversion residuals are likely conventions. Source prints these values, but causes are not established from this capture.',correction='Ask for definitions, scope, cost components and production denominator; do not label source error or explain residual without evidence.'),
 dict(id='F007',verdict='PARTLY SUPPORTED',origin='ledger semantic closure',evidence='inputs/ntu_assets.json Q-08aa5c3f257440ab; outputs/ntu_assets.md',finding='Measurement basis answer supported, but model marks question resolved while acknowledging total PBD scope reconciliation remains open under a new question. Original closure requires carrying-value reconciliation.',correction='Keep partial until principal plus other assets ties to total scope; valid evidence anchors alone cannot establish closure.'),
]
save(run/'findings.json',findings)
metrics['notes']=[n for n in metrics['notes'] if not n.startswith('Provider/account routing')]
metrics['notes']+=['Fireworks only, fallback disabled; none reasoning explicitly requested; no Nitro/speed override.','Five independent selected cases; not a chronological rerun or a controlled cost/accuracy benchmark.']
save(run/'metrics.json',metrics)
audit=f'''# Native extraction fix: limited independent audit

Evaluator: Codex. Recorded {datetime.now(timezone.utc).isoformat()}; local timezone Africa/Johannesburg (UTC+02:00).
Decision: **extraction improvement supported within selected coverage; model corrections still required**. Section-only engineering pilot; no valuation requested or validated.

## Implemented change
Numeric body anchors and native vertical rules separate nearby cells, wrapped headings map by overlap, broad prose is excluded from column inference, and paragraphs are emitted as prose. No company-specific extraction rules. The ledger prompt asks for short literal cell/sentence anchors; apply_delta and its atomic validation are byte-for-byte unchanged from the preserved function baseline. No dependency additions.

## Evidence and measurements
Original NTU and PAN PDF SHA-256 verified before export and after generation. Full-page before/after corpus: NTU9,13,18,22,24,25,30,31; PAN4,38,39,48,49,50. Offline extraction coverage is not full financial verification. Independently viewed original physical NTU22,24,25 and PAN48,49 this turn; retained renders in workflow/changes/20261028_table_extraction/renders. Read new answers and validation states for all five samples. NTU13/21/23/31 and PAN50 checked as extracted text, not newly visually audited. Unread remainder and external disclosures are NOT VERIFIED. Prior review/source images remain preserved.

All five selected calls complete, all five deltas syntactically/evidentially valid. Fireworks only, DeepSeek {plan['model']}, reasoning none/excluded, max16384, temperature0.1. No fallback, paid repair or Stage1/2. Incoming NTU ledger states and capture bounds reused from saved baseline; independent cases do not feed each other. PAN baseline predates additional prompt refinements. Both extraction and anchor instruction changed, so benefits cannot be attributed to either in isolation.

Cost USD {metrics['totals']['cost_usd']:.10f}; input {metrics['totals']['prompt_tokens']}; completion {metrics['totals']['completion_tokens']}; reasoning {metrics['totals']['reasoning_tokens']}; cached input {metrics['totals']['cached_prompt_tokens']}. Summed request time {metrics['totals']['elapsed_seconds']:.3f}s; first dispatch through last accounting {metrics['observed_first_dispatch_to_last_accounting_seconds']:.6f}s. Five unique IDs and all generation metadata available. Cost is API-reported, not invoice verification. See metrics.json, calls.csv, exact requests and receipts.

## Confirmed benefits and remaining analytical errors
NTU22 now keeps5/390 separate:5+390+3845+644=4884. NTU25 comparative FX dates are correct in new answer. NTU13 prose delta now validates, signed roll-forwards correct. NTU24 wrapped headers are improved, but answer still mislabels impairment loss as release; do not promote its earnings interpretation. PAN nearby tailings cells are separate, but grouped headers remain imperfect and model still double-counts1081oz in FY25. Correct disjoint sum92643+2654+98636+1081+1513=196527. No issuer fault established. Some literal-valid answers overstate ledger closure or invent likely explanations; findings.json records these separately from generation/validation success.

## Verification and preservation
Targeted tests: initial53passed(exit0); expanded run58passed/1failed(exit1), exposed genuine paragraph-ending/header leakage; corrected extraction; rerun59passed(exit0). Full offline suite232passed(exit0), DNS/connect/sendto denied. Six real-PDF regressions cover columns, wrapped headers, comparative dates, prose anchors, parentheses and dense PAN numeric cells. See saved result JSONs. New corpus exported after final code change. No new code changes after passing suite.

Production SQLite tables, source PDFs and baseline files unchanged (preservation.json). Original responses, incoming states and code snapshots retained. No guardrail SQL writes. Existing valuations preserved. No full report rerun, financial forecasts, current quote, Stage1, Stage2, or valuation readiness verified.

## Handoff
Use gemini/review_prompt.md in Antigravity. Review every new output, the same original sources, before/after text and ledger closure conditions. Prioritize remaining sign/overlap errors before requesting another paid trial. No additional analytical guardrails implemented; the sign and scope lessons overlap existing guidance. No embedding matcher, partial acceptance or fuzzy quote validation added.
'''
write(run/'audit.md',audit)
prompt=f'''Review the native PDF extraction pilot in this repository. Read AGENTS.md, workflow/STATE.md, workflow/WORKFLOW.md and docs/STOCK_EVALUATION_FORMAT.md section1A. You are Gemini evaluating DeepSeek; preserve all original evidence and save a new timestamped Gemini audit. Do not call paid models, change production SQLite, rewrite raw outputs or modify prompts/code.

Pilot directory:
{run}

Read plan.json, audit.md, findings.json, calculations.json, metrics.json, preservation.json, all five inputs/*_prompt.md and matching inputs/*.json, baseline Markdown answers, outputs/*.md, validation JSONs, requests and receipts. Read workflow/changes/20261028_table_extraction before/after corpus and renders. Check original PDFs from plan.json, verifying SHA-256, physical page numbering from1. NTU:13,21-25; PAN:48-50. Inspect originals rather than trusting Codex findings.

Determine which extraction improvements actually helped and what remains broken. Specifically verify NTU5/390/3845/644=4884, portfolio headings and signed -167 loss versus release, FX comparative dates, prose evidence anchors, POCI applicability and Q-08aa5c3f257440ab closure. For PAN, distinguish mining/surface/total operation scopes and buy-in overlap: test FY25 92643+2654+98636+1081+1513=196527; do not add1081 twice using93724. Check grouping labels, real one-ounce subtotal differences, unit/cost-conversion scope and speculative claims of source errors. Test all new closures against original conditions; five valid deltas does not imply five financially correct answers.

Assess whether remaining extraction work warrants one small generic change or whether source layout limitations should simply be carried as uncertainty. Avoid company-specific exceptions and complex table reconstruction. Separate implemented fixes, demonstrated benefits, remaining DeepSeek errors, Codex errors and proposed improvements. No Stage1/2 or valuation requested. Cost/time differences are not controlled benchmarks. Save versioned audit, claims/findings, independent calculations, inspected/unread coverage and input hashes under the company evaluations directory. End with a concise recommendation for the next minimal step; do not implement it.
'''
write(run/'gemini/review_prompt.md',prompt);write(HERE/'gemini_prompt.md',prompt)
manifest=[]
paths=list((run/'inputs').glob('*'))+list((run/'outputs').glob('*'))+list((run/'requests').glob('*'))+list((run/'receipts').glob('*'))
paths+=list((HERE/'before').glob('*'))+list((HERE/'after').glob('*'))+list((HERE/'renders').glob('*'))+list((run/'receipts_before_refresh').glob('*'))
for p in paths:
    if p.is_file():manifest.append(dict(path=str(p),sha256=sha(p)))
save(run/'input_manifest.json',manifest)
spec=importlib.util.spec_from_file_location('transport',ROOT/'workflow/changes/20261028_ntu_default_run/rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.preserve(run)
status=read(run/'status.json');status.update(status='complete_limited_review_gemini_pending',reviewed_utc=m.utc());save(run/'status.json',status)
save(HERE/'implementation_record.json',dict(run=str(run),changed_files={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'section_capture/pdf_source.py',ROOT/'section_capture/question_ledger.py',ROOT/'tests/test_native_table_extraction.py']},test_exit_code=0,full_tests=232,paid_calls=5,cost_usd=metrics['totals']['cost_usd'],validator_unchanged=True,limitations=[f['id'] for f in findings if f['verdict'] not in ['SUPPORTED WITHIN SAMPLE']]))
print('Saved independent audit, calculations, seven findings, input hashes and manual Gemini prompt.')
