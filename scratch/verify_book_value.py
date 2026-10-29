import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

share_cap = 5410.0
total_equity = 1329.0
shares = 780.651033

print(f"Gross Share Capital per share: {share_cap / shares:.2f} ZAR")
print(f"Actual Net Book Value per share: {total_equity / shares:.2f} ZAR")
