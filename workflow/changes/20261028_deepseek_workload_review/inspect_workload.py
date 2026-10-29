from pathlib import Path
import collections
import hashlib
import json
import sqlite3
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
DB = ROOT / 'documents/analysis.sqlite'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

before = digest(DB)
conn = sqlite3.connect(DB.resolve().as_uri() + '?mode=ro', uri=True)
conn.row_factory = sqlite3.Row
try:
    reports = conn.execute('SELECT sha256,filename,original_path,period,physical_page_count,questions_ledger FROM reports ORDER BY filename').fetchall()
    rows = conn.execute('SELECT report_sha256,section_number,heading,selected_text,prompt,llm_response,stored_questions_snapshot,manifest_json FROM sections ORDER BY report_sha256,section_number,id').fetchall()
    rules = [dict(row) for row in conn.execute('SELECT rule_code,sector,stage,rule_text FROM sector_guardrails WHERE enabled=1')]
finally:
    conn.close()
by_report = collections.defaultdict(list)
for row in rows:
    by_report[row['report_sha256']].append(row)
summary = []
section_details = []
for rep in reports:
    sections = by_report[rep['sha256']]
    if not sections:
        continue
    pages = set()
    for sec in sections:
        manifest = json.loads(sec['manifest_json'] or '{}')
        selections = manifest.get('selections', [])
        captured_pages = {s.get('physical_page') for s in selections if isinstance(s.get('physical_page'), int)}
        pages |= captured_pages
        section_details.append(dict(filename=rep['filename'],period=rep['period'],section_number=sec['section_number'],heading=sec['heading'],captured_pages=sorted(captured_pages),evidence_chars=len(sec['selected_text'] or ''),prompt_chars=len(sec['prompt'] or ''),response_chars=len(sec['llm_response'] or ''),prior_ledger_chars=len(manifest.get('stored_questions') or ''),stored_snapshot_chars=len(sec['stored_questions_snapshot'] or ''),review_metadata=manifest.get('review', {})))
    count = rep['physical_page_count'] or 0
    summary.append(dict(filename=rep['filename'],period=rep['period'],pages=count,sections=len(sections),analyzed=sum(bool((s['llm_response'] or '').strip()) for s in sections),captured_page_count=len(pages),uncaptured_pages=sorted(set(range(1,count+1))-pages),evidence_chars=sum(len(s['selected_text'] or '') for s in sections),section_prompt_chars=sum(len(s['prompt'] or '') for s in sections),section_response_chars=sum(len(s['llm_response'] or '') for s in sections),final_ledger_chars=len(rep['questions_ledger'] or '')))
comparison = ROOT / 'companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T175621Z_codex_max_comparison/outputs'
ntu_metadata = {}
for stage in ('stage1','stage2'):
    p = comparison / f'NTU_1H26_{stage}_response.run.json'
    ntu_metadata[stage] = json.loads(p.read_text(encoding='utf-8'))
inputs = [Path('section_capture/packages.py'),Path('section_capture/db.py'),Path('section_capture/one_shot_view.py'),Path('section_capture/section_matcher.py'),Path('section_capture/openrouter.py'),Path('workflow/export_stage1.py'),Path('workflow/generate_stage2.py'),Path('section_capture/valuation_policy.py')]
inputs += list(Path('prompts').glob('*/12-analyst-reading-brief/v1.1.0/prompt.md'))
manifest = [{'path':str(p).replace('\\','/'),'sha256':digest(ROOT/p)} for p in inputs]
after = digest(DB)
assert before == after, 'Database changed during inspection'
result = dict(recorded_utc=datetime.now(timezone.utc).isoformat(),scope='Offline workload inspection; not a financial evaluation or a fresh model benchmark',database_sha256_before=before,database_sha256_after=after,database_unchanged=True,reports=summary,sections=section_details,enabled_guardrail_count=len(rules),guardrail_scope_counts=dict(collections.Counter(f"{r['sector']}:{r['stage']}" for r in rules)),ntu_saved_comparison_metadata=ntu_metadata,input_code_and_prompt_hashes=manifest)
(OUT/'workload_metrics.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(dict(reports=summary,section_count=len(rows),largest_sections=sorted(section_details,key=lambda s:s['prompt_chars'],reverse=True)[:6],guardrails=result['guardrail_scope_counts'],database_unchanged=True),indent=2,ensure_ascii=True))