"""Preserve baseline and verify prompt-only scope without external calls."""
import hashlib,json,importlib.util,sys
from pathlib import Path
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('transport',ROOT/'workflow/changes/20261028_ntu_default_run/rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
files=['prompts/common/12-analyst-reading-brief/v1.1.0/prompt.md','prompts/consumer_lending/12-analyst-reading-brief/v1.1.0/prompt.md','section_capture/question_ledger.py']
def tables():
    c=m.ro(ROOT/'documents/analysis.sqlite')
    try:return m.snap(c)
    finally:c.close()
def validator():return (ROOT/'section_capture/question_ledger.py').read_text(encoding='utf-8').split('\ndef apply_delta',1)[1]
if sys.argv[1]=='before':
    paths=list((ROOT/'companies').rglob('*.pdf'))
    evaluations=ROOT/'companies/consumer_lending/NTU/briefs/1H26/evaluations'
    paths += [p for p in evaluations.rglob('*') if p.is_file() and p.suffix in {'.md','.json'}]
    save('baseline.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),production_tables=tables(),evidence={str(p.relative_to(ROOT)):sha(p) for p in paths},files={p:sha(ROOT/p) for p in files},validator_sha256=hashlib.sha256(validator().encode()).hexdigest()))
    print('Preserved evidence hashes, production contents and validator baseline.')
else:
    baseline=json.loads((HERE/'baseline.json').read_text(encoding='utf-8'))
    checks=dict(production_tables_unchanged=tables()==baseline['production_tables'],evidence_unchanged=all(sha(ROOT/p)==h for p,h in baseline['evidence'].items()),validator_unchanged=hashlib.sha256(validator().encode()).hexdigest()==baseline['validator_sha256'])
    assert all(checks.values())
    tests=json.loads((HERE/'test_result.json').read_text(encoding='utf-8'))
    save('implementation_record.json',dict(completed_utc=datetime.now(timezone.utc).isoformat(),changes={p:dict(before=baseline['files'][p],after=sha(ROOT/p)) for p in files},preservation=checks,tests=tests,paid_calls=0,scope='Three concise prompt clarifications; no validation logic, extraction or provider setting changes.',source_review='companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T191648Z_codex_native_extraction_review/audit.md',demonstrated_model_improvement='NOT TESTED: no fresh model generations'))
    print(json.dumps(checks))
