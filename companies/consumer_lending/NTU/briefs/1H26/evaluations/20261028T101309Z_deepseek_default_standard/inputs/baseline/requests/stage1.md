# STAGE 1: INDEPENDENT COGNITIVE AUDIT VIA SEQUENTIAL EXTRACTION & QUESTION LEDGER
**Target Asset:** Nutun Limited (NTU)  
**Sector:** Consumer_lending  
**Primary Document:** `nutunlimitedcondensedconsolidatedafs31march2026.pdf` (Integrated Annual Report [IAR] — 9 sections)  
**Input Mode:** Sequential Forensic Working Paper & Dynamic Questions Ledger (No PDF Attached)  
**Task Directive:** Forensic Reasoning, Conflict Reconciliation & Post-Balance-Sheet Determinations (No Full Forward Valuation Model Required)

---

### INSTRUCTIONS FOR FORENSIC AUDITOR (LLM):
You are acting as an independent **Managing Director and Senior Forensic Credit & Lending Accounting Auditor**. 
You have been provided with the complete, chronological working paper compiled during a section-by-section forensic capture of Nutun Limited's financial disclosures (9 total sections across primary report and companion disclosures).

Notice how this working paper is constructed:
1. At each stage, specific text, accounting notes, APMs, and operational tables were extracted directly from the report.
2. Across the sections, an **Open Questions Ledger** evolved dynamically: anomalies and high-level management claims in early sections were flagged with priority levels, specific verification instructions, and carried forward as `Pending` until verified against primary financial statements, detailed accounting notes, and subsequent continuous disclosures.

**YOUR MANDATE:**
Review the sequential evidence trail below. Trace how the questions evolved from initial anomalies to audited reconciliation. **Do not produce a forward equity research forecast or valuation report.** Your role is **forensic reasoning only**: you must evaluate the working papers and independently reach your own definitive determinations on the core accounting, operational, and balance sheet junctions, explicitly factoring in subsequent SENS disclosures.

---

## REQUIRED STRUCTURE OF YOUR AUDIT REPORT

Please format your response into the following four clear sections:
1. **Executive Forensic Audit Summary:** Concise synthesis of the group's true economic performance, balance sheet health, post-balance-sheet liquidity runway, and key findings.
2. **Detailed Forensic Reasoning & Determinations:** Step-by-step walkthrough of each key consumer lending & credit junction (IFRS 9 Stage 1/2/3 ECL migration and qualitative macro overlays, loan book vintage delinquency roll rates, carrying value & estimated remaining collections [ERC] of purchased book debts [PBD] and non-performing loan [NPL] portfolios, risk-adjusted net interest margin [NIM] vs credit loss ratio [CLR], National Credit Act [NCA] fee and rate caps, and securitization/debt covenant headroom), citing specific notes, tables, and calculations.
3. **Audit of Common Surface-Reading Pitfalls:** Contrast your findings against the common errors made by naive readers.
4. **Final Forensic Verification Matrix:** A clean markdown summary table listing each Junction, the Raw Initial Claim, the Resolving Note/SENS Announcement, and your Final Verified Determination.

---

## MANDATORY ACCOUNTING & VALUATION GUARDRAILS REGISTRY (SECTOR: CONSUMER_LENDING)

The following institutional guardrails are enforced from the SQLite `sector_guardrails` registry based on prior forensic audits. Violating any of these rules invalidates the report:

| Rule Code | Scope | Guardrail Title | Mandatory Enforcement Rule |
| :--- | :---: | :--- | :--- |
| `ALL-IFRS16-EV-BRIDGE` | **UNIVERSAL** | **IFRS 16 EV-to-Equity & Cash Flow Consistency** *(Origin: SPP)* | Never mix Pre-IFRS 16 cash flows/EBITDA with Post-IFRS 16 lease debt in an Enterprise Value (EV) to Equity bridge. If EV is derived by discounting or applying a multiple to Pre-IFRS 16 EBITDA/FCFF (where cash lease rental payments are already deducted as an operating outflow), DO NOT subtract capitalised IFRS 16 lease liabilities again in the EV-to-Equity bridge (and do not subtract lease principal payments a second time in FCFE). Conversely, if subtracting net IFRS 16 lease liabilities in the EV bridge, you must discount Post-IFRS 16 EBITDA/FCFF before lease payments. Always state explicitly whether your valuation bridge is on a Pre-IFRS 16 or Post-IFRS 16 basis. |
| `ALL-PNL-VERTICAL-ARITHMETIC` | **UNIVERSAL** | **Statutory vs. Normalized P&L Vertical Arithmetic & Impairment Bridge** *(Origin: SPP)* | Every income statement table must sum vertically line-by-line (Revenue - Cost of sales = Gross profit; Gross profit + Other revenue/income - Net operating expenses = Operating profit). Always verify from the primary AFS notes whether statutory Operating Profit is already stated AFTER impairments, restructuring, or extraordinary items before subtracting them; never subtract Note 7/exceptional impairments a second time from a statutory Operating Profit that already includes them, and ensure historical continuing PAT and HEPS match the statutory AFS reconciliation identically. |
| `ALL-SHARE-COUNT-ANCHOR` | **UNIVERSAL** | **Verified Weighted-Average Share Count & Continuing HEPS Denominator** *(Origin: SPP)* | Always extract and state the exact basic and diluted weighted-average number of ordinary shares (in millions, net of treasury shares) from the AFS EPS/HEPS note. Never confuse Headline Earnings in R'm with the share count in millions. In Stage 2 Section 3, include an explicit 'Weighted-Average Shares (m)' row immediately above 'Continuing HEPS (cents)', divide Continuing Headline Earnings (excluding discontinued operations and capital/Note 7 items) by that exact share count, and verify that full-year forecast HEPS is consistent with H1 continuing HEPS already banked. |
| `ALL-TREASURY-SHARE-DIVIDEND-BRIDGE` | **UNIVERSAL** | **Gross vs. Net Treasury Share Count & Parent vs. Consolidated Dividend Reconciliation** *(Origin: CGR)* | Before flagging an arithmetic discrepancy between parent-company dividends paid/declared and net shares in issue, always check gross issued shares vs treasury shares held by subsidiaries or share trusts (e.g. in the Integrated Report dividend declaration or Stated Capital note). Under South African corporate law, the parent company pays the gross dividend on all gross issued shares, whereas the Consolidated Statement of Changes in Equity and Cash Flow Statement eliminate intra-group dividends paid on treasury shares. |
| `ALL-ENTITY-ACRONYM-DISAMBIGUATION` | **UNIVERSAL** | **Full Legal Entity Name Verification Across Notes (No Acronym Conflation)** *(Origin: CGR)* | Never abbreviate two distinct legal entities to the same acronym and claim an accounting classification contradiction. When evaluating entities with similar names, acronyms, or operating divisions, always compare and cross-check full legal entity names across notes before concluding on whether an entity is a joint venture, joint operation, associate, or subsidiary. |
| `ALL-DCF-REPRODUCIBILITY` | **UNIVERSAL** | **DCF Schedule Reproducibility & Anti-Handwaving Component Bridge** *(Origin: DCP)* | Mandates explicit disclosure of annual forecast FCFF/FCFE, terminal value, WACC/discount rate, and a step-by-step numerical EV-to-Equity bridge. Forbids applying qualitative, unmodeled percentage uplifts to blended valuation components; any adjustment between underlying component valuations (e.g. DCF and P/E) and the published target price must be modeled directly within the underlying cash flows or valuation multiples. |
| `ALL-CASHFLOW-CLASSIFICATION-BRIDGE` | **UNIVERSAL** | **Statutory Operating Cash Flow to FCFF/FCFE Bridge & Capex/Lease Deduction** *(Origin: DCP)* | Prohibits labeling statutory Cash Generated from Operations (before capex, lease principal repayments, and interest) as Free Cash Flow to Equity (FCFE) or Free Cash Flow to Firm (FCFF). Models must explicitly bridge operating cash flow to true free cash flow by deducting replacement and expansion capex, IFRS 16 lease principal repayments, net finance costs, and working capital normalizations. |
| `ALL-CASH-ROLLFORWARD-CONSISTENCY` | **UNIVERSAL** | **Forecast Cash and Financing Must Reconcile** *(Origin: NTU)* | For every forecast period, reconcile opening cash plus operating, investing and financing cash flows and separately identified FX or scope changes to closing cash on the forecast balance sheet. Reconcile new borrowing, repayments and equity issuance to debt balances, equity and dilution. State the cash definition and rounding tolerance; bridge restricted cash, held-for-sale cash and overdrafts included in cash equivalents explicitly, without double counting. An unresolved material residual invalidates the forecast and dependent valuation; missing inputs are NOT VERIFIED, never PASS. Example: opening 100 + operating 20 - capex 10 + financing 5 = closing 115 passes; opening 100 plus net change -815 cannot produce closing 95 without an explicit 810 reconciling inflow. |
| `ALL-SENSITIVITY-REPRODUCIBILITY` | **UNIVERSAL** | **Sensitivity Cells Must Reproduce the Valuation** *(Origin: NTU)* | Recalculate every sensitivity cell using the same documented base valuation formula, changing only the named inputs. The central case MUST reproduce the published base target within a declared rounding tolerance. Preserve debt, share count, cash-flow basis, valuation bridges and all discounts unless explicitly varied. Show the formula and full transformation for any additional haircut; unexplained cells invalidate the sensitivity conclusions. Nonlinear models are allowed when their actual formulas are used; do not impose constant derivatives from another method. Missing formulas or inputs are NOT VERIFIED. Example: with 3,845 million of PBD assets, a 0.05 multiple change and one 25% discount over 780.7 million shares imply a 0.18469 ZAR/share change; 0.07 without a disclosed transformation fails. This supplements SOTP arithmetic and prohibits double counting adjustments. |
| `ALL-EQUITY-NAV-VS-CONTRIBUTED-CAPITAL` | **UNIVERSAL** | **Ordinary Shareholder NAV versus Contributed Capital** *(Origin: NTU)* | Calculate statutory ordinary book value/NAV per share from equity attributable to parent ordinary shareholders, excluding non-controlling interests and preference or other non-ordinary claims, divided by ordinary shares outstanding net of treasury shares at the same measurement date. Reconcile retained earnings or accumulated losses and reserves; never label contributed share capital alone as NAV. Use date-matched closing shares rather than silently substituting an earnings weighted-average denominator. Adjusted or tangible NAV is permitted only when clearly labelled and reconciled to statutory ordinary equity, with every adjustment disclosed. NAV is not automatically market fair value. Example: parent ordinary equity 1,329 million / 780.651033 million net shares = approximately 1.70 ZAR/share; share capital 5,410 million / those shares is not book NAV. |
| `ALL-MATERIAL-ISSUES-VALUATION-WITHHOLD` | **UNIVERSAL** | **Withhold Valuation Until Material Dependencies Are Resolved** *(Origin: NTU)* | If a material cash-flow, forecast, financing, share-count, portfolio or valuation dependency fails reconciliation or remains unsupported, return VALUATION WITHHELD - MATERIAL ISSUES UNRESOLVED. Preserve verified historical analysis and risks, identify each blocker and the evidence or correction needed, and carry unresolved Stage 1 findings forward. Do not publish a target, rating bands, upside, dividend yield, TSR or investment recommendation; use JSON null, never zero or HOLD. Illustrative scenarios must remain clearly conditional and separate from the headline valuation. READY requires explicit source evidence, consistent periods and scopes, cash/debt/portfolio roll-forwards, equity financing and terminal-policy consistency, valuation-bridge and sensitivity checks. Assumptions may be used when supported and disclosed; they cannot conceal material missing inputs. Application checks of declared evidence and numeric reconciliations do not replace independent review. |
| `CONSUMER-LENDING-ECL-PBD-ERC` | **CONSUMER_LENDING** | **Consumer Lending IFRS 9 Stage Migration & Purchased Book Debt (PBD) Amortization** | Reconcile gross loan book and Purchased Book Debt (PBD) carrying values against Estimated Remaining Collections (ERC), separating cash collections applied to revenue yield vs principal amortization and Stage 1/2/3 ECL coverage. |
| `CONSUMER-LENDING-PBD-AMORTISATION-EBITDA-ADD-BACK` | **CONSUMER_LENDING** | **Purchased Book Debt (PBD) Amortisation Exclusion from Operating Cash Flow** *(Origin: NTU)* | When valuing consumer debt purchasers and collectors, models are strictly prohibited from treating PBD amortisation as a non-cash add-back in Free Cash Flow to Equity (FCFE). Because portfolio replenishments (PBD acquisitions) are required to sustain collections, models must reflect net cash collections after portfolio acquisition reinvestment. |
| `CONSUMER-LENDING-POCI-GAIN-VS-ECL-RESERVE` | **CONSUMER_LENDING** | **POCI Cumulative Gains, Loss Allowances and Portfolio Scope** *(Origin: NTU)* | For purchased or originated credit-impaired (POCI) principal portfolios, identify the acquisition baseline and reconcile gross carrying amount, signed cumulative changes in lifetime expected credit losses, and net carrying amount using the original notes. A favourable cumulative impairment gain is NOT a conventional loss-coverage reserve: do not divide it by gross carrying amount and call the result loss coverage or describe its decline as a coverage collapse. Preserve reported labels such as ECL allowance while explaining their economic sign. Reconcile opening balance, gains or losses on new and historical portfolios, and closing balance. Separate amortised-cost POCI principal portfolios from other purchased-book-debt assets measured at FVTPL; do not apply one ECL regime to both. Example: gross 3,414 plus cumulative gain 431 = net 3,845; 431/3,414 is not conventional loss coverage. A rolling 12-month modelling disclosure warrants a lifetime/tail-methodology check, not an unsupported conclusion about the amount or direction of misstatement. Missing methodology is NOT VERIFIED. |

---

## MASTER WORKING PAPER: CUMULATIVE OPEN QUESTIONS LEDGER
> **Cognitive Audit Anchor:** The authoritative ledger below consolidates all priority questions, forensic hypotheses, and cross-reference resolutions developed across the entire disclosure set. Use this ledger as your reference matrix when auditing the sequential section extractions that follow.

- Q-3df04995ff2f4c6a [high] [partial] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D002
  Question: Extract headline financial metrics (Gross Advances, Net Advances, impairment charge, CLR %, NIM %, HEPS, DPS) and any management guidance/targets stated in Key Highlights, and confirm the printed-vs-physical page offset.
  Evidence required: Key Highlights section (printed p. 1, physical pp. 3-7): headline advances, impairment, CLR, NIM, HEPS, DPS figures with units (ZAR) and period (H1 FY2026 vs comparative), plus any stated guidance or targets.
  Closure condition: Headline figures captured with period, units and scope, page offset reconciled, and any guidance quoted verbatim; benign explanations for movements noted.
  Latest answer: Page offset re-confirmed (printed = physical - 2). No headline advances/CLR/NIM/HEPS/DPS or guidance in this capture. Group revenue R711m vs R745m captured.

- Q-995d98c7cabc40ba [high] [partial] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture statement of financial position and income statement values: gross vs net advances, total ECL allowance, Stage 1/2/3 split, net interest income, non-interest revenue, operating expenses, and impairment line.
  Evidence required: Statement of financial position (printed p. 6) and income statement (printed p. 7): advances gross/net, ECL allowance, stage breakdown, NII, NIR, opex, impairment charge, with comparatives and units.
  Closure condition: All line items captured with comparatives; implied gross advances = net + allowance reconciled; CLR and cost-to-income computable; discrepancies flagged.
  Latest answer: No statement lines, advances, ECL allowance, or Stage 1/2/3 split in this capture. New earnings-quality item: statements and forward-looking information are unreviewed by external auditors. Remainder open for D003.

- Q-64b704d06ed84c90 [medium] [partial] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture cash flow statement items: gross write-offs, bad debt recoveries, debt raised/repaid, and dividends paid.
  Evidence required: Statement of cash flows (printed p. 10): write-offs, recoveries, debt movements, dividends, with comparatives and units.
  Closure condition: Figures captured and net bad debt charge reconciliation (write-offs + ECL movement - recoveries) testable; funding flows identified.
  Latest answer: No write-offs, recoveries, debt movements or dividends. Cash collections on other financial assets R116m vs R90m; PBD net cash collections R728m vs R566m.

- Q-336536b6077249e3 [medium] [partial] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate and unpack IFRS 9 ECL staging note, SICR definition, macro overlay/scenario weightings, write-off policy, rescheduling/modification rules, and funding covenants.
  Evidence required: Notes to the financial statements (printed p. 11 onward): ECL staging tables, SICR thresholds (DPD), scenario weightings, write-off triggers, modification/re-aging rules, covenant terms and headroom.
  Closure condition: Each policy/note quoted with page reference; any relaxed SICR, delayed write-off, or covenant tightness identified; forecast consequences stated.
  Latest answer: No IFRS 9 staging/SICR/write-off/covenant content. PBD impairment loss R167m (H1 2026) vs R173m (H1 2025) disclosed in amortisation footnote.

- Q-007f8f020e154296 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Reconcile group net interest cost R216m (p.3 table) vs SA-segment R203m (p.4 commentary); confirm R13m International net interest cost in income statement / segment note 7.
  Evidence required: Income statement net interest line and segment note 7 net interest cost split (SA vs International), H1 2026 vs H1 2025, ZAR millions.
  Closure condition: Group net interest cost reconciled to segment split; any unexplained difference flagged; benign explanation (segment vs group scope) confirmed or discrepancy escalated.
  Latest answer: Pending: D003

- Q-e741a412cfd44a34 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Split PBD/RTC amortisation R597m into scheduled amortisation, accelerated/impairment write-down, and FX; determine whether acceleration is one-off or recurring run-rate.
  Evidence required: PBD/RTC amortisation note with components, assumptions (discount rate, collection curve, macro), and comparative H1 2025; any impairment line on PBD/RTC asset.
  Closure condition: Amortisation components quantified; recurring vs one-off classification supported by note; forecast run-rate stated.
  Latest answer: Pending: D003

- Q-b63cf1b01b6d4cf8 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Verify ERC R8,366m methodology (discount rate, collection curve, macro assumptions) and compare actual H1 2026 collections (PBD R773m + RTC R116m) to ERC run-off expectations.
  Evidence required: PBD/RTC note: ERC definition, discount rate, collection-curve assumptions, actual collections vs ERC, and any sensitivity disclosure.
  Closure condition: ERC methodology quoted; actual collections reconciled to ERC run-off; any under-run quantified and forecast consequence stated.
  Latest answer: Pending: D003

