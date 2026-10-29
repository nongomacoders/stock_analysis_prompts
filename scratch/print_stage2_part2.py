from pathlib import Path

stage2_path = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T081850Z_codex_workload_comparison/outputs/stage2.md")
lines = stage2_path.read_text(encoding="utf-8").splitlines()

print("--- Lines 146 to 263 ---")
for idx in range(145, min(263, len(lines))):
    print(f"{idx+1}: {lines[idx]}")
