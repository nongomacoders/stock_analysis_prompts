from pathlib import Path

out_dir = Path("scratch/extracted_afs")

print("=== NOTE 22 LEASES FULL ===")
print((out_dir / "p55_note22_leases.txt").read_text(encoding="utf-8"))

print("\n=== NOTE 23 BORROWINGS CONTINUED ===")
print((out_dir / "p56_note23_borrowings.txt").read_text(encoding="utf-8")[1200:3000])

print("\n=== NOTE 24 PAYABLES SCF PARAGRAPH ===")
p57 = (out_dir / "p57_note24_payables_scf.txt").read_text(encoding="utf-8")
print(p57[1000:2500])
