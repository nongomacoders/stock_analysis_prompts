import json
from pathlib import Path

pilot_dir = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T163642Z_section_prompt_paired_pilot")
v = json.loads((pilot_dir / "outputs/ntu_portfolio_new.validation.json").read_text(encoding="utf-8"))
print(json.dumps(v, indent=2)[:1000])
