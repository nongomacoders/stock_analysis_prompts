import os
import json
from pathlib import Path

pilot_dir = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T163642Z_section_prompt_paired_pilot")

print("Files in pilot directory:")
for p in sorted(pilot_dir.rglob("*")):
    if p.is_file():
        rel = p.relative_to(pilot_dir)
        print(f"{rel} ({p.stat().st_size} bytes)")
