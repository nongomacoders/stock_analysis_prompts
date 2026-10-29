import sys
import shutil
import json
import hashlib
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

run_dir = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T163950Z_gemini")
inputs_dir = run_dir / "inputs"
calcs_dir = run_dir / "calculations"

inputs_dir.mkdir(parents=True, exist_ok=True)
calcs_dir.mkdir(parents=True, exist_ok=True)

files_to_preserve = [
    Path("companies/consumer_lending/NTU/briefs/1H26/NTU_1H26_stage1_audit_response.md"),
    Path("companies/consumer_lending/NTU/briefs/1H26/NTU_1H26_stage1_forensic_prompt.md"),
    Path("companies/consumer_lending/NTU/briefs/1H26/NTU_1H26_stage2_valuation_note.md"),
    Path("companies/consumer_lending/NTU/briefs/1H26/NTU_1H26_stage2_valuation_prompt.md"),
]

manifest = {
    "evaluation_run": "20261027T163950Z_gemini",
    "ticker": "NTU",
    "period": "1H26",
    "timestamp_utc": "2026-10-27T16:39:50Z",
    "timestamp_local": "2026-10-27T18:39:50+02:00",
    "evaluator": "gemini",
    "model_id": "Gemini 3.8 Flash (High)",
    "pdf_source": {
        "filename": "nutunlimitedcondensedconsolidatedafs31march2026.pdf",
        "path": "companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf",
        "sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
        "size_bytes": 1719316,
        "physical_page_count": 38,
        "verified_against_sqlite": True
    },
    "preserved_inputs": []
}

for src in files_to_preserve:
    dst = inputs_dir / src.name
    shutil.copy2(src, dst)
    h = hashlib.sha256(src.read_bytes()).hexdigest()
    manifest["preserved_inputs"].append({
        "original_path": str(src).replace("\\", "/"),
        "preserved_path": str(dst).replace("\\", "/"),
        "sha256": h,
        "size_bytes": src.stat().st_size
    })

manifest_path = inputs_dir / "manifest.json"
manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(f"Preserved {len(files_to_preserve)} files and created manifest at {manifest_path}")
