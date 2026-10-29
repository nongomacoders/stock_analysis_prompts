"""User-authorized retry of outstanding analyses without a caller-set token cap."""
import importlib.util
from pathlib import Path
import shutil
import sqlite3
from datetime import datetime, timezone
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('runner',HERE/'rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
parent=Path(m.POINTER.read_text(encoding='utf-8').strip())
assert m.read(parent/'receipts/stage2.json')['finish_reason']=='length'
assert 'max_tokens' not in m.request_payload('Verify omission',None)
assert not {'reasoning','reasoning_effort','provider','service_tier','max_completion_tokens'} & m.request_payload('Verify omission',None).keys()
run=parent.parent/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_deepseek_default_no_requested_cap')
run.mkdir(exist_ok=False)
for folder in ['inputs','outputs','requests','receipts','gemini']: (run/folder).mkdir()
for name in ['source_pages.json','guardrails.json','lessons.md','seed_questions.json','codex_review.md','production_snapshot.sqlite']:
    shutil.copy2(parent/'inputs'/name,run/'inputs'/name)
for name in ['metrics.json','calls.csv','plan.json','RUN_SUMMARY.md']:
    shutil.copy2(parent/name,run/'inputs'/('parent_'+name))
source=m.ro(parent/'experiment.sqlite');target=sqlite3.connect(run/'experiment.sqlite')
source.backup(target);source.close()
# Preserve valid section work. Refresh both downstream stages after the outstanding capture.
for prefix in ['stage1','stage2']:
    cols=[r[1] for r in target.execute('PRAGMA table_info(reports)') if r[1].startswith(prefix+'_')]
    target.execute('UPDATE reports SET '+','.join('"'+col+'"=NULL' for col in cols))
target.commit();target.close()
plan=m.read(parent/'plan.json')
plan.update(created_utc=m.utc(),parent_run=str(parent),authorization='User explicitly requested rerunning incomplete sections with no token limit.',
 model=m.MODEL,section_prompt_revision='uncapped_v4',budgets=dict(section=None,stage1=None,stage2=None),
 token_limit_policy='Omit max_tokens and max_completion_tokens entirely; provider/model/account limits still apply. Default thinking/routing retained.',
 planned_calls=3,planned_scope='Outstanding pages22-24 capture, refreshed Stage1 for updated evidence, full Stage2 retry. Nine accepted captures reused without paid reruns.',
 continue_with_explicit_failed_section_source=False,
 retry_policy='One ledger repair if needed; no silent resubmission of incomplete generations. Any provider/default limit will be recorded.',
 original_files=[dict(path=str(p),sha256=m.sha(p)) for folder in ['outputs','requests','receipts'] for p in (parent/folder).iterdir() if p.is_file()]
   +[dict(path=str(parent/'experiment.sqlite'),sha256=m.sha(parent/'experiment.sqlite'))])
plan['revisions'].append(dict(utc=m.utc(),authorization='User: rerun the incomplete sections with no token limit',
 changes='No requested completion-token ceiling on outstanding capture, refreshed Stage1 or Stage2. Other model controls unchanged. Previous outputs remain in parent run.'))
m.save(run/'plan.json',plan)
m.save(run/'status.json',dict(status='prepared',stage='not_started',calls=0))
m.save(run/'inputs/uncapped_request_check.json',dict(passed=True,example_payload=m.request_payload('Check only; not submitted',None),
 no_token_limit_fields=True,no_reasoning_or_routing_overrides=True,paid_calls=0))
shutil.copy2(HERE/'rerun.py',run/'runner.py')
m.text(HERE/'previous_capped_run.txt',str(parent));m.text(m.POINTER,str(run))
print('Prepared',run)
