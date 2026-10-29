from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
root=Path.cwd();out=root/'workflow/changes/20261028_valuation_withholding';out.mkdir(parents=True,exist_ok=True)
for name in ['valuation-gate-offline-targeted-20261028-result.json','valuation-gate-offline-full-20261028-result.json']:
 p=root/'tmp'/name
 assert p.exists(),name
 data=json.loads(p.read_text(encoding='utf-8'));assert data['exit_code']==0
 shutil.copy2(p,out/name)
shutil.copy2(root/'scratch/valuation_gate_offline_plugin.py',out/'offline_pytest_plugin.py')
files=['section_capture/valuation_policy.py','section_capture/db.py','section_capture/one_shot_view.py','section_capture/portfolio_view.py','evaluate_stock.py','workflow/export_stage1.py','workflow/generate_stage2.py','workflow/generate_sens_update.py','tests/test_valuation_withholding.py','tests/valuation_examples.py','docs/VALUATION_WITHHOLDING.md']
record={'recorded_utc':datetime.now(timezone.utc).isoformat(),'authorized_change':'Withhold target and recommendation when material problems remain; prompts and production validation.','targeted':{'passed':91,'exit_code':0,'seconds':30.11},'full_suite':{'passed':178,'exit_code':0,'seconds':96.99},'test_transport':'Telemetry opt-outs plus pytest plugin denying all Python DNS/connect/sendto events before collection.','limitations':'Checks declared evidence, numerical reconciliations and existing CLI SOTP/guardrail checks; cannot independently prove source truth or detect every omitted defect. Legacy notes retain read compatibility; new saves require readiness evidence.','live_models_called':False,'source_PDF_changed':False,'existing_NTU_valuation_fields_changed':False,'guardrail_code':'ALL-MATERIAL-ISSUES-VALUATION-WITHHOLD','registry_count':37,'files':[{'path':name,'sha256':hashlib.sha256((root/name).read_bytes()).hexdigest()} for name in files]}
(out/'implementation_record.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
p=root/'workflow/STATE.md';s=p.read_text(encoding='utf-8')
s=s.replace('Last updated: 2026-10-27 (Africa/Johannesburg).','Last updated: 2026-10-28 (Africa/Johannesburg).',1)
entry='''- **Approved material-issue valuation withholding implemented (2026-10-28)**:
  - Added shared publication gate in `section_capture/valuation_policy.py`. New Stage2/SENS outputs require READY/WITHHELD status, blockers, seven evidence checks and numerical reconciliations. Missing/incomplete evidence, material FAIL/NOT VERIFIED or inconsistent reconciliation inputs withhold target, bands, upside, dividend yield, TSR and recommendation; no zero/HOLD fallback.
  - Stage1 carries unresolved material findings forward; Stage2/SENS reopen working claims rather than using a99% confidence prior. First-JSON readiness is mandatory; later/conflicting blocks cannot authorize an earlier scenario target. Legacy notes remain readable, but new saves/resyncs require the contract.
  - GUI/CLI preserve timestamped raw candidate files; SQLite retains `stage2_candidate_response`. Withheld publication notes show blockers and clear stale derived fields. Portfolio/company/final pipeline displays say Valuation withheld and suppress dynamic rating fallback. Parent/companion updates preserve each report's own baseline. CLI material SOTP/guardrail failures override model READY and block rerun promotion.
  - Codified only the approved `ALL-MATERIAL-ISSUES-VALUATION-WITHHOLD` in default registry and SQLite (36->37); unrelated registry rows verified unchanged. NTU original production report values and source PDF hash remain unchanged; no paid model call or valuation rerun. Other analytical amendments remain proposals.
  - Targeted offline regressions:91 passed in30.11s,exit0. Full offline suite:178 passed in96.99s,exit0. Existing and new Qt tests dispose windows. The network-denial pytest plugin and telemetry opt-outs allowed local testing after automatic review reported an unknown Visual Studio telemetry request on a normal output poll; that interrupted attempt has no claimed final test result.
  - Reference fallback and prompt-expectation failures from the interrupted turn were fixed. Also fixed parent-baseline preservation and conflicting JSON handling. Guarded exact-match edit preflights and UTF-8/CRLF import handling failures were corrected before final passing checks. Test results, approved-rule/data verification and implementation hashes saved in `workflow/changes/20261028_valuation_withholding/`; documentation in `docs/VALUATION_WITHHOLDING.md`.
  - READY is a publication prerequisite, not independent financial validation: falsely reported source data or omitted dependencies still need evidence review. Temporary test-folder cleanup recorded separately after verification.

'''
assert s.count('## Completed\n')==1
s=s.replace('## Completed\n','## Completed\n\n'+entry,1);p.write_text(s,encoding='utf-8')
p=root/'TOOL_CHEATSHEET.md';s=p.read_text(encoding='utf-8')
s+='''

### 28. Resuming Interrupted Edits and Offline Regression Tests
* **Issue**: The execution host disconnected before a combined edit/test command began. On reconnection, old failures remained. Exact-match preflights also exposed rendered emoji mismatches and incorrect variable names; an AST fixture edit decoded raw CRLF before Windows text writes, creating doubled line breaks and a misplaced future import.
* **Rule**: Verify actual files after a pre-execution transport failure; never assume edits ran. Match real source text/codepoints, keep changes bounded, normalize source newlines before text writes, and place imports after `from __future__`. Inspect each terminal result rather than treating a shell exit as proof every earlier operation succeeded.
* **Offline test alternative**: If approval review reports unexplained telemetry, do not retry the same network-capable test process. Inspect relevant project/profile code first. A materially safer local test session can opt out of runtime telemetry and load a pytest plugin before collection that denies Python DNS/connect/sendto events. Preserve the actual result/exit code; host telemetry and source financial truth are not established by a passing suite. `workflow/changes/20261028_valuation_withholding/offline_pytest_plugin.py` preserves the plugin used for178 passing regressions.
'''
p.write_text(s,encoding='utf-8')
print('Saved implementation record, full/targeted test receipts and continuity documentation.')
