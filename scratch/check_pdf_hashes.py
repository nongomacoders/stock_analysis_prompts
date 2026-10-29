import hashlib
from pathlib import Path

pdf_paths = [
    Path("companies/retail/DCP/sources/completed/FY26/1780031707-FY2026AnnualFinancialStatements.pdf"),
    Path("companies/retail/DCP/sources/completed/FY26/1780031786-FY2026AnalystPresentation.pdf"),
    Path("companies/retail/DCP/sources/completed/FY26/1785744572-DIS-CHEMIR2026INTERACTIVE.pdf"),
]

for p in pdf_paths:
    if p.exists():
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        print(f"{p.name}: {h}")
    else:
        print(f"MISSING: {p}")
