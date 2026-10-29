import sys
from pathlib import Path
import pdfplumber

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ntu_path = Path("companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf")
pan_path = Path("companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf")

print("=== NTU Physical Page 13 ===")
with pdfplumber.open(ntu_path) as pdf:
    # Physical page 13 is index 12
    p13 = pdf.pages[12]
    print(p13.extract_text()[:2000])

print("\n=== NTU Physical Page 25 ===")
with pdfplumber.open(ntu_path) as pdf:
    # Physical page 25 is index 24
    p25 = pdf.pages[24]
    print(p25.extract_text()[:2000])
