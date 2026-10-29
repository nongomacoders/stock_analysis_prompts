import sys
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pilot_dir = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T163642Z_section_prompt_paired_pilot")

for case in ["ntu_portfolio", "ntu_shared_page", "pan_apm", "pan_operations"]:
    for v in ["old", "new"]:
        val_path = pilot_dir / f"outputs/{case}_{v}.validation.json"
        val = json.loads(val_path.read_text(encoding="utf-8"))
        print(f"\n==================== {case} ({v}) ====================")
        print("ledger_valid:", val.get("ledger_valid"))
        print("errors:", val.get("errors"))
        print("questions count:", len(val.get("questions", [])))
        for q in val.get("questions", []):
            print(f"  ID: {q.get('question_id')}, status: {q.get('status')}")
            print(f"    Q: {q.get('question')[:100]}")
            print(f"    Ans: {q.get('answer')[:150]}...")
            ev = q.get("evidence", [])
            print(f"    Evidence ({len(ev)}): {[e.get('quote') for e in ev]}")
