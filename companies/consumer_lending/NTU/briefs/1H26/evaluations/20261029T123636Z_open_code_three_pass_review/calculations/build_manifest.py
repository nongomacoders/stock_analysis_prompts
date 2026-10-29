import sys, json, hashlib
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"C:\Users\diond\Desktop\Projects\stock_analysis_prompts")
RUN = Path(r"C:\Users\diond\Desktop\Projects\stock_analysis_prompts\companies\consumer_lending\NTU\briefs\1H26\evaluations\20261029T123636Z_open_code_three_pass_review")
ORIG = ROOT / "companies/consumer_lending/NTU/briefs/1H26/evaluations/20261029T112944Z_three_pass_experiment"
RES = ROOT / "companies/consumer_lending/NTU/briefs/1H26/evaluations/20261029T114212Z_three_pass_pan_resume"
COD = ROOT / "companies/consumer_lending/NTU/briefs/1H26/evaluations/20261029T121151Z_codex_three_pass_review"
CH = ROOT / "workflow/changes/20261029_three_pass"

files = [
    ROOT / "companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf",
    ROOT / "companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf",
    ORIG / "plan.json",
    ORIG / "audit.md",
    ORIG / "claims.json",
    ORIG / "findings.json",
    ORIG / "calculations.json",
    ORIG / "closure_comparison.json",
    ORIG / "metrics.json",
    ORIG / "input_manifest.json",
    ORIG / "outputs/ntu_assets_meaning.md",
    ORIG / "outputs/ntu_assets_movement.md",
    ORIG / "outputs/ntu_assets_why.md",
    ORIG / "outputs/ntu_assets_why.validation.json",
    ORIG / "outputs/ntu_assets_single.md",
    ORIG / "outputs/ntu_assets_single.validation.json",
    ORIG / "outputs/pan_dense_meaning.md",
    ORIG / "outputs/pan_dense_movement.md",
    RES / "comparison.md",
    RES / "combined_comparison.json",
    RES / "audit.md",
    RES / "plan.json",
    RES / "preservation.json",
    RES / "metrics.json",
    RES / "attempts.json",
    RES / "accepted_attempts.json",
    RES / "status.json",
    RES / "execution.json",
    RES / "input_manifest.json",
    RES / "outputs/pan_dense_why.md",
    RES / "outputs/pan_dense_why_attempt1.md",
    RES / "outputs/pan_dense_why.validation.json",
    RES / "outputs/pan_dense_single.md",
    RES / "outputs/pan_dense_single_attempt1.md",
    RES / "outputs/pan_dense_single.validation.json",
    RES / "requests/pan_dense_why_attempt1.md",
    RES / "gemini/review_prompt.md",
    COD / "audit.md",
    COD / "findings.json",
    COD / "pan_question_comparison.json",
    CH / "gemini_prompt.md",
    CH / "gemini_review.md",
]

out = []
for p in files:
    raw = p.read_bytes()
    out.append({"path": str(p), "sha256": hashlib.sha256(raw).hexdigest()})

manifest = RUN / "input_manifest.json"
manifest.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"wrote {manifest} with {len(out)} entries")
# re-verify
bad = 0
for e in out:
    if hashlib.sha256(Path(e["path"]).read_bytes()).hexdigest() != e["sha256"]:
        bad += 1
print("bad:", bad)
