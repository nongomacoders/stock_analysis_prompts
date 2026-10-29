from pathlib import Path

out_dir = Path("scratch/extracted_afs")

print("=== NOTE 29 GEARING (p79, p82) ===")
print((out_dir / "p79_82_note29_gearing.txt").read_text(encoding="utf-8")[:3000])

print("\n=== NOTE 31 SUBSEQUENT EVENTS (p83, p84) ===")
print((out_dir / "p83_84_note31_subsequent.txt").read_text(encoding="utf-8")[:3000])
