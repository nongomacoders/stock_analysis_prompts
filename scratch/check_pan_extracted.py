import sys
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pilot_dir = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T163642Z_section_prompt_paired_pilot")
data = json.loads((pilot_dir / "inputs/pan_operations.json").read_text(encoding="utf-8"))

texts = data.get("texts", [])
print(f"Number of text blocks: {len(texts)}")
for i, t in enumerate(texts):
    print(f"--- Block {i} (length {len(t)}) ---")
    lines = t.splitlines()
    for line in lines[:25]:
        print(line)
    if len(lines) > 25:
        print(f"... ({len(lines) - 25} more lines)")
