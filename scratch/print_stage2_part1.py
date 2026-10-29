from pathlib import Path

stage2_path = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T081850Z_codex_workload_comparison/outputs/stage2.md")
lines = stage2_path.read_text(encoding="utf-8").splitlines()

print("--- Lines 40 to 145 ---")
for idx in range(40, min(145, len(lines))):
    print(f"{idx+1}: {lines[idx]}")
