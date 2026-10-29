import sys, json, hashlib, sqlite3, shutil
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()
RUN = ROOT / 'companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T175621Z_codex_max_comparison'
CALC = RUN / 'calculations'
CALC.mkdir(exist_ok=True)

def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

manifest = json.loads((RUN / 'inputs/manifest.json').read_text(encoding='utf-8'))

verification = {
    'checked_utc': datetime.now(timezone.utc).isoformat(),
    'run_dir': str(RUN),
    'files': [],
    'source_pdf': None,
    'sqlite_production_checks': {}
}

all_files_match = True
for f in manifest.get('files', []):
    orig = Path(f['original'])
    saved = RUN / f['saved']
    orig_match = (digest(orig) == f['sha256'])
    saved_match = (digest(saved) == f['sha256'])
    if not (orig_match and saved_match):
        all_files_match = False
    verification['files'].append({
        'original': str(orig),
        'saved': f['saved'],
        'sha256': f['sha256'],
        'original_matches': orig_match,
        'saved_matches': saved_match
    })

pdf_info = manifest['sources'][0]
pdf_path = Path(pdf_info['path'])
pdf_sha = digest(pdf_path)
pdf_matches = (pdf_sha == pdf_info['sha256'] and pdf_sha == '9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc')

verification['source_pdf'] = {
    'path': str(pdf_path),
    'sha256': pdf_sha,
    'matches_expected': pdf_matches
}

conn = sqlite3.connect('file:documents/analysis.sqlite?mode=ro', uri=True)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
rep = cur.execute("SELECT * FROM reports WHERE sha256=?", (pdf_sha,)).fetchone()
verification['sqlite_production_checks']['report_row_exists'] = (rep is not None)
verification['sqlite_production_checks']['target_price_zar'] = rep['target_price_zar'] if rep else None
verification['sqlite_production_checks']['recommendation'] = rep['recommendation'] if rep else None

guardrails = cur.execute("SELECT rule_code, enabled FROM sector_guardrails ORDER BY rule_code").fetchall()
verification['sqlite_production_checks']['active_guardrails_count'] = len(guardrails)
conn.close()

(RUN / 'independent_verification.json').write_text(json.dumps(verification, indent=2), encoding='utf-8')
print("Verification complete. All baseline files match:", all_files_match, "PDF matches:", pdf_matches)
print("Production report target:", verification['sqlite_production_checks']['target_price_zar'], "rec:", verification['sqlite_production_checks']['recommendation'])
print("Active guardrails count:", len(guardrails))
