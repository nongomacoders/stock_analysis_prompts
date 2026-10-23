"""Script to generate the Stage 2 Institutional Valuation Prompt for Gemini 4 Argon.

Combines the source PDF report with the Stage 1 Forensic Audit Determinations as ground truth,
directing Argon to produce the final 2-year forecast, DCF/multiples valuation, and JSE equity research valuation note (ZAR per share).
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from companies import find_company_dir
from companies.sectors import get_sector_config
from section_capture.db import KNOWN_COMPANIES


def _format_section1_spec(ticker: str, company_title: str, sector_display: str, sector_code: str | None = None) -> list[str]:
    """Generates standardized Section 1 instructions with mandatory JSON block and Markdown table scaffold."""
    sec_code = (sector_code or sector_display).lower()
    return [
        "1. **Executive Investment Thesis & 12-Month JSE Price Target (ZAR/share):**",
        "   - **MANDATORY JSON SUMMARY BLOCK:** You MUST begin Section 1 with the following exact machine-readable JSON block before any prose or visual tables:",
        "     ```json",
        "     {",
        f'       "ticker": "{ticker}",',
        f'       "company_name": "{company_title}",',
        f'       "sector": "{sec_code}",',
        '       "recommendation": "BUY | HOLD | SELL",',
        '       "reference_price_zar": 0.00,',
        '       "target_price_zar": 0.00,',
        '       "implied_upside_pct": 0.0,',
        '       "forward_dividend_yield_pct": 0.0,',
        '       "projected_12m_tsr_pct": 0.0',
        "     }",
        "     ```",
        "   - **Executive Valuation Summary Card Table:** Follow the JSON block immediately with your publication-grade Markdown table:",
        "     | Metric | Determination | Basis & Key Commentary |",
        "     | :--- | :---: | :--- |",
        f"     | **Sector** | {sector_display} | [Sub-sector classification] |",
        "     | **Current Reference Share Price** | R[0.00] | [Closing date & reference price baseline] |",
        "     | **12-Month JSE Target Price** | R[0.00] | [Target price & primary valuation methodology] |",
        "     | **Implied Capital Upside / (Downside)** | [+/-0.0]% | [Relative to reference price] |",
        "     | **Forward Dividend Yield (FY27E)** | [0.0]% | [Distribution policy & payout ratio] |",
        "     | **Projected 12-Month TSR** | [+/-0.0]% | [Capital return + forward dividend yield] |",
        "     | **Institutional Recommendation** | [BUY | HOLD | SELL] | [Primary investment thesis] |",
        "   - Followed by the core institutional thesis and structural headwinds/tailwinds.",
    ]


def _format_critical_formatting_constraints() -> list[str]:
    """Generates the strict negative formatting rules placed at the very end of the prompt."""
    return [
        "---",
        "",
        "## CRITICAL OUTPUT FORMATTING CONSTRAINTS (STRICTLY ENFORCED)",
        "",
        "To ensure institutional publication quality and 100% deterministic parsing, you MUST follow these formatting rules:",
        "1. **Mandatory JSON Block First:** Section 1 MUST open with the exact ```json ... ``` summary block containing native float numbers (e.g. `0.42`, `-30.0`), not text descriptions.",
        "2. **Zero HTML Tags:** DO NOT use any HTML tags (`<br>`, `<br/>`, `<span>`, `<div>`, etc.). Use standard Markdown newlines.",
        "3. **Single-Line Table Rows:** Every Markdown table row MUST be on a single continuous line starting and ending with `|`. DO NOT insert blank lines (`\\n\\n`) within table rows or split cells across multiple lines.",
        "4. **Isolated Numeric Determination Cells:** In the Valuation Summary Card, keep the Determination column strictly limited to the metric value (e.g. `R0.42` or `-30.0%`). Reserve all commentary and secondary notes strictly for the Commentary column.",
        "5. **No Special Symbols or Arbitrary Code Blocks:** DO NOT wrap ordinary numbers or percentages in backticks (`). Reserve backticks solely for the initial JSON block and formal code/file identifiers.",
        "",
    ]


def build_stage2_prompt_content(
    stage1_content: str,
    company_title: str,
    ticker: str,
    detected_sector: str,
    sens_announcements: list[str] | None = None,
) -> str:
    """Constructs the Stage 2 Markdown prompt text incorporating Stage 1 determinations as 99% confidence prior."""
    md_lines: list[str] = []
    md_lines.append("# STAGE 2: INSTITUTIONAL 2-YEAR VALUATION & FORECAST PROMPT")
    md_lines.append(f"**Target Asset:** {company_title} ({ticker})  ")
    md_lines.append(f"**Sector:** {detected_sector.capitalize()}  ")
    if sens_announcements:
        sens_str = "; ".join(sens_announcements)
        md_lines.append(f"**Input Mode:** Full Company Results PDF + Subsequent SENS Notices ({sens_str}) + Audited Stage 1 Determinations  ")
    else:
        md_lines.append(f"**Input Mode:** Full Company Results PDF (Attached) + Audited Stage 1 Forensic Determinations (Below)  ")
    md_lines.append(f"**Target Deliverable:** 2-Year Forecast Model, Valuation Bridge, and JSE Equity Research Note (ZAR per Share)")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("### INSTRUCTIONS FOR GEMINI 4 ARGON:")

    if detected_sector == "retail":
        md_lines.append(
            "You are acting as an elite **Managing Director & Head of Retail & Consumer Equity Research** at a premier institutional investment bank."
        )
        md_lines.append(
            f"You are conducting a definitive 2-year operational and valuation forecast for **{company_title} ({ticker})**."
        )
        md_lines.append("")
        md_lines.append("### CORE OPERATING RULES & EVIDENCE HIERARCHY:")
        md_lines.append(
            "1. **High-Confidence Baseline Truth (99% Confidence Prior):** Treat the Stage 1 Forensic Determinations provided below "
            "as your 99% confidence baseline (e.g. merchandise vs credit revenue split, gross margin bridges, "
            "debtor costs & IFRS 9 ECL provisioning, store count expansion, and IFRS 16 lease liabilities). Do not revert to "
            "high-level PR narratives from the PDF. If you identify definitive evidence in the primary PDF financial notes "
            "that contradicts or refines a Stage 1 determination, you may depart from it ONLY by explicitly declaring the disagreement, "
            "citing the exact note/table and page from the PDF, and providing your quantitative justification."
        )
        md_lines.append(
            "2. **Primary Reporting & Trading Currency:** South African retail equities trade primarily on the **Johannesburg Stock Exchange (JSE)**. "
            "All final valuation targets, earnings per share, and dividends per share must be presented in **ZAR (Rands per share or ZAR cents)**."
        )
        md_lines.append(
            "3. **Retail Operating Model:** Model explicit operational drivers across:\n"
            "   - Merchandise sales growth by chain/brand and region.\n"
            "   - Customer financial services revenue (finance charges, service fees, insurance profit).\n"
            "   - Credit participation rate and debtors book impairment provision coverage.\n"
            "   - Store network roll-out (net openings, refurbishments, trading space in m², and trading density).\n"
            "   - IFRS 16 lease costs vs physical store capex."
        )
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## AUDITED STAGE 1 FORENSIC DETERMINATIONS (GROUND TRUTH)")
        md_lines.append("")
        md_lines.append(stage1_content)
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## REQUIRED SECTIONS OF THE INSTITUTIONAL VALUATION NOTE")
        md_lines.append("")
        md_lines.extend(_format_section1_spec(ticker, company_title, "Retail", "retail"))
        md_lines.append("2. **Detailed Operational Forecast (FY27E & FY28E):** Merchandise sales, credit vs cash mix, gross margin %, debtor cost %, store count, trading space m², and trading density.")
        md_lines.append("3. **Consolidated Financial Statements & Cash Flow Bridge:** Revenue, Gross Profit, Operating Expenses, Operating Profit, PAT, HEPS, and Free Cash Flow to Equity (FCFE).")
        md_lines.append("4. **Valuation Multiples & DCF Table:** Forward P/E, EV/EBITDA, dividend yield, and per-share equity value in ZAR.")
        md_lines.append("5. **Sensitivity Matrix:** 2D sensitivity table (Sales Growth vs Debtor Cost % or P/E Multiple).")
        md_lines.append("6. **Actionable Portfolio Monitoring Triggers & Catalysts ('What to Watch For That Will Move the Stock'):**")
        md_lines.append("   - **Operational & Financial Red Lines:** Explicitly list 3-5 specific triggers or warning thresholds (e.g. collection rate dipping below bonus hurdle, margin floors, working capital burn) that would break the thesis and trigger a de-rating.")
        md_lines.append("   - **Quantified Sensitivity Impacts:** Exact quantified rule of thumb for each catalyst (e.g. 'Every 75 bps swing in gross margin alters HEPS by X cents and fair value by R Y/share').")
        md_lines.append("   - **Re-Rating Catalysts:** Specific milestones required to trigger an upgrade (e.g. Speciality margin inflecting positive, credit book seasoning).")
        md_lines.append("   - **Upcoming Milestones & Reporting Dates:** Key calendar dates (e.g. Interim results date, AGM, trading updates) for portfolio managers to mark.")
        md_lines.append("")
    elif detected_sector == "reit":
        md_lines.append(
            "You are acting as an elite **Managing Director & Head of Listed Property & REIT Equity Research** at a premier institutional investment bank."
        )
        md_lines.append(
            f"You are conducting a definitive 2-year operational and valuation forecast for **{company_title} ({ticker})**."
        )
        md_lines.append("")
        md_lines.append("### CORE OPERATING RULES & EVIDENCE HIERARCHY:")
        md_lines.append(
            "1. **High-Confidence Baseline Truth (99% Confidence Prior):** Treat the Stage 1 Forensic Determinations provided below "
            "as your 99% confidence baseline (e.g. SA REIT distributable income adjustments, like-for-like NPI growth, "
            "GLA vacancies, WALE, nominal vs look-through LTV, cost of debt, interest rate hedging ratio, and cap rates). Do not revert to "
            "high-level PR narratives from the PDF. If you identify definitive evidence in the primary PDF financial notes "
            "that contradicts or refines a Stage 1 determination, you may depart from it ONLY by explicitly declaring the disagreement, "
            "citing the exact note/table and page from the PDF, and providing your quantitative justification."
        )
        md_lines.append(
            "2. **Primary Reporting & Trading Currency:** South African REITs trade primarily on the **Johannesburg Stock Exchange (JSE)**. "
            "All final valuation targets, Net Asset Value (NAV) per share, Distributable Income per share (DIPS), and Dividends per share (DPS) must be presented in **ZAR (Rands per share or ZAR cents)**."
        )
        md_lines.append(
            "3. **REIT Operating & Valuation Model:** Model explicit property drivers across:\n"
            "   - Contractual rental escalations vs renewal reversions across retail, logistics/industrial, and office portfolios.\n"
            "   - Like-for-like Net Property Income (NPI) growth and municipal recovery ratios.\n"
            "   - Balance sheet LTV, debt maturity profile, and interest rate hedging ratio.\n"
            "   - Distributable income bridge (SA REIT BPR) and dividend payout ratio (75%–100%).\n"
            "   - Sum-of-the-parts (SOTP) property capitalization (exit cap rates) and Net Asset Value (NAV) per share."
        )
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## AUDITED STAGE 1 FORENSIC DETERMINATIONS (GROUND TRUTH)")
        md_lines.append("")
        md_lines.append(stage1_content)
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## REQUIRED SECTIONS OF THE INSTITUTIONAL VALUATION NOTE")
        md_lines.append("")
        md_lines.extend(_format_section1_spec(ticker, company_title, "REIT / Listed Property", "reit"))
        md_lines.append("2. **Detailed Property Operating Forecast (FY27E & FY28E):** Like-for-like NPI growth, vacancy rates by sector, contractual escalations, renewal reversions, and WALE.")
        md_lines.append("3. **Distributable Income (DIPS) & Balance Sheet Bridge:** Reconciliation of IFRS profit to SA REIT distributable earnings, debt schedule, average cost of debt, interest rate hedging %, and LTV trajectory.")
        md_lines.append("4. **SOTP NAV Valuation & Yield Benchmarks:** Net Asset Value (NAV) per share by sub-sector (Retail, Logistics, Office), capitalization rates, target forward distribution yield, and implied target price in ZAR.")
        md_lines.append("5. **Sensitivity Matrix:** 2D sensitivity table (Capitalization Rate x Cost of Debt or Vacancy Rate vs DIPS / Target Price).")
        md_lines.append("6. **Actionable Portfolio Monitoring Triggers & Catalysts ('What to Watch For That Will Move the Stock'):**")
        md_lines.append("   - **Operational & Balance Sheet Red Lines:** Explicitly list 3-5 specific triggers (e.g. LTV breaching 42%, tenant retention dropping below 75%, office vacancy spike, ICR dipping below 2.5x).")
        md_lines.append("   - **Quantified Sensitivity Impacts:** Exact quantified rule of thumb (e.g. 'Every 25 bps movement in weighted average cap rate shifts NAV by R X.XX/share; every 50 bps rise in cost of debt impacts DIPS by Y%').")
        md_lines.append("   - **Re-Rating Catalysts:** Specific milestones required to trigger an upgrade (e.g. successful non-core asset disposals, de-gearing milestones, accretive development completions).")
        md_lines.append("   - **Upcoming Milestones & Reporting Dates:** Key calendar dates (e.g. distribution declaration dates, lease expiry cliff dates) for portfolio managers to mark.")
        md_lines.append("")
    elif detected_sector == "it":
        md_lines.append(
            "You are acting as an elite **Managing Director & Head of Technology & IT Services Equity Research** at a premier institutional investment bank."
        )
        md_lines.append(
            f"You are conducting a definitive 2-year operational and valuation forecast for **{company_title} ({ticker})**."
        )
        md_lines.append("")
        md_lines.append("### CORE OPERATING RULES & EVIDENCE HIERARCHY:")
        md_lines.append(
            "1. **High-Confidence Baseline Truth (99% Confidence Prior):** Treat the Stage 1 Forensic Determinations provided below "
            "as your 99% confidence baseline (e.g. recurring revenue / ARR mix, gross margin by line of business, "
            "technical headcount & billable consultant utilization rates, contract asset / WIP recovery, deferred revenue recognition, "
            "and debt/restructuring covenants). Do not revert to high-level PR narratives from the PDF. If you identify definitive evidence "
            "in the primary PDF financial notes that contradicts or refines a Stage 1 determination, you may depart from it ONLY by explicitly declaring the disagreement, "
            "citing the exact note/table and page from the PDF, and providing your quantitative justification."
        )
        md_lines.append(
            "2. **Primary Reporting & Trading Currency:** South African technology equities trade primarily on the **Johannesburg Stock Exchange (JSE)**. "
            "All final valuation targets, headline earnings per share (HEPS), and free cash flow per share must be presented in **ZAR (Rands per share or ZAR cents)**."
        )
        md_lines.append(
            "3. **Technology & IT Services Operating & Valuation Model:** Model explicit operational drivers across:\n"
            "   - Line-of-business revenue mix: Managed services & cloud infrastructure, digital solutions & custom software, systems integration, and third-party software/hardware resale.\n"
            "   - Recurring revenue proportion (Annual Recurring Revenue - ARR / Monthly Recurring Revenue - MRR %).\n"
            "   - Technical headcount capacity, billing rates, and consultant/developer utilization rates.\n"
            "   - Working capital efficiency: Contract assets (unbilled WIP), contract liabilities (deferred revenue), and DSO.\n"
            "   - Deleveraging, debt service obligations, legacy liability settlements, and Normalized Free Cash Flow to Equity (FCFE)."
        )
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## AUDITED STAGE 1 FORENSIC DETERMINATIONS (GROUND TRUTH)")
        md_lines.append("")
        md_lines.append(stage1_content)
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## REQUIRED SECTIONS OF THE INSTITUTIONAL VALUATION NOTE")
        md_lines.append("")
        md_lines.extend(_format_section1_spec(ticker, company_title, "Technology / IT Services", "it"))
        md_lines.append("2. **Detailed Operational & Segmental Forecast (FY27E & FY28E):** Segmental revenue by cluster (Digital, Infrastructure, OT, Resale), recurring ARR %, gross margin % by service line, utilization %, and EBITDA.")
        md_lines.append("3. **Consolidated Financial Statements & FCFE Bridge:** Revenue, Gross Profit, Operating Expenses, Normalized EBITDA, Amortization of Intangibles/IP, Net Finance Charges, Tax, HEPS, and Free Cash Flow to Equity.")
        md_lines.append("4. **Valuation Multiples & SOTP / DCF Table:** EV/EBITDA, EV/Sales, Forward P/E, FCF yield, and per-share equity value in ZAR.")
        md_lines.append("5. **Sensitivity Matrix:** 2D sensitivity table (EBITDA Margin vs Recurring Revenue % or Exit P/E Multiple).")
        md_lines.append("6. **Actionable Portfolio Monitoring Triggers & Catalysts ('What to Watch For That Will Move the Stock'):**")
        md_lines.append("   - **Operational & Balance Sheet Red Lines:** Explicitly list 3-5 specific triggers (e.g. key enterprise contract churn, bench utilization dipping below 70%, project margin slippage, contract asset write-downs).")
        md_lines.append("   - **Quantified Sensitivity Impacts:** Exact quantified rule of thumb (e.g. 'Every 100 bps expansion in EBITDA margin shifts HEPS by X cents and fair value by R Y/share').")
        md_lines.append("   - **Re-Rating Catalysts:** Specific milestones required to trigger an upgrade (e.g. multi-year public/private enterprise contract wins, legacy debt retirement, dividend resumption).")
        md_lines.append("   - **Upcoming Milestones & Reporting Dates:** Key calendar dates (e.g. interim/annual results dates, AGM, trading updates) for portfolio managers to mark.")
        md_lines.append("")
    elif detected_sector == "construction":
        md_lines.append(
            "You are acting as an elite **Managing Director & Head of Construction & Materials Equity Research** at a premier institutional investment bank."
        )
        md_lines.append(
            f"You are conducting a definitive 2-year operational and valuation forecast for **{company_title} ({ticker})**."
        )
        md_lines.append("")
        md_lines.append("### CORE OPERATING RULES & EVIDENCE HIERARCHY:")
        md_lines.append(
            "1. **High-Confidence Baseline Truth (99% Confidence Prior):** Treat the Stage 1 Forensic Determinations provided below "
            "as your 99% confidence baseline (e.g. residential development pipeline units, serviced stands, memorial park plot margins, "
            "infrastructure contracting order book, percentage of completion (POC) revenue recognition, contract assets / WIP, "
            "and debt/liquidity covenants). Do not revert to high-level PR narratives from the PDF. If you identify definitive evidence "
            "in the primary PDF financial notes that contradicts or refines a Stage 1 determination, you may depart from it ONLY by explicitly declaring the disagreement, "
            "citing the exact note/table and page from the PDF, and providing your quantitative justification."
        )
        md_lines.append(
            "2. **Primary Reporting & Trading Currency:** South African construction and materials equities trade primarily on the **Johannesburg Stock Exchange (JSE)**. "
            "All final valuation targets, headline earnings per share (HEPS), and Net Asset Value (NAV) per share must be presented in **ZAR (Rands per share or ZAR cents)**."
        )
        md_lines.append(
            "3. **Construction & Property Development Operating & Valuation Model:** Model explicit operational drivers across:\n"
            "   - Residential property development pipeline: Serviced stand roll-out, integrated housing construction volume, and gross profit margin by development project.\n"
            "   - Memorial parks: Burial plot sales volume, cash collections, and cemetery maintenance fund contributions.\n"
            "   - Infrastructure contracting: Order book execution, public vs private sector procurement, and POC margin recognition.\n"
            "   - Working capital efficiency: Contract assets, retentions, inventory land bank valuation, and trade payables.\n"
            "   - Capital structure & liquidity: Bank term facilities, DMTN corporate bonds, interest cover, and Free Cash Flow to Equity (FCFE)."
        )
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## AUDITED STAGE 1 FORENSIC DETERMINATIONS (GROUND TRUTH)")
        md_lines.append("")
        md_lines.append(stage1_content)
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## REQUIRED SECTIONS OF THE INSTITUTIONAL VALUATION NOTE")
        md_lines.append("")
        md_lines.extend(_format_section1_spec(ticker, company_title, "Construction & Materials", "construction"))
        md_lines.append("2. **Detailed Development & Operational Forecast (FY27E & FY28E):** Residential unit deliveries, serviced stand sales, memorial park cash collections, order book depletion, and gross margin by segment.")
        md_lines.append("3. **Consolidated Financial Statements & FCFE Bridge:** Revenue, Gross Profit, Operating Expenses, Statutory/Adjusted EBITDA, Net Finance Charges, Tax, HEPS, and Free Cash Flow to Equity.")
        md_lines.append("4. **Sum-of-the-Parts (SOTP) / DCF Valuation Table:** Project-by-project residential pipeline NAV, memorial parks capitalization, contracting multiple, net debt, and per-share equity value in ZAR.")
        md_lines.append("5. **Forward Valuation Multiples & Sensitivity Matrix:** Target P/E, EV/EBITDA, Price/NAV, and 2D sensitivity table (Sales Velocity vs Construction Cost Inflation or Exit Multiple).")
        md_lines.append("6. **Actionable Portfolio Monitoring Triggers & Catalysts ('What to Watch For That Will Move the Stock'):**")
        md_lines.append("   - **Operational & Balance Sheet Red Lines:** Explicitly list 3-5 specific triggers (e.g. municipal bulk infrastructure handover delays, slow residential unit off-take, contract asset write-downs, liquidity/DMTN covenants).")
        md_lines.append("   - **Quantified Sensitivity Impacts:** Exact quantified rule of thumb (e.g. 'Every 100 bps shift in gross margin impacts HEPS by X cents and fair value by R Y/share').")
        md_lines.append("   - **Re-Rating Catalysts:** Specific milestones required to trigger an upgrade (e.g. major infrastructure project award, acceleration of retail land parcel sales, debt de-gearing milestones, dividend resumption).")
        md_lines.append("   - **Upcoming Milestones & Reporting Dates:** Key calendar dates (e.g. interim/annual results dates, bond coupon dates, AGM) for portfolio managers to mark.")
        md_lines.append("")
    else:
        cfg = get_sector_config(detected_sector)
        md_lines.append(
            f"You are acting as an elite **{cfg.stage2_persona}** at a premier institutional investment bank."
        )
        md_lines.append(
            f"You are conducting a definitive 2-year operational and valuation forecast for **{company_title} ({ticker})**."
        )
        md_lines.append("")
        md_lines.append("### CORE OPERATING RULES & EVIDENCE HIERARCHY:")
        md_lines.append(
            "1. **High-Confidence Baseline Truth (99% Confidence Prior):** Treat the Stage 1 Forensic Determinations provided below "
            "as your 99% confidence baseline (e.g. share count anchors, net cash reconciliation, EBITDA adjustments, "
            "organic unit costs, and Section 36 cash tax step-up curve). Do not revert to high-level headline narratives from the PDF. "
            "If you identify definitive evidence in the primary PDF financial notes that contradicts or refines a Stage 1 determination, "
            "you may depart from it ONLY by explicitly declaring the disagreement, citing the exact note/table and page from the PDF, "
            "and providing your quantitative justification."
        )
        md_lines.append(
            "2. **Primary Reporting & Trading Currency:** Pan African / South African miners trade primarily on the **Johannesburg Stock Exchange (JSE)**. "
            "All final valuation targets, earnings per share, and dividends per share must be presented in **ZAR (Rands per share or ZAR cents)**, "
            "accompanied by USD conversions where relevant."
        )
        md_lines.append(
            "3. **Dual Capex Trajectory Modeling:** "
            "Explicitly model and contrast two operational trajectories:\n"
            "   - **Scenario A (Expedited Growth):** Follows management's forward capital wish-list.\n"
            "   - **Scenario B (Committed Capex Cliff):** Models technical sustaining and committed brownfield development only, releasing substantial Free Cash Flow to Equity (FCFE)."
        )
        md_lines.append(
            "4. **Tax Mechanics:** Apply the statutory South African Gold Mining Formula ($Y = 33 - 165/X$) or statutory corporate rate, "
            "reflecting 100% upfront Section 36 capital expenditure deductions."
        )
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## AUDITED STAGE 1 FORENSIC DETERMINATIONS (GROUND TRUTH)")
        md_lines.append("")
        md_lines.append(stage1_content)
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## REQUIRED SECTIONS OF THE INSTITUTIONAL VALUATION NOTE")
        md_lines.append("")
        cfg = get_sector_config(detected_sector)
        md_lines.extend(_format_section1_spec(ticker, company_title, cfg.display_name, cfg.code))
        md_lines.append("2. **Detailed Asset-by-Asset Operational Forecast (FY27E & FY28E):** Throughput, recovered grade, production (oz), cash costs, and AISC per asset.")
        md_lines.append("3. **Consolidated Financial Statements & FCFE Bridge:** Revenue, EBITDA, Section 36 Cash Tax, Net Profit, and Free Cash Flow to Equity.")
        md_lines.append("4. **Sum-of-the-Parts (SOTP) DCF Valuation Table:** Asset-by-asset NAV, unallocated corporate costs, net cash/debt, and per-share equity value in ZAR.")
        md_lines.append("5. **Forward Valuation Multiples & Sensitivity Matrix:** Target P/E, EV/EBITDA, FCF yield, and 2D sensitivity table (Gold Price vs USD/ZAR).")
        md_lines.append("6. **Actionable Portfolio Monitoring Triggers & Catalysts ('What to Watch For That Will Move the Stock'):**")
        md_lines.append("   - **Operational & Production Red Lines:** Explicitly list 3-5 specific triggers (e.g. AISC cost breaches, underground grade dilution, water/power disruptions) that would lower the target price.")
        md_lines.append("   - **Quantified Sensitivity Impacts:** Exact quantified rule of thumb for each catalyst (e.g. 'Every $50/oz move in gold price or R0.50 move in USD/ZAR impacts FCFE by R X million and fair value by R Y/share').")
        md_lines.append("   - **Expansion & Delivery Catalysts:** Specific milestones required to trigger an upgrade (e.g. MTR / Soweto tailings commercial commissioning, Section 36 capex cliff release).")
        md_lines.append("   - **Upcoming Milestones & Reporting Dates:** Key calendar dates (e.g. Interim results date, production reports, SENS announcements) for portfolio managers to mark.")
        md_lines.append("")

    md_lines.extend(_format_critical_formatting_constraints())
    return "\n".join(md_lines)


def generate_stage2_prompt(
    ticker: str,
    company_name: str | None = None,
    sector: str | None = None,
    period: str | None = None,
    stage1_response_path: Path | None = None,
    output_path: Path | None = None,
) -> Path:
    ticker = ticker.upper().strip()
    period_tag = (period or "FY26").upper()

    # Resolve company directory and sector
    found = find_company_dir(ticker, sector=sector)
    if found:
        detected_sector, company_dir = found
    else:
        detected_sector = (sector or "mining").lower()
        company_dir = PROJECT_ROOT / f"companies/{detected_sector}/{ticker}"

    default_title = (f"{ticker} Properties" if detected_sector == "reit" else (f"{ticker} Technologies" if detected_sector == "it" else (f"{ticker} Construction" if detected_sector == "construction" else (f"{ticker} Group" if detected_sector == "retail" else f"{ticker} Resources"))))
    company_title = company_name or KNOWN_COMPANIES.get(ticker, (default_title, detected_sector))[0]
    briefs_dir = company_dir / f"briefs/{period_tag}"
    root_briefs_dir = company_dir / "briefs"

    if stage1_response_path is None:
        candidates = [
            briefs_dir / f"{ticker}_{period_tag}_stage1_audit_response.md",
            briefs_dir / f"{ticker}_stage1_audit_response.md",
            root_briefs_dir / f"{ticker}_stage1_audit_response.md",
            root_briefs_dir / "stage1_audit_response.md",
        ]
        for cand in candidates:
            if cand.exists():
                stage1_response_path = cand
                break

    if stage1_response_path and stage1_response_path.exists():
        stage1_content = stage1_response_path.read_text(encoding="utf-8").strip()
    else:
        stage1_content = (
            "[PASTE STAGE 1 AUDIT DETERMINATIONS HERE — E.G. RECONCILED DILUTED SHARE COUNT, "
            "NET CASH POSITION, SBP EBITDA ADJUSTMENTS, ORGANIC UNIT COSTS / GROSS MARGIN, CAPEX SCENARIOS, AND TAX MECHANICS]"
        )

    content = build_stage2_prompt_content(
        stage1_content=stage1_content,
        company_title=company_title,
        ticker=ticker,
        detected_sector=detected_sector,
    )

    if output_path is None:
        briefs_dir.mkdir(parents=True, exist_ok=True)
        output_path = briefs_dir / f"{ticker}_{period_tag}_stage2_valuation_prompt.md"

    output_path.write_text(content, encoding="utf-8")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate Stage 2 Institutional Valuation Prompt for Gemini 4 Argon.")
    parser.add_argument("ticker", help="Company ticker (e.g. PAN, HAR, LEW, TRU)")
    parser.add_argument("--sector", help="Company sector (mining, retail, finance, telcos)", default=None)
    parser.add_argument("--name", help="Full company name", default=None)
    parser.add_argument("--period", help="Financial period (e.g. FY26, FY27)", default="FY26")
    parser.add_argument("--stage1", help="Path to Stage 1 audit response markdown file", default=None)
    parser.add_argument("--output", help="Custom output path", default=None)

    args = parser.parse_args()
    out = generate_stage2_prompt(
        ticker=args.ticker.upper(),
        company_name=args.name,
        sector=args.sector,
        period=args.period.upper() if args.period else None,
        stage1_response_path=Path(args.stage1) if args.stage1 else None,
        output_path=Path(args.output) if args.output else None,
    )
    print(f"Successfully generated Stage 2 Valuation Prompt at: {out}")


if __name__ == "__main__":
    main()
