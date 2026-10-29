import hashlib
from pathlib import Path

# Verify PDFs
ntu_pdf = Path("companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf")
pan_pdf = Path("companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf")

assert hashlib.sha256(ntu_pdf.read_bytes()).hexdigest() == "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc"
assert hashlib.sha256(pan_pdf.read_bytes()).hexdigest() == "62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd"
print("PDF hashes verified untouched.")
