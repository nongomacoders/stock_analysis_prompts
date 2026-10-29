```json
{
  "ticker": "NTU",
  "company_name": "Nutun Limited",
  "sector": "Financial Services (collections, recovery and BPO; not a bank)",
  "valuation_status": "WITHHELD",
  "blocking_issues": [
    "Covenant headroom and liquidity runway NOT VERIFIED: R1,396m interest-bearing liabilities payable within 12 months vs cash R112m and disclosed undrawn overdraft facilities R475m; management's '~R0.8bn unutilised facilities' (physical p.5) is not reconciled to disclosed facilities (physical p.14). No covenant ratios, security cover, LTV or refinancing schedule disclosed. Evidence needed: facility-by-schedule maturity, covenant definitions/headroom, refinancing plan, going-concern support.",
    "ERC methodology and actual-vs-expected collections NOT VERIFIED: ERC R8,366m (physical p.3) vs PBD carrying R4,489m; no collection-curve, discount-rate derivation, vintage/cohort or sensitivity disclosure. Evidence needed: ERC schedule, assumptions, actual vs expected reconciliation.",
    "PBD impairment sustainability NOT VERIFIED: cumulative impairment gain R431m (physical p.22) is being consumed; H1 FY2026 historical-book loss R191m already exceeds FY2025 R182m (physical p.24). No gross ECL charge vs favourable re-estimate split, write-offs, recoveries or FX. Evidence needed: full ECL movement note.",
    "PBD amortisation/cash-flow bridge NOT VERIFIED: CODM amortisation R597m footnote (physical p.31) is ambiguously presented; cash-flow 'purchased book debts' movement R182m (physical p.12) does not reconcile to note 1.1 net collections less additions (R728m - R382m = R346m). Evidence needed: sign convention and cash-flow bridge.",
    "Trade receivables provisioning NOT VERIFIED: 0.00% ELR on 30+ and 61-90 day buckets at 31 Mar 2026 (physical p.25) vs positive ELR at 30 Sep 2025; no concentration disclosure; R395m financial vs R374m trade table vs R497m SoFP not reconciled. Evidence needed: provision matrix policy, historical loss experience, top-client concentration.",
    "Other financial assets Level 3 valuation NOT VERIFIED: R644m FVTPL at 16% discount rate (physical p.28); no sensitivity analysis; retraction risk disclosed (physical p.13). Evidence needed: hierarchy inputs, cash-flow assumptions, sensitivity.",
    "Revenue sustainability and DTI incentives NOT VERIFIED: Australia revenue R27m vs R74m (-64%) unexplained (physical p.17); DTI incentive uncertainty unquantified (physical p.5). Evidence needed: contract wins/losses, FX effects, DTI contribution.",
    "Tax and DTA recoverability NOT VERIFIED: tax credit R29m on R92m loss (effective -31.5%); DTA R173m (physical pp.8-9); no tax note captured. Evidence needed: current/deferred split, DTA recognition basis.",
    "Audit assurance and governance NOT VERIFIED: H1 FY2026 statements unaudited and unreviewed by auditors (physical pp.6-7); board 'transition' unexplained (physical p.7); no SENS announcements supplied. Evidence needed: review statement, SENS, strategic-review disclosure.",
    "NCA fee/rate caps and vintage delinquency roll rates NOT VERIFIED: no disclosure in captured pages.",
    "TC Global Finance residual exposure NOT VERIFIED: R47m FY2025 impairment; carrying value not separately disclosed (physical p.35).",
    "Subsequent SENS and post-balance-sheet events NOT VERIFIED: Note 9 (physical p.36) is a bare IAS 10 statement; no SENS supplied.",
    "Fair value of interest-bearing liabilities swing NOT VERIFIED: 30 Sep 2025 fair value R3,468m vs carrying R3,807m (R339m deficit); 31 Mar 2026 fair value R3,769m vs carrying R3,743m (R26m surplus) (physical p.27). Evidence needed: interest-rate risk note, fixed/floating split, hedge accounting."
  ],
  "valuation_checks": [
    {
      "check_id": "historical_cash_flow",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "Cash roll-forward passes: opening R107m + net increase R6m + FX R0m = closing R113m; SoFP cash R112m + held-for-sale R1m = R113m (physical pp.8, 12). However, 'purchased book debts' operating-asset movement R182m (physical p.12) does not reconcile to note 1.1 net cash collections R728m less additions R382m = R346m (physical p.13). Cash-flow line 'Net cash generated/(utilised) by investing activities R178m' is mislabelled (should be financing). No gross write-offs, bad-debt recoveries or dividends paid separately disclosed.",
      "reconciliations": []
    },
    {
      "check_id": "forecast_cash_and_debt",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "No forecast cash or debt schedule is presented in the source. Management provides only qualitative outlook (physical p.5). No forecast financial information has been reviewed by auditors (physical p.6). Cannot reconcile forecast cash and debt without a director-prepared forecast.",
      "reconciliations": []
    },
    {
      "check_id": "portfolio_rollforward",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "Principal book roll-forward (physical p.13): opening R3,975m + additions R382m - net collections R728m + CAEIR R383m - impairment R167m = R3,845m (arithmetic passes). Other financial assets (physical p.13): opening R702m + additions R28m - collections R116m + FV R30m = R644m (passes). However, ERC R8,366m (physical p.3) is not reconciled to carrying value; no collection-curve, discount-rate derivation, vintage/cohort or actual-vs-expected collection reconciliation disclosed. Portfolio rollforward of ERC NOT VERIFIED.",
      "reconciliations": []
    },
    {
      "check_id": "valuation_bridge",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "No valuation bridge is presented. Fair value of principal book approximates carrying value at 18.50% market discount rate (physical p.26); fair value of interest-bearing liabilities R3,769m vs carrying R3,743m (physical p.27). No equity-value bridge, no net-debt-to-equity reconciliation, no target derivation. Valuation bridge NOT VERIFIED.",
      "reconciliations": []
    },
    {
      "check_id": "sensitivity",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "No sensitivity analysis is disclosed for the R644m Level 3 other financial assets (16% discount rate, physical p.28), the R3,845m principal book (18.50% market rate, physical p.26), the R431m cumulative impairment gain, or the R4,016m interest-bearing liabilities. No macro scenario weightings disclosed. Sensitivity NOT VERIFIED.",
      "reconciliations": []
    },
    {
      "check_id": "earnings_and_shares",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "Share count and EPS arithmetic verified: net shares 780,651,033 (physical p.16); weighted average 782.1m; headline loss R63m / 782.1m = -8.1c (physical pp.9, 18). NAV = R1,329m / 780.651m = R1.70 (physical pp.8, 16). However, earnings quality is NOT VERIFIED: core EBITDA R790m excludes PBD amortisation R597m and net finance costs (physical p.31); no full add-back itemisation; tax credit R29m on R92m loss unexplained; DTA R173m recoverability unverified. Earnings-and-shares check NOT VERIFIED overall.",
      "reconciliations": []
    },
    {
      "check_id": "financing_and_terminal",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "Interest-bearing liabilities R4,016m including overdrafts; R1,396m payable within 12 months; R2,620m thereafter (physical p.14). Undrawn overdraft facilities R475m (physical p.14). Management claims ~R0.8bn unutilised facilities (physical p.5) but only R475m is disclosed; remainder unreconciled. 100% of principal book R3,845m pledged, plus trade receivables and cash (physical pp.13, 15). No covenant ratios, LTV, DSCR, security cover or borrowing-base headroom disclosed. Going-concern statement bare (physical p.36). No terminal debt policy or refinancing plan disclosed. Financing and terminal NOT VERIFIED.",
      "reconciliations": []
    }
  ],
  "target_price_zar": null,
  "recommendation": null,
  "rating_bands": null,
  "implied_upside_pct": null,
  "forward_dividend_yield_pct": null,
  "projected_12m_tsr_pct": null
}
```

