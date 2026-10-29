import json
from pathlib import Path

pages_json = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T081850Z_codex_workload_comparison/source_pages/6cd395850b7a642b19ecd5e1c1b5f6eb0d00d15d40374d72d5383b661f285f06.json")
data = json.loads(pages_json.read_text(encoding="utf-8"))

print("Keys in source_pages json:", len(data))
# let's print page 16, 19, 21, 25
for p in [16, 19, 21, 23, 25]:
    str_p = str(p)
    if str_p in data:
        print(f"=== PAGE {p} ===")
        print(data[str_p][:800])
        print("...")
