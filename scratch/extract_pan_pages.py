import sys
from pathlib import Path
import pdfplumber

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pan_path = Path("companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf")

with pdfplumber.open(pan_path) as pdf:
    print("=== PAN Physical Pages 38-39 (APMs) ===")
    p38 = pdf.pages[37]
    p39 = pdf.pages[38]
    print("--- Page 38 ---")
    print(p38.extract_text()[:1500])
    print("--- Page 39 ---")
    print(p39.extract_text()[:2500])

    print("\n=== PAN Physical Pages 48-50 (Operations) ===")
    for pno in [48, 49, 50]:
        print(f"--- Page {pno} ---")
        p = pdf.pages[pno - 1]
        print(p.extract_text()[:1500])
