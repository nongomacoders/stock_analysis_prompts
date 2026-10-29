"""Preserve GLM/OpenCode review and document verified evaluator corrections."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,re
ROOT=Path(__file__).resolve().parents[3];B=ROOT/'companies/consumer_lending/NTU/briefs/1H26/evaluations'
G=B/'20261029T123636Z_open_code_three_pass_review';R=B/'20261029T114212Z_three_pass_pan_resume';O=B/'20261029T112944Z_three_pass_experiment'
run=B/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_codex_opencode_review');run.mkdir();(run/'inputs').mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def text(p):return p.read_text(encoding='utf-8')
def save(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
files=[p for p in G.rglob('*') if p.is_file()]+[ROOT/'workflow/changes/20261029_three_pass/open_code_comparision.md',B/'20261029T121151Z_codex_three_pass_review/audit.md',R/'outputs/pan_dense_why.md',R/'outputs/pan_dense_single.md',O/'outputs/ntu_assets_single.validation.json']
manifest=[]
for p in files:
    dst=run/'inputs'/f'{len(manifest):03d}{p.suffix}';shutil.copy2(p,dst);manifest.append(dict(original=str(p),copy=str(dst),sha256=sha(p)))
checks=[]
for e in json.loads(text(G/'input_manifest.json')):
    p=Path(e['path']);p=p if p.is_absolute() else ROOT/p
    checks.append(dict(path=str(p),match=sha(p)==e['sha256']))
assert all(e['match'] for e in checks);save(run/'input_checks.json',checks);save(run/'inputs/manifest.json',manifest)
pan=text(R/'outputs/pan_dense_why.md')
delta=json.loads(re.search(r'```json\s*(.*?)\s*```',pan,re.S).group(1))
assert '30,806' in pan and '25,043' not in pan and '5,763' not in pan
assert not any('MTR' in q['question'] for q in delta['new_questions'])
calc=dict(tailings_leaf_sum=15224+52606+25043,printed_tailings=98636,residual=(15224+52606+25043)-98636,elikhulu_sold_kg=53092*31.1034768/1000,elikhulu_rate=1130.9e6/(53092*31.1034768/1000),ebitda_leaf_sum=142.4+120.9+29.4+171.4+155.9+43.0,ebitda_total=663.1)
save(run/'calculations.json',calc)
findings=[dict(id='F001',verdict='SUPPORTED CORRECTION TO CODEX',finding='My prior review wrongly said both final PAN prose identifiedMTR5763conflict. Staged final only mentions30806in driver context,not the25043/5763conflict. Single identifies it and preserves medium-priority question; staged omits both.',revision='Explicitly supersedes point5/assessmentF009 in20261029T121151Zreview; original unchanged.'),dict(id='F002',verdict='GLM ARITHMETIC ERROR',finding='GLM writes15224+52606+25043=98636exact; actual92873,short5763. Using30806reproduces98636. Its proposed25043+5763closure imports aFY26buy-in quantity intoFY25without evidence; numericfit alone cannot resolve source uncertainty.'),dict(id='F003',verdict='GLM UNIT ERROR',finding='GLM says5309.2kgfor53092oz; actual1651.3518kg.1130.9m/5309.2wouldnotyield6848xx; correct conversion does.'),dict(id='F004',verdict='GLM VALIDATOR MISDIAGNOSIS',finding='3 414 is literal but5chars below8minimum; spaces are not the reason. Whitespace-only differences already normalized. Do not weaken literal matching to fix length failure.'),dict(id='F005',verdict='GLM OVERSTRICT ROUNDING',finding='663.0versus663.1explicit0.1roundingresidual does not automatically invalidate financial arithmetic. Sixone-decimal components and rounded total permit this residual; cause plausible,not proved. Contrast with false exact272310=118853+153458check.'),dict(id='F006',verdict='GLM OVERSTATEMENT',finding='No staged output mentions30806 is false; final has driver30806to51927. Substantive absence ofMTRgap is correct. PAN generic false definitions are not repeated in final; propagation into final is unproved. Stage1doesnotcontain71997identity,so threefold identity propagation overstates trace.'),dict(id='F007',verdict='SUPPORTED WITH LIMITS',finding='Highercost,clearerworksheet,prematureNTUclosure and failure to demonstrate robust superiority supported. Do not adoptyet; no general refutation. Arithmetic-validator proposalneeds bounded schema/exception design and userauthorization; do not close cross-yearsourceconflicts by forced arithmetic.')]
save(run/'findings.json',findings)
(run/'audit.md').write_text('''# Codex review of GLM5.3/OpenCode comparison

Decision: retain current app workflow; three-pass benefit not demonstrated reliably. GLM correctly identifies an error in my earlier review, but its own arithmetic and validation explanations require correction.

User identifies reviewer as GLM5.3/OpenCode; report uses Gemini-role terminology, not proof of Gemini execution. Preserved raw report and versioned audit/register/calculation files, verified input-manifest hashes without executing its scripts. Existing source PDF hashes are included in those checks. This is a focused consistency review against supplied raw experiment outputs and previously independently reviewed originalNTU13,21–23/PAN48–50; no new renders/fullvaluation audit this turn. Other sources/valuation dependencies NOT VERIFIED.

Correction to my previous record: final staged PAN does NOT identify theMTR25043vs30806gap in prose. It merely mentions30806as a comparative production figure. Thus the issue was not just dropped from its ledger; it was absent from final narrative too. Prior20261029T121151Zpoint5/assessmentF009 is superseded here; original preserved. Single identifiesgap and hasmedium-priorityMTRquestion.

GLM's tailings equation is false:15224+52606+25043=92873,not98636; discrepancy5763 remains. Its cost denominator5309.2kgfor53092oz is wrong;1651.35kg gives684835ZAR/kg from rounded1130.9m. Minimum8charquote rejection is not a spaces/literal-match error:3 414is literal but5chars. Explicit0.1EBITDAresidual across rounded components is not inherently a false pass; justified smallrounding is tolerable. Its blanketgrepstatement about30806also overstates: driver comparison includes30806. ProposedMTR25043+5763closure combinesFY25withFY26and does not establish cause/correctreplacement. No semantic-engine implementation or paid follow-up authorized by review.

The comparison still supports clearer staged worksheets and highercost,with unresolvedscope/closureerrors. No basis for universal verdict about three-pass workflows, nor a claim all interim mistakes propagate unchanged to final. Detailedfindings,independentcalcs,inputhashchecks saved. No rawoutput/source/production edits or paidcalls. No regression rerun for read-onlyreview; fullsuite is running separately for user's commit/push request. Proposed changes remain proposals.
''',encoding='utf-8')
assert all(sha(Path(e['original']))==e['sha256']==sha(Path(e['copy'])) for e in manifest)
save(run/'execution.json',dict(exit_code=0,paid_calls=0,originals_and_copies_unchanged=True));(Path(__file__).parent/'opencode_review_run.txt').write_text(str(run),encoding='utf-8');print(str(run))
