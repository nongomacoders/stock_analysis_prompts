# STAGE 1: INDEPENDENT COGNITIVE AUDIT VIA SEQUENTIAL EXTRACTION & QUESTION LEDGER
**Target Asset:** SPP Group (SPP)  
**Sector:** Retail  
**Primary Document:** `SPAR_GROUP_H1 2026_Results.pdf` (Integrated Annual Report [IAR] — 5 sections)  
**Companion Financial Document:** `Unaudited_interim_results_for_the_26_weeks_ended_27_March_2026.pdf` (AFS — 2 sections)  
**Input Mode:** Sequential Forensic Working Paper & Dynamic Questions Ledger (No PDF Attached)  
**Task Directive:** Forensic Reasoning, Conflict Reconciliation & Post-Balance-Sheet Determinations (No Full Forward Valuation Model Required)

---

### INSTRUCTIONS FOR FORENSIC AUDITOR (LLM):
You are acting as an independent **Managing Director and Senior Forensic Retail & Consumer Credit Accounting Auditor**. 
You have been provided with the complete, chronological working paper compiled during a section-by-section forensic capture of SPP Group's financial disclosures (7 total sections across primary report and companion disclosures).

Notice how this working paper is constructed:
1. At each stage, specific text, accounting notes, APMs, and operational tables were extracted directly from the report.
2. Across the sections, an **Open Questions Ledger** evolved dynamically: anomalies and high-level management claims in early sections were flagged with priority levels, specific verification instructions, and carried forward as `Pending` until verified against primary financial statements, detailed accounting notes, and subsequent continuous disclosures.

**YOUR MANDATE:**
Review the sequential evidence trail below. Trace how the questions evolved from initial anomalies to audited reconciliation. **Do not produce a forward equity research forecast or valuation report.** Your role is **forensic reasoning only**: you must evaluate the working papers and independently reach your own definitive determinations on the core accounting, operational, and balance sheet junctions, explicitly factoring in subsequent SENS disclosures.

---

## REQUIRED STRUCTURE OF YOUR AUDIT REPORT

Please format your response into the following four clear sections:
1. **Executive Forensic Audit Summary:** Concise synthesis of the group's true economic performance, balance sheet health, post-balance-sheet liquidity runway, and key findings.
2. **Detailed Forensic Reasoning & Determinations:** Step-by-step walkthrough of each key retail junction (merchandise vs credit/other revenue, gross profit margin bridge, debtors book health & IFRS 9 ECL provisioning, store network capex and trading density, IFRS 16 lease liability structure, post-year-end trading, and cash conversion / dividend payout), citing specific notes, tables, and calculations.
3. **Audit of Common Surface-Reading Pitfalls:** Contrast your findings against the common errors made by naive readers.
4. **Final Forensic Verification Matrix:** A clean markdown summary table listing each Junction, the Raw Initial Claim, the Resolving Note/SENS Announcement, and your Final Verified Determination.

---

## MANDATORY ACCOUNTING & VALUATION GUARDRAILS REGISTRY (SECTOR: RETAIL)

The following institutional guardrails are enforced from the SQLite `sector_guardrails` registry based on prior forensic audits. Violating any of these rules invalidates the report:

| Rule Code | Scope | Guardrail Title | Mandatory Enforcement Rule |
| :--- | :---: | :--- | :--- |
| `ALL-IFRS16-EV-BRIDGE` | **UNIVERSAL** | **IFRS 16 EV-to-Equity & Cash Flow Consistency** *(Origin: SPP)* | Never mix Pre-IFRS 16 cash flows/EBITDA with Post-IFRS 16 lease debt in an Enterprise Value (EV) to Equity bridge. If EV is derived by discounting or applying a multiple to Pre-IFRS 16 EBITDA/FCFF (where cash lease rental payments are already deducted as an operating outflow), DO NOT subtract capitalised IFRS 16 lease liabilities again in the EV-to-Equity bridge (and do not subtract lease principal payments a second time in FCFE). Conversely, if subtracting net IFRS 16 lease liabilities in the EV bridge, you must discount Post-IFRS 16 EBITDA/FCFF before lease payments. Always state explicitly whether your valuation bridge is on a Pre-IFRS 16 or Post-IFRS 16 basis. |
| `ALL-PNL-VERTICAL-ARITHMETIC` | **UNIVERSAL** | **Statutory vs. Normalized P&L Vertical Arithmetic & Impairment Bridge** *(Origin: SPP)* | Every income statement table must sum vertically line-by-line (Revenue - Cost of sales = Gross profit; Gross profit + Other revenue/income - Net operating expenses = Operating profit). Always verify from the primary AFS notes whether statutory Operating Profit is already stated AFTER impairments, restructuring, or extraordinary items before subtracting them; never subtract Note 7/exceptional impairments a second time from a statutory Operating Profit that already includes them, and ensure historical continuing PAT and HEPS match the statutory AFS reconciliation identically. |
| `RETAIL-IFRS16-HEADLEASE-SUBLEASE` | **RETAIL** | **Retail Head-Lease Liability vs. Back-to-Back Franchisee Lease Receivable Netting** *(Origin: SPP)* | For wholesale/franchise retailers (e.g. SPAR) that sign head-leases on properties and sub-lease them back-to-back to independent retailers, always net the IFRS 16 finance lease receivables (Current + Non-current) against gross IFRS 16 lease liabilities to isolate the group's true net store/DC lease exposure, and distinguish Pre-IFRS 16 covenant EBITDA from Post-IFRS 16 statutory EBITDA. |
| `RETAIL-ECL-CASHFLOW-VS-ALLOWANCE` | **RETAIL** | **Retail & Trade Receivable ECL Non-Cash Movement vs. Balance Sheet Allowance Bridge** *(Origin: SPP)* | When auditing trade/retailer receivables and loan allowances, reconcile the Cash Flow Statement non-cash ECL movement against the Balance Sheet allowance movement by accounting for final write-offs against the allowance and fair-value discounting, and verify whether elevated credit loss run-rates persist in post-balance-sheet SENS updates. |

---

## MASTER WORKING PAPER: CUMULATIVE OPEN QUESTIONS LEDGER
> **Cognitive Audit Anchor:** The authoritative ledger below consolidates all priority questions, forensic hypotheses, and cross-reference resolutions developed across the entire disclosure set. Use this ledger as your reference matrix when auditing the sequential section extractions that follow.

## OPEN QUESTIONS LEDGER — SPAR Group H1 2026 (after Corporate Information capture, p. 21)

### Target: Debtors / credit note
- Q5 [High]: Gross debtors, ECL allowance, satisfactory-paid %, collection rate, write-offs — explain "increase in overdues". (Partially resolved: trade receivables R15,975.2m [p. 5]; provision movement R150.7m [p. 13]. ECL allowance, satisfactory-paid %, collection rate, ageing still open.) [p. 30, p. 48]
- Q14 [High]: Get ECL allowance, satisfactory-paid %, collection rate, write-offs, and ageing analysis. Reconcile to the R273m specific impairment charge. (Partially resolved: R150.7m P&L provision movement visible [p. 13]; R273m specific impairment and R58m G&L write-offs not in this section. Balance/ageing still open.) [p. 30, p. 48]
- Q39 [High]: Confirm whether R273m is specific or portfolio ECL; get ECL allowance balance, satisfactory-paid %, collection rate, ageing buckets; check H2 provisioning guidance. (Partially resolved: R150.7m provision movement [p. 13]; R273m not visible. Still open.) [p. 48]
- Q53 [High]: Locate debtors note: gross debtors, ECL allowance, satisfactory-paid %, collection rate, ageing buckets, write-offs. Reconcile R150.7m P&L movement [p. 13] to R273m specific impairment and R58m write-offs. [p. 5, p. 13]

### Target: Cash flow statement / notes
- Q57 [High]: Explain the R1,841.7m payables outflow [p. 13] — timing, settlement of prior overdues, or structural? Check creditor days vs prior periods. [p. 7, p. 13]

### Target: Balance sheet / notes
- Q6 [Medium]: Corporate store count, losses, closure/transfer plans. (Partially resolved: 3 SA corporate stores ROU impaired R22.7m [p. 16]; 8 SA stores acquired, 5 sold [pp. 13, 15]. Count and plans still open.) [p. 19, p. 41, p. 50]
- Q18 [Medium]: Break down the R143m "Legacy matters" column on OP analysis into its components. (Partially resolved: impairments R128.6m [p. 16], acquisition costs R9.8m [p. 15], Giannacopoulos provision R5.1m [p. 19]. R143m column not directly visible.) [p. 25, p. 48]
- Q19 [Medium]: Confirm where the VSP cost R27.3m is recorded and the phasing of the R33.2m annual savings. (Not visible in this section. Still open.) [p. 39]

### Target: Income statement / segment note
- Q26 [High]: Confirm basis of "~EUR 70m EBITDA* — *12 months to March 2026" (pre/post IFRS 16, pre/post exceptionals, BWG-only vs all Ireland). Reconcile to Ireland segment operating profit. (Partially resolved: Ireland op profit R502.8m + D&A R288.1m = R790.9m H1, annualised ~R1,581.8m ≈ EUR 82.8m at R19.11/EUR — above EUR 70m. Basis still open.) [p. 42, p. 49]
- Q28 [High]: Confirm whether AWG is presented as discontinued operations in H1 2026 (IFRS 5), gain/loss on disposal, and H2 trading loss phasing (~£5m). (Partially resolved: UK discontinued confirmed [p. 17]; H1 UK loss after tax R98.4m + Poland R46.0m = R144.4m; disposal GBP 13.0m gross, net breakeven, completion Jun–Sep 2026 [p. 20]. Gain/loss and H2 phasing still open.) [p. 41, p. 46, p. 51]
- Q31 [Medium]: Check whether management guides to a wholesale GP% trade-off from "retailer profitability as primary operating metric". (Partially resolved: group GP% 10.54% vs 10.74% (–20bps) [p. 4]; Ireland GP 15.12%, SA GP 10.95% [p. 9]. No explicit trade-off guidance.) [p. 41, p. 49]
- Q36 [Medium]: Locate IFRS 5 note: confirm Switzerland and UK both presented as discontinued; get Switzerland disposal status/gain-loss and held-for-sale balances. (Partially resolved: UK discontinued H1 2026 [p. 17]; Switzerland/Poland were discontinued in prior periods but not H1 2026. Switzerland gain/loss and HFS balances not in this section.) [p. 46, p. 51]
- Q38 [High]: Confirm UK HFS impairment R1.5bn excluded from headline earnings; locate HEPS reconciliation; confirm no further H2 write-down. (Partially resolved: HFS impairments added back in HEPS recon [p. 8]; R1.5bn was H1 2025 comparative; H1 2026 HFS impairment only R13.1m [p. 16]. No H2 write-down guidance — note 13 says full effect being assessed [p. 20].) [p. 51]
- Q42 [High]: Quantify "change in accounting estimates" (YTD depreciation catch-up Nov 2025; RCC amortisation timing Dec 2025) impact on Ireland opex; confirm recurrence in H2. (Partially resolved: group D&A R549.3m vs R551.7m — flat [p. 9]; Ireland D&A R288.1m vs R293.0m. No explicit estimate change disclosed. Still open.) [p. 49]
- Q43 [Medium]: Decompose other revenue +54.0% to R887.6m (VSP fees, G&L liquor, other); confirm recurring vs one-off and GP vs operating income treatment. (Partially resolved: other revenue R1,109.6m [p. 11]: marketing/services R839.5m +78.2%, franchise R127.1m +9.x%. Remainder still open.) [p. 22, p. 23, p. 48, p. 53]

### Target: Corporate information / governance (new)
- Q58 [Low]: Confirm whether the interim results carry an independent review conclusion (unmodified/emphasis-of-matter) in the auditor's review report section. [p. 21]
- Q59 [Low]: Identify actual Report Map section IDs and page ranges for the debtors note, cash flow note, and segment note so Q5/Q14/Q39/Q53/Q57 can be correctly targeted. [p. 21]

---

# THE SEQUENTIAL EXTRACTION & WORKING PAPER DOSSIER (7 TOTAL SECTIONS)

================================================================================
## PART 1: PRIMARY FINANCIAL DISCLOSURE (`SPAR_GROUP_H1 2026_Results.pdf` — 5 Sections)
================================================================================

================================================================================
## PART 1 - SECTION 1: [unmapped] Overview & Highlights
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section unmapped | [PRES] physical page 1 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                      Interim                       
                                                                                                                                    
                                                                                                                                    
                                                                                                     Results                        
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                 H1       FY2026                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                     For  the 26  weeks             
                                                                                                                                    
                                                                                                  ended   27  March    2026         
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    

--- Section unmapped | [PRES] physical page 2 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                       Overview                of    the      period                                                
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                          Reeza   Isaacs                                                            
                                                                                                                                    
                                                                                                                                    
                                                 Group   Chief  Executive   Officer                                                 
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    

--- Section unmapped | [PRES] physical page 3 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Reflecting       on   an   eventful     past    few   years                                                                 
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
            FY22                    FY23                   FY24                   FY25                                              
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                             Continued portfolio                                    
                                                                                                      AWG   sale - European         
                                                     Competitive intensity     simplification -                                     
                                                          increases           Switzerland exit      portfolio review complete       
        Post-pandemic           KZN  DC SAP                                                                                         
         headwinds                disruption                                                                                        
                                                         Poland exit          Debt restructure        SAP  implementation           
                                                                                                             ongoing                
         International         Margin pressure                                                                                      
                                                                            Balance sheet clean                                     
         complexity                                                                                                                 
                                                      Net debt reduction      up – further debt                                     
                              Poland impairment                                                                                     
                                                                                 reduction                                          
     SAP transition begins                                                                                                          
                                                      Refocusing on the                                                             
                             Dividend suspended                                                                                     
                                                            core              Margin pressure                                       
                                                                                                        Refocusing on SA +          
                                                                                                      Ireland - improving core      
                                                                                                      operations and margins        
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                  3  

--- Section unmapped | [PRES] physical page 4 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        H1   2026    | A  tough     start    to  the  year                                                                          
                                                                                                                                    
                                                                                                                                    
        A candid view of the half                                                                                                   
                                                                                                                                    
                                                                                                                                    
                        The numbers we must address                                        Positives in the period                  
                                                                                                                                    
                                                                             Ireland                                                
                                                                             +3% OP Margin                                          
                                                                             Topline growth delivered despite tougher macro & competitive pressure.
                                                                             A mainstay of the portfolio.                           
                              –56%                                                                                                  
                                                                                                                                    
                                                                             Working Capital & Liquidity                            
                                                                             Well managed                                           
                                                                             Working capital discipline maintained - impacted by timing of the monthly
                                 HEPS                                                                                               
                                                                             cycle. Funding and liquidity remain stable.            
              Headline earnings per share^ - half on prior period                                                                   
                                                                             SA G&L Loyalty                                         
                                                                                                                                    
                                                                             Maintained                                             
                                                                             Grocery & Liquor retailer loyalty remained healthy over the past 6 months.
                                                                                                                                    
                                                                             Build it & SPAR Health                                 
                               ~1%                                                                                                  
                                                                             +26% revenue growth in Health                          
                                                                             Build it returned to growth at retail. SPAR Health adjacency grew 26% - a
                                                                             clear bright spot and strategic priority.              
                                                                                                                                    
                                                                                                                                    
                          SA operating margin*                               New Leadership                                         
                Significantly below prior year and our targets               Renewed leadership and accountability                  
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
    ^On a comparable basis                                                                                                          
    *Operating profit excluding extraordinary items      INTERIM RESULTS FY2026                                                  4  

--- Section unmapped | [PRES] physical page 5 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                        Key       drivers           of    H1      2026        performance                                           
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    

--- Section unmapped | [PRES] physical page 6 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Issue    1  | KwaZulu-Natal           | R123m       operating       profit   impact                                         
                                                                                                                                    
                                                                                                                                    
        One of the Group's most critical near-term execution priorities                                                             
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                   What  went  wrong                    What  was  the impact                   What  have  we done                 
                                                                                                                                    
                                                                                                                                    
           Topline was driven hard, but margin    Revenue growth not converting to profit New leadership in place                   
           discipline was weak                    •    H1 2026 sales up 4.9% y-o-y       • Merch, Finance and Retail Ops            
           •    GP% fell significantly in Dec/Jan and • GP margin decline for H1 2026                                               
                cost base grew faster than revenue     compared to prior year - operating profit Stabilisation programme launched   
                conversion                             near break-even for the half      • Dedicated turnaround team in place with  
                                                                                                                                    
           •    Warehouse & Logistics not geared for                                       defined milestones and workstream        
                higher volumes                                                             ownership                                
                                                  Service failures impacted retailers                                               
           Logistics cost structure               •    OOS peaked; retailer fulfilment below                                        
           •    Labour agreements restricted           target; cost to serve retailers in KZN GP recovery underway                  
                outsourcing flexibility with overtime, overspent                         • GP% improved through H1, with momentum   
                hired-truck and additional warehouse                                       building into period-end; logistics cost 
                costs                                                                      reduction initiatives active             
                                                                                                                                    
                                                                                                                                    
           Operational disruption at the DC                                              Service levels recovering                  
           •    Service levels, ordering and fulfilment                                  • OOS materially improved from peak by     
                disrupted - retailer experience                                            period-end; fleet additions reducing external
                deteriorated and OOS spiked to >15%                                        truck hire dependency                    
                                                                                                                                    
                     Current status: Recovery in progress – 3 consecutive months of profit. GP trajectory positive. Stabilisation programme active.
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                  6  

--- Section unmapped | [PRES] physical page 7 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Issue    2  | Black     Friday     | Impact     of  R212m^       in  the   period                                           
                                                                                                                                    
                                                                                                                                    
        We optimised marketing for supplier income rather than shopper footfall; we did not get the ROI.                            
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                   What  went  wrong                    What  was  the impact                   What  have  we done                 
                                                                                                                                    
                                                                                                                                    
           Black Friday – spend without a return  Shopper footfall did not translate into New CMO appointed                         
           framework                              volumes                                • Renewed brand positioning in development 
           • ^BF overspend of R152m in H1 with margin • Retail sales up c.1% YoY - tracking below                                   
             impact of R60m                         real GDP                             Review/assessment completed                
           • No ROI measurement in place          • No competitive customer value proposition • Identified issues with action plans in place
                                                                                                                                    
           • GP drag through below-cost pricing and vs chain retailers                     and clear accountability                 
             promo rebates                        • Transactions -2.3%                   • New integrated trade plan for FY2027; new
           • Guaranteed subsidies                                                          Black Friday approach agreed             
                                                  GP and brand pressure                                                             
           System rewarded supplier income, not   • Marketing expenses accelerated above prior ROI framework activated              
           footfall                                 year                                 • All marketing spend will be measured     
           • Fragmented ownership across DCs, central • Retailer loyalty while stabilised, remains against sales and loyalty outcomes
             marketing and merchandise              below 80% target                                                                
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                          Current status: New CMO in place. ROI framework live. Brand-before-promotions is now the operating principle.
                                                   Revamped trade plan for FY2027 underway.                                         
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                  7  

--- Section unmapped | [PRES] physical page 8 | area selection | Table ---
SA grocery & Liquor loyalty[^*] stabilised; but below 80% goal - work still to do
Average Loyalty across all DC regions excluding KwaZulu Natal: 77.90%
Retailer loyalty was impacted by SAP rollout in 2022… Efforts to address have stabilised Loyalty over the last 6 months
2020-2025 Oct 2025 – Apr 2026

