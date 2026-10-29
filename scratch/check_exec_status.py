import json
from pathlib import Path

path = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T081850Z_codex_workload_comparison/outputs/execution_status_before_handoff.json")
data = json.loads(path.read_text(encoding="utf-8"))
print("Keys:", list(data.keys()))
for k in ["status", "stage", "model_calls", "local_open_only_fallbacks_count", "withheld"]:
    if k in data:
        print(f"{k}: {data[k]}")
