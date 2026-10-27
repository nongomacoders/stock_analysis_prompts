# STAGE 1: INDEPENDENT COGNITIVE AUDIT VIA SEQUENTIAL EXTRACTION & QUESTION LEDGER
**Target Asset:** Nutun Limited (NTU)  
**Sector:** Consumer_lending  
**Primary Document:** `nutunlimitedcondensedconsolidatedafs31march2026.pdf` (Integrated Annual Report [IAR] — 2 sections)  
**Input Mode:** Sequential Forensic Working Paper & Dynamic Questions Ledger (No PDF Attached)  
**Task Directive:** Forensic Reasoning, Conflict Reconciliation & Post-Balance-Sheet Determinations (No Full Forward Valuation Model Required)

---

### INSTRUCTIONS FOR FORENSIC AUDITOR (LLM):
You are acting as an independent **Managing Director and Senior Forensic Credit & Lending Accounting Auditor**. 
You have been provided with the complete, chronological working paper compiled during a section-by-section forensic capture of Nutun Limited's financial disclosures (2 total sections across primary report and companion disclosures).

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
| `CONSUMER-LENDING-ECL-PBD-ERC` | **CONSUMER_LENDING** | **Consumer Lending IFRS 9 Stage Migration & Purchased Book Debt (PBD) Amortization** | Reconcile gross loan book and Purchased Book Debt (PBD) carrying values against Estimated Remaining Collections (ERC), separating cash collections applied to revenue yield vs principal amortization and Stage 1/2/3 ECL coverage. |

---

## MASTER WORKING PAPER: CUMULATIVE OPEN QUESTIONS LEDGER
> **Cognitive Audit Anchor:** The authoritative ledger below consolidates all priority questions, forensic hypotheses, and cross-reference resolutions developed across the entire disclosure set. Use this ledger as your reference matrix when auditing the sequential section extractions that follow.

## OPEN QUESTIONS LEDGER — Nutun H1 2026 (updated after Primary Financial Statements, pp. 8–32)

### Target: Highlights / p.3
- Q1 [High]: Recompute all Change % on p.3 — sign errors detected (opex "5%" vs −5.2%; amortisation "(41%)" vs +41.5%; Intl opex "(2%)" vs +1.9%). Confirm correct direction of every KPI line. [Underlying absolutes confirmed from pp. 9, 30; p.3 signs still open]

### Target: PBD/RTC note / accounting policies
- Q3 [High]: Quantify split of R175m amortisation increase between portfolio ageing/volume vs change in forward-looking macro/EIR assumptions. CAEIR rose to 19.2% from 17.9%; precise split not disclosed. [Partially resolved]
- Q6 [Medium]: Confirm ERC (R8,366m) estimation methodology and discount rate; check whether PBD/RTC carrying value (R4,489m) is impairment-tested; obtain portfolio ageing profile. [PBD carrying R4,489m confirmed; ERC not referenced; ageing not disclosed]
- Q13 [High]: Reconcile PBD fair value R3,845m to 18.50% market discount rate vs 19.2% CAEIR; management states fair value ≈ carrying value — verify cash flow risk adjustment. [New]
- Q14 [High]: Verify whether 12-month rolling ECL horizon is appropriate for POCI lifetime ECL; obtain tail beyond 12 months and vintage loss curves. [New]
- Q19 [Medium]: Quantify base-case vs actual collections; obtain vintage loss curves; verify payer drop-off rate behind R431m cumulative impairment gain reduction. [New]

### Target: Credit risk note
- Q4 [High]: Extract collections-vs-ERC actuals, vintage loss curves, DPD buckets, and coverage/impairment on PBD/RTC carrying value. Test achievability of R8,366m ERC. [Collections R773m gross / R728m net confirmed; coverage 12.6% confirmed; ERC and DPD/vintage still open]
- Q15 [High]: Verify SICR policy and 30-DPD backstop; check whether 90-DPD threshold for trade receivables ECL is a relaxation vs FY2025. [New]

### Target: Debt / funding note
- Q5 [High]: Obtain covenant ratios (interest cover, LTV, net debt/EBITDA, ABS triggers), headroom, maturity wall, facility types. Quantify "~R0.8bn unutilised facilities". [Maturity wall R1,396m <12m / R2,620m >12m confirmed; undrawn overdraft R475m confirmed; covenants and R0.8bn claim still open]
- Q12 [High]: Obtain pledge agreement terms, covenant ratios, ABS performance triggers, and unencumbered asset base — 100% of PBD (R3,845m) plus trade receivables and cash pledged. [New]
- Q18 [High]: Verify total undrawn facilities across all debt types (not just overdraft R475m); check R0.8bn claim source. [New]
- Q24 [Medium]: Verify rate sensitivity; check fixed vs floating split (all floating per note); explain R365m fair value swing in 6 months. [New]

### Target: Cash flow statement / segment note
- Q7 [Medium]: Reconcile EBITDA (R710m SA) to operating cash flow; check cash conversion, working capital, and actual PBD acquisition cash outflows (R382m confirmed). [Resolved]
- Q17 [High]: Build full EBITDA-to-cash bridge: Core EBITDA R790m vs operating cash outflow R(111)m — R901m gap; interest paid R225m, PBD additions R382m, WC R(23)m, tax R2m. [New]
- Q16 [High]: Reconcile CODM revenue R888m − IFRS net income R69m to amortisation R597m; footnote components (383+167+728+30+116) do not arithmetically reconcile. [New]

### Target: Segmental note 7 / revenue note
- Q8 [Medium]: Check FX sensitivity, hedge accounting, and DTI incentive income recognised; verify International margin drivers. [FX contracts confirmed; DTI and hedge accounting still open]
- Q9 [Medium]: Verify client concentration (top-10 % of revenue) and sustainability of R159m agency commission line after client count fell 23→20. [R159m confirmed; concentration still open]
- Q20 [Medium]: Obtain top-10 client % of revenue; verify SA agency commission sustainability. [New]
- Q21 [Medium]: Verify SA funding cost allocation and transfer pricing — SA PBT R(123)m vs International R31m. [New]

### Target: Currency risk note
- Q22 [Medium]: Verify hedge accounting treatment, effectiveness, and MTM for USD/GBP FX contracts. [New]

### Target: Fair value note
- Q23 [Medium]: Verify Level 3 FV gain drivers; R30m vs R74m Mar-25 vs R114m FY25 — declining. [New]

### Target: Board / governance / related-party note
- Q10 [Low]: Check for related-party transactions and key-person risk following Executive Chairman and joint CEO board appointments (1 Jan 2026). [Still open]
- Q25 [Low]: Check for related-party transactions and key-person risk. [New — duplicate of Q10]

