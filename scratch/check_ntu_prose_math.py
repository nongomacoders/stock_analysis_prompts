import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pilot_dir = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T163642Z_section_prompt_paired_pilot")
p = (pilot_dir / "outputs/ntu_portfolio_new.prose.md").read_text(encoding="utf-8")
for line in p.splitlines():
    if "702" in line or "644" in line or "Other financial assets" in line:
        print(line)
