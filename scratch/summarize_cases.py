import json
from pathlib import Path

pilot_dir = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T163642Z_section_prompt_paired_pilot")

for case in ["ntu_portfolio", "ntu_shared_page", "pan_apm", "pan_operations"]:
    print(f"\n==================== CASE: {case} ====================")
    meta = json.loads((pilot_dir / f"inputs/{case}.json").read_text(encoding="utf-8"))
    print("Capture info:")
    print(f"  section_title: {meta.get('section_title')}")
    print(f"  pages: {meta.get('pages')}")
    print(f"  open_questions: {len(meta.get('open_questions', []))}")
    for q in meta.get("open_questions", []):
        print(f"    - {q.get('id')}: {q.get('question')} (status={q.get('status')})")
    
    old_out = (pilot_dir / f"outputs/{case}_old.md").read_text(encoding="utf-8")
    new_out = (pilot_dir / f"outputs/{case}_new.md").read_text(encoding="utf-8")
    print(f"Old output length: {len(old_out)} chars")
    print(f"New output length: {len(new_out)} chars")
