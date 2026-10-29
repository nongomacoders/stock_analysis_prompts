import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pilot_dir = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T163642Z_section_prompt_paired_pilot")

for case in ["ntu_portfolio", "ntu_shared_page", "pan_apm", "pan_operations"]:
    print(f"\n==================== PROSE: {case} NEW ====================")
    new_prose = (pilot_dir / f"outputs/{case}_new.prose.md").read_text(encoding="utf-8")
    print(new_prose[:1500])
    print("\n--- [TRUNCATED FOR DISPLAY] ---")
    print(new_prose[-800:])
