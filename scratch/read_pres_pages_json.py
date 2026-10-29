import json
from pathlib import Path

pages_json = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T081850Z_codex_workload_comparison/source_pages/6cd395850b7a642b19ecd5e1c1b5f6eb0d00d15d40374d72d5383b661f285f06.json")
data = json.loads(pages_json.read_text(encoding="utf-8"))

for item in data:
    p = item["physical_page"]
    if p in [16, 19, 21, 23, 25, 27, 28]:
        print(f"=== PHYSICAL PAGE {p} ===")
        print(item["text"][:1000])
        print("\n" + "="*40 + "\n")
