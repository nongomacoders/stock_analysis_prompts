import sys
import hashlib
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

files_to_hash = [
    r"companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf",
    r"companies/consumer_lending/NTU/briefs/1H26/NTU_1H26_stage1_audit_response.md",
    r"companies/consumer_lending/NTU/briefs/1H26/NTU_1H26_stage1_forensic_prompt.md",
    r"companies/consumer_lending/NTU/briefs/1H26/NTU_1H26_stage2_valuation_note.md",
    r"companies/consumer_lending/NTU/briefs/1H26/NTU_1H26_stage2_valuation_prompt.md"
]

manifest = {}
for f in files_to_hash:
    p = Path(f)
    if p.exists():
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        size = p.stat().st_size
        manifest[str(p).replace("\\", "/")] = {"sha256": h, "size_bytes": size}
        print(f"{p.name}: {h} ({size} bytes)")
    else:
        print(f"NOT FOUND: {f}")
