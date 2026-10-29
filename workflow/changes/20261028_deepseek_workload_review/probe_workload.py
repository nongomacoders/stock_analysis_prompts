from pathlib import Path
import ast
import hashlib
import json
import re
import sqlite3

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent

def load_function(path, name):
    tree = ast.parse(path.read_text(encoding='utf-8-sig'))
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    env = {'re': re}
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), 'exec'), env)
    return env[name]

extract = load_function(ROOT/'section_capture/db.py', 'extract_questions_ledger_from_response')
clean = load_function(ROOT/'workflow/export_stage1.py', 'clean_reading_brief')
probes = {
    'missing_section4': extract('### 2. Footnotes\nAnalysis without a ledger.'),
    'empty_section4': extract('### 4. Updated Open Questions Ledger\n```markdown\n\n```\n### 5. Baseline Forecast Inputs Captured Here\nNone'),
    'unstructured_replacement': extract('### 4. Updated Open Questions Ledger\n```markdown\nEverything looks fine.\n```\n### 5. Baseline Forecast Inputs Captured Here\nNone'),
    'single_question_replacement': extract('### 4. Updated Open Questions Ledger\n```markdown\n- Q2 Pending: D003 - Inspect financing.\n```\n### 5. Baseline Forecast Inputs Captured Here\nNone'),
}
assert probes['missing_section4'] is None
assert probes['empty_section4'] is None
assert probes['unstructured_replacement'] == 'Everything looks fine.'
assert 'Q1' not in probes['single_question_replacement']
conn = sqlite3.connect((ROOT/'documents/analysis.sqlite').resolve().as_uri()+'?mode=ro', uri=True)
try:
    responses = conn.execute("SELECT llm_response FROM sections WHERE llm_response IS NOT NULL AND trim(llm_response) != ''").fetchall()
finally:
    conn.close()
raw = sum(len(r[0]) for r in responses)
compacted = sum(len(clean(r[0])) for r in responses)
metrics = json.loads((OUT/'workload_metrics.json').read_text(encoding='utf-8'))
analyzed = [s for s in metrics['sections'] if s['response_chars']]
token_rows = [(s,s.get('review_metadata',{}).get('tokens',{}).get('prompt_tokens')) for s in analyzed]
token_rows = [(s,t) for s,t in token_rows if isinstance(t,int)]
result = dict(scope='Isolated existing pure functions via AST; no production imports, network, Qt or database writes',probes=probes,probe_assertions=4,recorded_analyzed_sections=len(analyzed),sections_with_prompt_token_metadata=len(token_rows),saved_section_prompt_tokens_max=max(t for _,t in token_rows),sections_above_50000_recorded_prompt_tokens=sum(t>50000 for _,t in token_rows),section_response_chars=raw,after_current_stage1_compaction_chars=compacted,chars_removed_by_existing_compaction=raw-compacted,removed_percent=round(100*(raw-compacted)/raw,2),max_to_min_analyzed_prompt_chars_ratio=round(max(s['prompt_chars'] for s in analyzed)/min(s['prompt_chars'] for s in analyzed if s['prompt_chars']),2),database_still_matches=hashlib.sha256((ROOT/'documents/analysis.sqlite').read_bytes()).hexdigest()==metrics['database_sha256_before'])
assert result['database_still_matches']
(OUT/'offline_probe_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))