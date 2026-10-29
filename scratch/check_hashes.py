import hashlib
from pathlib import Path

files = [
    Path("companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf"),
    Path("companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf")
]

for p in files:
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    print(f"{p.name}: {h}")
