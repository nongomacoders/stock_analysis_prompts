import json
from pathlib import Path

pilot_dir = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T163642Z_section_prompt_paired_pilot")

for case in ["ntu_portfolio", "ntu_shared_page", "pan_apm", "pan_operations"]:
    data = json.loads((pilot_dir / f"inputs/{case}.json").read_text(encoding="utf-8"))
    print(f"\n=== {case} ===")
    print("questions:")
    for q in data.get("questions", []):
        print(" ", q)
    print("manifest selections / section_name:")
    print("  section_name:", data.get("manifest", {}).get("section_name"))
    print("  analyst_question:", data.get("manifest", {}).get("analyst_question"))
    selections = data.get("manifest", {}).get("selections", [])
    print(f"  selections count: {len(selections)}")
    for s in selections:
        print(f"    page={s.get('page')}, content_type={s.get('content_type')}, heading={s.get('heading')}")
