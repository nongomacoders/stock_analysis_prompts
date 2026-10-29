"""Independent arithmetic and evaluator review. No model calls or production writes."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,re,hashlib,importlib.util,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT))
run=Path((HERE/'run.txt').read_text().strip());BASE=run.parent
G=BASE/'20261028T184306Z_gemini';P=BASE/'20261028T182010Z_native_extraction_pilot'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def text(p):return p.read_text(encoding='utf-8')
calc={}
def check(key,expression,value,reported,scope):
    calc[key]=dict(expression=expression,calculated=value,reported=reported,residual=value-reported,scope=scope)
check('ntu_assets','5+390+3845+644',5+390+3845+644,4884,'NTU Mar26 Rm, physical22')
check('ntu_principal_roll','3975+382-728+383-167',3975+382-728+383-167,3845,'NTU H1FY26 Rm, physical13')
check('ntu_other_roll','702+28-116+30',702+28-116+30,644,'NTU H1FY26 Rm, physical13')
check('ntu_total_pbd','3845+644',3845+644,4489,'Note1 total, not independently tied to unread SoFP8')
check('ntu_movement','-241+69+4+1',-241+69+4+1,-167,'NTU H1FY26 Rm, physical24')
check('ntu_vintages','24-191',24-191,-167,'Acquired gain and historical loss, NTU24 Rm')
check('ntu_balance','598-167',598-167,431,'Cumulative gain Rm, Sep25-Mar26')
check('pan_fy25_disjoint_reported_subtotals','92643+2654+98636+1081+1513',92643+2654+98636+1081+1513,196527,'FY25 oz, uses reported tailings subtotal; does not validate its inconsistent component')
check('pan_fy25_model_overlap','93724+2654+98636+1081+1513',93724+2654+98636+1081+1513,196527,'FY25 oz, includes buy-in twice')
check('pan_fy26_underground','65233+40246',65233+40246,105478,'FY26 oz, source component/Group difference')
check('pan_fy26_mining','71997+46855',71997+46855,118853,'FY26 oz, source mining components/subtotal')
check('pan_fy26_group','118853+153458',118853+153458,272310,'FY26 oz, printed subtotals/Group')
check('pan_mtr_fy25_difference','30806-25043',30806-25043,0,'FY25 MTR tailings different source columns; same 5763 as FY26 buy-in is not causal proof')
check('pan_fy25_printed_leaf_tailings','15224+52606+25043',15224+52606+25043,98636,'FY25 oz, source leaf components vs printed subtotal')
oz_per_kg=1000/31.1034768
calc['tennant_denominator']={
 'source':'PAN49 A$1584835/kg, FY25 produced1513oz/sold1179oz; PAN50 A$58.1m all-in cost',
 'oz_per_kg':oz_per_kg,'implied_kg_from_rounded_cost':58.1e6/1584835,
 'produced_kg':1513/oz_per_kg,'sold_kg':1179/oz_per_kg,
 'rate_using_production':58.1e6/(1513/oz_per_kg),'rate_using_sales':58.1e6/(1179/oz_per_kg),
 'cost_implied_by_reported_rate_and_sales_million':1584835*1179/oz_per_kg/1e6,
 'sustaining_cost_plus_capex_at_report_average_A_million':3+35.8*1.54,
 'interpretation':'Sales denominator consistent with rounded reported cost. Exact methodology and commissioning causal attribution not independently proved; production denominator47kg does not reproduce1584835.'}
calc['fx_scope']={'expression':'985551/16.90/(1000/31.1034768)','calculated':985551/16.9/oz_per_kg,'reported_USD_per_oz':1867,
 'evidence':'PAN49 ZAR operations exclude Tennant in their A$ lines; PAN50 separately lists ZAR and A$ costs. A same-scope/same-definition reconciliation is required.',
 'interpretation':'Cannot establish transaction-date FX, asset weights, or sales-weighted methodology from these tables; no single proven cause of residual.'}
save(run/'calculations/reconciliations.json',calc)
outputs={p.stem:text(p) for p in (P/'outputs').glob('*.md')}
for k,v in outputs.items():assert v.strip()
assert len(outputs)==5
validations=[read(p) for p in (P/'outputs').glob('*.validation.json')]
assert len(validations)==5 and all(v['ledger_valid'] and not v['errors'] for v in validations)
item=read(P/'inputs/ntu_assets.json');q=next(q for q in item['questions'] if q['question_id']=='Q-08aa5c3f257440ab')
delta=json.loads(re.search(r'```json\s*(.*?)\s*```',outputs['ntu_assets'],re.S).group(1))
update=next(u for u in delta['updates'] if u['question_id']==q['question_id'])
save(run/'ledger_closure_check.json',dict(question=q,proposed_update=update,verdict='partial required; measurement basis supported, total-scope reconciliation deferred'))
assert update['status']=='resolved' and '4,489' in update['answer']
validator_old=text(ROOT/'workflow/changes/20261028_table_extraction/before_question_ledger.py').split('\ndef apply_delta',1)[1]
assert validator_old==text(ROOT/'section_capture/question_ledger.py').split('\ndef apply_delta',1)[1]
gfind=read(G/'findings.json');gclaims=read(G/'claims.json')
save(run/'gemini_registers.json',dict(findings=gfind,claims=gclaims,note='Use findings.json IDs; audit prose shifts IDs F007/F008/F009 relative to JSON.'))
assessments=[
 ('F001','supported','NTU22 source5/390/3845/644 and new answer agree; prior9879 allegation absent. Improvement demonstrated in this sample, not guaranteed elimination.'),
 ('F002','supported','NTU25 closing USD17.2/18.4/17.3 and GBP22.7/23.9/23.2 dates match new answer. Attribution solely to a specific extraction heuristic is not isolated.'),
 ('F003','partly supported','Five valid deltas and NTU13 correct prose/rolls confirmed. Both prompt and extraction changed; cannot prove short-anchor adherence or elimination of all quote brittleness. Several actual quotes exceed50chars and include pipes, yet match.'),
 ('F004','supported','NTU24 -167 impairment loss reduces cumulative gain598to431; DeepSeek calls it release. The +24 acquired gain is distinct from -191 historical loss.'),
 ('F005','supported','Actual resolved update explicitly defers4489 scope. Classification is answered but original carrying-value closure not fulfilled.'),
 ('F006','supported','Model adds1081 twice using93724; disjoint reported subtotals foot196527. This exact footing does not validate every printed tailings component.'),
 ('F007','partly supported','Speculative issuer-error explanation correctly criticized. Gemini substitutes unsupported transaction-date/weighted FX assertions and a47kg production explanation. Sold1179oz (36.671kg), not produced1513oz (47.060kg), fits reported A$58.1m and1584835/kg.'),
 ('F008','partly supported','Source MTR25043vs30806 difference5763 confirmed; printed tailings98636 uses30806. Cause, correct replacement and link to FY26 buy-in not established. One-ounce differences confirmed, but rounding is plausible rather than proved. Column numbering inaccurate: among13data columns MTR is6th/11th, with label/year/unit offsets9th/14th.'),
 ('F009','partly supported','Keep generic extractor and avoid complex company-specific parser, aligned with user preference. GFM lacks colspan, but fully qualified flat column labels can represent hierarchy; current placement is imperfect, not mathematically impossible to improve.')]
save(run/'gemini_finding_assessments.json',[dict(gemini_id=i,classification=v,evidence=e) for i,v,e in assessments])
findings=[
 dict(id='F001',severity='high',origin='DeepSeek section model',linked_gemini=['F004'],finding='NTU impairment loss still called release; signs in arithmetic alone insufficient.',correction='Interpret -167 as loss for this disclosed cumulative-gain balance; do not generalize to every reserve reduction.',financial_impact='167Rm direction mischaracterized; no forecast/valuation impact quantified.'),
 dict(id='F002',severity='medium',origin='DeepSeek ledger generation',linked_gemini=['F005'],finding='Q-08aa5c3f257440ab closed despite carrying-value scope deferred.',correction='Keep partial with answered basis and remaining scope; new question cannot substitute for original closure.',financial_impact='Premature removal from future evidence requests.'),
 dict(id='F003',severity='high',origin='DeepSeek column selection',linked_gemini=['F006'],finding='PAN model overlaps Group underground with buy-in, extra1081oz.',correction='Use disjoint scope; qualify reported subtotal components where source inconsistent.',financial_impact='False197608 vs196527oz model discrepancy.'),
 dict(id='F004',severity='medium',origin='Gemini evaluator',linked_gemini=['F007'],finding='47kg production denominator does not reproduce reported Tennant all-in cost rate; transaction-date/weighted FX assertion not established.',correction='Sold36.671kg and rounded58.1m imply1584358/kg, close to reported1584835; report consistency only, definitions/cause remain unverified.',financial_impact='Avoid replacing one invented cause with another; no valuation effect measured.'),
 dict(id='F005',severity='medium',origin='PAN original disclosure; evaluator certainty',linked_gemini=['F008'],finding='MTR FY25 tailings differs5763oz between asset/total columns; true source observation. Coincidence with FY26 buy-in does not identify cause or correct cell.',correction='Record both readings and unresolved source consistency. Qualify exact Group sum using reported subtotal.',financial_impact='5763oz component inconsistency, not proved Group-production error.'),
 dict(id='F006',severity='low',origin='Gemini evaluator',linked_gemini=['F003','F008','F009'],finding='Overstates quote-brittleness elimination, proven rounding and Markdown hierarchy impossibility.',correction='Restrict benefits to five cases, cause unverified; preserve optional qualified-label improvement without complex parser.',financial_impact='Limits engineering-confidence claims.'),
 dict(id='F007',severity='medium',origin='DeepSeek section interpretation; not singled out by Gemini',linked_gemini=[],finding='NTU24 says Debt review +69 gain is directionally consistent with payer-dropoff narrative. Aggregate deterioration does not establish that portfolio attribution.',correction='Separate management aggregate historical-book explanation from portfolio data; Debt review increased72to141.',financial_impact='Misleading portfolio-driver interpretation; no valuation effect quantified.')]
save(run/'findings.json',findings)
claims=[]
for n,(gid,verdict,evidence) in enumerate(assessments,1):
    claims.append(dict(id=f'C{n:03d}',origin='Gemini findings.json '+gid,claim=next(f['finding'] for f in gfind if f['id']==gid),classification='Evaluator inference from historical source evidence',primary_evidence='NTU physical13,21–25; PAN48–50 as specified in assessment',independent_check=evidence,verdict='PASS' if verdict=='supported' else 'NOT VERIFIED',assessment=verdict,consequence='See findings.json; no financial valuation validated'))
save(run/'claims.json',claims)
proposals=[
 dict(code='SECTION_SIGN_CONTEXT',sector='consumer_lending',title='Interpret disclosed cumulative-gain movements',mandate='When issuer presents POCI adjustment as cumulative gain added to book, a decrease is impairment loss; separate acquired gains and historical losses.',trigger='Signed POCI balance movement',evidence='Signed source row, opening/closing balances and basis',exceptions='Ordinary loss reserves/FVTPL require their own basis',double_counting_risk='Do not treat a balance movement and P&L line as independent charges',fail_example='598to431 labelled167release',pass_example='598-167=431; loss167=acquiredgain24-historicalloss191',implementation='Refine existing consumer-lending note, not new SQLite rule'),
 dict(code='SECTION_DISJOINT_SUM',sector='common',title='Disjoint column scopes',mandate='Before adding rows/columns, check whether subtotal already includes another component. If hierarchy uncertain, show alternatives and leave scope unresolved.',trigger='Multi-level table aggregation',evidence='Headers, component/subtotal values, period and units',exceptions='Clearly independent components may be summed',double_counting_risk='Subsidiary/operation totals plus their feedstock twice',fail_example='93724+2654+98636+1081+1513',pass_example='92643+2654+98636+1081+1513=196527 using reported subtotal with component caveat',implementation='One clause in existing common sign/scope instruction'),
 dict(code='LEDGER_KEEP_PARTIAL',sector='common',title='Closure conditions stay attached',mandate='If any essential closure evidence is pending or deferred to new question, retain partial and describe what remains.',trigger='Proposed resolved status',evidence='Incoming closure condition plus current evidence',exceptions='Explicit confirmed-not-disclosed closure alternative may satisfy a condition if established within searched scope',double_counting_risk='Avoid cloning unanswered scope as substitute for original question',fail_example='Resolved basis while4489scope deferred',pass_example='Partial: basis answered,totalcarryingscope pending',implementation='Clarify existing ledger contract; no new semantic engine')]
save(run/'proposed_prompt_refinements.json',dict(status='proposed only; not implemented',duplicate_check='Existing common prompt already requires signed scope arithmetic and closure; consumer notes already distinguish POCI gains. Refine wording, avoid duplicate checklists.',rules=proposals))
now=datetime.now(timezone.utc)
audit=f'''# Codex review of Gemini native-extraction pilot audit

Decision: **CORRECTIONS REQUIRED IN REVIEW DETAILS; EXTRACTION BENEFITS SUPPORTED WITHIN SAMPLE**.
Evaluator: Codex. UTC {now.isoformat()}; Africa/Johannesburg {now.astimezone(timezone(timedelta(hours=2))).isoformat()}.
Gemini self-reported Gemini3.8 Flash(High), audit20261028T184306Z; settings not independently observable. DeepSeek model/settings taken from exact pilot requests, not evaluator labels.

## Scope and preservation
Reviewed Gemini audit, claims, nine JSON findings and saved calculations as data; did not execute Gemini scripts. Preserved109 exact Gemini/pilot/code files under flat numbered inputs, original paths/SHA in inputs/manifest.json. Verified all39 Gemini manifest entries against both originals and copies. Audit says39 while STATE says40;39 is actual input count. Snapshot hashes match all production table contents in pilot plan; table-content hashing is not proof of identical database-file bytes or schema.

Independently rendered and viewed complete original NTU physical13,21,22,23,24,25 and PAN48,49,50. Source SHA matches pilot. Read all five raw DeepSeek answers, incoming assets closure condition, proposed delta and validations; before/after extraction corpus and relevant current prompt/validator code. Remaining original pages, companion reports and FX/cost definitions outside these captures NOT VERIFIED. This is section-only; no Stage1/2, market quote, forecast or valuation reviewed. Valuation scorecard NOT APPLICABLE, no target/recommendation issued.

## Gemini findings assessed
Use JSON finding IDs: audit body shifts the speculation/layout/new-source IDs. Full assessments are in gemini_finding_assessments.json.

- F001/F002 supported: source NTU22 has distinct5/390/3845/644=4884; new answer reads them correctly. NTU25 closing USD17.2/18.4/17.3 and GBP22.7/23.9/23.2 map to Mar26/Mar25/Sep25. Improvements in this selected sample, not universal guarantees or isolated proof of which heuristic caused them.
- F003 partly supported: five valid deltas and correct NTU13 rolls confirmed, strict validator unchanged. Extraction and anchor wording changed together. Actual valid quotes include longer-than50char passages and pipes, so complete adherence/eradication of brittleness not established. No full chronological convergence trial conducted.
- F004/F005 supported: -241+69+4+1=-167, and598-167=431; this cumulative-gain reduction is a loss, not release. Acquired+24 and historical-191 differ. Actual Q-08aa5c3f257440ab resolved update defers4489scope despite carrying-value closure. Semantic review required even when literal delta validates.
- F006 supported with source caveat: reported disjoint subtotals92643+2654+98636+1081+1513=196527. DeepSeek uses93724, which includes1081, then adds1081 again. Exact sum does not prove each tailings leaf is internally correct.
- F007 partly supported: speculative source-error assertions deserve rejection. Gemini's alternative explanation goes beyond inspected evidence: FY25 Tennant A$58.1m cost /1584835perkg implies36.660kg; production1513oz=47.060kg, sales1179oz=36.671kg. Sales-based rate1584358/kg agrees closely with rounded cost; production-based1234606/kg does not reproduce printed rate. Stated1584835 times sales impliesA$58.117m, consistent withA$58.1m rounding. A$3.0m sustaining plusUS$35.8mcapex*1.54=58.132m is additional consistency, not verified definition/cause. No proven printing error. ZAR and A$ operating cost scopes are separately shown; transaction-date FX, asset weights and sales weights are NOT established by these pages. Require matching cost scope and denominators rather than an invented conversion cause.
- F008 partly supported: new source observation genuine. PAN48 MTR FY25 tailings prints25043 in surface-asset column and30806 in total-MTR column, difference5763. BTRP15224+Elikhulu52606+MTR25043=92873 versus printed98636; using30806 reproduces98636. Equality to FY26 MTR buy-in5763 does not prove carryover, drafting cause, correct replacement or Group impact. Prior Codex missed this component conflict; revise prior exactness language accordingly. One-ounce differences confirmed at105479vs105478,118852vs118853 and272311vs272310; rounding plausible, not documented. Gemini's physical column indices mix data-only/all-column numbering; label+scope is safer.
- F009 partly supported: retain compact generic extractor and avoid company-specific parser. GFM lacks colspan, but qualified flat column names can carry hierarchy. Current extraction has imperfect parent-header placement; Markdown does not make semantic hierarchy impossible. No extra reconstruction warranted by this review alone.

## Additional DeepSeek issue and lessons
NTU24 describes Debt review+69 as directionally consistent with payer-dropoff explanation. Source management describes aggregate historical-book deterioration; Debt review gain rose72to141. Portfolio-specific attribution is unsupported. Gemini did not separately call this out. Neither evaluator should supply causal explanations merely because arithmetic or aggregate narrative seems compatible.

## Recommendation and unverified work
Retain extraction changes. Prefer three short refinements to existing guidance: signed cumulative-gain meaning; disjoint table aggregation with uncertainty; keep partial when an essential closure element is deferred. Existing prompts already cover related principles, so avoid duplicating rules or growing a checklist. Explicit pass/fail examples and exceptions saved in proposed_prompt_refinements.json. These are proposals only, no prompt edits or SQL guardrail codification. No production question status changed.

After authorization to change prompts, run appropriate offline checks and a small affected sample before considering a full chronological NTU trial. This review does not authorize paid reruns. Previous full offline suite232passed,exit0; no application changes or regression rerun this turn. Independent review calculation command and preservation verification exit0, recorded in execution.json. No temporary pytest folders created. All source, old model outputs, Gemini originals, pilot files and production tables rechecked unchanged.
'''
(run/'audit.md').write_text(audit,encoding='utf-8')
spec=importlib.util.spec_from_file_location('transport',ROOT/'workflow/changes/20261028_ntu_default_run/rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
baseline=read(run/'baseline.json');c=m.ro(ROOT/'documents/analysis.sqlite');tables=m.snap(c);c.close()
preservation=dict(production_tables_unchanged=tables==baseline['production_table_hashes'],sources_unchanged=all(sha(Path(s['path']))==s['sha256'] for s in baseline['sources']),originals_and_copies_unchanged=all(sha(Path(x['original_path']))==x['sha256']==sha(Path(x['preserved_path'])) for x in read(run/'inputs/manifest.json')))
assert all(preservation.values());save(run/'preservation.json',preservation)
save(run/'execution.json',dict(command='.venv/Scripts/python.exe workflow/changes/20261028_native_extraction_review/review.py',exit_code=0,paid_calls=0,application_changes=False,review_calculations_executed=True,gemini_scripts_executed=False))
print(json.dumps(dict(review=str(run),gemini_assessments=len(assessments),findings=len(findings),preservation=preservation)))
