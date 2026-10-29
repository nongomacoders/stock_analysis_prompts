import json
from pathlib import Path

pilot_dir = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T163642Z_section_prompt_paired_pilot")

data = json.loads((pilot_dir / "inputs/ntu_portfolio.json").read_text(encoding="utf-8"))
print("Keys in ntu_portfolio.json:", list(data.keys()))
for k, v in data.items():
    if isinstance(v, (str, int, float, bool)):
        print(f"  {k}: {v}")
    elif isinstance(v, list):
        print(f"  {k}: list of {len(v)} items")
    elif isinstance(v, dict):
        print(f"  {k}: dict with keys {list(v.keys())}")
