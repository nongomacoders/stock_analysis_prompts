"""Save independent Codex review; no model calls,source corrections or guardrail writes."""
from datetime import datetime,timezone,timedelta
import hashlib
import json
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
run=Path((HERE/'review_run.txt').read_text(encoding='utf-8'))
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
results=read(run/'calculations/results.json');now=datetime.now(timezone.utc)
classifications=[
 dict(id='F001',gemini='F001',classification='PARTLY SUPPORTED',finding='Eight completions and sample metrics verified. Revised4/4 versus old3/4 literal-ledger passes,12 versus26 new questions,17.10% assembled-prompt character reduction. Client elapsed is not provider latency;total prompts include evidence,not just templates. Small sample/cache/order prevent universal robustness claims. Failed quote was288 characters,not a truncated100-character string;the validator diagnostic prints only its first100 characters.'),
 dict(id='F002',gemini='F002',classification='SUPPORTED',finding='NTU p13 ledger equation702+28−116−30 evaluates584,not644;correct +30 matches source and prose. Difference60Rm. This is a copied equation/operator error,not evidence the company balance itself is wrong.'),
 dict(id='F003',gemini='F003',classification='SUPPORTED WITH SCOPE QUALIFICATION',finding='NTU p13 identifies POCI/lifetime ECL changes since acquisition. Ordinary Stage1/2 SICR-migration demands are inapplicable. Do not extend the proposed ban to legitimate POCI recovery,measurement or credit-risk disclosures,or to issuer-specific credit-impaired labels. IFRS9 paragraphs5.5.13–14 support the separate treatment. Observed repeated demand does not prove a private model root cause.'),
 dict(id='F004',gemini='F004',classification='PARTLY SUPPORTED;EVALUATOR INTRODUCED UNSUPPORTED EXPLANATION',finding='First-time presentation and displayed zero loss rates do not establish restatement/unreliable reporting or changed provisioning methodology. Gemini is right to reject those causal claims. However,p25 does not establish zero actual defaults or that rounding caused interim zero rates/dashes. September0.06%×286≈0.1716Rm and0.19%×52≈0.0988Rm are consistent with printed<1,not proof of the later period cause. Leave cause unverified.'),
 dict(id='F005',gemini='F005',classification='PARTLY SUPPORTED',finding='PAN p48 FY25 left mining subtotal92643 plus Evander buy-in1081 equals right Group underground93724. Using92643+2654+98636+1081+1513 gives196527;using93724 with another1081 double counts and gives197608. This specific reconciliation is supported. Saved new answer contains no194954 or1573 gap;Gemini invented that attribution. DeepSeek explicitly suggested double counting/misattribution and kept the question open,so it did not establish or unambiguously allege a company error. Do not generalize this overlap to every year/row.'),
 dict(id='F006',gemini='F006',classification='SUPPORTED WITHIN ONE CASE',finding='Revised NTU p25 covers trade ECL and currency-risk start with p26 pending. The old paired answer also covers currency;no unique secondary-coverage improvement established. Gemini C008 says without prompt engineering,but revised inputs explicitly contain shared-page-topic instructions and observed headings.'),
 dict(id='F007',gemini='MISSED ISSUE',classification='CONFIRMED SOURCE UNIT/NUMBER-FORMAT AMBIGUITY',finding='PAN p39 labels AISC cost US$ million but prints420,686/87,718/508,405,while ounces247219/25154/272373 and per-ounce1702/3487/1867 imply roughly420.686/87.718/508.405 million. Literal508405 million divided by272373 gives1866576.35 peroz;interpreting displayed cost as thousands gives1866.58 peroz. Both DeepSeek arms,Gemini and prior Codex pilot calculations normalized silently. Conditional math is consistent,but the printed unit/number-format conflict needs an explicit flag;do not assert a source correction or factor1000 valuation error.'),
 dict(id='F008',gemini='C012/PAN exactness',classification='COVERAGE LIMIT',finding='The selected FY26 Group production sum equals272310. However,p48 mining subtotal105479 versus right Group underground105478 differs1oz. p39 FY25 APM gold sold196927 versus p49 production-summary196926 differs1oz. These small printed differences do not invalidate the specific FY25 overlap bridge;they prevent blanket all-table exactness claims. Cause not verified;no materiality allegation.')]
