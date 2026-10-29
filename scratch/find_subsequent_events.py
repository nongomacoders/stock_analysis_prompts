import pdfplumber
from pathlib import Path

afs_pdf = Path("companies/retail/DCP/sources/completed/FY26/1780031707-FY2026AnnualFinancialStatements.pdf")

with pdfplumber.open(afs_pdf) as pdf:
    for page_idx, page in enumerate(pdf.pages):
        text = page.extract_text() or ""
        if "31. Events after the reporting date" in text or "31. Subsequent" in text or "Subsequent events" in text or "Events after the reporting" in text:
            print(f"Subsequent events found on physical page {page_idx + 1}")
            print(text[:1500])