- Q-b3d2bdde10394bac [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture funding note: facility sizes, maturities, covenant ratios (interest cover, LTV, DSCR), headroom, and details of FY2025 funding restructuring (Note 1, p.6).
  Evidence required: Borrowings/funding note: facility amounts, maturity profile, covenant terms and headroom, unutilised facilities reconciliation to R0.8bn, FY2025 restructuring detail.
  Closure condition: Facility sizes, maturities, covenant ratios and headroom captured; R0.8bn unutilised reconciled; refinancing/liquidity risk assessed.
  Latest answer: Pending: D003

- Q-fec447426706441e [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Confirm whether any IFRS 9 ECL / macro-overlay note exists for PBD/RTC asset or TC Global Finance associate; capture discount-rate and macro assumptions used in accelerated amortisation.
  Evidence required: Accounting policies and notes: ECL staging (if any), macro scenario weightings, discount rates, and associate (TC Global Finance) carrying value/impairment.
  Closure condition: Policy and assumptions quoted with page reference; whether macro conservatism is genuine or smoothing assessed; forecast consequence stated.
  Latest answer: Pending: D003

- Q-7acc435c1ae94e77 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Separate organic vs acquired PBD collection growth: PBD collections +28% to R773m against R593m (H2 FY2025) + R382m (H1 FY2026) acquisitions; compute collection yield on average carrying value.
  Evidence required: Segment note 7 and PBD note: collections split organic vs acquired, average carrying value, collection yield.
  Closure condition: Organic vs acquired growth separated; collection yield computed; genuine improvement vs acquisition-driven growth determined.
  Latest answer: Pending: D003

- Q-c06d7a5336224c7e [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture client concentration disclosure (top 5/10 clients as % of revenue) and any related-party client disclosure, given agency fee revenue -15% and clients 23 to 20.
  Evidence required: Concentration and related-party notes: top client revenue percentages, related-party revenue/balances.
  Closure condition: Concentration quantified; related-party exposure identified; revenue concentration risk to forecast stated.
  Latest answer: Pending: D003

- Q-e8e8f8f7354146ea [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Check related-party note for Mobalyz: confirm termination of management fee, no residual receivable/exposure, and whether Mobalyz is a related party.
  Evidence required: Related-party note: Mobalyz transactions, balances, and relationship.
  Closure condition: Mobalyz relationship and residual exposure confirmed or confirmed absent; forecast impact of lost fee stated.
  Latest answer: Pending: D003

- Q-174a38f8f4c04abc [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Quantify DTI incentive income in Nutun International revenue/EBITDA and check contingent-asset or government-grant note given stated uncertainty over future of DTI incentives.
  Evidence required: Revenue disaggregation and government-grant/contingent-asset note: DTI incentive amounts, recognition basis, contingency.
  Closure condition: DTI incentive contribution quantified; contingency disclosed; EBITDA sensitivity to loss stated.
  Latest answer: Pending: D003

- Q-aea94945233b418a [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Check TC Global Finance associate carrying value and whether further impairment risk remains after R47m H1 2025 impairment (nil this period).
  Evidence required: Associate note: TC Global Finance carrying value, impairment history, and any residual exposure.
  Closure condition: Carrying value and impairment risk captured; forecast consequence stated.
  Latest answer: Pending: D003

- Q-add37e0058a74df2 [low] [partial] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Confirm audit/review status of figures in D003 and whether any 'accelerated items' or 'normal operations' add-backs are applied in H1 2026 core continuing earnings reconciliation beyond the two shown.
  Evidence required: Audit/review statement and core continuing earnings reconciliation detail.
  Closure condition: Assurance level and APM add-backs confirmed; earnings quality assessed.
  Latest answer: Core earnings policy quoted: once-off transaction costs, put/call option adjustments, once-off or accelerated items, and headline exclusions if part of normal operations. H1 2026 exceptional items nil; H1 2025 R51m. Audit status of statements not in this capture.

- Q-59b88716280048c3 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Confirm whether the primary financial statements carry the same 'not reviewed or reported on by external auditors' disclaimer, and check for any note on restatement, prior-period error correction, or post-balance-sheet events; confirm whether any figures are marked audited/reviewed.
  Evidence required: Primary statements and notes: assurance/review statement, restatement or error-correction note, subsequent-events note, with page references.
  Closure condition: Assurance status of each statement confirmed; any restatement/error/subsequent event quoted with page reference; forecast reliability impact stated.
  Latest answer: Pending: D003

- Q-ebf661d7f2e740cd [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Determine what the 'transition of the business' overseen by the Executive Chairman refers to: check subsequent-events note, going-concern statement, and any strategic-review, disposal, recapitalisation, or funding event disclosure linked to the 1 Jan 2026 board changes.
  Evidence required: Subsequent-events note, going-concern statement, strategic-review/disposal/restructuring disclosures, with page references and amounts.
  Closure condition: Nature of the 'transition' established and quoted; any corporate event quantified; forecast base-case impact stated.
  Latest answer: Pending: D003

- Q-0b9b00a6c7da4496 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Check the Audit & Risk Committee / governance note for any qualification, internal-control deficiency, or change in risk appetite following the 1 Jan 2026 committee membership changes (two resignations, one appointment).
  Evidence required: Audit & Risk Committee report or governance note: qualifications, control deficiencies, risk-appetite changes, with page references.
  Closure condition: Any qualification or control issue quoted with page reference, or confirmed absent; forecast consequence stated.
  Latest answer: Pending: D003

- Q-5a1c41b2ef654626 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Identify which forward-looking figures exist (ERC run-off, amortisation assumptions, guidance) and confirm they are flagged as director-prepared/unreviewed in the notes; capture any sensitivity disclosures.
  Evidence required: Notes identifying forward-looking information, ERC/amortisation assumptions, and sensitivity disclosures, with page references.
  Closure condition: Forward-looking items listed and flagged; sensitivities captured; weight to place on management assumptions in forecast stated.
  Latest answer: Pending: D003

- Q-019095eae85848d1 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate the ECL/impairment note for purchased book debts: capture gross carrying amount, cumulative ECL allowance, Stage 1/2/3 (or purchased-credit-impaired) split, and coverage ratios for 31 Mar 2026 vs 31 Mar 2025 vs 30 Sep 2025, in ZAR millions.
  Evidence required: ECL/impairment note: gross carrying amount, cumulative ECL allowance, stage split, coverage ratios, with comparatives and units.
  Closure condition: Gross advances, allowance and stage split captured; implied coverage % reconciled; any discrepancy flagged; benign explanations noted.
  Latest answer: Pending: D003

- Q-48250bf920104880 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Decompose the R167m impairment loss on principal book portfolios into gross ECL charge vs favourable ECL re-estimate gain, and compare H1 2025 R173m and FY2025 R199m on the same basis.
  Evidence required: Impairment note: gross ECL charge, favourable re-estimate gain, net impairment loss, with comparatives.
  Closure condition: Components quantified; recurring vs one-off classification supported; forecast CLR consequence stated.
  Latest answer: Pending: D003

- Q-d999efdf22e5453b [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture funding/borrowings note: security-cover ratio, LTV, borrowing-base covenant, minimum collateral thresholds and headroom, given 100% of principal book portfolio (R3,845m) and receivables/cash are pledged.
  Evidence required: Borrowings note: covenant terms, security-cover/LTV ratios, headroom, collateral values, with page references.
  Closure condition: Covenant ratios and headroom captured; breach risk assessed; forecast consequence stated.
  Latest answer: Pending: D003

- Q-19a3c1172f494459 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture maturity profile by facility, refinancing plan, covenant ratios (interest cover, DSCR) and going-concern statement, given R1,396m payable within 12 months and only R475m undrawn overdraft facilities.
  Evidence required: Funding note and going-concern statement: facility maturities, refinancing arrangements, covenant ratios, liquidity reserves.
  Closure condition: Maturity wall and refinancing plan captured; liquidity risk assessed; forecast consequence stated.
  Latest answer: Pending: D003

- Q-d9c20b083a06486d [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate note 6.3 on fair value of other financial assets (R644m): fair value hierarchy level, valuation inputs, retraction/recourse terms and sensitivity.
  Evidence required: Note 6.3: fair value hierarchy, valuation inputs, retraction terms, sensitivity analysis.
  Closure condition: Methodology quoted; valuation and earnings volatility assessed; forecast consequence stated.
  Latest answer: Pending: D003

- Q-e0fd336bd6e441b5 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture vintage/seasoning or ERC note: collection curve assumptions, ERC balance, actual vs expected collections, given gross collections R773m vs net R728m and collection cost R45m (5.8%).
  Evidence required: ERC/vintage note: ERC balance, collection curve assumptions, actual vs expected collections, sensitivity.
  Closure condition: ERC methodology quoted; actual collections reconciled to ERC run-off; under-run quantified; forecast consequence stated.
  Latest answer: Pending: D003

- Q-28dc6d0fd29c48ce [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture portfolio-acquisition note: purchase price, acquired ERC, expected collections and contingent consideration for additions of R382m (H1 2026) vs R265m (H1 2025) vs R857m (FY2025).
  Evidence required: Business-combination/portfolio-acquisition note: purchase price, acquired ERC, expected collections, contingent consideration.
  Closure condition: Acquisition economics captured; organic vs acquired growth separated; forecast consequence stated.
  Latest answer: Pending: D003

- Q-11d46434b5e548de [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture drivers of the R30m fair value gain on other financial assets (H1 2025 R74m; FY2025 R114m) and assess recurrence.
  Evidence required: Fair value note: drivers of FV gain, Level 3 assumptions, recurrence assessment.
  Closure condition: FV gain drivers quantified; recurring vs one-off classification supported; forecast consequence stated.
  Latest answer: Pending: D003

- Q-9716a218b43b416b [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture associate note: TC Global Finance carrying value, share of loss (R1m H1 2026 vs R43m H1 2025 vs R48m FY2025) and any residual impairment.
  Evidence required: Associate note: carrying value, share of loss, impairment history, residual exposure.
  Closure condition: Carrying value and impairment risk captured; forecast consequence stated.
  Latest answer: Pending: D003

- Q-32dcbb2aeead41c8 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture discontinued-operations note: what was disposed (R398m proceeds H1 2025), residual liabilities/indemnities, and held-for-sale assets R4m/liabilities R6m.
  Evidence required: Discontinued-operations note: disposal detail, residual liabilities, indemnities, held-for-sale balances.
  Closure condition: Disposal complete and residual exposures confirmed or confirmed absent; forecast consequence stated.
  Latest answer: Pending: D003

- Q-ed4807de3ac74d68 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture tax note: basis for R29m income tax credit on R(92)m loss before tax (effective rate -31.5%), deferred tax asset R173m recognition and recoverability.
  Evidence required: Tax note: current/deferred tax split, DTA recognition basis, recoverability assumptions, comparatives.
  Closure condition: Tax credit basis captured; DTA recoverability assessed; forecast consequence stated.
  Latest answer: Pending: D003

- Q-8a74a12fefbf4e13 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture operating cost note: breakdown of R445m (vs R560m H1 2025, -20.5%) and cost of revenue R385m (vs R352m, +9.4%), identifying one-off items and sustainability of cost reduction.
  Evidence required: Opex note: breakdown, one-off items, staff costs, cost-of-revenue composition, comparatives.
  Closure condition: Cost base trajectory captured; one-off vs recurring classified; forecast consequence stated.
  Latest answer: Pending: D003

- Q-a14f390ef9d042b0 [low] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture revenue disaggregation note: SA vs International split, agency fees, DTI incentive contribution, given revenue R711m vs R745m (-4.6%) and gross profit from services R326m vs R393m (-17%).
  Evidence required: Revenue disaggregation note: segment split, agency fees, DTI incentives, comparatives.
  Closure condition: Revenue mix captured; DTI contingency quantified; forecast consequence stated.
  Latest answer: Pending: D003

- Q-429b0eebe1144e16 [low] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture EPS note: weighted average shares, dilution from conditional share plans, given treasury shares acquired (4m for R4m) and shares in issue 780m.
  Evidence required: EPS note: weighted average shares, dilution, conditional share plan detail.
  Closure condition: EPS denominator captured; dilution assessed; forecast consequence stated.
  Latest answer: Pending: D003

- Q-777af456b5384c00 [low] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture interest-rate risk/sensitivity note: fixed vs floating split and hedge accounting, given new facility-level disclosure of JIBAR + 2.8%-5.2% and Prime - 0.25% to 0.35% rates maturing to 2032.
  Evidence required: Interest-rate risk note: fixed/floating split, hedge accounting, sensitivity to JIBAR/Prime.
  Closure condition: Rate sensitivity captured; interest expense forecast sensitivity stated.
  Latest answer: Pending: D003

- Q-5a215339455549cb [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate the PBD note and reconcile the weighted average credit-adjusted EIR of 19.2% (31 Mar 2026) vs 17.9% (31 Mar 2025) and 18.4% (30 Sep 2025): is the +130bp YoY rise driven by mix (newer/higher-risk acquired vintages) or a methodology/assumption change, and what is the EIR by vintage/cohort? Reconcile to PBD amortisation R597m.
  Evidence required: PBD note: EIR by vintage/cohort, methodology-change disclosure, reconciliation to PBD amortisation R597m, H1 2026 vs H1 2025 vs FY2025, ZAR millions and %
  Closure condition: EIR movement decomposed into mix vs methodology; PBD amortisation reconciled; forecast run-rate of amortisation/ECL charge stated with benign explanation if mix-driven.
  Latest answer: Pending: D003

- Q-e0ad7294ef664877 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture the PBD carrying value note: gross PBD, cumulative ECL allowance, POCI coverage ratio, and comparatives at 31 Mar 2026, 31 Mar 2025 and 30 Sep 2025, in ZAR millions; reconcile to the R3,845m principal book portfolio pledged as security.
  Evidence required: PBD note: gross carrying amount, cumulative ECL allowance, POCI coverage %, comparatives, reconciliation to R3,845m pledged portfolio
  Closure condition: Gross PBD, allowance and coverage % captured and reconciled; any discrepancy vs R3,845m flagged; forecast CLR input stated.
  Latest answer: Pending: D003

- Q-e638336bf5bf48a6 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Decompose the R167m impairment loss on principal book portfolios into gross ECL charge vs favourable ECL re-estimate gain, and restate H1 2025 R173m and FY2025 R199m on the same basis.
  Evidence required: Impairment note: gross ECL charge, favourable re-estimate gain, net impairment loss, comparatives H1 2025 and FY2025, ZAR millions
  Closure condition: Components quantified; recurring vs one-off classification supported by note; forecast CLR consequence stated.
  Latest answer: Pending: D003

- Q-91785c26cc0b4e99 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Explain the Australia revenue decline from R74m (H1 2025) to R27m (H1 2026) and the UK increase from R259m to R303m: locate segment/geographic commentary, contract wins/losses, FX effects, or subsequent-events disclosure.
  Evidence required: Segment note or geographic commentary: Australia and UK revenue drivers, contract changes, FX, comparatives
  Closure condition: Drivers of Australia decline and UK growth identified and quantified; sustainability of International revenue base stated for forecast.
  Latest answer: Pending: D003

- Q-692b91fba36d46b3 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Confirm whether the first-time presentation of the revenue geographic/type split involved any reclassification of H1 2025 comparatives; locate any reclassification note and quantify remapping between SA/International or service/commission.
  Evidence required: Reclassification note or accounting policy change disclosure quantifying any remapping of H1 2025 revenue
  Closure condition: Reclassification quantified or confirmed absent; comparability of YoY growth confirmed.
  Latest answer: Pending: D003

- Q-abbce81b5da84312 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate the Conditional Share Plan note: number of conditional shares outstanding, vesting conditions, IFRS 2 charge for H1 2026, and potential dilution on return to profit.
  Evidence required: CSP/share-based payment note: conditional shares outstanding, vesting conditions, IFRS 2 expense, dilution calculation
  Closure condition: CSP overhang and IFRS 2 charge quantified; dilution on profitability modelled.
  Latest answer: Pending: D003

- Q-533b9024210549c0 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate the trade receivables note: gross balance, loss allowance, provision matrix, DPD aging and top-client concentration, to test the assertion that clients are diversified with no significant concentration risk.
  Evidence required: Trade receivables note: gross balance, loss allowance, provision matrix, DPD aging, top-client concentration %
  Closure condition: Receivables credit quality and concentration quantified; assertion tested; forecast ECL input stated.
  Latest answer: Pending: D003

- Q-83a5d39bd7374279 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Confirm the SICR/provisioning approach for trade receivables: whether the simplified approach provision matrix is used and whether a 30-DPD rebuttable presumption applies, given no DPD threshold is disclosed in the credit risk policy.
  Evidence required: Accounting policy note: trade receivables provisioning approach, DPD triggers, simplified approach confirmation
  Closure condition: Provisioning approach quoted with page reference; provisioning timeliness assessed.
  Latest answer: Pending: D003

- Q-74e79aaa44cc4a15 [low] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Check the statement of changes in equity for all equity movements (share-based payment reserve, treasury shares, NCI, other reserves) to reconcile share capital R5,410m and total equity.
  Evidence required: Statement of changes in equity: all reserve movements, NCI, comparatives
  Closure condition: Equity roll-forward reconciled; NAV forecast input captured.
  Latest answer: Pending: D003

- Q-0ada68da08fa49fc [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate the ECL model/assumption note and any methodology-change disclosure; reconcile the R233m release in Banking & Specialised Lending unsecured allowance (R460m to R227m on flat gross R2,371m) to genuine performance vs assumption change.
  Evidence required: ECL model note: assumption changes, coverage ratios by segment, H1 2026 vs H1 2025 vs FY2025, ZAR millions and %
  Closure condition: Release decomposed into performance vs methodology; forecast impairment consequence stated; benign explanation if performance-driven.
  Latest answer: Pending: D003

- Q-d781546003984272 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate the POCI/ERC note: investment base-case assumptions, actual vs expected collections, and run-off profile of the R431m cumulative impairment gain.
  Evidence required: POCI/ERC note: base-case assumptions, actual vs expected collections, cumulative gain run-off, sensitivity
  Closure condition: Run-off profile quantified; timing of flip from impairment gain to charge estimated; forecast consequence stated.
  Latest answer: Pending: D003

- Q-5e16f0ada73840c8 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate full ECL movement note with gross write-offs, post-write-off recoveries, FX and transfers, since the p.24 roll-forward omits these lines.
  Evidence required: ECL movement note: gross write-offs, recoveries, FX, transfers, H1 2026 vs H1 2025, ZAR millions
  Closure condition: Net bad debt charge reconciliation (write-offs + ECL movement - recoveries) testable; CLR computable.
  Latest answer: Pending: D003

- Q-c0430bffdd134145 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate accounting policy note on trade receivables provisioning and any methodology-change disclosure, given 0.00% ELR applied to 30+ and 61-90 day buckets at 31 Mar 2026 vs 0.06%/0.19%/6.67% at 30 Sep 2025.
  Evidence required: Trade receivables provisioning policy: matrix basis, DPD triggers, methodology-change disclosure, historical loss experience by bucket
  Closure condition: Zero ELR basis confirmed as methodology change or genuine zero loss experience; provisioning timeliness assessed.
  Latest answer: Pending: D003

- Q-5fc0971fd6174503 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate PBD EIR/vintage note and reconcile 18.50% market discount rate to 19.2% credit-adjusted EIR and to fair value = carrying R3,845m.
  Evidence required: PBD EIR note: EIR by vintage/cohort, market discount rate reconciliation, fair value sensitivity
  Closure condition: Reconciliation complete; whether carrying value is supportable at 18.50% market rate confirmed; forecast consequence stated.
  Latest answer: Pending: D003

- Q-c0e5fb0f2f3c409c [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate interest-rate risk note: fixed/floating split, hedge accounting, JIBAR/Prime sensitivity, and reconcile the R365m swing in interest-bearing liabilities fair value vs carrying between 30 Sep 2025 and 31 Mar 2026.
  Evidence required: Interest-rate risk note: fixed/floating split, hedge accounting, sensitivity to JIBAR/Prime, fair value reconciliation
  Closure condition: Rate sensitivity captured; interest expense forecast sensitivity stated; fair value swing explained.
  Latest answer: Pending: D003

- Q-d3214701599f4536 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate any restatement/prior-period note confirming 31 Mar 2025 net carrying values (principal book R3,690m, other financial assets R663m) unchanged despite represented gross/allowance split.
  Evidence required: Restatement/prior-period note: originally reported vs represented figures, net carrying values
  Closure condition: Net carrying values confirmed unchanged; comparability of YoY movements confirmed.
  Latest answer: Pending: D003

- Q-2a3622968261481a [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Reconcile trade & other receivables gross R5,395m (financial assets only) to statement of financial position trade & other receivables line; quantify excluded prepayments/VAT/deposits.
  Evidence required: Statement of financial position trade & other receivables line; breakdown of prepayments/VAT/deposits excluded
  Closure condition: Reconciliation complete; balance-sheet forecast input captured.
  Latest answer: Pending: D003

- Q-4ed57bbdde83420e [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate note 6.3 continuation or other financial assets note: fair value hierarchy level, inputs and sensitivity for the R644m other financial assets.
  Evidence required: Other financial assets note: hierarchy level, valuation inputs, sensitivity analysis
  Closure condition: Hierarchy level and sensitivity captured; earnings volatility assessed.
  Latest answer: Pending: D003

- Q-f8d00abd0de446f5 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate hedge accounting note for new USD/GBP FX hedging programme: notional, fair value of hedges, hedge reserve.
  Evidence required: Hedge accounting note: notional amounts, hedge fair values, hedge reserve movement
  Closure condition: FX hedging P&L and reserve impact quantified.
  Latest answer: Pending: D003

- Q-024f496e3b2f4b57 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate portfolio acquisition note: purchase price, acquired ERC, day-one ECL basis, contingent consideration for H1 2026 additions, given acquisition-day ECL swung from R96m loss to R24m gain.
  Evidence required: Portfolio acquisition note: purchase price, acquired ERC, day-one ECL, contingent consideration, H1 2026 vs H1 2025 vs FY2025
  Closure condition: Acquisition economics captured; whether day-one ECL is being managed to smooth P&L assessed.
  Latest answer: Pending: D003

- Q-48aec45bd7754483 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate debt review portfolio note: gross balance growth (R605m to R951m), coverage basis (14.8%), rescheduling/modification rules and re-aging policy.
  Evidence required: Debt review note: gross balance, coverage, rescheduling rules, re-aging policy, comparatives
  Closure condition: Debt review credit quality and growth drivers captured; forecast consequence stated.
  Latest answer: Pending: D003

- Q-b6b4741e827b495d [low] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Confirm retail book (gross R46m, allowance R51m, 111% coverage) is in run-off/wind-down.
  Evidence required: Retail portfolio note: run-off status, gross balance trend
  Closure condition: Run-off status confirmed; minor forecast input captured.
  Latest answer: Pending: D003

- Q-4cbda9067b3a48c5 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Reconcile PBD IFRS net income from purchased book debts R69m to footnote components (CAEIR R383m - impairment R167m - net cash collections R728m + FV R30m + cash collections R116m) which sum to -R366m; identify the missing bridge and confirm note 1.1/1.2 definitions.
  Evidence required: Note 1.1 (PBD) and note 1.2 (other financial assets) full text and tables, H1 2026 vs H1 2025, ZAR millions, showing how net cash collections and CAEIR imputed interest are defined and netted to the R69m IFRS line.
  Closure condition: R69m reconciled to components with each bridge item quantified; any unexplained difference flagged; benign explanation (definitional netting) confirmed or discrepancy escalated.
  Latest answer: Pending: D003

- Q-46a6ab41551d45d8 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Verify the 16% discount rate on other financial assets (vs 12.93% Mar 2025, 16% Sep 2025): is it market-driven or a conservatism overlay, and what is the sensitivity of the R644m carrying value and R30m FV gain to a 100bp change?
  Evidence required: Note 6.3 continuation / note 1.2: discount-rate derivation, cash-flow assumptions, sensitivity analysis, and reconciliation to PBD CAEIR 19.2%.
  Closure condition: Discount-rate basis quoted; sensitivity quantified; recurrence of FV gain assessed; forecast consequence stated.
  Latest answer: Pending: D003

- Q-d0b2a650c3b74485 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Decompose PBD impairment loss R167m (H1 2026) vs R173m (H1 2025) into gross ECL charge vs favourable re-estimate gain, and confirm coverage % on the PBD book given 28% higher collections.
  Evidence required: PBD ECL/impairment note: gross charge, re-estimate gain, coverage %, gross carrying amount, comparatives H1 2025 and FY2025, ZAR millions and %.
  Closure condition: Components quantified; coverage reconciled; whether impairment is being suppressed by re-estimates assessed; CLR forecast input stated.
  Latest answer: Pending: D003

- Q-935c75b4dc8f4cb8 [high] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Confirm whether any 'accelerated items' or 'normal operations' add-backs are applied in H1 2026 core earnings beyond the two shown, and whether PBD amortisation acceleration or ECL re-estimates are excluded from core EBITDA R790m.
  Evidence required: Full core-earnings reconciliation detail and any note on accelerated items; bridge from IFRS loss R63m to core EBITDA R790m with each add-back itemised.
  Closure condition: All add-backs itemised and quoted; earnings-quality assessment stated; forecast core vs IFRS gap quantified.
  Latest answer: Pending: D003

- Q-9405deee26f747ae [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Locate note 4.1 revenue disaggregation: SA vs International, agency fees, DTI incentives, PBD revenue split, H1 2026 vs H1 2025.
  Evidence required: Note 4.1: revenue by type and geography, DTI incentive amounts, comparatives, ZAR millions.
  Closure condition: Revenue mix captured; DTI contingency quantified; forecast consequence stated.
  Latest answer: Pending: D003

- Q-c24afb141706410e [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Explain Nutun International profit decline R33m to R23m on flat revenue R557m to R552m, and SA PBD operating cost fall R279m to R190m (-32%): structural or one-off?
  Evidence required: Segment cost detail / opex note: International cost drivers, SA PBD operating cost breakdown, one-off items, comparatives.
  Closure condition: Margin compression and cost-cut drivers quantified; recurring vs one-off classified; forecast run-rate stated.
  Latest answer: Pending: D003

- Q-d7463e5b54e445c3 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Reconcile net finance charge R39m (H1 2026) vs R52m (H1 2025) and SA PBD finance charge R32m vs R60m to borrowings facilities and rate sensitivity.
  Evidence required: Borrowings/interest note: facility rates, fixed/floating split, interest expense reconciliation, comparatives.
  Closure condition: Interest expense reconciled; rate sensitivity captured; forecast interest expense stated.
  Latest answer: Pending: D003

- Q-e6ecd9b08f9f4461 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Capture tax note: basis for R29m income tax credit on R(92)m loss (effective -31.5%), current/deferred split, DTA recognition and recoverability.
  Evidence required: Tax note: current/deferred split, DTA recognition basis, recoverability assumptions, comparatives.
  Closure condition: Tax credit basis captured; DTA recoverability assessed; forecast consequence stated.
  Latest answer: Pending: D003

- Q-b3c2a7970ec54ed3 [medium] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Confirm H1 2025 segment/core reconciliation presented 'for the first time' is consistently constructed and that R51m exceptional items and core EBITDA R615m are not cherry-picked.
  Evidence required: Representation/reclassification note and full H1 2025 core reconciliation detail.
  Closure condition: Construction basis confirmed; comparability of YoY core earnings stated.
  Latest answer: Pending: D003

- Q-94fcb1973800423d [low] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Confirm no residual discontinued-operations liabilities, indemnities or held-for-sale balances remain after Nutun Transact disposal (H1 2025 profit R58m; H1 2026 nil).
  Evidence required: Discontinued-operations note: residual liabilities, indemnities, held-for-sale balances.
  Closure condition: Residual exposures confirmed or confirmed absent; forecast base clean.
  Latest answer: Pending: D003

- Q-bb266d43a25e42a8 [low] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Explain other investments Level 2 swing R237m (Mar 2025) to R41m (Sep 2025) to R81m (Mar 2026) and confirm money market fund liquidity.
  Evidence required: Other investments note: balance drivers, liquidity terms.
  Closure condition: Swing explained; liquidity input captured.
  Latest answer: Pending: D003

- Q-e42ae34e23ea4ca5 [low] [open] Target: nutunlimitedcondensedconsolidatedafs31march2026.pdf / D003
  Question: Confirm the report ends at the financial statements/notes with no additional financial annexures or disclosures beyond the p. 38 administration page.
  Evidence required: Confirmation of the final page of financial notes/disclosures and that p. 38 is the terminal administration page; no omitted annexures.
  Closure condition: Document completeness confirmed; any omitted financial content identified or confirmed absent; forecast evidence base stated as complete.
  Latest answer: Pending: D003

---

# THE SEQUENTIAL EXTRACTION & WORKING PAPER DOSSIER (9 SECTIONS)

================================================================================
## SECTION 1: [D001] Source coverage remainder
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section D001 | [AFS] physical page 1 | area selection | Commentary ---
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                  TRANSFORM   YOUR FUTURE         
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                     Condensed        consolidated                                
                     Financial                                                    
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                           statements                                             
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                           FOR  THE HALF  YEAR  ENDED   31 MARCH   2026           
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                              Nutun       Limited                 
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  

--- Section D001 | [AFS] physical page 2 | area selection | Table ---
Condensed consolidated financial statements for the half year ended 31 March 2026

| Contents |  |
| --- | --- |
|  | Page |
| Key highlights | 1 |
| Condensed consolidated statement of financial position | 6 |
| Condensed consolidated income statement | 7 |
| Condensed consolidated statement of comprehensive income | 8 |
| Condensed consolidated statement of changes in equity | 9 |
| Condensed consolidated statement of cash flows | 10 |
| Notes to the condensed consolidated financial statements | 11 |
| Administration | 35 |

### [ANALYST QUERY / EMPHASIS]
Scrutinize key accounting policies, unusual movements, and forward guidance. This is one capture, not proof of whole-report coverage. Adjacent tables/footnotes may need verification.

### [SECTION READING RESPONSE / DETERMINATION]
### 1. Answers to Stored Questions for This Section
No stored questions were supplied (first section capture). Omitted per workflow rule.

### 2. Footnote & Qualification Deep-Dive
- No footnote markers (`[^1]`, `*`, note references) appear in the supplied D001 evidence on physical PDF pp. 1–2. There is therefore no footnote text to unpack, and none is missing from this capture.
- Qualification noted: the contents table `[D001, physical PDF p. 2]` lists printed page numbers (Key highlights p. 1 … Administration p. 35) that are **offset from the physical PDF page numbers** in the Report Map (e.g., Key highlights printed p. 1 vs physical p. 3; statement of financial position printed p. 6 vs physical p. 8). This is a pagination qualification only — it does not change any financial number, but it means all future citations must reconcile printed vs physical page labels.
- No accounting policy, ECL staging, write-off, rescheduling, yield, or covenant commentary is present in this capture. Nothing here alters headline numbers; all such verification is deferred to D002–D004.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q1 | High | D002 Highlights | Contents lists "Key highlights" at printed p. 1 `[D001, p. 2]`; no figures supplied | Extract headline Gross Advances, Net Advances, impairment charge, CLR %, NIM %, HEPS, DPS, and any stated guidance/targets; confirm printed-vs-physical page offset | Baseline forecast anchors and management guidance |
| Q2 | High | D003 Primary financial statements | Contents lists statement of financial position (printed p. 6) and income statement (printed p. 7) `[D001, p. 2]` | Capture gross vs net advances, total ECL allowance, Stage 1/2/3 split, net interest income, non-interest revenue, operating expenses, impairment line | Core P&L and balance-sheet model inputs; CLR and cost-to-income computation |
| Q3 | Medium | D003 Primary financial statements | Contents lists statement of cash flows (printed p. 10) `[D001, p. 2]` | Capture gross write-offs, bad debt recoveries, debt raised/repaid, dividends paid | Reconcile net bad debt charge and funding flows |
| Q4 | Medium | D003 Primary financial statements | Contents lists "Notes to the condensed consolidated financial statements" (printed p. 11) `[D001, p. 2]` | Locate IFRS 9 ECL staging note, SICR definition, macro overlay/scenario weightings, write-off policy, rescheduling/modification note, funding covenants | Forensic credit risk assessment; detect relaxed SICR, delayed write-offs, covenant tightness |
| Q5 | Low | D004 Unclassified (physical p. 38) | Contents lists "Administration" at printed p. 35 `[D001, p. 2]`; physical p. 38 unclassified | Confirm whether p. 38 is administration/corporate information or contains additional financial disclosures | Completeness of report coverage |

### 5. Baseline Forecast Inputs Captured Here
- Report identity: Nutun Limited — Condensed consolidated financial statements for the half year ended 31 March 2026 `[D001, p. 1]`.
- Contents structure and printed page labels `[D001, p. 2]`: Key highlights p. 1; Statement of financial position p. 6; Income statement p. 7; Statement of comprehensive income p. 8; Statement of changes in equity p. 9; Statement of cash flows p. 10; Notes p. 11; Administration p. 35.
- No financial figures, guidance, or credit metrics are present in this capture.

### 6. Next Section to Capture
`D002` (Highlights, physical pp. 3–7) — resolves Q1 and provides the baseline anchors (advances, impairment, CLR, NIM, HEPS, DPS, guidance) needed before D003 statement-level verification.

================================================================================
## SECTION 2: [D002] Highlights (part 1/2, p.3-6)
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section D002 | [AFS] physical page 3 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  | 1 |
| --- | --- | --- | --- | --- | --- |
| **Key highlights** | | | | | |
| **for the half year ended 31 March 2026** | | | | | |
| **Nutun South Africa and Nutun International remain customer-centric solution providers. Each has a clearly defined target** | | | | | |
| **market, an established client base, a streamlined operating structure and an experienced management team. These strengths** | | | | | |
| **support their positions in the South African collections and recovery market and the South African business process** | | | | | |
| **outsourcing (“BPO”) offshoring sector.** | | | | | |
| **Nutun South Africa focuses exclusively on collections and recovery services for clients in South Africa, both as a principal** | | | | | |
| **through the acquisition of unsecured non-performing loan (“NPL”) portfolios and as an agent on behalf of clients in the** | | | | | |
| **financial services, specialist lending and retail sectors.** | | | | | |
| **Nutun International specialises in BPO customer engagement services, including customer acquisition and retention,** | | | | | |
| **customer experience, and collections and recovery services for clients located in the United Kingdom, the United States and** | | | | | |
| **Australia. These clients operate mainly in the utilities, financial services, retail, telecommunications and e-commerce sectors.** | | | | | |
| **Growth is targeted in market segments where the business has entrenched expertise and can deliver innovative, value-added** | | | | | |
| **services that differentiate it from competitors.** | | | | | |
| **Performance – core continuing operations** | | | | | |
| **Refer to the segmental information in note 7 of the unaudited financial statements for the half year ended 31 March 2026** | | | | | |
| **for the reconciliation to the IFRS disclosure.** | | | | | |
|  | Half year |  | Half year |  |  |
|  | ended |  | ended |  |  |
|  | 31 March 31 March |  |  |  |  |
|  | 2026 |  | 2025 |  |  |
| Key Performance Indicators (Rm) | (“H1 2026”) (“H1 2025”) |  |  | Change |  |
| Revenue and other income | 1 610 |  | 1 480 | 9% |  |
| Nutun South Africa | 1 051 |  | 917 | 15% |  |
| Nutun International | 559 |  | 563 | (1%) |  |
| Operating costs | 820 |  | 865 | 5% |  |
| Nutun South Africa | 341 |  | 395 | 14% |  |
| Nutun International | 479 |  | 470 | (2%) |  |
| EBITDA | 790 |  | 615 | 28% |  |
| Nutun South Africa | 710 |  | 522 | 36% |  |
| Nutun International | 80 |  | 93 | (15%) |  |
| **Amortisation of Purchased Book Debts (“PBD”) and** | | | | | |
| Right to Collect (“RTC”) | 597 |  | 422 | (41%) |  |
| Net interest cost | 216 |  | 233 | 7% |  |
| Continuing core loss | (63) |  | (71) | 11% |  |
| PBD and RTC |  |  |  |  |  |
| Cost of acquisitions | 410 |  | 272 | 51% |  |
| Carrying value | 4 489 |  | 4 353 | 3% |  |
| Estimated remaining collections | 8 366 |  | 7 808 | 7% |  |
| Clients |  |  |  |  |  |
| Nutun South Africa | 20 |  | 23 | (13%) |  |
| Nutun International | 36 |  | 35 | 3% |  |
| Nutun International billable seats | 2 491 |  | 2 069 | 20% |  |

--- Section D002 | [AFS] physical page 4 | area selection | Commentary ---
                                                                                  
                                                                                  
                   Condensed consolidated financial statements for the half year ended 31 March 2026 2
                                                                                  
                                                                                  
      Key highlights continued                                                    
      for the half year ended 31 March 2026                                       
                                                                                  
      Performance   – core continuing  operations                                 
                                                   continued                      
      Continuing core earnings improved to a loss of R63 million from a loss of R71 million in H1 2025, primarily due to:
      • Nutun South Africa                                                        
        – PBD collections improved by 28% to R773 million impacted by PBD acquisitions in the second half of FY 2025 of R593 million
         and in the first half of FY 2026 of R382 million. Collections were also favourably impacted by enhanced collection
         methodologies despite the continued subdued economic environment and more recent geopolitical uncertainty.
        – RTC revenue improved by 27% to R116 million impacted by acquisitions in the second half of FY 2025 of R77 million and
         in the first half of FY 2026 of R28 million, in addition to the collections enhancements noted above.
        – Agency commission and associated fee revenue declined by 15% to R159 million following the continued strategic shift
         to focus on larger, scalable and more profitable mandates resulting in fewer clients.
        – Other income decreased by R31 million to R4 million due to the termination of the Mobalyz management fee and a gain
         on lease modification in the prior period.                               
        – Operating costs decreased by 14% to R341 million driven by ongoing cost optimisation, primarily through headcount
         reductions.                                                              
        – EBITDA improved by 36% to R710 million, demonstrating the strong growth in Nutun South Africa’s cash generation.
        – Portfolio amortisation costs increased by 41% to R597 million driven by portfolio ageing and macro-economic factors
         linked to interest rates, inflation and consumer health & payment behaviour.
        – Net interest costs decreased by 7% to R203 million, reflecting the repo rate cuts from November 2025 and tight treasury
         management.                                                              
      • Nutun International                                                       
        – Revenue and other income decreased by 1% to R559 million due to the adverse impact of average exchange rates for
         the period of R27 million offset by a growth in billable seats from existing and new clients. Closing billable seats grew
         by 20% to 2,491 with the client base growing to 36.                      
        – Operating costs increased by only 2% due to ongoing cost optimisation despite a R19 million adverse impact of the
         translation of balance sheet items and a loss on a foreign currency hedge in addition to increased head count due
         to the increase in billable seats.                                       
        – EBITDA decreased by 15% to R80 million, mainly as a result of the adverse foreign exchange impacts of R46 million
         as noted above.                                                          
      Refer to the group continuing core results on page 4 for a reconciliation of continuing core earnings to continuing headline
      earnings to continuing basic earnings.                                      
      Performance   – group  including discontinued  operations                   
                                                     Unit   H1 2026   H1 2025     
      Core loss from continuing operations            Rm       (63)      (71)     
      Core loss from discontinued operations          Rm         -        -       
      Core loss from total operations                 Rm       (63)      (71)     
      Core loss per share from total operations      cents     (8.1)     (9.1)    
      Headline loss from continuing operations        Rm       (63)     (122)     
      Headline loss from discontinued operations      Rm         -       (13)     
      Headline loss from total operations             Rm       (63)     (135)     
      Headline loss per share from total operations  cents     (8.1)    (17.2)    
      Basic loss from continuing operations           Rm       (63)     (122)     
      Basic earnings from discontinued operations     Rm         -       58       
      Basic loss from total operations                Rm       (63)      (64)     
      Basic loss per share from total operations     cents     (8.1)     (8.2)    
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  

--- Section D002 | [AFS] physical page 5 | area selection | Commentary ---
                                                                                  
                                                                                  
                   Condensed consolidated financial statements for the half year ended 31 March 2026 3
                                                                                  
                                                                                  
      Key highlights continued                                                    
      for the half year ended 31 March 2026                                       
                                                                                  
      Operational  update  and  outlook                                           
                                                                                  
      The simplified group is focused on two priorities. The first is profitability over the short-to-medium term. The second is
      sustainable high-quality growth over the long term.                         
      Operational performance during the period was strong, particularly for Nutun South Africa. Earnings were however adversely
      affected by Rand strength and accelerated amortisation driven by forward looking macro-economic assumptions including
      an elevated interest rate forecast relative to our expectations.            
      • Balance Sheet and Liquidity                                               
        The group’s funding covenants are comfortably complied with and have approximately R0.8 billion in unutilised facilities
        as 31 March 2026.                                                         
      • Nutun South Africa                                                        
        The business continues to streamline its operations, simplify its client approach and optimise its collections framework
        and associated technology infrastructure. It has been able to invest in PBD and RTC portfolios at healthy returns during the
        period. The ongoing acquisition of PBD and RTC portfolios on healthy commercial terms, combined with the acceleration
        of amortisation of older books, continues to improve the embedded discount rate within the portfolio which will enable
        higher profitability in future years. The improvement in the macro environment however remains uncertain.
        The outlook remains positive, with confidence that the business will continue to build on the strong collection
        performance trend and achieve its book buying objectives over the medium term, as supported by rigorous credit and
        risk mitigation policies performed throughout the valuation and acquisition processes. The demonstrable, albeit early-
        stage, success that the business has seen from the rollout of its Agentic AI solutions, which cover both interactive voice
        engagement and call insight analytics across its PBD portfolio and which leverage off a sizable data repository relating to
        consumer payment behaviour and health, will enable the business to accelerate the use of the proven technology into the
        remainder of its collection universe further enhancing the efficiency, effectiveness and profitability of its architecture.
      • Nutun International                                                       
        While the business grew its billable seats during the period the Rand strength exerted significant pressure on margins,
        the AI impact on contact centers started to drive down some inbound customer demand, and the current geopolitical
        environment continues to drive foreign exchange volatility. The BPO market remains highly competitive globally and the
        majority of growth continues to come from existing client mandates. Operational service delivery, driving efficiencies
        and demonstrating practical innovation remains a key driver of client acquisition and retention.
        Nutun International continues to focus on diversification of its services to handle more complex matters, specifically
        focusing on providing end-to-end services in the recoveries space, benefitting from the Nutun South Africa experience
        and technology. Geographically, the group is investing for growth in the United Kingdom and United States. Short and
        medium term risks include the continued Rand strength exerting pressure on margins and uncertainty regarding the future
        of the Department of Trade and Industry incentives, which support the BPO industry.
        We have used the learnings from our South African business and commenced an AI and automation strategy across
        our operational platforms, which will yield measurable improvements in workforce productivity and cost efficiency.
        Through the deployment of AI-enabled tools in quality assurance, workforce management, people orchestration and
        certain customer facing functions, we are reducing our payroll-to-revenue ratio while simultaneously improving the
        proportion of billable advisors relative to non-billable support headcount. These structural efficiencies are expected
        to deliver sustained reductions in operating costs, including lower technology subscription expenditure, reduced
        physical infrastructure requirements, and an improved cost-to-serve per transaction.
        Management is confident that the progressive integration of AI into our service delivery model will enhance operating
        margins and strengthen our competitive positioning as a technology-led BPO partner of choice.
      • Technology and AI                                                         
        The early but tangible benefits that AI can have on the group, as referred to above in both Nutun South Africa and
        Nutun International, are evident and investment will continue in this area.
      Dividend                                                                    
      As communicated in FY 2023, cash dividends have been suspended, with no cash dividend being declared in the
      current period.                                                             
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  

--- Section D002 | [AFS] physical page 6 | area selection | Commentary ---
                                                                                  
                                                                                  
                   Condensed consolidated financial statements for the half year ended 31 March 2026 4
                                                                                  
                                                                                  
      Key highlights continued                                                    
      for the half year ended 31 March 2026                                       
                                                                                  
      Basis of preparation                                                        
                                                                                  
      The condensed consolidated financial results for the six months ended 31 March 2026 have been prepared under the
      supervision of Robert Huddy CA(SA). The financial information on which this announcement is based has not been reviewed
      and reported on by Nutun Limited’s auditors. The condensed consolidated financial results for the six months ended
      31 March 2026 have been prepared in accordance with the JSE Listings Requirements, International Financial Reporting
      Standards IFRS Accounting Standards including IAS 34 – Interim Financial Reporting, the SAICA Financial Reporting Guides
      as issued by the Accounting Practices Committee and Financial Pronouncements as issued by the Financial Reporting
      Standards Council as well as the requirements of the Companies Act, 71 of 2008. The accounting policies applied in the
      preparation of the condensed consolidated financial statements for the six months ended 31 March 2026, are in accordance
      with IFRS Accounting Standards and are consistent, in all material respects, with those detailed in Nutun Limited’s
      consolidated financial statements for the 2025 financial year. Any forecast financial information has not been reviewed
      or reported on by the company’s auditors.                                   
      Group  continuing  core  results                                            
      Nutun assesses its performance using core continuing earnings, an alternative non-IFRS profit measure, alongside IFRS
      profit. Non-IFRS measures are not uniformly defined nor used by all entities and may not be comparable with similarly labelled
      measures and disclosures provided by other entities. Management considers that core continuing earnings is an appropriate
      alternative performance measure to enhance the comparability and understanding of the financial performance of the group.
      The group has set out its policy to calculate core continuing earnings below.
      Nutun calculates headline earnings in accordance with the latest SAICA Circular 1/2023 ‘Headline Earnings’.
      Core continuing earnings is calculated by adjusting headline earnings for the following:
      • Once-off transaction costs which are directly attributable to corporate activity (primarily legal and consulting fees).
      • Adjustments on put and call options over non-controlling interests, namely imputed interest on the put option liability,
        re-measurements of the put option liability and fair value adjustments on the call option derivative.
      • Once-off or accelerated items, where these are reasonably expected not to re-occur in the ordinary course of business
        in future reporting periods.                                              
      • Adding back specified headline earnings exclusions, if the gain/loss is considered part of Nutun’s normal operations.
      These adjustments are considered annually based on the transforming nature of the group. Management is responsible for
      the calculation of core continuing earnings and determining the inclusions and exclusions in accordance with the policy.
      The reconciliation of continuing basic loss, continuing headline loss and core continuing loss is as follows:
      Rm                                            Notes   H1 2026   H1 2025     
      Continuing basic and headline loss                       (63)     (122)     
      Transaction costs                                1         -        4       
      Impairment of financial assets held by an associate 2      -       47       
      Core continuing loss                                     (63)      (71)     
      Note 1: Once-off costs incurred in relation to the restructuring of the group’s funding arrangements during FY 2025.
      Note 2: Impairment of financial assets that are held by TC Global Finance.  
      The reconciliation of discontinued basic loss, discontinued headline loss and core discontinued loss is as follows:
      Rm                                             Note    H1 2026  H1 2025     
      Discontinued basic earnings                                –       58       
      Profit on disposal of Nutun Transact                       -       (71)     
      Discontinued headline loss                                 -       (13)     
      Transaction costs                                1         -       13       
      Core discontinued loss                                     -        –       
      Note 1: Once-off costs incurred in relation to the disposal of Nutun Transact during FY 2025.

### [ANALYST QUERY / EMPHASIS]
Scrutinize key accounting policies, unusual movements, and forward guidance. This is one capture, not proof of whole-report coverage. Adjacent tables/footnotes may need verification.

### [SECTION READING RESPONSE / DETERMINATION]
### 1. Answers to Stored Questions for This Section

**Q-3df04995ff2f4c6a [high] — Extract headline financial metrics (Gross Advances, Net Advances, impairment charge, CLR %, NIM %, HEPS, DPS) and any management guidance/targets stated in Key Highlights, and confirm the printed-vs-physical page offset.**
- **Status**: `Partially resolved (remainder stays open for D003)`
- **Answer & evidence**: This is a **collections/BPO group, not a lender with a loan book** — there are no "Gross Advances / Net Advances / impairment charge / CLR / NIM" lines in the Key Highlights. The relevant credit-asset metrics are the **PBD and RTC portfolios** (purchased book debts / right to collect):
  - PBD & RTC **cost of acquisitions** R410m (H1 2026) vs R272m (H1 2025), +51% `[D002, physical PDF p. 3]`
  - PBD & RTC **carrying value** R4,489m vs R4,353m, +3% `[D002, physical PDF p. 3]`
  - PBD & RTC **estimated remaining collections (ERC)** R8,366m vs R7,808m, +7% `[D002, physical PDF p. 3]`
  - **Amortisation of PBD and RTC** R597m vs R422m, +41% `[D002, physical PDF p. 3]`
  - **Net interest cost** R216m vs R233m, −7% `[D002, physical PDF p. 3]` — **note internal inconsistency**: p. 4 commentary states Nutun SA net interest cost "decreased by 7% to **R203 million**" `[D002, physical PDF p. 4]` vs R216m in the p. 3 table. R203m + R13m (International) = R216m, so the R203m is the SA segment only; the table R216m is group. Flagged as a reconciliation item (see Q-new below).
  - **Revenue and other income** R1,610m vs R1,480m (+9%); **Operating costs** R820m vs R865m (−5%); **EBITDA** R790m vs R615m (+28%) `[D002, physical PDF p. 3]`
  - **Core continuing loss** R(63)m vs R(71)m; **Headline loss** R(63)m vs R(135)m; **Basic loss** R(63)m vs R(64)m `[D002, physical PDF p. 4]`
  - **Core loss per share** (8.1)c vs (9.1)c; **Headline LPS** (8.1)c vs (17.2)c; **Basic LPS** (8.1)c vs (8.2)c `[D002, physical PDF p. 4]`
  - **DPS**: **nil** — "cash dividends have been suspended, with no cash dividend being declared in the current period" `[D002, physical PDF p. 5]`
  - **Guidance/targets**: no numeric guidance. Qualitative only — "profitability over the short-to-medium term" and "sustainable high-quality growth over the long term"; "outlook remains positive" for Nutun SA; Nutun International flags Rand strength, AI-driven inbound demand decline, and **uncertainty over DTI incentives** `[D002, physical PDF p. 5]`.
  - **Page offset confirmed**: printed page label = physical PDF page − 2 (physical p. 3 → printed "1"; p. 4 → "2"; p. 5 → "3"; p. 6 → "4"). `[D002, physical PDF pp. 3–6]`
  - **Remainder open**: the actual IFRS income statement / balance sheet lines (NII, NIR, opex, impairment, advances) must be captured in D003.

**Q-995d98c7cabc40ba [high] — Capture SoFP and income statement values (gross/net advances, ECL allowance, Stage 1/2/3, NII, NIR, opex, impairment).**
- **Status**: `Partially resolved (remainder stays open for D003)`
- **Answer & evidence**: Only the **P&L top-line and PBD/RTC carrying values** are visible here; no advances, no ECL allowance, no Stage 1/2/3 split, no separate NII/NIR/impairment lines. Captured: Revenue R1,610m; Operating costs R820m; EBITDA R790m; PBD/RTC amortisation R597m; Net interest cost R216m; PBD/RTC carrying value R4,489m `[D002, physical PDF p. 3]`. The full statement of financial position and income statement (with ECL staging) remain to be captured in **D003**.

**Q-64b704d06ed84c90 [medium] — Cash flow items (write-offs, recoveries, debt raised/repaid, dividends).**
- **Status**: `Partially resolved (remainder stays open for D003)`
- **Answer & evidence**: Only **dividends** confirmed here — nil declared, suspended since FY 2023 `[D002, physical PDF p. 5]`. No write-offs, recoveries, or debt movement figures in this section. Remainder open for **D003**.

**Q-336536b6077249e3 [medium] — IFRS 9 ECL staging note, SICR, macro overlay, write-off policy, rescheduling, covenants.**
- **Status**: `Partially resolved (remainder stays open for D003)`
- **Answer & evidence**: No IFRS 9 ECL staging, SICR, or write-off policy disclosed in this section. **Covenant statement captured**: "The group's funding covenants are comfortably complied with and have approximately **R0.8 billion in unutilised facilities** as at 31 March 2026" `[D002, physical PDF p. 5]` — qualitative only, no covenant ratios or headroom figures. **Macro overlay signal**: "accelerated amortisation driven by forward looking macro-economic assumptions including an **elevated interest rate forecast relative to our expectations**" `[D002, physical PDF p. 5]` — this is a forward-looking assumption change affecting PBD/RTC amortisation, not an IFRS 9 ECL overlay. Full ECL/SICR/write-off/covenant detail remains open for **D003**.

**Q-47cc084806ec463d [low] — Physical p. 38 nature.**
- **Status**: `Open — not addressed by this section` (carried forward to D004).

---

### 2. Footnote & Qualification Deep-Dive

- **"The financial information on which this announcement is based has not been reviewed and reported on by Nutun Limited's auditors."** `[D002, physical PDF p. 6]` — This is a **material qualification**: the entire H1 2026 condensed results are **unaudited and unreviewed**. All figures in this section carry no assurance. Forecast implication: treat all numbers as management-prepared; any credit-loss or amortisation figures in D003 must be flagged as unreviewed.
- **"Any forecast financial information has not been reviewed or reported on by the company's auditors."** `[D002, physical PDF p. 6]` — Any forward-looking statements (outlook, AI benefits, book-buying objectives) are unaudited management commentary.
- **Core continuing earnings definition (non-IFRS APM)** `[D002, physical PDF p. 6]` — Management adjusts headline earnings for: once-off transaction costs; put/call option adjustments over NCI; "once-off or accelerated items... reasonably expected not to re-occur"; and "adding back specified headline earnings exclusions, if the gain/loss is considered part of Nutun's normal operations." **This is a discretionary APM** — the "accelerated items" and "normal operations" add-backs are management-judged and could mask recurring credit/amortisation costs. The reconciliation shows only two adjustments in H1 2026 (nil transaction costs; nil associate impairment) vs H1 2025 (R4m transaction costs; R47m associate impairment), so core loss = headline loss = R(63)m this period — **no add-backs this period**, which is a positive transparency signal but the policy remains discretionary.
- **Note 1 (p. 6)**: "Once-off costs incurred in relation to the restructuring of the group's funding arrangements during FY 2025" — confirms a **funding restructuring occurred in FY 2025**; the covenant statement on p. 5 should be read against that restructured facility. No covenant ratios disclosed.
- **Note 2 (p. 6)**: "Impairment of financial assets that are held by TC Global Finance" — R47m H1 2025 associate impairment; nil this period. Confirms an **associate credit exposure (TC Global Finance)** exists outside the core PBD/RTC book — verify in D003 whether any residual carrying value or further impairment risk remains.
- **Discontinued operations note (p. 6)**: "Profit on disposal of Nutun Transact" R(71)m in H1 2025; transaction costs R13m — confirms **Nutun Transact was disposed in FY 2025**; H1 2026 discontinued = nil. No ongoing discontinued drag.
- **"Estimated remaining collections" (ERC) R8,366m vs carrying value R4,489m** `[D002, physical PDF p. 3]` — ERC is a **management-estimated, undiscounted, forward-looking metric** for PBD/RTC. The 1.86x ERC/carrying-value ratio is the key embedded-margin indicator; it is unaudited and assumption-driven (collection curves, discount rates, macro). Must be stress-tested against actual collection performance in D003.
- **"Accelerated amortisation driven by forward looking macro-economic assumptions including an elevated interest rate forecast relative to our expectations"** `[D002, physical PDF p. 5]` — This is the **single most important credit-quality signal in the section**: PBD/RTC amortisation rose 41% to R597m, partly due to **accelerated write-down of older books** on revised macro assumptions. This is effectively a **forward-looking impairment/valuation adjustment on the purchased-book-debt asset** — it depresses current earnings but (management claims) improves embedded discount rate for future profitability. Forensic question: is this a genuine one-off re-base, or the start of recurring upward revisions to amortisation as collection curves disappoint? Must be verified against the amortisation note and collection-vs-ERC tracking in D003.
- **"PBD collections improved by 28% to R773 million"** `[D002, physical PDF p. 4]` — but this is against a book that grew via R593m (H2 FY2025) + R382m (H1 FY2026) acquisitions. **Organic vs acquired collection growth is not separated** — a key forensic gap. Verify in D003 segmental/note 7.
- **"Agency commission and associated fee revenue declined by 15% to R159 million following the continued strategic shift to focus on larger, scalable and more profitable mandates resulting in fewer clients"** `[D002, physical PDF p. 4]` — client count fell from 23 to 20 (−13%) `[D002, physical PDF p. 3]`. **Client concentration risk rising** — verify top-client concentration in D003.
- **"Other income decreased by R31 million to R4 million due to the termination of the Mobalyz management fee and a gain on lease modification in the prior period"** `[D002, physical PDF p. 4]` — confirms **loss of a related-party/management fee stream (Mobalyz)**; check whether Mobalyz is a related party and whether any residual exposure exists (D003).
- **"Net interest costs decreased by 7% to R203 million, reflecting the repo rate cuts from November 2025"** `[D002, physical PDF p. 4]` — **inconsistent with p. 3 table R216m** (group). R203m appears to be SA segment only; R216m group. Flag reconciliation.
- **"approximately R0.8 billion in unutilised facilities"** `[D002, physical PDF p. 5]` — no facility size, maturity, or covenant ratio given. **Cannot assess covenant headroom** from this statement alone. Verify in D003 funding note.
- **"uncertainty regarding the future of the Department of Trade and Industry incentives, which support the BPO industry"** `[D002, physical PDF p. 5]` — a **contingent revenue/EBITDA risk** for Nutun International not quantified. Verify DTI incentive contribution in D003.
- **"AI impact on contact centers started to drive down some inbound customer demand"** `[D002, physical PDF p. 5]` — structural demand risk for the BPO segment, unquantified.
- **No footnote markers (`[^1]`, `*`) with missing definitions were found in this capture** — the only "Notes" are the two reconciliation notes on p. 6, both fully printed.

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| N1 | High | D003 | Net interest cost R216m (p. 3 table) vs "R203 million" SA segment (p. 4 commentary) `[D002, pp. 3–4]` | Reconcile group vs SA-segment net interest cost in the income statement / segment note 7; confirm R13m International net interest cost | Confirms segment funding cost split for NIM build |
| N2 | High | D003 | PBD/RTC amortisation +41% to R597m "driven by portfolio ageing and macro-economic factors" and "accelerated amortisation" `[D002, pp. 3, 5]` | Locate PBD/RTC amortisation note: split between (a) scheduled amortisation, (b) accelerated/impairment write-down, (c) FX; confirm whether acceleration is one-off or recurring | Determines whether R597m is a clean run-rate or a re-based higher amortisation level for FY2026–27 |
| N3 | High | D003 | ERC R8,366m vs carrying value R4,489m (1.86x) `[D002, p. 3]` | Check PBD/RTC note for ERC methodology, discount rate, collection-curve assumptions, and actual collections vs ERC run-off; compare H1 2026 actual collections (R773m PBD + R116m RTC) to ERC | ERC is the core embedded-value metric; if actual collections under-run ERC, carrying value is overstated |
| N4 | High | D003 | "Funding covenants comfortably complied with" + R0.8bn unutilised facilities `[D002, p. 5]` | Locate funding/borrowings note: facility sizes, maturities, covenant ratios (interest cover, LTV, DSCR), headroom, and the FY2025 "restructuring of funding arrangements" (Note 1, p. 6) | Covenant headroom and maturity wall drive liquidity/refinancing risk |
| N5 | High | D003 | "Accelerated amortisation driven by forward looking macro-economic assumptions including an elevated interest rate forecast" `[D002, p. 5]` | Check whether any IFRS 9 ECL / macro-overlay note exists for the PBD/RTC asset or associate (TC Global Finance); confirm discount-rate and macro assumptions used | Tests whether macro conservatism is genuine or a smoothing device |
| N6 | Medium | D003 | PBD collections +28% to R773m but book grew via R593m + R382m acquisitions `[D002, p. 4]` | Segment note 7: separate organic vs acquired collection growth; compute collection yield on average carrying value | Distinguishes genuine collection improvement from acquisition-driven growth |
| N7 | Medium | D003 | Agency fee revenue −15% to R159m; clients 23→20 `[D002, pp. 3–4]` | Check client concentration disclosure (top 5/10 clients as % of revenue) and any related-party client disclosure | Concentration risk to Nutun SA revenue |
| N8 | Medium | D003 | "Termination of the Mobalyz management fee" `[D002, p. 4]` | Check related-party note for Mobalyz; confirm no residual receivable/exposure and whether Mobalyz is a related party | Related-party income loss and potential receivable risk |
| N9 | Medium | D003 | "Uncertainty regarding the future of the DTI incentives" `[D002, p. 5]` | Quantify DTI incentive income in Nutun International revenue/EBITDA; check contingent-asset or government-grant note | Contingent EBITDA risk to BPO segment |
| N10 | Medium | D003 | TC Global Finance associate impairment R47m (H1 2025), nil this period `[D002, p. 6]` | Check associate carrying value and whether further impairment risk remains; confirm TC Global Finance exposure | Residual associate credit exposure |
| N11 | Low | D003 | "Unaudited and unreviewed" qualification `[D002, p. 6]` | Confirm whether any figures in D003 carry audit/review status or management-only representation | Assurance level of all forecast inputs |
| N12 | Low | D003 | Core continuing earnings APM policy (discretionary add-backs) `[D002, p. 6]` | Check whether any "accelerated items" or "normal operations" add-backs are applied in H1 2026 reconciliation beyond the two shown | APM transparency / earnings quality |

---

### 5. Baseline Forecast Inputs Captured Here

| Metric (Rm unless stated) | H1 2026 | H1 2025 | Change |
| --- | --- | --- | --- |
| Revenue and other income | 1,610 | 1,480 | +9% |
| — Nutun South Africa | 1,051 | 917 | +15% |
| — Nutun International | 559 | 563 | −1% |
| Operating costs | 820 | 865 | −5% |
| — Nutun South Africa | 341 | 395 | −14% |
| — Nutun International | 479 | 470 | +2% |
| EBITDA | 790 | 615 | +28% |
| — Nutun South Africa | 710 | 522 | +36% |
| — Nutun International | 80 | 93 | −15% |
| Amortisation of PBD and RTC | 597 | 422 | +41% |
| Net interest cost (group) | 216 | 233 | −7% |
| Net interest cost (SA segment, p.4) | 203 | — | −7% |
| Continuing core loss | (63) | (71) | +11% |
| PBD & RTC cost of acquisitions | 410 | 272 | +51% |
| PBD & RTC carrying value | 4,489 | 4,353 | +3% |
| PBD & RTC estimated remaining collections | 8,366 | 7,808 | +7% |
| PBD collections | 773 | — | +28% |
| RTC revenue | 116 | — | +27% |
| Agency commission & fee revenue | 159 | — | −15% |
| Other income | 4 | 35 | −R31m |
| Clients — Nutun SA | 20 | 23 | −13% |
| Clients — Nutun International | 36 | 35 | +3% |
| Nutun International billable seats | 2,491 | 2,069 | +20% |
| Core loss per share (cents) | (8.1) | (9.1) | — |
| Headline loss per share (cents) | (8.1) | (17.2) | — |
| Basic loss per share (cents) | (8.1) | (8.2) | — |
| DPS (cents) | nil | nil | suspended |
| Unutilised facilities | ~R0.8bn | — | — |
| Page offset | printed = physical − 2 | — | — |
| Audit status | unaudited & unreviewed | — | — |

---

### 6. Next Section to Capture

**`D003` (Primary financial statements, physical pp. 8–37)** — resolves the bulk of open items: **Q-995d98c7cabc40ba** (SoFP/income statement lines), **Q-64b704d06ed84c90** (cash flow write-offs/recoveries/debt), **Q-336536b6077249e3** (ECL/SICR/write-off/covenant notes), and new questions **N1–N12** (net interest reconciliation, PBD/RTC amortisation split, ERC methodology, funding covenants, macro assumptions, organic vs acquired collections, client concentration, Mobalyz, DTI incentives, TC Global Finance, audit status, APM add-backs).

================================================================================
## SECTION 3: [D002] Highlights (part 2/2, p.7-7)
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section D002 | [AFS] physical page 7 | area selection | Commentary ---
                                                                                  
                                                                                  
                   Condensed consolidated financial statements for the half year ended 31 March 2026 5
                                                                                  
                                                                                  
      Key highlights continued                                                    
      for the half year ended 31 March 2026                                       
                                                                                  
      Other  information                                                          
                                                                                  
      These condensed consolidated financial statements, including any forward-looking financial information, have not been
      reviewed or reported on by Nutun’s external auditors and is the responsibility of the directors.
      Changes   to the board of directors                                         
      Ian Kirk resigned as Chairman of the Board and as a member of the Remuneration and Nominations Committee and the Social,
      Ethics and Sustainability Committee on 1 January 2026.                      
      Jonathan Jawno was appointed as the Executive Chairman of the Board, to oversee the transition of the business, and as
      a member of the Social, Ethics and Sustainability Committee on 1 January 2026. Suresh Kana remained in his role of lead
      independent director.                                                       
      Albertinah Kekana resigned from the Board and as a member of the Audit and Risk Committee, Remuneration and
      Nominations Committee and the Social, Ethics and Sustainability Committee on 1 January 2026.
      Megandra Naidoo, previously the CFO of Life Healthcare, was appointed to the Board and as a member of the Audit
      and Risk Committee, Remuneration and Nominations Committee and the Social, Ethics and Sustainability Committee
      on 1 January 2026.                                                          
      Robert Amoils, the CEO of Nutun South Africa, and Ruben Moggee, the CEO of Nutun International, were appointed
      to the Board as joint CEOs on 1 January 2026.

### [ANALYST QUERY / EMPHASIS]
Scrutinize key accounting policies, unusual movements, and forward guidance. This is one capture, not proof of whole-report coverage. Adjacent tables/footnotes may need verification.

### [SECTION READING RESPONSE / DETERMINATION]
### 1. Answers to Stored Questions for This Section

- **Q-3df04995ff2f4c6a [high] [partial] — Extract headline financial metrics and confirm printed-vs-physical page offset.**
  - **Status**: `Partially resolved (remainder stays open for D003)`
  - **Answer & evidence**: This capture (physical p. 7) is the continuation of Key Highlights and contains only "Other information" — board changes and an assurance disclaimer. No new headline financial metrics, guidance, or targets appear here. The page offset is confirmed again: the printed footer reads "5" on physical p. 7, i.e. printed = physical − 2 `[D002, physical PDF p. 7]`. The financial metrics already captured from the earlier part of D002 stand; the IFRS statement-line remainder stays open for D003.

- **Q-995d98c7cabc40ba [high] [partial] — Statement of financial position / income statement values.**
  - **Status**: `Partially resolved (remainder stays open for D003)`
  - **Answer & evidence**: No statement lines, advances, ECL allowance, or Stage 1/2/3 split in this capture. Only new item relevant to earnings quality: explicit statement that the condensed consolidated financial statements (including forward-looking financial information) "have not been reviewed or reported on by Nutun's external auditors and is the responsibility of the directors" `[D002, physical PDF p. 7]`. This bears directly on Q-add37e0058a74df2 (assurance level). Remainder open for D003.

- **Q-64b704d06ed84c90 [medium] [partial] — Cash flow items.**
  - **Status**: `Partially resolved (remainder stays open for D003)`
  - **Answer & evidence**: No write-offs, recoveries, debt movements, or dividend figures in this capture. Dividend nil position unchanged (no new declaration disclosed here). Remainder open for D003.

- **Q-336536b6077249e3 [medium] [partial] — IFRS 9 ECL staging, SICR, write-off, covenants.**
  - **Status**: `Partially resolved (remainder stays open for D003)`
  - **Answer & evidence**: No ECL/SICR/write-off/covenant content in this capture. Remainder open for D003.

- **Q-add37e0058a74df2 [low] [open] — Audit/review status and APM add-backs.**
  - **Status**: `Partially resolved (assurance level answered; APM add-backs remain open for D003)`
  - **Answer & evidence**: Assurance level now explicit — the condensed consolidated financial statements, including forward-looking financial information, have **not** been reviewed or reported on by the external auditors and are the responsibility of the directors `[D002, physical PDF p. 7]`. This is a material earnings-quality flag: all H1 FY2026 figures are unaudited and unreviewed. The APM add-back detail (core continuing earnings reconciliation) is not in this capture and remains open for D003.

*(All other stored questions — Q-47cc084806ec463d, Q-007f8f020e154296, Q-e741a412cfd44a34, Q-b63cf1b01b6d4cf8, Q-b3d2bdde10394bac, Q-fec447426706441e, Q-7acc435c1ae94e77, Q-c06d7a5336224c7e, Q-e8e8f8f7354146ea, Q-174a38f8f4c04abc, Q-aea94945233b418a — relate to sections not in this capture and are carried forward unchanged in Section 4.)*

### 2. Footnote & Qualification Deep-Dive

- **Assurance disclaimer (not a footnote marker, but a small-print qualification)** `[D002, physical PDF p. 7]`: "These condensed consolidated financial statements, including any forward-looking financial information, have not been reviewed or reported on by Nutun's external auditors and is the responsibility of the directors."
  - **Implication**: No independent review/audit assurance over H1 FY2026 numbers or forward-looking statements. For a forensic credit review this raises the bar on internal reconciliation — every headline metric (revenue, EBITDA, PBD/RTC amortisation, ERC, carrying values) must be tied to the D003 primary statements and notes rather than relied upon as reviewed. Any forward-looking financial information (e.g. ERC run-off, amortisation assumptions) is director-prepared and unverified.
  - **Must verify in D003**: whether the primary statements carry the same disclaimer; whether any note flags restatement, error correction, or post-balance-sheet events.

- **Board changes** `[D002, physical PDF p. 7]`: Ian Kirk (Chairman) and Albertinah Kekana resigned 1 January 2026; Jonathan Jawno appointed Executive Chairman to "oversee the transition of the business"; Megandra Naidoo (ex-CFO Life Healthcare) appointed to Board and Audit & Risk Committee; Robert Amoils and Ruben Moggee appointed joint CEOs (Nutun SA and Nutun International respectively).
  - **Implication**: Significant board/executive turnover coinciding with the reporting period — Chairman exit, Audit & Risk Committee membership change, and a new joint-CEO structure. Governance instability is a qualitative risk factor for forecast reliability and for the credibility of director-prepared (unreviewed) forward-looking information. The "transition of the business" language is unexplained and needs context.
  - **Must verify in D003/D004**: whether the board changes are linked to any strategic review, disposal, or going-concern/restructuring event disclosed in the statements or subsequent-events note; whether the Audit & Risk Committee composition change affects sign-off.

- **No footnote markers (`[^1]`, `*`) present in this capture** — no missing footnote definitions to flag for this page.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| N1 | High | D003 | Financial statements "not reviewed or reported on by external auditors" `[D002, p. 7]` | Confirm the same disclaimer appears on the primary statements; check for any note on restatement, prior-period error correction, or post-balance-sheet events; confirm whether any figures are marked audited/reviewed. | Unreviewed figures and forward-looking info reduce forecast reliability; need to know if any line is independently assured. |
| N2 | High | D003 | Executive Chairman appointed "to oversee the transition of the business"; joint-CEO structure from 1 Jan 2026 `[D002, p. 7]` | Check subsequent-events note, going-concern statement, and any strategic-review/disposal/restructuring disclosure; confirm whether "transition" relates to a disposal, recapitalisation, or funding event. | Governance turnover + "transition" language may signal a corporate event that materially changes the forecast base case. |
| N3 | Medium | D003 | New Audit & Risk Committee member (Megandra Naidoo) appointed 1 Jan 2026; two committee members resigned `[D002, p. 7]` | Check the Audit & Risk Committee report / governance note for any qualification, internal-control deficiency, or change in risk appetite disclosure. | Committee churn during the period can coincide with control weaknesses or provisioning-policy changes. |
| N4 | Medium | D003 | Forward-looking financial information is director-prepared and unreviewed `[D002, p. 7]` | Identify which forward-looking figures exist (ERC run-off, amortisation assumptions, guidance) and confirm they are flagged as such in the notes; check sensitivity disclosures. | Determines how much weight to place on management's ERC/amortisation assumptions in the forecast. |

### 5. Baseline Forecast Inputs Captured Here

| Item | Value | Source |
| --- | --- | --- |
| Assurance status | Unreviewed / unreported by external auditors; director responsibility | `[D002, p. 7]` |
| Printed-vs-physical page offset | printed = physical − 2 (footer "5" on physical p. 7) | `[D002, p. 7]` |
| Chairman | Ian Kirk resigned 1 Jan 2026; Jonathan Jawno appointed Executive Chairman 1 Jan 2026 | `[D002, p. 7]` |
| Lead independent director | Suresh Kana (unchanged) | `[D002, p. 7]` |
| Board resignations | Albertinah Kekana (1 Jan 2026) | `[D002, p. 7]` |
| Board appointment | Megandra Naidoo (ex-CFO Life Healthcare) to Board + Audit & Risk Committee, 1 Jan 2026 | `[D002, p. 7]` |
| Joint CEOs | Robert Amoils (Nutun SA), Ruben Moggee (Nutun International), from 1 Jan 2026 | `[D002, p. 7]` |
| Dividend | Nil (no new declaration in this capture) | `[D002, p. 7]` |

*(No new financial metrics — advances, ECL, CLR, NIM, HEPS, DPS — appear on this page; prior D002 figures stand.)*

### 6. Next Section to Capture

**D003 (Primary financial statements, physical pp. 8–37)** — resolves the bulk of the open ledger: Q-995d98c7cabc40ba, Q-64b704d06ed84c90, Q-336536b6077249e3, Q-007f8f020e154296, Q-e741a412cfd44a34, Q-b63cf1b01b6d4cf8, Q-b3d2bdde10394bac, Q-fec447426706441e, Q-7acc435c1ae94e77, Q-c06d7a5336224c7e, Q-e8e8f8f7354146ea, Q-174a38f8f4c04abc, Q-aea94945233b418a, Q-add37e0058a74df2 (remainder), plus new N1–N4.

================================================================================
## SECTION 4: [D003] Primary financial statements (part 1/5, p.8-15)
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section D003 | [AFS] physical page 8 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  |  | 6 |
| --- | --- | --- | --- | --- | --- | --- |
| **Condensed consolidated statement of financial position** | | | | | | |
| at 31 March 2026 |  |  |  |  |  |  |
|  | 31 March 31 March 30 September |  |  |  |  |  |
|  | 2026 |  |  | 2025 | 2025 |  |
|  | Unaudited Unaudited |  |  |  | Audited |  |
|  | Notes Rm |  |  | Rm | Rm |  |
| Assets |  |  |  |  |  |  |
| Cash and cash equivalents | 112 |  |  | 118 | 106 |  |
| Other investments | 81 |  |  | 237 | 41 |  |
| Tax receivables | – |  |  | 3 | 5 |  |
| Trade and other receivables | 497 |  |  | 556 | 471 |  |
| Assets classified as held for sale | 4 |  |  | 2 | 4 |  |
| Purchased book debts | 1 4 489 |  |  | 4 353 | 4 677 |  |
| Other loans receivables | 5 |  |  | 2 | 4 |  |
| Equity accounted investments | 87 |  |  | 109 | 98 |  |
| Intangible assets | 67 |  |  | 82 | 63 |  |
| Property and equipment | 418 |  |  | 495 | 450 |  |
| Goodwill | 511 |  |  | 511 | 511 |  |
| Deferred tax assets | 173 |  |  | 193 | 174 |  |
| Total assets | 6 444 |  |  | 6 661 | 6 604 |  |
| Liabilities |  |  |  |  |  |  |
| Bank overdrafts | 2 273 |  |  | 457 | 364 |  |
| Tax payables | 5 |  |  | – | – |  |
| Trade and other payables | 221 |  |  | 266 | 482 |  |
| Provisions | – |  |  | 7 | – |  |
| Liabilities directly associated with assets held for sale | 6 |  |  | 1 | 4 |  |
| Derivative liabilities | 9 |  |  | – | – |  |
| Interest-bearing debt | 2 3 743 |  |  | 3 407 | 3 443 |  |
| Senior debt | 3 547 |  |  | 3 182 | 3 293 |  |
| Subordinated debt | 196 |  |  | 225 | 150 |  |
| Lease liabilities | 345 |  |  | 395 | 364 |  |
| Deferred tax liabilities | 513 |  |  | 577 | 551 |  |
| Total liabilities | 5 115 |  |  | 5 110 | 5 208 |  |
| Equity |  |  |  |  |  |  |
| Ordinary share capital | 3 5 410 |  |  | 5 414 | 5 414 |  |
| Other reserves | 30 |  |  | 10 | 30 |  |
| Retained loss | (4 111) |  |  | (3 873) | (4 048) |  |
| Total equity | 1 329 |  |  | 1 551 | 1 396 |  |
| Total equity and liabilities | 6 444 |  |  | 6 661 | 6 604 |  |

--- Section D003 | [AFS] physical page 9 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  |  | 7 |
| --- | --- | --- | --- | --- | --- | --- |
| **Condensed consolidated income statement** | | | | | | |
| **for the half year ended 31 March 2026** | | | | | | |
|  |  |  |  |  | Year ended |  |
|  | 31 March 31 March 30 September |  |  |  |  |  |
|  | 2026 |  |  | 2025 | 2025 |  |
|  | Unaudited Unaudited |  |  |  | Audited |  |
|  | Notes Rm |  |  | Rm | Rm |  |
| Gross profit from the provision of services | 326 |  |  | 393 | 703 |  |
| Revenue | 4 711 |  |  | 745 | 1 435 |  |
| Cost of revenue | (385) |  |  | (352) | (732) |  |
| Net income from purchased book debts | 69 |  |  | 53 | 244 |  |
| **Imputed interest revenue, calculated using the credit-adjusted** | | | | | | |
| effective interest rate | 383 |  |  | 333 | 683 |  |
| Interest expense | (177) |  |  | (181) | (354) |  |
| Impairment loss on principal book portfolios | (167) |  |  | (173) | (199) |  |
| Fair value movements on other financial assets | 30 |  |  | 74 | 114 |  |
| Operating costs | (445) |  |  | (560) | (1 063) |  |
| Net finance charge | (39) |  |  | (52) | (91) |  |
| Finance income | 6 |  |  | 22 | 36 |  |
| Finance charges | (45) |  |  | (74) | (127) |  |
| Net other income | 11 |  |  | 41 | 69 |  |
| Equity accounted loss | (1) |  |  | (43) | (48) |  |
| Operating loss | (79) |  |  | (168) | (186) |  |
| Non-operating (loss)/profit | (13) |  |  | 7 | 38 |  |
| Loss before tax | (92) |  |  | (161) | (148) |  |
| Income tax | 29 |  |  | 39 | 35 |  |
| Loss for the period from continuing operations | (63) |  |  | (122) | (113) |  |
| **Discontinued operations** | | | | | | |
| Profit/(loss) for the period from discontinued operations | - |  |  | 58 | (125) |  |
| Loss for the period | (63) |  |  | (64) | (238) |  |
| **Loss for the period from continuing operations** | | | | | | |
| attributable to: |  |  |  |  |  |  |
| Ordinary equity holders of the parent | (63) |  |  | (122) | (113) |  |
| Non-controlling interests | – |  |  | – | – |  |
| **Profit/(loss) for the period from discontinued operations** | | | | | | |
| attributable to: |  |  |  |  |  |  |
| Ordinary equity holders of the parent | - |  |  | 58 | (125) |  |
| Non-controlling interests | – |  |  | – | – |  |
| Loss per share (cents) |  |  |  |  |  |  |
| **From continuing operations** | | | | | | |
| Basic loss per share | 5 (8.1) |  |  | (15.6) | (14.4) |  |
| Diluted loss per share | 5 (8.1) |  |  | (15.6) | (14.4) |  |
| From total operations |  |  |  |  |  |  |
| Basic loss per share | 5 (8.1) |  |  | (8.2) | (30.3) |  |
| Diluted loss per share | 5 (8.1) |  |  | (8.2) | (30.3) |  |

--- Section D003 | [AFS] physical page 10 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  | 8 |
| --- | --- | --- | --- | --- | --- |
| **Condensed consolidated statement** | | | | | |
| **of comprehensive income** | | | | | |
| **for the half year ended 31 March 2026** | | | | | |
|  |  |  |  | Year ended |  |
|  | 31 March |  | 31 March 30 September |  |  |
|  | 2026 |  | 2025 | 2025 |  |
|  | Unaudited Unaudited |  |  | Audited |  |
|  | Rm |  | Rm | Rm |  |
| Loss for the period | (63) |  | (64) | (238) |  |
| **Other comprehensive income** | | | | | |
| **Items that may be reclassified subsequently to profit and loss:** | | | | | |
| Exchange (loss)/profit on translation of foreign operations | (4) |  | 2 | 24 |  |
| Total comprehensive loss for the period | (67) |  | (62) | (214) |  |
| **Total comprehensive loss attributable to:** | | | | | |
| Ordinary equity holders of the parent | (67) |  | (62) | (214) |  |
| Non-controlling interests | – |  | – | – |  |

--- Section D003 | [AFS] physical page 11 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  |  |  |  |  | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Condensed consolidated statement of changes in equity** | | | | | | | | | |
| **for the half year ended 31 March 2026** | | | | | | | | | |
|  |  |  |  |  |  |  | Equity |  |  |
|  |  |  |  |  |  |  | attributable |  |  |
|  |  |  |  | Share | Foreign |  | to ordinary |  |  |
|  | Number of |  |  | based | currency |  | equity | Non- |  |
|  | ordinary |  | Share | payment | translation | Retained | holders of | controlling | Total |
|  | shares |  | capital | reserve | reserve | loss | the parent | interests | equity |
|  | million |  | Rm | Rm | Rm | Rm | Rm | Rm | Rm |
| Balance at 30 September 2024 - Audited | 784 |  | 5 414 | 26 | 3 | (3 788) | 1 655 | 3 | 1 658 |
| Total comprehensive loss | – |  | – | – | 2 | (64) | (62) | – | (62) |
| Loss for the period | – |  | – | – | – | (64) | (64) | – | (64) |
| Other comprehensive income | – |  | – | – | 2 | – | 2 | – | 2 |
| Transactions with non-controlling interests | – |  | – | – | – | (27) | (27) | (3) | (30) |
| Grant of conditional share plans | – |  | – | (5) | – | – | (5) | – | (5) |
| Settlement of conditional share plans | – |  | – | (3) | – | 2 | (1) | – | (1) |
| Cancellation of conditional share plans | – |  | – | (13) | – | 4 | (9) | – | (9) |
| Balance at 31 March 2025 - Unaudited | 784 |  | 5 414 | 5 | 5 | (3 873) | 1 551 | – | 1 551 |
| Total comprehensive loss | – |  | – | – | 22 | (174) | (152) | – | (152) |
| Loss for the period | – |  | – | – | – | (174) | (174) | – | (174) |
| Other comprehensive income | – |  | – | – | 22 | – | 22 | – | 22 |
| Grant of conditional share plans | – |  | – | (2) | – | – | (2) | – | (2) |
| Cancellation of conditional share plans | – |  | – | – | – | (1) | (1) | – | (1) |
| Balance at 30 September 2025 - Audited | 784 |  | 5 414 | 3 | 27 | (4 048) | 1 396 | – | 1 396 |
| Total comprehensive loss | – |  | – | – | (4) | (63) | (67) | – | (67) |
| Loss for the period | – |  | – | – | – | (63) | (63) | – | (63) |
| Other comprehensive loss | – |  | – | – | (4) | – | (4) | – | (4) |
| Grant of conditional share plans | – |  | – | 4 | – | – | 4 | – | 4 |
| Treasury shares acquired | (4) |  | (4) | – | – | – | (4) | – | (4) |
| Balance at 31 March 2026 - Unaudited | 780 |  | 5 410 | 7 | 23 | (4 111) | 1 329 | – | 1 329 |

--- Section D003 | [AFS] physical page 12 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  | 10 |
| --- | --- | --- | --- | --- | --- |
| **Condensed consolidated statement of cash flows** | | | | | |
| **for the half year ended 31 March 2026** | | | | | |
|  |  |  |  | Year ended |  |
|  | 31 March 31 March |  |  | 30 September |  |
|  | 2026 |  | 2025 | 2025 |  |
|  | Unaudited Unaudited |  |  | Audited |  |
|  | Rm |  | Rm | Rm |  |
| **Cash flow from operating activities** | | | | | |
| Cash utilised by operations | (50) |  | (103) | (338) |  |
| Interest received | 3 |  | 16 | 15 |  |
| Interest paid | (225) |  | (251) | (468) |  |
| Income taxes refunded/(paid) | 2 |  | (4) | (15) |  |
| **Cash flow from operating activities before changes** | | | | | |
| in operating assets and working capital | (270) |  | (342) | (806) |  |
| Decrease in operating assets | 182 |  | 390 | 681 |  |
| Loans and advances | - |  | 6 | 3 |  |
| Purchased book debts | 182 |  | 384 | 678 |  |
| Changes in working capital | (23) |  | (261) | (172) |  |
| (Increase)/decrease in trade and other receivables | (25) |  | (63) | 21 |  |
| Decrease in other loans receivable | - |  | 2 | 25 |  |
| Increase/(decrease) in trade and other payables | 2 |  | (200) | (218) |  |
| Net cash utilised by operating activities | (111) |  | (213) | (297) |  |
| **Cash flow from investing activities** | | | | | |
| Acquisition of property and equipment | (17) |  | (13) | (51) |  |
| Proceeds on disposal of property and equipment | - |  | - | 10 |  |
| Acquisition of intangible assets | (13) |  | (5) | (23) |  |
| Dividends from equity accounted investment | 6 |  | 19 | 25 |  |
| Proceeds on disposal of subsidiary (net of cash disposed) | - |  | 398 | 398 |  |
| Deposits into other investments | (37) |  | - | - |  |
| Withdrawals from other investments | - |  | 38 | 243 |  |
| Proceeds on disposal of intangible assets | - |  | - | 1 |  |
| Net cash (utilised)/generated by investing activities | (61) |  | 437 | 603 |  |
| **Cash flow from financing activities** | | | | | |
| Proceeds from interest-bearing liabilities | 1 145 |  | 976 | 1 590 |  |
| Settlement of interest-bearing liabilities | (842) |  | (1 812) | (2 396) |  |
| Draw-down of bank overdrafts | 3 178 |  | 3 694 | 6 370 |  |
| Settlement of bank overdrafts | (3 269) |  | (3 519) | (6 289) |  |
| Repayment of lease liabilities | (30) |  | (35) | (62) |  |
| Acquisition of treasury shares | (4) |  | - | - |  |
| Net cash generated/(utilised) by investing activities | 178 |  | (696) | (787) |  |
| Net increase/(decrease) in cash and cash equivalents | 6 |  | (472) | (482) |  |
| Cash and cash equivalents at the beginning of the period | 107 |  | 588 | 588 |  |
| **Effects of exchange rate changes on the balance of cash held** | | | | | |
| in foreign currencies | - |  | 2 | 1 |  |
| Cash and cash equivalents at the end of period* | 113 |  | 118 | 107 |  |

* Cash and cash equivalents presented include R1 million (31 March 2025: R2 million; 30 September 2025: R1 million) of cash included in assets held for sale.

--- Section D003 | [AFS] physical page 13 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  | 11 |
| --- | --- | --- | --- | --- | --- |
| **Notes to the condensed consolidated** | | | | | |
| **financial statements** | | | | | |
| **for the half year ended 31 March 2026** | | | | | |
| 1 Purchased book debts |  |  |  |  |  |
| **Purchased credit-impaired financial assets (principal book portfolios) are those that, at the date of initial recognition** | | | | | |
| **(acquisition), are credit-impaired. The group purchases its portfolios at a deep discount that reflects the incurred** | | | | | |
| credit losses. |  |  |  |  |  |
| **Principal book portfolios are portfolios of written-off consumer debts purchased at prices below the nominal** | | | | | |
| **receivable amounts. Principal book portfolios are reflected at amortised cost on a portfolio basis. Cost includes** | | | | | |
| **amounts payable to the vendor and other direct acquisition costs. Principal book portfolios reflected below include** | | | | | |
| **cumulative changes in lifetime expected credit losses since acquisition as a loss allowance. The amount of the change** | | | | | |
| **in lifetime expected credit losses is reflected as an impairment gain or loss in profit or loss. Favourable changes in** | | | | | |
| **lifetime expected credit losses (where collections on portfolios are expected to outperform the collections expected** | | | | | |
| **when the portfolios were acquired) are recognised as an impairment gain even if the lifetime expected credit losses** | | | | | |
| **are less than the value of expected credit losses that were included in the estimated cash flows when acquired.** | | | | | |
| **Other financial assets relate to purchased book debt contracts where Nutun does not have title of the underlying** | | | | | |
| **portfolio. The portfolios include non-performing accounts held by South African banks and credit providers.** | | | | | |
| **Nutun’s return on the portfolio is driven mainly by its collection activities and performance. Nutun has no recourse** | | | | | |
| **to the banks or credit providers. Under certain circumstances, the titleholder may retract some of the underlying** | | | | | |
| **accounts and dispose thereof to third parties with Nutun being entitled to a portion of the proceeds. The terms of** | | | | | |
| **these contracts therefore do not give rise to cash flows that are solely payments of principal and interest as it is not** | | | | | |
| **consistent with a basic lending arrangement. Accordingly, these purchased book debts are measured on a fair value** | | | | | |
| **basis. Refer to note 6.3.** | | | | | |
|  | 31 March 31 March |  |  | 30 September |  |
|  | 2026 |  | 2025 | 2025 |  |
|  | Unaudited Unaudited |  |  | Audited |  |
|  | Rm |  | Rm | Rm |  |
| **Expected to be recovered after 12 months** | | | | | |
| Principal book portfolio | 2 688 |  | 2 592 | 2 853 |  |
| Other financial assets | 490 |  | 500 | 546 |  |
|  | 3 178 |  | 3 092 | 3 399 |  |
| **Expected to be recovered within 12 months** | | | | | |
| Principal book portfolio | 1 157 |  | 1 098 | 1 122 |  |
| Other financial assets | 154 |  | 163 | 156 |  |
|  | 1 311 |  | 1 261 | 1 278 |  |
| Total purchased book debts | 4 489 |  | 4 353 | 4 677 |  |
| 1.1 Principal book portfolio* |  |  |  |  |  |
| **Reconciliation of movements in the period** | | | | | |
| Balance at the beginning of the period | 3 975 |  | 3 831 | 3 831 |  |
| Additions | 382 |  | 265 | 857 |  |
| Net cash collections** | (728) |  | (566) | (1 197) |  |
| **Interest calculated using the credit-adjusted effective** | | | | | |
| interest rate (CAEIR) | 383 |  | 333 | 683 |  |
| Impairment loss | (167) |  | (173) | (199) |  |
| Balance at the end of the period | 3 845 |  | 3 690 | 3 975 |  |
| 1.2 Other financial assets |  |  |  |  |  |
| **Reconciliation of movements in the period** | | | | | |
| Balance at the beginning of the period | 702 |  | 672 | 672 |  |
| Additions | 28 |  | 7 | 84 |  |
| Cash collections | (116) |  | (90) | (168) |  |
| Fair value movements | 30 |  | 74 | 114 |  |
| Balance at the end of the period | 644 |  | 663 | 702 |  |

*  Purchased book debts of R3 845 million (31 March 2025: R3 690 million; 30 September 2025: R3 975 million) have been pledged as security for the
interest-bearing liabilities and bank overdrafts per the pledge agreement, refer to note 2. These assets are pledged for the duration of the agreement.
The terms of the pledges are usual and customary to such agreements.
** Included in net collections are gross collections of R773 million (31 March 2025: R604 million; 30 September 2025: R1 280 million) and directly
attributable and incremental collection costs of R45 million (31 March 2025: R38 million; 30 September 2025: R83 million).

--- Section D003 | [AFS] physical page 14 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  | 12 |
| --- | --- | --- | --- | --- | --- |
| **Notes to the condensed consolidated financial statements continued** | | | | | |
| **for the half year ended 31 March 2026** | | | | | |
| 2 Interest-bearing liabilities and bank overdrafts |  |  |  |  |  |
|  | 31 March 31 March |  |  | 30 September |  |
|  | 2026 |  | 2025 | 2025 |  |
|  | Unaudited Unaudited* |  |  | Audited |  |
|  | Rm |  | Rm | Rm |  |
| Type of loan |  |  |  |  |  |
| Notes | 822 |  | 929 | 802 |  |
| Loans | 2 921 |  | 2 478 | 2 641 |  |
| Bank overdrafts | 273 |  | 457 | 364 |  |
| Total interest-bearing liabilities | 4 016 |  | 3 864 | 3 807 |  |
| **Classes of interest-bearing liabilities** | | | | | |
| Senior debt | 3 547 |  | 3 182 | 3 293 |  |
| Subordinated debt | 196 |  | 225 | 150 |  |
| Bank overdrafts | 273 |  | 457 | 364 |  |
| Total interest-bearing liabilities | 4 016 |  | 3 864 | 3 807 |  |
| **Maturity profile** | | | | | |
| Payable within 12 months | 1 396 |  | 1 039 | 1 237 |  |
| Payable thereafter | 2 620 |  | 2 825 | 2 570 |  |
| Total interest-bearing liabilities | 4 016 |  | 3 864 | 3 807 |  |
| Total undrawn overdraft facilities | 475 |  | 43 | 136 |  |

*  Comparative disclosure for 31 March 2025 has been presented for the first time to enhance the overall presentation of the financial statements.

--- Section D003 | [AFS] physical page 15 | area selection | Financial note ---
                                                                                                                    
                                                                                                                    
                   Condensed consolidated financial statements for the half year ended 31 March 2026           13   
                                                                                                                    
                                                                                                                    
      Notes to the condensed consolidated financial statements continued                                            
      for the half year ended 31 March 2026                                                                         
                                                                                                                    
      2    Interest-bearing  liabilities and bank overdrafts                                                        
                                                            continued                                               
                                                                                    31 March 31 March 30 September  
                                                                                       2026     2025      2025      
                                                                                    Unaudited Unaudited** Audited   
      2.1  Type of loan Description Date issued Interest rate    Maturity date          Rm       Rm        Rm       
           Notes*                                                                                                   
           Notes   Bullet     15/11/2022 to 31/10/2025 3 Month JIBAR plus 2.8% to 3.7% 31/12/2026 to 31/03/2032 671 675 734
           Notes   Amortising 13/07/2023 to 23/10/2025 3 Month JIBAR plus 3.0% to 3.1% 29/09/2028 151 73   68       
           Notes   Bullet     15/02/2022      3 Month JIBAR plus 3.39% 18/09/2025        –      181         –       
           Total                                                                       822      929       802       
           Loans                                                                                                    
           Senior* Amortising 13/07/2023 to 07/04/2025 3 Month JIBAR plus 2.85% to 5.2% 30/06/2026 to 31/12/2030 1 738 1 393 1 430
           Senior* Bullet     09/12/2021 to 09/05/2025 3 Month JIBAR plus 3% to 3.28% 31/12/2026 to 28/06/2030 690 635 690
           Subordinated Amortising 03/10/2025 3 Month JIBAR plus 4.6% 29/09/2028        46        –         –       
           Subordinated Bullet 18/03/2022 to 13/09/2023 3 Month JIBAR plus 5.0% 31/03/2027 to 30/09/2027 150 225 150
           Senior* Revolving Facility 17/12/2024 to 20/02/2025 Prime minus 0.25% to 0.35% 30/09/2028 297 225 371    
           Total                                                                      2 921    2 478     2 641      
           * Purchased book debts, trade and other receivables and cash and cash equivalents have been pledged as security for the interest-bearing liabilities and bank overdrafts per the pledge agreement. These assets are pledged for the
            duration of the agreement. The terms of the pledges are usual and customary to such agreements.         
           ** Comparative disclosure for 31 March 2025 has been presented for the first time to enhance the overall presentation of the financial statements.

### [ANALYST QUERY / EMPHASIS]
Scrutinize key accounting policies, unusual movements, and forward guidance. This is one capture, not proof of whole-report coverage. Adjacent tables/footnotes may need verification.

### [SECTION READING RESPONSE / DETERMINATION]
> APPLICATION QUALIFICATION: DeepSeek ledger updates failed evidence validation. No existing question was resolved by this response. All prior questions remain open; any resolution claim in the narrative is unverified. Only valid new questions were retained.

### 1. Answers to Stored Questions for This Section

**Q-3df04995ff2f4c6a [high] — Extract headline financial metrics and confirm page offset**
- **Status**: `Partially resolved (remainder stays open for D002/D003 notes)`
- **Answer & evidence**: Page offset confirmed: printed footer "6" on physical p. 8, "7" on p. 9, "8" on p. 10, "9" on p. 11, "10" on p. 12, "11" on p. 13, "12" on p. 14, "13" on p. 15 → printed = physical − 2. Statement-level metrics captured: total assets R6,444m (31 Mar 2026) vs R6,661m (31 Mar 2025) vs R6,604m (30 Sep 2025); total equity R1,329m vs R1,551m vs R1,396m; loss for the period R(63)m vs R(64)m vs R(238)m; basic LPS total operations (8.1)c vs (8.2)c vs (30.3)c `[D003, physical PDF pp. 8–9]`. No HEPS, DPS, CLR%, NIM% or management guidance/targets appear in this capture — those remain open for D002/D003 notes.

**Q-995d98c7cabc40ba [high] — Statement lines, advances, ECL allowance, Stage 1/2/3 split**
- **Status**: `Partially resolved (Stage 1/2/3 split and ECL allowance remain open)`
- **Answer & evidence**: Statement lines captured. Purchased book debts R4,489m (31 Mar 2026) vs R4,353m (31 Mar 2025) vs R4,677m (30 Sep 2025) `[D003, physical PDF p. 8]`. Principal book portfolio gross reconciliation: opening R3,975m + additions R382m − net cash collections R728m + CAEIR interest R383m − impairment loss R167m = closing R3,845m `[D003, physical PDF p. 13]`. **No Stage 1/2/3 ECL staging table, no separate ECL allowance balance, and no SICR disclosure appear in this capture** — the impairment loss of R167m is a P&L charge only; the closing carrying value is stated net. Stage split and allowance balance remain open for later D003 notes (pp. 16–37).

**Q-64b704d06ed84c90 [medium] — Cash flow: write-offs, recoveries, debt raised/repaid, dividends**
- **Status**: `Partially resolved (write-offs/recoveries not separately disclosed)`
- **Answer & evidence**: Cash flow statement captured `[D003, physical PDF p. 12]`. Debt raised R1,145m; debt settled R(842)m; overdraft draw-down R3,178m / settlement R(3,269)m; lease repayments R(30)m; treasury shares R(4)m. **No dividend paid line** (consistent with nil dividend). **No gross write-off or bad-debt recovery lines** — the cash flow presents purchased book debt collections net (R182m decrease in operating assets). Net bad debt charge reconciliation (write-offs + ECL movement − recoveries) is therefore **not testable from this capture**; remains open for later notes.

**Q-336536b6077249e3 [medium] — IFRS 9 ECL staging, SICR, macro overlay, write-off policy, covenants**
- **Status**: `Partially resolved (policy narrative captured; staging/SICR/covenants remain open)`
- **Answer & evidence**: Note 1 `[D003, physical PDF p. 13]` confirms principal book portfolios are **purchased credit-impaired financial assets at initial recognition**, held at amortised cost on a portfolio basis, with cumulative changes in **lifetime ECL** since acquisition recognised as an impairment gain/loss. Favourable ECL changes (collections outperforming acquisition expectations) are recognised as an impairment **gain** even where lifetime ECL is below acquisition-date expected losses — a P&L-smoothing mechanism to scrutinise. Other financial assets (no title; non-SPPI) are at **fair value** (note 6.3 referenced but not in capture). **No SICR thresholds, DPD staging, macro scenario weightings, write-off triggers, modification/re-aging rules, or covenant terms appear in this capture** — remain open.

**Q-007f8f020e154296, Q-e741a412cfd44a34, Q-b63cf1b01b6d4cf8, Q-b3d2bdde10394bac, Q-fec447426706441e, Q-7acc435c1ae94e77, Q-c06d7a5336224c7e, Q-e8e8f8f7354146ea, Q-174a38f8f4c04abc, Q-aea94945233b418a, Q-59b88716280048c3, Q-ebf661d7f2e740cd, Q-0b9b00a6c7da4496, Q-5a1c41b2ef654626**
- **Status**: `Open` — the underlying question text for these IDs was not supplied in this prompt (only "Pending: D003" status lines). They cannot be answered without their question wording; carried forward unchanged in Section 4.

**Q-add37e0058a74df2 [low] — Audit/review status and APM add-backs**
- **Status**: `Partially resolved (assurance status confirmed; APM add-backs remain open)`
- **Answer & evidence**: Every primary statement is labelled **"Unaudited"** for 31 Mar 2026 and 31 Mar 2025, with 30 Sep 2025 labelled **"Audited"** `[D003, physical PDF pp. 8–12]`. No core continuing earnings reconciliation or "accelerated/normal operations" add-back table appears in this capture — remains open.

---

### 2. Footnote & Qualification Deep-Dive

- **Cash footnote (*), p. 12** `[D003, physical PDF p. 12]`: "Cash and cash equivalents presented include R1 million (31 March 2025: R2 million; 30 September 2025: R1 million) of cash included in assets held for sale." → Closing cash R113m includes R1m held-for-sale cash; clean-up adjustment of R1m needed for continuing-operations liquidity. Minor but confirms held-for-sale perimeter still open.

- **Note 1 pledge footnote (*), p. 13** `[D003, physical PDF p. 13]`: "Purchased book debts of R3,845 million … have been pledged as security for the interest-bearing liabilities and bank overdrafts per the pledge agreement … for the duration of the agreement." → **100% of the principal book portfolio (R3,845m) is encumbered.** This is a critical funding-structure finding: the entire purchased book debt asset base secures R4,016m of interest-bearing liabilities plus overdrafts. Asset encumbrance is effectively total; there is no unpledged collateral buffer. Must be cross-checked against covenant/security-cover terms in the funding note (not in capture).

- **Note 1 net collections footnote (**), p. 13** `[D003, physical PDF p. 13]`: "Included in net collections are gross collections of R773 million (31 March 2025: R604 million; 30 September 2025: R1 280 million) and directly attributable and incremental collection costs of R45 million (31 March 2025: R38 million; 30 September 2025: R83 million)." → Gross collections R773m − collection costs R45m = R728m net, reconciling to the movement table. **Collection cost ratio = 5.8% of gross collections** (H1 2025: 6.3%; FY2025: 6.5%) — modest efficiency improvement. Note the H1 2026 gross collections of R773m vs FY2025 R1,280m implies a **run-rate deceleration** (H1 annualised ≈ R1,546m would be growth, but H2 FY2025 alone was R676m — so H1 2026 R773m is +14% HoH; needs vintage/seasoning context). Also note: gross collections R773m vs net cash collections R728m — the R45m cost is deducted inside "net cash collections," meaning the cash flow statement's R182m "decrease in purchased book debts" is already net of collection costs.

- **Note 2 footnote (*), p. 14** `[D003, physical PDF p. 14]`: "Comparative disclosure for 31 March 2025 has been presented for the first time to enhance the overall presentation of the financial statements." → **The 31 Mar 2025 comparative interest-bearing liability maturity/type breakdown is a new disclosure, not previously presented.** This is a presentation change, not a restatement, but it means prior-period comparability for funding maturity analysis is limited to one period. Flag for consistency check in FY2026.

- **Note 2.1 footnote (*), p. 15** `[D003, physical PDF p. 15]`: Pledge footnote repeated — "Purchased book debts, trade and other receivables and cash and cash equivalents have been pledged as security…" → Confirms the encumbrance extends beyond book debts to receivables and cash. Combined with the p. 13 footnote, essentially the entire current-asset base is pledged.

- **Note 2.1 footnote (**), p. 15** `[D003, physical PDF p. 15]`: Same "comparative presented for the first time" qualification repeated for the loan-type/maturity table. → The detailed facility-level maturity and interest-rate table (JIBAR + spreads, Prime − 0.25% to 0.35%) is **new disclosure**; useful for interest-rate sensitivity but unverifiable against prior periods.

- **Note 1 policy narrative (unfootnoted but commentary-heavy), p. 13** `[D003, physical PDF p. 13]`: "Favourable changes in lifetime expected credit losses (where collections on portfolios are expected to outperform the collections expected when the portfolios were acquired) are recognised as an impairment gain even if the lifetime expected credit losses are less than the value of expected credit losses that were included in the estimated cash flows when acquired." → This is a **P&L gain-recognition mechanism on purchased credit-impaired books**. It means impairment loss of R167m in H1 2026 is a *net* figure that could be masking gross deterioration offset by favourable re-estimates. Must be decomposed in later notes (gross ECL charge vs favourable re-estimate gain). Also: "Other financial assets … Nutun has no recourse to the banks or credit providers … titleholder may retract some of the underlying accounts … measured on a fair value basis. Refer to note 6.3." → **Note 6.3 is referenced but not in this capture** — fair value methodology, retraction risk, and Level 3 inputs must be verified.

- **Missing footnote check**: No footnote markers in this capture lack a corresponding definition within the supplied pages. However, **note 6.3 (fair value of other financial assets) is cross-referenced but not supplied** — flagged as a verification question.

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| N1 | High | D003 (pp. 16–37 notes) | Principal book portfolio closing R3,845m is stated **net**; impairment loss R167m is P&L only; no ECL allowance balance or Stage 1/2/3 split disclosed `[D003, p. 13]` | Locate ECL/impairment note: gross carrying amount, cumulative ECL allowance, Stage 1/2/3 (or purchased-credit-impaired) split, coverage ratios | Needed to compute coverage %, CLR on gross advances, and assess provisioning adequacy |
| N2 | High | D003 (pp. 16–37 notes) | Policy allows **favourable ECL re-estimates recognised as impairment gains** even below acquisition-date expected losses `[D003, p. 13]` | Find impairment note decomposing R167m into gross ECL charge vs favourable re-estimate gain; check comparative H1 2025 R173m and FY2025 R199m on same basis | If gains are recurring, underlying credit deterioration is understated; affects CLR forecast |
| N3 | High | D003 (pp. 16–37 notes) | **100% of principal book portfolio (R3,845m) pledged** as security; receivables and cash also pledged `[D003, pp. 13, 15]` | Locate funding/borrowings note: security-cover ratio, LTV, borrowing-base covenant, minimum collateral thresholds, headroom | Total encumbrance = no unpledged buffer; covenant breach risk on collateral value decline |
| N4 | High | D003 (pp. 16–37 notes) | Interest-bearing liabilities R4,016m; **R1,396m payable within 12 months**; undrawn overdraft facilities only R475m `[D003, p. 14]` | Find maturity profile by facility, refinancing plan, covenant ratios (interest cover, DSCR), and going-concern statement | Refinancing wall + thin undrawn liquidity = liquidity risk to forecast |
| N5 | High | D003 (pp. 16–37 notes) | Note 6.3 referenced for **fair value of other financial assets (R644m)** but not supplied; retraction risk disclosed `[D003, p. 13]` | Locate note 6.3: fair value hierarchy level, valuation inputs, retraction/recourse terms, sensitivity | R644m (14% of book debts) at fair value with retraction risk — valuation and earnings volatility |
| N6 | Medium | D003 (pp. 16–37 notes) | Gross collections R773m vs net R728m; collection cost R45m (5.8%); H1 2026 vs H2 FY2025 (R676m implied) `[D003, p. 13]` | Find vintage/seasoning or ERC note: collection curve assumptions, ERC balance, actual vs expected collections | Tests whether collection performance is genuine or acquisition-driven; drives ERC amortisation forecast |
| N7 | Medium | D003 (pp. 16–37 notes) | Additions R382m (H1 2026) vs R265m (H1 2025) vs R857m (FY2025) — **portfolio acquisition pace decelerating HoH** `[D003, p. 13]` | Find business-combination/portfolio-acquisition note: purchase price, acquired ERC, expected collections, any contingent consideration | Acquisition-driven growth is slowing; organic collection run-off becomes the growth driver |
| N8 | Medium | D003 (pp. 16–37 notes) | Other financial assets: additions R28m, collections R116m, **fair value gain R30m** (H1 2025: R74m; FY2025: R114m) `[D003, p. 13]` | Find note 6.3 / fair value note: drivers of FV gain, whether recurring, Level 3 assumptions | FV gains R30m are 48% of the R63m loss — material to earnings quality |
| N9 | Medium | D003 (pp. 16–37 notes) | Equity accounted loss R(1)m vs R(43)m (H1 2025) vs R(48)m (FY2025); equity accounted investments R87m `[D003, pp. 8–9]` | Find associate note: TC Global Finance carrying value, share of loss, impairment | Sharp swing to near-nil loss needs explanation; residual impairment risk |
| N10 | Medium | D003 (pp. 16–37 notes) | Discontinued operations: **nil** H1 2026 vs +R58m (H1 2025) vs R(125)m (FY2025); proceeds on disposal R398m in H1 2025 `[D003, pp. 9, 12]` | Find discontinued-operations note: what was disposed, any residual liabilities/indemnities, held-for-sale assets R4m/liabilities R6m | Confirms disposal complete; check for residual exposures/warranties |
| N11 | Medium | D003 (pp. 16–37 notes) | Tax: **income tax credit R29m** on loss before tax R(92)m — effective tax rate −31.5% `[D003, p. 9]` | Find tax note: deferred tax asset recognition (R173m), basis for credit on losses, recoverability | A tax credit on a loss is an earnings-quality flag; DTA recoverability depends on forecast profits |
| N12 | Medium | D003 (pp. 16–37 notes) | Operating costs R445m vs R560m (H1 2025) — **−20.5%**; cost of revenue R385m vs R352m (+9.4%) `[D003, p. 9]` | Find opex note: breakdown, one-off items, staff costs, whether cost cut is sustainable | Cost base trajectory drives breakeven forecast |
| N13 | Low | D003 (pp. 16–37 notes) | Revenue R711m vs R745m (−4.6%); gross profit from services R326m vs R393m (−17%) `[D003, p. 9]` | Find revenue disaggregation note: SA vs International, agency fees, DTI incentives | Revenue mix and DTI contingency (carried from D002) |
| N14 | Low | D003 (pp. 16–37 notes) | Treasury shares acquired 4m shares for R4m; shares in issue down to 780m `[D003, p. 11]` | Find EPS note: weighted average shares, dilution from conditional share plans | EPS denominator for forecast |
| N15 | Low | D003 (pp. 16–37 notes) | Note 2.1: **new disclosure** of facility-level rates (JIBAR + 2.8%–5.2%; Prime − 0.25% to 0.35%) and maturities to 2032 `[D003, p. 15]` | Find interest-rate risk/sensitivity note: fixed vs floating split, hedge accounting | Interest expense forecast sensitivity to JIBAR/Prime |

---

### 5. Baseline Forecast Inputs Captured Here

| Metric (Rm unless stated) | 31 Mar 2026 (Unaudited) | 31 Mar 2025 (Unaudited) | 30 Sep 2025 (Audited) |
| --- | --- | --- | --- |
| Cash and cash equivalents | 112 | 118 | 106 |
| Other investments | 81 | 237 | 41 |
| Trade and other receivables | 497 | 556 | 471 |
| Purchased book debts (total) | 4,489 | 4,353 | 4,677 |
| — Principal book portfolio | 3,845 | 3,690 | 3,975 |
| — Other financial assets (FV) | 644 | 663 | 702 |
| Equity accounted investments | 87 | 109 | 98 |
| Intangible assets | 67 | 82 | 63 |
| Property and equipment | 418 | 495 | 450 |
| Goodwill | 511 | 511 | 511 |
| Deferred tax assets | 173 | 193 | 174 |
| **Total assets** | **6,444** | **6,661** | **6,604** |
| Bank overdrafts | 273 | 457 | 364 |
| Trade and other payables | 221 | 266 | 482 |
| Interest-bearing debt (total) | 3,743 | 3,407 | 3,443 |
| — Senior debt | 3,547 | 3,182 | 3,293 |
| — Subordinated debt | 196 | 225 | 150 |
| Lease liabilities | 345 | 395 | 364 |
| Deferred tax liabilities | 513 | 577 | 551 |
| **Total liabilities** | **5,115** | **5,110** | **5,208** |
| **Total equity** | **1,329** | **1,551** | **1,396** |
| Shares in issue (m) | 780 | 784 | 784 |
| Revenue | 711 | 745 | 1,435 |
| Cost of revenue | (385) | (352) | (732) |
| Gross profit from services | 326 | 393 | 703 |
| Net income from purchased book debts | 69 | 53 | 244 |
| Imputed interest revenue (CAEIR) | 383 | 333 | 683 |
| Interest expense | (177) | (181) | (354) |
| Impairment loss on principal book portfolios | (167) | (173) | (199) |
| Fair value movements on other financial assets | 30 | 74 | 114 |
| Operating costs | (445) | (560) | (1,063) |
| Net finance charge | (39) | (52) | (91) |
| Equity accounted loss | (1) | (43) | (48) |
| Operating loss | (79) | (168) | (186) |
| Non-operating (loss)/profit | (13) | 7 | 38 |
| Loss before tax | (92) | (161) | (148) |
| Income tax | 29 | 39 | 35 |
| Loss from continuing operations | (63) | (122) | (113) |
| Profit/(loss) from discontinued operations | – | 58 | (125) |
| **Loss for the period** | **(63)** | **(64)** | **(238)** |
| Basic LPS continuing (cents) | (8.1) | (15.6) | (14.4) |
| Basic LPS total (cents) | (8.1) | (8.2) | (30.3) |
| Gross collections (principal book) | 773 | 604 | 1,280 |
| Collection costs | 45 | 38 | 83 |
| Net cash collections (principal book) | 728 | 566 | 1,197 |
| Portfolio additions (principal book) | 382 | 265 | 857 |
| Other financial assets additions | 28 | 7 | 84 |
| Other financial assets collections | 116 | 90 | 168 |
| Interest-bearing liabilities total | 4,016 | 3,864 | 3,807 |
| — Payable within 12 months | 1,396 | 1,039 | 1,237 |
| — Payable thereafter | 2,620 | 2,825 | 2,570 |
| Undrawn overdraft facilities | 475 | 43 | 136 |
| Debt raised | 1,145 | 976 | 1,590 |
| Debt settled | (842) | (1,812) | (2,396) |
| Dividends paid | – | – | – |
| Pledged purchased book debts | 3,845 | 3,690 | 3,975 |

**Derived ratios (computed):**
- Collection cost ratio = 45/773 = **5.8%** (H1 2025: 6.3%; FY2025: 6.5%)
- Effective tax rate on loss before tax = 29/(92) = **−31.5%**
- Operating cost change YoY = **−20.5%**
- Revenue change YoY = **−4.6%**
- Gross profit from services change YoY = **−17.0%**
- Equity/total assets = 1,329/6,444 = **20.6%** (31 Mar 2025: 23.3%; 30 Sep 2025: 21.1%)
- Encumbered book debt ratio = 3,845/4,489 = **85.7%** of total purchased book debts pledged

---

### 6. Next Section to Capture

**`D003` (continued) — physical PDF pp. 16–21** (chunk 2 of 5). This will resolve the highest-priority open items: **N1** (ECL allowance and Stage 1/2/3 split), **N2** (impairment decomposition), **N3/N4** (funding covenants, maturity wall, going concern), **N5** (note 6.3 fair value), and the carried-forward D002 questions on ERC methodology, PBD/RTC amortisation, and funding restructuring.

================================================================================
## SECTION 5: [D003] Primary financial statements (part 2/5, p.16-21)
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section D003 | [AFS] physical page 16 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 14 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Notes to the condensed consolidated financial statements continued** | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| **for the half year ended 31 March 2026** | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| 3 Ordinary share capital |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | 31 March |  |  |  |  |  |  |  | 31 March 30 September |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | 2026 |  |  |  |  |  |  |  |  | 2025 |  |  |  |  |  |  |  |  |  | 2025 |  |  |  |  |  |  |  |
|  | Unaudited Unaudited |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Audited |  |  |  |  |  |  |  |
|  | Number |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |
|  | of shares |  |  |  |  |  |  |  | of shares |  |  |  |  |  |  |  |  |  |  | of shares |  |  |  |  |  |  |  |
| Authorised |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Ordinary shares | 1 000 000 000 1 000 000 000 1 000 000 000 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **Issued and fully paid up** | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| Ordinary share capital | 784 313 242 784 313 242 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 784 313 242 |  |  |  |  |  |  |  |  |  |  |
| Total ordinary shares outstanding | 780 651 033 784 313 242 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 784 313 242 |  |  |  |  |  |  |  |  |  |  |
| Ordinary shares issued | 784 313 242 784 313 242 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 784 313 242 |  |  |  |  |  |  |  |  |  |  |
| Treasury shares held by entities in the group | (3 662 209) |  |  |  |  |  |  |  |  | – |  |  |  |  |  |  |  |  |  |  |  |  | – |  |  |  |  |
| 3.1 Reconciliation of ordinary share capital |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | 31 March 31 March |  |  |  |  |  |  |  |  | 30 September |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | 2026 2025 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 2025 |  |  |  |  |  |  |  |  |  |  |
|  | Unaudited Unaudited |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Audited |  |  |  |  |  |  |  |  |  |  |
| Number | Share Number Share |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  | Share |  |  |  |  |  |  |  |
| of shares | capital* of shares capital* |  |  |  |  |  |  |  |  | of shares |  |  |  |  |  |  |  |  |  | capital* |  |  |  |  |  |  |  |
| million | Rm million Rm |  |  |  |  |  |  |  |  | million |  |  |  |  |  |  |  |  |  |  |  |  | Rm |  |  |  |  |
| **Balance at the beginning** | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| of the period | 784 5 414 784 5 414 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 784 |  |  | 5 414 |  |  |  |  |  |  |  |
| Treasury shares bought | (4) (4) – – |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | – |  |  |  |  |  | – |  |  |  |  |
| Balance at the end of the period | 780 5 410 784 5 414 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 784 |  |  | 5 414 |  |  |  |  |  |  |  |

* Net of share issue costs.
Share movements during the period
Nutun acquired 3,662,209 shares for a consideration of R3.7 million (average share price of R1 per share) during
the period. This was for the purpose of holding the shares as treasury shares to be utilised on the vestings of the
Conditional Share Plan.

--- Section D003 | [AFS] physical page 17 | area selection | Table ---
|  | Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  | 15 |
| --- | --- | --- | --- | --- | --- | --- |
| **Notes to the condensed consolidated financial statements continued** | | | | | | |
| **for the half year ended 31 March 2026** | | | | | | |
| 4 | Revenue |  |  |  |  |  |
|  |  | Nutun |  | Nutun |  |  |
|  |  | South Africa International |  |  | Total |  |
|  |  | Rm |  | Rm | Rm |  |
|  | Revenue comprises: |  |  |  |  |  |
|  | 31 March 2026 - Unaudited |  |  |  |  |  |
|  | Service fees: Over a period of time | – |  | 552 | 552 |  |
|  | Commissions and fees: At a point in time | 159 |  | – | 159 |  |
|  | Total revenue | 159 |  | 552 | 711 |  |
|  | 31 March 2025 - Unaudited* |  |  |  |  |  |
|  | Service fees: Over a period of time | – |  | 557 | 557 |  |
|  | Commissions and fees: At a point in time | 188 |  | – | 188 |  |
|  | Total revenue | 188 |  | 557 | 745 |  |
|  | 30 September 2025 - Audited |  |  |  |  |  |
|  | Service fees: Over a period of time | – |  | 1 094 | 1 094 |  |
|  | Commissions and fees: At a point in time | 341 |  | – | 341 |  |
|  | Total revenue | 341 |  | 1 094 | 1 435 |  |
|  | * This disclosure was presented for the first time in the annual financial statements for the year ended 30 September 2025 in order to enhance the overall |  |  |  |  |  |
|  | presentation of the financial statements. Comparative disclosure for 31 March 2025 has been presented for the first time. |  |  |  |  |  |
| 4.1 | Revenue disaggregation |  |  |  |  |  |
|  |  | 31 March 31 March |  |  | 30 September |  |
|  |  | 2026 |  | 2025 | 2025 |  |
|  |  | Unaudited Unaudited* |  |  | Audited |  |
|  |  | Rm |  | Rm | Rm |  |
|  | The group recognises revenue earned from the following |  |  |  |  |  |
|  | geographic regions: |  |  |  |  |  |
|  | South Africa | 159 |  | 188 | 341 |  |
|  | Australia | 27 |  | 74 | 127 |  |
|  | United Kingdom | 303 |  | 259 | 525 |  |
|  | United States | 212 |  | 224 | 428 |  |
|  | Other | 10 |  | – | 14 |  |
|  | Total revenue | 711 |  | 745 | 1 435 |  |

*  This disclosure was presented for the first time in the annual financial statements for the year ended 30 September 2025 in order to enhance the overall
presentation of the financial statements. Comparative disclosure for 31 March 2025 has been presented for the first time.

--- Section D003 | [AFS] physical page 18 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  |  | 16 |
| --- | --- | --- | --- | --- | --- | --- |
| **Notes to the condensed consolidated financial statements continued** | | | | | | |
| **for the half year ended 31 March 2026** | | | | | | |
| 5 Loss per share |  |  |  |  |  |  |
| 5.1 From total operations |  |  |  |  |  |  |
|  | 31 March |  |  | 31 March 30 September |  |  |
|  | 2026 |  |  | 2025 | 2025 |  |
|  | Units Unaudited Unaudited |  |  |  | Audited |  |
| Basic loss per share | cents (8.1) |  |  | (8.2) | (30.3) |  |
| Diluted loss per share | cents (8.1) |  |  | (8.2) | (30.3) |  |
| Headline loss per share | cents (8.1) |  |  | (17.2) | (39.4) |  |
| Diluted headline loss per share | cents (8.1) |  |  | (17.2) | (39.4) |  |
| **The calculation of loss per share is based** | | | | | | |
| **on the following data:** | | | | | | |
| Loss |  |  |  |  |  |  |
| **Loss for the purposes of basic and diluted** | | | | | | |
| loss per share | Rm (63) |  |  | (64) | (238) |  |
| Headline loss adjustments: | Rm – |  |  | (71) | (71) |  |
| Profit on disposal of business | Rm - |  |  | (100) | (100) |  |
| Tax impact | Rm - |  |  | 29 | 29 |  |
| **Loss for the purposes of headline and diluted** | | | | | | |
| headline loss per share | Rm (63) |  |  | (135) | (309) |  |
| **Weighted average numbers of shares** | | | | | | |
| **Number of ordinary shares in issue at the beginning** | | | | | | |
| of the period | million 784.3 |  |  | 784.3 | 784.3 |  |
| Effect of treasury shares bought | million (2.2) |  |  | – | – |  |
| **Weighted average number of ordinary shares for** | | | | | | |
| the purposes of basic and headline loss per share | million 782.1 |  |  | 784.3 | 784.3 |  |
| **Weighted average number of ordinary shares for** | | | | | | |
| **the purposes of diluted and diluted headline loss** | | | | | | |
| per share* | million 782.1 |  |  | 784.3 | 784.3 |  |

*  The denominators used are the same as those used for basic and headline loss per share. Shares deemed to be issued for no consideration in respect
of the conditional share plan do not have a dilutive effect in the current period.

--- Section D003 | [AFS] physical page 19 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  |  |  |  |  | 17 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Notes to the condensed consolidated financial statements continued** | | | | | | | | | |
| **for the half year ended 31 March 2026** | | | | | | | | | |
| 5 Loss per share continued |  |  |  |  |  |  |  |  |  |
| **5.2 From continuing and discontinued operations** | | | | | | | | | |
|  |  |  | Continuing operations |  |  | Discontinued operations |  |  |  |
|  | 31 March |  |  | 31 March 30 September |  | 31 March | 31 March 30 September |  |  |
|  | 2026 |  |  | 2025 | 2025 | 2026 | 2025 | 2025 |  |
|  | Units Unaudited |  |  | Unaudited | Audited | Unaudited | Unaudited | Audited |  |
| Basic (loss)/earnings per share | cents (8.1) |  |  | (15.6) | (14.4) | – | 7.4 | (15.9) |  |
| Diluted (loss)/earnings per share | cents (8.1) |  |  | (15.6) | (14.4) | – | 7.4 | (15.9) |  |
| Headline loss per share | cents (8.1) |  |  | (15.6) | (14.4) | – | (1.6) | (25.0) |  |
| Diluted headline loss per share | cents (8.1) |  |  | (15.6) | (14.4) | – | (1.6) | (25.0) |  |
| **The calculation of (loss)/earnings per share is based** | | | | | | | | | |
| **on the following data:** | | | | | | | | | |
| **(Loss)/Earnings for the purposes of basic and diluted** | | | | | | | | | |
| loss per share | Rm (63) |  |  | (122) | (113) | – | 58 | (125) |  |
| Headline earnings adjustments: | Rm |  | – | – | – | – | (71) | (71) |  |
| Profit on disposal of business | Rm |  | – | – | – | – | (100) | (100) |  |
| Tax impact | Rm |  | – | – | – | – | 29 | 29 |  |
| **Loss for the purposes of headline and diluted headline** | | | | | | | | | |
| loss per share | Rm (63) |  |  | (122) | (113) | – | (13) | (196) |  |

The denominators used are the same as those detailed above for both basic and diluted loss per share from continuing and discontinued operations. Shares deemed to be issued
for no consideration in respect of the conditional share plan do not have a dilutive effect in the current period.

--- Section D003 | [AFS] physical page 20 | area selection | Financial note ---
                                                                                  
                                                                                  
                   Condensed consolidated financial statements for the half year ended 31 March 2026 18
                                                                                  
                                                                                  
      Notes to the consolidated financial statements continued                    
      for the half year ended 31 March 2026                                       
                                                                                  
      6    Financial risk management                                              
                                                                                  
      6.1  Credit risk                                                            
           Credit risk is the risk of loss arising from the failure of a client or counterparty to discharge an obligation to the
           group. The primary credit risks that the group are exposed to as at 31 March 2026 relate to the risks associated with
           the purchased book debts, if the books fail to perform in accordance with estimate net future cash flows. Trade
           receivables include receivables from clients that have standard 30-day terms. The clients are diversified across
           numerous industries and geographies and do not result in significant concentration risk. It is not the group’s strategy
           to avoid credit risk, but rather to manage credit risk within the group’s risk appetite and to earn an appropriate
           risk-adjusted return.                                                  
           The group limits its counterparty exposure arising from money market instruments by dealing only with well
           established financial institutions of high credit standing. Deposits are limited to the big five banks within South
           Africa.                                                                
           Credit risk management and measurement                                 
           Each subsidiary is responsible for the identification, measurement, management, control and reporting of credit
           risk within their business units. Exposure to credit losses is managed by collectability of purchased book debts.
           Impairments are monitored and provided for using statistical techniques including experiential and behavioural
           models. These models are based on customers’ financial performance information while on book and assume that
           recent performance is a strong indicator of future performance. In the case of key asset classes, independent models
           are developed to monitor the robustness of the primary models relative to actual performance and to optimise their
           effectiveness. Models are either developed internally or by expert external advisors.
           The group assumes that the credit risk on a financial instrument has not increased significantly if the financial
           instrument is determined to have a low credit risk at the reporting date.
           Measurement of expected credit losses (ECL)                            
           The group measures ECL of a financial instrument in a way that reflects:
           • An unbiased and probability-weighted amount that is determined by evaluating a range of possible outcomes;
           • The time value of money; and                                         
           • Reasonable and supportable information that is available without undue cost or effort at the reporting date about
             past events, current conditions and forecasts of future economic conditions.
           The maximum period considered when measuring ECL is the maximum contractual period (including extension
           options) over which the group is exposed to credit risk, and not a longer period, even if that period is consistent
           with business practice.                                                
           The measurement of ECL is a function of the probability of default (PD), loss given default (LGD) and exposure
           at default (EAD). The assessment of the probability of default and loss given write-offs is based on historical data
           adjusted by forward-looking information as described above.            
           As for the EAD for financial assets, this is represented by the assets’ gross carrying amount at the reporting date
           and other relevant forward-looking information.                        
           For financial assets, the ECL is estimated as the difference between all contractual cash flows that are due to the
           group in accordance with the contract and all the cash flows that the group expects to receive, discounted at
           the original effective interest rate.                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  

--- Section D003 | [AFS] physical page 21 | area selection | Financial note ---
                                                                                  
                                                                                  
                   Condensed consolidated financial statements for the half year ended 31 March 2026 19
                                                                                  
                                                                                  
      Notes to the condensed consolidated financial statements continued          
      for the half year ended 31 March 2026                                       
                                                                                  
      6    Financial risk management                                              
                                       continued                                  
      6.1  Credit risk continued                                                  
           Purchased book debts                                                   
           Investment process                                                     
           Prior to the acquisition of purchased book debts (PBDs), there is a defined investment process that is followed in
           accordance with guidelines determined by a constituted investment committee. PBDs are acquired from various
           credit providers in multiple sectors. Valuations are determined by projecting the present value of anticipated monthly
           collections, net of directly attributable collection costs, using past performance characteristics applicable to similar
           PBDs. Said valuations are ultimately presented to the investment committee to decide upon pricing and bidding
           strategy.                                                              
           Collections process                                                    
           The Insights, Data & Enterprise Analytics (IDEA) team continually develops and recalibrates insights and analytics
           used by operations to optimise the collection processes, and infrastructure, associated with non-performing debt
           collected.                                                             
           Method of provisioning and fair valuing                                
           PBDs are classified as purchased credit-impaired (POCI) financial assets (stage 3) on initial recognition based on the
           presumption that events that have a detrimental impact on the estimated future cash flows of these financial assets
           have occurred before acquisition and initial recognition. The classification of PBDs does not change subsequent
           to initial recognition, even in the unlikely event of the expected cash flows associated thereto returning to full
           contractual terms.                                                     
           Any changes in lifetime expected credit losses (ECLs) are recognised in profit or loss. The group recognises
           favourable changes in lifetime ECLs as an impairment gain, even if lifetime ECLs are less than the amount of ECLs
           that were included in the estimated cash flows on initial recognition. 
           Nutun utilises statistical techniques and models to value PBDs on a monthly basis. Each PBD is modelled based on
           the collection activity applied to it. A combination of inflows applicable to each PBD and the direct, activity-based,
           cost projections applicable thereto are used to determine a net cash flow over a rolling 12-month period, which is
           subsequently discounted to present value using a credit-adjusted effective interest rate to determine its amortised
           cost value. The weighted average credit-adjusted effective interest rate at period end is 19.2% (31 March 2025: 17.9%;
           30 September 2025: 18.4%).                                             
           Other financial assets, recognised within the purchase book debts, include a receivables balance measured at fair
           value. The valuation technique applicable thereto calculates the present value of all future cash flows associated
           thereto net of all associated costs.                                   
           Carrying value of purchased book debts                                 
           The Nutun South Africa business model continues to gain relevance as slow economic growth drive up indebtedness
           and impair consumers’ ability to service their debt, leaving consumer facing entities with significantly larger
           non-performing loans (NPL) portfolios to manage. These impairment model parameters have been applied in
           determining expected cash shortfalls arising from non-payment in the best estimate provision on the loan book as
           at 31 March 2026. These books are not subsequently managed based on the credit risk rating but rather on a cash
           collection basis.

### [ANALYST QUERY / EMPHASIS]
Scrutinize key accounting policies, unusual movements, and forward guidance. This is one capture, not proof of whole-report coverage. Adjacent tables/footnotes may need verification.

### [SECTION READING RESPONSE / DETERMINATION]
> APPLICATION QUALIFICATION: DeepSeek ledger updates failed evidence validation. No existing question was resolved by this response. All prior questions remain open; any resolution claim in the narrative is unverified. Only valid new questions were retained.

### 1. Answers to Stored Questions for This Section

**Q-3df04995ff2f4c6a [high] [partial] — Extract headline financial metrics and confirm page offset**
- **Status**: `Partially resolved (remainder stays open for D003)`
- **Answer & evidence**: Page offset re-confirmed: printed footer "14" on physical p. 16, "15" on p. 17, "16" on p. 18, "17" on p. 19, "18" on p. 20, "19" on p. 21 → printed = physical − 2. No headline advances/CLR/NIM/HEPS/DPS in this capture. However, EPS data captured: basic and diluted LPS (8.1)c H1 2026 vs (8.2)c H1 2025 vs (30.3)c FY2025; headline LPS (8.1)c vs (17.2)c vs (39.4)c [D003, physical PDF p. 18]. Continuing-ops basic LPS (8.1)c vs (15.6)c vs (14.4)c; discontinued-ops basic EPS nil vs 7.4c vs (15.9)c [D003, physical PDF p. 19]. DPS: no dividend declared in this capture (nil position unchanged). Remainder (advances, CLR, NIM, guidance) open for D003.

**Q-64b704d06ed84c90 [medium] [partial] — Cash flow items: write-offs, recoveries, debt, dividends**
- **Status**: `Partially resolved (remainder stays open for D003)`
- **Answer & evidence**: No write-offs, bad debt recoveries, debt raised/repaid, or dividends in this capture. Only capital flow: treasury shares bought 3,662,209 shares for R3.7m (avg R1/share) for Conditional Share Plan vesting [D003, physical PDF p. 16]. Remainder open for D003.

**Q-336536b6077249e3 [medium] [partial] — IFRS 9 ECL staging, SICR, write-off policy, covenants**
- **Status**: `Partially resolved (remainder stays open for D003)`
- **Answer & evidence**: Partial policy capture at [D003, physical PDF pp. 20–21]: (i) SICR low-credit-risk presumption stated — "credit risk … has not increased significantly if the financial instrument is determined to have a low credit risk at the reporting date" (no DPD threshold disclosed); (ii) ECL measured PD × LGD × EAD, discounted at original EIR, max contractual period incl. extension options; (iii) PBDs classified POCI/Stage 3 on initial recognition and **classification does not change subsequently even if cash flows return to full contractual terms**; (iv) favourable lifetime ECL changes recognised as impairment gain even if below initial-recognition ECL; (v) PBD valuation: rolling 12-month net cash flow discounted at credit-adjusted EIR, weighted average 19.2% (31 Mar 2025: 17.9%; 30 Sep 2025: 18.4%). No write-off triggers, no DPD staging table, no covenant terms in this capture. Remainder open for D003.

**Q-007f8f020e154296 [high] [open] — Statement of financial position / income statement values**
- **Status**: `Partially resolved (remainder stays open for D003)`
- **Answer & evidence**: No balance-sheet or income-statement lines in this capture. Revenue note captured instead: total revenue R711m H1 2026 vs R745m H1 2025 vs R1,435m FY2025; SA R159m vs R188m vs R341m; International R552m vs R557m vs R1,094m [D003, physical PDF p. 17]. Advances, ECL allowance, stage split, NII, NIR, opex, impairment line remain open.

**Q-59b88716280048c3 [high] [open] — Revenue disaggregation note**
- **Status**: `Resolved`
- **Answer & evidence**: [D003, physical PDF p. 17] Revenue by geography: South Africa R159m (H1 2025: R188m; FY2025: R341m); Australia R27m (R74m; R127m); United Kingdom R303m (R259m; R525m); United States R212m (R224m; R428m); Other R10m (nil; R14m); Total R711m (R745m; R1,435m). By type: service fees over time R552m (R557m; R1,094m); commissions and fees at a point in time R159m (R188m; R341m). Note: SA revenue is entirely point-in-time commissions/fees; International entirely over-time service fees. Australia down 64% YoY (R74m→R27m) — flag for forecast.

**Q-ebf661d7f2e740cd [high] [open] — EPS note: weighted average shares, dilution, CSP**
- **Status**: `Resolved`
- **Answer & evidence**: [D003, physical PDF pp. 16, 18] Shares in issue 784,313,242; treasury 3,662,209 (bought at avg R1, R3.7m); shares outstanding 780,651,033. Weighted average for basic/headline: 782.1m (effect of treasury (2.2)m). Diluted denominator identical at 782.1m — CSP shares deemed issued for no consideration have **no dilutive effect** in the current period (loss-making). Dilution will re-emerge on return to profit — forecast note.

**Q-019095eae85848d1 [high] [open] — Tax note: R29m credit on loss, DTA R173m**
- **Status**: `Partially resolved (remainder stays open for D003)`
- **Answer & evidence**: Only the tax impact of headline adjustments visible: R29m credit relating to profit on disposal of business (H1 2025 and FY2025) [D003, physical PDF pp. 18–19]. No current/deferred tax split or DTA recognition basis in this capture. Remainder open.

**Q-0b9b00a6c7da4496 [medium] [open] — Operating cost note breakdown**
- **Status**: `Partially resolved (remainder stays open for D003)`
- **Answer & evidence**: No opex breakdown in this capture. Indirect evidence: PBD collection costs are "direct, activity-based" and netted in PBD cash-flow valuation [D003, physical PDF p. 21] — i.e. collection cost sits inside PBD amortisation/impairment, not opex. Remainder open.

**Q-47cc084806ec463d [low] [open] — Physical p. 38 nature**
- **Status**: `Open — carried forward to D004`
- **Answer & evidence**: Not in this capture.

**Q-3df04995ff2f4c6a remainder, Q-64b704d06ed84c90 remainder, Q-336536b6077249e3 remainder, Q-007f8f020e154296 remainder, Q-019095eae85848d1 remainder, Q-0b9b00a6c7da4496 remainder** — carried forward.

*(All other stored questions relate to sections/notes not present in this capture — carried forward unchanged in Section 4.)*

### 2. Footnote & Qualification Deep-Dive

- **Revenue comparative footnote (×2, pp. 17):** "*This disclosure was presented for the first time in the annual financial statements for the year ended 30 September 2025 … Comparative disclosure for 31 March 2025 has been presented for the first time.*" Implication: the H1 2025 geographic/type split is a **first-time restated presentation**, not originally reported — comparatives may have been re-mapped. Verify in D003 later pages whether any reclassification note quantifies the remapping; forecast base should use FY2025 audited split (SA R341m / Intl R1,094m) as the anchor.
- **Share capital footnote (*, p. 16):** "*Net of share issue costs.*" Share capital R5,410m (H1 2026) vs R5,414m — the R4m reduction equals the treasury share purchase (R3.7m rounded), not an issue-cost adjustment. Minor; no forecast impact beyond equity.
- **EPS footnote (p. 18):** "*The denominators used are the same as those used for basic and headline loss per share. Shares deemed to be issued for no consideration in respect of the conditional share plan do not have a dilutive effect in the current period.*" Implication: **anti-dilution while loss-making**; on a return to profit, diluted share count will step up by the CSP overhang (unquantified here — verify CSP note for number of conditional shares outstanding). Forecast: model dilution only in profitable periods.
- **POCI classification statement (p. 21):** "*PBDs are classified as purchased credit-impaired (POCI) financial assets (stage 3) on initial recognition … The classification of PBDs does not change subsequent to initial recognition, even in the unlikely event of the expected cash flows associated thereto returning to full contractual terms.*" Implication: **no Stage 1/Stage 2 migration exists for the core lending book** — the entire PBD book sits in Stage 3 permanently. This structurally suppresses apparent "stage migration" risk but means **all PBD ECL volatility flows straight through P&L as impairment gain/loss** with no staging buffer. Coverage ratio analysis must be done on a POCI basis (allowance vs gross PBD), not IFRS 9 three-stage.
- **Favourable ECL recognition policy (p. 21):** "*The group recognises favourable changes in lifetime ECLs as an impairment gain, even if lifetime ECLs are less than the amount of ECLs that were included in the estimated cash flows on initial recognition.*" Implication: **upward re-estimates of collections are booked as income immediately** — a potential earnings-smoothing lever. The R167m impairment loss decomposition (gross charge vs favourable re-estimate gain) is the key test — carried forward.
- **Credit-adjusted EIR (p. 21):** weighted average **19.2%** (31 Mar 2025: 17.9%; 30 Sep 2025: 18.4%) — a **+130bp YoY rise** in the discount rate. Higher discount rate lowers PV of future collections → mechanically increases ECL/amortisation charge. Verify whether the rate rise reflects higher-risk acquired vintages (mix) or methodology change; either way it is a headwind to PBD carrying value and a tailwind to reported impairment.
- **SICR low-credit-risk presumption (p. 20):** no quantitative DPD threshold disclosed; "low credit risk" presumption used to avoid SICR. For PBDs this is moot (POCI), but for **trade receivables** (30-day terms) it means no explicit 30-DPD SICR trigger is disclosed — verify simplified-approach provision matrix in later notes.
- **Model assumption qualification (p. 20):** "*These models are based on customers' financial performance information while on book and assume that recent performance is a strong indicator of future performance.*" Implication: **backward-looking model bias** — in a deteriorating consumer credit environment (management itself cites "slow economic growth drive up indebtedness"), recent-performance extrapolation may understate forward loss. Forecast: apply conservatism overlay to management PBD cash-flow estimates.
- **No footnote markers with missing definitions** were found in this capture — all asterisks/asterisks have visible definitions.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| N1 | High | D003 (pp. 22–37) | PBD weighted average credit-adjusted EIR rose to 19.2% from 17.9% (Mar-25) and 18.4% (Sep-25) `[D003, p. 21]` | Locate PBD note: EIR by vintage/cohort, whether rise is mix (newer riskier acquisitions) or methodology change; reconcile to PBD amortisation R597m | Higher EIR mechanically raises ECL/amortisation charge; determines whether R597m run-rate is structural or one-off |
| N2 | High | D003 (pp. 22–37) | POCI/Stage 3 permanent classification; no stage migration `[D003, p. 21]` | Locate PBD carrying value table: gross PBD, cumulative ECL allowance, POCI coverage %, comparatives 31 Mar 2025 / 30 Sep 2025 | Coverage ratio is the only credit-quality metric available for the core book; underpins CLR forecast |
| N3 | High | D003 (pp. 22–37) | Favourable ECL re-estimates booked as impairment gain even below initial ECL `[D003, p. 21]` | Locate impairment note: split R167m net impairment into gross ECL charge vs favourable re-estimate gain; compare H1 2025 R173m and FY2025 R199m on same basis | Determines recurring vs one-off CLR; tests earnings-smoothing risk |
| N3b | High | D003 (pp. 22–37) | PBD valuation uses rolling 12-month net cash flow `[D003, p. 21]` | Confirm whether ERC R8,366m (D002) is consistent with a 12-month rolling valuation horizon or a longer run-off; reconcile ERC to PBD carrying value | If ERC >> 12-month PV, carrying value may not capture full ERC; forecast collection runway |
| N4 | High | D003 (pp. 22–37) | Australia revenue −64% YoY (R74m→R27m) `[D003, p. 17]` | Locate segment/geographic commentary or subsequent-events note explaining Australia decline (contract loss, exit, FX) | Determines whether International revenue base is stable; R47m half-year revenue loss annualises to ~R94m |
| N5 | Medium | D003 (pp. 22–37) | UK revenue +17% YoY (R259m→R303m) offsets SA/Australia decline `[D003, p. 17]` | Verify UK revenue driver (new client, DTI incentive, FX) and sustainability in segment/related notes | Concentration and sustainability of the only growing region |
| N6 | Medium | D003 (pp. 22–37) | First-time comparative presentation of revenue split `[D003, p. 17]` | Check for reclassification note quantifying any remapping of H1 2025 revenue between SA/International or service/commission | Comparability of YoY growth rates |
| N3c | Medium | D003 (pp. 22–37) | CSP anti-dilution footnote `[D003, p. 18]` | Locate CSP note: number of conditional shares outstanding, vesting conditions, IFRS 2 charge | Quantify dilution overhang and share-based cost for forecast |
| N4b | Medium | D003 (pp. 22–37) | Trade receivables "standard 30-day terms … no significant concentration" `[D003, p. 20]` | Locate trade receivables note: gross balance, loss allowance, simplified provision matrix, DPD aging, top-client concentration | Tests the "no concentration" assertion; receivables ECL is a separate credit exposure to PBD |
| N5b | Medium | D003 (pp. 22–37) | Deposits "limited to the big five banks" `[D003, p. 20]` | Locate cash/deposits note: counterparty concentration, any unrated exposure | Liquidity/counterparty risk for forecast |
| N6b | Medium | D003 (pp. 22–37) | No DPD-based SICR threshold disclosed `[D003, p. 20]` | Locate accounting policy note: confirm whether 30-DPD rebuttable presumption applied to trade receivables or simplified approach used | Determines provisioning lag risk on non-PBD exposures |
| N7 | Low | D003 (pp. 22–37) | Share capital R5,410m vs R5,414m; treasury R3.7m `[D003, p. 16]` | Confirm no other equity movements (share-based payment reserve, NCI) in statement of changes in equity | Equity roll-forward for NAV forecast |

### 5. Baseline Forecast Inputs Captured Here

| Metric | H1 FY2026 (31 Mar 2026) | H1 FY2025 (31 Mar 2025) | FY2025 (30 Sep 2025) | Source |
|---|---|---|---|---|
| Revenue — Total | R711m | R745m | R1,435m | D003 p.17 |
| Revenue — South Africa | R159m | R188m | R341m | D003 p.17 |
| Revenue — International | R552m | R557m | R1,094m | D003 p.17 |
| Revenue — Australia | R27m | R74m | R127m | D003 p.17 |
| Revenue — UK | R303m | R259m | R525m | D003 p.17 |
| Revenue — US | R212m | R224m | R428m | D003 p.17 |
| Revenue — Other | R10m | nil | R14m | D003 p.17 |
| Service fees (over time) | R552m | R557m | R1,094m | D003 p.17 |
| Commissions & fees (point in time) | R159m | R188m | R341m | D003 p.17 |
| Basic/diluted LPS (total ops) | (8.1)c | (8.2)c | (30.3)c | D003 p.18 |
| Headline LPS (total ops) | (8.1)c | (17.2)c | (39.4)c | D003 p.18 |
| Basic LPS — continuing ops | (8.1)c | (15.6)c | (14.4)c | D003 p.19 |
| Basic EPS — discontinued ops | nil | 7.4c | (15.9)c | D003 p.19 |
| Loss for EPS (total ops) | R(63)m | R(64)m | R(238)m | D003 p.18 |
| Headline loss (total ops) | R(63)m | R(135)m | R(309)m | D003 p.18 |
| Loss — continuing ops | R(63)m | R(122)m | R(113)m | D003 p.19 |
| Earnings — discontinued ops | nil | R58m | R(125)m | D003 p.19 |
| Shares in issue | 784,313,242 | 784,313,242 | 784,313,242 | D003 p.16 |
| Treasury shares | 3,662,209 | nil | nil | D003 p.16 |
| Shares outstanding | 780,651,033 | 784,313,242 | 784,313,242 | D003 p.16 |
| Weighted avg shares (basic/diluted) | 782.1m | 784.3m | 784.3m | D003 p.18 |
| Share capital (net of issue costs) | R5,410m | R5,414m | R5,414m | D003 p.16 |
| Treasury share purchase | R3.7m (avg R1/share) | — | — | D003 p.16 |
| PBD weighted avg credit-adjusted EIR | 19.2% | 17.9% | 18.4% | D003 p.21 |
| PBD ECL methodology | POCI / Stage 3 permanent; rolling 12-month net cash flow PV | same | same | D003 p.21 |
| Dividend per share | nil | nil | nil | D003 pp.16–19 |

### 6. Next Section to Capture

**`D003` (physical pp. 22–27)** — the continuation of the notes to the condensed consolidated financial statements. This is the highest-value next capture because it should contain the **PBD carrying value / impairment note** (resolving N1, N2, N3), the **segment note** (resolving N4, N5), and the **trade receivables note** (resolving N8, N9). It will also likely contain the **borrowings/funding note** (carrying forward the high-priority covenant and maturity-wall questions from D002) and the **tax note** (resolving Q-019095eae85848d1 remainder).

================================================================================
## SECTION 6: [D003] Primary financial statements (part 3/5, p.22-27)
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section D003 | [AFS] physical page 22 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  |  |  | 20 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Notes to the condensed consolidated financial statements continued** | | | | | | | |
| **for the half year ended 31 March 2026** | | | | | | | |
| **6  Financial risk management continued** | | | | | | | |
| 6.1 Credit risk continued |  |  |  |  |  |  |  |
| **Financial assets subject to risk** | | | | | | | |
|  | Other Trade Principal |  |  |  | Other |  |  |
|  | loans and other book |  |  |  | financial |  |  |
|  | receivable receivables* portfolio |  |  |  | assets | Total |  |
|  | Rm Rm Rm |  |  |  | Rm | Rm |  |
| **31 March 2026 – Unaudited** | | | | | | | |
| Gross carrying value | 5 395 3 414 |  |  |  | 644 | 4 458 |  |
| Impairment (loss)/gain | – (5) 431 |  |  |  | – | 426 |  |
| **Non-performing trade and** | | | | | | | |
| other receivables | – (5) – |  |  |  | – | (5) |  |
| **Purchased credit-impaired** | | | | | | | |
| financial assets | – – 431 |  |  |  | – | 431 |  |
| Carrying value of financial assets | 5 390 3 845 |  |  |  | 644 | 4 884 |  |
| ***  Prepayments, VAT receivables and deposits are not financial assets and therefore have been excluded from trade and other receivables.** | | | | | | | |
|  | Other Trade Principal |  |  |  | Other |  |  |
|  | loans and other book |  |  |  | financial |  |  |
|  | receivable receivables* portfolio** |  |  |  | assets*** | Total |  |
|  | Rm Rm Rm |  |  |  | Rm | Rm |  |
| **31 March 2025 – Unaudited** | | | | | | | |
| Gross carrying value | 2 510 3 066 |  |  |  | 663 | 4 241 |  |
| Impairment (loss)/gain | – (6) 624 |  |  |  | – | 618 |  |
| **Non-performing trade and** | | | | | | | |
| other receivables | – (6) – |  |  |  | – | (6) |  |
| **Purchased credit-impaired** | | | | | | | |
| financial assets | – – 624 |  |  |  | – | 624 |  |
| Carrying value of financial assets | 2 504 3 690 |  |  |  | 663 | 4 859 |  |
| *** Prepayments, VAT receivables and deposits are not financial assets and therefore have been excluded from trade and other receivables.** | | | | | | | |
| **** The comparative disclosure has been represented to show the split between the gross carrying value and impairment for the principal book portfolio.** | | | | | | | |
| ***** The other financial assets have been represented to be shown separately from the principal book portfolio.** | | | | | | | |
|  | Other Trade Principal |  |  |  | Other |  |  |
|  | loans and other book |  |  |  | financial |  |  |
|  | receivable receivables* portfolio |  |  |  | assets | Total |  |
|  | Rm Rm Rm |  |  |  | Rm | Rm |  |
| **30 September 2025 – Audited** | | | | | | | |
| Gross carrying value | 4 388 3 377 |  |  |  | 702 | 4 471 |  |
| Impairment (loss)/gain | – (10) 598 |  |  |  | – | 588 |  |
| **Non-performing trade and** | | | | | | | |
| other receivables | – (10) – |  |  |  | – | (10) |  |
| **Purchased credit-impaired** | | | | | | | |
| financial assets | – – 598 |  |  |  | – | 598 |  |
| Carrying value of financial assets | 4 378 3 975 |  |  |  | 702 | 5 059 |  |

* Prepayments, VAT receivables and deposits are not financial assets and therefore have been excluded from trade and other receivables.

--- Section D003 | [AFS] physical page 23 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  | 21 |
| --- | --- | --- | --- | --- | --- |
| **Notes to the condensed consolidated financial statements continued** | | | | | |
| **for the half year ended 31 March 2026** | | | | | |
| **6  Financial risk management continued** | | | | | |
| 6.1 Credit risk continued |  |  |  |  |  |
| **Concentration of principal book portfolios** | | | | | |
|  | 31 March 2026 – Unaudited |  |  |  |  |
|  | Gross Expected |  |  |  |  |
|  | carrying credit loss |  |  | Net carrying |  |
|  | amount allowance |  |  | amount |  |
|  | Rm |  | Rm | Rm |  |
| **Carrying amount of principal book portfolios** | | | | | |
| Banking and specialised lending – unsecured | 2 371 |  | 227 | 2 598 |  |
| Debt review | 951 |  | 141 | 1 092 |  |
| Retail | 46 |  | 51 | 97 |  |
| Banking – secured | 46 |  | 12 | 58 |  |
| Total carrying amount | 3 414 |  | 431 | 3 845 |  |
|  | 31 March 2025 – Unaudited* |  |  |  |  |
|  | Gross Expected |  |  |  |  |
|  | carrying credit loss |  |  | Net carrying |  |
|  | amount allowance |  |  | amount |  |
|  | Rm |  | Rm | Rm |  |
| **Carrying amount of principal book portfolios** | | | | | |
| Banking and specialised lending – unsecured | 2 366 |  | 460 | 2 826 |  |
| Debt review | 605 |  | 65 | 670 |  |
| Retail | 32 |  | 54 | 86 |  |
| Banking – secured | 63 |  | 45 | 108 |  |
| Total carrying amount | 3 066 |  | 624 | 3 690 |  |
| *** This disclosure was presented for the first time in the annual financial statements for the year ended 30 September 2025 in order to enhance the overall** | | | | | |
| **presentation of the financial statements. Comparative disclosure for 31 March 2025 has been presented for the first time.** | | | | | |
|  | 30 September 2025 – Audited |  |  |  |  |
|  | Gross Expected |  |  |  |  |
|  | carrying credit loss |  |  | Net carrying |  |
|  | amount allowance |  |  | amount |  |
|  | Rm |  | Rm | Rm |  |
| **Carrying amount of principal book portfolios** | | | | | |
| Banking and specialised lending – unsecured | 2 482 |  | 468 | 2 950 |  |
| Debt review | 793 |  | 72 | 865 |  |
| Retail | 48 |  | 47 | 95 |  |
| Banking – secured | 54 |  | 11 | 65 |  |
| Total carrying amount | 3 377 |  | 598 | 3 975 |  |

--- Section D003 | [AFS] physical page 24 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  |  |  | 22 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Notes to the condensed consolidated financial statements continued** | | | | | | | |
| **for the half year ended 31 March 2026** | | | | | | | |
| **6  Financial risk management continued** | | | | | | | |
| 6.1 Credit risk continued |  |  |  |  |  |  |  |
| **Reconciliation of expected credit loss allowance on principal book portfolios*** | | | | | | | |
|  | Banking & |  |  |  |  |  |  |
|  | specialised |  |  |  |  |  |  |
|  | lending – Debt |  |  |  | Banking – |  |  |
|  | Unsecured review Retail |  |  |  | Secured | Total |  |
|  | Rm Rm Rm |  |  |  | Rm | Rm |  |
| **Balance at 30 September 2024 –** | | | | | | | |
| Audited | 575 148 30 |  |  |  | 44 | 797 |  |
| **Impairment (loss)/gain on principal** | | | | | | | |
| book portfolios | (115) (83) 24 |  |  |  | 1 | (173) |  |
| **Impairment loss on principal book** | | | | | | | |
| portfolios acquired during the period | (51) (45) - |  |  |  | - | (96) |  |
| **Impairment (loss)/gain on historical** | | | | | | | |
| principal book portfolios | (64) (38) 24 |  |  |  | 1 | (77) |  |
| **Balance at 31 March 2025 -** | | | | | | | |
| Unaudited** | 460 65 54 |  |  |  | 45 | 624 |  |
| **Impairment gain/(loss) on principal** | | | | | | | |
| book portfolios | 8 7 (7) |  |  |  | (34) | (26) |  |
| **Impairment gain on principal book** | | | | | | | |
| portfolios acquired during the period | 66 89 1 |  |  |  | – | 156 |  |
| **Impairment loss on historical principal** | | | | | | | |
| book portfolios | (58) (82) (8) |  |  |  | (34) | (182) |  |
| **Balance at 30 September 2025 –** | | | | | | | |
| Audited | 468 72 47 |  |  |  | 11 | 598 |  |
| **Impairment (loss)/gain on principal** | | | | | | | |
| book portfolios | (241) 69 4 |  |  |  | 1 | (167) |  |
| **Impairment gain on principal book** | | | | | | | |
| portfolios acquired during the period | 1 23 - |  |  |  | - | 24 |  |
| **Impairment (loss)/gain on historical** | | | | | | | |
| principal book portfolios | (242) 46 4 |  |  |  | 1 | (191) |  |
| Balance at 31 March 2026 – Unaudited | 227 141 51 |  |  |  | 12 | 431 |  |

*  This disclosure was presented for the first time in the annual financial statements for the year ended 30 September 2025 in order to enhance the overall
presentation of the financial statements.
** The comparative disclosure for 31 March 2025 has been presented for the first time to show the reconciliation of the expected credit loss allowance
on the principal book portfolios.
The cumulative impairment gain of R431 million relates to elevated performance, above the investment base-case,
predominantly within the Banking & Specialised Lending segment. The reduction in the cumulative impairment gain
in the current year relates to payer drop-offs and reduced settlement activity on historical book portfolios within
the applicable portfolio segments.

--- Section D003 | [AFS] physical page 25 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  |  |  |  | 23 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Notes to the condensed consolidated financial statements continued** | | | | | | | | |
| **for the half year ended 31 March 2026** | | | | | | | | |
| **6  Financial risk management continued** | | | | | | | | |
| 6.1 Credit risk continued |  |  |  |  |  |  |  |  |
| **Expected credit loss allowance on trade receivables*** | | | | | | | | |
|  | Amounts |  |  |  |  |  |  |  |
|  | Amounts Amounts in excess of |  |  |  |  |  |  |  |
|  | 30 days 61 to 90 days |  |  |  |  | 90 days |  |  |
|  | Current overdue overdue |  |  |  |  | overdue | Total |  |
|  | Rm Rm Rm |  |  |  |  | Rm | Rm |  |
| **31 March 2026 – Unaudited** | | | | | | | | |
| Expected loss rate | 0.00% 0.00% 0.00% |  |  |  |  | 100.00% | 1.34% |  |
| Gross carrying amount | 339 25 5 |  |  |  |  | 5 | 374 |  |
| Loss allowance | – – – |  |  |  |  | (5) | (5) |  |
| Net carrying amount | 339 25 5 |  |  |  |  | - | 369 |  |
| **31 March 2025 – Unaudited**** | | | | | | | | |
| Expected loss rate | 0.00% 0.00% 0.00% |  |  |  |  | 85.71% | 1.43% |  |
| Gross carrying amount | 345 61 6 |  |  |  |  | 7 | 419 |  |
| Loss allowance | – – – |  |  |  |  | (6) | (6) |  |
| Net carrying amount | 345 61 6 |  |  |  |  | 1 | 413 |  |
| **30 September 2025 – Audited** | | | | | | | | |
| Expected loss rate | 0.06% 0.19% 6.67% |  |  |  |  | 81.82% | 2.75% |  |
| Gross carrying amount | 286 52 15 |  |  |  |  | 11 | 364 |  |
| Loss allowance | <1 <1 (1) |  |  |  |  | (9) | (10) |  |
| Net carrying amount | 286 52 14 |  |  |  |  | 2 | 354 |  |
| *** The expected credit loss (ECL) on trade receivables is shown per the maturity of trade receivables. No separate classes of trade receivables have been** | | | | | | | | |
| **identified. Receivables originate from contracts with customers across various industries and geographies however credit risk is managed by reference** | | | | | | | | |
| **to past default experience of the debtor and analysis of the debtor's financial position, adjusted for factors that are specific to the debtors, and an** | | | | | | | | |
| **assessment of both the current as well as the forecast direction of conditions at the reporting date. This disclosure was presented for the first time in** | | | | | | | | |
| **the annual financial statements for the year ended 30 September 2025 in order to enhance the overall presentation of the financial statements.** | | | | | | | | |
| **** The comparative disclosure for 31 March 2025 has been presented for the first time to enhance overall disclosure.** | | | | | | | | |
| **6.2 Currency risk** | | | | | | | | |
| **Currency risk is the possibility of incurring a financial loss as a consequence of the depreciation in the measurement** | | | | | | | | |
| **currency relative to a foreign currency prior to payment of a commitment in that foreign currency or the** | | | | | | | | |
| **strengthening of the measurement currency prior to receiving payment in a foreign currency.** | | | | | | | | |
| **The foreign currencies to which the group has material exposure are US Dollar and British Pound. The exposure largely** | | | | | | | | |
| **relates to foreign currency denominated receivables which are realised in 60 days, in line with the credit terms and** | | | | | | | | |
| **are therefore subject to currency fluctuations. Expenses incurred are largely denominated in the functional currency** | | | | | | | | |
| **of the entities to which they relate.** | | | | | | | | |
| **During the current period, Nutun entered into foreign exchange contracts for the purposes of hedging the exposure** | | | | | | | | |
| **to the USD and GBP receipts for the Nutun International segment.** | | | | | | | | |
| **The following significant exchange rates were applied during the period:** | | | | | | | | |
|  | Average rate Reporting date closing rate |  |  |  |  |  |  |  |
| 31 March | 31 March 30 Sept 31 March 31 March |  |  |  |  |  | 30 Sept |  |
|  | 2026 2025 2025 2026 |  |  |  |  | 2025 | 2025 |  |
| Unaudited | Unaudited Audited Unaudited Unaudited |  |  |  |  |  | Audited |  |
|  | Rm Rm Rm Rm |  |  |  |  | Rm | Rm |  |
| US Dollar | 16.8 18.2 18.1 17.2 |  |  |  |  | 18.4 | 17.3 |  |
| Euro | 19.6 19.3 20.0 19.7 |  |  |  |  | 20.0 | 20.3 |  |
| British Pound | 22.4 23.1 23.6 22.7 |  |  |  |  | 23.9 | 23.2 |  |
| Australian Dollar | 11.3 11.6 11.6 11.8 |  |  |  |  | 11.6 | 11.4 |  |

--- Section D003 | [AFS] physical page 26 | area selection | Financial note ---
                                                                                  
                                                                                  
                   Condensed consolidated financial statements for the half year ended 31 March 2026 24
                                                                                  
                                                                                  
      Notes to the condensed consolidated financial statements continued          
      for the half year ended 31 March 2026                                       
                                                                                  
      6    Financial risk management                                              
                                       continued                                  
      6.2  Currency risk continued                                                
           The carrying amounts of the group’s foreign currency denominated monetary assets and monetary liabilities at the
           end of the reporting period are as follows:                            
                                    Liabilities              Assets*              
                            31 March 31 March 30 Sept 31 March 31 March 30 Sept   
                               2026    2025    2025    2026     2025    2025      
                            Unaudited Unaudited Audited Unaudited Unaudited Audited
                                Rm      Rm      Rm      Rm       Rm      Rm       
           Foreign amounts                                                        
           included in the financial                                              
           statements at the end of                                               
           the period:                                                            
           US Dollar            10       5       1      120      98     135       
           Euro                  –       –       –        3       2       3       
           British Pound         2      16       1      111      84      78       
           Australian Dollar     –       –       –        –       6       1       
           * Assets held in foreign currency relate to receivables of R207 million (31 March 2025: R171 million; 30 September 2025: R190 million) and bank balances
             of R27 million (31 March 2025: R19 million; 30 September 2025: R27 million).
      6.3  Fair value disclosure                                                  
           Fair values of financial instruments carried at amortised cost         
           The fair value of a financial instrument is the price that would be received to sell an asset or paid to transfer a liability
           between market participants at the measurement date.                   
           The best evidence of the fair value of a financial instrument at initial recognition is the transaction price (i.e. the fair
           value of the consideration given or received) unless the fair value of that instrument is evidenced by comparison with
           other observable current market transactions in the same instrument (i.e. without modification or repackaging) or
           based on a valuation technique whose variables include only data from observable markets.
           The method of determining the fair value of financial instruments is analysed into the following categories:
           Level 1 Unadjusted quoted prices in active markets where the quoted price is readily available and the price
                represents actual and regularly occurring market transactions on an arm’s length basis.
           Level 2 Valuation techniques using market observable inputs, including:
                • Using recent arm’s length market transactions;                  
                • Reference to the current fair value of similar instruments; and 
                • Discounted cash flow analysis, pricing models or other techniques commonly used by market
                  participants                                                    
           Level 3 Valuation techniques, as described for level 2 above, for which not all inputs are market observable prices
                or rates. Such a financial instrument is initially recognised at the transaction price, which is the best
                indicator of fair value, although the value obtained from the relevant valuation model may differ. The
                difference between the transaction price and the model value, commonly referred to as “day one profit
                or loss’, is either amortised over the life of the transaction, deferred until the instrument’s fair value can
                be determined using market observable inputs, or realised through settlement.
           The valuation techniques in level 2 and level 3 use inputs such as interest rate yield curves, equity prices and currency
           prices/yields, volatilities, and the correlation between inputs. The models used in these valuation techniques are
           calibrated against industry standards, economic models and against transaction process, where applicable.
           Valuation methods and assumptions:                                     
           Principal book portfolios are held at amortised cost. The balance at the end of the period is calculated based on
           the expected future cash flows which are adjusted for risk as it takes historical cash flows into account to predict
           forecasted cash flows. The fair value of principal book portfolios is determined by adjusting the discount rate from
           the credit-adjusted effective interest rate to a current market related discount rate of 18.50% (31 March 2025: 15.81%;
           30 September 2025: 15.93%) and adjusting the expected cash flows for risk. The fair values determined on this basis
           approximates the carrying value.                                       
           The fair value of interest-bearing liabilities is calculated based on future cash flows, discounted using a forward rate
           curve plus a valuation margin. The valuation margin is a consensus margin at which deals with similar remaining cash
           profiles could be secured in the market at the valuation date.         
           The carrying value of trade and other receivables, other investments, cash and cash equivalents, trade and other
           payables and bank overdrafts approximates fair value as they are short-term in nature and not subject to material
           changes in credit risk and fair value.                                 

--- Section D003 | [AFS] physical page 27 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  |  |  | 25 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Notes to the condensed consolidated financial statements continued** | | | | | | | |
| **for the half year ended 31 March 2026** | | | | | | | |
| **6  Financial risk management continued** | | | | | | | |
| **6.3 Fair value disclosure continued** | | | | | | | |
| **The following represents the fair values of financial instruments not carried at fair value on the statement of financial** | | | | | | | |
| **position, but for which fair value is required to be disclosed. For all other financial instruments, the carrying value is** | | | | | | | |
| **equal to or a reasonable approximation of the fair value.** | | | | | | | |
|  | Carrying Total |  |  |  |  |  |  |
|  | value fair value Level 1 |  |  |  | Level 2 | Level 3 |  |
|  | Rm Rm Rm |  |  |  | Rm | Rm |  |
| **31 March 2026 – Unaudited** | | | | | | | |
| Assets |  |  |  |  |  |  |  |
| Principal book portfolio | 3 845 3 845 – |  |  |  | – | 3 845 |  |
| Financial assets at amortised cost | 3 845 3 845 – |  |  |  | – | 3 845 |  |
| Liabilities |  |  |  |  |  |  |  |
| Interest-bearing liabilities | 3 743 3 769 – |  |  |  | – | 3 769 |  |
| Fixed rate liabilities | – – – |  |  |  | – | – |  |
| Floating rate liabilities | 3 743 3 769 – |  |  |  | – | 3 769 |  |
| Financial liabilities at amortised cost | 3 743 3 769 – |  |  |  | – | 3 769 |  |
| **31 March 2025 - Unaudited** | | | | | | | |
| Assets |  |  |  |  |  |  |  |
| Principal book portfolio | 3 690 3 690 – |  |  |  | – | 3 690 |  |
| Financial assets at amortised cost | 3 690 3 690 – |  |  |  | – | 3 690 |  |
| Liabilities |  |  |  |  |  |  |  |
| Interest-bearing liabilities | 3 407 3 428 – |  |  |  | – | 3 428 |  |
| Fixed rate liabilities | – – – |  |  |  | – | – |  |
| Floating rate liabilities | 3 407 3 428 – |  |  |  | – | 3 428 |  |
| Financial liabilities at amortised cost | 3 407 3 428 – |  |  |  | – | 3 428 |  |
| **30 September 2025 – Audited** | | | | | | | |
| Assets |  |  |  |  |  |  |  |
| Principal book portfolio | 3 975 3 975 – |  |  |  | – | 3 975 |  |
| Financial assets at amortised cost | 3 975 3 975 – |  |  |  | – | 3 975 |  |
| Liabilities |  |  |  |  |  |  |  |
| Interest-bearing liabilities | 3 807 3 468 – |  |  |  | – | 3 468 |  |
| Fixed rate liabilities | – – – |  |  |  | – | – |  |
| Floating rate liabilities | 3 807 3 468 – |  |  |  | – | 3 468 |  |
| Financial liabilities at amortised cost | 3 807 3 468 – |  |  |  | – | 3 468 |  |

### [ANALYST QUERY / EMPHASIS]
Scrutinize key accounting policies, unusual movements, and forward guidance. This is one capture, not proof of whole-report coverage. Adjacent tables/footnotes may need verification.

### [SECTION READING RESPONSE / DETERMINATION]
> APPLICATION QUALIFICATION: DeepSeek ledger updates failed evidence validation. No existing question was resolved by this response. All prior questions remain open; any resolution claim in the narrative is unverified. Only valid new questions were retained.

### 1. Answers to Stored Questions for This Section

**Q-D003-01 (from Q-d9efef… / PCD carrying value):** Locate the ECL/impairment note for purchased book debts: capture gross carrying amount, cumulative ECL allowance, Stage 1/2/3 (or purchased-credit-impaired) split, and coverage ratios for 31 Mar 2026 vs 31 Mar 2025 vs 30 Sep 2025.
- **Status**: `Partially resolved (remainder stays open for D003 later pages / D004)`
- **Answer & evidence**: Gross principal book portfolio R3,414m; cumulative ECL allowance R431m; net carrying R3,845m at 31 Mar 2026 [D003, physical PDF p. 22]. Comparatives: 31 Mar 2025 gross R3,066m / allowance R624m / net R3,690m; 30 Sep 2025 gross R3,377m / allowance R598m / net R3,975m [D003, physical PDF p. 22]. Implied total coverage: 12.6% (31 Mar 2026), 20.4% (31 Mar 2025), 17.7% (30 Sep 2025) — coverage has fallen sharply YoY. **No Stage 1/2/3 split is presented** — the entire allowance is labelled "Purchased credit-impaired financial assets" (POCI), so IFRS 9 staging is not disclosed here. Remainder (stage split, SICR) stays open.

**Q-D003-02 (from Q-48250b… / impairment decomposition):** Decompose the R167m impairment loss into gross ECL charge vs favourable ECL re-estimate gain; restate H1 2025 R173m and FY2025 R199m on same basis.
- **Status**: `Resolved`
- **Answer & evidence**: H1 2026 net impairment loss R167m = impairment gain on portfolios acquired during the period R24m + impairment loss on historical portfolios R191m [D003, physical PDF p. 24]. H1 2025 net R173m = acquired R96m loss + historical R77m loss. FY2025 (full year) net R26m = acquired R156m gain + historical R182m loss. Note the sign convention: "acquired during the period" lines are gains in H1 2026 and FY2025 but losses in H1 2025 — a swing of R252m between H1 2025 and H1 2026 on acquisition-day ECL. Historical-book losses are running at R191m (H1 2026) vs R77m (H1 2025) vs R182m (FY2025) — i.e. H1 2026 historical-book deterioration already exceeds the full FY2025 figure.

**Q-D003-03 (from Q-3df0… / headline metrics & page offset):** Extract headline metrics and confirm printed-vs-physical page offset.
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: Page offset confirmed: printed footer "20" on physical p. 22, "21" on p. 23, "22" on p. 24, "23" on p. 25, "24" on p. 26, "25" on p. 27 → printed = physical − 2. No HEPS/DPS/NIM/CLR headline in this capture; those remain open for D002/D003 earlier pages.

**Q-D003-04 (from Q-3df0… / statement of financial position & income statement):** Capture gross vs net advances, total ECL allowance, Stage 1/2/3 split, NII, NIR, opex, impairment line.
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: Gross principal book R3,414m, ECL allowance R431m, net R3,845m [D003, p. 22]. Impairment line R167m net loss [D003, p. 24]. NII/NIR/opex not in this capture — remain open.

**Q-D003-05 (from Q-3df0… / cash flow write-offs, recoveries, debt, dividends):** 
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: No cash-flow statement in this capture. However, interest-bearing liabilities carrying value R3,743m (31 Mar 2026) vs R3,407m (31 Mar 2025) vs R3,807m (30 Sep 2025) [D003, p. 27] — debt has risen R336m YoY but fallen R64m since year-end. Write-offs/recoveries/dividends remain open.

**Q-D003-06 (from Q-3df0… / IFRS 9 ECL staging, SICR, macro overlay, write-off policy, covenants):**
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: No IFRS 9 staging table, SICR DPD threshold, macro scenario weighting, write-off trigger, or covenant term is disclosed in this capture. The principal book is treated as **purchased credit-impaired (POCI)** with a single cumulative allowance, not staged. Trade receivables use a simplified maturity-bucket matrix (see §2). SICR/macro/write-off/covenant remain open for later D003 pages.

**Q-D003-07 (from Q-3df0… / trade receivables note — gross, allowance, matrix, DPD, concentration):**
- **Status**: `Resolved`
- **Answer & evidence**: Trade receivables gross R374m, loss allowance R5m, net R369m at 31 Mar 2026 (vs R419m/R6m/R413m at 31 Mar 2025; R364m/R10m/R354m at 30 Sep 2025) [D003, p. 25]. Buckets: Current R339m (0.00% ELR), 30+ days R25m (0.00%), 61–90 days R5m (0.00%), 90+ days R5m (100% ELR). Total ELR 1.34% (vs 1.43% Mar 2025, 2.75% Sep 2025). **No client concentration % disclosed** — assertion of diversification not evidenced here; concentration remains open.

**Q-D003-08 (from Q-3df0… / trade receivables provisioning approach — simplified matrix, 30-DPD rebuttable presumption):**
- **Status**: `Resolved`
- **Answer & evidence**: Footnote confirms ECL on trade receivables is shown "per the maturity of trade receivables. No separate classes of trade receivables have been identified… credit risk is managed by reference to past default experience of the debtor and analysis of the debtor's financial position, adjusted for factors specific to the debtors, and an assessment of both the current as well as the forecast direction of conditions" [D003, p. 25]. This is a simplified maturity-matrix approach. **No 30-DPD rebuttable presumption is stated**; the matrix applies 0% ELR to 30+ and 61–90 day buckets and 100% only at 90+ days — a very late loss-recognition trigger.

**Q-D003-09 (from Q-3df0… / fair value of other financial assets R644m — hierarchy, inputs, sensitivity):**
- **Status**: `Resolved`
- **Answer & evidence**: Other financial assets R644m (31 Mar 2026) vs R663m (31 Mar 2025) vs R702m (30 Sep 2025) [D003, p. 22]. Fair value note [D003, p. 26] describes Level 1/2/3 methodology but **does not assign other financial assets to a level or give inputs/sensitivity** — the fair value table on p. 27 covers only the principal book portfolio and interest-bearing liabilities. Residual: hierarchy level and sensitivity for the R644m remain open.

**Q-D003-10 (from Q-3df0… / interest-rate risk — fixed vs floating, hedge accounting):**
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: All interest-bearing liabilities are **floating rate** — fixed rate liabilities nil at all three dates [D003, p. 27]. Carrying R3,743m vs fair value R3,769m (31 Mar 2026); R3,407m vs R3,428m (31 Mar 2025); R3,807m vs R3,468m (30 Sep 2025 — fair value R339m *below* carrying, a material mark). Hedge accounting and JIBAR/Prime sensitivity not in this capture — remain open.

**Q-D003-11 (from Q-3df0… / PBD weighted-average credit-adjusted EIR 19.2% vs 17.9% vs 18.4%):**
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: The fair value note discloses the **current market-related discount rate** used to fair-value the principal book: **18.50% at 31 Mar 2026 vs 15.81% at 31 Mar 2025 vs 15.93% at 30 Sep 2025** [D003, p. 26] — a +269bp YoY rise in the market discount rate. This is distinct from the credit-adjusted EIR (19.2%) but is a strong corroborating signal that market pricing/risk premium on this asset class has risen sharply. EIR-by-vintage decomposition and reconciliation to PBD amortisation R597m remain open.

**Q-D003-12 (from Q-3df0… / PBD carrying value note — gross, allowance, POCI coverage, reconcile to R3,845m pledged):**
- **Status**: `Resolved`
- **Answer & evidence**: Gross R3,414m, allowance R431m, net R3,845m [D003, p. 22] — **reconciles exactly** to the R3,845m principal book portfolio pledged as security and to the fair value table carrying value R3,845m [D003, p. 27]. Coverage 12.6%.

**Q-D003-13 (from Q-3df0… / Australia revenue decline, UK growth):**
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: No segment revenue commentary in this capture. FX rates captured [D003, p. 25]: GBP average 22.4 (H1 2026) vs 23.1 (H1 2025) — GBP weakened ~3%, so UK revenue growth in ZAR is *understated* by FX, not explained by it. AUD average 11.3 vs 11.6. Drivers remain open.

**Q-D003-14 (from Q-3df0… / reclassification of H1 2025 revenue geographic split):**
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: No revenue reclassification note in this capture. However, **two balance-sheet reclassifications are disclosed**: (i) 31 Mar 2025 comparative "represented to show the split between gross carrying value and impairment for the principal book portfolio" [D003, p. 22]; (ii) "other financial assets have been represented to be shown separately from the principal book portfolio" [D003, p. 22]. Revenue reclassification remains open.

**Q-D003-15 (from Q-3df0… / statement of changes in equity):**
- **Status**: `Open — not in this capture`

**Q-D003-16 (from Q-3df0… / EPS note, weighted average shares, dilution):**
- **Status**: `Open — not in this capture`

**Q-D003-17 (from Q-3df0… / operating cost note breakdown):**
- **Status**: `Open — not in this capture`

**Q-D003-18 (from Q-3df0… / revenue disaggregation, DTI incentives):**
- **Status**: `Open — not in this capture`

**Q-D003-19 (from Q-3df0… / tax note, DTA R173m):**
- **Status**: `Open — not in this capture`

**Q-D003-20 (from Q-3df0… / discontinued operations, held-for-sale):**
- **Status**: `Open — not in this capture`

**Q-D003-21 (from Q-3df0… / associate TC Global Finance):**
- **Status**: `Open — not in this capture`

**Q-D003-22 (from Q-3df0… / fair value gain R30m drivers):**
- **Status**: `Open — not in this capture`

**Q-D003-23 (from Q-3df0… / portfolio acquisition note — purchase price, acquired ERC, contingent consideration):**
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: Acquisition-day ECL recognised in H1 2026 was a **net gain of R24m** (vs a **loss of R96m** in H1 2025 and a **gain of R156m** in FY2025) [D003, p. 24]. This is the only acquisition economics disclosed; purchase price, acquired ERC and contingent consideration remain open.

**Q-D003-24 (from Q-3df0… / ERC methodology, collection curve, actual vs expected):**
- **Status**: `Open — not in this capture`

**Q-D003-25 (from Q-3df0… / funding note — facility sizes, maturities, covenants, headroom):**
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: Interest-bearing liabilities R3,743m carrying / R3,769m fair value, all floating rate [D003, p. 27]. Facility sizes, maturities, covenant ratios and headroom not in this capture — remain open.

**Q-D003-26 (from Q-3df0… / maturity profile, refinancing, going concern):**
- **Status**: `Open — not in this capture`

**Q-D003-27 (from Q-3df0… / audit/review status of primary statements):**
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: Each table is explicitly labelled "Unaudited" (31 Mar 2026, 31 Mar 2025) or "Audited" (30 Sep 2025) [D003, pp. 22–27]. No restatement/error-correction or subsequent-events note in this capture — remain open.

**Q-D003-28 (from Q-3df0… / 'transition of the business', going concern, strategic review):**
- **Status**: `Open — not in this capture`

**Q-D003-29 (from Q-3df0… / Audit & Risk Committee governance, qualifications):**
- **Status**: `Open — not in this capture`

**Q-D003-30 (from Q-3df0… / forward-looking figures flagged as director-prepared):**
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: The fair value note states principal book fair value is "determined by adjusting the discount rate from the credit-adjusted effective interest rate to a current market related discount rate of 18.50%… and adjusting the expected cash flows for risk. The fair values determined on this basis approximates the carrying value" [D003, p. 26] — a director-prepared forward-looking assumption. Sensitivity not disclosed — remains open.

**Q-D003-31 (from Q-3df0… / Mobalyz related party):** `Open — not in this capture`
**Q-D003-32 (from Q-3df0… / DTI incentive income quantification):** `Open — not in this capture`
**Q-D003-33 (from Q-3df0… / TC Global Finance associate carrying value):** `Open — not in this capture`
**Q-D003-34 (from Q-3df0… / client concentration top 5/10):** `Open — not in this capture`
**Q-D003-35 (from Q-3df0… / organic vs acquired PBD collection growth):** `Open — not in this capture`
**Q-D003-36 (from Q-3df0… / group net interest cost R216m vs SA R203m reconciliation):** `Open — not in this capture`
**Q-D003-37 (from Q-3df0… / PBD/RTC amortisation R597m split):** `Open — not in this capture`
**Q-D003-38 (from Q-3df0… / ERC R8,366m methodology):** `Open — not in this capture`
**Q-D003-39 (from Q-3df0… / funding restructuring Note 1 p.6):** `Open — not in this capture`
**Q-D003-40 (from Q-3df0… / ECL/macro note for PBD/RTC or TC Global):** `Partially resolved` — see Q-D003-06; no IFRS 9 staging/macro overlay note exists for the POCI book in this capture.
**Q-D003-41 (from Q-3df0… / physical p. 38 administration):** `Open — not in this capture`

---

### 2. Footnote & Qualification Deep-Dive

**Footnote `*` on p. 22 (trade and other receivables):** "Prepayments, VAT receivables and deposits are not financial assets and therefore have been excluded from trade and other receivables." [D003, p. 22] — This means the R5,395m "Other loans and receivable" gross figure is *financial* receivables only; the balance-sheet trade & other receivables line will be higher by the excluded prepayments/VAT/deposits. **Verification needed:** reconcile R5,395m to the statement of financial position trade & other receivables line and quantify the excluded non-financial amounts.

**Footnote `**` on p. 22 (31 Mar 2025 comparative):** "The comparative disclosure has been represented to show the split between the gross carrying value and impairment for the principal book portfolio." [D003, p. 22] — The 31 Mar 2025 principal book gross R3,066m / allowance R624m split is a **restated presentation**, not as originally reported. **Verification needed:** confirm the originally reported 31 Mar 2025 net carrying value (R3,690m) is unchanged and only the gross/allowance split is new; any change to the net figure would be a prior-period error.

**Footnote `***` on p. 22 (31 Mar 2025 other financial assets):** "The other financial assets have been represented to be shown separately from the principal book portfolio." [D003, p. 22] — Same restatement concern: R663m other financial assets at 31 Mar 2025 is a re-presented figure. **Verification needed:** confirm no reclassification between principal book and other financial assets changed the 31 Mar 2025 net totals.

**Footnote `*` on p. 23 (concentration table):** "This disclosure was presented for the first time in the annual financial statements for the year ended 30 September 2025… Comparative disclosure for 31 March 2025 has been presented for the first time." [D003, p. 23] — The segment split of the principal book (Banking & specialised lending unsecured, Debt review, Retail, Banking secured) is **new disclosure with no long-run history**. Critically, the 31 Mar 2025 comparatives show **Banking & specialised lending unsecured allowance R460m on gross R2,366m (19.4% coverage)** vs **31 Mar 2026 R227m on R2,371m (9.6% coverage)** — coverage halved YoY on a flat gross balance. This is the single largest credit-quality signal in the capture. **Verification needed:** explain the R233m release in unsecured allowance on a flat book — is it genuine performance (as the p. 24 narrative claims) or a model/assumption change?

**Footnote `*` on p. 24 (ECL reconciliation):** "This disclosure was presented for the first time in the annual financial statements for the year ended 30 September 2025… The comparative disclosure for 31 March 2025 has been presented for the first time to show the reconciliation of the expected credit loss allowance on the principal book portfolios." [D003, p. 24] — The ECL roll-forward is **new disclosure**; there is no prior-period roll-forward to test methodology consistency. The roll-forward is also **not a standard IFRS 9 stage-migration reconciliation** — it splits only "acquired during the period" vs "historical", with no Stage 1/2/3, no write-offs, no recoveries, and no FX line. **Verification needed:** locate a full ECL movement note (write-offs, recoveries, transfers) elsewhere in D003; the absence of write-off lines here means gross write-offs cannot be reconciled from this table.

**Narrative qualification on p. 24 (below the table):** "The cumulative impairment gain of R431 million relates to elevated performance, above the investment base-case, predominantly within the Banking & Specialised Lending segment. The reduction in the cumulative impairment gain in the current year relates to payer drop-offs and reduced settlement activity on historical book portfolios within the applicable portfolio segments." [D003, p. 24] — This is the most important qualification in the capture. It confirms:
- The **entire R431m allowance is a "cumulative impairment gain"** — i.e. the book is carried *below* its investment base-case expected cash flows because collections have outperformed. This is a POCI asset where the "allowance" is really an unamortised gain, not a forward-looking credit reserve.
- The **R167m H1 2026 net impairment loss is a reduction of that gain**, driven by "payer drop-offs and reduced settlement activity" — i.e. **actual credit deterioration**, not a provisioning top-up.
- The **Banking & Specialised Lending segment absorbed R241m of the R167m net loss** (its allowance fell from R468m to R227m) [D003, p. 24] — the segment the narrative says drove the original gain is now driving its reversal.
- **Forecast consequence:** the "impairment gain" cushion is being consumed at ~R167m per half; at that run-rate the R431m cumulative gain would be exhausted within ~2.5 halves. Once exhausted, the P&L flips from impairment *gains* to impairment *charges* — a material swing to model.

**Footnote `*` on p. 25 (trade receivables ECL):** "The expected credit loss (ECL) on trade receivables is shown per the maturity of trade receivables. No separate classes of trade receivables have been identified… credit risk is managed by reference to past default experience of the debtor and analysis of the debtor's financial position, adjusted for factors that are specific to the debtors, and an assessment of both the current as well as the forecast direction of conditions at the reporting date. This disclosure was presented for the first time…" [D003, p. 25] — Two issues: (i) the matrix applies **0.00% ELR to Current, 30+ days and 61–90 days** buckets at 31 Mar 2026, with 100% only at 90+ days — loss recognition is deferred to 90 DPD, which is late relative to a 30-DPD SICR norm; (ii) the 30 Sep 2025 audited matrix applied 0.06%/0.19%/6.67% to those buckets, so the **current-period matrix has been relaxed to zero** on the same buckets. **Verification needed:** confirm whether the zero ELR on 30+ and 61–90 day buckets is a methodology change or reflects genuinely zero historical loss experience in those buckets.

**Footnote `**` on p. 25 (31 Mar 2025 trade receivables comparative):** "The comparative disclosure for 31 March 2025 has been presented for the first time to enhance overall disclosure." [D003, p. 25] — No prior-period matrix to test consistency; the 85.71% ELR at 90+ days (31 Mar 2025) vs 100% (31 Mar 2026) vs 81.82% (30 Sep 2025) shows the 90+ ELR is being **raised over time**, consistent with a late-recognition matrix.

**Footnote `*` on p. 26 (foreign currency assets):** "Assets held in foreign currency relate to receivables of R207 million (31 March 2025: R171 million; 30 September 2025: R190 million) and bank balances of R27 million (31 March 2025: R19 million; 30 September 2025: R27 million)." [D003, p. 26] — Total FX assets R234m (31 Mar 2026) vs R190m (31 Mar 2025) vs R217m (30 Sep 2025). FX liabilities are small (USD R10m, GBP R2m). Net FX asset exposure ~R222m — modest but growing; the new FX hedging programme (p. 25) is a change in risk management to verify.

**Fair value note qualification on p. 26:** "The fair value of principal book portfolios is determined by adjusting the discount rate from the credit-adjusted effective interest rate to a current market related discount rate of 18.50% (31 March 2025: 15.81%; 30 September 2025: 15.93%) and adjusting the expected cash flows for risk. The fair values determined on this basis approximates the carrying value." [D003, p. 26] — The **+269bp YoY rise in the market discount rate** is a major signal: either market risk premium on this asset class has risen sharply, or the credit-adjusted EIR itself has risen (consistent with the 19.2% EIR disclosed elsewhere). The claim that fair value "approximates carrying value" despite a 269bp discount-rate move is only credible if expected cash flows were also revised upward — which contradicts the "payer drop-offs and reduced settlement activity" narrative on p. 24. **Verification needed:** reconcile the 18.50% market discount rate to the 19.2% credit-adjusted EIR and to the fair value table showing carrying = fair value at R3,845m.

**Fair value table on p. 27:** Interest-bearing liabilities at 30 Sep 2025: carrying R3,807m vs fair value R3,468m — a **R339m fair-value deficit** (liabilities worth less than carrying, i.e. below-market funding). At 31 Mar 2026 the position reverses to a **R26m fair-value surplus** (carrying R3,743m vs fair value R3,769m). This R365m swing in six months is consistent with the sharp rise in market rates and needs to be reconciled to the interest-rate risk note.

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| N1 | High | D003 (remaining pages 8–21, 28–37) | Banking & specialised lending unsecured allowance fell from R460m (19.4% coverage) to R227m (9.6%) on flat gross R2,371m `[D003, p. 23]` | Locate the ECL model/assumption note and any methodology-change disclosure; reconcile the R233m release to performance vs assumption change | If release is model-driven, the R431m cumulative gain is overstated and future impairment charges will be larger |
| N2 | High | D003 (remaining pages) | "Cumulative impairment gain of R431m… reduction relates to payer drop-offs and reduced settlement activity" `[D003, p. 24]` | Locate the POCI/ERC note: investment base-case assumptions, actual vs expected collections, run-off profile of the R431m gain | Determines when impairment flips from gain to charge — critical P&L swing factor |
| N3 | High | D003 (remaining pages) | No write-off, recovery or FX lines in the ECL roll-forward `[D003, p. 24]` | Locate full ECL movement note with gross write-offs, post-write-off recoveries, FX and transfers | Needed to compute net bad debt charge and CLR |
| N4 | High | D003 (remaining pages) | Trade receivables matrix applies 0.00% ELR to 30+ and 61–90 day buckets at 31 Mar 2026 vs 0.06%/0.19%/6.67% at 30 Sep 2025 `[D003, p. 25]` | Locate accounting policy note on trade receivables provisioning and any methodology-change disclosure | A relaxed matrix understates receivables ECL and flatters earnings |
| N5 | High | D003 (remaining pages) | Market discount rate for principal book rose to 18.50% from 15.81% YoY, yet fair value "approximates carrying value" `[D003, p. 26]` | Locate PBD EIR/vintage note and reconcile 18.50% market rate to 19.2% credit-adjusted EIR and to fair value = carrying R3,845m | Tests whether the carrying value is genuinely supportable |
| N6 | High | D003 (remaining pages) | Interest-bearing liabilities fair value swung from R339m below carrying (30 Sep 2025) to R26m above (31 Mar 2026) `[D003, p. 27]` | Locate interest-rate risk note: fixed/floating split, hedge accounting, JIBAR/Prime sensitivity | Quantifies interest expense sensitivity and funding cost trajectory |
| N7 | Medium | D003 (remaining pages) | 31 Mar 2025 principal book gross/allowance split and other financial assets "represented" `[D003, p. 22]` | Locate any restatement/prior-period note confirming net carrying values unchanged | Confirms comparability of YoY movements |
| N8 | Medium | D003 (remaining pages) | Trade & other receivables gross R5,395m excludes prepayments/VAT/deposits `[D003, p. 22]` | Reconcile to statement of financial position trade & other receivables line; quantify excluded non-financial amounts | Needed for balance-sheet forecast |
| N9 | Medium | D003 (remaining pages) | Other financial assets R644m not assigned a fair value hierarchy level or sensitivity `[D003, p. 26–27]` | Locate note 6.3 continuation or other financial assets note: hierarchy level, inputs, sensitivity | Assesses earnings volatility from R644m Level 3 asset |
| N10 | Medium | D003 (remaining pages) | New FX hedging programme for USD/GBP receipts `[D003, p. 25]` | Locate hedge accounting note: notional, fair value of hedges, hedge reserve | Quantifies FX hedging P&L and reserve impact |
| N11 | Medium | D003 (remaining pages) | Acquisition-day ECL swung from R96m loss (H1 2025) to R24m gain (H1 2026) `[D003, p. 24]` | Locate portfolio acquisition note: purchase price, acquired ERC, day-one ECL basis | Tests whether acquisition economics are being managed to smooth P&L |
| N12 | Medium | D003 (remaining pages) | Debt review allowance rose from R65m (31 Mar 2025) to R141m (31 Mar 2026) on gross R951m (14.8% coverage) `[D003, p. 23]` | Locate debt review portfolio note: gross balance growth, coverage basis, rescheduling rules | Debt review is the fastest-growing segment — key credit risk driver |
| N13 | Low | D003 (remaining pages) | Retail allowance R51m exceeds gross R46m (111% coverage) `[D003, p. 23]` | Confirm retail book is in run-off/wind-down | Minor but confirms portfolio strategy |
| N14 | Low | D004 (p. 38) | Unclassified page 38 | Confirm nature (administration vs financial disclosure) | Completeness check |

---

### 5. Baseline Forecast Inputs Captured Here

| Metric | 31 Mar 2026 (Unaudited) | 31 Mar 2025 (Unaudited) | 30 Sep 2025 (Audited) |
|---|---|---|---|
| Principal book portfolio — gross carrying (Rm) | 3,414 | 3,066 | 3,377 |
| Principal book portfolio — ECL allowance (Rm) | 431 | 624 | 598 |
| Principal book portfolio — net carrying (Rm) | 3,845 | 3,690 | 3,975 |
| Implied total coverage % | 12.6% | 20.4% | 17.7% |
| — Banking & specialised lending unsecured: gross / allowance / coverage | 2,371 / 227 / 9.6% | 2,366 / 460 / 19.4% | 2,482 / 468 / 18.9% |
| — Debt review: gross / allowance / coverage | 951 / 141 / 14.8% | 605 / 65 / 10.7% | 793 / 72 / 9.1% |
| — Retail: gross / allowance / coverage | 46 / 51 / 110.9% | 32 / 54 / 168.8% | 48 / 47 / 97.9% |
| — Banking secured: gross / allowance / coverage | 46 / 12 / 26.1% | 63 / 45 / 71.4% | 54 / 11 / 20.4% |
| Net impairment (loss)/gain on principal book (Rm) | (167) | (173) | (26) FY |
| — Acquired during period (Rm) | +24 | (96) | +156 FY |
| — Historical book (Rm) | (191) | (77) | (182) FY |
| Trade receivables — gross / allowance / net (Rm) | 374 / 5 / 369 | 419 / 6 / 413 | 364 / 10 / 354 |
| Trade receivables total ELR | 1.34% | 1.43% | 2.75% |
| Other loans and receivables — gross / net (Rm) | 5,395 / 5,390 | 2,510 / 2,504 | 4,388 / 4,378 |
| Other financial assets (Rm) | 644 | 663 | 702 |
| Total financial assets carrying (Rm) | 4,884 | 4,859 | 5,059 |
| Interest-bearing liabilities — carrying / fair value (Rm) | 3,743 / 3,769 | 3,407 / 3,428 | 3,807 / 3,468 |
| Fixed rate liabilities (Rm) | nil | nil | nil |
| Market-related discount rate (principal book) | 18.50% | 15.81% | 15.93% |
| FX assets — USD / GBP / EUR / AUD (Rm) | 120 / 111 / 3 / – | 98 / 84 / 2 / 6 | 135 / 78 / 3 / 1 |
| FX liabilities — USD / GBP (Rm) | 10 / 2 | 5 / 16 | 1 / 1 |
| FX rates — USD avg / closing | 16.8 / 17.2 | 18.2 / 18.4 | 18.1 / 17.3 |
| FX rates — GBP avg / closing | 22.4 / 22.7 | 23.1 / 23.9 | 23.6 / 23.2 |
| Page offset | printed = physical − 2 | | |

---

### 6. Next Section to Capture

**`D003` remaining pages (physical pp. 8–21 and 28–37)** — specifically the statement of financial position (physical p. 8), income statement, cash flow statement (physical p. 12), and the notes covering IFRS 9 ECL staging, PBD EIR/vintage, funding/covenants, and segment reporting. These will resolve **N1–N12** (ECL model change, POCI run-off, write-offs/recoveries, trade receivables policy, EIR reconciliation, interest-rate sensitivity, restatement confirmation, receivables reconciliation, other financial assets hierarchy, FX hedging, acquisition economics, debt review). If only one further capture is possible, prioritise the **notes covering IFRS 9 ECL staging / PBD EIR / funding covenants** — these resolve the highest-priority open items (N1, N2, N3, N5, N6).

================================================================================
## SECTION 7: [D003] Primary financial statements (part 4/5, p.28-33)
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section D003 | [AFS] physical page 28 | area selection | Financial note ---
                                                                                  
                                                                                  
                   Condensed consolidated financial statements for the half year ended 31 March 2026 26
                                                                                  
                                                                                  
      Notes to the condensed consolidated financial statements continued          
      for the half year ended 31 March 2026                                       
                                                                                  
      6    Financial risk management                                              
                                       continued                                  
      6.3  Fair value disclosure continued                                        
           Fair values of financial instruments measured at fair value through profit and loss
           Financial assets that do not meet the criteria for being measured at amortised cost or fair value through other
           comprehensive income are measured at fair value through profit and loss. Certain purchased book debts (other
           financial assets) are managed on a fair value basis.                   
           The value of the purchased book debts managed on a fair value basis may change over time through the collection
           of underlying amounts that did not form part of the initial ring-fenced purchased book debt. The quantum of the
           return is also impacted by the quality of the collection services performed, rather than services associated with
           normal lending arrangements. On this basis, therefore, the cash flows collected on these books do not present solely
           payments of principal and interest on the principal amount outstanding.
           Valuation methods and assumptions:                                     
           Other financial assets: The valuation of other financial assets is based on the estimated future cash flows, discounted
           to their present value using a pre-tax discount rate that reflects current market assessments of the time value of
           money and the risks specific to the asset. These represent the significant unobservable parameters applied in the fair
           value model. The group estimates the expected cash flows by considering all the contractual terms of the financial
           instrument. The discount rate of 16% (31 March 2025: 12.93%; 30 September 2025: 16%) applied to the expected future
           cash flows reflects specific risk premiums relating to the asset and is based on the purchase-price average credit-
           adjusted effective interest rate (CAEIR) for unsecured loan books purchased in the last two years.
           Other investments: The value of money market investments is determined by fund managers on a net asset value
           basis, which is the total value of all the assets in the portfolio including any income accrual and less permissible
           deductions from the portfolio divided by the number of participatory interests in issue. Unit prices are calculated
           by fund managers and published daily.                                  
      6.4  Level disclosure                                                       
                                           Level 1  Level 2  Level 3    Total     
                                             Rm       Rm        Rm       Rm       
           31 March 2026 – Unaudited                                              
           Financial assets at fair value through                                 
           profit and loss                                                        
            Other financial assets            –         –      644       644      
            Other investments*                –        81        –       81       
           Total financial assets             –        81      644       725      
           31 March 2025 – Unaudited                                              
           Financial assets at fair value through                                 
           profit and loss                                                        
            Other financial assets            –         –      663       663      
            Other investments*                –       237        –       237      
           Total financial assets             –       237      663       900      
           30 September 2025 – Audited                                            
           Financial assets at fair value through                                 
           profit and loss                                                        
            Other financial assets            –         –      702       702      
            Other investments*                –        41        –       41       
           Total financial assets             –        41      702       743      
           * Other investments which have been categorised in level 2 comprise of money market fund investments.
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  

--- Section D003 | [AFS] physical page 29 | area selection | Financial note ---
                                                                                  
                                                                                  
                   Condensed consolidated financial statements for the half year ended 31 March 2026 27
                                                                                  
                                                                                  
      Notes to the condensed consolidated financial statements continued          
      for the half year ended 31 March 2026                                       
                                                                                  
      6    Financial risk management                                              
                                       continued                                  
      6.4  Level disclosure continued                                             
           Reconciliation of level 3 fair value measurements of financial assets and liabilities
                                                                                  
                                                   31 March 31 March 30 September 
                                                     2026      2025     2025      
                                                  Unaudited Unaudited Audited     
                                                      Rm        Rm       Rm       
           Financial assets at fair value through profit or loss                  
           Opening balance                            702      672       672      
           Total gains or losses                                                  
            In profit or loss                          30       74       114      
            Other movements*                          (88)      (83)     (84)     
           Closing balance                            644      663       702      
           * Other movements include additions of R28 million (31 March 2025: R7 million; 30 September 2025: R84 million) and cash collections of R116 million
             (31 March 2025: R90 million; 30 September 2025: R168 million).       
      7    Segment   report                                                       
           The Nutun group, has defined its operating and reportable segments to reflect its operating structure and internal
           reporting framework. Segmental reporting to the executive committee (who is considered the Chief Operating
           Decision Maker (CODM) in terms of IFRS 8) is organised based on the nature of the business units, which are split into:
           Nutun South Africa                                                     
           • Focuses exclusively on collections and recovery services for clients in South Africa, both as a principal through the
             acquisition of unsecured non-performing loan (NPL) portfolios and as an agent on behalf of clients in the financial
             services, specialist lending and retail sectors.                     
           • Revenue is mainly derived from debt collection and recovery services.
           Nutun International                                                    
           • Specialises in business process outsourcing (BPO) customer engagement services, including customer
             acquisition and retention customer experience, and collections and recovery services for clients located in the
             United Kingdom, the United States and Australia.                     
           • Revenue is derived from fee-for-services and collection services.    
           Group core results                                                     
           Nutun assesses its performance using core earnings, an alternative non-IFRS profit measure, alongside IFRS profit.
           Non-IFRS measures are not uniformly defined nor used by all entities and may not be comparable with similarly
           labelled measures and disclosures provided by other entities. Management considers that core earnings is an
           appropriate alternative performance measure to enhance the comparability and understanding of the financial
           performance of the group. The Group has set out its policy to calculate core earnings below.
           Core earnings is calculated by adjusting basic earnings for headline adjustments and the following:
           • Once-off transaction costs which are directly attributable to corporate activity (primarily legal and consulting
             fees).                                                               
           • Adjustments on put and call options over non-controlling interests, namely imputed interest on the put option
             liability, re-measurements of the put option liability and fair value adjustments on the call option derivative.
           • Once-off or accelerated items, where these are reasonably expected not to re-occur in the ordinary course
             of business in future reporting periods.                             
           • Adding back specified headline earnings exclusions, if the gain/loss is considered part of Nutun’s normal
             operations.                                                          
           These adjustments are considered annually based on the transforming nature of the group. Management is
           responsible for the calculation of core earnings and determining the inclusions and exclusions in accordance
           with the policy. The Nutun audit and risk committee reviews the core earnings for transparency and consistency.
           The reconciliation of basic (loss)/earnings, and core (loss)/earnings is included in this segment report.
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  

--- Section D003 | [AFS] physical page 30 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  |  |  |  | 28 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Notes to the condensed consolidated financial statements continued** | | | | | | | | |
| **for the half year ended 31 March 2026** | | | | | | | | |
| 7 Segment report continued |  |  |  |  |  |  |  |  |
| **Group core results continued** | | | | | | | | |
| **The CODM view of the Nutun South Africa segment reflects the manner in which the CODM measures the segment** | | | | | | | | |
| **for the purpose of allocating resources and assessing its performance. Under the CODM view, purchased book debt** | | | | | | | | |
| **collections are included in the revenue number, and the amortisation of the purchased book debts are reflected in** | | | | | | | | |
| **cost of revenue. Adjustments are reflected in the table below to reconcile the CODM view to the IFRS reporting. In** | | | | | | | | |
| **terms of IFRS reporting, collections are taken into account in the movement of the amortised cost on the statement** | | | | | | | | |
| **of financial position, and the income statement therefore reflects interest revenue and impairment gains/(losses).** | | | | | | | | |
|  |  |  |  |  |  | Nutun |  |  |
|  | Nutun South Africa International |  |  |  |  |  | Group |  |
|  | PBD |  |  |  |  |  |  |  |
|  | CODM accounting IFRS |  |  |  |  |  |  |  |
|  | view adjustments reporting |  |  |  |  |  |  |  |
|  | Rm Rm Rm |  |  |  |  | Rm | Rm |  |
| **Summarised income** | | | | | | | | |
| statement |  |  |  |  |  |  |  |  |
| **for the half year ended** | | | | | | | | |
| **31 March 2026 – Unaudited** | | | | | | | | |
| Revenue* | 159 – 159 |  |  |  |  | 552 | 711 |  |
| **Revenue from purchased** | | | | | | | | |
| book debts | 888 (888) - |  |  |  |  | – | - |  |
| **Net income from purchased** | | | | | | | | |
| book debts | – 69 69 |  |  |  |  | – | 69 |  |
| **Total operating expenses and** | | | | | | | | |
| cost of revenue | (968) 642 (326) |  |  |  |  | (504) | (830) |  |
| Cost of revenue | (241) 105 (136) |  |  |  |  | (249) | (385) |  |
| **Amortisation of purchased** | | | | | | | | |
| book debts | (597) 597 - |  |  |  |  | – | - |  |
| Operating costs | (130) (60) (190) |  |  |  |  | (255) | (445) |  |
| Other income | 4 – 4 |  |  |  |  | 7 | 11 |  |
| Equity accounted loss | (1) – (1) |  |  |  |  | – | (1) |  |
| Non-operating loss | (2) – (2) |  |  |  |  | (11) | (13) |  |
| Net finance charge | (203) 177 (26) |  |  |  |  | (13) | (39) |  |
| Finance income | 6 – 6 |  |  |  |  | – | 6 |  |
| Finance charge | (209) 177 (32) |  |  |  |  | (13) | (45) |  |
| (Loss)/profit before tax | (123) – (123) |  |  |  |  | 31 | (92) |  |
| Income tax credit/(expense) | 37 – 37 |  |  |  |  | (8) | 29 |  |
| **(Loss)/profit for the period** | | | | | | | | |
| from continuing operations | (86) – (86) |  |  |  |  | 23 | (63) |  |
| **Profit for the period from** | | | | | | | | |
| discontinued operations | – – – |  |  |  |  | – | – |  |
| (Loss)/profit for the period | (86) – (86) |  |  |  |  | 23 | (63) |  |

*  Refer to note 4.1 for the disaggregation of revenue.

--- Section D003 | [AFS] physical page 31 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  | 29 |
| --- | --- | --- | --- | --- | --- |
| **Notes to the condensed consolidated financial statements continued** | | | | | |
| **for the half year ended 31 March 2026** | | | | | |
| **7  Segment report continued** | | | | | |
| **Group core results continued** | | | | | |
|  | Nutun |  | Nutun |  |  |
|  | South Africa International |  |  | Group |  |
|  | Rm |  | Rm | Rm |  |
| **Reconciliation to core continuing earnings** | | | | | |
| **and core EBITDA** | | | | | |
| **for the half year ended 31 March 2026 - Unaudited** | | | | | |
| (Loss)/profit for the period from continuing operations | (86) |  | 23 | (63) |  |
| Exceptional items (core and headline adjustments) | - |  | - | - |  |
| Core continuing (loss)/earnings per segment | (86) |  | 23 | (63) |  |
| Tax expense | (37) |  | 8 | (29) |  |
| Depreciation and amortisation | 32 |  | 36 | 68 |  |
| Amortisation of purchased book debts* | 597 |  | - | 597 |  |
| Equity accounted loss | 1 |  | - | 1 |  |
| Net finance charge | 203 |  | 13 | 216 |  |
| Core EBITDA per segment** | 710 |  | 80 | 790 |  |

*   Amortisation of purchased book debts is calculated as CAEIR imputed interest revenue of R383 million, impairment loss of R167 million and net cash
collections of R728 million per note 1.1 and fair value movements of R30 million and cash collections of R116 million per note 1.2.
** Core EBITDA is a non-IFRS measure calculated as core earnings per the policy above adjusted for Interest, Tax, Depreciation and Amortisation and
Equity accounted earnings. It represents management’s view of operating cash flows.

--- Section D003 | [AFS] physical page 32 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  |  |  |  | 30 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Notes to the condensed consolidated financial statements continued** | | | | | | | | |
| **for the half year ended 31 March 2026** | | | | | | | | |
| **7  Segment report continued** | | | | | | | | |
| **Group core results continued** | | | | | | | | |
|  |  |  |  |  |  | Nutun |  |  |
|  | Nutun South Africa International |  |  |  |  |  | Group |  |
|  | PBD |  |  |  |  |  |  |  |
|  | CODM accounting IFRS |  |  |  |  |  |  |  |
|  | view adjustments reporting |  |  |  |  |  |  |  |
|  | Rm Rm Rm |  |  |  |  | Rm | Rm |  |
| **Summarised income** | | | | | | | | |
| statement |  |  |  |  |  |  |  |  |
| **for the half year ended** | | | | | | | | |
| **31 March 2025 – Unaudited** | | | | | | | | |
| Revenue* | 188 – 188 |  |  |  |  | 557 | 745 |  |
| **Revenue from purchased** | | | | | | | | |
| book debts | 694 (694) – |  |  |  |  | – | - |  |
| **Net income from purchased** | | | | | | | | |
| book debts | – 53 53 |  |  |  |  | – | 53 |  |
| **Total operating expenses** | | | | | | | | |
| and cost of revenue | (858) 460 (398) |  |  |  |  | (514) | (912) |  |
| Cost of revenue | (226) 107 (119) |  |  |  |  | (233) | (352) |  |
| **Amortisation of purchased** | | | | | | | | |
| book debts | (422) 422 - |  |  |  |  | - | - |  |
| Operating costs | (210) (69) (279) |  |  |  |  | (281) | (560) |  |
| Other income | 35 - 35 |  |  |  |  | 6 | 41 |  |
| Equity accounted loss | (43) - (43) |  |  |  |  | - | (43) |  |
| Non-operating profit | 1 - 1 |  |  |  |  | 6 | 7 |  |
| Net finance charge | (219) 181 (38) |  |  |  |  | (14) | (52) |  |
| Finance income | 22 - 22 |  |  |  |  | - | 22 |  |
| Finance charge | (241) 181 (60) |  |  |  |  | (14) | (74) |  |
| Operating (loss)/profit | (202) - (202) |  |  |  |  | 41 | (161) |  |
| Income tax credit/(expense) | 47 - 47 |  |  |  |  | (8) | 39 |  |
| **(Loss)/profit for the period** | | | | | | | | |
| from continuing operations | (155) - (155) |  |  |  |  | 33 | (122) |  |
| **Profit for the period from** | | | | | | | | |
| discontinued operations | 58 - 58 |  |  |  |  | - | 58 |  |
| (Loss)/profit for the period | (97) - (97) |  |  |  |  | 33 | (64) |  |

*  Refer to note 4.1 for the disaggregation of revenue.

--- Section D003 | [AFS] physical page 33 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  |  | 31 |
| --- | --- | --- | --- | --- | --- | --- |
| **Notes to the consolidated financial statements continued** | | | | | | |
| **for the half year ended 31 March 2026** | | | | | | |
| 7 Segment report continued |  |  |  |  |  |  |
| **Group core results continued** | | | | | | |
|  | Nutun |  |  | Nutun |  |  |
|  | Foot- South Africa International |  |  |  | Group |  |
|  | notes Rm |  |  | Rm | Rm |  |
| **Reconciliation to core continuing** | | | | | | |
| **earnings and core EBITDA** | | | | | | |
| **for the half year ended 31 March 2025 - Unaudited**** | | | | | | |
| (Loss)/profit for the period from continuing operations | (155) |  |  | 33 | (122) |  |
| Exceptional items (core and headline adjustments) | 51 |  |  | – | 51 |  |
| Transaction costs | 1 5 |  |  | – | 5 |  |
| Tax impact | (1) |  |  | – | (1) |  |
| Impairment of investment in associate | 2 47 |  |  | – | 47 |  |
| Tax impact | – |  |  | – | – |  |
| Core continuing (loss)/earnings per segment | (104) |  |  | 33 | (71) |  |
| Tax expense | 3 (46) |  |  | 8 | (38) |  |
| Depreciation and amortisation | 35 |  |  | 38 | 73 |  |
| Amortisation of purchased book debts | 4 422 |  |  | – | 422 |  |
| Equity accounted loss | 5 (4) |  |  | – | (4) |  |
| Net finance charge | 219 |  |  | 14 | 233 |  |
| Core EBITDA per segment* | 522 |  |  | 93 | 615 |  |
| *** Core EBITDA is a non-IFRS measure calculated as core earnings per the policy above adjusted for Interest, Tax, Depreciation and Amortisation and** | | | | | | |
| **Equity accounted earnings. It represents management’s view of operating cash flows.** | | | | | | |
| **** Comparative disclosure for 31 March 2025 has been presented for the first time in order to enhance the overall presentation of the financial statements.** | | | | | | |
| **1   Once-off costs incurred in relation to the restructuring of the group.** | | | | | | |
| **2  Impairment of financial assets which were held by TC Global Finance.** | | | | | | |
| **3   Tax expense per Income statement adjusted for tax on exceptional items.** | | | | | | |
| **4   Amortisation of purchased book debts is calculated as CAEIR imputed interest revenue of R333 million, impairment loss of R173 million and net cash** | | | | | | |
| **collections of R566 million per note 1.1 and fair value movements of R74 million and cash collections of R90 million per note 1.2.** | | | | | | |
| **5  Equity accounted loss adjusted for exceptional items.** | | | | | | |
|  | Nutun |  |  | Nutun |  |  |
|  | Foot- South Africa International |  |  |  | Group |  |
|  | notes Rm |  |  | Rm | Rm |  |
| **Reconciliation to core discontinued loss** | | | | | | |
| **for the half year ended 31 March 2025 - Unaudited*** | | | | | | |
| Profit/(loss) for the year from discontinued operations | 58 |  |  | – | 58 |  |
| Exceptional items (core and headline adjustments) | (58) |  |  | – | (58) |  |
| Profit on disposal | 1 (100) |  |  | – | (100) |  |
| Tax impact | 29 |  |  | – | 29 |  |
| Transaction costs | 2 16 |  |  | – | 16 |  |
| Tax impact | (3) |  |  | – | (3) |  |
| Core discontinued loss per segment | – |  |  | – | – |  |

* Comparative disclosure for 31 March 2025 has been presented for the first time in order to enhance the overall presentation of the financial statements.
1 Profit on disposal of Nutun Transact.
2 Transaction costs incurred on disposal of Nutun Transact.

### [ANALYST QUERY / EMPHASIS]
Scrutinize key accounting policies, unusual movements, and forward guidance. This is one capture, not proof of whole-report coverage. Adjacent tables/footnotes may need verification.

### [SECTION READING RESPONSE / DETERMINATION]
### 1. Answers to Stored Questions for This Section

**Q-3df04995ff2f4c6a [high] [partial] — Headline metrics, guidance, page offset**
- **Status**: `Partially resolved (remainder stays open for D003/D004)`
- **Answer & evidence**: Page offset re-confirmed: printed footer "26" on physical p. 28, "31" on physical p. 33 → printed = physical − 2. No headline advances/CLR/NIM/HEPS/DPS or guidance in this capture. Segment revenue captured: Group revenue R711m (H1 2026) vs R745m (H1 2025) [D003, physical p. 30, p. 32]. Remainder open.

**Q-64b704d06ed84c90 — Write-offs, recoveries, debt, dividends**
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: No gross write-offs, bad-debt recoveries, debt raised/repaid, or dividends in this capture. Cash collections on other financial assets R116m (H1 2026) vs R90m (H1 2025) vs R168m (FY2025) [D003, physical p. 29]. Net cash collections on PBD R728m (H1 2026) vs R566m (H1 2025) [D003, physical p. 31, p. 33]. Remainder open.

**Q-336536b6077249e3 — IFRS 9 ECL staging, SICR, write-off policy, covenants**
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: No IFRS 9 staging/SICR/write-off/covenant content. However, PBD impairment loss of R167m (H1 2026) vs R173m (H1 2025) is disclosed inside the amortisation footnote [D003, physical p. 31, p. 33]. Remainder open.

**Q-add37e0058a74df2 [low] [partial] — Audit/review status & APM add-backs**
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: Core earnings policy now fully quoted [D003, physical p. 29]: adjustments for (i) once-off transaction costs, (ii) put/call option adjustments over NCI, (iii) "once-off or accelerated items… reasonably expected not to re-occur", (iv) adding back specified headline exclusions if part of "normal operations". H1 2026 exceptional items = nil [D003, physical p. 31]; H1 2025 exceptional items R51m (transaction costs R5m, associate impairment R47m, tax −R1m) [D003, physical p. 33]. Note the discretionary "considered annually" review and management responsibility — earnings-quality flag. Remainder (audit status of statements) open.

**Q-47cc084806ec463d [low] — p. 38 nature**: Not addressed in this capture; carried forward.

**Q-007f8f020e154296, Q-e741a412cfd44a34, Q-b63cf1b01b6d4cf8, Q-b3d2bdde10394bac, Q-fec447426706441e, Q-7acc435c1ae94e77, Q-c06d7a5336224c7e, Q-e8e8f8f7354146ea, Q-174a38f8f4c04abc, Q-aea94945233b418a, Q-59b88716280048c3, Q-ebf661d7f2e740cd, Q-0b9b00a6c7da4496, Q-5a1c41b2ef654626, Q-019095eae85848d1, Q-48250bf920104880, Q-d999efdf22e5453b, Q-19a3c1172f494459, Q-d9c20b083a06486d, Q-e0fd336bd6e441b5, Q-28dc6d0fd29c48ce, Q-11d46434b5e548de, Q-9716a218b43b416b, Q-32dcbb2aeead41c8, Q-ed4807de3ac74d68, Q-8a74a12fefbf4e13, Q-a14f390ef9d042b0, Q-429b0eebe1144e16, Q-777af456b5384c00, Q-5a215339455549cb, Q-e0ad7294ef664877, Q-e638336bf5bf48a6, Q-91785c26cc0b4e99, Q-692b91fba36d46b3, Q-abbce81b5da84312, Q-533b9024210549c0, Q-83a5d39bd7374279, Q-74e79aaa44cc4a15, Q-0ada68da08fa49fc, Q-d781546003984272, Q-5e16f0ada73840c8, Q-c0430bffdd134145, Q-5fc0971fd6174503, Q-c0e5fb0f2f3c409c, Q-d3214701599f4536, Q-2a3622968261481a, Q-4ed57bbdde83420e, Q-f8d00abd0de446f5, Q-024f496e3b2f4b57, Q-48aec45bd7754483, Q-b6b4741e827b495d**: Not addressed by this capture (no statement of financial position, cash flow, ECL staging, funding, or vintage content here). Carried forward.

---

### 2. Footnote & Qualification Deep-Dive

- **Other financial assets discount rate 16% (31 Mar 2025: 12.93%; 30 Sep 2025: 16%)** [D003, physical p. 28]. The rate is "based on the purchase-price average credit-adjusted effective interest rate (CAEIR) for unsecured loan books purchased in the last two years." Implication: the +307bp YoY jump in discount rate is a **valuation input change**, not necessarily a cash-flow change — it mechanically depresses fair value and can flatter future "fair value gains" as the rate normalises. Must verify whether the 16% is a genuine market-risk repricing or a conservatism overlay, and reconcile to the PBD CAEIR of 19.2% (Q-3df04995ff2f4c6a / PBD EIR question). Also note the fair value basis is justified by "cash flows… do not present solely payments of principal and interest" — i.e., the book is classified FVTPL to avoid amortised-cost/ECL staging. **This means no IFRS 9 Stage 1/2/3 disclosure exists for the R644m other financial assets** — a structural gap for credit-risk forecasting.

- **Level 3 reconciliation footnote** [D003, physical p. 29]: "Other movements include additions of R28m (31 Mar 2025: R7m; 30 Sep 2025: R84m) and cash collections of R116m (31 Mar 2025: R90m; 30 Sep 2025: R168m)." Arithmetic check: opening 702 + gains 30 − other movements 88 = 644 ✓. But "other movements" of −R88m = additions +R28m − collections −R116m = −R88m ✓. **Key observation**: H1 2026 fair value gain R30m vs R74m (H1 2025) vs R114m (FY2025) — gain run-rate is decelerating sharply (−59% YoY) while additions rose to R28m. Collections fell to R116m from R168m (FY2025 half-year equivalent ~R84m). Verify whether the R30m gain is a genuine re-estimate or a plug to offset the higher 16% discount rate.

- **Segment CODM-vs-IFRS reconciliation** [D003, physical p. 30]: PBD "Revenue from purchased book debts" R888m (CODM) reversed out (−R888m) to nil under IFRS; "Net income from purchased book debts" R69m under IFRS = CAEIR imputed interest R383m − impairment R167m − net cash collections R728m + fair value movements R30m + cash collections R116m (per footnote, p. 31). **Arithmetic tension**: 383 − 167 − 728 + 30 + 116 = **−R366m**, not +R69m. The footnote components do not reconcile to the R69m IFRS net income line — this is a material reconciliation gap requiring verification (likely the R728m "net cash collections" is being netted differently, or the R888m CODM revenue embeds gross collections). Flag as high-priority.

- **Amortisation of PBD footnote** [D003, physical p. 31]: "CAEIR imputed interest revenue of R383m, impairment loss of R167m and net cash collections of R728m per note 1.1 and fair value movements of R30m and cash collections of R116m per note 1.2." H1 2025 equivalent [p. 33]: CAEIR R333m, impairment R173m, net cash collections R566m, FV movements R74m, cash collections R90m. **Impairment loss fell only R6m (−3.5%) YoY despite gross PBD collections rising 28%** — coverage adequacy question. Also note the R597m amortisation line (p. 30) is the CODM-view amortisation, distinct from the IFRS impairment R167m — do not conflate.

- **Core earnings policy** [D003, physical p. 29]: "Once-off or accelerated items, where these are reasonably expected not to re-occur in the ordinary course of business" and "Adding back specified headline earnings exclusions, if the gain/loss is considered part of Nutun's normal operations." **Qualification risk**: the "accelerated items" carve-out is precisely the mechanism that could exclude recurring PBD amortisation acceleration or ECL re-estimate charges from core earnings. H1 2026 exceptional items = nil, but the policy permits future add-backs. Verify in D004/D006 whether any "accelerated" PBD amortisation or impairment is being excluded from core.

- **Comparative disclosure footnote** [D003, physical p. 33]: "Comparative disclosure for 31 March 2025 has been presented for the first time in order to enhance the overall presentation." This means the H1 2025 segment/core reconciliation is **newly constructed**, not previously reported — comparability and potential cherry-picking of the R51m exceptional items must be verified.

- **Discontinued operations footnote** [D003, physical p. 33]: H1 2025 profit from discontinued ops R58m = profit on disposal of Nutun Transact R100m − tax R29m − transaction costs R16m + tax R3m. H1 2026 discontinued = nil. Confirms disposal complete; no residual in current period.

- **Revenue footnote `*`** [D003, physical p. 30, p. 32]: "Refer to note 4.1 for the disaggregation of revenue" — note 4.1 not in this capture; must be located.

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| N1 | High | D003 (remaining pp. 8–27, 34–37) | PBD IFRS net income R69m vs footnote components summing to −R366m [D003, p. 30–31] | Locate note 1.1 (PBD) and note 1.2 (other financial assets) and reconcile CAEIR R383m − impairment R167m − net collections R728m + FV R30m + collections R116m to the R69m IFRS line; identify the missing R435m bridge | Determines true PBD economics and whether R69m is a genuine margin or an accounting artefact |
| N2 | High | D003 (remaining) | Other financial assets discount rate 16% vs 12.93% YoY; FV gain R30m vs R74m [D003, p. 28–29] | Locate note 1.2 / 6.3 continuation: discount-rate sensitivity, cash-flow assumptions, and whether the 16% is market-driven or overlay; reconcile to PBD CAEIR 19.2% | Fair value gain recurrence and R644m carrying value supportability |
| N3 | High | D003 (remaining) | PBD impairment R167m vs R173m on 28% higher collections [D003, p. 31, p. 33] | Locate PBD ECL/impairment note: gross ECL charge vs favourable re-estimate, coverage %, and whether impairment is being suppressed by re-estimates | CLR forecast and provisioning adequacy |
| N4 | High | D003 (remaining) | Core earnings policy permits "accelerated items" and "normal operations" add-backs [D003, p. 29] | Locate any core-earnings reconciliation detail beyond the two shown; check whether PBD amortisation acceleration or ECL re-estimates are excluded from core | Earnings quality; core EBITDA R790m vs IFRS loss R63m gap |
| N5 | Medium | D003 (remaining) | H1 2025 segment/core reconciliation presented "for the first time" [D003, p. 33] | Locate reclassification/representation note; confirm H1 2025 exceptional items R51m and core EBITDA R615m are consistently constructed | Comparability of YoY core earnings |
| N6 | Medium | D003 (remaining) | Note 4.1 revenue disaggregation referenced but not captured [D003, p. 30, p. 32] | Locate note 4.1: SA vs International, agency fees, DTI incentives, PBD revenue split | Revenue mix and DTI contingency |
| N7 | Medium | D003 (remaining) | Nutun International profit R23m (H1 2026) vs R33m (H1 2025) on revenue R552m vs R557m [D003, p. 30, p. 32] | Locate International segment cost detail; explain margin compression despite flat revenue | International EBITDA sustainability |
| N8 | Medium | D003 (remaining) | SA PBD operating costs R190m vs R279m (−32%) [D003, p. 30, p. 32] | Locate cost-of-revenue/opex note; confirm whether cost cut is structural or one-off | SA cost base run-rate |
| N9 | Medium | D003 (remaining) | Net finance charge R39m (H1 2026) vs R52m (H1 2025); SA PBD finance charge R32m vs R60m [D003, p. 30, p. 32] | Locate borrowings/interest note; reconcile to funding facilities and rate sensitivity | Interest expense forecast |
| N10 | Medium | D003 (remaining) | Income tax credit R29m on R(92)m loss (effective −31.5%) [D003, p. 30] | Locate tax note: current/deferred split, DTA recognition | Tax forecast and DTA recoverability |
| N11 | Low | D003 (remaining) | Other investments Level 2 R81m vs R237m vs R41m [D003, p. 28] | Locate other investments note; explain swing | Minor liquidity input |
| N12 | Low | D003 (remaining) | Discontinued ops nil H1 2026 vs R58m H1 2025 [D003, p. 30, p. 32] | Confirm no residual discontinued liabilities/indemnities | Clean base for continuing forecast |

---

### 5. Baseline Forecast Inputs Captured Here

| Metric | H1 2026 | H1 2025 | FY2025 (Sep) |
|---|---|---|---|
| Group revenue | R711m | R745m | — |
| SA revenue (IFRS) | R159m | R188m | — |
| International revenue | R552m | R557m | — |
| PBD CODM revenue from purchased book debts | R888m | R694m | — |
| Net income from PBD (IFRS) | R69m | R53m | — |
| Cost of revenue | R385m | R352m | — |
| Operating costs | R445m | R560m | — |
| PBD amortisation (CODM) | R597m | R422m | — |
| — CAEIR imputed interest | R383m | R333m | — |
| — PBD impairment loss | R167m | R173m | — |
| — PBD net cash collections | R728m | R566m | — |
| Other financial assets FV gain | R30m | R74m | R114m |
| Other financial assets cash collections | R116m | R90m | R168m |
| Other financial assets additions | R28m | R7m | R84m |
| Other financial assets closing (Level 3) | R644m | R663m | R702m |
| Other financial assets discount rate | 16% | 12.93% | 16% |
| Other investments (Level 2) | R81m | R237m | R41m |
| Net finance charge (Group) | R39m | R52m | — |
| SA PBD finance charge | R32m | R60m | — |
| International net finance charge | R13m | R14m | — |
| Equity accounted loss | R1m | R43m | — |
| Non-operating (loss)/profit | R(13)m | R7m | — |
| (Loss)/profit before tax | R(92)m | R(161)m | — |
| Income tax credit/(expense) | R29m | R39m | — |
| Profit from continuing ops | R(63)m | R(122)m | — |
| Profit from discontinued ops | nil | R58m | — |
| Core continuing earnings | R(63)m | R(71)m | — |
| Core EBITDA | R790m | R615m | — |
| Exceptional items | nil | R51m | — |
| D&A | R68m | R73m | — |

---

### 6. Next Section to Capture

**D003 remaining pages (physical pp. 8–27 and 34–37)** — specifically the statement of financial position (p. 8), income statement, cash flow (p. 12), and notes 1.1/1.2/4.1/ECL/funding. This will resolve **N1, N2, N3, N4, N5, N6** and the bulk of the carried-forward D002 questions (gross advances, ECL staging, write-offs, funding covenants, PBD EIR). If only one further capture is possible, prioritise **physical pp. 8–15** (primary statements + notes 1.1/1.2) to close the R69m PBD reconciliation (N1) and the discount-rate/FV question (N2).

================================================================================
## SECTION 8: [D003] Primary financial statements (part 5/5, p.34-37)
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section D003 | [AFS] physical page 34 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  |  |  |  | 32 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Notes to the consolidated financial statements continued** | | | | | | | | |
| **for the half year ended 31 March 2026** | | | | | | | | |
| 7 Segment report continued |  |  |  |  |  |  |  |  |
| **Group core results continued** | | | | | | | | |
|  |  |  |  |  |  | Nutun |  |  |
|  | Nutun South Africa International |  |  |  |  |  | Group |  |
|  | PBD |  |  |  |  |  |  |  |
|  | CODM accounting IFRS |  |  |  |  |  |  |  |
|  | view adjustments reporting |  |  |  |  |  |  |  |
|  | Rm Rm Rm |  |  |  |  | Rm | Rm |  |
| **Summarised income** | | | | | | | | |
| statement |  |  |  |  |  |  |  |  |
| **for the year ended** | | | | | | | | |
| **30 September 2025 –** | | | | | | | | |
| Audited |  |  |  |  |  |  |  |  |
| Revenue* | 341 – 341 |  |  |  |  | 1 094 | 1 435 |  |
| **Revenue from purchased** | | | | | | | | |
| book debts | 1 449 (1 449) – |  |  |  |  | – | – |  |
| **Net income from purchased** | | | | | | | | |
| book debts | – 244 244 |  |  |  |  | – | 244 |  |
| **Total operating expenses and** | | | | | | | | |
| cost of revenue | (1 625) 851 (774) |  |  |  |  | (1 021) | (1 795) |  |
| Cost of revenue | (474) 210 (264) |  |  |  |  | (468) | (732) |  |
| **Amortisation of purchased** | | | | | | | | |
| book debts | (767) 767 – |  |  |  |  | – | – |  |
| Operating costs | (384) (126) (510) |  |  |  |  | (553) | (1 063) |  |
| Other income | 56 – 56 |  |  |  |  | 13 | 69 |  |
| Equity accounted loss | (48) – (48) |  |  |  |  | – | (48) |  |
| Non-operating profit | (1) – (1) |  |  |  |  | 39 | 38 |  |
| Net finance charge | (419) 354 (65) |  |  |  |  | (26) | (91) |  |
| Finance income | 36 – 36 |  |  |  |  | – | 36 |  |
| Finance charge | (455) 354 (101) |  |  |  |  | (26) | (127) |  |
| (Loss)/profit before tax | (247) – (247) |  |  |  |  | 99 | (148) |  |
| Income tax credit/(expense) | 58 – 58 |  |  |  |  | (23) | 35 |  |
| **(Loss)/profit for the year from** | | | | | | | | |
| continuing operations | (189) – (189) |  |  |  |  | 76 | (113) |  |
| **Loss for the year from** | | | | | | | | |
| discontinued operations | (125) – (125) |  |  |  |  | – | (125) |  |
| (Loss)/profit for the year | (314) – (314) |  |  |  |  | 76 | (238) |  |

* Refer to note 4.1 for the disaggregation of revenue.

--- Section D003 | [AFS] physical page 35 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  |  | 33 |
| --- | --- | --- | --- | --- | --- | --- |
| **Notes to the consolidated financial statements continued** | | | | | | |
| **for the half year ended 31 March 2026** | | | | | | |
| 7 Segment report continued |  |  |  |  |  |  |
| **Group core results continued** | | | | | | |
|  | Nutun |  |  | Nutun |  |  |
|  | Foot- South Africa International |  |  |  | Group |  |
|  | notes Rm |  |  | Rm | Rm |  |
| **Reconciliation to core continuing** | | | | | | |
| **(loss)/earnings and core EBITDA** | | | | | | |
| **for the year ended 30 September 2025 - Audited** | | | | | | |
| (Loss)/profit for the year from continuing operations | (189) |  |  | 76 | (113) |  |
| Exceptional items (core and headline adjustments) | 68 |  |  | – | 68 |  |
| Transaction costs | 1 29 |  |  | – | 29 |  |
| Tax impact | (8) |  |  | – | (8) |  |
| Impairment of investment in associate | 2 47 |  |  | – | 47 |  |
| Tax impact | – |  |  | – | – |  |
| Core continuing (loss)/earnings per segment | (121) |  |  | 76 | (45) |  |
| Tax expense | 3 (50) |  |  | 23 | (27) |  |
| Depreciation and amortisation | 90 |  |  | 73 | 163 |  |
| Amortisation of purchased book debts | 4 767 |  |  | – | 767 |  |
| Equity accounted loss | 5 1 |  |  | – | 1 |  |
| Net finance charge | 419 |  |  | 26 | 445 |  |
| Core EBITDA per segment* | 1 106 |  |  | 198 | 1 304 |  |
| *** Core EBITDA is a non-IFRS measure calculated as core earnings per the policy above adjusted for Interest, Tax, Depreciation and Amortisation and** | | | | | | |
| **Equity accounted earnings. It represents management’s view of operating cash flows.** | | | | | | |
| **1   Once-off costs incurred in relation to the restructuring of the group.** | | | | | | |
| **2  Impairment of financial assets which were held by TC Global Finance.** | | | | | | |
| **3   Tax expense per Income statement adjusted for tax on exceptional items.** | | | | | | |
| **4   PBD amortisation is calculated as CAEIR imputed interest revenue of R683 million, impairment loss of R199 million and net cash collections of** | | | | | | |
| **R1 197 million per note 1.1 and fair value movements of R114 million and cash collections of R168 million per note 1.2.** | | | | | | |
| **5  Equity accounted loss adjusted for exceptional items.** | | | | | | |
|  | Nutun |  |  |  |  |  |
|  | Foot- South Africa |  |  | Other | Group |  |
|  | notes Rm |  |  | Rm | Rm |  |
| **Reconciliation to core discontinued loss** | | | | | | |
| **for the year ended 30 September 2025 - Audited** | | | | | | |
| Profit/(loss) for the year from discontinued operations | 51 |  |  | (176) | (125) |  |
| Exceptional items (core and headline adjustments) | (58) |  |  | 176 | 118 |  |
| Settlement fee | 1 - |  |  | 176 | 176 |  |
| Tax impact | - |  |  | - | - |  |
| Profit on disposal | 2 (100) |  |  | - | (100) |  |
| Tax impact | 29 |  |  | - | 29 |  |
| Transaction costs | 3 16 |  |  | - | 16 |  |
| Tax impact | (3) |  |  | - | (3) |  |
| Core discontinued loss per segment | (7) |  |  | - | (7) |  |

1 As part of the disposal of shares in Mobalyz Group Holdings Proprietary Limited, and in return for a 3 year commitment from its main bank funders to
renew and/or revolve all facilities that mature before 30 September 2027, Nutun agreed that 90% of any dividends that it receives from Nutun Holdings
Proprietary Limited, if and when declared, will be utilised to acquire SA Taxi Holdings Proprietary Limited (“SAT”) loan claims to a value of R200 million,
if settled by 26 November 2026, or R250 million, if settled post that date. Nutun satisfied its commitments under this agreement through a full and final
settlement of R176 million. As a result, Nutun is no longer required to acquire SAT loan claims. No further amounts are outstanding between the parties
in respect of this transaction.
2 Profit on disposal of Nutun Transact.
3 Transaction costs incurred on disposal of Nutun Transact.

--- Section D003 | [AFS] physical page 36 | area selection | Table ---
| Condensed consolidated financial statements for the half year ended 31 March 2026 |  |  |  |  | 34 |
| --- | --- | --- | --- | --- | --- |
| **Notes to the condensed consolidated financial statements continued** | | | | | |
| **for the half year ended 31 March 2026** | | | | | |
| 7 Segment report continued |  |  |  |  |  |
| **Geographical information** | | | | | |
| **The group recognises revenue earned from the following geographic regions:** | | | | | |
|  | Total revenue* |  |  |  |  |
|  | 31 March 31 March 30 September |  |  |  |  |
|  | 2026 |  | 2025 | 2025 |  |
|  | Unaudited Unaudited |  |  | Audited |  |
|  | Rm |  | Rm | Rm |  |
| Nutun South Africa | 1 047 |  | 882 | 1 790 |  |
| South Africa | 1 047 |  | 882 | 1 790 |  |
| Nutun International | 552 |  | 557 | 1 094 |  |
| United Kingdom | 303 |  | 259 | 525 |  |
| United States | 212 |  | 224 | 428 |  |
| Australia | 27 |  | 74 | 127 |  |
| Other | 10 |  | – | 14 |  |
| Total | 1 599 |  | 1 439 | 2 884 |  |

* Revenue comprises gross revenue as presented on the income statement, and revenue from purchased book debts as presented in the CODM view.
8  Going concern
The condensed consolidated financial statements were prepared on a going concern basis. Based on their
assessment, the directors have no reason to believe that the group will not continue as a going concern for the
foreseeable future. This assessment included an assessment of the relevance of its business models, the nature
of the primary assets and the cash flows generated from these assets as well as the group’s balance sheet.
9 Subsequent events
The directors are not aware of any material events occurring between the end of the reporting period and the date
of approval of these financial statements that would require adjustment or disclosure in terms of IAS 10 – Events
after the reporting period.

--- Section D003 | [AFS] physical page 37 | area selection | Financial note ---
                                                                                  
                                                                                  
                   Condensed consolidated financial statements for the half year ended 31 March 2026 35
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
      Administration                                                              
                                                                                  
                                                                                  
                                                                                  
                                                                                  
      Company    information              Legal advisers                          
      Share code: NTU                     Edward Nathan Sonnenbergs Inc.          
      ISIN: ZAE000167391                  (Registration number 2006/018200/21)    
      JSE Limited sector: Financial Services The MARC                             
      Listing date: 7 June 2012           Tower 1                                 
      Year end: 30 September              129 Rivonia Road                        
      Company registration number: 2002/031730/06 Sandton, 2196                   
      Country of incorporation: South Africa (PO Box 783347, Sandton, 2146)       
                                                                                  
      Directors                           Transfer secretaries                    
                                                                                  
      Executive                           Computershare Investor Services         
      Jonathan Jawno (Executive chairman) Proprietary Limited                     
      Robert Huddy (CFO)                  (Registration number 2004/003647/07)    
      Robert Amoils (Joint CEO)           Rosebank Towers                         
      Ruben Moggee (Joint CEO)            15 Biermann Avenue                      
                                          Rosebank, 2196                          
      Non-executive                                                               
                                          (Private Bag X9000, Saxonwold, 2132)    
      Michael Mendelowitz                                                         
      Roberto Rossi                                                               
                                          Independent   auditors                  
      Independent non-executive                                                   
                                          PricewaterhouseCoopers Inc              
      Suresh Kana (Lead independent director)                                     
                                          (Practice number 901121)                
      Diane Radley                                                                
                                          4 Lisbon Lane                           
      Sharon Wapnick                                                              
                                          Waterfall City, Jukskei View, 2090      
      Megandra Naidoo                                                             
                                          (Private Bag X36, Sunninghill, 2157)    
      Company    secretary and                                                    
      registered  office                                                          
      Jerain Naidoo                                                               
      115 West Street, Sandown, Sandton,                                          
      Johannesburg, Gauteng, 2196                                                 
      (PO Box 41888, Craighall, 2024)                                             
      JSE  sponsor                                                                
      Investec Bank Limited                                                       
      (Registration number 1925/002833/06)                                        
      100 Grayston Drive                                                          
      Sandton, 2196                                                               
      (PO Box 785700, Sandton, 2146)

### [ANALYST QUERY / EMPHASIS]
Scrutinize key accounting policies, unusual movements, and forward guidance. This is one capture, not proof of whole-report coverage. Adjacent tables/footnotes may need verification.

### [SECTION READING RESPONSE / DETERMINATION]
> APPLICATION QUALIFICATION: DeepSeek ledger updates failed evidence validation. No existing question was resolved by this response. All prior questions remain open; any resolution claim in the narrative is unverified. Only valid new questions were retained.

### 1. Answers to Stored Questions for This Section

**Q-3df04995ff2f4c6a [high] [partial] — Extract headline financial metrics and confirm page offset**
- **Status**: `Resolved` (for the D003 scope of this question)
- **Answer & evidence**: Page offset re-confirmed: printed page 32 = physical p. 34; printed 33 = physical 35; printed 34 = physical 36; printed 35 = physical 37 (offset = physical − 2). No headline advances/CLR/NIM/HEPS/DPS in this capture. Segment revenue captured: Nutun SA R1,047m (H1 2026) vs R882m (H1 2025) vs R1,790m (FY2025); Nutun International R552m vs R557m vs R1,094m; Group total revenue R1,599m vs R1,439m vs R2,884m `[D003, physical PDF p. 36]`. Note: Group total revenue R1,599m here is the CODM "gross revenue + revenue from purchased book debts" basis, not the IFRS R711m revenue line — a definitional difference to reconcile.

**Q-64b704d06ed84c90 [medium] — Capture statement of financial position and income statement values**
- **Status**: `Partially resolved (remainder stays open for D003/D004)`
- **Answer & evidence**: No statement of financial position or IFRS income statement lines in this capture. Only the FY2025 audited segment summarised income statement is present `[D003, physical PDF p. 34]`: FY2025 Group revenue R1,435m; revenue from PBD R1,449m (eliminated); net income from PBD R244m; total opex & cost of revenue R(1,795)m; amortisation of PBD R(767)m; operating costs R(1,063)m; other income R69m; equity accounted loss R(48)m; non-operating profit R38m; net finance charge R(91)m; loss before tax R(148)m; tax credit R35m; loss from continuing ops R(113)m; discontinued loss R(125)m; total loss R(238)m. Gross advances, ECL allowance and Stage 1/2/3 split remain absent.

**Q-336536b6077249e3 [medium] — Capture cash flow statement items**
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: No cash flow statement in this capture. Indirect PBD cash data from footnote 4 `[D003, physical PDF p. 35]`: FY2025 PBD amortisation R767m = CAEIR imputed interest revenue R683m − impairment loss R199m − net cash collections R1,197m + fair value movements R114m + cash collections R168m. No gross write-offs, recoveries, debt raised/repaid or dividends disclosed here.

**Q-995d98c7cabc40ba [high] [partial] — Statement lines / ECL / Stage split / audit status**
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: Still no advances, ECL allowance or Stage 1/2/3 split. Audit status now clarified: the FY2025 comparatives in the segment report are explicitly labelled "Audited" `[D003, physical PDF p. 34, p. 35]`, while H1 2026 columns are labelled "Unaudited" `[D003, physical PDF p. 36]`. Independent auditors are PricewaterhouseCoopers Inc (practice number 901121) `[D003, physical PDF p. 37]`. No review-opinion statement appears in this capture.

**Q-add37e0058a74df2 [low] [partial] — Audit/review status and core-earnings add-backs**
- **Status**: `Partially resolved (remainder stays open)`
- **Answer & evidence**: FY2025 core reconciliation add-backs itemised `[D003, physical PDF p. 35]`: exceptional items R68m (transaction costs R29m, tax impact R(8)m, impairment of associate R47m); core continuing loss R(45)m; then tax R(27)m, D&A R163m, PBD amortisation R767m, equity accounted loss R1m, net finance charge R445m → core EBITDA R1,304m. Discontinued: settlement fee R176m, profit on disposal R(100)m, tax R29m, transaction costs R16m, tax R(3)m → core discontinued loss R(7)m. No H1 2026 core reconciliation in this capture; "accelerated items" add-backs not shown here.

**Q-47cc084806ec463d [low] — Physical p. 38 purpose**
- **Status**: `Partially resolved (remainder stays open for D004)`
- **Answer & evidence**: Physical p. 37 (printed 35) is the Administration page (company information, directors, advisers, auditors, sponsor) `[D003, physical PDF p. 37]`. Physical p. 38 remains unread; carry forward.

**Q-3df04995ff2f4c6a sub-item — Mobalyz / SAT loan claims settlement**
- **Status**: `Resolved`
- **Answer & evidence**: Footnote 1 `[D003, physical PDF p. 35]`: as part of the Mobalyz Group Holdings disposal, and in return for a 3-year commitment from main bank funders to renew/revolve all facilities maturing before 30 Sep 2027, Nutun agreed 90% of dividends received from Nutun Holdings would be used to acquire SA Taxi Holdings ("SAT") loan claims to R200m (if settled by 26 Nov 2026) or R250m (post that date). Nutun satisfied this via a full and final settlement of R176m; no longer required to acquire SAT loan claims; no further amounts outstanding. This is a **funding-covenant-linked contingent obligation** now extinguished — relevant to liquidity/covenant assessment.

**Q-3df04995ff2f4c6a sub-item — Subsequent events / going concern**
- **Status**: `Resolved`
- **Answer & evidence**: Going concern: directors have no reason to believe group will not continue; assessment covered business-model relevance, nature of primary assets, cash flows and balance sheet `[D003, physical PDF p. 36]`. Subsequent events: directors aware of no material IAS 10 events between period end and approval date `[D003, physical PDF p. 36]`. Note: this is a bare statement with no quantified liquidity/covenant support — flagged below.

**Q-3df04995ff2f4c6a sub-item — TC Global Finance associate impairment**
- **Status**: `Partially resolved`
- **Answer & evidence**: Footnote 2 `[D003, physical PDF p. 35]`: R47m impairment of financial assets held by TC Global Finance, treated as exceptional in FY2025. Equity accounted loss FY2025 R48m (R1m adjusted for exceptional items). Carrying value and residual exposure still not disclosed here.

**Q-3df04995ff2c46d8 — Core earnings definition / exceptional items**: Confirmed via footnote 2 and the segment reconciliation above; no further detail on "once-off transaction costs, put/call adjustments" in this capture.

---

### 2. Footnote & Footnote Commentary Analysis

**Footnote 1 (p.36, physical) — SA "Settlement" footnote (p.35 capture):** The R176m settlement fee is a **cash cost to extinguish a funding-linked contingent obligation** (SAT loan-claim acquisition). It is classified as an exceptional item in discontinued operations and excluded from core discontinued loss (R(7)m). Forensic point: the obligation was tied to a **3-year bank facility renewal commitment to 30 Sep 2027** — this is a covenant/liquidity signal. The R176m cash outflow must be traced in the cash flow statement (not in this capture) and the extinguishment confirmed as full and final (footnote states "no further amounts outstanding").

**Footnote 2 (p.35) — TC Global Finance impairment R47m:** Treated as exceptional and added back to core earnings. This is a **credit-quality signal on the associate's loan book**; the add-back means core EBITDA R1,304m is flattered by R47m of genuine credit losses at the associate. Must verify whether further impairment risk remains (carrying value not disclosed).

**Footnote 3 (p.35) — Tax expense adjusted for tax on exceptional items:** Core tax R(27)m vs IFRS tax credit R35m. The reconciliation bridges a **tax credit in IFRS to a tax expense in core** — verify the deferred tax asset recognition basis (DTA R173m per earlier capture) is not being propped by exceptional-item tax credits.

**Footnote 4 (p.35) — PBD amortisation R767m decomposition:** CAEIR imputed interest R683m − impairment R199m − net cash collections R1,197m + FV movements R114m + cash collections R168m = R767m. **Arithmetic check:** 683 − 199 − 1,197 + 114 + 168 = **−431m**, not +767m. The sign convention in the footnote is internally inconsistent with the stated R767m amortisation charge (which is a cost, shown as R(767)m in the income statement). This is a **material reconciliation anomaly** — the footnote as printed does not arithmetically bridge to R767m under any obvious sign convention. Flag as high-priority verification (see Q below). Also note impairment R199m FY2025 vs R167m H1 2026 vs R173m H1 2025 — the FY2025 full-year impairment is only modestly above the H1 2025 half-year figure, implying a **much lower H2 FY2025 impairment charge (~R26m)** — possible under-provisioning in H2 FY2025 or a large re-estimate gain; must be tested.

**Footnote 5 (p.35) — Equity accounted loss adjusted for exceptional items:** R48m IFRS vs R1m core — the R47m TC Global impairment is stripped out. Confirms associate losses are being normalised away from core.

**Footnote * (p.35) — Core EBITDA definition:** "non-IFRS measure... represents management's view of operating cash flows." Forensic point: core EBITDA R1,304m is **before** PBD amortisation R767m and finance costs — i.e., it excludes the actual cash cost of acquiring and running down the purchased book. "Management's view of operating cash flows" is a promotional framing; the true operating cash generation must be tested against the cash flow statement.

**Footnote * (p.36) — Revenue definition:** "Revenue comprises gross revenue as presented on the income statement, and revenue from purchased book debts as presented in the CODM view." This confirms the R1,599m "total revenue" is a **non-IFRS aggregation** (IFRS revenue R711m + PBD gross revenue R1,449m less eliminations). Do not use R1,599m as an IFRS revenue forecast input.

**Going concern (p.36) and Subsequent events (p.36):** Bare, unquantified statements. No covenant headroom, liquidity reserve or maturity-wall support is provided in the going-concern paragraph — a **qualification gap** given R1,196m (approx.) of borrowings payable within 12 months noted in earlier captures. Must be tested against the funding note.

**Administration page (p.37):** Confirms PwC as independent auditors, Investec as JSE sponsor, year-end 30 September, JSE listing 7 June 2012. No audit qualification or emphasis-of-matter disclosed on this page.

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| N1 | High | D003 (remaining pages 8–33) / D004 | Footnote 4 PBD amortisation bridge does not arithmetically sum to R767m (683−199−1,197+114+168 = −431m) `[D003, p. 35]` | Locate note 1.1 (PBD) and note 1.2 (other financial assets) full text; reconcile each component sign and confirm the R767m amortisation charge; identify missing bridge item | If the bridge is misstated, the PBD impairment/amortisation run-rate and CLR forecast are unreliable |
| N2 | High | D003 (remaining) / D004 | FY2025 impairment R199m vs H1 2025 R173m implies H2 FY2025 charge ~R26m `[D003, p. 35]` | Locate PBD ECL/impairment note: H2 FY2025 gross charge vs re-estimate gain; confirm whether H2 was under-provisioned or a large re-estimate gain was booked | Tests whether impairment is being smoothed; drives CLR forecast |
| N3 | High | D003 (remaining) / D004 | R176m SAT loan-claim settlement tied to 3-year bank facility renewal to 30 Sep 2027 `[D003, p. 35]` | Locate cash flow statement (settlement outflow) and funding note (facility renewal terms, covenant reset); confirm full-and-final extinguishment | Liquidity/covenant risk; R176m cash outflow timing |
| N4 | High | D003 (remaining) / D004 | TC Global Finance R47m impairment added back to core; carrying value not disclosed `[D003, p. 35]` | Locate associate note: carrying value, residual impairment risk, share of loss H1 2026 | Core EBITDA quality; further impairment risk |
| N5 | Medium | D003 (remaining) / D004 | Core EBITDA R1,304m defined as "management's view of operating cash flows" but excludes PBD amortisation R767m and finance costs `[D003, p. 35]` | Locate cash flow statement: reconcile core EBITDA to actual operating cash flow; quantify PBD amortisation and finance cost cash impact | Earnings-quality / cash conversion test |
| N6 | Medium | D003 (remaining) / D004 | Group "total revenue" R1,599m (CODM) vs IFRS revenue R711m — definitional gap `[D003, p. 36]` | Locate note 4.1 revenue disaggregation: reconcile CODM gross revenue + PBD revenue to IFRS revenue line | Prevents double-counting revenue in forecast |
| N7 | Medium | D003 (remaining) / D004 | Going concern and subsequent events statements are bare/unquantified `[D003, p. 36]` | Locate funding note and going-concern support: covenant headroom, liquidity reserves, maturity wall vs R1,196m within 12 months | Liquidity/refinancing risk to forecast |
| N8 | Medium | D003 (remaining) / D004 | Australia revenue collapse R74m→R27m; UK growth R259m→R303m `[D003, p. 36]` | Locate segment/geographic commentary: contract wins/losses, FX, subsequent events | International revenue base sustainability |
| N9 | Low | D004 | Physical p. 38 unread `[D003, p. 37]` | Confirm p. 38 content (administration vs financial disclosure) | Completeness of capture |
| N10 | Medium | D003 (remaining) / D004 | Core tax R(27)m vs IFRS tax credit R35m; DTA R173m `[D003, p. 35]` | Locate tax note: current/deferred split, DTA recoverability, tax on exceptional items | Tax forecast and DTA impairment risk |

---

### 5. Baseline Forecast Inputs Captured Here

| Metric | H1 FY2026 (Unaudited) | H1 FY2025 (Unaudited) | FY2025 (Audited) | Source |
|---|---|---|---|---|
| Nutun SA revenue | R1,047m | R882m | R1,790m | D003 p.36 |
| Nutun International revenue | R552m | R557m | R1,094m | D003 p.36 |
| — UK | R303m | R259m | R525m | D003 p.36 |
| — US | R212m | R224m | R428m | D003 p.36 |
| — Australia | R27m | R74m | R127m | D003 p.36 |
| — Other | R10m | – | R14m | D003 p.36 |
| Group total revenue (CODM basis) | R1,599m | R1,439m | R2,884m | D003 p.36 |
| Group revenue (IFRS, per earlier capture) | R711m | R745m | — | D002 |
| FY2025 Group revenue (segment) | — | — | R1,435m | D003 p.34 |
| FY2025 net income from PBD | — | — | R244m | D003 p.34 |
| FY2025 PBD amortisation | — | — | R(767)m | D003 p.34 |
| FY2025 operating costs | — | — | R(1,063)m | D003 p.34 |
| FY2025 net finance charge | — | — | R(91)m | D003 p.34 |
| FY2025 loss before tax | — | — | R(148)m | D003 p.34 |
| FY2025 tax credit | — | — | R35m | D003 p.34 |
| FY2025 loss from continuing ops | — | — | R(113)m | D003 p.34 |
| FY2025 discontinued loss | — | — | R(125)m | D003 p.34 |
| FY2025 total loss | — | — | R(238)m | D003 p.34 |
| FY2025 core continuing loss | — | — | R(45)m | D003 p.35 |
| FY2025 core EBITDA | — | — | R1,304m | D003 p.35 |
| FY2025 core discontinued loss | — | — | R(7)m | D003 p.35 |
| FY2025 exceptional items | — | — | R68m | D003 p.35 |
| FY2025 TC Global impairment | — | — | R47m | D003 p.35 |
| FY2025 SAT settlement fee | — | — | R176m | D003 p.35 |
| FY2025 PBD CAEIR imputed interest | — | — | R683m | D003 p.35 |
| FY2025 PBD impairment loss | — | — | R199m | D003 p.35 |
| FY2025 PBD net cash collections | — | — | R1,197m | D003 p.35 |
| FY2025 PBD FV movements | — | — | R114m | D003 p.35 |
| FY2025 PBD cash collections | — | — | R168m | D003 p.35 |
| H1 FY2026 PBD impairment (earlier capture) | R167m | R173m | — | D002 |
| Independent auditors | PricewaterhouseCoopers Inc (901121) | — | — | D003 p.37 |
| Year end | 30 September | — | — | D003 p.37 |

---

### 6. Next Section to Capture

**`D003` remaining pages (physical pp. 8–33)** — specifically the statement of financial position (p.8), income statement, cash flow statement (p.12), and the notes containing **note 1.1 (PBD), note 1.2 (other financial assets), note 4.1 (revenue disaggregation), the ECL/impairment note, funding/borrowings note, and tax note**. These will resolve **N1, N2, N3, N4, N5, N6, N7, N9, N10** and the outstanding stored questions on advances/ECL staging, funding covenants, and the PBD amortisation bridge. If the remaining D003 pages are unavailable, capture **`D004` (physical p. 38)** to close N9 and confirm no further financial disclosure.

================================================================================
## SECTION 9: [D004] Source coverage remainder
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section D004 | [AFS] physical page 38 | area selection | Commentary ---
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                     nutun.com                                    
                               115 West Street, Sandown, Sandton,                 
                                 Johannesburg, Gauteng 2196                       
                                (PO Box 41888, Craighall, 2024)

### [ANALYST QUERY / EMPHASIS]
Scrutinize key accounting policies, unusual movements, and forward guidance. This is one capture, not proof of whole-report coverage. Adjacent tables/footnotes may need verification.

### [SECTION READING RESPONSE / DETERMINATION]
### 1. Answers to Stored Questions for This Section

- **Q-47cc084806ec463d**:
- **Status**: `Resolved`
- **Answer & evidence**: Physical p. 38 contains only corporate/administration information — the company website (`nutun.com`) and registered/head office address (115 West Street, Sandown, Sandton, Johannesburg, Gauteng 2196; PO Box 41888, Craighall, 2024) `[D004, physical PDF p. 38]`. No financial disclosures, notes, or figures are present. Page purpose established as administration/contact information; no financial content to capture.

*(No other stored questions relate to this section's evidence — all are carried forward in Section 4.)*

### 2. Footnote & Qualification Deep-Dive

No footnotes, table notes, or qualifications appear in this section. The page contains only the company website and postal/physical address `[D004, physical PDF p. 38]`. Nothing here alters any headline or table number, and no verification of accounting policy, ECL staging, write-off, or covenant terms is possible from this capture.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
|---|---|---|---|---|---|
| 1 | Low | D003 (Primary financial statements, pp. 8–37) | p. 38 is administration only; no financial content `[D004, p. 38]` | Confirm no financial notes/disclosures were omitted between the last note page and p. 38; verify the document ends at the financial statements/notes with no additional annexures | Confirms completeness of the evidence base for the forecast model |

### 5. Baseline Forecast Inputs Captured Here

None — p. 38 contains no financial figures (administration/contact information only).

### 6. Next Section to Capture

`D003` (Primary financial statements, physical pp. 8–37) — the substantive financial statements and notes that will resolve the bulk of the open ledger (Q-995d98c7cabc40ba, Q-64b704d06ed84c90, Q-336536b6077249e3, Q-019095eae85848d1, Q-0ada68da08fa49fc, Q-5e16f0ada73840c8, Q-d999efdf22e5453b, Q-19a3c1172f494459, and related ECL/funding questions).

## Stage 2 handoff: unresolved material dependencies
List material FAIL/NOT VERIFIED claims with source pages, calculations and evidence needed. Carry them forward explicitly; do not declare a 99% confidence baseline. Stage 2 must withhold valuation while a material dependency remains unresolved. Do not produce a target or recommendation in Stage 1.