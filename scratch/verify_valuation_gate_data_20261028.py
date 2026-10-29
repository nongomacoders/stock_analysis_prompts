from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,sqlite3
root=Path.cwd();folder=root/'workflow/changes'/('20261028_valuation_withholding')
folder.mkdir(parents=True,exist_ok=True)
rule=json.loads((root/'scratch/valuation_withholding_rule.json').read_text(encoding='utf-8'))
con=sqlite3.connect('file:documents/analysis.sqlite?mode=ro',uri=True);con.row_factory=sqlite3.Row
stored=con.execute('SELECT * FROM sector_guardrails WHERE rule_code=?',(rule['rule_code'],)).fetchone()
assert stored is not None,'Rule has not yet been seeded by migration'
for key in ['rule_code','sector','stage','title','rule_text','origin_ticker']:
 assert stored[key]==rule[key],key
all_rules=[dict(x) for x in con.execute('SELECT * FROM sector_guardrails ORDER BY rule_code')]
sha='9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc'
live=dict(con.execute('SELECT * FROM reports WHERE sha256=?',(sha,)).fetchone())
baseline_path=root/'companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T175621Z_codex_max_comparison/inputs/analysis_snapshot.sqlite'
old=sqlite3.connect(baseline_path);old.row_factory=sqlite3.Row
prior=dict(old.execute('SELECT * FROM reports WHERE sha256=?',(sha,)).fetchone())
old_rules=[dict(x) for x in old.execute('SELECT * FROM sector_guardrails ORDER BY rule_code')]
old.close();con.close()
prior_reports_unchanged=all(live[k]==v for k,v in prior.items())
assert prior_reports_unchanged,'Unexpected NTU production data change'
current_without_new=[x for x in all_rules if x['rule_code']!=rule['rule_code']]
assert current_without_new==old_rules,'Unrelated guardrails changed'
pdf=next((root/'companies/consumer_lending/NTU/sources').rglob('*.pdf'))
assert hashlib.sha256(pdf.read_bytes()).hexdigest()==sha
record={'checked_utc':datetime.now(timezone.utc).isoformat(),'approval':'User yes to implementing material-issue withholding in prompts and production validation; carried forward by continue.','guardrail':dict(stored),'prior_registry_count':len(old_rules),'current_registry_count':len(all_rules),'other_rules_unchanged':True,'NTU_production_old_columns_unchanged':True,'new_candidate_column_present':'stage2_candidate_response' in live,'PDF_sha256':sha,'baseline_snapshot':str(baseline_path)}
(folder/'guardrail_and_data_verification.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print('Approved rule verified in SQLite:',len(old_rules),'->',len(all_rules))
print('Other guardrails, original NTU production values and PDF remain unchanged.')