## Historical facts with physical source pages

**Business model (physical pp.3, 13, 21).** Nutun is a collections/recovery and BPO group, not a bank. The IFRS statements contain no gross advances, NIM, CLR or IFRS 9 Stage 1/2/3 migration for a traditional loan book. The core credit asset is the Purchased Book Debt (PBD) / Right to Collect (RTC) portfolio.

**PBD carrying value (physical pp.13, 22).** Principal book gross carrying amount R3,414m; cumulative impairment gain R431m; net carrying value R3,845m. Other financial assets at FVTPL R644m. Total PBD R4,489m. ERC R8,366m (physical p.3). The R431m is a positive cumulative impairment gain, not a loss reserve; gross + gain = net. 12.6% = gain/gross, not coverage.

**POCI classification (physical p.21).** Principal book portfolios are purchased credit-impaired (POCI / Stage 3) at initial recognition; classification does not change subsequently. No Stage 1/2 migration.

**Impairment decomposition (physical p.24).** H1 FY2026 net impairment loss R167m = acquired +R24m gain + historical -R191m loss. H1 FY2025 net loss R173m = acquired -R96m loss + historical -R77m loss. FY2025 net loss R199m = acquired +R156m gain + historical -R182m loss. Historical-book loss in H1 FY2026 (R191m) already exceeds FY2025 (R182m).

