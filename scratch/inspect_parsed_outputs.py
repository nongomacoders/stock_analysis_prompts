import json
from pathlib import Path

pilot_dir = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T163642Z_section_prompt_paired_pilot")

def inspect_output(case, version):
    md_path = pilot_dir / f"outputs/{case}_{version}.md"
    content = md_path.read_text(encoding="utf-8")
    val_path = pilot_dir / f"outputs/{case}_{version}.validation.json"
    val = json.loads(val_path.read_text(encoding="utf-8")) if val_path.exists() else {}
    return content, val

for case in ["ntu_portfolio", "ntu_shared_page", "pan_apm", "pan_operations"]:
    for v in ["old", "new"]:
        c, val = inspect_output(case, v)
        print(f"\n==================== {case} ({v}) ====================")
        print(f"Validation valid: {val.get('valid')}, errors: {val.get('errors')}")
        parsed = val.get("parsed", {})
        updates = parsed.get("updates", [])
        new_q = parsed.get("new_questions", [])
        print(f"Updates ({len(updates)}):")
        for u in updates:
            print(f"  [{u.get('question_id')}] status={u.get('status')}")
            print(f"    answer: {u.get('answer')[:120]}...")
            ev = u.get("evidence", [])
            for e in ev:
                print(f"    evidence: p.{e.get('physical_page')} quote={e.get('quote')}")
        print(f"New questions ({len(new_q)}):")
        for nq in new_q:
            print(f"  [{nq.get('question_id')}] {nq.get('question')[:100]}... (pri={nq.get('priority')})")
