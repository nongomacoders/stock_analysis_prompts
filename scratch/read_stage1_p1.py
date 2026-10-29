from pathlib import Path

stage1_path = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T081850Z_codex_workload_comparison/outputs/stage1.md")
lines = stage1_path.read_text(encoding="utf-8").splitlines()

print("=== STAGE 1: LINES 1 - 100 ===")
for i in range(min(100, len(lines))):
    print(f"{i+1}: {lines[i]}")