**IFRS net income from PBD (physical p.9).** R69m = CAEIR imputed interest R383m - interest expense R177m - impairment R167m + FV movements R30m. Arithmetic passes.

**CODM amortisation (physical p.31).** R597m footnote components: CAEIR R383m, impairment R167m, net cash collections R728m, FV R30m, cash collections R116m. Printed arithmetic is ambiguous; approximately reconciles as R728m + R167m - R383m + R116m - R30m = R598m (R1m rounding). Sign convention requires clarification.

**Income statement (physical p.9).** Revenue R711m (H1 FY2025 R745m); cost of revenue R385m (R352m); gross profit from services R326m (R393m); operating costs R445m (R560m); net finance charge R39m (R52m); loss before tax R92m (R161m); tax credit R29m (R39m); loss from continuing operations R63m (R122m); basic loss per share -8.1c (-8.2c total operations).

**Cash flow (physical p.12).** Opening cash R107m + net increase R6m + FX R0m = closing R113m. SoFP cash R112m + held-for-sale R1m = R113m. Net cash utilised by operating activities R111m. Line 'Net cash generated/(utilised) by investing activities R178m' is mislabelled (should be financing).

**Funding (physical pp.14-15).** Total interest-bearing liabilities including overdrafts R4,016m; senior debt R3,547m; subordinated debt R196m; bank overdrafts R273m. Payable within 12 months R1,396m; thereafter R2,620m. Total undrawn overdraft facilities R475m. Facility rates: 3-month JIBAR + 2.8% to 5.2%; Prime - 0.25% to 0.35%; maturities to 2032.

**Encumbrance (physical pp.13, 15).** Purchased book debts R3,845m pledged as security; trade and other receivables and cash also pledged. No unpledged collateral buffer disclosed.

**Trade receivables (physical pp.22, 25).** Financial trade and other receivables gross R395m, allowance R5m, net R390m. Trade receivables table gross R374m, allowance R5m, net R369m. SoFP trade and other receivables R497m (includes R102m non-financial prepayments/VAT/deposits). ELR matrix at 31 Mar 2026: 0.00%/0.00%/0.00%/100.00%, total 1.34%; at 30 Sep 2025: 0.06%/0.19%/6.67%/81.82%, total 2.75%.

**Other financial assets (physical pp.26-28).** R644m Level 3 FVTPL. Discount rate 16% (31 Mar 2025: 12.93%; 30 Sep 2025: 16%). FV gain R30m (H1 FY2025 R74m; FY2025 R114m). No sensitivity analysis. Retraction risk disclosed.

**Fair value of interest-bearing liabilities (physical p.27).** 31 Mar 2026: carrying R3,743m, fair value R3,769m (R26m surplus). 30 Sep 2025: carrying R3,807m, fair value R3,468m (R339m deficit). 31 Mar 2025: carrying R3,407m, fair value R3,428m (R21m surplus).

