import pdfplumber
from pathlib import Path

afs_pdf = Path("companies/retail/DCP/sources/completed/FY26/1780031707-FY2026AnnualFinancialStatements.pdf")

with pdfplumber.open(afs_pdf) as pdf:
    p83 = pdf.pages[82]
    # let's crop the page or extract words
    # page width and height:
    w, h = p83.width, p83.height
    # left half:
    left_half = p83.crop((0, 0, w * 0.6, h))
    print("=== LEFT HALF P83 ===")
    print(left_half.extract_text())
