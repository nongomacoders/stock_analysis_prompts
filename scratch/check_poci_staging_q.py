import sys
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pilot_dir = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T163642Z_section_prompt_paired_pilot")
v = json.loads((pilot_dir / "outputs/ntu_portfolio_new.validation.json").read_text(encoding="utf-8"))
for q in v.get("questions", []):
    if q.get("question_id") == "Q-b332e6c7ddfc4e8d":
        print(json.dumps(q, indent=2))
