"""Read-only input verification for the Gemini review of the one-pass vs three-pass experiment.
Hashes inputs, checks reuse/byte identity, request-setting parity and capture containment.
Writes input_manifest.json and input_checks.json next to the audit. No network, no model calls."""
import hashlib, json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RUN = Path(__file__).resolve().parents[1]
EV = RUN.parent
ROOT = RUN.parents[6]
ORIG = EV / "20261029T112944Z_three_pass_experiment"
NEW = EV / "20261029T114212Z_three_pass_pan_resume"
PRIOR = EV / "20261028T191648Z_codex_native_extraction_review" / "source_pages"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


manifest = {"generated_by": "scripts/verify_inputs.py", "files": []}
for base in (ORIG, NEW):
    for p in sorted(base.rglob("*")):
        if p.is_file():
            manifest["files"].append({"path": str(p.relative_to(ROOT)).replace("\\", "/"), "bytes": p.stat().st_size, "sha256": sha(p)})
for p in sorted(PRIOR.glob("*")):
    manifest["files"].append({"path": str(p.relative_to(ROOT)).replace("\\", "/"), "bytes": p.stat().st_size, "sha256": sha(p), "role": "prior render (reference only)"})
for p in sorted((RUN / "inputs").glob("*")):
    manifest["files"].append({"path": str(p.relative_to(ROOT)).replace("\\", "/"), "bytes": p.stat().st_size, "sha256": sha(p), "role": "preserved copy in this review run"})
gp = ROOT / "workflow/changes/20261029_three_pass/gemini_prompt.md"
manifest["files"].append({"path": "workflow/changes/20261029_three_pass/gemini_prompt.md", "bytes": gp.stat().st_size, "sha256": sha(gp), "role": "user handoff prompt"})
manifest["sources"] = json.loads((RUN / "source_pages/render_record.json").read_text(encoding="utf-8"))

checks = {}
# 1. plan.json recorded hashes of original files still match
plan = json.loads((NEW / "plan.json").read_text(encoding="utf-8"))
checks["plan_original_file_hashes"] = [
    {"path": o["path"].split("stock_analysis_prompts\\")[-1], "recorded": o["sha256"], "actual": sha(Path(o["path"])) if Path(o["path"]).exists() else None,
     "match": Path(o["path"]).exists() and sha(Path(o["path"])) == o["sha256"]} for o in plan["original_files"]]
checks["plan_document_hashes"] = [{"path": d["path"].split("stock_analysis_prompts\\")[-1], "match": sha(Path(d["path"])) == d["sha256"]} for d in plan["documents"]]

# 2. byte identity of reuse / canonical copies
pairs = {
    "failed_request_copy == original pan_dense_why request": (NEW / "inputs/failed_request.json", ORIG / "requests/pan_dense_why.json"),
    "new why request == original failed request (json)": (NEW / "requests/pan_dense_why_attempt1.json", ORIG / "requests/pan_dense_why.json"),
    "new why prompt md == original failed prompt md": (NEW / "requests/pan_dense_why_attempt1.md", ORIG / "requests/pan_dense_why.md"),
    "reused meaning == original meaning output": (NEW / "inputs/pan_dense_meaning.md", ORIG / "outputs/pan_dense_meaning.md"),
    "reused movement == original movement output": (NEW / "inputs/pan_dense_movement.md", ORIG / "outputs/pan_dense_movement.md"),
    "new single prompt md == frozen pan_dense_base.md": (NEW / "requests/pan_dense_single_attempt1.md", ORIG / "inputs/pan_dense_base.md"),
    "canonical why == attempt1 why": (NEW / "outputs/pan_dense_why.md", NEW / "outputs/pan_dense_why_attempt1.md"),
    "canonical single == attempt1 single": (NEW / "outputs/pan_dense_single.md", NEW / "outputs/pan_dense_single_attempt1.md"),
    "pan_dense.json capture copy == original": (NEW / "inputs/pan_dense.json", ORIG / "inputs/pan_dense.json"),
    "NTU single output copy == original": (NEW / "inputs/previous_outputs_ntu_assets_single.md", ORIG / "outputs/ntu_assets_single.md"),
    "NTU why output copy == original": (NEW / "inputs/previous_outputs_ntu_assets_why.md", ORIG / "outputs/ntu_assets_why.md"),
}
checks["byte_identity"] = {k: sha(a) == sha(b) for k, (a, b) in pairs.items()}

# 3. request settings parity across all 8 successful/failed requests
reqs = {
    "ntu_single": ORIG / "requests/ntu_assets_single.json", "ntu_meaning": ORIG / "requests/ntu_assets_meaning.json",
    "ntu_movement": ORIG / "requests/ntu_assets_movement.json", "ntu_why": ORIG / "requests/ntu_assets_why.json",
    "pan_meaning": ORIG / "requests/pan_dense_meaning.json", "pan_movement": ORIG / "requests/pan_dense_movement.json",
    "pan_why_new": NEW / "requests/pan_dense_why_attempt1.json", "pan_single_new": NEW / "requests/pan_dense_single_attempt1.json",
}
settings = {}
for k, p in reqs.items():
    r = json.loads(p.read_text(encoding="utf-8"))
    settings[k] = {x: r.get(x) for x in ("model", "temperature", "max_tokens", "provider", "reasoning", "stream")}
    settings[k]["n_messages"] = len(r["messages"])
    settings[k]["prompt_chars"] = sum(len(m["content"]) for m in r["messages"])
ref = {x: settings["ntu_single"][x] for x in ("model", "temperature", "max_tokens", "provider", "reasoning")}
checks["request_settings"] = settings
checks["request_settings_identical"] = all({x: s[x] for x in ref} == ref for s in settings.values())

# 4. capture containment: does each prompt contain the frozen source capture text?
def capture_blocks(capture_json: Path):
    j = json.loads(capture_json.read_text(encoding="utf-8"))
    out = []
    def walk(o):
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str) and len(o) > 400:
            out.append(o)
    walk(j)
    return out

contain = {}
for case, cap in (("ntu", ORIG / "inputs/ntu_assets.json"), ("pan", ORIG / "inputs/pan_dense.json")):
    blocks = capture_blocks(cap)
    for k, p in reqs.items():
        if not k.startswith(case):
            continue
        text = "".join(m["content"] for m in json.loads(p.read_text(encoding="utf-8"))["messages"])
        contain[k] = {"long_capture_strings": len(blocks), "contained": sum(1 for b in blocks if b in text)}
checks["capture_containment"] = contain

# 5. key PAN figures present in the PAN prompts (spot check of frozen capture)
figs = ["94,929", "272,310", "196,527", "25,043", "30,806", "93,724", "92,643", "2,688", "68,843", "209.3", "205,143"]
checks["pan_prompt_figures"] = {k: {f: f in "".join(m["content"] for m in json.loads(p.read_text(encoding="utf-8"))["messages"]) for f in figs}
                                for k, p in reqs.items() if k.startswith("pan")}
ntu_figs = ["4,489", "4 489", "644", "3 845", "fair value"]
checks["ntu_prompt_figures"] = {k: {f: f in "".join(m["content"] for m in json.loads(p.read_text(encoding="utf-8"))["messages"]) for f in ntu_figs}
                                for k, p in reqs.items() if k.startswith("ntu")}

(RUN / "input_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
(RUN / "input_checks.json").write_text(json.dumps(checks, indent=2), encoding="utf-8")
print(json.dumps({k: v for k, v in checks.items() if k != "request_settings"}, indent=1))
print("files hashed:", len(manifest["files"]))