### Target: Share capital note
- Q27 [Low]: Verify market price vs book value (~R6.90/share); treasury shares acquired at R1/share. [New]

### Target: FY2026 audited AFS / subsequent events
- Q11 [Low]: H1 2026 is unaudited and unreviewed. At FY2026 audit, check for restatements to PBD/RTC carrying value, amortisation, CAEIR, or core-earnings adjustments. [Still open]
- Q26 [Low]: Check for restatements to PBD carrying value, amortisation, CAEIR, or core earnings at FY2026 audit. [New — duplicate of Q11]

---

# THE SEQUENTIAL EXTRACTION & WORKING PAPER DOSSIER (2 SECTIONS)

================================================================================
## SECTION 1: [unmapped] Highlights
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section unmapped | [AFS] physical page 3 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 4 | area selection | Commentary ---
                                                                                  
                                                                                  
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
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  

--- Section unmapped | [AFS] physical page 5 | area selection | Commentary ---
                                                                                  
                                                                                  
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
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  

--- Section unmapped | [AFS] physical page 6 | area selection | Commentary ---
                                                                                  
                                                                                  
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
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  

--- Section unmapped | [AFS] physical page 7 | area selection | Commentary ---
                                                                                  
                                                                                  
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
Scrutinize key accounting policies, unusual movements, and forward guidance.

### [SECTION READING RESPONSE / DETERMINATION]
### 1. Answers to Stored Questions for This Section
*(No stored questions were supplied — first section capture. Omitted per workflow rule.)*

### 2. Footnote & Qualification Deep-Dive

- **"The financial information on which this announcement is based has not been reviewed and reported on by Nutun Limited's auditors"** `[unmapped, physical PDF p. 6]` — This is a material qualification. All H1 2026 figures (revenue, EBITDA, PBD/RTC carrying values, amortisation, covenant compliance) are **unaudited and unreviewed**. Any forecast built on these numbers carries unverified-basis risk; the FY2026 audited AFS must be checked for restatement of PBD/RTC carrying values and amortisation.
- **"Any forecast financial information has not been reviewed or reported on by the company's auditors"** `[unmapped, physical PDF p. 6]` — Forward-looking statements (book-buying objectives, AI-driven margin enhancement, "higher profitability in future years") are unverified management assertions, not audited guidance.
- **"accelerated amortisation driven by forward looking macro-economic assumptions including an elevated interest rate forecast relative to our expectations"** `[unmapped, physical PDF p. 5]` — This is the key accounting-policy signal in the capture. PBD/RTC amortisation rose 41% to R597m (vs R422m) on cost of acquisitions up 51% to R410m. Management attributes part of the increase to a **forward-looking macro assumption change (higher interest rate forecast)** — i.e., a valuation-model input change, not purely portfolio ageing. This must be reconciled: how much of the R175m amortisation increase is (a) volume/ageing vs (b) assumption change? If assumption-driven, it is a non-cash P&L hit that could reverse — or could signal the embedded discount rate / EIR assumptions were previously too optimistic.
- **"Portfolio amortisation costs increased by 41%... driven by portfolio ageing and macro-economic factors linked to interest rates, inflation and consumer health & payment behaviour"** `[unmapped, physical PDF p. 4]` — Consumer payment behaviour deterioration is flagged qualitatively but **no delinquency, roll-rate, vintage or coverage data is disclosed in this capture**. This is the single largest gap for credit-risk assessment.
- **"funding covenants are comfortably complied with and have approximately R0.8 billion in unutilised facilities as at 31 March 2026"** `[unmapped, physical PDF p. 5]` — "Comfortably complied" is unquantified. No covenant headroom ratios, no maturity profile, no ABS trigger levels disclosed here. Must be verified against debt note.
- **"cash dividends have been suspended, with no cash dividend being declared"** `[unmapped, physical PDF p. 5]` — Consistent with continuing core loss; DPS = 0. Confirms no payout in forecast.
- **Core earnings reconciliation notes** `[unmapped, physical PDF p. 6]` — Note 1 (transaction costs, FY2025 funding restructuring) and Note 2 (impairment of financial assets held by associate TC Global Finance, R47m in H1 2025) are clean prior-period adjustments; H1 2026 has **zero** core adjustments, meaning core loss = headline loss = basic loss = R63m. No add-backs flattering the current period.
- **Discontinued operations** `[unmapped, physical PDF p. 6]` — Nutun Transact disposal (FY2025) fully washed through; H1 2026 discontinued = nil. Forecast should model continuing operations only.
- **No footnote markers (`[^1]`, `*`) with missing definitions were detected in this capture** — the table on p. 3 carries no footnote markers. However, the p. 3 table's "Change %" column contains a **sign/label inconsistency** (see Q1 below) that functions as an unlabelled qualification.