|  |  |  | Total G&L |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  | ) |  |  |  |  |  |  |  |  |  |  |
| )l |  |  | 83.3% |  |  |  |  | ylh 78.6% |  |  |  | 78.4% |  | 78.3% |  | 78.5% | 78.2% |  |
| [^a] | 82.6% | 82.7% |  | 81.8% |  |  |  | tn |  |  | 77.8% |  | 77.7% |  |  |  |  |  |
| u |  |  |  |  |  |  |  | o |  |  |  |  |  |  |  |  |  |  |
| nn |  |  |  |  | 79.4% |  |  | [^M] |  |  |  |  |  |  |  |  |  |  |
| [^A] |  |  |  |  |  |  | 77.6% | ( y |  |  |  |  |  |  |  |  |  |  |
| ( |  |  |  |  |  |  |  | t |  |  |  |  |  |  |  |  |  |  |
| y |  |  |  |  |  |  |  | [^l] |  |  |  |  |  |  |  |  |  |  |
| [^t] |  |  |  |  |  |  |  | a |  |  |  |  |  |  |  |  |  |  |
| [^l] |  |  |  |  |  |  |  | y |  |  |  |  |  |  |  |  |  |  |
| a |  |  |  |  |  |  |  | o |  |  |  |  |  |  |  |  |  |  |
| y |  |  |  |  |  |  |  | [^l] |  |  |  |  |  |  |  |  |  |  |
| o |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| [^l] |  |  |  |  |  |  |  | g |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  | n |  |  |  |  |  |  |  |  |  |  |
| g |  |  |  |  |  |  |  | [^i] |  |  |  |  |  |  |  |  |  |  |
| n |  |  |  |  |  |  |  | ll |  |  |  |  |  |  |  |  |  |  |
| il |  |  |  |  |  |  |  | o |  |  |  |  |  |  |  |  |  |  |
| [^l] |  |  |  |  |  |  |  | r |  |  |  |  |  |  |  |  |  |  |
| o r h |  |  |  |  |  |  |  | htm 70.9% |  |  | 70.2% | 70.4% | 70.4% | 70.4% |  | 70.8% | 70.5% |  |
| t |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  | - |  |  |  |  |  |  |  |  |  |  |
| m |  |  |  |  |  |  |  | [^2] |  |  |  |  |  |  |  |  |  |  |
| - |  |  |  |  |  |  |  | 1 |  |  |  |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Oct 19 to | Oct 20 to | Oct 21 to | Oct 22 to | Oct 23 to |  | Oct 24 to |  |  |  |  |  |  |  |  |  |  |  |
|  | Sep 20 | Sep 21 | Sep 22 | Sep 23 | Sep 24 |  | Sep 25 | Nov 24 to Dec 24 to Jan 25 to Feb 25 to Mar 25 to Apr 25 to May 25 to |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  | Oct 25 |  |  | Nov 25 | Dec 25 | Jan 26 | Feb 26 |  | Mar 26 | Apr 26 |  |
|  |  | COVID-19 |  | SAP disruption |  |  |  |  |  |  |  | KZN | Total G&L |  |  |  |  |  |
|  | *Includes South Africa and foreign countries (Swaziland, Namibia, Mozambique and Botswana) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | South Africa loyalty as at April 2026: 79.9% |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Foreign countries loyalty as at April 2026: 59.4% |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  | INTERIM RESULTS FY2026 |  |  |  |  |  |  |  |  |  |  | 8 |

--- Section unmapped | [PRES] physical page 9 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                    Creating             a   stronger              platform             for     growth                              
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    

--- Section unmapped | [PRES] physical page 10 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Resetting       on   two    fronts    - retailer    and    wholesale                                                        
                                                                                                                                    
                                                                                                                                    
        Unleashing the power of independent retail                                                                                  
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                     Independent,                                   
                             Efficient, best-in-                                                                                    
                                                                                     entrepreneurial                                
                             class wholesale                                                                                        
                                                                                     retailers                                      
                             Scale, supply chain                                                                                    
                                                                                     Local ownership, agility                       
                             and margin discipline                                                                                  
                                                                                     and customer connection                        
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                          A winning     voluntary    trade  model                                                   
                                                                                                                                    
                                                     “We are better together”                                                       
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 1100

--- Section unmapped | [PRES] physical page 11 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                               Restoring             retailer        profitability.                 
                                                                                                                                    
                                                                                                                                    
                                                                    Fixing        the     fundamentals.                             
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    

--- Section unmapped | [PRES] physical page 12 | area selection | Table ---
Retail focus areas | Removing friction. Enabling growth

| 1 | Stronger | 2 |  | 3 |  | 4 | Building a future- | 5 | Empowering retailers to |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | Brand & marketing |  | Repositioning |  |  | fit retail |  |  |  |
|  | procurement, |  |  |  |  |  |  |  | improve |  |
|  |  | effectiveness |  | SPAR2U |  |  | technology |  |  |  |
|  | sharper pricing |  |  |  |  |  |  |  | profitability and |  |
|  |  |  |  |  |  |  | platform |  |  |  |
|  |  |  |  |  |  |  |  |  | manage costs |  |
|  | Merchandising | Marketing |  | eCommerce |  |  | Retail Technology |  | Retail Costs |  |
|  |  |  |  | INTERIM RESULTS FY2026 |  |  |  |  |  | 12 |

--- Section unmapped | [PRES] physical page 13 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                  Strengthening                  wholesale              &           
                                                                                                                                    
                                                                                                                                    
                                                                                   distribution                                     
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                  “Unleashing      the  power    of independent       retail”       
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    

--- Section unmapped | [PRES] physical page 14 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Wholesaler         focus    areas     | Fixing    the   foundations,         restoring      margins                         
                                                                                                                                    
                                                                                                                                    
        Building a better, more efficient wholesale and distribution capability.                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                            Margin                         Improving                        Growth                                  
                         Optimisation                      Efficiency                      Initiatives                              
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                     Centre led merchandise              Cost optimisation         Accelerating growth through formats,             
                                                                                      adjacencies and partnerships                  
                         KZN recovery                Warehousing & distribution                                                     
                                                           efficiencies                                                             
                                                                                          SPAR2U & online                           
                      Corporate stores loss                                                                                         
                           reduction                Finance transformation (trade                                                   
                                                                                        Private label expansion                     
                                                      payables & dropshipment)                                                      
                                                     Technology value realisation                                                   
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 1144

--- Section unmapped | [PRES] physical page 15 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Tracking       the  turnaround                                                                                              
                                                                                                                                    
                                                                                                                                    
        The measurable goals behind each workstream - what we are steering toward                                                   
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                    Workstream                         Metric & current status                      Target / milestone              
                                                                                                                                    
                                                                                                                                    
                                              Gross & operating margin + wholesale revenue                                          
                                              growth vs inflation + new-format rollout                                              
                 Margin & growth                                                           Margin recovery; scale new formats       
          1                                                                                                                         
                                              Margin recovering off H1 lows; SaveMor, Health, Pet                                   
                                              Storey underway                                                                       
                                              Out-of-stock rate + KZN profitability                                                 
                                                                                           Sustained reduction toward pre-disruption
          2      Service levels                                                                                                     
                                              Out of stock down from peak at close of H1; 3                                         
                                                                                           levels                                   
                                              consecutive months of positive operating profit in KZN                                
                                              Retailer loyalty + profitability                                                      
                                                                                           Restore loyalty to ≥80%; improve retailer
          3      Retailer health              Loyalty stabilised, below 80% goal; increase in                                       
                                                                                           margins                                  
                                              overdues                                                                              
                                              Net leverage + Free Cash Flow                Trend toward medium term target range of 
          4      Deleveraging & cash                                                                                                
                                              2.73x vs 3.5x SA covenant; negative FCF      1.5 – 2.0x leverage; free cash flow positive
                                                                                                                                    
                                                                                                                                    
                                              ROI on IT investments + cost-to-serve                                                 
          5      Future-fit platform          improvements                                 Stable go-live; lower cost-to-serve      
                                              Various investments ongoing                                                           
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 1155

### [ANALYST QUERY / EMPHASIS]
Scrutinize key accounting policies, unusual movements, and forward guidance.

### [SECTION READING RESPONSE / DETERMINATION]
### 1. Answers to Stored Questions for This Section
*(Omitted — no stored questions were supplied; this is the first captured section.)*

### 2. Footnote & Qualification Deep-Dive

- **`^On a comparable basis` (HEPS –56%)** `[unmapped, physical PDF p. 4]`: The –56% HEPS decline is explicitly flagged as "comparable basis," meaning reported HEPS may differ from –56% due to one-offs (e.g., KZN R123m operating profit impact, Black Friday R212m impact, potential Poland/Switzerland exit residual items, SAP costs). **Must verify** the reconciliation between reported and comparable HEPS, and what items were excluded, in the financial statements/HEPS note.

- **`*Operating profit excluding extraordinary items` (SA operating margin ~1%)** `[unmapped, physical PDF p. 4]`: The ~1% SA operating margin is stated *excluding extraordinary items*. This means the "true" reported SA operating margin could be lower (if extraordinary costs are included) or the ~1% already strips out KZN/BF hits. **Must verify** the definition of "extraordinary items" and whether KZN R123m / BF R212m are inside or outside this ~1%.

- **`^BF overspend of R152m in H1 with margin impact of R60m`** `[unmapped, physical PDF p. 7]`: The R212m headline "impact" decomposes into R152m overspend (cash/marketing cost) + R60m margin impact (GP drag from below-cost pricing/promo rebates). These are **two different P&L lines** (opex vs gross margin) and must not be double-counted. **Must verify** in the income statement/segment note how much of the R212m is in cost of sales vs operating expenses.

- **`[^*]` loyalty footnote** `[unmapped, physical PDF p. 8]`: Footnote text is **partially present** — "*Includes South Africa and foreign countries (Swaziland, Namibia, Mozambique and Botswana)". However, the chart itself is heavily garbled (OCR corruption of axis labels and data labels). Key readable facts: **Average loyalty across all DC regions excluding KZN = 77.90%**; **SA loyalty as at April 2026 = 79.9%**; **Foreign countries loyalty as at April 2026 = 59.4%**. The 59.4% foreign loyalty is a material drag — **must verify** whether foreign (Swaziland/Namibia/Mozambique/Botswana) operations are being assessed for impairment or exit, given the FY25 "portfolio review complete" narrative.

- **Missing footnote definitions**: The page 8 table contains footnote markers `[^a]`, `[^M]`, `[^A]`, `[^l]`, `[^t]`, `[^2]`, `[^i]` embedded in the garbled chart — **the corresponding footnote definitions are NOT present in this section capture**. These cannot be reconstructed and must be checked in later sections (likely the loyalty/operational metrics note or the financial review).

- **"Negative FCF" qualification** `[unmapped, physical PDF p. 15]`: The turnaround tracker states "2.73x vs 3.5x SA covenant; **negative FCF**" — this is a critical qualification. Net leverage of 2.73x is *below* the 3.5x SA covenant (headroom exists), but negative free cash flow means the deleveraging trend toward the 1.5–2.0x target is **not yet supported by cash generation**. **Must verify** the FCF bridge (operating cash flow, working capital absorption, capex, lease payments) in the cash flow statement.

- **"Increase in overdues"** `[unmapped, physical PDF p. 15]`: Retailer health metric explicitly notes "increase in overdues" alongside loyalty below 80%. This is a **credit/debtors book deterioration signal** — must verify gross debtors, impairment allowance (ECL), and satisfactory-paid customer % in the financial review/credit note.

- **"Corporate stores loss reduction"** `[unmapped, physical PDF p. 14]`: Listed as a margin optimisation workstream — implies corporate (company-owned) stores are loss-making. **Must verify** the magnitude of corporate store losses and store count in the segment note.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[unmapped, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q1 | High | Financial review / HEPS note (D00X) | HEPS –56% "on a comparable basis" `[p. 4]` | Reconcile reported HEPS vs comparable HEPS; list all items excluded (KZN, BF, SAP, exit costs) | Determines sustainable earnings base for forecast |
| Q2 | High | Income statement / segment note (D00X) | SA operating margin ~1% "excluding extraordinary items" `[p. 4]` | Confirm whether KZN R123m and BF R212m sit inside or outside the ~1%; get reported SA operating margin | Avoids double-counting one-offs in margin forecast |
| Q3 | High | Cost of sales / margin bridge (D00X) | BF R152m overspend + R60m margin impact `[p. 7]` | Split R212m between COGS (GP drag) and opex (marketing overspend) | Correct gross margin vs opex forecast |
| Q4 | High | Cash flow statement (D00X) | "Negative FCF" `[p. 15]` | Get operating cash flow, working capital movement, capex, IFRS 16 lease payments; compute FCF bridge | Deleveraging forecast depends on FCF turning positive |
| Q5 | High | Debtors / credit note (D00X) | "Increase in overdues" `[p. 15]` | Gross debtors, ECL allowance, satisfactory-paid %, collection rate, write-offs | Credit loss forecast and working capital absorption |
| Q6 | Medium | Segment / store note (D00X) | "Corporate stores loss reduction" `[p. 14]` | Corporate store count, losses, closure/transfer plans | Margin recovery trajectory |
| Q7 | Medium | Operational metrics note (D00X) | Foreign loyalty 59.4% vs SA 79.9% `[p. 8]` | Whether foreign ops (Swaziland, Namibia, Mozambique, Botswana) flagged for impairment/exit | Portfolio simplification risk |
| Q8 | Medium | Loyalty footnote definitions (D00X) | Missing `[^a]`, `[^M]`, `[^A]`, `[^l]`, `[^t]`, `[^2]`, `[^i]` definitions `[p. 8]` | Locate footnote text for loyalty chart markers | Clarifies loyalty methodology/definitions |
| Q9 | Medium | KZN recovery note (D00X) | "3 consecutive months of profit" `[p. 6, p. 15]` | Quantify KZN H2 run-rate profit vs R123m H1 hit; confirm GP% recovery trajectory | H2 earnings recovery assumption |
| Q10 | Medium | Revenue note (D00X) | KZN sales +4.9% y-o-y `[p. 6]`; group retail sales +c.1% `[p. 7]`; transactions –2.3% `[p. 7]` | Reconcile KZN +4.9% vs group +1% vs transactions –2.3% (basket inflation vs volume) | Volume vs price decomposition for revenue forecast |
| Q11 | Low | Ireland segment note (D00X) | Ireland +3% OP margin `[p. 4]` | Ireland revenue, OP, margin; confirm "mainstay" contribution | Segment mix forecast |
| Q12 | Low | SPAR Health / Build it note (D00X) | Health +26% revenue growth; Build it "returned to growth" `[p. 4]` | Absolute revenue and profit contribution of adjacencies | Growth initiative sizing |
| Q13 | Low | SAP / IT note (D00X) | "SAP implementation ongoing"; "various investments ongoing" `[p. 3, p. 15]` | Capitalised vs expensed SAP costs; go-live timeline | Capex and opex forecast |

### 5. Baseline Forecast Inputs Captured Here

| Metric | Value | Source |
| --- | --- | --- |
| Period | 26 weeks ended 27 March 2026 (H1 FY2026) | p. 1 |
| HEPS change | –56% (comparable basis) | p. 4 |
| SA operating margin | ~1% (excl. extraordinary items) | p. 4 |
| Ireland OP margin | +3% | p. 4 |
| KZN operating profit impact | R123m | p. 6 |
| KZN sales growth | +4.9% y-o-y | p. 6 |
| KZN OOS peak | >15% | p. 6 |
| Black Friday total impact | R212m (R152m overspend + R60m margin) | p. 7 |
| Group retail sales growth | c.+1% y-o-y | p. 7 |
| Transactions change | –2.3% | p. 7 |
| Loyalty (all DC excl. KZN) | 77.90% | p. 8 |
| Loyalty SA (Apr 2026) | 79.9% | p. 8 |
| Loyalty foreign (Apr 2026) | 59.4% | p. 8 |
| Loyalty target | ≥80% | p. 7, p. 15 |
| SPAR Health revenue growth | +26% | p. 4 |
| Net leverage | 2.73x (vs 3.5x SA covenant) | p. 15 |
| Leverage target range | 1.5–2.0x | p. 15 |
| Free cash flow | Negative | p. 15 |
| Dividend | Suspended (FY23, per timeline) | p. 3 |

### 6. Next Section to Capture

**Most useful next section: the Financial Review / Income Statement & HEPS reconciliation (D00X).** This will resolve **Q1, Q2, Q3, Q10** (HEPS bridge, extraordinary items definition, BF cost split, revenue decomposition) and likely **Q4** (cash flow) and **Q5** (debtors) if presented together. If the report map separates them, capture the **Income Statement + HEPS note** first, then the **Cash Flow Statement**, then the **Debtors/Credit note**.

================================================================================
## PART 1 - SECTION 2: [unmapped] Financial review - Megan Pydigadu
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section unmapped | [PRES] physical page 16 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                             Financial                review                                                        
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                       Megan     Pydigadu                                                           
                                                                                                                                    
                                                                                                                                    
                                                 Group   Chief  Financial  Officer                                                  
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    

--- Section unmapped | [PRES] physical page 17 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Operating        environment                                                                                                
                                                                                                                                    
                                                                                                                                    
        Navigating trading conditions across our territories                                                                        
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                        South Africa                                                                                
                                                                                                                                    
                                                                                                                                    
                                •  Food inflation softened to 3.4% in Mar 2026 (Sep 2025: 4.4%), signs of acceleration due to high transport
                                   costs                                                                                            
                                                                                                                                    
                                •  Shifting consumer habits towards discount and online channels                                    
                                                                                                                                    
                                •  Informal sector (spaza shops) remains robust                                                     
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                           Ireland                                                                                  
                                                                                                                                    
                                                                                                                                    
                                •  Continued investment in omnichannel and "experiential retail" strategies to attract customers    
                                                                                                                                    
                                •  Labour market remains tight with the unemployment rate of c.4.7% in March 2026                   
                                                                                                                                    
                                                                                                                                    
                                •  Consumer confidence at 3-year low driven by geopolitical concerns and high living costs          
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 17  

--- Section unmapped | [PRES] physical page 18 | area selection | Table ---
Group salient features
On a comparable basis, continuing operations for 26 weeks
R67.5bn R730.7m 199.9cps -R2.0bn

|  |  | Operating profit |  | HEPS |  | Free cash flow |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Group turnover |  | Margin 1.1% |  |  |  |  |  |
| +2.1%  |  H1 FY25 R66.1bn |  |  | -55.6%  |  FY25 450.1cps |  |  | (H1 FY25: +R693.6m) |  |
|  | (H1 FY25: R1 401.1m; Margin 2.1%) |  |  |  |  |  |  |
|  | 11.7% |  | R7.3bn |  | 2.73x |  |  |
|  | ROCE |  | Net debt |  | Gearing ratio |  |  |
|  | Return on capital employed | (FY25: +35.9%; H1 FY25: -24.4%) |  |  | H1 FY25 2.81x  |  SA covenant <3.5x |  |  |
|  |  | INTERIM RESULTS FY2026 |  |  |  |  | 18 |

--- Section unmapped | [PRES] physical page 19 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Group      income      statement        | continuing        comparable                                                      
                                                                                                                                    
                                                                                                                                    
        Margins resilient on muted topline; operating profit pressured by KZN, Black Friday and clean-ups                           
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                        Turnover growth was muted with highly competitive trading
         R'm                                   H1 2026       H1 2025      % change                                                  
                                                                                        conditions in both Southern Africa and Ireland. The South
                                                                                        African operations were up 1.7% and Ireland was up by
                                                                                        2.2% in Euro. Sales were up 1.8% in constant currency.
         Revenue                                  67 482.5     66 078.8        +2.1%                                                
                                                                                        Gross profit margin softened on product mix and
                                                                                        promotional activity related to Black Friday in South Africa &
                                                                                        weak performance in KZN.                    
         Gross profit                              7 134.1      7 088.6                                                             
                                                                               +0.6%                                                
         Margin                                     10.6%        10.7%                                                              
                                                                                        Operating expenses - Significant increase in SA marketing
                                                                                        and selling costs due to investment in Black Friday
         Operating profit before extraordinary                                          campaign. The cost to serve retailers in KZN also saw an
                                                    882.0       1 464.1                 overspend in costs. ECL costs increased due to elevated
         items                                                                -39.8%                                                
                                                    1.3%          2.2%                  specific provisions raised on debtors in SA. Warehousing
         Margin                                                                                                                     
                                                                                        and distribution contained in SA and reduced delivery costs
                                                                                        in Ireland due to lower volumes.            
         Operating profit                           730.7       1 401.1                                                             
                                                                              -47.8%                                                
         Margin                                     1.1%          2.1%                                                              
                                                                                        Extraordinary items include impairments of PPE,
                                                                                        intangibles and goodwill: goodwill and PPE (R72.8m),
                                                                                        software (R30.7m), Build it imports warehouse closure
         Net finance costs                         (362.9)       (366.3)       -0.9%                                                
                                                                                        (R27.5m) and corporate stores sustaining losses (R25.1m).
                                                                                        Net finance expenses lower overall: interest on the
         Profit after tax                           291.7         812.1       -64.1%    assumed Polish debt in SA was offset by lower interest in
                                                                                        Ireland.                                    
                                                         INTERIM RESULTS FY2026                                                 19  

--- Section unmapped | [PRES] physical page 20 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Southern       Africa     | G&L    sales    performance                                                                     
                                                                                                                                    
                                                                                                                                    
        Modest sales growth below inflation, with retailer loyalty stable                                                           
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                  +1.1%                          +1.1%                         +2.6%                          78.5%                 
                                                                                                                                    
            Wholesale revenue growth         Retail sales growth         Internal selling price inflation   Retailer loyalty        
                                                                                                                                    
                 H1 2025: +1.1%                                             Official food CPI: 3.4%          FY25: 78.9%            
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                              Perishables revenue +2.9%                             
                                                                              48-hr local procurement model delivering in KZN       
                              H1 2026          H1 2025          Signal                                                              
                                                                              Dry warehouse revenue flat                            
                                                                              Reflecting continued pressure in core grocery lines   
                                                                                                                                    
        Grocery retail sales  +0.9%            +1.7%            Muted                                                               
                                                                              Liquor                                                
                                                                              LADS^ portfolio shift continues                       
                                                                              Geographical divergence                               
        Liquor retail sales   +2.1%            +2.6%           Resilient      Coastal retail sales growing ahead of inland          
                                                                                                                                    
                                                                              SPAR Rewards: +9.3% YoY reward sales                  
                                                                              Loyalty programme scale building across network       
        G&L Retail LFL*       +1.4%            +1.6%            Muted                                                               
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        G&L - Groceries and Liquor                                                                                                  
        *Like-For-Like                                                                                                              
        ^Low Alcoholic Drinks                                                                                                       
                                                         INTERIM RESULTS FY2026                                                 20  

--- Section unmapped | [PRES] physical page 21 | area selection | Table ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Southern       Africa     | G&L    revenue       trend                                                                      
                                                                                                                                    
                                                                                                                                    
        Promotion-led volume gave way to a genuine margin recovery by February into March                                           
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                               H1 2026: YoY Growth % by Period                     Oct - Nov | Black Friday period                  
                                                                                   • Short-lived lift from the Black Friday campaign over a
                                                                                     two-week campaign period                       
                                                                    2.3%           • Marketing investment drove significant below-cost
                                                              2.1%                                                                  
                                                                                     pricing and promotional subsidies that suppressed
                                                                                     margin sharply                                 
                                       1.0%                                                                                         
                                                                                   Dec - Jan | Christmas and festive period         
                 0.5%                                                                                                               
                                                                                   • Improved sales momentum as festive season      
                                                                                     delivered stronger consumer activity           
                                                                                   • GP remained deeply negative - continued promotional
                                                                                     intensity and KZN margin pressure              
                                                                                                                                    
                                                                                   Feb - Mar | Underlying recovery emerging         
                                                                                   • The most encouraging period: revenue growth    
                                                                                     accelerated to +2.1% and GP growth turned positive
                                                                                     at +2.3%                                       
                                                                                                                                    
                                                                                   • GP recovery reflects early stabilisation in KZN,
                                                                                     reduced promotional drag, and improved category
                                                                                     mix                                            
                                                                                   • However: operating profit materially impacted by ECL
                       -3.7%                 -3.6%                                                                                  
                                                                                     provisions and extraordinary items - recognised as
                   Oct-Nov               Dec-Jan               Feb-Mar                                                              
                                                                                     part of half-year balance sheet review         
                                 Revenue Growth % GP Growth %                                                                       
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 21  

--- Section unmapped | [PRES] physical page 22 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Build    it  | Financial      highlights                                                                                    
                                                                                                                                    
                                                                                                                                    
        Resilient organic retail growth of 6.1% - micro credit tailwind; regional outperformance & network rationalisation ongoing  
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                  R5.2bn                         +1.5%                         +6.1%                          68.1%                 
               Wholesale revenue              Retail sales growth         Organic retail sales growth       Retailer loyalty        
                    +1.3%                                                                                                           
                                                                                                                                    
                 H1 2025: +4.1%                H1 2025: +5.1%                 H1 2025: +5.4%                H1 2025: 67.9%          
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                 Key  performance   drivers & context                                               
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                    Organic growth significantly            Strong growth in SA driven by                                           
                                                                                                    Robust growth in Namibia,       
                    outperforming product                   increased micro credit                                                  
                                                                                                    KZN and Eastern Cape            
                    inflation                               extension                                                               
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 22  

--- Section unmapped | [PRES] physical page 23 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        SPAR      Health      |  Financial      highlights                                                                          
                                                                                                                                    
                                                                                                                                    
        Continued sales growth momentum - profitability behind, driven by deliberate investment cycle                               
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                  137                                                                               
                  R1.2bn                                                                                      65.5%                 
                                                 Stores                                                                             
                                                                               +12.2%                                               
               Total sales revenue                                                                            Loyalty               
                                                                              Scriptwise                                            
                   +26.1%                      (H1 2025: 118)                                               (H1 2025: 58.4%)        
                                                                                                                                    
                                                                                                                                    
                                                 Key performance   drivers & context                                                
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                      Aptekor (WC Pharmacy                                                          Pharmacy at SPAR: Retail turnover
                                                              Scriptwise: #1 position in                                            
                      Wholesaler): Operating as SPAR                                                growth +13.6% YTD (LFL +7.7%) - 
                                                              Patient Support Programmes                                            
                      subsidiary since 1 Nov                                                        outperforming competitors       
                                                                                                                                    
                                                                                                                                    
                                       Profitability impacted by: Planned          Academy: Durban and Pretoria training            
                                       investment over 2026 – 2028 and             labs oversubscribed                              
                                       SEP* annual increases                                                                        
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
       *Single Exit Price                                                                                                           
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 23  

--- Section unmapped | [PRES] physical page 24 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Ireland     (BWG)      | Financial      highlights                                                                          
                                                                                                                                    
                                                                                                                                    
        Solid result against challenging Irish consumer backdrop                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                Sales €856m (+2.2%)                                                 
                                    €117.4m                                                                                         
                                                                • Underlying growth across the business                             
             €855.7m                                                                                                                
                                    Gross profit                                                                                    
                                                                • Continuing strong growth in Foodservice                           
                Sales                 +4.1%                                                                                         
                +2.2%                GP% 13.7%                                                                                      
                                   (H1 2025:13.5%)                                                                                  
                                                                GP margin 13.7% (+20bps)                                            
                                                                • Improved supplier trading terms                                   
                                                                • Improved category mix                                             
              €25.3m                                                                                                                
            Operating profit         €21.2m                                                                                         
                +1.8%                                                                                                               
                                       PBT                                                                                          
                                      +6.2%                                                                                         
              OP% 3.0%                                          Cost control                                                        
             (H1 2025:3.0%)                                                                                                         
                                                                • Payroll and opex budget savings                                   
                                                                • Wage inflation (+3.5%) managed through distribution efficiencies  
             €139.3m                 €96.7m                                                                                         
                                                                Net interest €3.8m (-22.8%)                                         
               Net Debt            Available Facility                                                                               
                                                                • Significant reduction in finance costs as debt deleveraging programme continues
              At 27 Mar 2026        Unused headroom                                                                                 
                                                                • Net debt €139.3m: €44m below 2022 peak                            
            Gearing ratio 2.12x Comfortable covenant position   • Available facility €96.7m - strong headroom                       
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 24  

--- Section unmapped | [PRES] physical page 25 | area selection | Table ---
Operating profit analysis
Operating profit decline driven primarily by 3 factors – KZN, Black Friday and balance sheet clean ups

|  |  |  | Current period anomalies |  |  |  |  |  |  |  | Legacy matters |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | 1 401 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  | -212 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | -123 |  |  |  | 6 | 1 006 |  |  |  |  |  |  |  |  |
|  |  |  |  | -38 |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  | -28 |  |  |  |  |  |  |  |  |  |  |  |  |
| m |  |  |  |  |  |  |  | -143 |  |  |  |  |  |  |  |  |
| ' |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| R |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  | -73 |  |  | 27 | 731 |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  | 704 |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  | -86 |  |  |  |
|  | March 2025 | Black Friday | KZN | Current year Build it |  |  | Other | Operating profit Legacy |  |  | Credit risk Credit risk other |  |  | Trading impacts | MHa1rc 2h0 220626 |  |
|  | H1 2025 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  | impact | performance | impairments SIW closure |  |  |  | after current impairments |  |  | policy change |  |  |  |  |  |
|  |  |  |  |  |  |  |  | period impacts |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  | INTERIM RESULTS FY2026 |  |  |  |  |  |  |  |  | 25 |

--- Section unmapped | [PRES] physical page 26 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        HEPS      &  EPS     reconciliation                                                                                         
                                                                                                                                    
                                                                                                                                    
        HEPS on comparable basis down 55.6%                                                                                         
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                  (R'm)                                 H1 2026  H1 2025 % change   
            Total continuing operations* (cents per share)                                                                          
                                                                                                                                    
                                                                  Profit for the year attributable to equity holders of             
     500'0                                                                                                                          
                                                                  the company                            291.7    799.5   -63.5%    
                                                   450.1                                                                            
     450'0                                                                                                                          
                                            415.1                 Adjusted for:                                                     
                                                                                                         93.3      67.3             
     400'0                                                                                                                          
                                                                  Loss on sale of PPE and intangible assets (26.9) 7.6              
     350'0                                                                                                                          
                                                                  Write back/impairment of assets held for sale 13.1 68.9           
     300'0                                                                                                                          
                                                                  Gain on bargain purchase                (0.7)     -               
     250'0                                                                                                                          
                                                                  Impairment of goodwill                  47.4     2.0              
                         199.9                                                                                                      
     200'0                                                                                                                          
                                                                  Impairment of PPE and intangible assets 41.2      -               
                 151.5                                                                                                              
     150'0                                                                                                                          
                                                                  Impairment to right of use asset       26.9       -               
     100'0                                                                                                                          
                                                                  Gain on disposal of businesses          (0.9)    (11.2)           
     50'0                                                         Tax effect of adjustments               (6.8)     -               
       -                                                                                                                            
                    MH1a r2 0220526           MHa1r 22002265      Headline earnings                      385.0    866.8   -55.9%    
                 Earnings per share Headline earnings per share                                                                     
       *Comparable basis, 182 days                                                                                                  
                                                         INTERIM RESULTS FY2026                                                 26  

--- Section unmapped | [PRES] physical page 27 | area selection | Table ---
Group statement of financial position
Continued optimisation of the balance sheet, enhancing financial quality and resilience

| (R'm) | H1 2026 | FY 2025 |  |  |
| --- | --- | --- | --- | --- |
| ASSETS | 44 848.2 | 46 221.4 |  |  |
| Non-current assets | 19 428.4 | 19 548.0 |  |  |
| Property, plant and equipment | 4 957.2 | 5 071.7 |  |  |
| Right of use assets | 2 654.4 | 2 644.9 |  |  |
| Goodwill and intangible assets | 6 500.2 | 6 424.1 |  |  |
| Other non-current assets[^1] | 5 316.6 | 5 407.3 |  |  |
| Current assets | 25 419.8 | 26 673.4 |  |  |
| Inventories | 4 617.2 | 4 653.1 | Closing exchange rates |  |
| Trade and other receivables | 15 975.2 | 16 107.3 | EUR/ZAR |  |
| Cash and cash equivalents (excl. guild and trusts) | 1 069.5 | 2 327.3 |  |  |
| Other current assets (incl. held for sale)[^1] | 3 757.9 | 3 585.7 | Mar 2026 |  |
| LIABILITIES | (39 446.9) | (40 909.1) | 19.679 |  |
| Non-current liabilities | (13 843.3) | (14 111.9) |  |  |
| Long-term borrowings | (6 403.6) | (6 514.5) | Sep 2025 |  |
| Lease liability | (6 930.4) | (7 075.6) | 20.230 |  |
| Other non-current liabilities | (509.3) | (521.8) |  |  |
| Current liabilities | (25 603.6) | (26 797.2) |  |  |
|  |  |  | % change |  |
| Trade and other payables | (20 561.9) | (22 336.8) |  |  |
|  |  |  | -2.7% |  |
| Bank overdraft | (1 430.7) | (680.2) |  |  |
| Current portion of long-term borrowings | (573.9) | (532.8) |  |  |
| Current portion of lease liability | (1 489.8) | (1 462.0) |  |  |
| Other current liabilities (incl. held for sale) | (1 547.3) | (1 785.4) |  |  |
| EQUITY | (5 401.3) | (5 312.3) |  |  |
| **1. The comparative periods have been restated for the amounts receivable related to bond perfected stores, which were reclassified as current assets from non-current assets.** | | | | |
| Note: The current period and year-end include the UK operations as held for sale. |  |  |  |  |
|  | INTERIM RESULTS FY2026 |  |  | 27 |

--- Section unmapped | [PRES] physical page 28 | area selection | Table ---
Debt overview
Debt and leverage per entity

|  | March 2026 March 2025 Southern Group Ireland Group Southern Africa Ireland Africa |  |  |  |  |  |  |  |  | Switzerland |  |  |  | Net debt (R'm) |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gross Debt | 8 408.2 5 477.1 2 931.1 10 858.3 4 604.5 3 059.1 |  |  |  |  |  |  |  |  | 3 194.7 |  |  |  | 10 001 |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  | 9 748 |  |  |  |  |  |  |  |  |
| Cash | 1 069.5 880.1 189.4 1 147.1 822.0 | 204.9 |  |  |  |  |  |  |  | 120.2 |  |  |  |  | 9 115 |  |  |  |  |
| Net debt | 7 338.7 4 597.0 2 741.7 9 711.2 3 782.5 2 854.2 |  |  |  |  |  |  |  |  | 3 074.5 |  |  |  |  |  |  |  |  |  |
| Debt headroom | 5 567.5 3 873.4 1 694.1 6 023.1 3 756.0 1 929.4 |  |  |  |  |  |  |  |  | 337.7 |  |  |  |  |  |  |  | 7 339 |  |
| Total available |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | 6 637.0 4 753.5 1 883.5 7 170.2 4 578.0 2 134.3 |  |  |  |  |  |  |  |  | 457.9 |  |  |  |  |  |  |  |  |  |
| funding^ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 5 400 |  |  |
| Leverage ratio | 2.73 3.29 2.12 2.81x 2.10x | 2.02x |  |  |  |  |  |  |  | 14.27x |  |  |  |  |  |  |  |  |  |
|  | EURIBOR+[1.05 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Term margins | 3mJ+[1.4-1.7%] -1.2%] 3mJ+[2.15-2.45%] EURIBOR+[1.05-1.2%] SARON+[06.5-2.47%] |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 3mJ hedged rate* | 7.35% 7.35% |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Average funding cost | 9.70% 3.10% 9.30% | 4.30% |  |  |  |  |  |  |  | 1.80% |  |  |  |  |  |  |  |  |  |
| Leverage covenant | 3.50x 3.50x 3.25x | 3.50x |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  | Sep 2022 Sep 2023 |  |  |  | Sep 2024 Sep 2025 |  |  | Mar 2026 |  |
| Interest cover |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | 3.25x 4.00x 3.50x | 4.00x |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| covenant |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ***Hedged rate applies to R800m of funding** | | | | | | | | | | | | | | | | | | | |
| **¹Total available funding includes cash and debt headroom** | | | | | | | | | | | | | | | | | | | |
| • Adequate funding at reporting date; creditor payment run on 30/31 March |  |  |  |  |  |  |  |  |  |  | • Adequate available funding |  |  |  |  |  |  |  |  |
| • Higher leverage year-on-year from Swiss outflow (R670m exit funding; R800m incl. disposal costs) |  |  |  |  |  |  |  |  |  |  | • Higher leverage, mainly as a result of lower |  |  |  |  |  |  |  |  |
| and lower EBITDA on margin compression and higher costs |  |  |  |  |  |  |  |  |  |  | EBITDA due to the increase in operating costs |  |  |  |  |  |  |  |  |
| • Term margins cut from Dec 2025 - Facility A 1.9% to 1.4%, Facility B 2.2% to 1.7% - as a result of |  |  |  |  |  |  |  |  |  |  | year on year |  |  |  |  |  |  |  |  |
| lower Sept 2025 covenant measurement |  |  |  |  |  |  |  |  |  |  | • Funding cost reducing in line with lower |  |  |  |  |  |  |  |  |
| • Funding costs up after terming out part of the overdraft at higher margins (end-March 2025) |  |  |  |  |  |  |  |  |  |  | interest rates |  |  |  |  |  |  |  |  |
|  | INTERIM RESULTS FY2026 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 28 |  |

--- Section unmapped | [PRES] physical page 29 | area selection | Table ---
Group working capital[^*]
Continued focus on working capital management, underpinned strong balance sheet

|  | 30 000 20 000 | 16 264 | 15 442 | 15 216 | 16 107 | 15 975 | 2 000 1 500 |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  | 1 000 |  |
|  | 10 000 |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  | 500 |  |
|  |  | 5 054 | 4 899 | 4 739 | 4 653 | 4 617 |  |  |
| m' | - |  |  |  |  | 31 | - |  |
| R |  |  | ( 49) |  |  |  |  |  |
|  |  | ( 268) |  |  |  |  |  |  |
|  |  |  |  | ( 360) |  |  |  |  |
|  |  |  |  |  |  |  | ( 500) |  |
|  | (10 000) |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  | (1 000) |  |
|  |  |  | (20 391) | (20 316) |  | (20 562) |  |  |
|  | (20 000) | (21 586) |  |  | (22 337) |  |  |  |
|  |  |  |  |  |  |  | (1 500) |  |
|  |  |  |  |  | (1 576) |  |  |  |
|  | (30 000) |  |  |  |  |  | (2 000) |  |
|  |  | Sep 2023 | Sep 2024 | Mar 2025 | Sep 2025 | Mar 2026 |  |  |
|  |  | Inventory | Trade and other receivables | Trade and other payables |  | Net working capital |  |  |
|  | *Excludes Poland and Switzerland |  |  |  |  |  |  |  |
|  |  |  |  | INTERIM RESULTS FY2026 |  |  |  | 29 |

--- Section unmapped | [PRES] physical page 30 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        G&L     debtors’      book                                                                                                  
                                                                                                                                    
                                                                                                                                    
        Overdues signal retailer distress                                                                                           
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                               Mitigants & actions                  
                Item              H1 2026        H1 2025          Trend                                                             
                                                                                        Credit committee oversight intensified      
                                                                                                                                    
                                                                                                                                    
          Total debtor book       R8.9bn          R8.7bn         + Growth                 Early warning indicators in place         
                                                                                                                                    
                                                                                           Monitoring of high-risk stores           
                                                                                           Retail operations teams assisting        
                                                                                               the highest-risk stores              
          Overdues %               15.9%          13.6%          + Higher                                                           
                                                                                        Prioritising direct retailer engagement     
                                                                                       In distressed areas - proactive intervention 
                                                                                                                                    
          Specific impairment                                                                                                       
                                                                 + Higher                                                           
          charge                  R273.1m        R112.5m                                      Monitoring of security                
                                                                                       Monitoring of security relative to credit limits
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 30  

--- Section unmapped | [PRES] physical page 31 | area selection | Table ---
Continuing operations cashflows for the period
Group cashflows is distorted by the inclusion of discontinued operations. Below is a FCF view of continuing operations and net
cashflow post the outflows as a result of the disposal of offshore operations
Southern Africa Ireland Total continuing operations

|  |  | R'm |  |  |  |  | EUR'm |  |  |  | R'm |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | 2026 |  | 2025 2026 |  |  |  |  | 2025 |  | 2026 |  | 2025 |  |  |
| EBITDA (pre IFRS 16) |  | 348.8 | 1 010.7 |  |  |  | 32.2 |  | 31.5 |  | 976.4 | 1 618.9 |  |  |
| Capital expenditure, including retailer contributions | (198.6) |  | (219.5) |  |  |  | (12.3) | (12.1) |  | (438.7) |  | (452.9) |  |  |
| Working capital | (1 227.7) |  | 417.8 |  |  |  | (29.9) | (15.8) |  | (1 811.3) |  |  | 113.0 |  |
| - Net movement in inventories | (75.0) |  | (315.8) |  |  |  | 5.4 |  |  |  | 30.4 | (244.4) |  |  |
|  |  |  |  |  |  |  |  |  | 3.7 |  |  |  |  |  |
| - Net movement in trade and other receivables | (304.8) |  | (472.7) |  |  |  | 6.3 |  | 11.2 | (181.8) |  | (256.6) |  |  |
| - Net movement in trade and other payables | (848.0) |  | 1 206.3 |  |  |  | (41.6) | (30.7) |  | (1 659.8) |  |  | 614.0 |  |
| Taxation | (208.1) |  | (49.5) |  |  |  | (3.6) |  | (2.8) | (278.3) |  | (103.5) |  |  |
| Net interest paid (pre IFRS 16) | (241.5) |  | (218.8) |  |  |  | (1.9) |  | (2.6) | (278.5) |  | (269.0) |  |  |
| Operational cashflows | (1 527.1) |  | 940.8 |  |  |  | (15.5) |  | (1.8) | (1 830.4) |  |  | 906.5 |  |
| Acquisitions of businesses and/subsidiaries | (204.5) |  | (54.7) |  |  |  | (0.5) |  | (8.2) | (214.3) |  | (212.9) |  |  |
| Proceeds from sale of businesses |  | 24.9 |  |  |  |  | 0.4 |  |  |  | 32.7 |  |  |  |
|  |  |  | - |  |  |  |  |  | - |  |  |  | - |  |
| Free cash flow | (1 706.7) |  | 886.1 |  |  |  | (15.6) | (10.0) |  | (2 011.9) |  |  | 693.6 |  |
| Ireland dividend |  | 166.1 |  |  |  |  | (8.5) |  |  |  |  |  |  |  |
|  |  |  | - |  |  |  |  |  | - |  | - |  | - |  |
| Net cash flow | (1 540.7) |  | 886.1 |  |  |  | (24.2) | (10.0) |  | (2 011.9) |  |  | 693.6 |  |
|  |  | INTERIM RESULTS FY2026 |  |  |  |  |  |  |  |  |  |  |  | 31 |

--- Section unmapped | [PRES] physical page 32 | area selection | Table ---
Cash flow generation, including discontinued operations
Cash has been absorbed into operations mainly working capital for H1

| m ' | 2742 | 11 554432 | -1840 |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [^R] |  |  |  |  |  |  |  |  |  | 1237 |  |  |  |  |  |
|  |  |  |  | -369 |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | -179 |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  | -778 |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  | 840 |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  | -279 |  |  |  | -1231 |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  | 136 | 585 |  |
|  |  |  |  |  |  |  |  |  |  |  |  | -397 |  |  |  |
|  | OpHe1n i2n0g2 c5ash | Cash | Net working | Net capital | Net acquisitions/ | Lease | Taxation Cash available |  |  | Proceeds | Debt | Net | Other cash | ClHos1i n2g0 2c6ash |  |
|  | balance | generated from | capital | expenditure | disposals of | obligations | paid to service debt |  |  | from debt | repayments | finance costs | movements | balance |  |
|  |  | operations | movements |  | businesses |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  | INTERIM RESULTS FY2026 |  |  |  |  |  |  |  |  | 32 |

--- Section unmapped | [PRES] physical page 33 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Capital     expenditure                                                                                                     
                                                                                                                                    
                                                                                                                                    
        Disciplined phasing of capex spend | Capex target of - c.1% of revenue remains in place                                     
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                       Group                                                                                                        
                                                                                    • H1 spend on strategic initiatives related to SAP and Omni
                                                                                      initiatives                                   
                                                               43%                                                                  
                                                                            47%                                                     
                                                                    R373m                                                           
                                                                                    • Expansion capex - store acquisition spend of R118m
                                                                                    • Strategic capex in H2 largely relates to SAP finance go-live
                                                                     10%                                                            
                30%             29%                                                                                                 
                                                                                                                                    
                       R659m                                                                                                        
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                       6%                                                           
                                                                   13%                                                              
                                                                                    • Replacement capex - Retailer capital contributions of
                        41%                                                                                                         
                                                                                      EUR3.8m for store revamps                     
                                                                     €15m                                                           
                                                                                    • Strategic projects included the acquisition of a cash and
                                                                                      carry business                                
                                                                     81%                                                            
                                                                                                                                    
                                                                                                                                    
                                        Expansion  Replacement  Strategic                                                           
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 33  

--- Section unmapped | [PRES] physical page 34 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Capital     allocation      | Our    framework                                                                              
                                                                                                                                    
                                                                                                                                    
        Capital is being preserved and directed at recovery - not distributed before the work is done.                              
                                                                                                                                    
                                                                                                                                    
                                                     Our capital hierarchy:                                                         
                                                                                                                                    
                                                                                                                                    
               1   Operational investment & capex 2 Debt reduction & covenant headroom 3 Shareholder returns when sustainable       
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                    Dividends                             Share Buybacks                              Rights Issue                  
                                                                                                                                    
                Remain suspended                       Logical when appropriate                       Not required                  
                                                                                                                                    
                Free cash flow negative              Shares are materially undervalued         Organic levers not yet deployed      
                                                                                                                                    
               Earnings not yet restored            No equity dilution; accretive to HEPS     Adequate funding headroom exists      
                                                                                                                                    
                 Gearing still elevated             Discretionary and conditions-based         Dilution at trough destroys value    
                                                                                                                                    
            Capital preservation is the mandate       Recovery creates the catalyst          Recovery generates the cash internally 
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                   Fleet             Assets           Working capital      Disposals                
        Organic cash levers — not yet fully activated:                                                                              
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 34  

--- Section unmapped | [PRES] physical page 35 | area selection | Table ---
Portfolio optimisation complete | UK disposal
Final milestone in portfolio simplification - AWG (UK) exit completed
APA signed with AF Blakemore - Saltash Depot & 71 Stores. Stores to transfer on phased basis.
Transaction Timeline

| APA signed with AF Blakemore |  | 4 May 2026 |  |
| --- | --- | --- | --- |
| Saltash Depot & 71 stores |  | Core transaction |  |
| Completion — take over Saltash |  | End June 2026 |  |
| Store transfer (phased) |  | Sept 2026 |  |
| Landlord consent required (36 of top 40) |  | Key condition |  |
| 63 remaining stores |  | Terms agreed except 3 |  |
| Forecast H2 trading losses (UK) |  | ~£5m |  |
|  | INTERIM RESULTS FY2026 |  | 35 |

--- Section unmapped | [PRES] physical page 36 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Fuel    cost   risk   &   impact     | South     Africa                                                                     
                                                                                                                                    
                                                                                                                                    
        Fuel is 15 - 18% of warehouse & distribution costs — the single largest controllable cost variable in the DC network        
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                         Macro context                                 Direct cost impact — W&D* fuel spend                         
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                H1 2026: R18.42                                                                                     
              Avg Diesel                                       Cost Line               H1 2026             H1 2025                  
                                H1 2025: R18.67                                                                                     
              (R/liter)                                                                                                             
                                Δ -1.34%                                                                                            
                                                       Total W&D costs (YTD)          R1 709.2m            R1 631.1m                
                                                       Fuel component (15 - 18%)       R254.6m             R247.6m                  
                                H1 2026 : $64.91                                                                                    
              Brent Crude                                                                                                           
                                H1 2025 : $74.82                                                                                    
              (USD/bbl)                                Diesel price (avg R/liter)       R18.42              R16.67                  
                                Δ -13.25%                                                                                           
                                                       Liters consumed                 7 422m L            7 693m L                 
                                H1 2026 : R18.86                                                                                    
              ZAR/USD                                                                                                               
                                H1 2025 : R18.17      *Warehouse & Distribution                                                     
              Average                                                                                                               
                                Δ 2.70%                                                                                             
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 36  

--- Section unmapped | [PRES] physical page 37 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Fuel    cost   risk   &   impact     | Mitigation                                                                           
                                                                                                                                    
                                                                                                                                    
        H1 tailwind | H2 headwind sized and mitigated                                                                               
                                                                                                                                    
                                                                                                                                    
                                                       Contractual Surcharge                   3PL Renegotiation - Group            
               Operational Efficiency                                                                                               
                                                           Pass-Through                                 Scale                       
            • Route optimisation & load                                                                                             
                                                                                                                                    
             consolidation - litres                                                                                                 
                                                                                              • SA + Ireland combined               
             consumed down 3.5% in H1                                                                                               
                                                                                                logistics volume leveraged in       
                                                     • Fuel surcharge mechanisms                                                    
                                                                                                carrier negotiations                
            • Cost per case target: H2                in supply agreements                                                          
             ambition in place                        activated.                                                                    
                                                                                              • KZN: structural shift from          
                                                                                                spot truck hire to owned fleet      
            • Cases per man-hour                     • Retail price adjustment                                                      
                                                                                                - cost certainty restored           
             productivity programme -                 protocol under review to                                                      
             targets reset across all DCs             protect network margins                                                       
                                                                                              • Ireland: H2 headwind                
                                                                                                contained; delivery savings         
            • Fleet additions in KZN                                                                                                
                                                                                                partially offsetting                
             reducing expensive 3PL                                                                                                 
             truck hire dependency                                                                                                  
                       1                                        2                                        3                          
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 37  

--- Section unmapped | [PRES] physical page 38 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Macro      outlook      into  H2                                                                                            
                                                                                                                                    
                                                                                                                                    
        Constrained Macro environment                                                                                               
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                             Fuel increases                                                                         
                Competitive                                                 Interest rate                                           
                                         As a result of Middle East                                         Inflation               
                environment                                                hikes expected                                           
                                                 conflict                                                                           
                                                                             South Africa                                           
           Intensifying price competition      South Africa                                                                         
                                                                       SARB increased interest by                                   
             in SA grocery as chains     Successive fuel hikes in H2 to                             Increases coming through from   
                                                                           25bps in May 2026                                        
            expand discount formats      raise distribution and logistics                                   suppliers               
                                                  costs                                                                             
                                                                               Ireland                                              
           Independent retailers under                                                                                              
                                                                        ECB expected to increase                                    
               margin pressure                   Ireland                                                                            
                                                                       interest by at least 50bps in                                
                                        Fuel cost increases forecast to                                                             
                                                                                2026                                                
           Ireland convenience market        impact costs in H2                                                                     
            remains highly contested                                                                                                
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 38  

--- Section unmapped | [PRES] physical page 39 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Cost    optimisation         | Realignment         programme                                                                
                                                                                                                                    
                                                                                                                                    
        Structural cost reset underway                                                                                              
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                    Cost growth above inflation in H1                                               
                                             Realignment programme  targets H2 improvement                                          
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                Cost review commenced                                                                                               
                                                                                                                   Approved         
                Group wide cost review commenced                                                                                    
                                                                                                                                    
                                                                                                                                    
                Centralised non- trade procurement                                                                In progress       
                Non-trade spend centralisation capturing group leverage on a national basis.                                        
                                                                                                                                    
                                                                                                                                    
                 Distribution Network                                                                                               
                                                                                                                  In Progress       
                Fleet refresh, routing optimisation, targeting logistics cost per case reduction.                                   
                                                                                                                                    
                                                                                                                                    
                                                                                                                    Review          
                Marketing & Advertising                                                                                             
                                                                                                                   Complete         
                Spend rationalised against measurable sales and loyalty outcomes.                                                   
                Employment  Costs & Headcount                                                                                       
                                                                                                                   Ongoing          
                VSP  implemented in the centre, R27.3m cost with annual savings expected of R33.2m. Organisational                  
                design, spans and layers commenced across various functions.                                                        
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 39

### [ANALYST QUERY / EMPHASIS]
Scrutinize key accounting policies, unusual movements, and forward guidance.

### [SECTION READING RESPONSE / DETERMINATION]
### 1. Answers to Stored Questions for This Section

**Q1 [High]: Reconcile reported HEPS vs "comparable basis" HEPS (–56%); list all excluded items (KZN, BF, SAP, exit costs).**
- **Status**: `Resolved`
- **Answer & evidence**: The HEPS reconciliation is provided on [p. 26]. Headline earnings fell 55.9% to R385.0m (H1 2025: R866.8m), and HEPS fell 55.6% to 199.9cps (H1 2025: 450.1cps). The adjustments to profit for the year (R291.7m) to arrive at headline earnings (R385.0m) are: Loss on sale of PPE and intangibles (26.9); Write-back/impairment of assets held for sale 13.1; Gain on bargain purchase (0.7); Impairment of goodwill 47.4; Impairment of PPE and intangibles 41.2; Impairment to right of use asset 26.9; Gain on disposal of businesses (0.9); Tax effect (6.8). Note: The "comparable basis" HEPS of 199.9cps is the headline figure; the KZN, Black Friday, and SAP costs are *not* excluded from HEPS but are embedded in the operating profit line (see Q2/Q3).

**Q2 [High]: Confirm whether KZN R123m and BF R212m sit inside or outside the ~1% SA operating margin "excluding extraordinary items"; get reported SA operating margin.**
- **Status**: `Resolved`
- **Answer & evidence**: The KZN (R123m) and Black Friday (R212m) impacts sit **inside** the "Operating profit before extraordinary items" line of R882.0m (margin 1.3%) on [p. 19]. The extraordinary items (R151.3m total: goodwill/PPE R72.8m, software R30.7m, Build it warehouse closure R27.5m, corporate stores R25.1m) are excluded to arrive at the reported operating profit of R730.7m (margin 1.1%). The SA operating margin is not explicitly stated as a separate line, but the group margin before extraordinary items is 1.3%.

**Q3 [High]: Split BF R212m between COGS/GP drag (R60m) and opex/marketing overspend (R152m).**
- **Status**: `Resolved`
- **Answer & evidence**: The operating profit analysis on [p. 25] shows the Black Friday impact as a single R212m deduction from the H1 2025 operating profit of R1,401m. The commentary on [p. 19] and [p. 21] confirms this was driven by "marketing investment drove significant below-cost pricing and promotional subsidies that suppressed margin sharply" (GP drag) and "significant increase in SA marketing and selling costs" (opex). The exact split is not separately disclosed in the provided evidence, but the total R212m is confirmed as the combined BF impact.

**Q4 [High]: Get operating cash flow, working capital movement, capex, IFRS 16 lease payments; compute FCF bridge to explain "negative FCF".**
- **Status**: `Resolved`
- **Answer & evidence**: The FCF view for continuing operations is on [p. 31]. Key figures (Total continuing operations, R'm): EBITDA (pre IFRS 16) 976.4; Capex (438.7); Working capital (1,811.3); Taxation (278.3); Net interest paid (278.5); Operational cashflows (1,830.4); Acquisitions (214.3); Proceeds from disposals 32.7; **Free cash flow (2,011.9)** vs H1 2025 +693.6. The negative FCF is driven by a massive working capital outflow of R1,811.3m (primarily trade payables R1,659.8m) and lower EBITDA. IFRS 16 lease payments are not separately shown in this FCF table but are included in the cash flow generation chart on [p. 32] (lease obligations -778).

**Q5 [High]: Gross debtors, ECL allowance, satisfactory-paid %, collection rate, write-offs — explain "increase in overdues".**
- **Status**: `Partially resolved (remainder stays open for [Debtors note])`
- **Answer & evidence**: The G&L debtors' book on [p. 30] shows: Total debtor book R8.9bn (H1 2025: R8.7bn); Overdues % 15.9% (H1 2025: 13.6%); Specific impairment charge R273.1m (H1 2025: R112.5m). The commentary attributes the increase to "retailer distress" and notes mitigants (credit committee oversight, early warning indicators, monitoring high-risk stores). ECL allowance, satisfactory-paid %, collection rate, and write-offs are **not** disclosed in this section; these remain open for the debtors/credit note.

**Q6 [Medium]: Corporate store count, losses, closure/transfer plans ("corporate stores loss reduction").**
- **Status**: `Partially resolved (remainder stays open for [Segment/store note])`
- **Answer & evidence**: Extraordinary items on [p. 19] include "corporate stores sustaining losses (R25.1m)". The operating profit analysis on [p. 25] shows a "Legacy matters" column with a R143m deduction, which likely includes corporate store losses, but the exact count and closure/transfer plans are not detailed in this section.

**Q7 [Medium]: Whether foreign ops (Swaziland, Namibia, Mozambique, Botswana — loyalty 59.4%) flagged for impairment/exit.**
- **Status**: `Partially resolved (remainder stays open for [Operational metrics/loyalty note])`
- **Answer & evidence**: The balance sheet note on [p. 27] states "The current period and year-end include the UK operations as held for sale." No mention of Swaziland, Namibia, Mozambique, or Botswana being held for sale or impaired in this section. The portfolio optimisation on [p. 35] focuses on the UK (AWG) exit. This remains open for the operational metrics/loyalty note.

**Q8 [Medium]: Locate missing footnote definitions for loyalty chart markers [^a], [^M], [^A], [^l], [^t], [^2], [^i].**
- **Status**: `Unresolved (carried forward)`
- **Answer & evidence**: The loyalty chart with these markers is not included in this section capture. No footnote definitions are present here.

**Q9 [Medium]: Quantify KZN H2 run-rate profit vs R123m H1 hit; confirm GP% recovery trajectory and "3 consecutive months of profit".**
- **Status**: `Partially resolved (remainder stays open for [KZN recovery note])`
- **Answer & evidence**: The KZN impact of R123m is confirmed on [p. 25]. The revenue trend on [p. 21] shows "Feb - Mar | Underlying recovery emerging" with revenue growth +2.1% and GP growth +2.3%, reflecting "early stabilisation in KZN". The "3 consecutive months of profit" claim is not explicitly stated in this section; this remains open for the KZN recovery note.

**Q10 [Medium]: Reconcile KZN sales +4.9% y-o-y vs group retail sales +c.1% vs transactions –2.3% (volume vs basket inflation).**
- **Status**: `Unresolved (carried forward)`
- **Answer & evidence**: This section does not provide KZN sales growth or transaction volume data. The G&L sales performance on [p. 20] shows SA wholesale revenue +1.1%, retail sales +1.1%, internal selling price inflation +2.6%, and retailer loyalty 78.5%. KZN-specific sales growth is not disclosed here.

**Q11 [Low]: Ireland revenue, OP, margin; confirm +3% OP margin and "mainstay" contribution.**
- **Status**: `Resolved`
- **Answer & evidence**: Ireland (BWG) highlights on [p. 24]: Sales €855.7m (+2.2%); Gross profit €117.4m (+4.1%, GP% 13.7%); Operating profit €25.3m (+1.8%, OP% 3.0%); PBT €21.2m (+6.2%); Net debt €139.3m; Available facility €96.7m; Gearing ratio 2.12x. The +3.0% OP margin is confirmed.

**Q12 [Low]: Absolute revenue and profit contribution of SPAR Health (+26.1% growth) and Build it.**
- **Status**: `Partially resolved (remainder stays open for [Segment note])`
- **Answer & evidence**: SPAR Health on [p. 23]: Total sales revenue R1.2bn (+26.1%); 137 stores; Loyalty 65.5%; Scriptwise +12.2%. Profitability is "behind, driven by deliberate investment cycle" but absolute profit is not disclosed. Build it on [p. 22]: Wholesale revenue R5.2bn (+1.5%); Retail sales growth +6.1%; Organic retail sales growth +6.1%; Retailer loyalty 68.1%. Absolute profit contribution is not disclosed.

**Q13 [Low]: Capitalised vs expensed SAP costs; go-live timeline; "various investments ongoing".**
- **Status**: `Partially resolved (remainder stays open for [SAP/IT/capex note])`
- **Answer & evidence**: Capex on [p. 33] notes "H1 spend on strategic initiatives related to SAP and Omni initiatives" and "Strategic capex in H2 largely relates to SAP finance go-live". The capitalised vs expensed split is not disclosed. The go-live timeline is indicated as H2.

---

### 2. Footnote & Qualification Deep-Dive

- **Footnote [^1] on [p. 27] (Balance Sheet)**: "The comparative periods have been restated for the amounts receivable related to bond perfected stores, which were reclassified as current assets from non-current assets." This reclassification affects "Other non-current assets" (R5,316.6m) and "Other current assets (incl. held for sale)" (R3,757.9m). It does not change total assets or equity but affects working capital and liquidity ratios. **Verification needed**: The quantum of the reclassification is not disclosed; check the full financial statements for the amount.

- **Note on [p. 27]**: "The current period and year-end include the UK operations as held for sale." This means the balance sheet includes UK assets/liabilities in "held for sale" lines. The income statement, however, treats UK as discontinued operations (not in continuing operations). **Verification needed**: Confirm the UK held-for-sale assets/liabilities quantum and whether they are included in the "Other current assets/liabilities" lines.

- **Footnote [^*] on [p. 29] (Working Capital)**: "*Excludes Poland and Switzerland." The working capital chart therefore excludes these disposed/held-for-sale operations. This is consistent with the focus on continuing operations but means the working capital figures are not directly comparable to the group balance sheet, which includes UK held for sale. **Verification needed**: Reconcile the working capital chart to the balance sheet lines.

- **Footnote [^R] on [p. 32] (Cash Flow)**: The marker [^R] appears next to the opening cash balance of 2,742, but the footnote definition is **missing from this section capture**. This is a critical omission as it may explain a restatement or reclassification of opening cash. **Verification needed**: Locate the definition of [^R] in the full financial statements.

- **Footnote * on [p. 28] (Debt Overview)**: "*Hedged rate applies to R800m of funding." This qualifies the 7.35% hedged rate, meaning only R800m of the R8,408.2m gross debt is hedged at that rate. The average funding cost of 9.70% for Southern Africa reflects the unhedged portion. **Verification needed**: Confirm the split between hedged and unhedged debt and the sensitivity to interest rate changes.

- **Footnote ¹ on [p. 28] (Debt Overview)**: "¹Total available funding includes cash and debt headroom." This clarifies that the "Total available funding" line of R6,637.0m (Southern Africa) is the sum of debt headroom (R5,567.5m) and cash (R1,069.5m). This is a liquidity measure, not a debt measure.

- **Qualification on [p. 31] (Cash Flows)**: "Group cashflows is distorted by the inclusion of discontinued operations. Below is a FCF view of continuing operations and net cashflow post the outflows as a result of the disposal of offshore operations." This is a critical qualification: the group cash flow statement includes discontinued operations (UK, Poland, Switzerland), which distorts the FCF picture. The table provided is the clean continuing operations view. **Verification needed**: Reconcile the continuing operations FCF to the group cash flow statement.

- **Qualification on [p. 35] (UK Disposal)**: "Forecast H2 trading losses (UK) ~£5m." This is a forward-looking estimate of the losses from the UK operations that will be incurred in H2 before the disposal completes. This will impact the group's H2 results (as discontinued operations) and should be factored into the full-year forecast.

- **Qualification on [p. 39] (Cost Optimisation)**: "VSP implemented in the centre, R27.3m cost with annual savings expected of R33.2m." This is a one-off cost in H1 (likely in the R143m "Legacy matters" column on [p. 25]) with a future annual benefit. **Verification needed**: Confirm the R27.3m is included in the H1 operating expenses and the phasing of the R33.2m annual savings.

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q14 | High | Debtors / credit note | Specific impairment charge R273.1m vs H1 2025 R112.5m; overdues 15.9% vs 13.6% [p. 30] | Get ECL allowance, satisfactory-paid %, collection rate, write-offs, and ageing analysis. Reconcile to the R273.1m charge. | Credit losses are a major drag on profit; need to forecast future ECL. |
| Q15 | High | Cash flow statement / notes | Footnote [^R] on opening cash balance 2,742 is missing [p. 32] | Locate the definition of [^R] in the full financial statements. | May indicate a restatement or reclassification of cash. |
| Q16 | High | Balance sheet / notes | Footnote [^1] reclassification of bond perfected stores [p. 27] | Quantify the amount reclassified from non-current to current assets. | Affects working capital and liquidity ratios. |
| Q17 | High | Balance sheet / notes | UK operations held for sale [p. 27] | Quantify UK held-for-sale assets and liabilities included in "Other current assets/liabilities". | Affects balance sheet quality and disposal proceeds. |
| Q18 | Medium | Income statement / segment note | "Legacy matters" column R143m on OP analysis [p. 25] | Break down the R143m into its components (corporate stores, VSP, other). | Need to separate one-off from recurring costs. |
| Q19 | Medium | Income statement / segment note | VSP cost R27.3m, annual savings R33.2m [p. 39] | Confirm where the R27.3m is recorded and the phasing of the R33.2m savings. | Affects H2 and FY2027 cost base. |
| Q20 | Medium | KZN recovery note | "3 consecutive months of profit" claim [p. 21] | Confirm the exact months and the profit quantum. | Validates the recovery trajectory for H2. |
| Q21 | Medium | Operational metrics / loyalty note | Foreign ops (Swaziland, Namibia, Mozambique, Botswana) loyalty 59.4% [p. 8] | Check if any of these are flagged for impairment/exit. | Potential further disposals/impairments. |
| Q22 | Medium | SAP / IT / capex note | SAP finance go-live in H2 [p. 33] | Get capitalised vs expensed SAP costs and go-live timeline. | Affects H2 capex and opex. |
| Q23 | Low | Debt overview / notes | Hedged rate applies to R800m of funding [p. 28] | Confirm split of hedged vs unhedged debt and interest rate sensitivity. | Affects finance costs forecast. |
| Q24 | Low | Working capital note | Working capital chart excludes Poland and Switzerland [p. 29] | Reconcile chart to balance sheet lines. | Ensures consistency of working capital forecast. |
| Q25 | Low | UK disposal note | Forecast H2 trading losses (UK) ~£5m [p. 35] | Confirm the phasing and treatment (discontinued ops). | Affects group H2 earnings. |

---

### 5. Baseline Forecast Inputs Captured Here

| Metric | H1 2026 | H1 2025 | % Change |
| --- | --- | --- | --- |
| Group turnover | R67,482.5m | R66,078.8m | +2.1% |
| Gross profit | R7,134.1m | R7,088.6m | +0.6% |
| Gross margin % | 10.6% | 10.7% | -10bps |
| Operating profit before extraordinary items | R882.0m | R1,464.1m | -39.8% |
| OP margin before extraordinary items | 1.3% | 2.2% | -90bps |
| Operating profit (reported) | R730.7m | R1,401.1m | -47.8% |
| OP margin (reported) | 1.1% | 2.1% | -100bps |
| Net finance costs | (R362.9m) | (R366.3m) | -0.9% |
| Profit after tax | R291.7m | R812.1m | -64.1% |
| Headline earnings | R385.0m | R866.8m | -55.9% |
| HEPS | 199.9cps | 450.1cps | -55.6% |
| EPS | 151.5cps | 415.1cps | -63.5% |
| DPS | Suspended | — | — |
| Free cash flow (continuing ops) | (R2,011.9m) | +R693.6m | n/a |
| Net debt | R7,338.7m | R9,711.2m | -24.4% |
| Gearing ratio | 2.73x | 2.81x | — |
| ROCE | 11.7% | 35.9% | — |
| SA wholesale revenue growth | +1.1% | +1.1% | — |
| SA retail sales growth | +1.1% | — | — |
| SA internal selling price inflation | +2.6% | — | — |
| SA retailer loyalty | 78.5% | 78.9% (FY25) | — |
| Build it wholesale revenue | R5.2bn | — | +1.5% |
| Build it retail sales growth | +6.1% | +5.1% | — |
| Build it retailer loyalty | 68.1% | 67.9% | — |
| SPAR Health total sales revenue | R1.2bn | — | +26.1% |
| SPAR Health stores | 137 | 118 | +19 |
| SPAR Health loyalty | 65.5% | 58.4% | — |
| Ireland sales | €855.7m | — | +2.2% |
| Ireland gross profit | €117.4m | — | +4.1% |
| Ireland GP% | 13.7% | 13.5% | +20bps |
| Ireland operating profit | €25.3m | — | +1.8% |
| Ireland OP% | 3.0% | 3.0% | — |
| Ireland PBT | €21.2m | — | +6.2% |
| Ireland net debt | €139.3m | — | — |
| Ireland gearing ratio | 2.12x | — | — |
| G&L total debtor book | R8.9bn | R8.7bn | +2.3% |
| G&L overdues % | 15.9% | 13.6% | +230bps |
| G&L specific impairment charge | R273.1m | R112.5m | +142.8% |
| Capex (continuing ops) | R438.7m | R452.9m | -3.1% |
| Capex target | ~1% of revenue | — | — |
| Inventory | R4,617.2m | R4,653.1m (FY25) | -0.8% |
| Trade receivables | R15,975.2m | R16,107.3m (FY25) | -0.8% |
| Trade payables | R20,561.9m | R22,336.8m (FY25) | -7.9% |
| Cash (excl. guild/trusts) | R1,069.5m | R2,327.3m (FY25) | -54.0% |
| Gross debt | R8,408.2m | R10,858.3m | -22.6% |
| Lease liability (non-current) | R6,930.4m | R7,075.6m (FY25) | -2.1% |
| Lease liability (current) | R1,489.8m | R1,462.0m (FY25) | +1.9% |
| Right-of-use assets | R2,654.4m | R2,644.9m (FY25) | +0.4% |
| Equity | R5,401.3m | R5,312.3m (FY25) | +1.7% |
| VSP cost | R27.3m | — | — |
| VSP annual savings expected | R33.2m | — | — |
| UK H2 forecast trading losses | ~£5m | — | — |
| Fuel component of W&D costs | R254.6m | R247.6m | +2.8% |
| Total W&D costs | R1,709.2m | R1,631.1m | +4.8% |
| Diesel price (avg R/liter) | R18.42 | R16.67 | +10.5% |
| Liters consumed | 7,422m L | 7,693m L | -3.5% |

---

### 6. Next Section to Capture

**Next section to capture: Debtors / credit note (full note in financial statements).**

This will resolve **Q5, Q14** (ECL allowance, satisfactory-paid %, collection rate, write-offs, ageing) and provide the detail needed to forecast credit losses. If the full financial statements are not available, the next most useful section is the **Cash flow statement / notes** to resolve **Q15** (footnote [^R]) and reconcile the FCF bridge.

================================================================================
## PART 1 - SECTION 3: [unmapped] Looking ahead - Reeza Isaacs
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section unmapped | [PRES] physical page 40 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                               Looking                ahead                                                         
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                          Reeza   Isaacs                                                            
                                                                                                                                    
                                                                                                                                    
                                                 Group   Chief  Executive   Officer                                                 
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    

--- Section unmapped | [PRES] physical page 41 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Focus      on   accountability         and    execution                                                                     
                                                                                                                                    
                                                                                                                                    
        Six data points across leadership, operations and the portfolio                                                             
                                                                                                                                    
                                                                                                                                    
                                                                                          Growth momentum                           
                                                                                          Revenue growth accelerated to +2.1% in Feb–Mar
                        New leadership in place                                                                                     
                                                       6                  1               with GP stabilising. The most encouraging trading
      New Group CEO and Group CFO. New MD: G&L                                                                                      
                                                                                          period of H1.                             
      and CMO appointed. Clear accountability in place.                                                                             
                                                                                          Post-period: early signs of progress albeit y-o-y
                                                                                          growth rate impacted by Easter timing.    
                                                                                                                                    
                 3 profitable months in KZN                                                   Increased retailer focus and engagement
         GP%  recovered from Dec/Jan to March. 5                                    2         5 Retailer focus areas identified. Dedicated
         Operating profit positive in the final three                                         retailer committee established with retailer
                            months of H1.                                                     representation. Guild engagements intensified.
                                                                                                                                    
                                                                                              Retailer profitability adopted as the primary
                                                                                              operating metric.                     
                                                                                                                                    
                                                                                                                                    
                    Margin stabilisation in G&L                                                                                     
                                                                                                                                    
           Feb - Mar GP growth turned positive post-                                      Sale of AWG                               
                                                        4                  3                                                        
              Black Friday. Underlying category mix                                       APA signed with AF Blakemore (4 May 2026).
                                  improving.                                              Saltash Depot and 71 stores. Final step in the
                                                                                          three-year portfolio simplification programme -
                                                                                          focus is now entirely on SA and Ireland.  
                                                                                                                                    
                                     Action has been taken and is ongoing. The evidence will be in the numbers.                     
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 41  

--- Section unmapped | [PRES] physical page 42 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        The    case    for  SPAR                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
             2nd largest food retailer*                                                                                             
                                                                                                      Market share                  
                   6 countries                                                                                                      
                  2000+ stores                                                                     Convenience 38% *                
                 1000+ retailers                                                                      *AC Nielsen                   
                                                                                                                                    
            Capital light, working capital                                                                                          
                                                                                                                                    
                    neutral                                                                                                         
                                                                                              #1 Irish voluntary trading group      
          The wholesale model earns before it                                                                                       
                                                                                                by store count (~1 068 stores)      
                    spends                                                                                                          
         Largest building materials supplier                                                                                        
              for independent retailers                                                                  80%                        
                                                                                             BWG Foodservice growth since 2021      
            Strongest liquor brand in SA                                                                                            
                                                                                                                                    
                                                                                                      ~EUR 70m                      
             Footprint provides growth                                                                                              
                                                                                                       EBITDA*                      
            foundation for adjacencies                                                                                              
                                                                                                   *12 months to March 2026         
                               We are fixing what went wrong. We are not changing what makes us different.                          
                                                                                                                                    
         * By retail sales                                                                                                          
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 42  

--- Section unmapped | [PRES] physical page 43 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Recognition         of  our   brands      and    capabilities                                                               
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                         #1                          #1                          #2                         #1                      
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                    Top Job Contributor      Top Private Label Player     Community  Value Index          Industry Awards           
                                                                                                                                    
                    YES (Youth Employment         Advantage Group                 Kantar             Product of the Year 2025 - Juice
                   Service) ESG Awards 2025                                                           Kantar Consumer Survey (2,000+
                                                                                                             respondents)           
                                                                                                            Qualité Award           
                                                                                                      SA Dairy Championships (2025) 
                                                                                                                                    
                                                                                                                                    
                         #1                          #1                          #1                         #1                      
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                     National Foodservice       Sustainable Logistics         Digital Marketing         HR Business Growth          
                     Supplier of The Year        Excellence Award             Excellence Award            Strategy - H2R            
                          CATEX               Business and Finance ESG        SPAR International          HR Leadership &           
                                                   Awards 2026                                          Management Awards           
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 43  

--- Section unmapped | [PRES] physical page 44 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Now     it's about     execution                                                                                            
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                    Behind us                                                       
                                                                                                                                    
                                                                          The heavy lifting is done, but there’s hard               
                                                                          work ahead                                                
                                                                                                                                    
                                                                             •  Portfolio streamlined - focused on South            
                                                                                                                                    
                                                                                Africa & Ireland                                    
                 The model  is sound                                                                                                
                                                                             •  Balance sheet materially strengthened               
                                                                             •  Leadership team in place                            
             •  The independent retailer                                                                                            
                                                                                                                                    
                model                                                                                                               
                                                                                                                                    
             •  Strength of the SPAR brand                          The focus now                                                   
                                                                                                                                    
             •  Market-leading positions                                                                                            
                                                                          The best wholesale & distribution business                
                across key categories                                                                                               
             •  Long-term wholesale &                                       •  Backing independent retailers to compete             
                distribution opportunity                                       and win                                              
                                                                                                                                    
                                                                            •  Restore retailer profitability                       
                                                                            •  Improve wholesale execution and margins              
                                                                                                                                    
                                                                            •  Continue deleveraging                                
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 44

### [ANALYST QUERY / EMPHASIS]
Scrutinize key accounting policies, unusual movements, and forward guidance.

### [SECTION READING RESPONSE / DETERMINATION]
### 1. Answers to Stored Questions for This Section

Review of the `STORED QUESTIONS FROM EARLIER SECTIONS` against the evidence in this capture (physical PDF pp. 40–44, "Looking ahead" / "The case for SPAR" / "Now it's about execution"):

- **Q6 [Medium] — Corporate store count, losses, closure/transfer plans ("corporate stores loss reduction")**:
  - **Status**: `Partially resolved (remainder stays open for later sections)`
  - **Answer & evidence**: No corporate store count or closure/transfer plan is disclosed in this section. The only portfolio action referenced is the **sale of AWG** (APA signed with AF Blakemore 4 May 2026; Saltash Depot and 71 stores), described as "the final step in the three-year portfolio simplification programme — focus is now entirely on SA and Ireland" `[unmapped, physical PDF p. 41]`. This confirms portfolio simplification is complete but does **not** address SA corporate stores. Count, losses and plans remain open.

- **Q7 / Q21 [Medium] — Whether foreign ops (Swaziland, Namibia, Mozambique, Botswana) are flagged for impairment/exit**:
  - **Status**: `Partially resolved (remainder stays open)`
  - **Answer & evidence**: This section states the portfolio is now "focused on South Africa & Ireland" and that AWG sale is "the final step in the three-year portfolio simplification programme" `[unmapped, physical PDF p. 41, p. 44]`. However, the "6 countries" claim on p. 42 `[unmapped, physical PDF p. 42]` is inconsistent with a "SA and Ireland only" focus — implying the Southern Africa regional markets (Namibia, Botswana, Swaziland, Mozambique, etc.) remain in the footprint and are **not** being exited. No impairment/exit flag is stated. Still open for confirmation in segment/PPE notes.

- **Q25 [Low] — Phasing and treatment (discontinued ops) of forecast H2 trading losses (UK) ~£5m**:
  - **Status**: `Partially resolved (remainder stays open)`
  - **Answer & evidence**: The AWG disposal (APA signed 4 May 2026) is confirmed as the final portfolio step `[unmapped, physical PDF p. 41]`. No H2 loss phasing or discontinued-ops presentation is given here. Remains open for the UK disposal note.

- **Q9 / Q20 [Medium] — KZN recovery: "3 consecutive months of profit" and quantum**:
  - **Status**: `Partially resolved (remainder stays open)`
  - **Answer & evidence**: This section states "**3 profitable months in KZN** — GP% recovered from Dec/Jan to March. Operating profit positive in the final three months of H1" `[unmapped, physical PDF p. 41]`. This confirms the months are **Jan, Feb, Mar 2026** (final three months of H1) and that **operating profit** (not just GP) was positive. The **quantum** of that profit is still not disclosed — remains open.

- **Q10 [Medium] — KZN sales +4.9% vs group retail +c.1% vs transactions –2.3%**:
  - **Status**: `Partially resolved (remainder stays open)`
  - **Answer & evidence**: This section adds "Revenue growth accelerated to **+2.1% in Feb–Mar** with GP stabilising. The most encouraging trading period of H1" and "Post-period: early signs of progress albeit y-o-y growth rate impacted by **Easter timing**" `[unmapped, physical PDF p. 41]`. This is group-level, not KZN-specific, and does not reconcile the volume/basket split. Remains open.

- **Q12 [Low] — Absolute revenue and profit contribution of SPAR Health and Build it**:
  - **Status**: `Unresolved in this section` — no mention. Carried forward.

- **Q13 / Q22 [Medium] — Capitalised vs expensed SAP costs; go-live timeline**:
  - **Status**: `Unresolved in this section` — no mention. Carried forward.

- **Q5 / Q14 [High] — ECL allowance, satisfactory-paid %, collection rate, write-offs, ageing**:
  - **Status**: `Unresolved in this section` — no credit book data. Carried forward.

- **Q15 [High] — Footnote [^R] definition (opening cash 2,742)**:
  - **Status**: `Unresolved in this section` — no cash flow note. Carried forward.

- **Q16 / Q17 [High] — Bond perfected stores reclassification; UK held-for-sale assets/liabilities**:
  - **Status**: `Unresolved in this section` — no balance sheet detail. Carried forward.

- **Q18 [Medium] — R143m "Legacy matters" breakdown**:
  - **Status**: `Unresolved in this section` — no OP analysis table. Carried forward.

- **Q19 [Medium] — VSP cost R27.3m location and R33.2m savings phasing**:
  - **Status**: `Unresolved in this section` — no mention. Carried forward.

- **Q8 [Medium] — Missing loyalty chart footnote definitions**:
  - **Status**: `Unresolved in this section` — no loyalty chart. Carried forward.

- **Q23 [Low] — Hedged vs unhedged debt split**:
  - **Status**: `Unresolved in this section` — no debt note. Carried forward.

- **Q24 [Low] — Working capital chart reconciliation**:
  - **Status**: `Unresolved in this section` — no working capital chart. Carried forward.

---

### 2. Footnote & Qualification Deep-Dive

This capture is almost entirely narrative/commentary with **very few footnote markers**. The only footnote markers present are on p. 42:

- **`*` on "2nd largest food retailer*"** and **`* By retail sales`** `[unmapped, physical PDF p. 42]`:
  - The footnote definition **is present** ("By retail sales"). This qualifies the "2nd largest" claim as being measured on **retail sales**, not wholesale/turnover. For forecasting, this means the ranking claim does not translate into a wholesale revenue metric — do not use it as a proxy for group turnover share.

- **`*` on "Convenience 38% *"** with **`*AC Nielsen`** `[unmapped, physical PDF p. 42]`:
  - Definition present: market share sourced from **AC Nielsen**. This is an external, unaudited market-share estimate — treat as directional only, not a forecast input.

- **`*` on "~EUR 70m EBITDA*"** with **`*12 months to March 2026`** `[unmapped, physical PDF p. 42]`:
  - Definition present: the ~EUR 70m EBITDA figure is a **12-month trailing (to March 2026)** metric, **not** an H1 2026 figure. Critical qualification: this is a **BWG/Ireland** EBITDA proxy and is a **rolling 12-month** number. Do not annualise or halve it for H1 modelling. Also note it is an **EBITDA** (pre-IFRS 16? pre-exceptionals?) figure — the basis (pre/post IFRS 16, pre/post exceptionals) is **not stated** and must be verified.

- **`*` on "2nd largest food retailer*"** — second occurrence with **`* By retail sales`** at bottom of p. 42 `[unmapped, physical PDF p. 42]`:
  - Same qualification as above.

**Qualifications embedded in narrative (not footnoted but consequential):**

- **"6 countries" vs "focus is now entirely on SA and Ireland"** `[unmapped, physical PDF p. 41 vs p. 42]`: A direct tension. If the portfolio is "entirely SA and Ireland," the "6 countries" claim must refer to the **retailer/store footprint** (independent retailers operating in neighbouring countries under the SPAR licence) rather than **group-owned operations**. This distinction matters for revenue consolidation vs royalty/fee income. **Verification needed** in the segment note.

- **"Post-period: early signs of progress albeit y-o-y growth rate impacted by Easter timing"** `[unmapped, physical PDF p. 41]`: A forward-looking qualification that **H2 growth will be distorted by Easter timing** (Easter fell in a different period y-o-y). This is a **calendar-shift caveat** — H2 revenue growth may look weaker/stronger purely on Easter phasing. Must be flagged when forecasting H2 and when comparing to H1 +2.1% Feb–Mar run-rate.

- **"Revenue growth accelerated to +2.1% in Feb–Mar"** `[unmapped, physical PDF p. 41]`: This is a **three-month run-rate**, not an H1 average. Do not extrapolate +2.1% as the H1 or FY growth rate without checking the full H1 revenue figure elsewhere.

- **"GP% recovered from Dec/Jan to March"** and **"Operating profit positive in the final three months of H1"** `[unmapped, physical PDF p. 41]`: Confirms KZN returned to **operating profit** (not just GP) in Jan–Mar. But the **quantum** is absent — the R123m H1 hit (from earlier capture) implies the Jan–Mar profit was insufficient to offset Dec/Jan losses. **Verification needed**: the actual Jan–Mar operating profit rand amount to size the H2 run-rate.

- **"Sale of AWG — APA signed with AF Blakemore (4 May 2026). Saltash Depot and 71 stores"** `[unmapped, physical PDF p. 41]`: This is a **post-period event** (4 May 2026, after H1 close). For H1 2026 reporting, AWG remains in **continuing or discontinued operations** depending on IFRS 5 criteria at 31 March 2026. The **71 stores and Saltash Depot** are the disposal perimeter. **Verification needed**: whether AWG is presented as discontinued ops in H1, and the gain/loss on disposal and H2 trading loss phasing (links to Q25).

- **"Balance sheet materially strengthened"** and **"Continue deleveraging"** `[unmapped, physical PDF p. 44]`: Forward-looking capital allocation guidance. **Verification needed**: the actual net debt/EBITDA ratio and deleveraging target to test against the forecast.

- **"Retailer profitability adopted as the primary operating metric"** `[unmapped, physical PDF p. 41]`: A **KPI change** — management is now steering on retailer profitability, not group wholesale margin. This has forecasting implications: wholesale margin may be **sacrificed** to support retailer profitability (e.g., lower wholesale prices, higher rebates), which could compress group GP%. **Verification needed**: any guidance on wholesale margin trade-off.

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q26 | High | Segment note / Ireland | "~EUR 70m EBITDA* — *12 months to March 2026" `[unmapped, p. 42]` | Confirm the **basis** of the EUR 70m EBITDA: pre/post IFRS 16, pre/post exceptionals, and whether it is BWG-only or includes other Ireland ops. Reconcile to the Ireland segment operating profit in the segment note. | Determines whether Ireland EBITDA can be used as a run-rate input or must be adjusted for IFRS 16 and exceptionals. |
| Q27 | High | Segment note / geographic | "6 countries" `[p. 42]` vs "focus is now entirely on SA and Ireland" `[p. 41, p. 44]` | Confirm which entities are consolidated vs which are retailer/licence footprint. Check the geographic segment note for Namibia, Botswana, Swaziland, Mozambique revenue/profit. | Affects revenue consolidation, FX exposure, and whether foreign ops carry impairment risk (links Q7/Q21). |
| Q28 | High | Income statement / discontinued ops note | AWG sale APA signed 4 May 2026; "Saltash Depot and 71 stores" `[p. 41]` | Confirm whether AWG is presented as **discontinued operations** in H1 2026 (IFRS 5), the **gain/loss on disposal**, and the **H2 trading loss phasing** (~£5m per earlier capture). | Drives H2 earnings bridge, HEPS from continuing vs total ops, and DPS sustainability. |
| Q29 | High | Revenue / trading update | "Revenue growth accelerated to +2.1% in Feb–Mar" and "Easter timing" caveat `[p. 41]` | Locate the **full H1 2026 group revenue growth** figure and the **Feb–Mar** run-rate. Confirm the Easter calendar shift impact on H2 y-o-y comparatives. | Prevents over-extrapolating the +2.1% run-rate into H2; Easter shift distorts H2 growth. |
| Q30 | Medium | KZN note / segment | "3 profitable months in KZN — GP% recovered from Dec/Jan to March. Operating profit positive in final three months" `[p. 41]` | Get the **rand quantum** of Jan–Mar KZN operating profit and GP% by month. Reconcile to the R123m H1 hit. | Sizes the H2 KZN run-rate recovery and tests whether the R123m hit is fully recoverable. |
| Q31 | Medium | Income statement / margin note | "Retailer profitability adopted as the primary operating metric" `[p. 41]` | Check whether management guides to a **wholesale GP% trade-off** (lower wholesale margin to support retailer profitability). Look for GP% guidance in the financial review. | Could compress group GP% in H2/FY27 — key margin forecast input. |
| Q32 | Medium | Balance sheet / debt note | "Balance sheet materially strengthened" and "Continue deleveraging" `[p. 44]` | Confirm **net debt/EBITDA ratio** at 31 March 2026 and any stated deleveraging target. | Tests dividend sustainability and capex headroom. |
| Q33 | Low | Store network / operational metrics | "2000+ stores", "1000+ retailers", "~1 068 stores" (Ireland) `[p. 42]` | Reconcile store counts across SA, Ireland, and other regions to the operational metrics section. Confirm net store movement H1 2026. | Store count drives trading space, sales per store, and lease liability forecasts. |
| Q34 | Low | Market share / external data | "Convenience 38% *AC Nielsen" `[p. 42]` | Confirm the **date** of the AC Nielsen data and whether it is SA-only or group. | Directional only; not a forecast input but useful for sanity-checking volume assumptions. |

---

### 5. Baseline Forecast Inputs Captured Here

| Metric | Value | Source |
| --- | --- | --- |
| Group revenue growth, Feb–Mar 2026 run-rate | +2.1% | `[unmapped, p. 41]` |
| KZN profitable months (H1) | Jan, Feb, Mar 2026 (3 months) | `[unmapped, p. 41]` |
| KZN GP% trajectory | Recovered from Dec/Jan to March | `[unmapped, p. 41]` |
| KZN operating profit, Jan–Mar | Positive (quantum not disclosed) | `[unmapped, p. 41]` |
| G&L GP growth | Turned positive Feb–Mar post-Black Friday | `[unmapped, p. 41]` |
| AWG disposal perimeter | Saltash Depot + 71 stores | `[unmapped, p. 41]` |
| AWG APA signing date | 4 May 2026 (post-period) | `[unmapped, p. 41]` |
| Countries in footprint | 6 | `[unmapped, p. 42]` |
| Store count (group) | 2000+ | `[unmapped, p. 42]` |
| Retailer count | 1000+ | `[unmapped, p. 42]` |
| Ireland store count | ~1 068 | `[unmapped, p. 42]` |
| Convenience market share (SA) | 38% (AC Nielsen) | `[unmapped, p. 42]` |
| BWG Foodservice growth since 2021 | 80% | `[unmapped, p. 42]` |
| Ireland EBITDA (12m to March 2026) | ~EUR 70m (basis unstated) | `[unmapped, p. 42]` |
| Portfolio focus post-AWG | SA and Ireland only | `[unmapped, p. 41, p. 44]` |
| Primary operating metric | Retailer profitability | `[unmapped, p. 41]` |
| Capital allocation guidance | Continue deleveraging | `[unmapped, p. 44]` |

---

### 6. Next Section to Capture

**Most useful next section: the Segment Note / Geographic Segment note (or the Income Statement / Discontinued Operations note).**

This will resolve the highest-priority open items:
- **Q26** (EUR 70m EBITDA basis and reconciliation to Ireland segment profit)
- **Q27** ("6 countries" vs "SA and Ireland only" — consolidated vs licence footprint)
- **Q28** (AWG discontinued ops presentation, gain/loss on disposal, H2 loss phasing)
- **Q6** (SA corporate store count and losses)
- **Q12** (SPAR Health and Build it profit contribution)

If the segment note is unavailable, the **Income Statement / Discontinued Operations note** is the next best capture to resolve Q28 and the H2 earnings bridge.

================================================================================
## PART 1 - SECTION 4: [unmapped] Q&A Session
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section unmapped | [PRES] physical page 45 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                      Thank                         
                                                                                                                                    
                                                                                                                                    
                                                                                                         You                        
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                          Q&A                       
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                         IR@spar.co.za              
                                                                                                 www.thespargroup.com/investors     
                                                                                                            JSE: SPP                
                                                                                                       ISIN: ZAE000058517           
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    

--- Section unmapped | [PRES] physical page 46 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                   Important   information    & disclaimer                          
                                                                                                                                    
                                                                                                                                    
                                                                   Forward-looking statements                                       
                                                                   This presentation contains forward-looking statements based on management's
                                                                   current expectations and projections. Actual results may differ materially. SPAR
                                                                                                                                    
                                                                   undertakes no obligation to revise or update these statements.   
                                                                                                                                    
                                                                   Currency                                                         
                                                                   All values in South African Rand (R) unless otherwise stated. Ireland results
                                                                   shown in EUR for operational comparability.                      
                                                                                                                                    
                                                                   Not investment advice                                            
                                                                                                                                    
                                                                   This presentation is for information purposes only and does not constitute an
                                                                   offer or invitation to purchase or subscribe for securities in The SPAR Group
                                                                   Limited.                                                         
                                                                                                                                    
                                                                   Comparable  basis                                                
                                                                   All comparatives are restated to the 26-week calendar basis adopted in FY2025.
                                                                                                                                    
                                                                   Switzerland and UK operations are classified as discontinued (IFRS 5) and
                                                                   excluded from continuing operations in both periods shown.       
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026

### [ANALYST QUERY / EMPHASIS]
Scrutinize key accounting policies, unusual movements, and forward guidance.

### [SECTION READING RESPONSE / DETERMINATION]
### 1. Answers to Stored Questions for This Section

No stored questions can be tested, answered, or partially answered using the evidence in this section. The captured pages (physical PDF pp. 45–46) contain only a Q&A contact/back-cover page and the standard "Important information & disclaimer" boilerplate (forward-looking statements, currency convention, not-investment-advice, comparable-basis note). None of the open ledger items (debtors/ECL, cash flow footnote [^R], bond perfected stores, UK held-for-sale, KZN quantum, Ireland EBITDA basis, AWG discontinued-ops treatment, etc.) are addressed here.

All stored questions remain open and are carried forward in Section 4.

### 2. Footnote & Qualification Deep-Dive

Two qualifications in the disclaimer page are worth flagging because they set the accounting frame for the whole forecast, even though they contain no new numbers:

- **"Comparable basis — All comparatives are restated to the 26-week calendar basis adopted in FY2025."** `[unmapped, physical PDF p. 46]`
  - Implication: any H1 2026 vs H1 2025 growth figure (revenue, GP%, debtor costs) must be checked to confirm both periods are on the 26-week basis. If a prior-period figure in an earlier section was on a 52/53-week or calendar-month basis, the y-o-y comparison is not clean. This directly bears on Q29 (group revenue growth / Feb–Mar run-rate) and Q10 (KZN +4.9% vs group +c.1% vs transactions –2.3%).
  - Must verify in the income statement / segment note whether the restatement is disclosed and whether any "as reported" vs "restated" bridge exists.

- **"Switzerland and UK operations are classified as discontinued (IFRS 5) and excluded from continuing operations in both periods shown."** `[unmapped, physical PDF p. 46]`
  - Implication: this is a direct, explicit confirmation relevant to **Q28** (AWG/UK discontinued-ops presentation) and **Q25** (UK H2 trading losses ~£5m phasing). It confirms UK is IFRS 5 discontinued in both periods — but it does **not** give the gain/loss on disposal, the H2 loss phasing, or the held-for-sale balance sheet quantification (Q17). Those remain open.
  - It also implies Switzerland is discontinued — relevant to **Q24** (working capital chart excludes Poland and Switzerland) and to any segment revenue/profit reconciliation.

- **"Currency — All values in ZAR unless otherwise stated. Ireland results shown in EUR for operational comparability."** `[unmapped, physical PDF p. 46]`
  - Implication: the ~EUR 70m EBITDA figure (Q26) is presented in EUR for "operational comparability" — this does not resolve whether it is pre/post IFRS 16 or pre/post exceptionals. Q26 stays open.

No footnote markers (`[^1]`, `*`) with missing definitions appear on these two pages; the only asterisk-style qualification is the forward-looking statement boilerplate, which carries no numeric content.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q35 | High | Income statement / segment note (unmapped — target the financial statements section) | "All comparatives are restated to the 26-week calendar basis adopted in FY2025" `[unmapped, p. 46]` | Confirm both H1 2026 and H1 2025 revenue, GP, and operating profit are on the 26-week basis; check for any "as reported vs restated" bridge or reclassification note. | Clean y-o-y growth and margin bridge depend on comparable period length; affects Q29, Q10, Q31. |
| Q36 | Medium | Discontinued operations / IFRS 5 note | "Switzerland and UK operations are classified as discontinued (IFRS 5) and excluded from continuing operations in both periods" `[unmapped, p. 46]` | Locate the IFRS 5 note: confirm Switzerland and UK both presented as discontinued; get Switzerland disposal status/gain-loss and any held-for-sale balances (links Q17, Q25, Q28). | Determines whether Switzerland (not just UK/AWG) distorts continuing-ops revenue and net debt. |
| Q37 | Low | Segment / geographic note | "Ireland results shown in EUR for operational comparability" `[unmapped, p. 46]` | Confirm the ZAR/EUR translation rate used and whether the ~EUR 70m EBITDA (Q26) is translated at the same rate as the Ireland segment operating profit. | Needed to reconcile EUR operational figures to ZAR group financials. |

### 5. Baseline Forecast Inputs Captured Here

No new numeric forecast inputs are present on pp. 45–46. Only framing conventions are captured:

| Item | Value / Convention | Source |
| --- | --- | --- |
| Reporting currency | ZAR; Ireland shown in EUR for operational comparability | `[unmapped, p. 46]` |
| Comparable period basis | 26-week calendar basis (adopted FY2025), both periods restated | `[unmapped, p. 46]` |
| Discontinued operations | Switzerland and UK classified IFRS 5, excluded from continuing ops in both periods | `[unmapped, p. 46]` |
| Forward-looking statement caveat | Standard no-obligation-to-update disclaimer | `[unmapped, p. 46]` |
| Investor contact | IR@spar.co.za; www.thespargroup.com/investors; JSE: SPP; ISIN ZAE000058517 | `[unmapped, p. 45]` |

### 6. Next Section to Capture

The most useful next section is the **IFRS 5 / discontinued operations note and the income statement / segment note** (the financial statements section that follows the Q&A). It will resolve **Q28** (AWG discontinued-ops presentation, gain/loss, H2 loss phasing), **Q36** (Switzerland discontinued status and held-for-sale balances), **Q35** (26-week restatement bridge), and feed **Q17** (UK held-for-sale assets/liabilities) and **Q26** (Ireland EBITDA basis reconciliation). If the report map is available, capture the section containing the consolidated income statement and the IFRS 5 note first.

================================================================================
## PART 1 - SECTION 5: [unmapped] Appendices & Supplementary Information
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section unmapped | [PRES] physical page 47 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                    Appendices                                                                      
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    

--- Section unmapped | [PRES] physical page 48 | area selection | Table ---
Appendix 1 | Southern Africa income statement
Muted topline growth; gross margin erosion and higher costs weighed on underlying operating profit

| (R'000s) Income statement | H1 2026 | H1 2025 |  | % change | Turnover grew marginally on prior year, impacted by softer dropshipment volumes and weaker case movement across |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Revenue - sale of merchandise | 50 783 212 | 49 934 547 |  | 1.7% | G&L. Build it faced construction sector pressure and adverse |  |  |
|  |  |  |  |  | weather, with lower consumer loyalty also weighing on |  |  |
| Gross profit | 4 843 195 | 4 912 563 |  | -1.4% | revenue. Health delivered a strong performance. |  |  |
| Gross margin % | 9.5% | 9.8% |  | -3.1% |  |  |  |
| Revenue other+Other income | 887 644 | 576 222 |  | 54.0% |  |  |  |
| Net operating expenses | (5 334 438) | (4 500 262) |  | 18.5% | Gross margin declined on | Other revenue/income |  |
|  |  |  |  |  | product mix and promotional | lifted by the value-added |  |
| Operating profit before extraordinary items | 396 400 | 988 523 |  | -59.9% | activity supporting Black | services platform and the |  |
|  |  |  |  |  | Friday and Christmas. | G&L liquor business. |  |
| Operating profit before extraordinary items margin % | 0.8% | 2.0% |  | -60.6% |  |  |  |
| Extraordinary items | (159 153) | (79 542) |  | 100.1% |  |  |  |
| Operating profit | 237 247 | 908 981 |  | -73.9% | Operating expenses rose across the business — |  |  |
| Operating profit margin % | 0.5% | 1.8% |  | -74.3% | employment and IT costs, higher warehousing and |  |  |
|  |  |  |  |  | distribution to support KZN deliveries, stepped-up marketing |  |  |
| Share of associates profits | 1 364 | 4 449 |  | -69.3% | campaigns, and additional IT and consultancy spend. |  |  |
| Net finance income/(expense) | (289 476) | (272 244) |  | 6.3% |  |  |  |
| (Loss)/profit before tax | (50 864) | 641 186 |  | -107.9% |  |  |  |
| Taxation | (2 400) | (167 467) |  | -98.6% |  |  |  |
|  |  |  |  |  | ECL, debtors write-offs and provisions include additional |  |  |
| (Loss)/profit after tax | (53 264) | 473 720 |  | -111.2% | provisions of R273m (mainly KZN and SR) and R58m of |  |  |
|  |  |  |  |  | write-offs in G&L. |  |  |
| EBITDA (pre IFRS 16) | 697 408 | 1 093 271 |  | -36.2% |  |  |  |
|  | INTERIM RESULTS FY2026 |  |  |  |  |  | 48 |

--- Section unmapped | [PRES] physical page 49 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Appendix        2  | Ireland    income       statement                                                                      
                                                                                                                                    
                                                                                                                                    
        Q2 sales pressured by macro headwinds; gross margin up 20bps on prior year                                                  
                                                                                                                                    
                                                                                                                                    
        (EUR'000)                                    H1 2026         H1 2025     % change                                           
                                                                                                                                    
                                                                                                                                    
                                                                                                   Revenue ahead of prior year. Ireland started
                                                                                                   strongly but February and March were challenging,
        Income statement                                                                                                            
                                                                                                   with severe weather curtailing consumer activity
        Revenue - sale of merchandise                     855 652         836 849            2.2%  and sentiment hitting a three-year low. Further
                                                                                                   interest rate increases and food inflation are
        Gross profit                                      117 385         112 798            4.1%  expected. Softer tobacco volumes weighed on
                                                                                                   revenue, with minimal margin impact.
        Gross margin %                                     13.7%           13.5%             1.8%                                   
        Revenue other+Other income                         14 529          14 152            2.7%  Gross margin % improved year on year. Vaping
                                                                                                   benefited from a regulatory-driven switch from
        Net operating expenses                           (107 031)       (102 271)           4.7%  single-use to longer-life products at higher
                                                                                                   wholesale margin; alcohol delivered well on
        Operating profit before extraordinary items        24 883          24 679            0.8%                                   
                                                                                                   targeted promotions and a shift to ready-to-drink
                                                                                                   cans; tobacco mix was favourable. Margin
        Operating profit before extraordinary items margin % 2.9%           2.9%            -1.4%                                   
                                                                                                   protection remains a priority while continuing to
                                                                                                   offer value to retailers and consumers.
        Extraordinary items                                  403             159           153.5%                                   
        Operating profit                                   25 286          24 838            1.8%  Operating cost growth was contained and only
                                                                                                   slightly above prior year. Warehousing and
        Operating profit margin %                           3.0%            3.0%            -0.4%  distribution benefited from open vacancies and
                                                                                                   lower delivery volumes; admin, IT and depreciation
        Share of associates losses                          (317)              -                                                    
                                                                                                   reflect a change in accounting estimates (YTD
                                                                                                   depreciation catch-up in Nov 2025) and timing on
        Net finance income/(expense)                      (3 763)          (4 874)         -22.8%                                   
                                                                                                   RCC amortisation in Dec 2025.    
        Profit before tax                                  21 206          19 964            6.2%                                   
                                                                                                   Interest savings on lower bank rates year-on-year
        Taxation                                          (3 528)          (3 097)          13.9%  and reduced debt drawn.          
        Profit after tax                                   17 678          16 867            4.8%                                   
                                                                                                   The UK operations are treated as discontinued.
        EBITDA (pre IFRS 16)                               29 773          28 712            3.7%                                   
                                                         INTERIM RESULTS FY2026                                                 49  

--- Section unmapped | [PRES] physical page 50 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Appendix        3  | SPAR     Sri   Lanka     JV                                                                            
                                                                                                                                    
                                                                                                                                    
        Topline growth up on last year underpinned by independent retailer growth but slower than planned store openings; offset    
        by higher establishment and selling and distribution costs                                                                  
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                           Footfall                              Items  sold                                                        
                                                                                                                                    
                           +8%                                   +5%                                                                
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
         (Rs'000)                                                     % change                                                      
                                             H1 2026      H1 2025                                                                   
                                                                                                      Operating profit              
                                                                                                                                    
         Revenue - sale of merchandise         8 341 595    7 751 808       7.6%          Compared to the prior year, there have been significant
                                                                                          increases in establishment of independent retailers (Mar
         Gross profit                          1 618 475    1 527 941       5.9%          2025: 10), with establishment expenses up 14.0%, sales
                                                                                          and distribution (+7.3%) as well as personnel costs
         Operating profit                        40 525      142 223       -71.5%                                                   
                                                                                          (+12.2%) which resulted in a lower operating profit in the
                                                                                          current year compared to prior year.      
         Key performance indicators:                                                                                                
         Gross margin %                          19.4%        19.7%         -1.6%                                                   
         Operating profit %                       0.5%         1.8%        -73.5%                                                   
                                                                                                                                    
                                                                                                                                    
         SPAR Sri Lanka has the following:                                                                                          
         • 12 corporate stores (Sep 2025: 11)                                                                                       
         • 13 independent retailers (Sep 2025: 17)                                                                                  
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 50  

--- Section unmapped | [PRES] physical page 51 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Appendix        4  | UK*   income       statement       - Discontinued                                                      
                                                                                                                                    
                                                                                                      Formatting                    
                                                                                                      of table and                  
        Adverse trading conditions weighed on wholesale and retail sales, resulting in an operating loss of EUR7.4m                 
                                                                                                      slideto be                    
                                                                                                       checked                      
       (EUR'000)                                   H1 2026       H1 2025    % change                                                
                                                                                          Operating performance declined year on year:
                                                                                          Revenues remained under pressure from the UK
                                                                                          cost of living crisis and weak consumer   
       Income statement                                                                                                             
                                                                                          confidence. Wet, cold weather hurt convenience
       Revenue - sale of merchandise                   110 362       123 017     -10.3%                                             
                                                                                          trading, and a quieter Christmas in the Devon and
       Gross profit                                     27 409        32 642     -16.0%   Cornwall coastal holiday areas added further
       Gross margin %                                    24.8%         26.5%      -6.4%   pressure.                                 
       Revenue other+Other income                        2 453         2 667      -8.0%                                             
       Net operating expenses                          (37 016)      (38 314)     -3.4%   Gross margin declined materially on prior year,
       Operating loss before extraordinary items        (7 154)       (3 005)    138.1%   largely on the back of weaker sales.      
       Operating profit before extraordinary items margin % -6.5%      -2.4%     165.4%                                             
       Extraordinary items                               (253)         (217)     16.6%    Operating expenses were lifted by higher retail
                                                                                          labour costs and elevated wastage and leakage.
       Operating loss                                   (7 407)       (3 222)    129.9%                                             
        Operating profit margin %                        -6.7%         -2.6%     156.2%                                             
                                                                                          Operating loss widened significantly on prior year
       Share of associates profits/(losses)                 -             -               on the factors above; the group recorded an
                                                                                          EBITDA loss of c.EUR5.8m for the period.  
       Net finance income/(expense)                     (1 474)       (1 405)     4.9%                                              
       Profit before tax                                (8 881)       (4 627)     91.9%                                             
                                                                                          Extraordinary items include restructuring costs.
       Taxation                                             -             -                                                         
       Profit after tax                                 (8 881)       (4 627)     91.9%                                             
                                                                                                                                    
                                                                                                                                    
       *As reported, 182 days in current period compared to 179 days in prior period An impairment loss of R1.5bn (EUR78.5m) was recognised on held for sale classification.
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 51  

--- Section unmapped | [PRES] physical page 52 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Appendix        5  | Build    it  -  Strategic      Priorities                                                              
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                             Store Growth: New Business Forum                       
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                             Build it 2U (App Commerce)                             
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                             Build it Rewards                                       
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                             Product Mix (CAT 1&2 vs CAT 3&4)                       
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 52  

--- Section unmapped | [PRES] physical page 53 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Appendix        6  | SPAR     Health      -  Strategic      Priorities                                                      
                                                                                                                                    
                                                                                                                                    
        Building the infrastructure for a high-conviction health and pharmacy growth platform                                       
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                          Project 125 - Doubling the Pharmacy Network               
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                  47                              65%+            +27%+             
                                                                                   28                                               
                                                             Pharmacies signed                     Loyalty     Wholesale purchases  
                                                                             Pharmacies launched                                    
                                                                  up                             (P125 stores)      growth          
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                 1                          2                                       
                                                                      Profitability recovery     Aptekor scale-up                   
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                 3    KZN wholesaler license 4    Academy enrolment recovery        
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                 5   Pharmacy Guild &       6     SPAR Rewards in pharmacies        
                                                                     network defence                                                
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 53  

--- Section unmapped | [PRES] physical page 54 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Appendix        7  Pet   Storey     update                                                                                  
                                                                                                                                    
                                                                                                                                    
        Building the platform - Phase 1 of 2 | Pipeline accelerating in H2                                                          
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                     PHASE    1 (now):                  PHASE   2:                  
                                                            1        Brand building,           2        Margin improvement,         
                                                                                                                                    
                                                                     operational foundations,           private label scale,        
                                                                     scalable growth                    sustainable returns         
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                 Own  brand & product               Partnerships & growth           
                                                                                                                                    
                                                                                                                                    
                                                           • Chirp & Chew Bird Seed            • Dotsure Pet Insurance              
                                                                launched; Buildit rollout in progress in-store sales; recurring annuity income to
                                                                                                                                    
                                                           • Pet Storey Biscuit Range          Group                                
                                                                4 flavours / 4 sizes live      • Uber Eats                          
                                                           • Grooming Range                    Boksburg live; rolling out to all stores
                                                                launched                       • Scood Endless Aisle                
                                                           • Interzoo Trade Show               signed; expands range without floor space
                                                                new import & supplier sourcing • Mobile Grooming                    
                                                                                               Boksburg pilot launching July 2026   
                                                                                                                                    
                                                           5% of home brand grooming sales donated to                               
                                                                  SA Blind Dog Association                                          
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 54  

--- Section unmapped | [PRES] physical page 55 | area selection | Table ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Appendix        8  | Returns      on   capital    and    equity                                                             
                                                                                                                                    
                                                                                                                                    
        Continuing operations | Group ROIC 8.3% | ROCE 11.7% | ROE 7.8% | Ireland outperforming SA                                  
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                 Southern Africa                Ireland                     Group                                                   
                                                                                                            ROIC 8.3% and ROCE      
                                                                                                   Group    11.7% - improving       
                                                                                                            trajectory expected in H2.
                                                         17.4%                                                                      
                                                                                                                                    
                                        14.1%                                                                                       
                                                                                                            ROIC 3.7% and ROCE 6.5% 
                                                                                     11.7%                  reflect H1 margin       
                                                                                                            compression; recovery   
                                                                                                            underway.               
                                                                    8.3%                                                            
                                                 7.8%                        7.8%                                                   
                              6.5%                                                                                                  
                                                                                                                                    
             3.7%                                                                                           Strong returns across all
                                                                                                            metrics; ROCE 17.4%     
                                                                                                            reflects high capital   
                                                                                                            efficiency.             
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                               ROIC    ROE    ROCE                                                                  
                                                                                                                                    
                                                                                                                                    
                     -6.8%                                                                                                          
         ROIC - Pre-IFRS 16 Net operating profit after tax (NOPAT) divided by Invested capital (average debt plus average shareholders equity)
         ROE - Pre-IFRS 16 Profit after tax (PAT) divided by average shareholders equity                                            
         ROCE - Pre-IFRS 16 Net operating profit divided by capital employed (average total assets less average current liabilities)
                                                         INTERIM RESULTS FY2026                                                 55  

--- Section unmapped | [PRES] physical page 56 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Appendix        9  | Retail    KPIs    - Southern       Africa    G&L                                                       
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
               Footfall / Number of transactions                                                                                    
                                                                                            Average basket spend                    
                           at till                                                                                                  
                                                                                                                                    
                                                                                                                                    
             Combined                  -2.30%                                          Combined                +3.53%               
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
             Supermarkets                                                             Supermarkets             +3.40%               
                                       -2.35%                                                                                       
                                                                                                                                    
                                                                                                                                    
             TOPS at SPAR Liquor       -2.02%                                         TOPS at SPAR Liquor      +4.20%               
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
       KPIs reflected are based on information shared by our retailers and are considered pro forma – they give a directional view of trading at store level
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 56  

--- Section unmapped | [PRES] physical page 57 | area selection | Commentary ---
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
        Appendix        10   | SAP                                                                                                  
                                                                                                                                    
                                                                                                                                    
        Lessons from KZN applied - every future phase ring-fenced                                                                   
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                          Strategy                         Finance Go-Live                       DC Integration                     
                      Revised H2 FY25                          FY2026                               FY2027                          
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                  Reporting risk closed - lower risk, faster payback           Real-time data                                       
                  Unified chart of accounts goes live in FY2026 before         Readily available DC-level cost data will support real-
                  any DC integration. A unified chart of accounts across       time tracking of margin recovery initiatives         
                                                                                                                                    
                  every DC means one version of the truth. The                                                                      
                  management  reporting gap that allowed KZN to                                                                     
                  deteriorate undetected is structurally closed - earlier                                                           
                  visibility, earlier                                          No increase in capex - sequenced for payback         
                                                                                                                                    
                  intervention                                                 Drop-shipment capability and credit management       
                                                                               enhancements follow post finance go-live -           
                                                                               sequenced to deliver payback before the next phase of
                  Supply chain risk ring-fenced                                                                                     
                                                                               spend is committed. Total capex budget unchanged.    
                  DC integration follows in FY2027 only once the finance                                                            
                  foundation is confirmed stable. The highest-risk phase-                                                           
                  touching retailer ordering and fulfilment - does not                                                              
                  begin until controls are proven.                                                                                  
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                         INTERIM RESULTS FY2026                                                 57  

--- Section unmapped | [PRES] physical page 58 | area selection | Table ---
Appendix 11 | Ireland (BWG)  |  Market Position & Brand Portfolio
The independent convenience and grocery model - a resilient, cash-generative business

| 1 068 Stores across Ireland |  | Irish Voluntary Trading Group By store count | #1 |  | Shoppers every day | 1m+ |  | 38% Largest convenience market share |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | 2 142 |  |  | 9% |  | 98.5% |  |  |  |
|  | People employed |  | Foodservice wholesale |  |  | Service level |  |  |  |
| Across all operations |  |  |  | share | Consistent supplier fill |  |  |  |  |
|  |  |  | Growing channel |  |  |  |  |  |  |
| 650+ |  | 20 |  |  | 127 |  | 80% |  |  |
| Supplier relationships |  | Cash & Carrys |  |  | Retail properties |  | BWG Foodservice |  |  |
| Across all categories |  | Value Centre network |  |  | 102 franchise / 25 |  | growth |  |  |
|  |  |  |  |  | CoCo |  | Since 2021 |  |  |
|  |  |  |  |  | INTERIM RESULTS FY2026 |  |  |  | 58 |

### [ANALYST QUERY / EMPHASIS]
Scrutinize key accounting policies, unusual movements, and forward guidance.

### [SECTION READING RESPONSE / DETERMINATION]
### 1. Answers to Stored Questions for This Section

**Q26 [High]: Confirm basis of "~EUR 70m EBITDA* — *12 months to March 2026" (pre/post IFRS 16, pre/post exceptionals, BWG-only vs all Ireland). Reconcile to Ireland segment operating profit.**
- **Status**: `Partially resolved (remainder stays open for [segment note / basis-of-preparation])`
- **Answer & evidence**: Appendix 2 gives Ireland H1 2026 EBITDA (pre IFRS 16) of EUR 29,773k vs EUR 28,712k prior year (+3.7%) `[unmapped, physical PDF p. 49]`. This is a **six-month** figure and is explicitly **pre IFRS 16**. It does **not** reconcile to the "~EUR 70m EBITDA (12 months to March 2026)" claim — annualising H1 (×2) gives ~EUR 59.6m, leaving a ~EUR 10m gap. The basis (pre/post IFRS 16, pre/post exceptionals, BWG-only vs all-Ireland, and whether the 12-month figure includes a stronger H2) remains **unresolved**. Also note the Appendix 2 heading is "Ireland income statement" and the UK is stated to be treated as discontinued `[unmapped, physical PDF p. 49]`, so the EUR 29.8m appears to be Ireland-continuing only — but this needs confirmation against the segment note.

**Q28 [High]: Confirm whether AWG is presented as discontinued operations in H1 2026 (IFRS 5), gain/loss on disposal, and H2 trading loss phasing (~£5m).**
- **Status**: `Partially resolved (gain/loss and phasing still open)`
- **Answer & evidence**: Appendix 4 is headed "UK* income statement - **Discontinued**" `[unmapped, physical PDF p. 51]`, confirming IFRS 5 discontinued presentation. H1 2026 UK operating loss EUR 7,407k (vs EUR 3,222k), EBITDA loss c.EUR 5.8m, and an **impairment loss of R1.5bn (EUR 78.5m) recognised on held-for-sale classification** `[unmapped, physical PDF p. 51]`. The gain/loss on disposal and the ~£5m H2 trading-loss phasing are **not** in this section — still open.

**Q36 [Medium]: Locate IFRS 5 note: confirm Switzerland and UK both presented as discontinued; get Switzerland disposal status/gain-loss and held-for-sale balances.**
- **Status**: `Partially resolved (Switzerland still open)`
- **Answer & evidence**: UK discontinued confirmed (Appendix 4 heading and footnote) `[unmapped, physical PDF p. 51]`. Switzerland is **not mentioned** anywhere in this Appendices capture — disposal status, gain/loss, and held-for-sale balances remain open.

**Q25 [Low]: Confirm the phasing and treatment (discontinued ops) of forecast H2 trading losses (UK) ~£5m.**
- **Status**: `Partially resolved (phasing still open)`
- **Answer & evidence**: Discontinued treatment confirmed `[unmapped, physical PDF p. 51]`. H1 actual UK operating loss EUR 7.4m is now known; the ~£5m H2 phasing is not addressed here — still open.

**Q33 [Low]: Reconcile store counts (2000+ stores, 1000+ retailers, ~1 068 Ireland stores) to operational metrics; confirm net store movement H1 2026.**
- **Status**: `Partially resolved (net movement still open)`
- **Answer & evidence**: Appendix 11 confirms **1,068 stores across Ireland**, 2,142 people employed, 650+ supplier relationships, 20 Cash & Carry sites, 127 retail properties (102 franchise / 25 CoCo), 38% convenience market share, 98.5% service level, 1m+ shoppers/day `[unmapped, physical PDF p. 58]`. Net store movement H1 2026 is **not** disclosed here — still open.

**Q34 [Low]: Confirm date and scope (SA-only vs group) of "Convenience 38% *AC Nielsen" market share.**
- **Status**: `Partially resolved (date still open)`
- **Answer & evidence**: Appendix 11 states "38% Largest convenience market share" in the **Ireland (BWG)** context `[unmapped, physical PDF p. 58]` — so scope is Ireland, not SA. The Nielsen date/as-at period is not stated — still open.

**Q12 [Low]: Absolute revenue and profit contribution of SPAR Health (+26.1% growth) and Build it.**
- **Status**: `Partially resolved (profit still not disclosed)`
- **Answer & evidence**: Appendix 1 commentary confirms "Health delivered a strong performance" and Build it faced construction-sector pressure and adverse weather `[unmapped, physical PDF p. 48]`. Appendix 6 gives SPAR Health Project 125 metrics: 47 pharmacies signed up, 28 launched, 65%+ loyalty (P125 stores), +27%+ wholesale purchases growth `[unmapped, physical PDF p. 53]`. Absolute revenue/profit by brand still **not** disclosed — open.

**Q13 / Q22 [Low/Medium]: Capitalised vs expensed SAP costs; go-live timeline.**
- **Status**: `Partially resolved (split still open)`
- **Answer & evidence**: Appendix 10 confirms **Finance Go-Live FY2026** (unified chart of accounts before any DC integration), **DC Integration FY2027**, strategy revised H2 FY25, and "**No increase in capex — sequenced for payback. Total capex budget unchanged**" `[unmapped, physical PDF p. 57]`. Capitalised vs expensed split still **not** disclosed — open.

**Q6 [Medium]: Corporate store count, losses, closure/transfer plans.**
- **Status**: `Partially resolved (SA corporate stores still open)`
- **Answer & evidence**: Appendix 3 gives **SPAR Sri Lanka** corporate stores: 12 (Sep 2025: 11) and 13 independent retailers (Sep 2025: 17) `[unmapped, physical PDF p. 50]`. SA corporate store count/losses/plans still **not** addressed — open.

**Q9 / Q20 / Q30 [Medium]: KZN H2 run-rate, rand quantum of Jan–Mar operating profit, GP% by month.**
- **Status**: `Partially resolved (rand quantum still open)`
- **Answer & evidence**: Appendix 1 confirms "ECL, debtors write-offs and provisions include additional provisions of **R273m (mainly KZN and SR)** and **R58m of write-offs in G&L**" `[unmapped, physical PDF p. 48]`. This ties the R273m to KZN and SR (SPAR Retail?) but does **not** give the Jan–Mar KZN operating profit quantum or monthly GP% — still open.

**Q18 [Medium]: Break down the R143m "Legacy matters" column on OP analysis.**
- **Status**: `Partially resolved (components still open)`
- **Answer & evidence**: Appendix 1 extraordinary items rose to R159,153k (vs R79,542k) `[unmapped, physical PDF p. 48]`; the R273m provisions and R58m G&L write-offs are flagged as within ECL/debtors line, not necessarily the R143m legacy column. Component split still **not** given — open.

**Q35 [High]: Confirm both H1 2026 and H1 2025 revenue, GP, and operating profit are on the 26-week calendar basis; check for "as reported vs restated" bridge.**
- **Status**: `Partially resolved (calendar-basis bridge still open)`
- **Answer & evidence**: Appendix 4 footnote states "**As reported, 182 days in current period compared to 179 days in prior period**" `[unmapped, physical PDF p. 51]` — i.e., UK is **not** on a matched 26-week basis. No equivalent day-count footnote appears for Southern Africa (Appendix 1) or Ireland (Appendix 2), so the calendar-basis confirmation for those segments remains open.

**Q37 [Low]: Confirm ZAR/EUR translation rate used and whether ~EUR 70m EBITDA is translated at the same rate as Ireland segment operating profit.**
- **Status**: `Partially resolved (rate still not stated)`
- **Answer & evidence**: Appendix 4 gives the UK impairment as "**R1.5bn (EUR78.5m)**" `[unmapped, physical PDF p. 51]`, implying an implied rate of ~R19.11/EUR. No explicit translation rate is stated for Ireland segment figures — still open.

**Q32 [Medium]: Confirm net debt/EBITDA ratio at 31 March 2026 and any stated deleveraging target.**
- **Status**: `Partially resolved (ratio still open)`
- **Answer & evidence**: Appendix 8 gives **Group ROIC 8.3%, ROCE 11.7%, ROE 7.8%** (continuing operations, pre-IFRS 16) `[unmapped, physical PDF p. 55]`. No net debt/EBITDA ratio or deleveraging target is stated in this section — still open.

**Q23 [Low]: Confirm split of hedged vs unhedged debt and interest rate sensitivity.**
- **Status**: `Not addressed in this section — carried forward`
- **Answer & evidence**: No debt/hedging disclosure in Appendices pp. 47–58.

**Q5 / Q14 [High]: ECL allowance, satisfactory-paid %, collection rate, write-offs, ageing analysis.**
- **Status**: `Partially resolved (write-offs partially quantified; ECL/satisfactory-paid/collection/ageing still open)`
- **Answer & evidence**: Appendix 1 confirms **R273m additional provisions (mainly KZN and SR)** and **R58m write-offs in G&L** `[unmapped, physical PDF p. 48]`. ECL allowance balance, satisfactory-paid %, collection rate, and ageing analysis are **not** in this section — still open.

**Q15 [High]: Definition of footnote [^R] on opening cash balance 2,742.**
- **Status**: `Not addressed in this section — carried forward`

**Q16 / Q17 [High]: Bond perfected stores reclassification; UK held-for-sale assets/liabilities.**
- **Status**: `Partially resolved (UK HFS impairment quantified; balance still open)`
- **Answer & evidence**: UK held-for-sale **impairment loss of R1.5bn (EUR 78.5m)** recognised `[unmapped, physical PDF p. 51]`. The gross HFS asset/liability balances and the bond perfected stores reclassification are **not** quantified here — still open.

**Q7 / Q21 / Q27 [Medium/High]: Foreign ops impairment/exit; "6 countries" vs "SA and Ireland only"; geographic segment note.**
- **Status**: `Partially resolved (Sri Lanka now visible; others still open)`
- **Answer & evidence**: Appendix 3 discloses **SPAR Sri Lanka JV** as a separate reporting appendix with 12 corporate stores and 13 independent retailers `[unmapped, physical PDF p. 50]` — confirming Sri Lanka is a consolidated/JV operation beyond "SA and Ireland only". Namibia, Botswana, Swaziland, Mozambique revenue/profit still **not** disclosed — open.

**Q8 [Medium]: Missing footnote definitions for loyalty chart markers.**
- **Status**: `Not addressed in this section — carried forward`

**Q10 [Medium]: KZN sales +4.9% vs group +c.1% vs transactions –2.3% (volume vs basket).**
- **Status**: `Partially resolved (basket/transaction split now available for SA G&L)`
- **Answer & evidence**: Appendix 9 gives SA G&L retail KPIs: **combined transactions –2.30%** (Supermarkets –2.35%, TOPS at SPAR Liquor –2.02%) and **combined average basket spend +3.53%** (Supermarkets +3.40%, TOPS +4.20%) `[unmapped, physical PDF p. 56]`. This confirms the volume/basket split at SA G&L level (negative volume, positive basket). KZN-specific split still open.

**Q29 [High]: Full H1 2026 group revenue growth and Feb–Mar run-rate; Easter calendar shift.**
- **Status**: `Partially resolved (segment revenue growth now available; group total still open)`
- **Answer & evidence**: Segment revenue growth: **Southern Africa +1.7%** (R50,783,212k) `[unmapped, physical PDF p. 48]`; **Ireland +2.2%** (EUR 855,652k) `[unmapped, physical PDF p. 49]`; **Sri Lanka +7.6%** (Rs 8,341,595k) `[unmapped, physical PDF p. 50]`; **UK –10.3%** (discontinued) `[unmapped, physical PDF p. 51]`. Group consolidated revenue growth and Feb–Mar run-rate still **not** stated — open.

**Q31 [Medium]: Wholesale GP% trade-off from "retailer profitability as primary operating metric".**
- **Status**: `Partially resolved (Ireland GP% up 20bps confirmed)`
- **Answer & evidence**: Appendix 2 confirms Ireland **gross margin 13.7% vs 13.5% (+20bps)** with "Margin protection remains a priority while continuing to offer value to retailers and consumers" `[unmapped, physical PDF p. 49]`. No explicit wholesale GP% trade-off guidance — still open.

**Q19 [Medium]: VSP cost R27.3m recording and R33.2m annual savings phasing.**
- **Status**: `Not addressed in this section — carried forward`

**Q24 [Low]: Reconcile working capital chart (excludes Poland and Switzerland) to balance sheet lines.**
- **Status**: `Not addressed in this section — carried forward`

---

### 2. Footnote & Qualification Deep-Dive

- **Appendix 4 footnote — "As reported, 182 days in current period compared to 179 days in prior period"** `[unmapped, physical PDF p. 51]`. This is a **material calendar mismatch**: the UK discontinued figures are **not** on a like-for-like 26-week basis. The –10.3% revenue decline and widened operating loss are therefore flattered/penalised by 3 extra trading days in H1 2026. Any H2 phasing of the ~£5m loss must be adjusted for this. Also note the slide itself flags "**Formatting of table and slide to be checked**" — treat the UK table as provisional.

- **Appendix 4 footnote — "An impairment loss of R1.5bn (EUR78.5m) was recognised on held for sale classification"** `[unmapped, physical PDF p. 51]`. This is the single largest one-off in the appendices. It sits **below** the operating loss line (not in EBITDA), so it does **not** affect the ~EUR 5.8m UK EBITDA loss but **does** hit group PAT and HEPS. Implied rate ~R19.11/EUR. Must be confirmed as non-recurring and excluded from headline earnings — check the HEPS reconciliation in the income statement/notes.

- **Appendix 1 commentary — "ECL, debtors write-offs and provisions include additional provisions of R273m (mainly KZN and SR) and R58m of write-offs in G&L"** `[unmapped, physical PDF p. 48]`. This is the key credit-quality qualification. It confirms the R273m is **provisions** (not cash write-offs) concentrated in KZN and "SR" (likely SPAR Retail), plus **R58m actual write-offs in G&L**. Critically, it does **not** disclose the ECL allowance balance, satisfactory-paid %, collection rate, or ageing — so the debtors book health (Q5/Q14) remains unquantified. The R273m sits within net operating expenses (hence the +18.5% opex growth), which is why operating profit fell 59.9% despite only 1.7% revenue growth.

- **Appendix 1 — "Revenue other+Other income R887,644k (+54.0%)"** `[unmapped, physical PDF p. 48]`. Commentary attributes the lift to "the value-added services platform and the G&L liquor business." This is a **large, fast-growing other-revenue line** (1.7% of merchandise revenue) that must be decomposed — is it recurring (VSP fees, liquor) or one-off? It materially supports the 9.5% gross margin and 0.8% operating margin.

- **Appendix 2 commentary — "admin, IT and depreciation reflect a change in accounting estimates (YTD depreciation catch-up in Nov 2025) and timing on RCC amortisation in Dec 2025"** `[unmapped, physical PDF p. 49]`. This is an **accounting-estimate change** embedded in Ireland opex (+4.7%). It means the Ireland cost base is not cleanly comparable y-o-y; the +0.8% operating profit growth is partly flattered/penalised by this catch-up. Must be quantified and stripped out for a clean run-rate.

- **Appendix 2 — "The UK operations are treated as discontinued"** `[unmapped, physical PDF p. 49]`. Confirms Ireland segment figures are **continuing-only**; the ~EUR 70m EBITDA claim (Q26) must be checked to see whether it includes or excludes UK.

- **Appendix 3 — SPAR Sri Lanka: "significant increases in establishment of independent retailers (Mar 2025: 10)... establishment expenses up 14.0%, sales and distribution (+7.3%), personnel (+12.2%)... lower operating profit"** `[unmapped, physical PDF p. 50]`. Operating profit collapsed –71.5% to Rs 40,525k on +7.6% revenue. This is a **JV (equity-accounted?)** — confirm whether it flows through "share of associates" or is consolidated. Store mix shifted: corporate stores up (11→12), independent retailers down (17→13) — a **franchise-to-corporate mix shift** that raises cost base.

- **Appendix 8 footnotes — ROIC/ROE/ROCE definitions all "Pre-IFRS 16"** `[unmapped, physical PDF p. 55]`. Group ROIC 8.3%, ROCE 11.7%, ROE 7.8%; Southern Africa ROIC 3.7%, ROCE 6.5%, ROE –6.8% (negative ROE!); Ireland ROIC 14.1%, ROCE 17.4%, ROE 7.8%. The **negative Southern Africa ROE (–6.8%)** is a red flag consistent with the R273m provisions driving a segment loss. "Improving trajectory expected in H2" is forward guidance with no quantum.

- **Appendix 9 footnote — "KPIs reflected are based on information shared by our retailers and are considered pro forma – they give a directional view of trading at store level"** `[unmapped, physical PDF p. 56]`. This is a **critical qualification**: the –2.30% transactions and +3.53% basket figures are **pro forma, retailer-supplied, directional only** — not audited group sales. Do not use them to reconcile to group revenue without caveat.

- **Appendix 10 — "No increase in capex — sequenced for payback. Total capex budget unchanged"** `[unmapped, physical PDF p. 57]`. Forward guidance: Finance Go-Live FY2026, DC Integration FY2027. Confirms SAP capex is **within existing budget** (no incremental capex), but the capitalised vs expensed split (Q13/Q22) is still not given.

- **Appendix 11 — "38% Largest convenience market share"** `[unmapped, physical PDF p. 58]`. Scope is **Ireland** (BWG), not SA. No Nielsen date given. 1,068 stores, 2,142 employees, 98.5% service level, 1m+ shoppers/day, 20 Cash & Carrys, 127 retail properties (102 franchise / 25 CoCo).

- **Appendix 5 & 7 (Build it, Pet Storey)** `[unmapped, physical PDF pp. 52, 54]`. Strategic-priority slides with **no financial figures** — qualitative only. Pet Storey Phase 1/2, mobile grooming pilot July 2026, Uber Eats Boksburg live. No revenue/profit contribution disclosed.

- **Appendix 6 (SPAR Health)** `[unmapped, physical PDF p. 53]`. Project 125: 47 pharmacies signed, 28 launched, 65%+ loyalty, +27%+ wholesale purchases growth. Six priorities listed (profitability recovery, Aptekor scale-up, KZN wholesaler license, Academy enrolment recovery, Pharmacy Guild defence, SPAR Rewards in pharmacies). **No rand figures** — cannot size the +26.1% growth contribution.

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q38 | High | Income statement / HEPS note | UK HFS impairment R1.5bn (EUR78.5m) `[unmapped, p. 51]` | Confirm impairment is excluded from headline earnings; locate HEPS reconciliation showing the R1.5bn as a non-headline item; confirm no further HFS write-down expected in H2 | Determines HEPS vs EPS gap and dividend cover; a second write-down would hit FY2026 PAT |
| Q39 | High | Debtors / credit note | R273m additional provisions (KZN, SR) + R58m G&L write-offs `[unmapped, p. 48]` | Get ECL allowance balance, satisfactory-paid %, collection rate, ageing buckets; confirm whether R273m is specific or portfolio ECL; check if further provisioning guided for H2 | Credit book health is the biggest swing factor in SA profitability; R273m is ~3% of R8.9bn book |
| Q40 | High | Segment / geographic note | Sri Lanka JV operating profit –71.5% `[unmapped, p. 50]` | Confirm whether Sri Lanka is equity-accounted (share of associates) or consolidated; get its contribution to group operating profit and whether it sits in "6 countries" | Determines whether Sri Lanka drags group EBIT directly or via associates line |
| Q41 | High | Ireland segment / basis of preparation | ~EUR 70m EBITDA (12m to Mar 2026) vs H1 EUR 29.8m annualised ~EUR 59.6m `[unmapped, p. 49]` | Reconcile the ~EUR 10m gap: is the 12m figure pre/post IFRS 16, pre/post exceptionals, BWG-only vs all-Ireland, and does it include a stronger H2? | Ireland is the group's profit engine; mis-sizing EBITDA distorts group valuation and net debt/EBITDA |
| Q42 | High | Income statement / notes | "Change in accounting estimates (YTD depreciation catch-up Nov 2025; RCC amortisation timing Dec 2025)" `[unmapped, p. 49]` | Quantify the rand/EUR impact of the depreciation catch-up and RCC amortisation timing on Ireland opex; confirm whether it recurs in H2 | Ireland opex +4.7% is partly an accounting artefact; clean run-rate needed for H2 forecast |
| Q43 | Medium | Income statement / other revenue note | Other revenue +54.0% to R887.6m (VSP + G&L liquor) `[unmapped, p. 48]` | Decompose other revenue into VSP fees, liquor, and other; confirm recurring vs one-off; check treatment in gross profit vs operating income | Other revenue is 1.7% of merchandise sales and supports the 9.5% GP margin; sustainability affects margin forecast |
| Q44 | Medium | Discontinued ops / IFRS 5 note | UK 182 vs 179 days `[unmapped, p. 51]` | Confirm H1 2025 UK comparatives are not restated to 182 days; quantify the 3-day revenue/loss impact; check H2 ~£5m loss phasing on a matched-day basis | Day-count mismatch distorts UK y-o-y and H2 phasing of discontinued losses |
| Q45 | Medium | Discontinued ops / IFRS 5 note | Switzerland not mentioned in Appendices `[unmapped, pp. 47–58]` | Locate Switzerland disposal status, gain/loss, and held-for-sale balances; confirm both UK and Switzerland in discontinued | Completes the IFRS 5 picture and one-off items for FY2026 |
| Q46 | Medium | Balance sheet / notes | UK HFS impairment R1.5bn `[unmapped, p. 51]` | Get gross HFS assets and liabilities for UK at 31 Mar 2026; confirm net carrying value after R1.5bn impairment | Needed for net asset value and disposal proceeds reconciliation |
| Q47 | Medium | Capex / SAP note | "No increase in capex — total capex budget unchanged" `[unmapped, p. 57]` | Get capitalised vs expensed SAP split for H1 2026 and FY2026 guidance; confirm Finance Go-Live FY2026 timing and DC Integration FY2027 | SAP spend affects capex, depreciation, and opex; "unchanged budget" needs a number |
| Q48 | Medium | Operational metrics / segment note | SA G&L transactions –2.30%, basket +3.53% (pro forma) `[unmapped, p. 56]` | Reconcile pro-forma retailer KPIs to group SA revenue +1.7%; confirm KZN-specific transaction/basket split | Volume vs basket inflation drives SA revenue and margin forecast |
| Q49 | Medium | Store network / operational metrics | Ireland 1,068 stores; Sri Lanka 12 corporate + 13 independent `[unmapped, pp. 50, 58]` | Get net store movement H1 2026 by segment (SA, Ireland, Sri Lanka); confirm total group store count | Store count drives trading space, sales per store, and lease liabilities |
| Q50 | Low | Segment note | Southern Africa ROE –6.8% `[unmapped, p. 55]` | Confirm SA segment PAT and equity base; reconcile negative ROE to the R273m provisions and R159m extraordinary items | Negative ROE signals capital destruction; affects group ROE and dividend capacity |
| Q51 | Low | SPAR Health / segment note | Project 125: 47 signed, 28 launched, +27% wholesale growth `[unmapped, p. 53]` | Get SPAR Health absolute revenue and profit; confirm +26.1% growth base and H2 run-rate | Sizes the health platform contribution to SA revenue/margin |
| Q52 | Low | Market share / Ireland note | "38% convenience market share" `[unmapped, p. 58]` | Confirm Nielsen date/as-at period and whether 38% is value or volume, Republic of Ireland only | Context for Ireland growth ceiling and competitive position |

---

### 5. Baseline Forecast Inputs Captured Here

| Metric | Value | Source |
| --- | --- | --- |
| **Southern Africa (Appendix 1)** | | `[p. 48]` |
| Revenue — sale of merchandise | R50,783,212k (+1.7%) | |
| Gross profit | R4,843,195k (–1.4%) | |
| Gross margin % | 9.5% (vs 9.8%) | |
| Revenue other + other income | R887,644k (+54.0%) | |
| Net operating expenses | (R5,334,438k) (+18.5%) | |
| Operating profit before extraordinary items | R396,400k (–59.9%) | |
| OP before extraordinary margin % | 0.8% (vs 2.0%) | |
| Extraordinary items | (R159,153k) | |
| Operating profit | R237,247k (–73.9%) | |
| Share of associates | R1,364k | |
| Net finance expense | (R289,476k) | |
| (Loss)/profit before tax | (R50,864k) | |
| Taxation | (R2,400k) | |
| (Loss)/profit after tax | (R53,264k) | |
| EBITDA (pre IFRS 16) | R697,408k (–36.2%) | |
| Additional provisions (KZN, SR) | R273m | |
| G&L write-offs | R58m | |
| **Ireland (Appendix 2)** | | `[p. 49]` |
| Revenue — sale of merchandise | EUR 855,652k (+2.2%) | |
| Gross profit | EUR 117,385k (+4.1%) | |
| Gross margin % | 13.7% (vs 13.5%) | |
| Revenue other + other income | EUR 14,529k (+2.7%) | |
| Net operating expenses | (EUR 107,031k) (+4.7%) | |
| Operating profit before extraordinary items | EUR 24,883k (+0.8%) | |
| OP before extraordinary margin % | 2.9% | |
| Extraordinary items | EUR 403k | |
| Operating profit | EUR 25,286k (+1.8%) | |
| Share of associates losses | (EUR 317k) | |
| Net finance expense | (EUR 3,763k) | |
| Profit before tax | EUR 21,206k (+6.2%) | |
| Taxation | (EUR 3,528k) | |
| Profit after tax | EUR 17,678k (+4.8%) | |
| EBITDA (pre IFRS 16) | EUR 29,773k (+3.7%) | |
| **SPAR Sri Lanka JV (Appendix 3)** | | `[p. 50]` |
| Revenue — sale of merchandise | Rs 8,341,595k (+7.6%) | |
| Gross profit | Rs 1,618,475k (+5.9%) | |
| Gross margin % | 19.4% (vs 19.7%) | |
| Operating profit | Rs 40,525k (–71.5%) | |
| Operating profit % | 0.5% (vs 1.8%) | |
| Corporate stores | 12 (Sep 2025: 11) | |
| Independent retailers | 13 (Sep 2025: 17) | |
| Footfall / items sold | +8% / +5% | |
| **UK — Discontinued (Appendix 4)** | | `[p. 51]` |
| Revenue — sale of merchandise | EUR 110,362k (–10.3%) | |
| Gross profit | EUR 27,409k (–16.0%) | |
| Gross margin % | 24.8% (vs 26.5%) | |
| Revenue other + other income | EUR 2,453k (–8.0%) | |
| Net operating expenses | (EUR 37,016k) (–3.4%) | |
| Operating loss before extraordinary items | (EUR 7,154k) | |
| Extraordinary items | (EUR 253k) | |
| Operating loss | (EUR 7,407k) | |
| Net finance expense | (EUR 1,474k) | |
| Profit after tax | (EUR 8,881k) | |
| EBITDA loss | c.EUR 5.8m | |
| HFS impairment loss | R1.5bn (EUR 78.5m) | |
| Day count | 182 (H1 2026) vs 179 (H1 2025) | |
| **Returns (Appendix 8)** | | `[p. 55]` |
| Group ROIC / ROCE / ROE | 8.3% / 11.7% / 7.8% | |
| Southern Africa ROIC / ROCE / ROE | 3.7% / 6.5% / –6.8% | |
| Ireland ROIC / ROCE / ROE | 14.1% / 17.4% / 7.8% | |
| **SA G&L Retail KPIs (Appendix 9, pro forma)** | | `[p. 56]` |
| Combined transactions | –2.30% | |
| Supermarkets transactions | –2.35% | |
| TOPS at SPAR Liquor transactions | –2.02% | |
| Combined average basket spend | +3.53% | |
| Supermarkets basket | +3.40% | |
| TOPS at SPAR Liquor basket | +4.20% | |
| **SAP (Appendix 10)** | | `[p. 57]` |
| Strategy revised | H2 FY25 | |
| Finance Go-Live | FY2026 | |
| DC Integration | FY2027 | |
| Capex | No increase; total budget unchanged | |
| **Ireland BWG (Appendix 11)** | | `[p. 58]` |
| Stores across Ireland | 1,068 | |
| People employed | 2,142 | |
| Supplier relationships | 650+ | |
| Cash & Carry sites | 20 | |
| Retail properties | 127 (102 franchise / 25 CoCo) | |
| Convenience market share | 38% (#1) | |
| Service level | 98.5% | |
| Shoppers per day | 1m+ | |
| Foodservice wholesale share | 9% | |
| BWG Foodservice growth since 2021 | 80% | |
| **SPAR Health (Appendix 6)** | | `[p. 53]` |
| Pharmacies signed (P125) | 47 | |
| Pharmacies launched | 28 | |
| Loyalty (P125 stores) | 65%+ | |
| Wholesale purchases growth | +27%+ | |

---

### 6. Next Section to Capture

**Next section to capture: the consolidated income statement / HEPS reconciliation and the IFRS 5 discontinued-operations note** (the section containing the group income statement, headline earnings per share reconciliation, and the note on discontinued operations / held-for-sale).

This will resolve the highest-priority open items:
- **Q38** (UK R1.5bn impairment excluded from HEPS; no further H2 write-down)
- **Q28 / Q45** (gain/loss on disposal; Switzerland discontinued status)
- **Q46** (gross UK HFS assets/liabilities)
- **Q35** (as-reported vs restated bridge; calendar basis)
- **Q29** (full group revenue growth and Feb–Mar run-rate)
- **Q26 / Q37** (Ireland EBITDA basis and translation rate)

If the consolidated income statement is not available, the **debtors/credit note** (for Q5/Q14/Q39) is the next most valuable capture, as the R273m provisioning is the single largest driver of the SA profit collapse.

================================================================================
## PART 2: AFS FINANCIAL STATEMENTS & NOTES (`Unaudited_interim_results_for_the_26_weeks_ended_27_March_2026.pdf` — 2 Sections)
================================================================================

================================================================================
## PART 2 (AFS) - SECTION 1: [unmapped] Primary financial statements
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section unmapped | [AFS] physical page 4 | area selection | Table ---
THE SPAR GROUP LTD
INTERIM FINANCIAL
RESULTS 2026
Condensed consolidated
statement of profit or loss and
other comprehensive income

|  |  | Unaudited for the 26 weeks ended | Unaudited for the 26 weeks ended | Audited Year ended |  |
| --- | --- | --- | --- | --- | --- |
|  |  | 27 March | 28 March 26 September |  |  |
| Rmillion | Notes | 2026 | 2025 | 2025 |  |
| Continuing operations |  |  |  |  |  |
| Revenue – sale of merchandise | 3 | 67 482.5 | 65 160.2 | 131 457.7 |  |
| Cost of sales |  | (60 370.8) | (58 162.2) | (117 312.9) |  |
| Gross profit |  | 7 111.7 | 6 998.0 | 14 144.8 |  |
| Revenue – other | 3 | 1 109.6 | 730.2 | 1 950.6 |  |
| Other income |  | 61.6 | 104.0 | 171.8 |  |
| Net operating expenses |  | (7 542.4) | (6 478.5) | (14 283.7) |  |
| Operating profit |  | 740.5 | 1 353.7 | 1 983.5 |  |
| Other non-operating items | 6.5 | (9.8) | (2.2) | (8.9) |  |
| Finance income |  | 304.6 | 307.3 | 613.8 |  |
| Finance costs |  | (667.5) | (669.0) | (1 304.8) |  |
| Share of equity-accounted associate (losses)/profits |  | (4.8) | 4.4 | 4.2 |  |
| Profit before taxation |  | 363.0 | 994.2 | 1 287.8 |  |
| Taxation |  | (71.3) | (226.1) | (468.0) |  |
| Profit after taxation from continuing operations |  | 291.7 | 768.1 | 819.8 |  |
| Discontinued operations | 9 | (144.4) | (5 026.4) | (5 647.9) |  |
| Profit/(loss) after taxation for the period |  | 147.3 | (4 258.3) | (4 828.1) |  |
| Attributable to: |  |  |  |  |  |
| Equity holders of the Company |  | 147.3 | (4 258.3) | (4 828.1) |  |
| Profit/(loss) after taxation attributable to owners: |  | 147.3 | (4 258.3) | (4 828.1) |  |
| From: |  |  |  |  |  |
| Continuing operations |  | 291.7 | 768.1 | 819.8 |  |
| Discontinued operations |  | (144.4) | (5 026.4) | (5 647.9) |  |
| Items that will not be reclassified subsequently to profit or loss: |  |  |  |  |  |
| Remeasurement of employee benefits |  | – | – | 10.0 |  |
| Deferred tax relating to remeasurement of employee benefits |  | – | – | (2.7) |  |
| Remeasurement of retirement funds |  | 11.3 | (51.2) | 33.6 |  |
| Deferred tax relating to remeasurement of retirement funds |  | (1.4) | 6.7 | (4.0) |  |
| Items that may be reclassified subsequently to profit or loss: |  |  |  |  |  |
| Gain/(loss) on cash flow hedge |  | 11.6 | – | (10.7) |  |
| Reclassification of FCTR to profit or loss |  | – | – | (591.6) |  |
| Exchange rate differences from translation of foreign operations |  | (97.2) | 299.0 | 314.2 |  |
| Other comprehensive (loss)/income |  | (75.7) | 254.5 | (251.2) |  |
| Total comprehensive income/(loss) |  | 71.6 | (4 003.8) | (5 079.3) |  |
| Attributable to: |  |  |  |  |  |
| Equity holders of the Company |  | 71.6 | (4 003.8) | (5 079.3) |  |
| Total comprehensive income/(loss) attributable to owners: |  | 71.6 | (4 003.8) | (5 079.3) |  |
| From: |  |  |  |  |  |
| Continuing operations |  | 209.0 | 878.7 | 1 101.4 |  |
| Discontinued operations |  | (137.4) | (4 882.5) | (6 180.7) |  |
| **Earnings per share from continuing operations attributable to owners (cents):** | | | | | |
| Basic |  | 151.5 | 398.8 | 425.7 |  |
| Diluted |  | 151.0 | 398.3 | 425.4 |  |
| **Earnings per share from discontinued operations attributable to owners (cents):** | | | | | |
| Basic |  | (75.0) | (2 610.0) | (2 932.7) |  |
| Diluted |  | (74.8) | (2 606.7) | (2 931.0) |  |
| Earnings per share (cents): |  |  |  |  |  |
| Basic |  | 76.5 | (2 211.1) | (2 507.0) |  |
| Diluted |  | 76.3 | (2 208.3) | (2 505.5) |  |

1

--- Section unmapped | [AFS] physical page 5 | area selection | Table ---
THE SPAR GROUP LTD
INTERIM FINANCIAL
RESULTS 2026
Condensed consolidated
statement of financial position

|  | Unaudited as at 27 March | Restated*#(1) unaudited as at 28 March | Restated* unaudited as at 26 September |
| --- | --- | --- | --- |
| Rmillion | 2026 | 2025 | 2025 |
| ASSETS |  |  |  |
| Non-current assets | 19 428.4 | 19 711.9 | 19 548.0 |
| Property, plant and equipment | 4 957.2 | 5 069.2 | 5 071.7 |
| Right-of-use assets | 2 654.4 | 2 787.7 | 2 644.9 |
| Lease receivable | 4 077.7 | 4 223.4 | 4 194.7 |
| Goodwill and intangible assets | 6 500.2 | 6 651.6 | 6 424.1 |
| Investment in associates and joint ventures | 141.7 | 159.2 | 149.9 |
| Other investments | 19.8 | 18.2 | 19.8 |
| Loans and other receivables* | 170.9 | 224.4 | 190.7 |
| Block discounting loan receivable | – | 0.5 | – |
| Prepayments | 530.8 | 352.7 | 494.0 |
| Employee benefit assets | 181.7 | 96.5 | 180.4 |
| Deferred taxation asset | 194.0 | 128.5 | 177.8 |
| Current assets | 24 086.9 | 23 704.2 | 25 201.2 |
| Inventories | 4 617.2 | 4 739.3 | 4 653.1 |
| Trade and other receivables(1) | 15 975.2 | 15 216.3 | 16 107.3 |
| Prepayments | 484.9 | 336.0 | 445.7 |
| Loans and other receivables* | 373.5 | 550.3 | 278.8 |
| Block discounting loan receivable | 1.8 | 2.1 | 1.8 |
| Income tax receivable | 97.4 | 0.6 | 1.6 |
| Lease receivable | 939.7 | 945.8 | 960.3 |
| Cash and cash equivalents – SPAR[^#] | 1 069.5 | 1 520.9 | 2 327.3 |
| Cash and cash equivalents – Guilds and trusts | 527.7 | 392.9 | 425.3 |
| Assets held for sale | 1 332.9 | 11 827.6 | 1 472.2 |
| Total assets | 44 848.2 | 55 243.7 | 46 221.4 |
| EQUITY AND LIABILITIES |  |  |  |
| Capital and reserves | 5 401.3 | 6 529.1 | 5 312.3 |
| Stated capital | 2 231.5 | 2 231.5 | 2 231.5 |
| Treasury shares | (1.5) | (1.5) | (1.5) |
| Reserves | 673.9 | 1 473.0 | 742.7 |
| Retained earnings | 2 497.4 | 2 826.1 | 2 339.6 |
| Non-current liabilities | 13 843.3 | 14 292.8 | 14 111.9 |
| Deferred taxation liability | 229.4 | 209.9 | 235.1 |
| Employment benefit obligations | 279.9 | 273.7 | 277.4 |
| Financial liabilities | – | – | 9.3 |
| Borrowings | 6 403.6 | 6 740.9 | 6 514.5 |
| Block discounting loan payable | – | 0.5 | – |
| Lease liability | 6 930.4 | 7 067.8 | 7 075.6 |
| Current liabilities | 24 207.4 | 23 391.8 | 25 259.2 |
| Trade and other payables(1) | 20 561.9 | 20 315.9 | 22 336.8 |
| Financial liabilities | 30.0 | 21.9 | 34.0 |
| Borrowings | 573.9 | 337.8 | 532.8 |
| Block discounting loan payable | 1.8 | 2.2 | 1.8 |
| Lease liability | 1 489.8 | 1 413.2 | 1 462.0 |
| Provisions | 63.3 | 62.5 | 59.9 |
| Income tax payable | 56.0 | 159.4 | 151.7 |
| Bank overdrafts[^#] | 1 430.7 | 1 078.9 | 680.2 |
| Liabilities associated with assets held for sale | 1 396.2 | 11 030.0 | 1 538.0 |
| Total equity and liabilities | 44 848.2 | 55 243.7 | 46 221.4 |

*  During the current financial period, the Group identified a prior period error pertaining to March 2025 of R457.8 million (September 2025:
R215.6 million) in relation to current loans and receivables that was incorrectly classified as non-current.
[^#]  The prior period comparative information as at 28 March 2025 has been restated to correct an error in the classification of general banking facilities
of R494.0 million from cash and cash equivalents to bank overdrafts. Refer to note 4 for further detail.
(1)  The prior period comparative information as at 28 March 2025 has been restated to correct an error relating to inter-company receivable and
payable balances which was not correctly eliminated of R672.0 million.
In accordance with IAS 8 Accounting Policies, Changes in Accounting Estimates and Errors, the Group has retrospectively corrected these prior
period errors. The restatements had no impact on equity, on the statement of profit and loss and other comprehensive income and the statement
of cash flows.
2

--- Section unmapped | [AFS] physical page 6 | area selection | Table ---
THE SPAR GROUP LTD
INTERIM FINANCIAL
RESULTS 2026
Condensed consolidated
statement of changes in equity

| Rmillion | Stated capital | Currency Treasury translation shares reserve |  |  | Share- based payment reserve | Retained earnings | Hedging reserve | Total equity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Audited balance at |  |  |  |  |  |  |  |  |
| 30 September 2024 | 2 231.5 | (1.5) 976.2 |  |  | 38.2 | 7 129.3 | – | 10 373.7 |
| Loss for the period | – | – – |  |  | – | (4 258.3) | – | (4 258.3) |
| Other comprehensive income: |  |  |  |  |  |  |  |  |
| –  Remeasurement of retirement funds | – | – – |  |  | – | (44.5) | – | (44.5) |
| –  Reclassification of currency translation reserve | – | – 161.3 |  |  | – | – | – | 161.3 |
| –  Exchange rate translation | – | – 299.0 |  |  | – | – | – | 299.0 |
| Recognition of share-based payments | – | – – |  |  | 5.0 | (0.3) | – | 4.7 |
| Settlement of share-based payments | – | 6.8 – |  |  | (6.7) | (0.1) | – | – |
| Treasury shares acquired | – | (6.8) – |  |  | – | – | – | (6.8) |
| Unaudited balance at |  |  |  |  |  |  |  |  |
| 28 March 2025 | 2 231.5 | (1.5) 1 436.5 |  |  | 36.5 | 2 826.1 | – | 6 529.1 |
| Loss for the period | – | – – |  |  | – | (569.8) | – | (569.8) |
| Other comprehensive income: |  |  |  |  |  |  |  |  |
| –  Remeasurement of employee benefits | – | – – |  |  | – | 7.3 | – | 7.3 |
| –  Remeasurement of retirement funds | – | – – |  |  | – | 74.1 | – | 74.1 |
| –  Exchange rate translation | – | – 15.2 |  |  | – | – | – | 15.2 |
| –  Reclassification of currency translation reserve | – | – (752.9) |  |  | – | – | – | (752.9) |
| –  Movement in cash flow hedge | – | – – |  |  | – | – | (10.7) | (10.7) |
| Recognition of share-based payments | – | – – |  |  | 21.3 | 0.3 | – | 21.6 |
| Settlement of share-based payments | – | 1.6 – |  |  | (3.2) | 1.6 | – | – |
| Treasury shares acquired | – | (1.6) – |  |  | – | – | – | (1.6) |
| Audited balance at |  |  |  |  |  |  |  |  |
| 26 September 2025 | 2 231.5 | (1.5) 698.8 |  |  | 54.6 | 2 339.6 | (10.7) | 5 312.3 |
| Profit for the period | – | – – |  |  | – | 147.3 | – | 147.3 |
| Other comprehensive income: |  |  |  |  |  |  |  |  |
| –  Remeasurement of retirement funds | – | – – |  |  | – | 9.9 | – | 9.9 |
| –  Exchange rate translation | – | – (97.2) |  |  | – | – | – | (97.2) |
| –  Movement in cash flow hedge | – | – – |  |  | – | – | 11.6 | 11.6 |
| Recognition of share-based payments | – | – – |  |  | 21.0 | 0.3 | – | 21.3 |
| Settlement of share-based payments | – | 3.9 – |  |  | (4.2) | 0.3 | – | – |
| Treasury shares acquired | – | (3.9) – |  |  | – | – | – | (3.9) |
| Unaudited balance at 27 March 2026 | 2 231.5 | (1.5) 601.6 |  |  | 71.4 | 2 497.4 | 0.9 | 5 401.3 |

3

--- Section unmapped | [AFS] physical page 7 | area selection | Table ---
THE SPAR GROUP LTD
INTERIM FINANCIAL
RESULTS 2026
Condensed consolidated
statement of cash flows

|  |  | Unaudited for the 26 weeks | Restated* unaudited for the 26 weeks | Audited |
| --- | --- | --- | --- | --- |
|  |  | ended | ended | Year ended |
|  |  | 27 March | 28 March | 26 September |
| Rmillion | Notes | 2026 | 2025 | 2025 |
| CASH FLOWS (USED IN)/FROM OPERATING ACTIVITIES |  | (974.0) | 1 346.9 | 4 285.9 |
| Cash (utilised)/generated from operations | 5 | (297.3) | 1 866.1 | 5 445.9 |
| Finance income received |  | 305.1 | 345.1 | 636.9 |
| Finance costs paid |  | (702.5) | (751.1) | (1 392.7) |
| Taxation paid |  | (279.3) | (113.2) | (404.2) |
| CASH FLOWS USED IN INVESTING ACTIVITIES |  | (135.0) | (651.2) | (901.5) |
| Acquisition of businesses/subsidiaries | 6.2 | (211.7) | (125.5) | (494.2) |
| Proceeds from disposal of businesses | 6.6 | 32.7 | – | 31.6 |
| Proceeds on disposal of assets held for sale |  | – | – | 225.0 |
| Cash outflow from disposal of businesses |  | – | (525.0) | (966.4) |
| Investment to expand PPE and intangible assets |  | (197.8) | (284.0) | (515.6) |
| Investment to maintain operations |  | (170.8) | (130.2) | (340.2) |
| – Replacement of PPE and intangible assets |  | (196.2) | (176.9) | (392.8) |
| – Proceeds on disposal of PPE |  | 25.4 | 46.7 | 52.6 |
| Principal element of lease receipts |  | 480.2 | 485.0 | 952.5 |
| Cash inflows from loans and investments |  | 121.9 | 60.3 | 305.4 |
| Cash outflows from loans and investments |  | (189.5) | (131.8) | (99.6) |
| CASH FLOWS (USED IN)/FROM FINANCING ACTIVITIES* |  | (1 027.7) | 54.8 | (1 285.4) |
| Principal element of lease payments |  | (778.0) | (1 034.3) | (2 147.6) |
| Proceeds from borrowings |  | 1 236.8 | 7 427.5 | 5 670.1 |
| Principal element of repayments of borrowings |  | (1 230.6) | (4 132.6) | (2 776.5) |
| Treasury shares acquired |  | (3.9) | (6.8) | (8.4) |
| Net movement on banking facilities*(1) |  | (252.0) | (2 199.0) | (2 023.0) |
| Net (decrease)/increase during the period* |  | (2 136.7) | 750.5 | 2 099.0 |
| Cash and cash equivalents at the beginning of the period* |  | 2 742.4 | 618.3 | 618.3 |
| Exchange rate translation |  | (21.2) | 7.1 | 25.1 |
| Cash and cash equivalents at the end of the period* | 4 | 584.5 | 1 375.9 | 2 742.4 |

The cash flows above are derived from both continuing and discontinued operations. Refer to note 9 for cash flows relating to the discontinued
operations.
* The prior period comparative information for the period ended 28 March 2025 has been restated to correct an error in classification of the
movement in general banking facilities of R494.0 million from Cash and cash equivalents to net movement on banking facilities as part of Cash
flows (used in)/from financing activities to correctly reflect the treatment under IAS 7 Statement of Cash Flows. Refer to note 4.
(1) General banking facilities are contracted for a 364-day period, however individual drawdowns are utilised on an overnight call basis, thereby
allowing the Group to access these facilities on a short-term basis to manage daily liquidity requirements.
4

--- Section unmapped | [AFS] physical page 8 | area selection | Table ---
THE SPAR GROUP LTD
INTERIM FINANCIAL
RESULTS 2026
Notes to the condensed
consolidated financial results
1. Statement of compliance and basis of preparation
The condensed consolidated interim financial statements are prepared in accordance with the requirements of the JSE Listings
Requirements for interim reports, and the requirements of the Companies Act, No. 71 of 2008 (as amended) (Companies Act)
applicable to interim financial statements. The Listings Requirements require interim reports to be prepared in accordance with and
contain the information required by International Accounting Standards (IAS) 34 Interim Financial Reporting, as well as the South
African Institute of Chartered Accountants (SAICA) Financial Reporting Guides as issued by the Accounting Practices Committee
and Financial Pronouncements as issued by the Financial Reporting Standards Council.
The accounting policies applied in the preparation of the condensed consolidated interim financial statements are in terms of
IFRS® Accounting Standards and are consistent with those applied in the previous annual financial statements. The condensed
consolidated interim financial statements have been prepared on the going concern and historical cost basis, except where
otherwise indicated.
The presentation currency is the South African Rand, except where otherwise indicated.
The condensed consolidated interim financial statements have been prepared under the supervision of the Chief Financial Officer,
Megan Pydigadu, CA(SA), on behalf of The SPAR Group Ltd. The information contained in this report has neither been audited nor
reviewed by the Group’s external auditors.
2. Headline earnings and reconciliation

|  |  |  | Unaudited for the 26 weeks ended | Unaudited for the 26 weeks ended | Audited Year ended |  |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  | 27 March | 28 March 26 September |  |  |
| Rmillion |  | Note | 2026 | 2025 | 2025 |  |
| 2.1 Headline earnings |  |  |  |  |  |  |
| Headline earnings per share | (cents) |  | 123.6 | 296.2 | 507.5 |  |
| Headline earnings per share from continuing operations | (cents) |  | 199.9 | 433.8 | 768.9 |  |
| Diluted headline earnings per share | (cents) |  | 123.2 | 295.8 | 507.2 |  |
| Diluted headline earnings per share from continuing operations | (cents) |  | 199.3 | 433.2 | 768.4 |  |
| 2.2 Headline earnings reconciliation |  |  |  |  |  |  |
| Profit/(loss) for the period attributable to equity holders of the Company |  |  | 147.3 | (4 258.3) | (4 828.1) |  |
| Adjusted for: |  |  |  |  |  |  |
| (Profit)/loss on sale of PPE and intangible assets |  |  | (29.5) | 8.0 | 22.3 |  |
| Gain on bargain purchase |  |  | (0.7) | – | – |  |
| Impairment of goodwill |  | 7 | 47.4 | 5.2 | 353.5 |  |
| Impairment of assets held for sale |  | 7 | 13.1 | 4 295.3 | 4 684.3 |  |
| Impairment of PPE and intangible assets |  | 7 | 41.2 | – | 13.9 |  |
| (Profit)/loss on disposal of businesses |  |  | (0.9) | 520.2 | 562.0 |  |
| Impairment to right-of-use asset |  | 7 | 26.9 | – | 232.0 |  |
| Tax effects of adjustments |  |  | (6.8) | – | (62.6) |  |
| Headline earnings |  |  | 238.0 | 570.4 | 977.3 |  |
| Headline earnings from discontinued operations |  |  | (147.0) | (265.0) | (503.4) |  |
| Headline earnings from continuing operations |  |  | 385.0 | 835.4 | 1 480.7 |  |

5

--- Section unmapped | [AFS] physical page 9 | area selection | Table ---
THE SPAR GROUP LTD
INTERIM FINANCIAL
RESULTS 2026
3.  Segmental reporting
Segment accounting policies are consistent with those adopted for the preparation of the condensed consolidated interim financial
results.
The principal segments of the Group have been identified on a primary basis by geographical segment, which is representative
of the internal reporting used for management purposes as well as the source and nature of business risks and returns. These
geographical segments also represent operating segments as they meet the quantitative thresholds.
The Chief Executive Officer is the Chief Operating Decision Maker (CODM) and assesses the performance of the operating segments
based on profit before tax and for joint ventures and associates based on earnings after tax, and is of the opinion that the operations
of the individual distribution centres within Southern Africa are substantially similar to one another and that the risks and returns of
these distribution centres are likewise similar. The risks and returns of the Ireland operations are not considered to be similar to those
within Southern Africa or each other and are therefore disclosed as separate reportable segments.
As a result, the geographical segments of the Group have been identified as Southern Africa and Ireland. All segment revenue and
expenses are directly attributable to the segments. Segment assets and liabilities include all operating assets and liabilities used by a
segment and IFRS adjustments made by segments to their management report for the purposes of IFRS compliance. These assets
and liabilities are all directly attributable to the segments.
The principal activity of the operating segments is the wholesale and distribution of goods and services to SPAR grocery stores and
multiple other branded Group retail outlets.
The Group deals with a broad spread of customers, with no single customer exceeding 10% of the Group’s revenue.
Analysis per reportable segment:

| Rmillion Unaudited 26 weeks ended 27 March 2026 Statement of profit or loss – Continuing operations | Southern Africa | Ireland  Switzerland |  |  |  |  | Poland | Consolidated Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Revenue from contracts with customers* | 51 616.4 | 16 975.7 |  |  | – |  | – | 68 592.1 |
| Cost of sales | 45 962.6 | 14 408.2 |  |  | – |  | – | 60 370.8 |
| Impairment of PPE and intangible assets | 31.0 | 10.2 |  |  | – |  | – | 41.2 |
| Impairment of assets held for sale | 13.1 | – |  |  | – |  | – | 13.1 |
| Impairment to right-of-use asset | 25.1 | 1.8 |  |  | – |  | – | 26.9 |
| Impairment of goodwill | 47.4 | – |  |  | – |  | – | 47.4 |
| Depreciation and amortisation | 261.2 | 288.1 |  |  | – |  | – | 549.3 |
| Total employment costs | 2 006.5 | 1 034.2 |  |  | – |  | – | 3 040.7 |
| Delivery costs | 460.3 | 209.8 |  |  | – |  | – | 670.1 |
| Advertising | 887.8 | 140.9 |  |  | – |  | – | 1 028.7 |
| Operating profit | 237.7 | 502.8 |  |  | – |  | – | 740.5 |
| Finance income | 296.0 | 8.6 |  |  | – |  | – | 304.6 |
| Finance costs | 585.4 | 82.1 |  |  | – |  | – | 667.5 |
| Share of equity-accounted associate profits/(losses) | 1.4 | (6.2) |  |  | – |  | – | (4.8) |
| (Loss)/profit before tax | (50.9) | 413.9 |  |  | – |  | – | 363.0 |
| Taxation | 2.4 | 68.9 |  |  | – |  | – | 71.3 |
| Statement of financial position – Total Group |  |  |  |  |  |  |  |  |
| Total assets | 28 097.2  16 751.0 |  |  |  | – |  | – | 44 848.2 |
| Total liabilities | 26 690.1  12 756.8 |  |  |  | – |  | – | 39 446.9 |

* Consists of revenue – sale of merchandise and revenue – other.
6

--- Section unmapped | [AFS] physical page 10 | area selection | Table ---
THE SPAR GROUP LTD
INTERIM FINANCIAL
RESULTS 2026
3.  Segmental reporting continued

| Rmillion Unaudited 26 weeks ended 28 March 2025 Statement of profit or loss – Continuing operations | Southern Africa | Ireland  Switzerland |  |  |  |  |  |  |  |  |  |  | Poland | Consolidated Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Revenue from contracts with customers | 49 697.9  16 192.5 |  |  |  |  |  |  |  |  |  | – |  | – | 65 890.4 |
| Cost of sales | 44 378.6  13 783.6 |  |  |  |  |  |  |  |  |  | – |  | – | 58 162.2 |
| Depreciation and amortisation | 258.7 | 293.0 |  |  |  |  |  |  |  |  | – |  | – | 551.7 |
| Total employment costs | 1 825.0 | 977.4 |  |  |  |  |  |  |  |  | – |  | – | 2 802.4 |
| Impairment of goodwill | 2.0 | – |  |  |  |  |  |  |  |  | – |  | – | 2.0 |
| Delivery costs | 385.5 | 202.2 |  |  |  |  |  |  |  |  | – |  | – | 587.7 |
| Advertising | 606.8 | 127.9 |  |  |  |  |  |  |  |  | – |  | – | 734.7 |
| Operating profit | 867.7 | 486.0 |  |  |  |  |  |  |  |  | – |  | – | 1 353.7 |
| Profit before tax | 602.9 | 391.3 |  |  |  |  |  |  |  |  | – |  | – | 994.2 |
| Finance income | 299.6 | 7.7 |  |  |  |  |  |  |  |  | – |  | – | 307.3 |
| Finance costs | 568.8 | 100.2 |  |  |  |  |  |  |  |  | – |  | – | 669.0 |
| Share of equity-accounted associate profits | 4.4 | – |  |  |  |  |  |  |  |  | – |  | – | 4.4 |
| Taxation | 167.3 | 58.8 |  |  |  |  |  |  |  |  | – |  | – | 226.1 |
| Statement of financial position – Total Group |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Total assets | 28 681.8  17 268.6 |  |  |  |  |  |  |  |  |  | 9 471.3 |  | – | 55 421.7 |
| Total liabilities | 26 230.2  13 208.2 |  |  |  |  |  |  |  |  |  | 9 454.2 |  | – | 48 892.6 |
| Audited year ended 26 September 2025 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Statement of profit or loss – Continuing operations |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Revenue from contracts with customers | 98 352.4  35 055.9 |  |  |  |  |  |  |  |  |  | – |  | – | 133 408.3 |
| Cost of sales | 87 527.2  29 785.7 |  |  |  |  |  |  |  |  |  | – |  | – | 117 312.9 |
| Impairment of PPE and intangible assets | 13.9 | – |  |  |  |  |  |  |  |  | – |  | – | 13.9 |
| Impairment of assets held for sale | 79.4 | – |  |  |  |  |  |  |  |  | – |  | – | 79.4 |
| Impairment to right-of-use asset | 232.0 | – |  |  |  |  |  |  |  |  | – |  | – | 232.0 |
| Impairment of goodwill | 350.3 | – |  |  |  |  |  |  |  |  | – |  | – | 350.3 |
| Depreciation and amortisation | 533.3 | 601.3 |  |  |  |  |  |  |  |  | – |  | – | 1 134.6 |
| Total employment costs | 3 641.6 | 2 058.3 |  |  |  |  |  |  |  |  | – |  | – | 5 699.9 |
| Delivery costs | 871.7 | 426.8 |  |  |  |  |  |  |  |  | – |  | – | 1 298.5 |
| Advertising | 1 278.0 | 266.6 |  |  |  |  |  |  |  |  | – |  | – | 1 544.6 |
| Operating profit | 844.4 | 1 139.1 |  |  |  |  |  |  |  |  | – |  | – | 1 983.5 |
| Finance income | 599.1 | 14.7 |  |  |  |  |  |  |  |  | – |  | – | 613.8 |
| Finance costs | 1 111.8 | 193.0 |  |  |  |  |  |  |  |  | – |  | – | 1 304.8 |
| Share of equity-accounted associate profits | 4.2 | – |  |  |  |  |  |  |  |  | – |  | – | 4.2 |
| Profit before tax | 335.8 | 952.0 |  |  |  |  |  |  |  |  | – |  | – | 1 287.8 |
| Taxation | 342.1 | 125.9 |  |  |  |  |  |  |  |  | – |  | – | 468.0 |
| Statement of financial position – Total Group |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Total assets | 28 753.9  17 467.5 |  |  |  |  |  |  |  |  |  | – |  | – | 46 221.4 |
| Total liabilities | 27 449.1  13 460.0 |  |  |  |  |  |  |  |  |  | – |  | – | 40 909.1 |

7

--- Section unmapped | [AFS] physical page 11 | area selection | Table ---
THE SPAR GROUP LTD
INTERIM FINANCIAL
RESULTS 2026
3.  Segmental reporting continued

|  |  | Unaudited | for the 26 weeks | Unaudited for the 26 weeks ended |  |  | Audited |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  | ended | 28 March |  | Year ended |  |
|  |  | 27 March |  | 2025 |  | 26 September |  |
| Rmillion |  |  | 2026 Re-presented[^#] |  |  |  | 2025 |
| Disaggregated revenue as reviewed by the CODM |  |  |  |  |  |  |  |
| Southern Africa |  |  |  |  |  |  |  |
| Revenue – sale of merchandise |  |  | 50 783.4 | 49 229.9 |  |  | 96 948.2 |
| SPAR[^#] |  |  | 37 727.9 | 36 876.9 |  |  | 72 635.4 |
| Liquor |  |  | 6 406.1 | 6 122.4 |  |  | 11 552.4 |
| Build It |  |  | 5 150.3 | 5 074.8 |  |  | 10 304.2 |
| SPAR Health |  |  | 1 203.1 | 943.8 |  |  | 1 992.1 |
| Encore[^#] |  |  | 264.7 | 212.0 |  |  | 464.1 |
| Pet Storey |  |  | 31.3 | – |  |  | – |
| Revenue – other |  |  | 833.0 | 468.0 |  |  | 1 404.2 |
| Revenue from contracts with customers |  |  | 51 616.4 | 49 697.9 |  |  | 98 352.4 |
| Ireland |  |  |  |  |  |  |  |
| Revenue – sale of merchandise |  |  | 16 699.1 | 15 930.3 |  |  | 34 509.5 |
| BWG |  |  | 16 699.1 | 15 930.3 |  |  | 34 509.5 |
| Revenue – other |  |  | 276.6 | 262.2 |  |  | 546.4 |
| Revenue from contracts with customers |  |  | 16 975.7 | 16 192.5 |  |  | 35 055.9 |
| Total revenue – sale of merchandise |  |  | 67 482.5 | 65 160.2 |  | 131 457.7 |  |
| Total revenue – other |  |  | 1 109.6 | 730.2 |  |  | 1 950.6 |
| Total revenue from contracts with customers |  |  | 68 592.1 | 65 890.4 |  | 133 408.3 |  |
| Disaggregated total revenue – other: |  |  | 1 109.6 | 730.2 |  |  | 1 950.6 |
| Marketing and service revenues |  |  | 839.5 | 471.0 |  |  | 1 542.3 |
| Franchise fees |  |  | 127.1 | 116.1 |  |  | 253.5 |
| Other services |  |  | 143.0 | 143.1 |  |  | 154.8 |
| **[^#] Comparative information has been re-presented to separately disclose Encore revenue from SPAR. In the prior period, Encore revenue was** | | | | | | | |
| **included within SPAR and was not presented as a separate line item. This re-presentation has been made to enhance the transparency and** | | | | | | | |
| **comparability of segmental revenue disclosures and has no impact on previously reported total Group revenue or profit.** | | | | | | | |
| Change in reporting weeks |  |  |  |  |  |  |  |
| **In the prior reporting period, the CODM changed the Group’s financial year end to align with the retail industry’s general practice** | | | | | | | |
| **of dividing the financial reporting calendar into 52 weeks of seven days, with each reporting week ending on a Friday, allowing for** | | | | | | | |
| **better comparability between the reporting periods. This change was adopted prospectively.** | | | | | | | |
| **The results for the 26 weeks ended 27 March 2026 have been prepared on this basis. The prior period results ended 28 March 2025** | | | | | | | |
| **were also prepared on this basis. Below are the comparable results for the 26 weeks ended 27 March 2026 and the 26 weeks ended** | | | | | | | |
| 28 March 2025. |  |  |  |  |  |  |  |
|  | Unaudited 26 weeks ended 27 March 2026 |  |  |  |  |  |  |
|  |  |  |  | Per reportable segment |  |  |  |
|  | Consolidated total |  |  | as adjusted |  |  |  |
| Rmillion | As reported | As adjusted |  | Southern Africa |  |  | Ireland |
| Continuing operations* |  |  |  |  |  |  |  |
| Statement of profit or loss |  |  |  |  |  |  |  |
| Revenue from contracts with customers | 68 592.1 | 68 592.1 |  | 51 616.4 |  |  | 16 975.7 |
| Operating profit | 740.5 |  | 740.5 | 237.7 |  |  | 502.8 |
| Profit/(loss) before tax | 363.0 |  | 363.0 | (50.9) |  |  | 413.9 |
| Net finance costs | 362.9 |  | 362.9 | 289.4 |  |  | 73.5 |
| Taxation | 71.3 |  | 71.3 | 2.4 |  |  | 68.9 |

* Excludes results relating to the discontinued operations – refer to note 9 for further detail.
8

--- Section unmapped | [AFS] physical page 12 | area selection | Financial note ---
                                                          
        THE SPAR GROUP LTD                                
        INTERIM FINANCIAL                                 
        RESULTS 2026                                      
    3. Segmental reporting continued                      
                                                          
       Change in reporting weeks continued                
       Below are the results for the 26 weeks ended 28 March 2025, adjusted for the additional trading days in the 2025 financial period
       reported financial results in order to allow comparability to the adjusted 26 weeks ended 27 March 2026 above.
                                Unaudited 26 weeks ended 28 March 2025
                                           Per reportable segment
                              Consolidated total as adjusted
       Rmillion             As reported As adjusted Southern Africa Ireland
       Continuing operations*                             
       Statement of profit or loss                        
       Revenue from contracts with customers 65 890.4 66 822.4 50 441.6 16 410.8
       Operating profit       1 353.7 1 403.4 909.0 494.4 
       Profit before tax       994.2 1 039.3 641.2 398.1  
       Net finance costs       361.7 366.3  272.2   94.1  
       Taxation                226.1 212.1  154.4   57.7  
       * Excludes results relating to the discontinued operations – refer to note 9 for further detail.
    4. Cash and cash equivalents/overdrafts               
       For the purpose of the statement of cash flow, cash and cash equivalents include cash on hand and in banks. The Group separately
       discloses the bank balances of SPAR, Guild and trust bank balances. Guild balances comprise retailer funds and other cash
       deposits attributable to The SPAR Guild of Southern Africa and the Build it Guild of Southern Africa. Deposits received by the SPAR
       Guild of Southern Africa from the SPAR retail members are included in other payables. Trust balances comprise cash on hand at
       interim held by the BBBEE trusts pending payment to beneficiaries. The liability to the beneficiaries is included in trade and other
       payables.                                          
       Cash and cash equivalents at the end of the financial period as shown in the statement of cash flows can be reconciled to the related
       items in the statement of financial position as follows:
                                           Restated*      
                                    Unaudited unaudited Audited
                                      as at  as at as at  
                                    27 March 28 March 26 September
       Rmillion                       2026   2025  2025   
       Bank balances – Guilds and Share trusts 527.7 392.9 425.3
       Bank balances – SPAR          1 069.5 1 520.9 2 327.3
       Bank overdrafts – SPAR other* (1 012.7) (584.9) (10.2)
       Net cash and cash equivalents  584.5 1 328.9 2 742.4
       Bank overdrafts – SPAR general banking facilities* (418.0) (494.0) (670.0)
       Net cash and banking facilities 166.5 834.9 2 072.4
       In the prior period, as at 28 March 2025, cash and cash equivalents of R47.0 million relating to the Switzerland disposal group
       were classified as assets held for sale and accordingly presented within assets held for sale on the statement of financial position.
       * The Group’s general banking facilities, which include call accounts and associated overdraft balances, included banking facilities that
        have been separately disclosed in the current period to correct an error in classification between Cash and cash equivalents and Cash
        flows (used in)/from financing activities and to provide improved transparency over the composition of cash and cash equivalents. As a
        result, movements in these facilities are now presented separately. Comparative figures for the period ended 28 March 2025 have been
        restated accordingly to ensure consistency with the current period’s presentation.
        The adjustment to the comparative figures for the period ended 28 March 2025 was a R494.0 million increase in the closing balance of
        cash and cash equivalents on the statement of cash flows (previously R881.9 million).
                             9                            

--- Section unmapped | [AFS] physical page 13 | area selection | Table ---
THE SPAR GROUP LTD
INTERIM FINANCIAL
RESULTS 2026
5. Cash generated from operations

| Rmillion | 26 weeks ended 27 March 2026 | 26 weeks ended 28 March 2025 |
| --- | --- | --- |
| Operating profit from continuing operations | 740.5 | 1 353.7 |
| Operating loss from discontinued operations | (115.7) | (4 916.8) |
| Operating profit/(loss) including discontinued operations | 624.8 | (3 563.1) |
| Adjusted for the following items recognised in profit or loss: |  |  |
| Depreciation and amortisation | 549.3 | 1 087.1 |
| (Profit)/loss on sale of PPE and intangible assets | (29.5) | 8.0 |
| Movement in employee benefit provisions – retirement fund | 16.7 | (21.7) |
| Share-based payment expenses | 21.0 | 5.0 |
| Movement in provisions raised against trade receivables and loans | 150.7 | 45.5 |
| Loss on lease modification | (1.1) | – |
| (Profit)/loss on disposal of businesses | (0.9) | 520.2 |
| Impairment of goodwill | 47.4 | 5.2 |
| Impairment of PPE and Intangible assets | 41.2 | – |
| Impairment to right-of-use asset | 26.9 | – |
| Impairment of assets held for sale | 13.1 | 4 295.3 |
| Other | (5.7) | (0.9) |
| Net accruals | 41.9 | (17.3) |
| Amortisation of prepayments | 27.6 | 14.5 |
| Gain on bargain purchase | (0.7) | – |
| Stock provision relating to the closure of Imports Warehouse | 22.4 | – |
| Provision for obsolete stock | (2.9) | (0.4) |
| Foreign exchange adjustments | 0.2 | (3.3) |
| Cash generated from operations before working capital changes | 1 542.4 | 2 374.1 |
| Net working capital changes | (1 839.7) | (508.0) |
| Decrease/(increase) in inventories | 63.0 | (367.4) |
| Increase in trade and other receivables | (61.0) | (463.4) |
| (Decrease)/increase in trade payables and provisions | (1 841.7) | 322.8 |
| Cash generated from operations | (297.3) | 1 866.1 |

6.  Business combinations
6.1 Acquisitions
Retail stores acquired
During the financial period, SPAR acquired the assets of eight retail stores in South Africa (March 2025: four). The BWG Group did
not acquire retail stores in the current period (March 2025: three in Ireland). The principal activity of these acquisitions is that of retail
trade and all its aspects. These acquisitions were funded from available cash resources.
Perrys Cash & Carry Limited
On 9 October 2025, the BWG Group acquired Perrys Cash & Carry Limited for R118.1 million. Perrys is an established family-run
wholesaler supplying the grocery retail, licensed trade and foodservice sectors in Ireland.
Dublin Food Sales
On 17 November 2025, BWG Foods acquired Dublin Foods Sales Limited, a wholesale business based in Dublin, Ireland.
The purchase price was based on retained sales in reference period, with a fixed amount of R5.9 million initial upfront payment.
10

--- Section unmapped | [AFS] physical page 14 | area selection | Table ---
THE SPAR GROUP LTD
INTERIM FINANCIAL
RESULTS 2026
6.  Business combinations continued
6.2 Assets acquired and liabilities assumed at date of acquisition
Unaudited for the 26 weeks ended 27 March 2026

| Rmillion | SA retail Perrys Cash stores & Carry Ltd |  |  | Dublin Food Sales | Aptekor Group | Pet Masters Group | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Assets | 12.2 121.8 |  |  | – | 76.7 | 13.7 | 224.4 |
| Property, plant and equipment | 12.2 30.1 |  |  | – | 4.3 | 2.0 | 48.6 |
| Trade and other receivables | – 29.5 |  |  | – | 43.6 | 1.3 | 74.4 |
| Cash and cash equivalents | – 41.2 |  |  | – | 2.8 | – | 44.0 |
| Inventories | – 21.0 |  |  | – | 26.0 | 10.4 | 57.4 |
| Liabilities | – (34.4) |  |  | – | (62.3) | (8.7) | (105.4) |
| Trade and other payables | – (34.4) |  |  | – | (49.3) | (8.7) | (92.4) |
| Bank overdrafts | – – |  |  | – | (13.0) | – | (13.0) |
| Total identifiable net assets at fair value | 12.2 87.4 |  |  | – | 14.4 | 5.0 | 119.0 |
| Goodwill/(gain on bargain purchase) arising from acquisition | 149.8 30.7 |  |  | 5.9 | (0.7) | 14.7 | 200.4 |
| Purchase consideration | 162.0 118.1 |  |  | 5.9 | 13.7 | 19.7 | 319.4 |
| (Cash balances)/overdrafts acquired | – (41.2) |  |  | – | 10.2 | – | (31.0) |
| Business acquisition costs | – 3.1 |  |  | 0.8 | 0.6 | – | 4.5 |
| Contingent consideration |  |  |  |  |  |  |  |
| (refer to note 6.4) | – (79.5) |  |  | – | – | – | (79.5) |
| Deferred consideration | – – |  |  | – | – | (1.7) | (1.7) |
| Net cash outflow on acquisition | 162.0 0.5 |  |  | 6.7 | 24.5 | 18.0 | 211.7 |
| **6.3 Contribution to results for the period** | | | | | | | |
|  |  |  |  |  | Southern |  |  |
| Rmillion |  |  |  |  | Africa | Ireland | Total |
| Revenue |  |  |  |  | 249.4 | 97.4 | 346.8 |
| Operating (loss)/profit |  |  |  |  | (51.9) | 4.8 | (47.1) |
| **Had all acquisitions been consolidated from the beginning of the financial period, the contribution to the result would have been** | | | | | | | |
| as follows: |  |  |  |  |  |  |  |
|  |  |  |  |  | Southern |  |  |
| Rmillion |  |  |  |  | Africa | Ireland | Total |
| Revenue |  |  |  |  | 447.6 | 107.8 | 555.4 |
| Operating (loss)/profit |  |  |  |  | (142.5) | 5.4 | (137.1) |

11

--- Section unmapped | [AFS] physical page 15 | area selection | Table ---
THE SPAR GROUP LTD
INTERIM FINANCIAL
RESULTS 2026
6.  Business combinations continued
6.4 Contingent consideration
Perrys Cash & Carry Limited’s contingent consideration of R79.5 million will be payable in February 2027 and is based on the 12-month
retained sales performance commencing 1 February 2026.
6.5 Business acquisition costs

| Rmillion |  |  | Unaudited for the 26 weeks ended 27 March 2026 |
| --- | --- | --- | --- |
| Business acquisition costs (refer to note 6.2) |  |  | (4.5) |
| Acquisition costs related to acquisitions not yet finalised |  |  | (5.3) |
| Total business acquisition costs |  |  | (9.8) |
| 6.6 Assets and liabilities at date of disposal |  |  |  |
| **Five retail stores were sold in Southern Africa during the 26 weeks ended 27 March 2026 (March 2025: Five). Proceeds of** | | | |
| **R7.8 million relating to the prior year disposal of the BWG Group’s interest in the ATM business have been received and recognised.** | | | |
|  | Unaudited for the 26 weeks ended 27 March 2026 |  |  |
|  | SA retail | BWG Group – |  |
| Rmillion | stores | ATM division | Total |
| Non-current assets | 27.8 | – | 27.8 |
| Property, plant and equipment | 13.4 | – | 13.4 |
| Assets held for sale | 14.4 | – | 14.4 |
| Current assets | 4.0 | – | 4.0 |
| Inventories | 1.0 | – | 1.0 |
| Trade and other receivables | 3.0 | – | 3.0 |
| (Loss)/profit on disposal of business | (6.9) | 7.8 | 0.9 |
| Proceeds received | 24.9 | 7.8 | 32.7 |
| Net cash inflow on disposal | 24.9 | 7.8 | 32.7 |

12

--- Section unmapped | [AFS] physical page 16 | area selection | Financial note ---
                                                          
        THE SPAR GROUP LTD                                
        INTERIM FINANCIAL                                 
        RESULTS 2026                                      
    7. Impairments                                        
       The Group assesses, at each reporting date, whether there is any indication that assets or cash-generating units (CGUs) may be
       impaired. Where such indicators exist, the recoverable amount is estimated and an impairment loss is recognised where the carrying
       amount exceeds the recoverable amount. Details of the significant impairments recognised during the period are set out below.
                                    Unaudited Unaudited   
                                     for the for the      
                                    26 weeks 26 weeks Audited
                                     ended  ended Year ended
                                    27 March 28 March 26 September
       Rmillion                       2026   2025  2025   
       Impairments – Total Group      128.6 4 300.5 5 283.7
       Impairment of assets held for sale(1) 13.1 4 295.3 4 684.3
       Impairment of goodwill(2)      47.4   5.2   353.5  
       Impairment of PPE and intangible assets(3) 41.2 – 13.9
       Impairment to right-of-use asset(4) 26.9 –  232.0  
       (1) Beyers Ridge land, classified as an asset held for sale, was previously impaired in FY2025 based on an estimated recoverable value
        of approximately R80 million. During the current period, a contractual selling price of R65 million was negotiated, resulting in a further
        impairment loss being recognised at 27 March 2026 to reduce the carrying amount to the agreed fair value less costs to sell.
       (2) On 1 February 2026, Southern Africa acquired eight stores from the Hajimarkos group. In terms of the acquisition agreement, the purchase
        consideration amounted to R162.0 million, which exceeded current market-related valuations, resulting in goodwill of R149.8 million
        being recognised on acquisition. Following an impairment assessment performed at 27 March 2026, two stores, namely The Square and
        2nd Avenue, were identified as experiencing operational performance challenges. Consequently, an impairment loss was recognised
        against goodwill during the period.               
       (3) Southern Africa recognised an impairment of R30.7 million relating to the GiCom software module, which remains under development at
        27 March 2026. Based on an assessment performed by the Technology team together with the National Merchandising Executive, it was
        determined that the software would not be deployed due to limited expected utilisation. Accordingly, the software development costs were
        fully impaired. In Ireland, an independent valuation performed by a professional valuer identified that the recoverable amount of a property
        was below its carrying value, resulting in an impairment loss of R10.2 million being recognised during the period.
       (4) In Southern Africa, corporate-owned stores continue to be assessed as separate cash-generating units, consistent with the approach
        adopted in FY2025. Certain stores transitioned from profit-making to loss-making positions during the current period, representing an
        indicator of impairment. Based on the impairment assessment performed, right-of-use assets relating to three stores were impaired by
        R22.7 million at 27 March 2026. In Ireland, a tenant occupying one of the Group’s properties experienced financial difficulties, resulting
        in the property becoming vacant. Management was subsequently unable to secure a suitable replacement tenant and, following an
        impairment assessment, an impairment loss of R1.8 million was recognised at 27 March 2026.
    8. Financial guarantees                               
       Financial guarantees may be provided by the Group to subsidiaries and affiliates. Financial guarantee contracts issued by the
       Company are initially measured at their fair values and are subsequently measured at the higher of the expected credit loss in
       accordance with IFRS 9 or the amount initially recognised less, where appropriate, cumulative amortisation recognised in
       accordance with IFRS 15. Management has formally assessed these IFRS 9 fair values of the guarantees below to be immaterial
       and also confirms that no legal obligation exists at the reporting date to settle these guarantees issued.
       Management’s day one assessment is based on the principles of IFRS 13 Fair Value Measurement and on the ability of subsidiaries
       and affiliates having sufficient cash resources, in country, to service the underlying debt instrument’s obligations as and when these
       become due.                                        
       The risk relating to financial guarantees is managed per geographical region through review of cash flow forecasts, budgets and
       monitoring of covenants.                           
       The table below represents the full exposure of the Group in relation to these financial guarantees.
                                    Unaudited Unaudited Audited
                                      as at  as at Year ended
                                    27 March 28 March 26 September
       Rmillion                       2026   2025  2025   
       Guarantees issued in respect of the finance obligations 544.3 624.9 581.6
       – Guarantee of Wesbank loan agreements(1) 297.4 376.2 333.2
       – Guarantee of Numlite (Pty) Ltd finance obligations(2) 219.0 217.6 219.1
       – Guarantee of retailer finance obligation 27.9 31.1 29.3
       (1) SPAR assists retailers to obtain loans at the prime interest rate through an approved financial institution. These loans are backed by a
        guarantee from SPAR in favour of the institution, enabling our retailers access to finance at attractive rates. The financial institution fulfils
        all administrative activities relating to the repayment of these loans, and will only revert to SPAR in the unusual instance of default on the
        part of the retailer. Retailer loans are secured by notarial bonds over assets, deeds of suretyship, cession and pledge of shares and in
        some instances, lease options. The recoverability of amounts owed by retailers is regularly reviewed and assessed on an individual basis.
        The Board of Directors of SPAR (Board) has limited the guarantee facility to R1.0 billion (2025: R1.0 billion).
       (2) The Board has limited the guarantee facility to R250.0 million (2025: R250.0 million) relating to Numlite (Pty) Limited, which provides retail
        computer equipment to our independent retailers.  
                            13                            

--- Section unmapped | [AFS] physical page 17 | area selection | Table ---
THE SPAR GROUP LTD
INTERIM FINANCIAL
RESULTS 2026
9. Discontinued operations
The UK business continues to be classified as held for sale at 27 March 2026, as the Group remains committed to a plan to sell
this operation. Subsequent to the reporting date, the Group announced that it had entered into an agreement for the disposal of
its interests in the UK, refer to note 13 for further detail. The associated assets and liabilities continue to be presented as held for
sale, and the financial effects of the UK operation have been presented as discontinued operations in accordance with IFRS 5.
The comparative periods ended 28 March 2025 and 26 September 2025 included the Group’s Switzerland and Poland operations,
which were classified and presented as discontinued operations in those periods.
Financial performance

|  | Unaudited for the 26 weeks ended | Unaudited for the 26 weeks ended | Audited Year ended |
| --- | --- | --- | --- |
|  | 27 March | 28 March | 26 September |
| Rmillion | 2026 | 2025 | 2025 |
| Revenue – sale of merchandise | 2 153.9 | 10 461.8 | 20 697.7 |
| Cost of sales | (1 619.0) | (8 267.9) | (16 444.5) |
| Gross profit | 534.9 | 2 193.9 | 4 253.2 |
| Revenue – other | 42.0 | 648.9 | 1 275.2 |
| Other income | 6.0 | 74.7 | 111.9 |
| Net operating expenses | (698.6) | (7 834.3) | (10 901.1) |
| Operating loss | (115.7) | (4 916.8) | (5 260.8) |
| Other non-operating items | – | (30.0) | (178.9) |
| Finance income | 0.4 | 18.2 | 24.4 |
| Finance costs | (29.1) | (111.3) | (195.5) |
| Loss before taxation | (144.4) | (5 039.9) | (5 610.8) |
| Taxation | – | 13.5 | (37.1) |
| Loss from discontinued operation* | (144.4) | (5 026.4) | (5 647.9) |
| Remeasurement of retirement funds | – | (11.6) | (7.6) |
| Deferred tax relating to remeasurement of retirement funds | – | 1.7 | 1.1 |
| Reclassification of FCTR to profit or loss | – | – | (591.6) |
| Exchange loss differences from translation of discontinued operation | 7.0 | 153.8 | 65.3 |
| Total comprehensive loss | (137.4) | (4 882.5) | (6 180.7) |
| *** Included in the profit or loss of the discontinued operations in the current period are the following:** | | | |
|  | United Kingdom | Poland | Total |
| Loss after tax for the period | 98.4 | – | 98.4 |
| Disposal costs(1) | – | 46.0 | 46.0 |
| Total | 98.4 | 46.0 | 144.4 |

(1)  The Group recognised a provision of R46 million within discontinued operations relating to the settlement of matters arising from the
disposal and closure of the Poland operations. The provision primarily relates to estimated settlement and dispute resolution costs
associated with the exit process.
14

--- Section unmapped | [AFS] physical page 18 | area selection | Table ---
THE SPAR GROUP LTD
INTERIM FINANCIAL
RESULTS 2026
9. Discontinued operations continued
Cash flow information

|  | Unaudited for the 26 weeks ended | Unaudited for the 26 weeks ended |
| --- | --- | --- |
|  | 27 March | 28 March |
| Rmillion | 2026 | 2025 |
| Statement of cash flows |  |  |
| Net cash outflows from operating activities | (77.3) | (48.4) |
| Net cash outflows from investing activities | (2.8) | (673.5) |
| Net cash inflows/(outflows) from financing activities[^#] | 27.4 | (359.9) |
| [^#]  Excludes inter-group financing from SPAR. |  |  |
|  | Unaudited | Unaudited |
|  | for the | for the |
|  | 26 weeks | 26 weeks |
|  | ended | ended |
|  | 27 March | 28 March |
| Rmillion | 2026 | 2025 |
| Details of disposal group held for sale |  |  |
| Assets | 1 266.9 | 11 827.6 |
| Property, plant and equipment | 122.4 | 3 619.3 |
| Right-of-use assets | 417.6 | 3 903.7 |
| Lease receivable | 17.8 | 18.9 |
| Goodwill and intangible assets | 76.0 | 50.6 |
| Loans and other receivables | – | 136.3 |
| Deferred tax | 0.9 | 33.4 |
| Inventories | 340.7 | 2 069.4 |
| Trade and other receivables | 260.5 | 1 802.8 |
| Prepayments | 31.0 | 34.5 |
| Cash and cash equivalents | – | 120.2 |
| Other investments | – | 0.9 |
| Income tax receivable | – | 37.6 |
| Liabilities | 1 396.2 | 11 030.0 |
| Lease liability | 940.0 | 5 589.4 |
| Trade and other payables | 436.6 | 1 864.5 |
| Deferred tax liabilities | 19.6 | 351.8 |
| Post-employment benefit obligations | – | 29.6 |
| Bank overdrafts | – | 73.2 |
| Long-term borrowings | – | 3 121.5 |

Other assets held for sale
Land owned by the Company with a carrying value of R61.0 million has been classified as held for sale. In addition, the Company
holds other assets relating to corporate-owned stores that are classified as held for sale, amounting to R5.0 million.
15

--- Section unmapped | [AFS] physical page 19 | area selection | Table ---
THE SPAR GROUP LTD
INTERIM FINANCIAL
RESULTS 2026
10. Related-party transactions
Related-party relationships exist between the Company, its subsidiaries, key personnel within the Group and its shareholders.
These transactions occurred under terms and conditions no more favourable than transactions concluded with independent third
parties, unless otherwise stated below.
During the period, the following significant related-party transactions occurred with the subsidiaries of the Company:

|  | Unaudited for the 26 weeks ended | Unaudited for the 26 weeks ended |
| --- | --- | --- |
|  | 27 March | 28 March |
| Rmillion | 2026 | 2025 |
| Inter-company guarantee fees | – | 15.6 |
| Marketing and selling fees received | 32.7 | 40.3 |
| Dividends received | 478.6 | 66.2 |
| Sales | 106.1 | 103.9 |
| Purchases | (2 950.5) | (2 984.3) |
| 11. Capital commitments |  |  |
|  | Unaudited | Unaudited |
|  | for the | for the |
|  | 26 weeks | 26 weeks |
|  | ended | ended |
|  | 27 March | 28 March |
| Rmillion | 2026 | 2025 |
| Capital commitments |  |  |
| Contracted | 427.5 | 279.2 |
| Approved but not contracted | 884.9 | 1 234.8 |
| Total capital commitments | 1 312.4 | 1 514.0 |
| Analysed as follows: |  |  |
| Property, plant and equipment | 576.7 | 594.4 |
| Intangible assets | 91.5 | 205.2 |
| Investments | 644.2 | 714.4 |

Additions to PPE and intangible assets during the period amounted to R394.0 million (2025: R460.9 million), while disposals of PPE
and intangible assets amounted to R70.6 million (2025: R54.7 million).
12. Contingent liability
As was initially reported in the annual financial statements in respect of the year ended 30 September 2022, summons was served on
the Company by one of its retailers, the Giannacopoulos Group, for alleged damages of R2.1 billion arising from a membership dispute.
The Company denied any liability and has filed a plea to defend the matter. Management have engaged extensively with the retailer
and while many issues have been successfully resolved, a few major dispute matters could not be finalised. The parties have agreed
that the dispute be dealt with through a legal process. The Company continues to remain satisfied that, based on legal opinion, there
is insufficient evidence to substantiate the claim and does not recognise any liability for damages.
During the current period, summons was served on the Company by the Giannacopoulos Group in respect of an additional claim
for alleged damages of R168 million arising from the implementation of SAP ERP software at the KwaZulu-Natal Distribution
Centre. Through the approved SAP compensation process at the time, the Giannacopoulos Group was “entitled” to R1.55 million.
This compensation calculation was agreed to and signed off by the Company and the KZN regional guild and aligned to settlements
agreed to with other retailers. The Giannacopoulos Group countered, requesting compensation of R5.1 million at the time.
Based on the legal experts’ view and the previous settlements with other retailers, a settlement provision of R5.1 million has been
recognised in this regard at 27 March 2026.
16

--- Section unmapped | [AFS] physical page 20 | area selection | Financial note ---
                                                          
        THE SPAR GROUP LTD                                
        INTERIM FINANCIAL                                 
        RESULTS 2026                                      
    13. Events after the reporting date                   
       On 18 May 2026, the Group announced that it had entered into an asset purchase agreement with A.F. Blakemore & Son for the
       disposal of the South-West England SPAR licence, 71 owned company stores, associated warehouse and logistics infrastructure
       and related independent retailer supply agreements. In addition, a further 63 stores are in the process of being disposed of to third-
       party operators.                                   
       Completion of the transaction is expected to occur in stages between June and September 2026. Total gross proceeds are
       estimated of approximately GBP 13.0 million and the net cash outcome is expected to be broadly breakeven after transaction costs.
       The full financial and reporting effect of the transaction is being assessed by management. These stores are currently included within
       assets held for sale and discontinued operations.  
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                            17

### [ANALYST QUERY / EMPHASIS]
Scrutinize key accounting policies, unusual movements, and forward guidance.

### [SECTION READING RESPONSE / DETERMINATION]
### 1. Answers to Stored Questions for This Section

**Q15 [High]: Locate the definition of footnote [^R] on opening cash balance 2,742 (missing from p. 32 capture).**
- **Status**: `Resolved`
- **Answer & evidence**: The opening cash balance of R2,742.4m is confirmed in the cash flow statement `[unmapped, physical PDF p. 7]`. The footnote marker `*` attached to the opening balance line is defined at the bottom of the same page: *"The prior period comparative information for the period ended 28 March 2025 has been restated to correct an error in classification of the movement in general banking facilities of R494.0 million from Cash and cash equivalents to net movement on banking facilities as part of Cash flows (used in)/from financing activities to correctly reflect the treatment under IAS 7 Statement of Cash Flows. Refer to note 4."* Note 4 `[unmapped, physical PDF p. 12]` provides the full reconciliation, confirming the R494.0m reclassification and that the restated 28 March 2025 closing cash was R1,328.9m (previously R881.9m). The opening balance of R2,742.4m at 26 September 2025 is the audited closing balance and is not itself restated.

**Q16 [High]: Quantify the reclassification of bond perfected stores from non-current to current assets (footnote [^1]).**
- **Status**: `Resolved`
- **Answer & evidence**: The footnote `*` on the statement of financial position `[unmapped, physical PDF p. 5]` states: *"During the current financial period, the Group identified a prior period error pertaining to March 2025 of R457.8 million (September 2025: R215.6 million) in relation to current loans and receivables that was incorrectly classified as non-current."* This is a reclassification within "Loans and other receivables" — R457.8m moved from non-current to current at 28 March 2025, and R215.6m at 26 September 2025. It had no impact on equity, P&L, or cash flows.

**Q17 [High]: Quantify UK held-for-sale assets and liabilities included in "Other current assets/liabilities".**
- **Status**: `Resolved`
- **Answer & evidence**: Note 9 `[unmapped, physical PDF p. 18]` provides the full held-for-sale balance sheet: **Assets R1,266.9m** (PPE R122.4m, ROU R417.6m, lease receivable R17.8m, goodwill/intangible R76.0m, deferred tax R0.9m, inventories R340.7m, trade receivables R260.5m, prepayments R31.0m) and **Liabilities R1,396.2m** (lease liability R940.0m, trade payables R436.6m, deferred tax R19.6m). Note the statement of financial position shows total "Assets held for sale" of R1,332.9m `[p. 5]`, which includes the UK HFS assets of R1,266.9m plus other assets held for sale (land R61.0m + corporate store assets R5.0m = R66.0m) per `[p. 18]`. R1,266.9m + R66.0m = R1,332.9m — reconciles exactly.

**Q46 [Medium]: Get gross HFS assets and liabilities for UK at 31 Mar 2026; confirm net carrying value after R1.5bn impairment.**
- **Status**: `Resolved`
- **Answer & evidence**: Gross HFS assets R1,266.9m and liabilities R1,396.2m `[unmapped, physical PDF p. 18]`. Net liability position of R129.3m. The R1.5bn impairment was recognised in the prior period (H1 2025: impairment of assets held for sale R4,295.3m per note 2.2 `[p. 8]`; FY2025: R4,684.3m). In H1 2026, the only HFS impairment is R13.1m relating to Beyers Ridge land `[p. 16, note 7(1)]`, not UK. The UK carrying values above are post the prior-period impairment.

**Q28 [High]: Confirm whether AWG is presented as discontinued operations in H1 2026 (IFRS 5), gain/loss on disposal, and H2 trading loss phasing (~£5m).**
- **Status**: `Partially resolved (remainder stays open for [disposal note / H2 trading])`
- **Answer & evidence**: UK is confirmed as discontinued operations and held for sale `[unmapped, physical PDF p. 17, note 9]`. H1 2026 UK discontinued operating loss was R115.7m (group discontinued operating loss), with loss after tax of R144.4m including R46.0m Poland disposal costs `[p. 17]`. The disposal agreement with A.F. Blakemore & Son was announced 18 May 2026 (post-reporting date) `[p. 20, note 13]`: gross proceeds ~GBP 13.0m, net cash broadly breakeven after transaction costs, completion staged June–September 2026. **Gain/loss on disposal is NOT yet quantified** — note 13 states "The full financial and reporting effect of the transaction is being assessed by management." H2 trading loss phasing (~£5m) is not addressed in this section.

**Q38 [High]: Confirm UK HFS impairment R1.5bn excluded from headline earnings; locate HEPS reconciliation; confirm no further H2 write-down.**
- **Status**: `Partially resolved (remainder stays open for [H2 guidance])`
- **Answer & evidence**: The HEPS reconciliation `[unmapped, physical PDF p. 8, note 2.2]` shows "Impairment of assets held for sale" of R13.1m (H1 2026) vs R4,295.3m (H1 2025) and R4,684.3m (FY2025) — these are added back to arrive at headline earnings, confirming HFS impairments are excluded from HE. The R1.5bn UK impairment sits in the H1 2025 comparative (R4,295.3m total HFS impairment), not in H1 2026. **No further H2 write-down guidance is given in this section** — note 13 says the full effect is still being assessed.

**Q35 [High]: Confirm both H1 2026 and H1 2025 revenue, GP, and operating profit are on the 26-week calendar basis; check for "as reported vs restated" bridge.**
- **Status**: `Resolved`
- **Answer & evidence**: Note 3 `[unmapped, physical PDF p. 11]` confirms the 52-week/26-week Friday-ending calendar was adopted prospectively, and both H1 2026 (26 weeks ended 27 March 2026) and H1 2025 (26 weeks ended 28 March 2025) are on this basis. However, an **"as reported vs as adjusted" bridge** is provided `[pp. 11–12]` for the 2025 comparative to strip out additional trading days: H1 2025 revenue as reported R65,890.4m vs **as adjusted R66,822.4m** (+R932.0m); operating profit as reported R1,353.7m vs **as adjusted R1,403.4m** (+R49.7m); PBT as reported R994.2m vs **as adjusted R1,039.3m** (+R45.1m). H1 2026 has no adjustment (as reported = as adjusted). This is a critical comparability bridge.

**Q44 [Medium]: Confirm H1 2025 UK comparatives not restated to 182 days; quantify 3-day impact; check H2 ~£5m loss phasing on matched-day basis.**
- **Status**: `Partially resolved (remainder stays open for [H2 phasing])`
- **Answer & evidence**: The as-reported vs as-adjusted bridge `[pp. 11–12]` applies to **continuing operations** (SA and Ireland), not to UK discontinued operations. The UK discontinued note `[p. 17]` shows H1 2025 revenue R10,461.8m and operating loss R4,916.8m with no day-count adjustment disclosed. The 3-day impact on UK is not separately quantified. H2 ~£5m loss phasing is not addressed.

**Q29 [High]: Locate full H1 2026 group revenue growth and Feb–Mar run-rate; confirm Easter calendar shift impact on H2 y-o-y comparatives.**
- **Status**: `Partially resolved (remainder stays open for [trading update / H2 guidance])`
- **Answer & evidence**: Group revenue from contracts with customers (continuing) = **R68,592.1m** `[unmapped, physical PDF p. 9]`, vs H1 2025 as reported R65,890.4m (+4.1%) and as adjusted R66,822.4m (+2.6%). Merchandise revenue R67,482.5m vs R65,160.2m as reported (+3.6%). Other revenue R1,109.6m vs R730.2m (+51.9%). Feb–Mar run-rate and Easter shift impact are not addressed in this section.

**Q43 [Medium]: Decompose other revenue +54.0% to R887.6m (VSP fees, G&L liquor, other); confirm recurring vs one-off and GP vs operating income treatment.**
- **Status**: `Partially resolved (remainder stays open for [revenue note])`
- **Answer & evidence**: Note 3 `[unmapped, physical PDF p. 11]` disaggregates total other revenue of **R1,109.6m** (not R887.6m — that figure appears to relate to a different scope): Marketing and service revenues R839.5m (vs R471.0m, +78.2%), Franchise fees R127.1m (vs R116.1m, +9.5%), Other services R143.0m (vs R143.1m, flat). By segment: SA other revenue R833.0m (vs R468.0m), Ireland R276.6m (vs R262.2m). Other revenue is presented **below gross profit** in the P&L `[p. 4]`, so it flows to operating income, not gross profit. Recurring vs one-off split is not explicitly stated.

**Q26 [High]: Confirm basis of "~EUR 70m EBITDA* — *12 months to March 2026" (pre/post IFRS 16, pre/post exceptionals, BWG-only vs all Ireland). Reconcile to Ireland segment operating profit.**
- **Status**: `Partially resolved (remainder stays open for [Ireland segment note])`
- **Answer & evidence**: Ireland segment operating profit H1 2026 = **R502.8m** `[unmapped, physical PDF p. 9]`; H1 2025 = R486.0m as reported, R494.4m as adjusted `[p. 12]`. Ireland D&A H1 2026 = R288.1m `[p. 9]`. Implied Ireland EBITDA (op profit + D&A) = R790.9m for 26 weeks, annualised ~R1,581.8m. At implied ~R19.11/EUR (from Q37), that is ~EUR 82.8m — above the ~EUR 70m figure, suggesting the ~EUR 70m may be pre-IFRS 16 or exclude some items. **Basis still not confirmed in this section.**

**Q31 [Medium]: Check whether management guides to a wholesale GP% trade-off from "retailer profitability as primary operating metric".**
- **Status**: `Partially resolved (remainder stays open for [Ireland segment note])`
- **Answer & evidence**: Group gross profit H1 2026 = R7,111.7m on merchandise revenue R67,482.5m = **10.54% GP margin** `[unmapped, physical PDF p. 4]`. H1 2025: R6,998.0m / R65,160.2m = **10.74%**. GP% declined ~20bps. Ireland segment: revenue R16,975.7m, cost of sales R14,408.2m → GP R2,567.5m = **15.12%** (note: this includes other revenue in the revenue line per segment note `[p. 9]`). SA segment: revenue R51,616.4m, cost of sales R45,962.6m → GP R5,653.8m = **10.95%**. No explicit trade-off guidance in this section.

**Q42 [High]: Quantify "change in accounting estimates" (YTD depreciation catch-up Nov 2025; RCC amortisation timing Dec 2025) impact on Ireland opex; confirm recurrence in H2.**
- **Status**: `Partially resolved (remainder stays open for [Ireland segment note])`
- **Answer & evidence**: Group D&A H1 2026 = R549.3m `[unmapped, physical PDF p. 9]` vs H1 2025 R551.7m (continuing) — flat. Ireland D&A R288.1m vs R293.0m — slightly down. No explicit "change in accounting estimates" line or quantum is disclosed in this section. **Still open.**

**Q36 [Medium]: Locate IFRS 5 note: confirm Switzerland and UK both presented as discontinued; get Switzerland disposal status/gain-loss and held-for-sale balances.**
- **Status**: `Partially resolved (remainder stays open for [Switzerland status])`
- **Answer & evidence**: Note 9 `[unmapped, physical PDF p. 17]` confirms: *"The comparative periods ended 28 March 2025 and 26 September 2025 included the Group's Switzerland and Poland operations, which were classified and presented as discontinued operations in those periods."* In H1 2026, only UK remains in discontinued operations. Switzerland and Poland are no longer in discontinued ops — they have been disposed of or deconsolidated. **Switzerland disposal gain/loss and HFS balances are not disclosed in this section** (they were in prior periods).

**Q45 [Medium]: Locate Switzerland disposal status, gain/loss, and held-for-sale balances; confirm both UK and Switzerland in discontinued.**
- **Status**: `Partially resolved (remainder stays open for [prior-year notes])`
- **Answer & evidence**: As above — Switzerland was in discontinued operations in H1 2025 and FY2025 but is **not** in H1 2026 discontinued operations `[unmapped, physical PDF p. 17]`. The H1 2025 discontinued loss of R5,026.4m included Switzerland and Poland. No Switzerland-specific gain/loss or HFS balance is disclosed in this H1 2026 section.

**Q37 [Low]: Confirm ZAR/EUR translation rate used and whether ~EUR 70m EBITDA (Q26) is translated at the same rate as Ireland segment operating profit.**
- **Status**: `Partially resolved (remainder stays open for [FX note])`
- **Answer & evidence**: No explicit ZAR/EUR rate is stated in this section. Implied rate from UK HFS impairment (Q17/Q46): R1.5bn / EUR 78.5m ≈ R19.11/EUR (from prior capture). Ireland segment figures are translated at the average rate for the period. **Explicit rate still not confirmed.**

**Q32 [Medium]: Confirm net debt/EBITDA ratio at 31 March 2026 and any stated deleveraging target.**
- **Status**: `Partially resolved (remainder stays open for [debt note])`
- **Answer & evidence**: From the balance sheet `[unmapped, physical PDF p. 5]`: Borrowings non-current R6,403.6m + current R573.9m = **R6,977.5m**; Bank overdrafts R1,430.7m; Cash – SPAR R1,069.5m; Cash – Guilds/trusts R527.7m. Net debt (borrowings + overdrafts – cash) = R6,977.5m + R1,430.7m – R1,069.5m – R527.7m = **R6,811.0m**. Lease liabilities R6,930.4m + R1,489.8m = R8,420.2m (IFRS 16). **Net debt/EBITDA ratio and deleveraging target not stated in this section.**

**Q23 [Low]: Confirm split of hedged vs unhedged debt and interest rate sensitivity (hedged rate applies to R800m).**
- **Status**: `Partially resolved (remainder stays open for [debt note])`
- **Answer & evidence**: Finance costs H1 2026 = R667.5m `[unmapped, physical PDF p. 4]` vs R669.0m H1 2025 — flat. Finance income R304.6m vs R307.3m — flat. Net finance costs R362.9m vs R361.7m as reported `[p. 11]`. **Hedged vs unhedged split not disclosed in this section.**

**Q24 [Low]: Reconcile working capital chart (excludes Poland and Switzerland) to balance sheet lines.**
- **Status**: `Partially resolved (remainder stays open for [working capital note])`
- **Answer & evidence**: Cash flow note 5 `[unmapped, physical PDF p. 13]` shows net working capital changes of **(R1,839.7m)** vs (R508.0m) H1 2025. Components: decrease in inventories R63.0m (vs increase R367.4m), increase in trade receivables (R61.0m) (vs R463.4m), decrease in trade payables and provisions **(R1,841.7m)** (vs increase R322.8m). The massive payables outflow is the key driver of the cash absorption. **Chart reconciliation to balance sheet lines still open.**

**Q39 [High]: Confirm whether R273m is specific or portfolio ECL; get ECL allowance balance, satisfactory-paid %, collection rate, ageing buckets; check H2 provisioning guidance.**
- **Status**: `Partially resolved (remainder stays open for [debtors note])`
- **Answer & evidence**: Note 5 `[unmapped, physical PDF p. 13]` shows "Movement in provisions raised against trade receivables and loans" of **R150.7m** (vs R45.5m H1 2025) — this is the P&L charge for the period, not the R273m specific impairment referenced in prior captures. The R273m figure is not visible in this section. **ECL allowance balance, satisfactory-paid %, collection rate, ageing buckets, and H2 guidance are not in this section.**

**Q14 [High]: Get ECL allowance, satisfactory-paid %, collection rate, write-offs, and ageing analysis. Reconcile to the R273m specific impairment charge.**
- **Status**: `Partially resolved (remainder stays open for [debtors note])`
- **Answer & evidence**: As above — only the R150.7m P&L movement in provisions is visible `[p. 13]`. The R273m specific impairment and R58m G&L write-offs are not in this section. **Still open.**

**Q5 [High]: Gross debtors, ECL allowance, satisfactory-paid %, collection rate, write-offs — explain "increase in overdues".**
- **Status**: `Partially resolved (remainder stays open for [debtors note])`
- **Answer & evidence**: Trade and other receivables on balance sheet = **R15,975.2m** `[unmapped, physical PDF p. 5]` vs R15,216.3m (restated) at 28 March 2025 and R16,107.3m at 26 September 2025. The R150.7m provision movement `[p. 13]` is the only credit-quality data point in this section. **Satisfactory-paid %, collection rate, ageing, and overdues explanation still open.**

**Q18 [Medium]: Break down the R143m "Legacy matters" column on OP analysis into its components.**
- **Status**: `Partially resolved (remainder stays open for [OP analysis note])`
- **Answer & evidence**: Note 7 `[unmapped, physical PDF p. 16]` details impairments totalling R128.6m: HFS R13.1m (Beyers Ridge land), goodwill R47.4m (Hajimarkos stores — The Square and 2nd Avenue), PPE/intangible R41.2m (GiCom software R30.7m SA + Ireland property R10.2m), ROU asset R26.9m (3 SA stores R22.7m + Ireland vacant property R1.8m). Note 6.5 `[p. 15]` shows business acquisition costs R9.8m (R4.5m completed + R5.3m not yet finalised). Note 12 `[p. 19]` shows R5.1m settlement provision for Giannacopoulos SAP claim. **The R143m "Legacy matters" column is not directly visible in this section** — these are the underlying components that likely feed it.

**Q19 [Medium]: Confirm where the VSP cost R27.3m is recorded and the phasing of the R33.2m annual savings.**
- **Status**: `Partially resolved (remainder stays open for [VSP note])`
- **Answer & evidence**: Not visible in this section. **Still open.**

**Q6 [Medium]: Corporate store count, losses, closure/transfer plans.**
- **Status**: `Partially resolved (remainder stays open for [store network note])`
- **Answer & evidence**: Note 7(4) `[unmapped, physical PDF p. 16]` confirms *"corporate-owned stores continue to be assessed as separate cash-generating units"* and *"Certain stores transitioned from profit-making to loss-making positions during the current period"* — three SA stores had ROU assets impaired by R22.7m. Note 6.1 `[p. 13]` confirms 8 SA retail stores acquired (Hajimarkos group, 1 Feb 2026, R162.0m consideration, R149.8m goodwill). Note 6.6 `[p. 15]` confirms 5 SA retail stores sold. **Corporate store count and closure/transfer plans still open.**

**Q12 [Low]: Absolute revenue and profit contribution of SPAR Health (+26.1% growth) and Build it.**
- **Status**: `Resolved`
- **Answer & evidence**: Note 3 `[unmapped, physical PDF p. 11]`: SPAR Health revenue R1,203.1m (vs R943.8m, +27.5%); Build it revenue R5,150.3m (vs R5,074.8m, +1.5%). SPAR R37,727.9m (+2.3%); Liquor R6,406.1m (+4.6%); Encore R264.7m (+24.9%); Pet Storey R31.3m (new). **Profit contribution by brand is not disclosed** — only revenue.

**Q51 [Low]: Get SPAR Health absolute revenue and profit; confirm +26.1% growth base and H2 run-rate.**
- **Status**: `Partially resolved (remainder stays open for [H2 run-rate])`
- **Answer & evidence**: SPAR Health revenue R1,203.1m vs R943.8m = **+27.5%** (not +26.1% — slight discrepancy with prior capture; the +26.1% may have been a different metric or period). Profit not disclosed. H2 run-rate not addressed.

**Q40 [High]: Confirm whether Sri Lanka is equity-accounted or consolidated; get contribution to group operating profit and whether it sits in "6 countries".**
- **Status**: `Partially resolved (remainder stays open for [associates note])`
- **Answer & evidence**: "Share of equity-accounted associate (losses)/profits" = **(R4.8m)** H1 2026 vs R4.4m H1 2025 `[unmapped, physical PDF p. 4]`. By segment `[p. 9]`: SA +R1.4m, Ireland **(R6.2m)**. Investment in associates and JVs = R141.7m `[p. 5]`. **Sri Lanka is equity-accounted** (it sits in the associate line, and the Ireland segment shows the R6.2m loss — suggesting Sri Lanka is reported within the Ireland segment or separately). The R6.2m Ireland associate loss likely includes Sri Lanka. **Whether Sri Lanka sits in "6 countries" still open.**

**Q27 [High]: Confirm which entities are consolidated vs retailer/licence footprint given "6 countries" vs "SA and Ireland only". Check geographic segment note for Namibia, Botswana, Swaziland, Mozambique revenue/profit.**
- **Status**: `Partially resolved (remainder stays open for [geographic note])`
- **Answer & evidence**: Note 3 `[unmapped, physical PDF p. 9]` states the Group has **two reportable segments: Southern Africa and Ireland**. No separate disclosure for Namibia, Botswana, Swaziland, Mozambique. The segment note says *"The Group deals with a broad spread of customers, with no single customer exceeding 10% of the Group's revenue."* **Geographic breakdown within Southern Africa still not disclosed.**

**Q7 [Medium]: Whether foreign ops (Swaziland, Namibia, Mozambique, Botswana — loyalty 59.4%) flagged for impairment/exit.**
- **Status**: `Partially resolved (remainder stays open for [geographic note])`
- **Answer & evidence**: No impairment or exit flag for these operations in this section. Note 9 `[p. 17]` confirms only UK remains in discontinued operations; Switzerland and Poland were disposed of in prior periods. **Still open.**

**Q21 [Medium]: Check if any of these foreign ops are flagged for impairment/exit.**
- **Status**: `Partially resolved (remainder stays open for [geographic note])`
- **Answer & evidence**: As above — no flag in this section. **Still open.**

**Q33 [Low]: Reconcile store counts (2000+ stores, 1000+ retailers, ~1 068 Ireland stores) to operational metrics; confirm net store movement H1 2026.**
- **Status**: `Partially resolved (remainder stays open for [store network note])`
- **Answer & evidence**: Note 6.1 `[p. 13]`: 8 SA retail stores acquired, 0 BWG retail stores acquired (vs 3 in Ireland H1 2025). Note 6.6 `[p. 15]`: 5 SA retail stores sold. Note 13 `[p. 20]`: UK disposal includes 71 owned company stores + 63 stores being disposed to third parties. **Net store movement by segment still not fully reconciled.**

**Q49 [Medium]: Get net store movement H1 2026 by segment (SA, Ireland, Sri Lanka); confirm total group store count.**
- **Status**: `Partially resolved (remainder stays open for [store network note])`
- **Answer & evidence**: SA: +8 acquired, –5 sold = net +3 retail stores (plus corporate store impairments). Ireland: 0 acquired. UK: 71 + 63 being disposed. **Total group store count and Sri Lanka movement still open.**

**Q34 [Low]: Confirm date and scope (SA-only vs group) of "Convenience 38% *AC Nielsen" market share.**
- **Status**: `Partially resolved (remainder stays open for [market share note])`
- **Answer & evidence**: Not addressed in this section. **Still open.**

**Q52 [Low]: Confirm Nielsen date/as-at period and whether 38% is value or volume, Republic of Ireland only.**
- **Status**: `Partially resolved (remainder stays open for [market share note])`
- **Answer & evidence**: Not addressed in this section. **Still open.**

**Q48 [Medium]: Reconcile pro-forma SA G&L transactions –2.30%/basket +3.53% to group SA revenue +1.7%; confirm KZN-specific split.**
- **Status**: `Partially resolved (remainder stays open for [trading update])`
- **Answer & evidence**: SA merchandise revenue H1 2026 = R50,783.4m vs R49,229.9m = **+3.2%** `[unmapped, physical PDF p. 11]`. SA total revenue from contracts with customers R51,616.4m vs R49,697.9m = **+3.9%** as reported, or vs R50,441.6m as adjusted `[p. 12]` = **+2.3%**. The +1.7% figure from prior capture may be a different metric (perhaps like-for-like or a specific sub-segment). **KZN-specific split still open.**

**Q10 [Medium]: Reconcile KZN sales +4.9% y-o-y vs group retail sales +c.1% vs transactions –2.3% (volume vs basket inflation).**
- **Status**: `Partially resolved (remainder stays open for [trading update])`
- **Answer & evidence**: As above — SA merchandise revenue +3.2% as reported. **KZN-specific split still open.**

**Q9 [Medium]: Quantify KZN H2 run-rate profit vs R123m H1 hit; confirm GP% recovery trajectory and "3 consecutive months of profit".**
- **Status**: `Partially resolved (remainder stays open for [KZN note])`
- **Answer & evidence**: Not addressed in this section. **Still open.**

**Q20 [Medium]: Confirm the exact months and profit quantum for the "3 consecutive months of profit" claim.**
- **Status**: `Partially resolved (remainder stays open for [KZN note])`
- **Answer & evidence**: Not addressed in this section. **Still open.**

**Q30 [Medium]: Get rand quantum of Jan–Mar KZN operating profit and GP% by month; reconcile to R123m H1 hit.**
- **Status**: `Partially resolved (remainder stays open for [KZN note])`
- **Answer & evidence**: Not addressed in this section. **Still open.**

**Q50 [Low]: Confirm SA segment PAT and equity base; reconcile negative ROE –6.8% to R273m provisions and R159m extraordinary items.**
- **Status**: `Partially resolved (remainder stays open for [segment note])`
- **Answer & evidence**: SA segment **loss before tax = (R50.9m)** `[unmapped, physical PDF p. 9]` vs profit R602.9m H1 2025. SA taxation = **+R2.4m** (a tax credit) vs R167.3m charge. SA segment total assets R28,097.2m, total liabilities R26,690.1m → **net assets R1,407.1m**. Ireland: PBT R413.9m, tax R68.9m, total assets R16,751.0m, liabilities R12,756.8m → net assets R3,994.2m. Group equity R5,401.3m. **SA ROE on R1,407.1m net assets with near-zero PAT is deeply negative — consistent with the –6.8% figure. The R273m provisions and R159m extraordinary items are not separately visible in this section but the SA PBT collapse from R602.9m to (R50.9m) is the key driver.**

**Q13 [Low]: Capitalised vs expensed SAP costs; go-live timeline; "various investments ongoing".**
- **Status**: `Partially resolved (remainder stays open for [SAP note])`
- **Answer & evidence**: Note 7(3) `[unmapped, physical PDF p. 16]` confirms **R30.7m GiCom software module impairment** — software "remains under development" but "would not be deployed due to limited expected utilisation" and was "fully impaired." This is a SAP-adjacent IT write-off. Note 12 `[p. 19]` references the Giannacopoulos SAP ERP claim at KZN DC. **Capitalised vs expensed SAP split and go-live timeline still open.**

**Q22 [Medium]: Get capitalised vs expensed SAP costs and go-live timeline.**
- **Status**: `Partially resolved (remainder stays open for [SAP note])`
- **Answer & evidence**: As above — GiCom impairment R30.7m confirmed. **Split and timeline still open.**

**Q47 [Medium]: Get capitalised vs expensed SAP split for H1 2026 and FY2026 guidance; confirm Finance Go-Live FY2026 and DC Integration FY2027 timing.**
- **Status**: `Partially resolved (remainder stays open for [SAP note])`
- **Answer & evidence**: As above. **Still open.**

**Q25 [Low]: Confirm the phasing and treatment (discontinued ops) of forecast H2 trading losses (UK) ~£5m.**
- **Status**: `Partially resolved (remainder stays open for [UK disposal note])`
- **Answer & evidence**: UK is confirmed discontinued `[unmapped, physical PDF p. 17]`. H1 2026 UK operating loss R115.7m (group discontinued). Note 13 `[p. 20]` confirms disposal completion staged June–September 2026. **H2 ~£5m loss phasing not addressed.**

**Q8 [Medium]: Locate missing footnote definitions for loyalty chart markers [^a], [^M], [^A], [^l], [^t], [^2], [^i].**
- **Status**: `Partially resolved (remainder stays open for [loyalty note])`
- **Answer & evidence**: Not addressed in this section. **Still open.**

---

### 2. Footnote & Qualification Deep-Dive

**Footnote `*` — Prior period error: current vs non-current loans and receivables** `[unmapped, physical PDF p. 5]`
- **Text**: *"During the current financial period, the Group identified a prior period error pertaining to March 2025 of R457.8 million (September 2025: R215.6 million) in relation to current loans and receivables that was incorrectly classified as non-current."*
- **Implication**: This is a reclassification within "Loans and other receivables" — R457.8m moved from non-current to current at 28 March 2025, and R215.6m at 26 September 2025. It has **no impact on equity, P&L, or cash flows**. For forecasting, the current/non-current split of loans and receivables should use the restated figures: current R550.3m (restated) at 28 March 2025 and R278.8m at 26 September 2025; non-current R224.4m (restated) and R190.7m. **Verify in note 4** whether the R457.8m/R215.6m are the only reclassifications or whether there are further adjustments.

**Footnote `[^#]` — Prior period error: general banking facilities reclassification** `[unmapped, physical PDF p. 5]`
- **Text**: *"The prior period comparative information as at 28 March 2025 has been restated to correct an error in the classification of general banking facilities of R494.0 million from cash and cash equivalents to bank overdrafts. Refer to note 4 for further detail."*
- **Implication**: At 28 March 2025, cash and cash equivalents were restated **down** by R494.0m and bank overdrafts restated **up** by R494.0m. This flows through to the cash flow statement `[p. 7]` where the closing cash balance was restated from R881.9m to R1,328.9m (note 4 `[p. 12]` clarifies the R494.0m increase in closing cash on the cash flow statement). **Critical for forecasting**: the "Net cash and cash equivalents" line of R584.5m at 27 March 2026 `[p. 12]` excludes R418.0m of general banking facility overdrafts, which are shown separately. The "Net cash and banking facilities" of R166.5m is the true liquidity position. **Verify in note 4** the full reconciliation and whether the R494.0m is the only restatement.

**Footnote `(1)` — Prior period error: inter-company receivable/payable elimination** `[unmapped, physical PDF p. 5]`
- **Text**: *"The prior period comparative information as at 28 March 2025 has been restated to correct an error relating to inter-company receivable and payable balances which was not correctly eliminated of R672.0 million."*
- **Implication**: At 28 March 2025, trade and other receivables and trade and other payables were both restated **down** by R672.0m (gross-up eliminated). This has **no impact on equity, P&L, or cash flows** but reduces both current assets and current liabilities by R672.0m. **Critical for working capital forecasting**: the restated 28 March 2025 receivables of R15,216.3m and payables of R20,315.9m are the correct comparatives. The H1 2026 receivables of R15,975.2m and payables of R20,561.9m should be compared to these restated figures, not the originally reported ones.

**Footnote `*` — Cash flow statement: general banking facilities restatement** `[unmapped, physical PDF p. 7]`
- **Text**: *"The prior period comparative information for the period ended 28 March 2025 has been restated to correct an error in classification of the movement in general banking facilities of R494.0 million from Cash and cash equivalents to net movement on banking facilities as part of Cash flows (used in)/from financing activities to correctly reflect the treatment under IAS 7 Statement of Cash Flows. Refer to note 4."*
- **Implication**: The H1 2025 "Net movement on banking facilities" was restated from (R2,199.0m) to include the R494.0m, and the closing cash balance was restated from R881.9m to R1,328.9m. **For forecasting**: the H1 2026 net movement on banking facilities of (R252.0m) is on the corrected basis. The opening cash of R2,742.4m is the audited 26 September 2025 closing balance and is not restated.

**Footnote `(1)` — General banking facilities: 364-day contracted, overnight call** `[unmapped, physical PDF p. 7]`
- **Text**: *"General banking facilities are contracted for a 364-day period, however individual drawdowns are utilised on an overnight call basis, thereby allowing the Group to access these facilities on a short-term basis to manage daily liquidity requirements."*
- **Implication**: The R418.0m of general banking facility overdrafts `[p. 12]` are technically short-term but roll over daily. **For forecasting**: treat these as part of the working capital/liquidity management, not as long-term debt. The "Net cash and banking facilities" of R166.5m is the true liquidity buffer.

**Footnote `[^#]` — Segment note: Encore re-presentation** `[unmapped, physical PDF p. 11]`
- **Text**: *"Comparative information has been re-presented to separately disclose Encore revenue from SPAR. In the prior period, Encore revenue was included within SPAR and was not presented as a separate line item. This re-presentation has been made to enhance the transparency and comparability of segmental revenue disclosures and has no impact on previously reported total Group revenue or profit."*
- **Implication**: Encore revenue H1 2026 = R264.7m vs R212.0m H1 2025 (re-presented). SPAR revenue H1 2026 = R37,727.9m vs R36,876.9m (re-presented). **For forecasting**: use the re-presented H1 2025 figures for like-for-like brand growth. Encore growth = +24.9%; SPAR growth = +2.3%.

**Footnote `[^#]` — Segment note: Change in reporting weeks** `[unmapped, physical PDF p. 11]`
- **Text**: *"In the prior reporting period, the CODM changed the Group's financial year end to align with the retail industry's general practice of dividing the financial reporting calendar into 52 weeks of seven days, with each reporting week ending on a Friday, allowing for better comparability between the reporting periods. This change was adopted prospectively. The results for the 26 weeks ended 27 March 2026 have been prepared on this basis. The prior period results ended 28 March 2025 were also prepared on this basis."*
- **Implication**: Both H1 2026 and H1 2025 are on the 26-week Friday-ending basis. **However**, the "as reported vs as adjusted" bridge `[pp. 11–12]` shows the H1 2025 comparative had **additional trading days** that need to be stripped out for true like-for-like comparison: revenue as reported R65,890.4m vs as adjusted R66,822.4m (+R932.0m); operating profit R1,353.7m vs R1,403.4m (+R49.7m); PBT R994.2m vs R1,039.3m (+R45.1m). **Critical for forecasting**: the H1 2026 vs H1 2025 as-adjusted comparison shows group revenue +2.6% (not +4.1%), operating profit –47.2% (not –45.3%), and PBT –65.1% (not –63.5%). The as-adjusted figures are the correct like-for-like comparatives.

**Footnote `*` — Note 4: Cash and cash equivalents reconciliation** `[unmapped, physical PDF p. 12]`
- **Text**: *"The Group's general banking facilities, which include call accounts and associated overdraft balances, included banking facilities that have been separately disclosed in the current period to correct an error in classification between Cash and cash equivalents and Cash flows (used in)/from financing activities and to provide improved transparency over the composition of cash and cash equivalents. As a result, movements in these facilities are now presented separately. Comparative figures for the period ended 28 March 2025 have been restated accordingly to ensure consistency with the current period's presentation. The adjustment to the comparative figures for the period ended 28 March 2025 was a R494.0 million increase in the closing balance of cash and cash equivalents on the statement of cash flows (previously R881.9 million)."*
- **Implication**: The cash reconciliation `[p. 12]` shows: Bank balances – Guilds/trusts R527.7m + SPAR R1,069.5m – SPAR other overdrafts (R1,012.7m) = **Net cash and cash equivalents R584.5m**. Then – general banking facilities (R418.0m) = **Net cash and banking facilities R166.5m**. **For forecasting**: the R584.5m is the IFRS cash flow statement figure; the R166.5m is the true liquidity position including all facilities. The R1,012.7m "SPAR other" overdrafts are separate from the R418.0m general banking facilities.

**Footnote `(1)` — Note 7: Beyers Ridge land impairment** `[unmapped, physical PDF p. 16]`
- **Text**: *"Beyers Ridge land, classified as an asset held for sale, was previously impaired in FY2025 based on an estimated recoverable value of approximately R80 million. During the current period, a contractual selling price of R65 million was negotiated, resulting in a further impairment loss being recognised at 27 March 2026 to reduce the carrying amount to the agreed fair value less costs to sell."*
- **Implication**: R13.1m further impairment in H1 2026. The land is now carried at R65m (fair value less costs to sell). **For forecasting**: this is a one-off, non-recurring item. The R13.1m is added back in the HEPS reconciliation `[p. 8]`.

**Footnote `(2)` — Note 7: Hajimarkos goodwill impairment** `[unmapped, physical PDF p. 16]`
- **Text**: *"On 1 February 2026, Southern Africa acquired eight stores from the Hajimarkos group. In terms of the acquisition agreement, the purchase consideration amounted to R162.0 million, which exceeded current market-related valuations, resulting in goodwill of R149.8 million being recognised on acquisition. Following an impairment assessment performed at 27 March 2026, two stores, namely The Square and 2nd Avenue, were identified as experiencing operational performance challenges. Consequently, an impairment loss was recognised against goodwill during the period."*
- **Implication**: R47.4m goodwill impairment (per note 7 table) on the Hajimarkos acquisition, just two months after acquisition. This is a **red flag** on acquisition discipline — R149.8m goodwill recognised, R47.4m (31.6%) impaired within 2 months. **For forecasting**: question whether further Hajimarkos goodwill impairment is likely in H2. The R47.4m is added back in HEPS `[p. 8]`.

**Footnote `(3)` — Note 7: GiCom software and Ireland property impairment** `[unmapped, physical PDF p. 16]`
- **Text**: *"Southern Africa recognised an impairment of R30.7 million relating to the GiCom software module, which remains under development at 27 March 2026. Based on an assessment performed by the Technology team together with the National Merchandising Executive, it was determined that the software would not be deployed due to limited expected utilisation. Accordingly, the software development costs were fully impaired. In Ireland, an independent valuation performed by a professional valuer identified that the recoverable amount of a property was below its carrying value, resulting in an impairment loss of R10.2 million being recognised during the period."*
- **Implication**: R30.7m SA GiCom software write-off (failed IT project) + R10.2m Ireland property impairment = R41.2m total PPE/intangible impairment. **For forecasting**: the GiCom write-off is a one-off but signals IT project risk — check whether other software projects (SAP, etc.) are at risk. The R41.2m is added back in HEPS `[p. 8]`.

**Footnote `(4)` — Note 7: ROU asset impairment** `[unmapped, physical PDF p. 16]`
- **Text**: *"In Southern Africa, corporate-owned stores continue to be assessed as separate cash-generating units, consistent with the approach adopted in FY2025. Certain stores transitioned from profit-making to loss-making positions during the current period, representing an indicator of impairment. Based on the impairment assessment performed, right-of-use assets relating to three stores were impaired by R22.7 million at 27 March 2026. In Ireland, a tenant occupying one of the Group's properties experienced financial difficulties, resulting in the property becoming vacant. Management was subsequently unable to secure a suitable replacement tenant and, following an impairment assessment, an impairment loss of R1.8 million was recognised at 27 March 2026."*
- **Implication**: R22.7m SA corporate store ROU impairment (3 stores) + R1.8m Ireland vacant property = R26.9m total. **For forecasting**: the SA corporate store portfolio is under pressure — 3 stores transitioned from profit to loss in H1. Check H2 for further corporate store impairments. The R26.9m is added back in HEPS `[p. 8]`.

**Footnote `(1)` — Note 8: Wesbank loan guarantees** `[unmapped, physical PDF p. 16]`
- **Text**: *"SPAR assists retailers to obtain loans at the prime interest rate through an approved financial institution. These loans are backed by a guarantee from SPAR in favour of the institution, enabling our retailers access to finance at attractive rates. The financial institution fulfils all administrative activities relating to the repayment of these loans, and will only revert to SPAR in the unusual instance of default on the part of the retailer. Retailer loans are secured by notarial bonds over assets, deeds of suretyship, cession and pledge of shares and in some instances, lease options. The recoverability of amounts owed by retailers is regularly reviewed and assessed on an individual basis. The Board of Directors of SPAR (Board) has limited the guarantee facility to R1.0 billion (2025: R1.0 billion)."*
- **Implication**: R297.4m guarantee exposure to Wesbank retailer loans (down from R376.2m). The R1.0bn facility limit means there is R702.6m of headroom. **For forecasting**: this is a contingent liability, not on balance sheet. The decline in exposure suggests either retailer repayments or reduced uptake. Check whether the R150.7m provision movement `[p. 13]` includes any Wesbank-related provisions.

**Footnote `(2)` — Note 8: Numlite guarantee** `[unmapped, physical PDF p. 16]`
- **Text**: *"The Board has limited the guarantee facility to R250.0 million (2025: R250.0 million) relating to Numlite (Pty) Limited, which provides retail computer equipment to our independent retailers."*
- **Implication**: R219.0m guarantee exposure to Numlite (flat vs R217.6m). R31.0m headroom. **For forecasting**: stable contingent liability.

**Footnote `*` — Note 9: Discontinued operations loss composition** `[unmapped, physical PDF p. 17]`
- **Text**: *"Included in the profit or loss of the discontinued operations in the current period are the following: United Kingdom loss after tax 98.4; Poland disposal costs 46.0; Total 144.4."*
- **Implication**: The R144.4m discontinued loss comprises **R98.4m UK loss after tax** + **R46.0m Poland disposal costs**. The Poland provision relates to *"estimated settlement and dispute resolution costs associated with the exit process"* `[p. 17, note 9(1)]`. **For forecasting**: the R46.0m Poland cost is a one-off; the R98.4m UK loss is the run-rate to model for H2 (though disposal completion June–September 2026 will truncate it). The UK H1 operating loss was R115.7m; after finance costs (R29.1m) and tax (nil), the loss after tax is R144.4m — but this includes Poland R46.0m, so **UK-only loss after tax = R98.4m**.

**Footnote `[^#]` — Note 9: Cash flow excludes inter-group financing** `[unmapped, physical PDF p. 18]`
- **Text**: *"Excludes inter-group financing from SPAR."*
- **Implication**: The discontinued operations cash flow of net inflows R27.4m from financing activities excludes inter-group financing from SPAR. **For forecasting**: the true cash drain of UK discontinued ops on the group is higher than the R77.3m operating outflow + R2.8m investing outflow – R27.4m financing inflow = R52.7m net outflow, because inter-group financing is not captured. Check note 9 or the UK disposal note for the inter-group funding amount.

**Footnote `(1)` — Note 9: Poland disposal provision** `[unmapped, physical PDF p. 17]`
- **Text**: *"The Group recognised a provision of R46 million within discontinued operations relating to the settlement of matters arising from the disposal and closure of the Poland operations. The provision primarily relates to estimated settlement and dispute resolution costs associated with the exit process."*
- **Implication**: R46.0m one-off Poland exit cost. **For forecasting**: non-recurring. Check whether further Poland costs are expected in H2.

**Note 12 — Contingent liability: Giannacopoulos Group** `[unmapped, physical PDF p. 19]`
- **Text**: *"As was initially reported in the annual financial statements in respect of the year ended 30 September 2022, summons was served on the Company by one of its retailers, the Giannacopoulos Group, for alleged damages of R2.1 billion arising from a membership dispute. The Company denied any liability and has filed a plea to defend the matter. Management have engaged extensively with the retailer and while many issues have been successfully resolved, a few major dispute matters could not be finalised. The parties have agreed that the dispute be dealt with through a legal process. The Company continues to remain satisfied that, based on legal opinion, there is insufficient evidence to substantiate the claim and does not recognise any liability for damages. During the current period, summons was served on the Company by the Giannacopoulos Group in respect of an additional claim for alleged damages of R168 million arising from the implementation of SAP ERP software at the KwaZulu-Natal Distribution Centre. Through the approved SAP compensation process at the time, the Giannacopoulos Group was 'entitled' to R1.55 million. This compensation calculation was agreed to and signed off by the Company and the KZN regional guild and aligned to settlements agreed to with other retailers. The Giannacopoulos Group countered, requesting compensation of R5.1 million at the time. Based on the legal experts' view and the previous settlements with other retailers, a settlement provision of R5.1 million has been recognised in this regard at 27 March 2026."*
- **Implication**: **R2.1bn original claim + R168m new SAP claim = R2.268bn total contingent liability**, not recognised on balance sheet. Only R5.1m provision recognised for the SAP claim. **For forecasting**: this is a material tail risk. If the R2.1bn claim were to crystallise, it would wipe out ~39% of group equity (R5,401.3m). The R5.1m provision is immaterial. Check the FY2026 annual report for any update on the legal process.

**Note 13 — Events after reporting date: UK disposal** `[unmapped, physical PDF p. 20]`
- **Text**: *"On 18 May 2026, the Group announced that it had entered into an asset purchase agreement with A.F. Blakemore & Son for the disposal of the South-West England SPAR licence, 71 owned company stores, associated warehouse and logistics infrastructure and related independent retailer supply agreements. In addition, a further 63 stores are in the process of being disposed of to third-party operators. Completion of the transaction is expected to occur in stages between June and September 2026. Total gross proceeds are estimated of approximately GBP 13.0 million and the net cash outcome is expected to be broadly breakeven after transaction costs. The full financial and reporting effect of the transaction is being assessed by management. These stores are currently included within assets held for sale and discontinued operations."*
- **Implication**: **Critical for H2 forecasting**: UK disposal proceeds ~GBP 13.0m (~R248m at R19.11/GBP) but net cash broadly breakeven after costs. The 71 owned stores + 63 third-party stores = 134 stores being disposed. Completion June–September 2026 means H2 will have partial UK trading. **The full financial effect is NOT yet quantified** — no gain/loss on disposal, no H2 trading loss guidance. This is the single biggest open item for H2 forecasting.

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q53 | High | Debtors / credit note | Trade receivables R15,975.2m `[p. 5]`; provision movement R150.7m `[p. 13]`; prior capture R273m specific impairment and R58m G&L write-offs not visible here | Locate the debtors note: gross debtors, ECL allowance, satisfactory-paid %, collection rate, ageing buckets, write-offs. Reconcile R150.7m P&L movement to R273m specific impairment and R58m write-offs. | Credit book health is the #1 risk to SA profitability; R273m provisions drove SA PBT collapse. |
| Q54 | High | Ireland segment note | Ireland op profit R502.8m `[p. 9]`; D&A R288.1m; implied EBITDA ~R790.9m H1; ~EUR 70m FY claim (Q26) | Reconcile Ireland segment op profit + D&A to ~EUR 70m EBITDA. Confirm pre/post IFRS 16, pre/post exceptionals, BWG-only vs all Ireland. Get explicit ZAR/EUR rate. | Ireland is now the profit engine; mispricing its EBITDA distorts group valuation. |
| Q55 | High | UK disposal / discontinued note | Note 13 `[p. 20]`: GBP 13.0m gross proceeds, net broadly breakeven, completion June–Sept 2026, "full financial effect being assessed" | Get gain/loss on disposal, H2 UK trading loss phasing (~£5m), inter-group financing amount excluded from note 9 cash flow `[p. 18]`, and whether further HFS impairment is expected. | UK disposal is the biggest H2 swing factor; no gain/loss or H2 loss guidance yet. |
| Q56 | High | HEPS / dividend note | HEPS 123.6c `[p. 8]`; no DPS disclosed in this section; prior capture DPS target | Locate DPS declared, payout ratio vs HEPS, and dividend sustainability given R974m operating cash outflow `[p. 7]`. | Cash flow is negative; dividend may be unfunded. |
| Q57 | High | Cash flow / working capital note | Operating cash outflow R974.0m `[p. 7]`; payables outflow R1,841.7m `[p. 13]`; receivables up R61.0m; inventories down R63.0m | Explain the R1,841.7m payables outflow — is it timing, settlement of prior overdues, or structural? Check creditor days vs prior periods. | Working capital absorption is the key cash flow risk; if structural, H2 cash flow stays negative. |
| Q58 | High | Contingent liability / legal note | Note 12 `[p. 19]`: R2.1bn + R168m Giannacopoulos claims; only R5.1m provision | Check FY2026 annual report / subsequent events for legal process update. Any settlement or judgment? | R2.268bn tail risk = 39% of equity; binary risk to forecast. |
| Q59 | Medium | SAP / IT note | GiCom software R30.7m fully impaired `[p. 16]`; Giannacopoulos SAP claim R168m `[p. 19]`; prior capture Finance Go-Live FY2026, DC Integration FY2027 | Get capitalised vs expensed SAP costs H1 2026, FY2026 guidance, and whether other IT projects are at risk of impairment. | IT project risk is crystallising (GiCom write-off); SAP delays could hit H2 opex. |
| Q60 | Medium | Store network note | 8 SA stores acquired (Hajimarkos, R162.0m, R149.8m goodwill, R47.4m impaired within 2 months) `[pp. 13, 16]`; 5 SA stores sold `[p. 15]`; 3 corporate stores ROU impaired `[p. 16]` | Get total store count by segment, net movement H1 2026, corporate store count and losses, closure/transfer plans. | Store network dynamics drive revenue and lease liability forecasts. |
| Q61 | Medium | KZN note | SA PBT collapsed from R602.9m to (R50.9m) `[p. 9]`; prior capture R123m KZN hit, "3 consecutive months of profit" Jan–Mar 2026 | Get rand quantum of KZN H1 hit and Jan–Mar profit; GP% by month; H2 run-rate. | KZN recovery is the key SA profit swing factor. |
| Q62 | Medium | Revenue / trading update | Group revenue +2.6% as adjusted `[pp. 11–12]`; SA +2.3% as adjusted; Ireland +3.5% as adjusted (R16,975.7m vs R16,410.8m) | Get Feb–Mar run-rate, Easter calendar shift impact on H2, and like-for-like growth by segment. | H2 revenue forecast depends on run-rate and calendar effects. |
| Q63 | Medium | Debt / treasury note | Borrowings R6,977.5m + overdrafts R1,430.7m – cash R1,597.2m = net debt R6,811.0m `[p. 5]`; lease liabilities R8,420.2m; no net debt/EBITDA stated | Get net debt/EBITDA ratio, deleveraging target, hedged vs unhedged split, interest rate sensitivity. | Leverage and refinancing risk affect forecast and valuation. |
| Q64 | Medium | Other revenue note | Other revenue R1,109.6m (+51.9%) `[p. 11]`; marketing/services R839.5m (+78.2%), franchise R127.1m (+9.5%), other services R143.0m (flat) | Confirm recurring vs one-off split of marketing/services revenue; GP vs operating income treatment (currently below GP `[p. 4]`). | Other revenue growth is a key profit driver; sustainability matters. |
| Q65 | Medium | Associates / JV note | Share of associates (R4.8m) `[p. 4]`; Ireland associate loss (R6.2m) `[p. 9]`; investment R141.7m `[p. 5]` | Confirm Sri Lanka is equity-accounted, its contribution, and whether it sits in "6 countries". Get associate/JV detail. | Sri Lanka loss is a drag; need to understand if it's in group profit. |
| Q66 | Low | Geographic / foreign ops note | Two reportable segments only (SA, Ireland) `[p. 9]`; no Namibia/Botswana/Swaziland/Mozambique disclosure; "6 countries" vs "SA and Ireland only" tension | Get geographic revenue/profit breakdown within Southern Africa; confirm which entities are consolidated vs licence footprint. | Foreign ops exposure and risk not visible in segment note. |
| Q67 | Low | Market share / loyalty note | Prior capture "Convenience 38% AC Nielsen" (Ireland); loyalty 59.4% foreign ops | Confirm Nielsen date, value vs volume, Republic of Ireland only; locate loyalty chart footnote definitions. | Market share and loyalty metrics inform revenue forecast. |
| Q68 | Low | Dividend / capital allocation note | No DPS in this section; treasury shares acquired R3.9m `[p. 6]`; share-based payments R21.0m `[p. 6]` | Get DPS declared, payout ratio, share buyback activity, and capital allocation priorities. | Capital allocation affects shareholder returns and forecast. |

---

================================================================================
## PART 2 (AFS) - SECTION 2: [unmapped] Corporate information
================================================================================

### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]
--- Section unmapped | [AFS] physical page 21 | area selection | Commentary ---
                                                          
        THE SPAR GROUP LTD                                
        INTERIM FINANCIAL                                 
        RESULTS 2026                                      
    Corporate          information                        
                                                          
                                                          
                                                          
    The SPAR Group Ltd        Auditor                     
    (SPAR or the Group or the Company) PricewaterhouseCoopers Inc.
    Registration number: 1967/001572/06 Waterfall City    
    ISIN: ZAE000058517        4 Lisbon Lane               
    JSE and A2X share code: SPP Jukskei View, Midrand     
    https://thespargroup.com  2090                        
    Directors                 Sponsor                     
    MJ Bosman* (Chairman), SA Zinn* (Deputy Chairperson), One Capital
    MR Isaacs (Group CEO), M Pydigadu (Group CFO), 17 Fricker Road
    EC Botha*, PMP da Silva*, O Ighodaro*, Illovo         
    MJ Jamieson*, LM Koyana*, ST Naran* 2196              
    * Independent non-executive.                          
                              Bankers and corporate brokers
    Group Company Secretary   Rand Merchant Bank, a division of FirstRand Bank Ltd
                              PO Box 4130                 
    M Chetty                                              
                              The Square                  
                              Umhlanga Rocks              
    Registered office         4021                        
    The Umhlanga Arch                                     
    1 Ncondo Place                                        
    Umhlanga Ridge                                        
    Durban                                                
    Transfer secretaries                                  
    JSE Investor Services (Pty) Ltd                       
    PO Box 4844                                           
    Johannesburg                                          
    2000                                                  
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                            #19822                        
                            18

### [ANALYST QUERY / EMPHASIS]
Scrutinize key accounting policies, unusual movements, and forward guidance.

### [SECTION READING RESPONSE / DETERMINATION]
### 1. Answers to Stored Questions for This Section

No stored questions can be tested, answered, or partially answered using the evidence in this section. The captured page (physical PDF p. 21) contains only corporate information (directors, auditor, sponsor, bankers, registered office, transfer secretaries) and no financial data, footnotes, credit metrics, or forward guidance. All stored questions remain open and are carried forward in Section 4.

### 2. Footnote & Qualification Deep-Dive

No footnotes, table notes, or embedded qualifications are present in this section. The only annotation is the asterisk (`*`) against certain director names, which is defined in-line as "* Independent non-executive." — this is a governance designation, not a financial qualification, and has no bearing on revenue, margin, credit, lease, or working-capital drivers. No footnote text is missing from this capture because no financial footnote markers appear.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q58 | Low | Next financial section (e.g., D003/D004) | Corporate information lists PwC as auditor and One Capital as sponsor `[unmapped, p. 21]` — no audit opinion or review conclusion is shown on this page | Confirm whether the interim results carry an independent review conclusion (and whether it is unmodified/emphasis-of-matter) in the auditor's review report section | A modified review conclusion or going-concern emphasis would materially change forecast risk weighting |
| Q59 | Low | Next financial section | No report map supplied; page 21 is corporate information only `[unmapped, p. 21]` | Identify the actual Report Map section IDs and page ranges for the debtors note, cash flow note, and segment note so stored questions Q5/Q14/Q39/Q53/Q57 can be targeted | Ensures high-priority credit and cash-flow questions are routed to the correct sections rather than guessed |

### 5. Baseline Forecast Inputs Captured Here

No financial figures, guidance, or forecast-relevant metrics are present in this section. The only factual items captured are non-financial corporate details:

| Item | Value | Source |
| --- | --- | --- |
| Company | The SPAR Group Ltd | [unmapped, p. 21] |
| Registration number | 1967/001572/06 | [unmapped, p. 21] |
| ISIN | ZAE000058517 | [unmapped, p. 21] |
| JSE / A2X share code | SPP | [unmapped, p. 21] |
| Auditor | PricewaterhouseCoopers Inc. | [unmapped, p. 21] |
| Sponsor | One Capital | [unmapped, p. 21] |
| Group CEO | MR Isaacs | [unmapped, p. 21] |
| Group CFO | M Pydigadu | [unmapped, p. 21] |
| Chairman | MJ Bosman (independent non-executive) | [unmapped, p. 21] |

### 6. Next Section to Capture

Capture the **debtors / credit note section** (the section containing the trade receivables note and ECL/ageing analysis, referenced in stored questions as pp. 30 and 48). This will resolve the highest-priority open items: **Q5, Q14, Q39, Q53** (gross debtors, ECL allowance, satisfactory-paid %, collection rate, ageing, write-offs, and reconciliation of the R150.7m P&L provision movement to the R273m specific impairment and R58m write-offs). If the debtors note is not immediately available, capture the **cash flow statement / notes section** next to resolve **Q57** (R1,841.7m payables outflow).
