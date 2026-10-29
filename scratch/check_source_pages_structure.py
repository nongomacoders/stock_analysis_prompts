import json
from pathlib import Path

pages_json = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T081850Z_codex_workload_comparison/source_pages/6cd395850b7a642b19ecd5e1c1b5f6eb0d00d15d40374d72d5383b661f285f06.json")
data = json.loads(pages_json.read_text(encoding="utf-8"))

print("Type of data:", type(data))
if isinstance(data, dict):
    print("Dict keys:", list(data.keys())[:10])
elif isinstance(data, list):
    print("List length:", len(data))
    print("First item type:", type(data[0]))
    if isinstance(data[0], dict):
        print("First item keys:", list(data[0].keys()))