**Arithmetic checks on supplied numbers:**
- Revenue 1,610 − Operating costs 820 = **EBITDA 790** ✓ (ties).
- Segment EBITDA: SA 710 + Intl 80 = **790** ✓.
- Segment revenue: 1,051 + 559 = **1,610** ✓.
- Segment opex: 341 + 479 = **820** ✓.
- EBITDA 790 − PBD/RTC amortisation 597 − net interest 216 = **−23**, but reported continuing core loss = **−63**. **Unexplained R40m gap** (likely D&A, tax, NCI, or other costs not shown in this extract) — flagged as Q2.
- PBD/RTC: Carrying value 4,489 vs Estimated remaining collections 8,366 → **implied embedded uplift 86%** (ERC/CV = 1.86x). H1 2025: 7,808/4,353 = 1.79x. Uplift widened — consistent with management's "improving embedded discount rate" claim, but also raises ERC-estimate reliance risk.
- Cost of acquisitions 410 vs amortisation 597 → amortisation running **1.46x** current-period acquisition spend; book is being consumed faster than replenished in P&L terms.
- Change % column anomalies: Operating costs "5%" but 820 vs 865 = **−5.2%** (sign error); PBD/RTC amortisation "(41%)" but 597 vs 422 = **+41.5%** (sign/parenthesis error); Nutun International opex "(2%)" but 479 vs 470 = **+1.9%**. Treat all Change % signs on p. 3 as unreliable; use absolute values.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q1 | High | Segment note (note 7) / financial statements | Change % column sign errors on p. 3 (opex "5%" vs −5.2%; amortisation "(41%)" vs +41.5%; Intl opex "(2%)" vs +1.9%) `[unmapped, p. 3]` | Recompute every Change % from absolute H1 2026 vs H1 2025 figures in note 7; confirm correct direction of each line | Mis-signed growth rates corrupt any trend-based forecast |
| Q2 | High | Group income statement / note on EBITDA-to-loss bridge | EBITDA 790 − amortisation 597 − net interest 216 = −23, but core loss reported −63 (R40m unexplained) `[unmapped, pp. 3–4]` | Locate the R40m: D&A, tax, NCI, associate losses, or other opex not in the KPI table; reconcile EBITDA to core loss line by line | Forecast P&L bridge must be complete; hidden R40m cost base changes margin math |
| Q3 | High | PBD/RTC note / accounting policies | "Accelerated amortisation driven by forward looking macro-economic assumptions including an elevated interest rate forecast" `[unmapped, p. 5]` | Quantify split of the R175m amortisation increase between (a) portfolio ageing/volume and (b) change in macro/EIR assumptions; check EIR and discount-rate methodology vs FY2025 | Determines whether amortisation is a recurring cash-equivalent cost or a reversible non-cash assumption hit — directly drives core earnings forecast |
| Q4 | High | PBD/RTC note / credit risk note | "Consumer health & payment behaviour" cited as amortisation driver; no delinquency, roll-rate, vintage or coverage data disclosed `[unmapped, p. 4]` | Extract collections-vs-ERC actuals, vintage loss curves, DPD buckets, and any impairment/coverage on PBD/RTC carrying value of R4,489m | Core credit-risk assessment of the principal lending book; tests whether ERC of R8,366m is achievable |
| Q5 | High | Debt / funding note | "Funding covenants comfortably complied with; ~R0.8bn unutilised facilities" — unquantified `[unmapped, p. 5]` | Obtain covenant ratios (interest cover, LTV, net debt/EBITDA, ABS triggers), headroom, maturity wall, and facility types (RCF/syndicated/ABS) | Funding covenant tightness is a going-concern and forecast-flexibility input |
| Q6 | Medium | PBD/RTC note | Carrying value R4,489m vs ERC R8,366m (1.86x uplift); acquisitions R410m vs amortisation R597m `[unmapped, p. 3]` | Confirm ERC estimation methodology, discount rate, and whether carrying value is subject to impairment testing; check portfolio ageing profile | ERC is the revenue backbone; overstatement inflates forward collections forecast |
| Q7 | Medium | Cash flow statement | "Strong growth in Nutun South Africa's cash generation" (EBITDA R710m) but group core loss R63m `[unmapped, pp. 4–5]` | Reconcile EBITDA to operating cash flow; check cash conversion, working capital, and actual PBD acquisition cash outflows (R593m FY2025 H2 + R382m H1 2026) | Cash generation claim underpins liquidity forecast; EBITDA ≠ cash |
| Q8 | Medium | Segmental note 7 | Nutun International EBITDA −15% to R80m on R46m FX impact; Rand strength and DTI incentive uncertainty flagged `[unmapped, pp. 4–5]` | Check FX sensitivity disclosure, hedge accounting, and any DTI incentive income recognised in revenue/other income | International margin forecast hinges on FX and incentive assumptions |
| Q9 | Medium | Revenue note / agency segment | Agency commission revenue −15% to R159m on "strategic shift to larger mandates, fewer clients"; client count SA 23→20 `[unmapped, pp. 3–4]` | Verify client concentration (top-10 % of revenue) and sustainability of the R159m agency line | Client concentration risk to revenue forecast |
| Q10 | Low | Related-party / board note | Executive Chairman appointment (Jonathan Jawno) and joint CEO board appointments 1 Jan 2026; Ian Kirk and Albertinah Kekana resigned `[unmapped, p. 7]` | Check for related-party transactions, key-person risk, and any governance flags in the board/governance section | Governance stability affects forecast risk premium, not core numbers |
| Q11 | Low | Subsequent events / FY2026 AFS | Entire H1 2026 result is unaudited and unreviewed `[unmapped, p. 6]` | At FY2026 audited AFS, check for restatements to PBD/RTC carrying value, amortisation, or core-earnings adjustments | Unaudited basis risk to all baseline inputs |

### 5. Baseline Forecast Inputs Captured Here

| Metric (Rm unless stated) | H1 2026 | H1 2025 | Change |
| --- | --- | --- | --- |
| Revenue and other income | 1,610 | 1,480 | +8.8% |
| — Nutun South Africa | 1,051 | 917 | +14.6% |
| — Nutun International | 559 | 563 | −0.7% |
| Operating costs | 820 | 865 | −5.2% |
| — Nutun South Africa | 341 | 395 | −13.7% |
| — Nutun International | 479 | 470 | +1.9% |
| EBITDA | 790 | 615 | +28.5% |
| — Nutun South Africa | 710 | 522 | +36.0% |
| — Nutun International | 80 | 93 | −14.0% |
| PBD & RTC amortisation | 597 | 422 | +41.5% |
| Net interest cost | 216 | 233 | −7.3% |
| Continuing core loss | (63) | (71) | improved R8m |
| PBD/RTC cost of acquisitions | 410 | 272 | +50.7% |
| PBD/RTC carrying value | 4,489 | 4,353 | +3.1% |
| PBD/RTC estimated remaining collections | 8,366 | 7,808 | +7.1% |
| Clients — Nutun South Africa | 20 | 23 | −13.0% |
| Clients — Nutun International | 36 | 35 | +2.9% |
| Nutun International billable seats | 2,491 | 2,069 | +20.4% |
| Core loss per share (cents) | (8.1) | (9.1) | — |
| Headline loss per share (cents) | (8.1) | (17.2) | — |
| Basic loss per share (cents) | (8.1) | (8.2) | — |
| DPS (cents) | 0 | 0 | suspended |
| Unutilised facilities | ~R0.8bn | n/a | — |
| PBD collections (SA) | 773 | 604 (implied) | +28% |
| RTC revenue (SA) | 116 | 91 (implied) | +27% |
| Agency commission & fee revenue (SA) | 159 | 187 (implied) | −15% |
| Other income (SA) | 4 | 35 (implied) | −R31m |
| Net interest cost (SA) | 203 | 218 (implied) | −7% |
| FX adverse impact (Intl revenue) | 27 | — | — |
| FX adverse impact (Intl EBITDA) | 46 | — | — |

*Derived: implied ERC/CV uplift 1.86x (H1 2026) vs 1.79x (H1 2025); amortisation/acquisition spend 1.46x; EBITDA-to-core-loss bridge gap R40m (unresolved — Q2).*

### 6. Next Section to Capture
**The PBD/RTC note and credit-risk note (and the segmental note 7)** — these will resolve **Q3, Q4, Q6** (amortisation assumption split, ERC methodology, delinquency/vintage/coverage data) and **Q1** (segment Change % recomputation). If the Report Map orders sections differently, capture the **debt/funding note** next to resolve **Q5** (covenant headroom and facility structure), as funding is the highest going-concern priority after the credit book.

