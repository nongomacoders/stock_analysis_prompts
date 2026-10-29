from pathlib import Path

stage1_path = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T081850Z_codex_workload_comparison/outputs/stage1.md")

lines = stage1_path.read_text(encoding="utf-8").splitlines()
print(f"Total lines in stage1.md: {len(lines)}")

print("\n--- Headings in stage1.md ---")
for i, line in enumerate(lines):
    if line.startswith("#"):
        print(f"Line {i+1}: {line}")
