# REIT & Listed Property Sector Companies

Scaffold directory for Real Estate Investment Trusts (REITs), listed property funds, and property development holding companies (e.g. Growthpoint Properties `GRT`, Redefine Properties `RDF`, Vukile Property Fund `VKE`, Hyprop Investments `HYP`, Attacq `ATT`, Fortress Real Estate `FFB`, Resilient REIT `RES`, Equites Property Fund `EQU`).

### Core Forensic & Valuation Focus
- **Distributable Income / DIPS**: SA REIT Best Practice Recommendations (BPR), payout ratio on distributable income, and reconciliation to IFRS EPS/HEPS.
- **Loan-to-Value (LTV) & Capital Structure**: Look-through LTV, debt maturity profile, interest rate hedging ratio (typically >70%), average cost of debt, and interest cover ratio (ICR) covenant headroom.
- **Property Portfolio Metrics**: Like-for-like Net Property Income (NPI) growth, Weighted Average Lease Expiry (WALE), contractual rental escalations vs tenant retention, vacancies across sub-sectors (Retail, Logistics/Industrial, Office, Residential).
- **Valuation & Fair Value Adjustments**: Exit capitalization rates (cap rates), discount rates, reversionary yields, net asset value (NAV) discounts/premiums.

Use `new_company.py` to initialize a new company hub:
```powershell
python new_company.py <TICKER> --sector reit --name "<Company Name>"
```
