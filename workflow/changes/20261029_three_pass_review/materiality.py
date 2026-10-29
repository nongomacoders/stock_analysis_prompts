"""Conditional input-error materiality; no new target or paid generation."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,hashlib,importlib.util,sys,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT))
BASE=ROOT/'companies/consumer_lending/NTU/briefs/1H26/evaluations'
review=BASE/'20261029T121151Z_codex_three_pass_review'
run=BASE/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_codex_error_materiality');run.mkdir();(run/'inputs').mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
paths=[review/n for n in ['audit.md','findings.json','calculations/reconciliations.json','baseline.json']]
paths += [BASE/'20261029T112944Z_three_pass_experiment/plan.json',BASE/'20261029T114212Z_three_pass_pan_resume/plan.json',ROOT/'docs/VALUATION_WITHHOLDING.md']
manifest=[]
for p in paths:
    dest=run/'inputs'/f'{len(manifest):02d}{p.suffix}';shutil.copy2(p,dest);manifest.append(dict(original_path=str(p),preserved_path=str(dest),sha256=sha(p)))
save(run/'inputs/manifest.json',manifest)
sources=read(review/'baseline.json')['sources'];assert all(sha(Path(s['path']))==s['sha256'] for s in sources)
calc=dict(sign_flip_Rm=dict(correct=-167,misread=167,difference=167-(-167),qualification='Potential earnings-input difference only if interpretation enters numerical model;not measured cash-flow or equity-value impact.'),fv_scope=dict(component_Rm=644,total_PBD_Rm=4489,share_percent=100*644/4489,qualification='Portfolio carrying-value scope,not percentage of equity/company value. No demonstrated actual omission from a final valuation.'),pan_one_oz=dict(ounces=1,group_produced=272310,share_percent=100/272310),pan_overlap=dict(ounces=1081,group_FY25=196527,share_percent=100*1081/196527),pan_source_subtotal=dict(ounces=10000,group_FY26=272310,share_percent=100*10000/272310,qualification='Source column conflict,not proved Group production/revenue overstatement.'))
save(run/'calculations.json',calc)
claims=[dict(id='C001',claim='These experiments contain section outputs and no new Stage1/2 valuation.',verdict='PASS',evidence='Preserved experiment plans and previous run records.'),dict(id='C002',claim='167gain versus167loss differs by334Rm.',verdict='PASS',evidence='calculations.json;conditionalearnings-input reading,not valuation effect.'),dict(id='C003',claim='644is14.346%of4489PBD.',verdict='PASS',evidence='Prior originalNTU13,21–23 source review;calculations.json.'),dict(id='C004',claim='OnePANozis0.000367%of272310oz.',verdict='PASS',evidence='Prior originalPAN48–50 source review;calculations.json.'),dict(id='C005',claim='Exact effect on company/equity valuation.',verdict='NOT VERIFIED',evidence='No downstream propagation audit or paired final valuation recomputation in these experiments.'),dict(id='C006',claim='10000ozcolumnconflictmeanscompanyproduction/revenuemisstated.',verdict='NOT VERIFIED',evidence='Prior source inconsistency supports conflicting subtotals only;correct replacement/cause not established.')]
save(run/'claims.json',claims)
now=datetime.now(timezone.utc)
audit=f'''# Error tolerance and potential valuation materiality

Evaluator Codex;UTC{now.isoformat()};Africa/Johannesburg{now.astimezone(timezone(timedelta(hours=2))).isoformat()}.
Decision: **SMALL ROUNDING TOLERABLE; MATERIAL MEASUREMENT/SIGN/CLOSURE ERRORS REQUIRE RECONCILIATION BEFORE RELYING ON A NEW VALUATION. Exact valuation impact NOT VERIFIED.**

User asks whether section errors can be tolerated and how they affect final value. This record is conditional input-risk triage,not a new investment valuation or confirmation of an existing saved target. Experiments were section-only;no Stage1/2valuationgenerated. No claim that their specific mistakes reached an older saved valuation. Actual per-share or percentage valuation effect requires tracing which inputs downstream model uses and recomputing same valuation after corrections;not performed. No paid models,old targets/metricschanged or newfinancialguardrails.

Evidence inspected this turn:prior independent audit/findings/calculations,experimentplans,withholdingpolicy;original source hashes reverified. Primary pages previously independently viewed:NTU13,21–23,PAN48–50;no new page rendering or whole-report audit this turn. Exact analyzed inputs preserved in inputs/manifest.json. All remaining final-valuation dependencies NOT VERIFIED.

## Conditional scale
- Misreading a167Rmimpairmentloss as167Rmgain could introduce334Rmearnings-inputdifference if actually modeled numerically. Wording-only error with correctly reconciled cash-flow inputs has no demonstrated direct valuation change. A noncash measurement adjustment must not be mechanically treated as cash or doublecounted.
-644Rm is14.346%of4489RmPBDportfolio. Excluding an applicable component could be material;these section claims do not prove a final model omitted it. Portfolio share is not equity-value share. Avoid adding its accounting carrying amount to a DCF that already includes its collections.
-1oz/272310oz=0.000367%,normally immaterial rounding in this context.1081oz/196527oz=0.5501%FY25production;trace whether it affects forecast assumptions or simply an erroneous diagnostic.10000oz/272310oz=3.6723%scaleofsourcecolumnconflict,not established actualproductionorrevenueerror.
- Premature closure has no direct priced magnitude,but may remove required evidence checks from subsequent analysis;not tolerable as final proof of reconciliation.

## Tolerance rule
Errors may exist in draft section notes if downstream verified figures,scope and cash-flow bridges correct them. Final analysis should tolerate justified rounding/immaterial presentation differences,not unreconciled signs,assetcoverage,cash-vs-profit treatment or essential closure. Where a material dependency remains unresolved,the repository requires VALUATION WITHHELD - MATERIAL ISSUES UNRESOLVED rather than an unsupported target. Existing preserved valuations were not rewritten by this triage.

General valuation principle reference inspected:https://pages.stern.nyu.edu/adamodar/New_Home_Page/littlebook/intrinsicvsrelative.htm (NYUStern,AswathDamodaran):DCF depends on expected cash flows. Supplementary:https://pages.stern.nyu.edu/adamodar/pdfiles/eqnotes/dcfall2pg.pdf distinguishes accounting earnings from cash flows. These support method only,not company-specific effects. No targets,newmarketquotes or discount-rate assumptions supplied.

Next necessary evidence for quantification:chosen final valuation,source-linked opening balances,cash-flow and portfolio forecasts,exact use of impairment movements/otherassets,consistent tax/debt/sharecount/discounting,and same-model corrected arithmetic. Prefer offline recalculation rather than paying for another opaque narrative. This review proposes no SQLrule;existingwithholding/closure/scopepolicyalreadycoversmaterialerrors. No newtests for read-onlytriage;prior232full/27targetedofflinepassesretained,no tempfolders.
'''
(run/'audit.md').write_text(audit,encoding='utf-8')
spec=importlib.util.spec_from_file_location('transport',ROOT/'workflow/changes/20261028_ntu_default_run/rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.ro(ROOT/'documents/analysis.sqlite');tables=m.snap(c);c.close()
checks=dict(production_tables_match_previous_review=tables==read(review/'baseline.json')['production_table_hashes'],sources_unchanged=all(sha(Path(s['path']))==s['sha256'] for s in sources),originals_and_copies_unchanged=all(sha(Path(e['original_path']))==e['sha256']==sha(Path(e['preserved_path'])) for e in manifest))
assert all(checks.values());save(run/'preservation.json',checks);save(run/'execution.json',dict(exit_code=0,paid_calls=0,valuation_recomputed=False))
(HERE/'materiality_run.txt').write_text(str(run),encoding='utf-8');print(str(run))
