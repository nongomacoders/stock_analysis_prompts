import sys
from pathlib import Path
import pdfplumber

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pan_path = Path("companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf")

with pdfplumber.open(pan_path) as pdf:
    p48 = pdf.pages[47]
    lines = p48.extract_text().splitlines()
    for l in lines:
        if "FY25" in l:
            print(l)
