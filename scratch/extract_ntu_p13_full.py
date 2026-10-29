import sys
from pathlib import Path
import pdfplumber

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ntu_path = Path("companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf")

with pdfplumber.open(ntu_path) as pdf:
    p13 = pdf.pages[12]
    print(p13.extract_text())
