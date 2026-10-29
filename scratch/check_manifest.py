import json
from pathlib import Path

manifest_path = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T081850Z_codex_workload_comparison/inputs/manifest.json")
data = json.loads(manifest_path.read_text(encoding="utf-8"))
print("Keys in manifest:", list(data.keys()))
for k, v in data.items():
    if isinstance(v, (str, int, float, bool)):
        print(f"{k}: {v}")
    elif isinstance(v, list):
        print(f"{k}: list of length {len(v)}")
    elif isinstance(v, dict):
        print(f"{k}: dict with keys {list(v.keys())}")
