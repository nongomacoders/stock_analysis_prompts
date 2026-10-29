from pathlib import Path

out_dir = Path("scratch/extracted_afs")

print("=== P13 PNL ===")
print((out_dir / "p13_pnl.txt").read_text(encoding="utf-8")[:1000])

print("\n=== P14 BALANCE SHEET ===")
print((out_dir / "p14_balance_sheet.txt").read_text(encoding="utf-8")[:1000])

print("\n=== P17 CASH FLOW ===")
print((out_dir / "p17_cash_flow.txt").read_text(encoding="utf-8")[:1000])
