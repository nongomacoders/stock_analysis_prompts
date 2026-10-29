"""Codify the single user-approved NTU ECL rule; preserve all other business rows."""
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding='utf-8')
def offline(event, args):
    if event in {'socket.connect','socket.getaddrinfo','socket.sendto'}:
        raise RuntimeError('Network disabled for guardrail codification checks')
sys.addaudithook(offline)
CODE='CONSUMER-LENDING-TRADE-RECEIVABLES-SIMPLIFIED-ECL'
AUDIT=ROOT/'companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T093647Z_codex_review/audit.md'
now=datetime.now(timezone.utc)
RUN=ROOT/'workflow/changes'/('20261028_ntu_ecl_guardrail_'+now.strftime('%H%M%SZ'))
RUN.mkdir(exist_ok=False)
def save(name, obj):
    (RUN/name).write_bytes((json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode('utf-8'))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(c):
    tables=[r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    return {t:sorted([list(r) for r in c.execute('SELECT * FROM "'+t.replace('"','""')+'"')], key=repr) for t in tables}
def hashes(tables):
    return {t:dict(rows=len(rows),sha256=hashlib.sha256(json.dumps(rows,ensure_ascii=False,default=str).encode('utf-8')).hexdigest()) for t,rows in tables.items()}
text=AUDIT.read_text(encoding='utf-8')
lines=text.splitlines()
parts={label:next(line.split(':** ',1)[1] for line in lines if line.startswith('- **'+label+':** '))
       for label in ['Title','Mandate','Required evidence','Exceptions','Double-counting risk','Should fail','Should pass']}
rule_text=' '.join([parts['Mandate'], 'Required evidence: '+parts['Required evidence'],
 'Exceptions: '+parts['Exceptions'], 'Avoid double counting: '+parts['Double-counting risk'],
 'Fail example: '+parts['Should fail'], 'Pass example: '+parts['Should pass']])
spec=dict(rule_code=CODE,sector='consumer_lending',stage='all',title=parts['Title'].rstrip('.'),
          rule_text=rule_text,origin_ticker='NTU',enabled=1)
save('approved_rule.json',dict(authorization='User replied yes to codifying the corrected conditional trade-receivables ECL rule into SQLite.',
 source_audit=str(AUDIT.relative_to(ROOT)),source_audit_sha256=digest(AUDIT),rule=spec,
 scope='Only this registry rule. No other prompt/ledger proposals or paid reruns authorized by this confirmation.'))
db=ROOT/'documents/analysis.sqlite'
source=sqlite3.connect(db.resolve().as_uri()+'?mode=ro',uri=True)
backup=sqlite3.connect(RUN/'before.sqlite')
source.backup(backup)
baseline=snapshot(backup)
backup.close();source.close()
c=sqlite3.connect(db)
c.row_factory=sqlite3.Row
try:
    c.execute('BEGIN IMMEDIATE')
    before=snapshot(c)
    assert before==baseline, 'Database changed during preparation; inspect before mutation.'
    existing=[dict(r) for r in c.execute('SELECT * FROM sector_guardrails ORDER BY rule_code')]
    assert not any(r['rule_code']==CODE for r in existing), 'Rule already exists; do not overwrite silently.'
    relevant=[r for r in existing if r['sector'] in ('all','consumer_lending')]
    save('duplicate_conflict_review.json',dict(existing_rules=relevant,assessment=
      'No same-code or simplified-trade-receivables rule. Complements POCI gain/scope, cash reconciliation and withholding; no existing rules changed.'))
    ts=now.isoformat()
    c.execute('INSERT INTO sector_guardrails (rule_code,sector,stage,title,rule_text,origin_ticker,enabled,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?)',
              (*spec.values(),ts,ts))
    inserted=dict(c.execute('SELECT * FROM sector_guardrails WHERE rule_code=?',(CODE,)).fetchone())
    after=snapshot(c)
    assert set(after)==set(before)
    for table in before:
        if table not in {'sector_guardrails','sqlite_sequence'}: assert after[table]==before[table], table
    assert len(after['sector_guardrails'])==len(before['sector_guardrails'])+1
    new_id=inserted['id']
    assert [r for r in after['sector_guardrails'] if r[0]!=new_id]==before['sector_guardrails']
    before_seq=dict(before['sqlite_sequence']); after_seq=dict(after['sqlite_sequence'])
    assert {k:v for k,v in before_seq.items() if k!='sector_guardrails'}=={k:v for k,v in after_seq.items() if k!='sector_guardrails'}
    c.commit()
finally: c.close()

# Exercise real prompt generation on a separate DB. Application helpers may migrate/seed it.
source=sqlite3.connect(db.resolve().as_uri()+'?mode=ro',uri=True)
copy=sqlite3.connect(RUN/'prompt_check.sqlite')
source.backup(copy);copy.close();source.close()
from workflow.export_stage1 import build_stage1_prompt_content
from workflow.generate_stage2 import build_stage2_prompt_content
from workflow.generate_sens_update import build_sens_update_prompt_content
checks=[]
for sector,ticker in [('consumer_lending','NTU'),('retail','DCP')]:
    common=dict(company_title='Verification Company',ticker=ticker,detected_sector=sector,db_path=RUN/'prompt_check.sqlite')
    prompts={
      'stage1':build_stage1_prompt_content(sections=[],filename='interim.pdf',**common),
      'stage2':build_stage2_prompt_content(stage1_content='Verification working paper',reference_price_zar=0.89,**common),
      'sens':build_sens_update_prompt_content(baseline_valuation_report='Verification baseline',reference_price_zar=0.89,stage1_audit_report='Verification audit',**common),
    }
    for stage,prompt in prompts.items():
        assert (CODE in prompt)==(sector=='consumer_lending'),(sector,stage)
        if sector=='consumer_lending': assert parts['Mandate'] in prompt
        checks.append(dict(sector=sector,stage=stage,rule_present=CODE in prompt,passed=True))

c=sqlite3.connect(db.resolve().as_uri()+'?mode=ro',uri=True)
assert snapshot(c)==after,'Production changed during isolated checks.'
c.close()
save('implementation_record.json',dict(completed_utc=datetime.now(timezone.utc).isoformat(),inserted_rule=inserted,
 changed_tables=['sector_guardrails','sqlite_sequence (sector_guardrails entry only)'],
 before_tables=hashes(before),after_tables=hashes(after),prompt_checks=checks,
 other_business_rows_unchanged=True,network_disabled=True,paid_calls=0,
 source_audit_unchanged=digest(AUDIT)==json.loads((RUN/'approved_rule.json').read_text(encoding='utf-8'))['source_audit_sha256'],
 limits='Registry/prompt wiring verified; future model compliance is not demonstrated. Section prompt integration unchanged.'))
(RUN/'codify_guardrail.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(dict(run=str(RUN.relative_to(ROOT)),rule_code=CODE,prompt_checks_passed=len(checks),other_business_rows_unchanged=True,paid_calls=0)))
