import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Let's verify the cash flow statement lines
# Physical page 12:
# Cash utilised by operations: (50)
# Interest received: 3
# Interest paid: (225)
# Income taxes refunded: 2
# Subtotal before changes in operating assets & WC: (270)
# Decrease in operating assets: 182 (PBD: 182)
# Changes in working capital: (23) (receivables (25), payables 2)
# Net cash utilised by operating activities: (111)

# Now where did the 182 come from in PBD?
# Note 1.1: Additions = 382. Net collections = (728).
# Note 1.2: Additions = 28. Cash collections = (116).
# Total additions = 382 + 28 = 410 (which matches "Cost of acquisitions 410" on p. 3!).
# Total cash collections = 728 + 116 = 844 (net) or gross 773 + 116 = 889.
# Collections (844) - Additions (410) = 434?
# Wait! In the cash flow statement, "Decrease in operating assets: Purchased book debts" is 182!
# Why is it 182?
# Let's check:
# Operating cash flow has "Cash utilised by operations: (50)". What is in "Cash utilised by operations"?
# In standard IFRS cash flow statements, "Cash generated/(utilised) by operations" starts with operating profit/loss or profit before tax,
# and adjusts for non-cash items (D&A, imputed interest, impairment, etc.)
print("PBD analysis:")
print("Gross collections:", 773, "+ RTC:", 116, "=", 889)
print("Net collections:", 728, "+ 116 =", 844)
print("Additions:", 382, "+ 28 =", 410)
print("Difference net collections - additions:", 844 - 410, "= 434")
