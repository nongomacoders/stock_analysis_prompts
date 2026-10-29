import pdfplumber
from pathlib import Path

pres_pdf = Path("companies/retail/DCP/sources/completed/FY26/1780031786-FY2026AnalystPresentation.pdf")
iar_pdf = Path("companies/retail/DCP/sources/completed/FY26/1785744572-DIS-CHEMIR2026INTERACTIVE.pdf")

with pdfplumber.open(pres_pdf) as pdf:
    print("=== PRES PAGE 16 (Better Rewards) ===")
    print(pdf.pages[15].extract_text()[:1500])
    
    print("\n=== PRES PAGE 19 (S189 / Store rollout) ===")
    print(pdf.pages[18].extract_text()[:1500])
    
    print("\n=== PRES PAGE 21 (Wholesale) ===")
    print(pdf.pages[20].extract_text()[:1500])
    
    print("\n=== PRES PAGE 23 & 25 (Stores) ===")
    print(pdf.pages[22].extract_text()[:800])
    print("--- p25 ---")
    print(pdf.pages[24].extract_text()[:800])