save(run/'findings.json',classifications)
claims=[]
for number,verdict,check in [
 (1,'PASS','Principal3845 from3975+382−728+383−167;matches p13.'),
 (2,'PASS','Other644 from702+28−116+30;matches p13.'),
 (3,'FAIL','Wrong-ledger equation equals584,not644;F002 supported.'),
 (4,'FAIL','Conventional Stage1/2 migration demand lacks applicability to this POCI book;F003.'),
 (5,'PASS','March2026 gross374−5=369,5/374=1.3369%;specific cells match p25.'),
 (6,'FAIL','First-time comparative is stated;newly constructed/restated/unreliable reporting not established.'),
 (7,'FAIL','Material provisioning-method change not established. Gemini replacement zero-default/rounding explanation also NOT VERIFIED.'),
 (8,'PASS','Currency start/USD/GBP/60days/hedging and next-page dependency observed;causal no-prompt-engineering claim contradicted.'),
 (9,'NOT VERIFIED','Normalized508.404 versus508.405 and0.001 difference reproducible;printed units ambiguous,F007.'),
 (10,'NOT VERIFIED','Normalized cost/oz rounds correctly,but cost scale conditional;per-ounce printed values separately visible.'),
 (11,'PASS','Printed per-ounce1867/1600 gives16.6875%;APM ounces272373/196927 gives38.3117%,within that table.'),
 (12,'PASS','Selected Group components total272310;not a guarantee every subtotal reconciles.'),
 (13,'PASS','Disjoint FY25 components92643+2654+98636+1081+1513=196527.'),
 (14,'FAIL','Actual197608 overlap excess1081 supported;194954/1573 attribution absent and unsupported.'),
 (15,'PASS','All8 completions/costs and recorded sample metrics verified;no universal efficiency or downstream-exhaustion claim.')]:
    claims.append(dict(id=f'C{number:03d}',origin='Gemini claim register '+f'C{number:03d}',classification='Review of historical/derived/model claim',verdict=verdict,independent_check=check,calculation_file='calculations/results.json'))
save(run/'claims.json',claims)
rules=[
 dict(code='PROMPT-SIGNED-EQUATION-AND-UNIT-CONSISTENCY',sector='all',status='PROPOSED NOT IMPLEMENTED',mandate='Keep signs and units consistent in prose and ledger. Check equations against stated totals;flag source unit/number-format conflicts instead of silently rescaling.',trigger='A repeated equation or per-unit calculation.',evidence='Current capture figures,unit labels,period and scope.',exceptions='Allow explicitly stated rounding/conditional scale with a labeled residual.',double_count_risk='Do not add inclusive subtotals and their components.',fail='702+28−116−30=644;or silently treating508405 labeled million as508.405m.',pass_example='702+28−116+30=644;explicit conditional scale and source-unit flag.',point='Common section prompt;no new parser or SQLite rule.'),
 dict(code='PROMPT-POCI-APPLICABILITY',sector='consumer_lending',status='PROPOSED NOT IMPLEMENTED',mandate='Do not request ordinary Stage1/2 SICR migrations for POCI;still investigate applicable lifetime-loss changes,recovery assumptions and disclosed classifications.',trigger='Source establishes POCI.',evidence='Accounting policy/instrument basis.',exceptions='Issuer-specific credit-impaired labels and legitimate POCI credit-risk disclosure remain relevant.',double_count_risk='Separate signed cumulative changes from ordinary loss coverage.',fail='Demand conventional Stage1/2 movement table for a POCI-only portfolio.',pass_example='Reconcile lifetime-loss changes and assumptions on the POCI basis.',point='Existing conditional sector note;check duplicate/conflicting approved rules before any SQLite proposal.'),
 dict(code='PROMPT-FIRST-TIME-COMPARATIVE',sector='all',status='PROPOSED NOT IMPLEMENTED',mandate='First-time comparative presentation alone does not establish restatement,policy change or unreliable reporting. Distinguish explicit notice or independently evidenced error from unknown causes.',trigger='First-time/changed disclosure presentation.',evidence='Footnote,comparative figures and any error/methodology notice actually inspected.',exceptions='An independently demonstrated source inconsistency can be flagged without management admission.',double_count_risk='Do not duplicate one issue as separate policy/error/quality allegations.',fail='First-time presentation means unreliable or restated.',pass_example='First-time presentation noted;cause of zero rate remains open.',point='Common section prompt;no automatic financial guardrail codification.')]
