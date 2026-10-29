import sys
from pathlib import Path

stage2_path = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T081850Z_codex_workload_comparison/outputs/stage2.md")
stage1_path = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T081850Z_codex_workload_comparison/outputs/stage1.md")

print(f"stage2 exists: {stage2_path.exists()}, size: {stage2_path.stat().st_size}")
lines2 = stage2_path.read_text(encoding="utf-8").splitlines()
print(f"stage2 total lines: {len(lines2)}")
print("--- stage2 first 40 lines ---")
for line in lines2[:40]:
    print(line)

print("\n--- stage2 last 40 lines ---")
for line in lines2[-40:]:
    print(line)
