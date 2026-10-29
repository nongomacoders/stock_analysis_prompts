import pdfplumber
from pathlib import Path

afs_pdf = Path("companies/retail/DCP/sources/completed/FY26/1780031707-FY2026AnnualFinancialStatements.pdf")

with pdfplumber.open(afs_pdf) as pdf:
    # Note 21 is around physical page 54
    p54 = pdf.pages[53].extract_text()
    print("=== NOTE 21 (PHYSICAL PAGE 54) ===")
    print(p54[:1500])
