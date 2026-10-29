import os
import sys
import json
import shutil
import hashlib
from pathlib import Path

# Paths
base_dir = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations")
eval_name = "20261028T170032Z_gemini"
eval_dir = base_dir / eval_name
inputs_dir = eval_dir / "inputs"
calc_dir = eval_dir / "calculations"

inputs_dir.mkdir(parents=True, exist_ok=True)
calc_dir.mkdir(parents=True, exist_ok=True)

# Pilot directory
pilot_dir = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T163642Z_section_prompt_paired_pilot")

# Copy key files from pilot into inputs_dir
files_to_copy = [
    "RUN_SUMMARY.md",
    "comparison.json",
    "findings.json",
    "audit.md",
    "calls.csv",
    "metrics.json",
    "plan.json",
    "closure_checks.json",
    "inputs/ntu_portfolio.json",
    "inputs/ntu_portfolio_new_prompt.md",
    "inputs/ntu_portfolio_old_prompt.md",
    "inputs/ntu_shared_page.json",
    "inputs/ntu_shared_page_new_prompt.md",
    "inputs/ntu_shared_page_old_prompt.md",
    "inputs/pan_apm.json",
    "inputs/pan_apm_new_prompt.md",
    "inputs/pan_apm_old_prompt.md",
    "inputs/pan_operations.json",
    "inputs/pan_operations_new_prompt.md",
    "inputs/pan_operations_old_prompt.md",
    "outputs/ntu_portfolio_new.md",
    "outputs/ntu_portfolio_old.md",
    "outputs/ntu_shared_page_new.md",
    "outputs/ntu_shared_page_old.md",
    "outputs/pan_apm_new.md",
    "outputs/pan_apm_old.md",
    "outputs/pan_operations_new.md",
    "outputs/pan_operations_old.md",
    "outputs/ntu_portfolio_new.validation.json",
    "outputs/ntu_portfolio_old.validation.json",
    "outputs/ntu_shared_page_new.validation.json",
    "outputs/ntu_shared_page_old.validation.json",
    "outputs/pan_apm_new.validation.json",
    "outputs/pan_apm_old.validation.json",
    "outputs/pan_operations_new.validation.json",
    "outputs/pan_operations_old.validation.json",
]

manifest = []

for rel_p in files_to_copy:
    src = pilot_dir / rel_p
    dst = inputs_dir / Path(rel_p).name
    if src.exists():
        shutil.copy2(src, dst)
        h = hashlib.sha256(src.read_bytes()).hexdigest()
        manifest.append({
            "original_path": str(src).replace("\\", "/"),
            "preserved_path": str(dst).replace("\\", "/"),
            "sha256": h,
            "bytes": src.stat().st_size
        })

(inputs_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(f"Copied {len(manifest)} files to inputs/ and generated manifest.json")
