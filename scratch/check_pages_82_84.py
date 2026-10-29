import pdfplumber
from pathlib import Path

afs_pdf = Path("companies/retail/DCP/sources/completed/FY26/1780031707-FY2026AnnualFinancialStatements.pdf")

with pdfplumber.open(afs_pdf) as pdf:
    for p_num in [82, 83, 84]:
        page = pdf.pages[p_num - 1]
        print(f"=== PHYSICAL PAGE {p_num} ===")
        # extract words or lines
        text = page.extract_text(layout=False)
        for line in text.splitlines():
            if any(w in line.lower() for w in ["31.", "subsequent", "event", "dividend", "restructur", "section 189", "s189", "bullet", "standard bank", "facility"]):
                print(f"  {line}")
