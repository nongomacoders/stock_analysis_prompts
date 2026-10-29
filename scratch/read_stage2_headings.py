from pathlib import Path

stage2_path = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T081850Z_codex_workload_comparison/outputs/stage2.md")
content = stage2_path.read_text(encoding="utf-8")
print(f"Total characters: {len(content)}")
print(f"Total lines: {len(content.splitlines())}")

# Let's print the table of contents / headings
for i, line in enumerate(content.splitlines()):
    if line.startswith("#"):
        print(f"Line {i+1}: {line}")