================================================================================
## SECTION 2: [unmapped] Primary financial statements
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section unmapped | [AFS] physical page 8 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 9 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 10 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 11 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 12 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 13 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 14 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 15 | area selection | Financial note ---
                                                                                                                    
                                                                                                                    
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
                                                                                                                    
                                                                                                                    
                                                                                                                    
                                                                                                                    
                                                                                                                    
                                                                                                                    
                                                                                                                    
                                                                                                                    
                                                                                                                    
                                                                                                                    
                                                                                                                    
                                                                                                                    
                                                                                                                    
                                                                                                                    
                                                                                                                    
                                                                                                                    

--- Section unmapped | [AFS] physical page 16 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 17 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 18 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 19 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 20 | area selection | Financial note ---
                                                                                  
                                                                                  
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
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  

--- Section unmapped | [AFS] physical page 21 | area selection | Financial note ---
                                                                                  
                                                                                  
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
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  

--- Section unmapped | [AFS] physical page 22 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 23 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 24 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 25 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 26 | area selection | Financial note ---
                                                                                  
                                                                                  
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

--- Section unmapped | [AFS] physical page 27 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 28 | area selection | Financial note ---
                                                                                  
                                                                                  
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
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  

--- Section unmapped | [AFS] physical page 29 | area selection | Financial note ---
                                                                                  
                                                                                  
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
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  

--- Section unmapped | [AFS] physical page 30 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 31 | area selection | Table ---
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

--- Section unmapped | [AFS] physical page 32 | area selection | Table ---
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

### [ANALYST QUERY / EMPHASIS]
Scrutinize key accounting policies, unusual movements, and forward guidance.

### [SECTION READING RESPONSE / DETERMINATION]
### 1. Answers to Stored Questions for This Section

**Q1 [High]: Recompute all Change % on p.3 — sign errors detected. Confirm correct direction of every KPI line.**
- **Status**: `Partially resolved (remainder stays open for [Highlights / p.3])`
- **Answer & evidence**: The primary statements captured here (pp. 8–32) do not include the p.3 Highlights table, so the sign-error recomputation cannot be completed. However, the underlying absolute figures needed to recompute the KPI lines are now available and confirm the direction of travel: Revenue R711m vs R745m (down 4.6%); Gross profit from services R326m vs R393m (down 17.0%); Operating costs R445m vs R560m (down 20.5%); Amortisation of PBD R597m vs R422m (up 41.5%); Net finance charge R39m vs R52m (down 25.0%); Loss for the period R(63)m vs R(64)m. The amortisation direction (+41.5%) and opex direction (−20.5%) are confirmed from `[unmapped, physical PDF p. 9]` and `[unmapped, physical PDF p. 30]`. The p.3 percentage signs still require the Highlights section to verify.

**Q2 [High]: EBITDA 790 − amortisation 597 − net interest 216 = −23, but core loss = −63. Locate the unexplained R40m.**
- **Status**: `Resolved`
- **Answer & evidence**: The bridge is fully disclosed in the segment reconciliation `[unmapped, physical PDF p. 31]`. Core EBITDA R790m − amortisation of PBD R597m − net finance charge R216m − equity accounted loss R1m − depreciation & amortisation R68m + tax credit R29m = R(63)m. The "unexplained R40m" is the **R68m depreciation & amortisation** (of intangibles/PPE, distinct from PBD amortisation) net of the **R29m tax credit** (68 − 29 = 39 ≈ 40). No residual remains. Note: the earlier stored question's arithmetic omitted D&A and tax.

**Q3 [High]: Quantify split of R175m amortisation increase between portfolio ageing/volume vs change in forward-looking macro/EIR assumptions.**
- **Status**: `Partially resolved (remainder stays open for [PBD/RTC note / accounting policies])`
- **Answer & evidence**: Amortisation of PBD rose from R422m (H1 2025) to R597m (H1 2026), +R175m `[unmapped, physical PDF p. 30 vs p. 32]`. The segment footnote `[unmapped, physical PDF p. 31]` defines amortisation as CAEIR imputed interest R383m + impairment loss R167m + net cash collections R728m + fair value movements R30m + cash collections R116m. The increase is therefore driven by higher net cash collections (R728m vs R566m, +R162m) and higher CAEIR interest (R383m vs R333m, +R50m), partly offset by lower impairment (R167m vs R173m). The **CAEIR rose to 19.2% from 17.9%** `[unmapped, physical PDF p. 21]`, which mechanically inflates imputed interest and amortisation. The precise split between volume/ageing vs EIR/macro assumption change is **not disclosed** and remains open.

**Q4 [High]: Extract collections-vs-ERC actuals, vintage loss curves, DPD buckets, and coverage/impairment on PBD/RTC carrying value.**
- **Status**: `Partially resolved (remainder stays open for [Credit risk note / PBD/RTC note])`
- **Answer & evidence**: Collections: gross collections R773m, net collections R728m, collection costs R45m `[unmapped, physical PDF p. 13]`. PBD principal book gross carrying R3,414m, ECL allowance R431m, net R3,845m → **coverage 12.6%** `[unmapped, physical PDF p. 22–23]`. Segment split: Banking & specialised lending unsecured gross R2,371m / ECL R227m (9.6% coverage); Debt review gross R951m / ECL R141m (14.8%); Retail gross R46m / ECL R51m (>100%); Banking secured gross R46m / ECL R12m (26.1%) `[unmapped, physical PDF p. 23]`. **No DPD buckets or vintage loss curves are disclosed for PBD** (PBDs are POCI/Stage 3 by definition and managed on cash-collection basis, not DPD). ERC of R8,366m is **not referenced in this section** — remains open.

**Q5 [High]: Obtain covenant ratios, headroom, maturity wall, facility types. Quantify "~R0.8bn unutilised facilities".**
- **Status**: `Partially resolved (remainder stays open for [Debt / funding note])`
- **Answer & evidence**: Maturity wall: R1,396m payable within 12 months, R2,620m thereafter `[unmapped, physical PDF p. 14]`. Facility types: Notes (bullet/amortising, JIBAR+2.8–3.7%), Senior amortising (JIBAR+2.85–5.2%), Senior bullet (JIBAR+3–3.28%), Subordinated (JIBAR+4.6–5.0%), Revolving facility (Prime−0.25–0.35%) `[unmapped, physical PDF p. 15]`. **Undrawn overdraft facilities R475m** (vs R43m Mar-25, R136m Sep-25) `[unmapped, physical PDF p. 14]` — this is the only quantified "unutilised" figure; the "~R0.8bn" claim is **not corroborated** here (R475m undrawn overdraft only). **Covenant ratios and headroom are NOT disclosed** — remains open.