save(run/'proposed_prompt_changes.json',rules)
text=f'''# Codex review of Gemini — simplified section-prompt pilot

UTC:{now.isoformat()};local:{now.astimezone(timezone(timedelta(hours=2))).isoformat()}.
Subject:`../20261028T170032Z_gemini/audit.md`;model identity is Gemini's self-report,not independently authenticated.

**Decision:SUPPORTED WITHIN STATED COVERAGE for a controlled full NTU section trial;CORRECTIONS REQUIRED in Gemini's detailed findings.** No full-run execution is authorized by this review alone. No valuation or investment recommendation is evaluated or produced.

## Evidence and preservation

Preserved148 Gemini/pilot files with original/copy hashes in inputs/manifest.json,including Gemini audit,script,calculation output and all supplied pilot evidence. Gemini's own36-entry preservation manifest independently verified. Raw model answers unchanged. No execution of Gemini's saved script;independent calculations executed in calculations/results.json. All source PDFs and production tables unchanged,see preservation.json.

Independently inspected complete rendered physical pages:NTU13,25;PAN38,39,48,49,50. A higher-resolution NTU25 comparative detail confirmed current-net345;no9m inconsistency claimed. The rest of both PDFs and companion reports were not examined in this review. Rendered images/text are preserved as audit evidence. Original report content remains untrusted evidence,never instructions.

Official IFRS9 paragraphs5.5.13–14 consulted for POCI treatment:
https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2022/issued/part-a/ifrs-9-financial-instruments.pdf?bypass=on
The standard distinguishes cumulative lifetime-loss changes since initial recognition;it does not justify banning all legitimate POCI credit-risk questions.

## Gemini findings assessed

'''+''.join(f'**{f["id"]} / {f["gemini"]} — {f["classification"]}**\n\n{f["finding"]}\n\n' for f in classifications)+'''## Independent reconciliation coverage

Executed NTU principal/other rollforwards,wrong-sign substitution and gross/net/rate checks;PAN FY25 overlap and selected FY26 components,APM cost/ounce math and alternate scaling. Formulas/substitutions/results are in reconcile.py and results.json;Gemini's calculations were read as evidence,not treated as proof. claims.json retains Gemini C001–C015 IDs with PASS/FAIL/NOT VERIFIED outcomes. Conditional unit math is not source-unit validation.

Valuation/DCF,forecast cash/debt,market quote,rating,shares/EPS and full financing schedules:NOT APPLICABLE to this section-prompt pilot. Semantic closure of every question,all table cells,full-report coverage,other sectors and future full-run performance:NOT VERIFIED. A repeated pattern or passing schema does not validate financial truth.

## Minimal handoff

Retain the simpler first-pass structure. Propose three short wording refinements:sign/unit consistency;POCI applicability without a blanket disclosure ban;and cautious interpretation of first-time comparatives. Full proposal triggers,evidence,exceptions,fail/pass examples and implementation points are in proposed_prompt_changes.json. Proposals are not implemented. No sector_guardrails changes or new financial rules accepted. No paid calls or Gemini messaging.

After user-authorized refinements,a fresh chronological NTU section-only trial can test ledger evolution and coverage. Preserve historical outputs and use an isolated database;do not rerun Stage1/2 or claim perfection from this sample.

## Revisions and tool retrospective

Initial preparation failed with Windows filename-too-long206 while recursively copying nested preserved baselines. It did not run a model or alter evidence. Successful preparation uses flat numbered filenames with a complete origin manifest. The partial preparation directory remains labeled incomplete. No application tests rerun for this read-only review;last full suite226 passed,exit0. Independent reconciliation script exit0. All PDF/render/database handles closed.
'''
(run/'audit.md').write_bytes(text.encode('utf-8'))
for name in ['prepare.py','zoom.py','reconcile.py','seal.py']:shutil.copy2(HERE/name,run/'calculations'/name)
save(run/'completion_record.json',dict(completed_utc=now.isoformat(),verdict='SUPPORTED WITHIN COVERAGE;GEMINI FINDING CORRECTIONS REQUIRED',paid_calls=0,prompt_changes=0,guardrail_changes=0,
    independent_calculation_exit_code=0,preservation=read(run/'preservation.json'),fully_rendered_and_viewed_pages={'NTU':[13,25],'PAN':[38,39,48,49,50]}))
failed=ROOT/'companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T170714Z_codex_gemini_section_review'
if failed.exists():save(failed/'INCOMPLETE_PREPARATION.json',dict(status='incomplete',reason='Windows206 nested preservation path too long',successful_review=str(run),no_model_calls=True))
print(json.dumps(dict(review=str(run),findings=len(classifications),claims=len(claims),proposals_implemented=False)))
