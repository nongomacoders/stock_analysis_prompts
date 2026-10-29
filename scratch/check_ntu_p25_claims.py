import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pilot_dir = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T163642Z_section_prompt_paired_pilot")

for v in ["old", "new"]:
    print(f"\n==================== NTU SHARED PAGE ({v}) ====================")
    prose = (pilot_dir / f"outputs/ntu_shared_page_{v}.prose.md").read_text(encoding="utf-8")
    for line in prose.splitlines():
        if any(w in line.lower() for w in ["first-time", "comparative", "zero", "0.00%", "restat"]):
            print(f"[{v}] {line}")