**Q7 [Medium]: Reconcile EBITDA (R710m SA) to operating cash flow; check cash conversion, working capital, and actual PBD acquisition cash outflows.**
- **Status**: `Resolved`
- **Answer & evidence**: Cash utilised by operations R(50)m; interest paid R(225)m; tax refunded R2m → operating cash before WC R(270)m `[unmapped, physical PDF p. 12]`. PBD acquisition cash outflow: **Additions R382m** `[unmapped, physical PDF p. 13]` (matches stored question's R382m H1 2026). Decrease in PBD (collections net) R182m inflow. Net cash utilised by operating activities R(111)m. Core EBITDA R790m vs operating cash outflow R(111)m — the gap is explained by interest paid R225m, PBD additions R382m, and WC movements. Cash conversion is **negative**; EBITDA is not converting to cash.

**Q8 [Medium]: Check FX sensitivity, hedge accounting, and DTI incentive income; verify International margin drivers.**
- **Status**: `Partially resolved (remainder stays open for [Segmental note 7 / revenue note])`
- **Answer & evidence**: FX: Nutun entered FX contracts to hedge USD/GBP receipts for International segment `[unmapped, physical PDF p. 25]`. Foreign currency assets R207m receivables + R27m bank balances; liabilities USD R10m, GBP R2m `[unmapped, physical PDF p. 26]`. Revenue by geography: SA R159m, Australia R27m, UK R303m, US R212m, Other R10m `[unmapped, physical PDF p. 17]`. International revenue R552m vs R557m (flat). **DTI incentive income and hedge accounting treatment not disclosed** — remains open.

**Q9 [Medium]: Verify client concentration (top-10 % of revenue) and sustainability of R159m agency commission line after client count fell 23→20.**
- **Status**: `Partially resolved (remainder stays open for [Segmental note 7 / revenue note])`
- **Answer & evidence**: SA commissions and fees R159m vs R188m (down 15.4%) `[unmapped, physical PDF p. 17]`. **Client concentration (top-10 %) is NOT disclosed** — remains open. The R159m line is confirmed but sustainability cannot be assessed without concentration data.

**Q10 [Low]: Check for related-party transactions and key-person risk.**
- **Status**: `Open (not addressed in this section)`
- **Answer & evidence**: No related-party note captured in this section. Carried forward.

**Q11 [Low]: H1 2026 unaudited and unreviewed; check for restatements at FY2026 audit.**
- **Status**: `Partially resolved (remainder stays open for [FY2026 audited AFS])`
- **Answer & evidence**: All H1 2026 statements are marked "Unaudited" `[unmapped, physical PDF pp. 8–32]`. No "reviewed" designation. Restatement risk remains open for FY2026 audit.

**Q6 [Medium]: Confirm ERC (R8,366m) estimation methodology and discount rate; check whether PBD/RTC carrying value (R4,489m) is impairment-tested; obtain portfolio ageing profile.**
- **Status**: `Partially resolved (remainder stays open for [PBD/RTC note])`
- **Answer & evidence**: PBD carrying value R4,489m `[unmapped, physical PDF p. 8, p. 13]`. PBDs are POCI/Stage 3, measured at amortised cost using CAEIR of **19.2%** (Mar-25: 17.9%; Sep-25: 18.4%) `[unmapped, physical PDF p. 21]`. Fair value disclosure uses current market discount rate **18.50%** (Mar-25: 15.81%; Sep-25: 15.93%) and states fair value approximates carrying value `[unmapped, physical PDF p. 26]`. **ERC R8,366m is NOT referenced in this section** — remains open. Portfolio ageing profile not disclosed (PBDs managed on cash-collection basis, not DPD).

---

### 2. Footnote & Qualification Deep-Dive

**Footnote 1.1 `*` — Pledged PBD as security** `[unmapped, physical PDF p. 13]`
- Quote: "Purchased book debts of R3 845 million ... have been pledged as security for the interest-bearing liabilities and bank overdrafts per the pledge agreement ... These assets are pledged for the duration of the agreement."
- Implication: **100% of the principal book portfolio (R3,845m) is encumbered**. This is a critical funding-structure constraint: the entire PBD asset base secures R4,016m of interest-bearing liabilities + overdrafts. Any ABS/securitisation trigger breach or pledge covenant could crystallise. Must verify pledge covenant terms and ABS performance triggers in the debt note.

**Footnote 1.1 `**` — Net collections composition** `[unmapped, physical PDF p. 13]`
- Quote: "Included in net collections are gross collections of R773 million ... and directly attributable and incremental collection costs of R45 million."
- Implication: Gross collections R773m less collection costs R45m = R728m net. Collection cost ratio = 5.8% of gross collections (Mar-25: 6.3%; Sep-25: 6.5%). Improving cost efficiency, but must verify whether "directly attributable and incremental" excludes overhead allocation — if so, true collection economics are worse.

**Footnote 2 `*` — Comparative disclosure presented for first time** `[unmapped, physical PDF p. 14]`
- Quote: "Comparative disclosure for 31 March 2025 has been presented for the first time to enhance the overall presentation."
- Implication: The Mar-25 debt maturity/class split is **newly presented**, not previously audited at interim. Increases restatement/comparability risk. Must verify against FY2025 audited AFS.

**Footnote 2.1 `*` — Pledge security (debt note)** `[unmapped, physical PDF p. 15]`
- Quote: "Purchased book debts, trade and other receivables and cash and cash equivalents have been pledged as security for the interest-bearing liabilities and bank overdrafts."
- Implication: Broader encumbrance than just PBD — trade receivables and cash also pledged. Reduces unencumbered liquidity. Must quantify unencumbered asset base for covenant headroom.

**Footnote 3.1 `*` — Share capital net of issue costs; treasury shares** `[unmapped, physical PDF p. 16]`
- Quote: "Nutun acquired 3,662,209 shares for a consideration of R3.7 million (average share price of R1 per share) ... for the purpose of holding the shares as treasury shares to be utilised on the vestings of the Conditional Share Plan."
- Implication: Share buyback at R1/share signals **market price distress** (vs R5,414m/784m = ~R6.90 book value per share). Treasury shares reduce weighted average shares to 782.1m, marginally inflating loss per share. Minor but signals capital management stress.

**Footnote 4 `*` and 4.1 `*` — Revenue disaggregation first-time presentation** `[unmapped, physical PDF p. 17]`
- Quote: "This disclosure was presented for the first time in the annual financial statements for the year ended 30 September 2025 ... Comparative disclosure for 31 March 2025 has been presented for the first time."
- Implication: Geographic revenue split is **newly disclosed** — no audited interim comparator. UK R303m (42.6% of revenue) is the largest geography; US R212m (29.8%); SA only R159m (22.4%). Concentration in UK/US BPO revenue — FX and client-concentration risk. Must verify client concentration.

**Footnote 5.1 `*` — Dilutive shares** `[unmapped, physical PDF p. 18]`
- Quote: "Shares deemed to be issued for no consideration in respect of the conditional share plan do not have a dilutive effect in the current period."
- Implication: Diluted = basic LPS at R(8.1)c. Conditional share plan is anti-dilutive in a loss period. On return to profit, dilution could re-emerge. Minor.

**Footnote 6.1 — ECL methodology: "low credit risk" presumption** `[unmapped, physical PDF p. 20]`
- Quote: "The group assumes that the credit risk on a financial instrument has not increased significantly if the financial instrument is determined to have a low credit risk at the reporting date."
- Implication: **SICR low-credit-risk exemption** applied. For PBDs (POCI/Stage 3 by definition) this is moot, but for trade receivables it could delay Stage 2 migration. Must verify SICR thresholds and whether 30-DPD backstop is applied.

**Footnote 6.1 — ECL maximum period = contractual period** `[unmapped, physical PDF p. 20]`
- Quote: "The maximum period considered when measuring ECL is the maximum contractual period (including extension options) ... and not a longer period, even if that period is consistent with business practice."
- Implication: For PBDs, ECL is measured over **rolling 12-month net cash flow** discounted at CAEIR `[unmapped, physical PDF p. 21]` — not full lifetime. This is a **shortened ECL horizon** vs full-lifetime Stage 3 ECL. Understates lifetime loss allowance if collections tail extends beyond 12 months. Must verify whether 12-month rolling is appropriate for POCI lifetime ECL.

**Footnote 6.1 — POCI classification irrevocable** `[unmapped, physical PDF p. 21]`
- Quote: "The classification of PBDs does not change subsequent to initial recognition, even in the unlikely event of the expected cash flows associated thereto returning to full contractual terms."
- Implication: PBDs permanently Stage 3. **No cure/re-aging to Stage 1/2 possible.** This is conservative and correct under IFRS 9, but means the entire R3,845m net PBD book is credit-impaired — coverage ratio of 12.6% is the key metric. Must benchmark 12.6% coverage against expected recovery rates.

**Footnote 6.1 — CAEIR 19.2%** `[unmapped, physical PDF p. 21]`
- Quote: "The weighted average credit-adjusted effective interest rate at period end is 19.2% (31 March 2025: 17.9%; 30 September 2025: 18.4%)."
- Implication: **CAEIR rose 130bps YoY**. Higher discount rate on same cash flows → lower PV → lower carrying value → but also higher imputed interest revenue (R383m vs R333m). This is a **double-edged sword**: it inflates the P&L interest line while depressing the balance sheet. Must verify whether CAEIR increase reflects higher market rates (benign) or higher credit risk premium (adverse). The fair value note uses 18.50% market rate vs 19.2% CAEIR — a 70bps gap that management says "approximates carrying value" `[unmapped, physical PDF p. 26]`. **This is a tension**: if market rate is 18.50% and CAEIR is 19.2%, fair value should be *higher* than carrying value, not equal. Must verify the fair value approximation.

**Footnote 6.1 — "elevated interest rate forecast" / impairment model parameters** `[unmapped, physical PDF p. 21]`
- Quote: "These impairment model parameters have been applied in determining expected cash shortfalls arising from non-payment in the best estimate provision on the loan book as at 31 March 2026. These books are not subsequently managed based on the credit risk rating but rather on a cash collection basis."
- Implication: Confirms forward-looking macro overlay applied. **No quantification of overlay** — must verify in PBD/RTC note. "Cash collection basis" confirms no DPD staging for PBDs.

**Footnote 6.1 — Trade receivables ECL table `*` and `**`** `[unmapped, physical PDF p. 25]`
- Quote: "The expected credit loss (ECL) on trade receivables is shown per the maturity of trade receivables ... This disclosure was presented for the first time..."
- Implication: Trade receivables ECL: Current 0.00%, 30-day 0.00%, 61–90 day 0.00%, 90+ day 100.00%, total 1.34% `[unmapped, physical PDF p. 25]`. **Zero ECL on 61–90 day overdue** is aggressive — no Stage 2 provisioning until 90+ days. This is a **relaxed SICR threshold** (90 DPD vs standard 30 DPD). Must verify SICR policy and whether this masks deterioration. Gross 90+ overdue fell to R5m from R7m, but 61–90 day fell to R5m from R6m — small book but policy is lenient.

**Footnote 6.2 `*` — Foreign currency assets** `[unmapped, physical PDF p. 26]`
- Quote: "Assets held in foreign currency relate to receivables of R207 million ... and bank balances of R27 million."
- Implication: FX exposure R234m assets vs R12m liabilities — net long FX. GBP strengthened (22.4 vs 23.1 avg) — translation loss R4m in OCI. Hedge contracts in place but **no hedge effectiveness disclosure**. Must verify hedge accounting.

**Footnote 6.3 — Fair value of PBD: discount rate 18.50% vs CAEIR 19.2%** `[unmapped, physical PDF p. 26]`
- Quote: "The fair value of principal book portfolios is determined by adjusting the discount rate from the credit-adjusted effective interest rate to a current market related discount rate of 18.50% ... The fair values determined on this basis approximates the carrying value."
- Implication: **Critical tension**: market rate 18.50% < CAEIR 19.2%. Lower discount rate → higher PV → fair value should exceed carrying value by ~R100m+. Yet management states fair value ≈ carrying value (both R3,845m) `[unmapped, physical PDF p. 27]`. Either (a) expected cash flows were also adjusted downward for risk, or (b) the approximation is imprecise. Must verify the cash flow adjustment and reconcile the R3,845m fair value to the 18.50% discount rate.

**Footnote 6.3 — Interest-bearing liabilities fair value** `[unmapped, physical PDF p. 27]`
- Quote: Carrying R3,743m vs fair value R3,769m (Mar-25: R3,407m vs R3,428m; Sep-25: R3,807m vs R3,468m).
- Implication: At Sep-25, fair value was **R339m below carrying** (favourable to group); at Mar-26, fair value is **R26m above carrying** (unfavourable). Swing of R365m in six months — reflects rising rates. Must verify rate sensitivity.

**Footnote 6.4 `*` — Level 3 other movements** `[unmapped, physical PDF p. 29]`
- Quote: "Other movements include additions of R28 million ... and cash collections of R116 million."
- Implication: Level 3 other financial assets R644m, gains R30m in P&L. Fair value gains of R30m (vs R74m Mar-25, R114m FY25) — **declining fair value gains** signal deteriorating performance on fair-value PBDs. Must verify.

**Footnote 7 `*` — Segment revenue** `[unmapped, physical PDF p. 30]`
- Quote: "Refer to note 4.1 for the disaggregation of revenue."
- Implication: Cross-reference only. No new information.

**Footnote 7 `*` — Amortisation of PBD composition** `[unmapped, physical PDF p. 31]`
- Quote: "Amortisation of purchased book debts is calculated as CAEIR imputed interest revenue of R383 million, impairment loss of R167 million and net cash collections of R728 million per note 1.1 and fair value movements of R30 million and cash collections of R116 million per note 1.2."
- Implication: **Critical reconciliation**: Amortisation R597m = CAEIR R383m + impairment R167m + net collections R728m + FV movements R30m + cash collections R116m − ? Let's check: 383 + 167 + 728 + 30 + 116 = 1,424. That does not equal 597. The footnote is describing the *components* of the CODM-view amortisation, not a simple sum. The CODM view amortisation R597m is the difference between CODM revenue from PBD (R888m) and IFRS net income from PBD (R69m) plus adjustments. Must verify the exact arithmetic: CODM revenue R888m − IFRS net income R69m = R819m, not R597m. **Reconciliation tension** — must verify.

**Footnote 7 `**` — Core EBITDA definition** `[unmapped, physical PDF p. 31]`
- Quote: "Core EBITDA is a non-IFRS measure calculated as core earnings per the policy above adjusted for Interest, Tax, Depreciation and Amortisation and Equity accounted earnings. It represents management's view of operating cash flows."
- Implication: **"Management's view of operating cash flows"** — but actual operating cash flow is R(111)m `[unmapped, physical PDF p. 12]`. Core EBITDA R790m vs operating cash outflow R(111)m — a **R901m gap**. This is the single most important qualification: EBITDA is NOT cash flow. Must verify the cash conversion bridge.

**Footnote 7 — Segment reconciliation: SA loss R(86)m, International profit R23m** `[unmapped, physical PDF p. 30]`
- Quote: SA (Loss)/profit before tax R(123)m; International R31m; Group R(92)m.
- Implication: **SA is loss-making at PBT level**; International is the only profitable segment. SA loss driven by net finance charge R(203)m (CODM view) vs International R(13)m. Must verify SA funding cost allocation.

**Footnote 7 — "Exceptional items (core and headline adjustments) = nil"** `[unmapped, physical PDF p. 31]`
- Quote: "Exceptional items (core and headline adjustments) — — —"
- Implication: **No core adjustments in H1 2026** — core loss = IFRS loss = R(63)m. This is cleaner than prior periods (H1 2025 had R71m headline adjustments). But must verify no items were reclassified as "normal operations" to avoid adjustment.

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q12 | High | Debt / funding note | 100% of PBD (R3,845m) pledged as security; trade receivables and cash also pledged `[unmapped, p. 13, p. 15]` | Obtain pledge agreement terms, covenant ratios (LTV, interest cover, net debt/EBITDA), ABS performance triggers, and unencumbered asset base | Encumbrance constrains refinancing and liquidity; covenant breach could accelerate debt |
| Q13 | High | PBD/RTC note / accounting policies | CAEIR 19.2% vs fair value discount rate 18.50%; management states fair value ≈ carrying value `[unmapped, p. 21, p. 26–27]` | Reconcile R3,845m fair value to 18.50% discount rate; verify cash flow risk adjustment; check whether CAEIR increase is market-rate or credit-risk driven | If fair value < carrying value, impairment write-down needed; CAEIR increase inflates P&L interest but may mask credit deterioration |
| Q14 | High | PBD/RTC note | 12-month rolling ECL horizon for POCI assets `[unmapped, p. 21]` | Verify whether 12-month rolling net cash flow is appropriate for lifetime ECL on POCI; check tail beyond 12 months; obtain vintage loss curves | Shortened horizon may understate lifetime loss allowance |
| Q15 | High | Credit risk note | Trade receivables ECL: 0% on 61–90 day overdue, 100% only at 90+ `[unmapped, p. 25]` | Verify SICR policy and 30-DPD backstop; check whether 90-DPD threshold is a relaxation vs FY2025 | Relaxed SICR delays Stage 2 provisioning; masks deterioration |
| Q16 | High | Segment note 7 / PBD note | Amortisation R597m composition footnote does not arithmetically reconcile (383+167+728+30+116 ≠ 597) `[unmapped, p. 31]` | Reconcile CODM revenue R888m − IFRS net income R69m to amortisation R597m; verify each component | If amortisation is misstated, core EBITDA R790m is misstated |
| Q17 | High | Cash flow statement / segment note | Core EBITDA R790m vs operating cash outflow R(111)m — R901m gap `[unmapped, p. 12, p. 31]` | Build full EBITDA-to-cash bridge: interest paid R225m, PBD additions R382m, WC R(23)m, tax R2m | EBITDA is not converting to cash; liquidity risk |
| Q18 | High | Debt / funding note | Undrawn overdraft facilities R475m only; "~R0.8bn unutilised" claim not corroborated `[unmapped, p. 14]` | Verify total undrawn facilities across all debt types (not just overdraft); check R0.8bn claim source | Liquidity headroom may be overstated |
| Q19 | Medium | PBD/RTC note | Cumulative impairment gain R431m "relates to elevated performance above investment base-case"; reduction due to "payer drop-offs and reduced settlement activity" `[unmapped, p. 24]` | Quantify base-case vs actual collections; obtain vintage loss curves; verify payer drop-off rate | If base-case is too optimistic, R431m gain could reverse |
| Q20 | Medium | Segment note 7 / revenue note | SA commissions R159m (down 15.4%); client count 23→20; no top-10 concentration disclosed `[unmapped, p. 17]` | Obtain top-10 client % of revenue; verify SA agency commission sustainability | Revenue concentration risk |
| Q21 | Medium | Segment note 7 | SA PBT R(123)m vs International R31m; SA net finance charge R(203)m CODM view `[unmapped, p. 30]` | Verify SA funding cost allocation; check transfer pricing | SA loss-making; group reliant on International |
| Q22 | Medium | Currency risk note | FX hedge contracts for USD/GBP; no hedge effectiveness disclosure `[unmapped, p. 25]` | Verify hedge accounting treatment, effectiveness, and MTM | FX volatility could hit P&L |
| Q23 | Medium | Fair value note | Level 3 FV gains R30m (vs R74m Mar-25, R114m FY25) — declining `[unmapped, p. 29]` | Verify FV gain drivers; check whether decline signals deteriorating performance | Declining FV gains signal credit deterioration |
| Q24 | Medium | Debt note | Interest-bearing liabilities fair value swing R365m in 6 months (Sep-25 FV R339m below carrying → Mar-26 R26m above) `[unmapped, p. 27]` | Verify rate sensitivity; check fixed vs floating split (all floating per note) | Rising rates increase funding cost and fair value liability |
| Q25 | Low | Board / governance / related-party note | No related-party note captured `[unmapped, pp. 8–32]` | Check for related-party transactions and key-person risk | Governance risk |
| Q26 | Low | FY2026 audited AFS | All H1 2026 statements "Unaudited"; no "reviewed" designation `[unmapped, pp. 8–32]` | Check for restatements to PBD carrying value, amortisation, CAEIR, or core earnings at FY2026 audit | Restatement risk |
| Q27 | Low | Share capital note | Treasury shares acquired at R1/share vs book value ~R6.90/share `[unmapped, p. 16]` | Verify market price vs book value; check capital management strategy | Market distress signal |

---

### 5. Baseline Forecast Inputs Captured Here

| Metric | H1 2026 (Mar-26) | H1 2025 (Mar-25) | FY2025 (Sep-25) |
| --- | --- | --- | --- |
| Revenue | R711m | R745m | R1,435m |
| Gross profit from services | R326m | R393m | R703m |
| Cost of revenue | R(385)m | R(352)m | R(732)m |
| Net income from PBD | R69m | R53m | R244m |
| CAEIR imputed interest | R383m | R333m | R683m |
| Interest expense | R(177)m | R(181)m | R(354)m |
| Impairment loss on PBD | R(167)m | R(173)m | R(199)m |
| Fair value movements other financial assets | R30m | R74m | R114m |
| Operating costs | R(445)m | R(560)m | R(1,063)m |
| Net finance charge | R(39)m | R(52)m | R(91)m |
| Operating loss | R(79)m | R(168)m | R(186)m |
| Loss before tax | R(92)m | R(161)m | R(148)m |
| Income tax credit | R29m | R39m | R35m |
| Loss from continuing ops | R(63)m | R(122)m | R(113)m |
| Loss from discontinued ops | – | R58m | R(125)m |
| Loss for period | R(63)m | R(64)m | R(238)m |
| Basic LPS (total) | (8.1)c | (8.2)c | (30.3)c |
| Headline LPS (total) | (8.1)c | (17.2)c | (39.4)c |
| Core EBITDA | R790m | n/a | n/a |
| SA Core EBITDA | R710m | n/a | n/a |
| Intl Core EBITDA | R80m | n/a | n/a |
| **Balance sheet** | | | |
| Cash & equivalents | R112m | R118m | R106m |
| Other investments | R81m | R237m | R41m |
| Trade & other receivables | R497m | R556m | R471m |
| PBD (net) | R4,489m | R4,353m | R4,677m |
| — Principal book (net) | R3,845m | R3,690m | R3,975m |
| — Other financial assets | R644m | R663m | R702m |
| Total assets | R6,444m | R6,661m | R6,604m |
| Bank overdrafts | R273m | R457m | R364m |
| Interest-bearing debt | R3,743m | R3,407m | R3,443m |
| — Senior debt | R3,547m | R3,182m | R3,293m |
| — Subordinated debt | R196m | R225m | R150m |
| Lease liabilities | R345m | R395m | R364m |
| Total liabilities | R5,115m | R5,110m | R5,208m |
| Total equity | R1,329m | R1,551m | R1,396m |
| **Credit metrics** | | | |
| PBD gross carrying (principal) | R3,414m | R3,066m | R3,377m |
| PBD ECL allowance | R431m | R624m | R598m |
| PBD coverage ratio | 12.6% | 20.4% | 17.7% |
| — Banking unsecured coverage | 9.6% | 19.4% | 18.9% |
| — Debt review coverage | 14.8% | 10.7% | 9.1% |
| — Retail coverage | >100% | >100% | 97.9% |
| — Banking secured coverage | 26.1% | 71.4% | 20.4% |
| Gross collections | R773m | R604m | R1,280m |
| Net collections | R728m | R566m | R1,197m |
| Collection costs | R45m | R38m | R83m |
| PBD additions | R382m | R265m | R857m |
| CAEIR | 19.2% | 17.9% | 18.4% |
| Fair value discount rate (PBD) | 18.50% | 15.81% | 15.93% |
| Other financial assets discount rate | 16.0% | 12.93% | 16.0% |
| Trade receivables ECL rate | 1.34% | 1.43% | 2.75% |
| **Funding** | | | |
| Total interest-bearing liabilities | R4,016m | R3,864m | R3,807m |
| Payable <12 months | R1,396m | R1,039m | R1,237m |
| Payable >12 months | R2,620m | R2,825m | R2,570m |
| Undrawn overdraft facilities | R475m | R43m | R136m |
| **Cash flow** | | | |
| Cash utilised by operations | R(50)m | R(103)m | R(338)m |
| Interest paid | R(225)m | R(251)m | R(468)m |
| Net cash utilised by operating activities | R(111)m | R(213)m | R(297)m |
| PBD additions (cash) | R(382)m | R(265)m | R(857)m |
| Net cash from investing | R(61)m | R437m | R603m |
| Net cash from financing | R178m | R(696)m | R(787)m |
| Net cash movement | R6m | R(472)m | R(482)m |
| **Revenue by geography** | | | |
| South Africa | R159m | R188m | R341m |
| Australia | R27m | R74m | R127m |
| United Kingdom | R303m | R259m | R525m |
| United States | R212m | R224m | R428m |
| Other | R10m | – | R14m |
| **Segment PBT** | | | |
| SA PBT | R(123)m | R(202)m | n/a |
| Intl PBT | R31m | R41m | n/a |
| Group PBT | R(92)m | R(161)m | R(148)m |

---

### 6. Next Section to Capture

**Next section: Debt / funding note (covenants, maturity profile, ABS triggers) — or the PBD/RTC note if available.**

This section will resolve:
- **Q5** (covenant ratios, headroom, R0.8bn unutilised facilities)
- **Q12** (pledge agreement terms, ABS triggers, unencumbered assets)
- **Q18** (total undrawn facilities)
- **Q24** (rate sensitivity, fixed vs floating)
- **Q13** (partially — funding cost context for CAEIR vs market rate)

If the PBD/RTC note is available instead, it will resolve **Q3, Q6, Q13, Q14, Q19** (CAEIR methodology, ERC, vintage curves, base-case assumptions).
