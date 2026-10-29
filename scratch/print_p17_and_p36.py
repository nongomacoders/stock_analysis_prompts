from pathlib import Path

out_dir = Path("scratch/extracted_afs")

print("=== P17 CASH FLOW FULL ===")
print((out_dir / "p17_cash_flow.txt").read_text(encoding="utf-8"))

print("\n=== P36 NOTE 11 HEPS ===")
print((out_dir / "p36_note11_heps.txt").read_text(encoding="utf-8"))
