import pdfplumber
from pathlib import Path

afs_pdf = Path("companies/retail/DCP/sources/completed/FY26/1780031707-FY2026AnnualFinancialStatements.pdf")

with pdfplumber.open(afs_pdf) as pdf:
    for p_num in range(1, 9):
        text = pdf.pages[p_num - 1].extract_text() or ""
        if "dividend" in text.lower():
            print(f"=== PAGE {p_num} ===")
            for line in text.splitlines():
                if "dividend" in line.lower() or "cents" in line.lower():
                    print(f"  {line}")
