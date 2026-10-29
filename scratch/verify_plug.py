import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Physical page 8 (Balance sheet at 31 March 2026):
# Assets:
# Cash: 112
# Other investments: 81
# Tax receivables: 0
# Trade and other receivables: 497
# Assets held for sale: 4
# Purchased book debts: 4,489 (principal 3,845 + other fin assets 644)
# Other loans receivables: 5
# Equity accounted investments: 87
# Intangible assets: 67
# Property and equipment: 418
# Goodwill: 511
# Deferred tax assets: 173
# Total assets: 6,444

# Liabilities:
# Bank overdrafts: 273
# Tax payables: 5
# Trade and other payables: 221
# Provisions: 0
# Liabilities held for sale: 6
# Derivative liabilities: 9
# Interest-bearing debt: 3,743
# Lease liabilities: 345
# Deferred tax liabilities: 513
# Total liabilities: 5,115
# Total equity: 1,329

# What is "Other assets net of other liabilities" in DeepSeek's model?
# In DeepSeek's balance sheet table (FY27E):
# Other assets = 1,315
# Other liabilities = 765
# Difference = 1,315 - 765 = 550?
# But DeepSeek added 1,479!
# Where did 1,479 come from?
# Let's check:
# Total equity at H1 2026 is 1,329.
# Total equity at FY27E in DeepSeek's forecast is 1,115!
# Look at row 150 of DeepSeek's Stage 2:
# "Total equity: FY25A: 1,396 | H1 2026A: 1,329 | FY26E: 1,250 | FY27E: 1,115 | FY28E: 980"
# Look at row 190 of SOTP:
# "Adjusted Equity Value: 1,115"!
# Look at that!
# DeepSeek wanted Adjusted Equity Value to equal FY27E Total Equity (1,115)!
# Because EV minus net debt was -364, DeepSeek plugged 1,115 - (-364) = 1,479!
print("Plug calculation:")
print("FY27E Book Equity:", 1115)
print("EV less Net Debt:", -364)
print("Required plug to make Adjusted Equity equal Book Equity:", 1115 - (-364), "= 1479!")
