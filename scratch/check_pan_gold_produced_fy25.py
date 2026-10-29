import sys
from pathlib import Path
import pdfplumber

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pan_path = Path("companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf")

with pdfplumber.open(pan_path) as pdf:
    # Page 48 and 49
    for pno in [48, 49]:
        p = pdf.pages[pno - 1]
        lines = p.extract_text().splitlines()
        for idx, line in enumerate(lines):
            if "gold produced" in line.lower():
                print(f"p.{pno} [L{idx}]: {line}")
                if idx + 1 < len(lines):
                    print(f"p.{pno} [L{idx+1}]: {lines[idx+1]}")
                if idx + 2 < len(lines):
                    print(f"p.{pno} [L{idx+2}]: {lines[idx+2]}")
