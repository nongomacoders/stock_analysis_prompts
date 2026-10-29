import sys
from pathlib import Path
import pdfplumber

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pan_path = Path("companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf")

with pdfplumber.open(pan_path) as pdf:
    p48 = pdf.pages[47]
    p49 = pdf.pages[48]
    print("--- Page 48 text lines ---")
    for idx, l in enumerate(p48.extract_text().splitlines()):
        if "gold" in l.lower():
            print(f"L{idx}: {l}")
    print("--- Page 49 text lines ---")
    for idx, l in enumerate(p49.extract_text().splitlines()):
        if "gold" in l.lower():
            print(f"L{idx}: {l}")
