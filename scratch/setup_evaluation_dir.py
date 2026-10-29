import hashlib
import json
import shutil
from pathlib import Path

eval_dir = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T092808Z_gemini")
inputs_dir = eval_dir / "inputs"
calcs_dir = eval_dir / "calculations"

inputs_dir.mkdir(parents=True, exist_ok=True)
calcs_dir.mkdir(parents=True, exist_ok=True)

source_trial_dir = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T081850Z_codex_workload_comparison")

files_to_copy = [
    (source_trial_dir / "outputs" / "stage1.md", "stage1.md"),
    (source_trial_dir / "outputs" / "stage2.md", "stage2.md"),
    (source_trial_dir / "outputs" / "publication_assessment.json", "publication_assessment.json"),
    (source_trial_dir / "comparison_metrics.json", "comparison_metrics.json"),
    (source_trial_dir / "status.json", "status.json"),
    (source_trial_dir / "inputs" / "manifest.json", "trial_manifest.json"),
    (source_trial_dir / "inputs" / "DCP_FY26_stage1_audit_response.md", "baseline_stage1.md"),
    (source_trial_dir / "inputs" / "DCP_FY26_stage2_valuation_note.md", "baseline_stage2.md"),
]

manifest = {
    "evaluation_utc": "2026-10-28T09:28:08Z",
    "evaluator": "gemini",
    "ticker": "DCP",
    "period": "FY26",
    "source_trial": str(source_trial_dir.resolve()),
    "source_pdfs": [
        {
            "filename": "1780031707-FY2026AnnualFinancialStatements.pdf",
            "path": "companies/retail/DCP/sources/completed/FY26/1780031707-FY2026AnnualFinancialStatements.pdf",
            "sha256": "f346d2001b093345157587cc62dbc998c9841def5ba93c0f55a3b677dc18c0cb",
            "pages": 87
        },
        {
            "filename": "1780031786-FY2026AnalystPresentation.pdf",
            "path": "companies/retail/DCP/sources/completed/FY26/1780031786-FY2026AnalystPresentation.pdf",
            "sha256": "6cd395850b7a642b19ecd5e1c1b5f6eb0d00d15d40374d72d5383b661f285f06",
            "pages": 40
        },
        {
            "filename": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf",
            "path": "companies/retail/DCP/sources/completed/FY26/1785744572-DIS-CHEMIR2026INTERACTIVE.pdf",
            "sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6",
            "pages": 132
        }
    ],
    "preserved_files": []
}

for src, dest_name in files_to_copy:
    dest_path = inputs_dir / dest_name
    shutil.copy2(src, dest_path)
    sha = hashlib.sha256(dest_path.read_bytes()).hexdigest()
    manifest["preserved_files"].append({
        "original_path": str(src.resolve()),
        "preserved_path": str(dest_path.resolve()),
        "filename": dest_name,
        "sha256": sha,
        "bytes": dest_path.stat().st_size
    })

(inputs_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

# Copy calculation script and run it to output
shutil.copy2("scratch/run_all_reconciliations.py", calcs_dir / "reconciliations.py")
reconciliations_text = Path("scratch/run_all_reconciliations.py").read_text(encoding="utf-8")

import subprocess
res = subprocess.run([".venv/Scripts/python.exe", str(calcs_dir / "reconciliations.py")], capture_output=True, text=True)
(calcs_dir / "reconciliation_output.json").write_text(res.stdout, encoding="utf-8")

print("Preservation completed successfully.")
