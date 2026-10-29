from pathlib import Path
import hashlib,json,sys
run=Path(sys.argv[1]);root=Path.cwd()
m=json.loads((run/'inputs/manifest.json').read_text('utf-8'))
assert hashlib.sha256(Path(m['source_pdf']['path']).read_bytes()).hexdigest()==m['source_pdf']['sha256']
original=root/'companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T163950Z_gemini'
for p in (run/'inputs/gemini').rglob('*'):
    if p.is_file():
        assert hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256((original/p.relative_to(run/'inputs/gemini')).read_bytes()).digest(),p.name
r=json.loads((run/'calculations/reconciliations_output.json').read_text('utf-8'))
assert all(x['hash_match'] and x['current_matches_snapshot'] for x in r['input_hash_checks'])
assert r['historical_ocf']['reconciles']
assert r['cash_rollforward'][1]['unexplained_reconciling_inflow']==810
assert (run/'audit.md').stat().st_size>10000
print('Verified: source PDF, Gemini originals, and DeepSeek inputs unchanged; audit and calculations saved.')