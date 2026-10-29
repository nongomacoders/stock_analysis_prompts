import sys
from pathlib import Path
import pdfplumber

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pan_path = Path("companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf")

with pdfplumber.open(pan_path) as pdf:
    p48 = pdf.pages[47]
    lines = p48.extract_text().splitlines()
    for idx, l in enumerate(lines):
        if "2,654" in l:
            print(f"L{idx-2}: {lines[idx-2]}")
            print(f"L{idx-1}: {lines[idx-1]}")
            print(f"L{idx}: {lines[idx]}")
