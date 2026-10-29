import sys
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pilot_dir = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T163642Z_section_prompt_paired_pilot")

for case in ["ntu_portfolio", "ntu_shared_page", "pan_apm", "pan_operations"]:
    val = json.loads((pilot_dir / f"outputs/{case}_new.validation.json").read_text(encoding="utf-8"))
    print(f"\n==================== CASE: {case} (NEW QUESTIONS) ====================")
    for q in val.get("questions", []):
        if q.get("status") == "open":
            print(f"ID: {q.get('question_id')}")
            print(f"  Priority: {q.get('priority')}")
            print(f"  Target: {q.get('target_section')} in {q.get('target_document')}")
            print(f"  Question: {q.get('question')}")
            print(f"  Evidence required: {q.get('evidence_required')}")
            print(f"  Closure condition: {q.get('closure_condition')}")