**Equity and shares (physical pp.8, 16, 18).** Total equity R1,329m; NCI nil. Shares in issue 784,313,242; treasury 3,662,209; net 780,651,033. NAV per share R1.70. Weighted average shares 782.1m. Headline loss R63m / 782.1m = -8.1c.

**Revenue geography (physical p.17).** South Africa R159m (R188m); Australia R27m (R74m, -64%); UK R303m (R259m, +17%); US R212m (R224m, -5%); Other R10m (nil). CODM total revenue R1,599m includes PBD gross revenue R888m; not IFRS revenue.

**Audit and governance (physical pp.6-7).** H1 FY2026 statements unaudited and unreviewed by auditors; director responsibility. FY2025 comparatives audited. Board changes 1 Jan 2026: Ian Kirk resigned; Jonathan Jawno appointed Executive Chairman 'to oversee the transition of the business'; Albertinah Kekana resigned; Megandra Naidoo appointed; Robert Amoils and Ruben Moggee appointed joint CEOs.

**Subsequent events (physical p.36).** Note 9: directors not aware of any material IAS 10 events between period end and approval date. No SENS announcements supplied.

**Mobalyz/SAT (physical p.35).** Mobalyz management fee terminated. SAT loan claims settlement R176m full and final; no further amounts outstanding.

**TC Global Finance (physical pp.6, 35).** R47m impairment FY2025; equity accounted loss R1m H1 FY2026 vs R43m H1 FY2025. Carrying value within R87m equity accounted investments; not separately disclosed.

## Evidence and corrections needed

1. **Covenant and liquidity schedule:** facility-by-facility maturity, covenant definitions (interest cover, LTV, DSCR, security cover, borrowing-base), headroom, and reconciliation of the claimed ~R0.8bn unutilised facilities to the disclosed R475m undrawn overdrafts.
2. **ERC methodology:** collection-curve assumptions, discount-rate derivation, vintage/cohort data, actual-vs-expected collections, and sensitivity.
3. **Full ECL movement note:** gross ECL charge vs favourable re-estimate gain, write-offs, recoveries, FX and transfers, restated for H1 FY2025 and FY2025.
4. **PBD amortisation and cash-flow bridge:** sign convention for the R597m CODM footnote; reconciliation of the R182m cash-flow 'purchased book debts' movement to note 1.1 net collections less additions (R346m).
5. **Trade receivables provisioning policy:** basis for 0.00% ELR on 30+ and 61-90 day buckets at 31 Mar 2026; historical loss experience by bucket; top-client concentration; reconciliation of R395m/R374m/R497m.
6. **Other financial assets Level 3:** hierarchy inputs, cash-flow assumptions, sensitivity to discount rate and collections, retraction terms.
7. **Revenue drivers:** Australia decline (-64%) and UK growth (+17%) explanation; DTI incentive contribution and contingency.
8. **Tax note:** current/deferred split, DTA recognition basis and recoverability.
9. **Audit review statement and SENS:** confirmation of review status; all SENS announcements after 31 Mar 2026 including refinancing, covenant waivers, disposals, recapitalisation; nature of the 'transition of the business'.
10. **NCA compliance and vintage roll rates:** NCA fee/rate cap analysis; vintage delinquency roll rates or collection curves for the PBD book.
11. **TC Global Finance:** carrying value, residual impairment risk, share of loss.
12. **Interest-rate risk note:** fixed/floating split, hedge accounting, JIBAR/Prime sensitivity, reconciliation of the R365m fair-value swing on interest-bearing liabilities.
13. **Cash-flow label correction:** reclassify R178m 'investing' to financing; provide corrected statement.

**Process note:** Stage 2 completion could not finish within its budget. This is a process limitation, not proof of missing disclosure. The historical accounting above is reconstructed from the supplied primary source; forward valuation remains withheld pending resolution of the material dependencies listed. No target, rating, upside, dividend yield, TSR or recommendation is published.