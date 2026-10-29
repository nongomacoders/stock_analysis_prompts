"""Script to generate the Stage 2 Institutional Valuation Prompt for Institutional Valuation (LLM).

Combines the source PDF report with reviewable Stage 1 working determinations,
directing the LLM to produce the final 2-year forecast, DCF/multiples valuation, and JSE equity research valuation note (ZAR per share).
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import warnings

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from section_capture.valuation_policy import enforce_valuation_publication, valuation_gate_prompt

from companies import find_company_dir
from companies.sectors import (
    get_icb_code,
    get_jse_sector_code,
    get_jse_sector_name,
    get_sector_config,
)
from section_capture.db import (
    DOC_TYPES,
    KNOWN_COMPANIES,
    format_sector_guardrails_block,
    validate_and_repair_rating_bands,
)


def format_documents_considered_table(
    source_documents: list[dict] | None = None,
    include_placeholder_roles: bool = False,
) -> list[str]:
    """Formats the Markdown table listing all source documents and SENS disclosures considered."""
    lines = [
        "### Source Documents & Disclosures Considered",
        "| # | Document Filename | Document Type | Pages | Period / Date | Primary Analytical Role & Key Evidence Considered |",
        "| :---: | :--- | :---: | :---: | :---: | :--- |",
    ]
    if source_documents:
        for idx, doc in enumerate(source_documents, 1):
            fname = doc.get("filename", f"Document_{idx}.pdf")
            dt_key = (doc.get("doc_type") or ("sens" if doc.get("is_sens") else "annual_report")).lower()
            dt_info = DOC_TYPES.get(dt_key, {"badge": doc.get("badge", "[DOC]"), "label": dt_key.upper()})
            type_str = f"{dt_info['badge']} {dt_info['label']}"
            pages = doc.get("page_count")
            pages_str = str(pages) if pages else "—"
            period_or_date = doc.get("announcement_date") or doc.get("period") or "—"
            role = doc.get("role")
            if not role:
                if include_placeholder_roles:
                    if doc.get("is_sens") or dt_key == "sens":
                        role = "[Summarize post-balance-sheet / trading update evidence incorporated]"
                    elif dt_key == "presentation":
                        role = "[Summarize operational KPIs, segment slides & management guidance]"
                    elif dt_key == "afs":
                        role = "[Summarize audited/reviewed primary statements, notes & cash flow]"
                    else:
                        role = "[Summarize primary financial & operational disclosures]"
                else:
                    if doc.get("is_sens") or dt_key == "sens":
                        role = "Subsequent SENS continuous disclosure & post-balance-sheet event update"
                    elif dt_key == "presentation":
                        role = "Results presentation deck, segmental KPIs & management outlook"
                    elif dt_key == "afs":
                        role = "Primary financial statements, accounting notes & cash flow reconciliation"
                    else:
                        role = "Integrated / annual report financial and operational disclosures"
            lines.append(f"| {idx} | `{fname}` | {type_str} | {pages_str} | {period_or_date} | {role} |")
    else:
        lines.append(
            "| 1 | `[Report Filename.pdf]` | `[IAR / AFS / PRES]` | [Pages] | [Period] | [Summarize primary financial & operational evidence extracted] |"
        )
    return lines


def ensure_documents_considered_table(
    note_markdown: str,
    source_documents: list[dict] | None = None,
) -> str:
    """Ensures the 'Source Documents & Disclosures Considered' table appears at the beginning of the Valuation Note
    (immediately following the opening JSON summary block).
    """
    if not note_markdown or not source_documents:
        return note_markdown

    # Check if the LLM already included the Source Documents table
    lower_head = note_markdown[:3500].lower()
    if "documents & disclosures considered" in lower_head or "documents considered" in lower_head or "| document filename |" in lower_head:
        return note_markdown

    table_block = "\n".join(format_documents_considered_table(source_documents, include_placeholder_roles=False))

    import re
    json_match = re.search(r"```json\s*\{.*?\}\s*```", note_markdown, flags=re.DOTALL)
    if json_match:
        insert_pos = json_match.end()
        return (
            note_markdown[:insert_pos]
            + "\n\n"
            + table_block
            + "\n\n"
            + note_markdown[insert_pos:].lstrip()
        )

    return table_block + "\n\n" + note_markdown.lstrip()


def sanitize_stage2_valuation_markdown(
    note_markdown: str,
    target_price_hint: float | None = None,
    reference_price_hint: float | None = None,
) -> str:
    """Validates the opening JSON block in a Stage 2 / Stage 2-U valuation note and repairs degenerate rating_bands."""
    if not note_markdown:
        return note_markdown
    note_markdown = enforce_valuation_publication(note_markdown)
    import json
    import re

    m = re.search(r"(```(?:json)?\s*)(\{[\s\S]*?\})(\s*```)", note_markdown, flags=re.IGNORECASE)
    if not m:
        return note_markdown
    try:
        data = json.loads(m.group(2))
        if not isinstance(data, dict):
            return note_markdown
        tp = data.get("target_price_zar", data.get("target_price", target_price_hint))
        ref = data.get("reference_price_zar", data.get("reference_price", reference_price_hint))
        if ref is None and reference_price_hint and reference_price_hint > 0:
            data["reference_price_zar"] = round(float(reference_price_hint), 2)
            ref = data["reference_price_zar"]
        if data.get('valuation_status') == 'WITHHELD':
            return note_markdown
        repaired = validate_and_repair_rating_bands(data.get("rating_bands"), tp, ref)
        if repaired and data.get("rating_bands") != repaired:
            data["rating_bands"] = repaired
            new_json = json.dumps(data, indent=2, ensure_ascii=False)
            return note_markdown[: m.start(2)] + new_json + note_markdown[m.end(2) :]
    except Exception:
        pass
    return note_markdown


def _format_section1_spec(
    ticker: str,
    company_title: str,
    sector_display: str,
    sector_code: str | None = None,
    reference_price_zar: float | None = None,
    source_documents: list[dict] | None = None,
) -> list[str]:
    """Generates standardized Section 1 instructions with mandatory JSON block, Documents Considered table, and Valuation Summary Card."""
    sec_code = (sector_code or sector_display).lower()
    jse_code = get_jse_sector_code(sec_code, ticker=ticker)
    icb_code = get_icb_code(sec_code, ticker=ticker)
    jse_name = get_jse_sector_name(sec_code, ticker=ticker)
    table_sec = f"{sector_display} ({jse_name} — {jse_code} / ICB {icb_code})" if jse_code and icb_code else sector_display

    ref_str = f"{reference_price_zar:.2f}" if reference_price_zar and reference_price_zar > 0 else "0.00"
    table_ref_val = f"R{reference_price_zar:.2f}" if reference_price_zar and reference_price_zar > 0 else "R[0.00]"
    table_ref_comment = (
        f"Verified closing share price ({ticker}.JO via Yahoo Finance / confirmed input)"
        if reference_price_zar and reference_price_zar > 0
        else "[Closing date & reference price baseline]"
    )

    lines = [
        "1. **Research Summary & Conditional Valuation (Target Only When READY):**",
        "   - **MANDATORY JSON SUMMARY BLOCK:** You MUST begin Section 1 with the following exact machine-readable JSON block before any prose or visual tables:",
        "     ```json",
        "     {",
        f'       "ticker": "{ticker}",',
        f'       "company_name": "{company_title}",',
        f'       "sector": "{sec_code}",',
        f'       "jse_sector_code": "{jse_code}",',
        f'       "jse_sector_name": "{jse_name}",',
        '       "recommendation": null,',
        f'       "reference_price_zar": {ref_str},',
        '       "target_price_zar": null,',
        '       "implied_upside_pct": null,',
        '       "forward_dividend_yield_pct": null,',
        '       "projected_12m_tsr_pct": null,',
        '       "valuation_status": "WITHHELD",',
        '       "blocking_issues": [],',
        '       "valuation_checks": [],',
        '       "rating_bands": null',
        "     }",
        "     ```",
    ]
    if reference_price_zar and reference_price_zar > 0:
        lines.append(
            f"   - **Confirmed JSE Market Closing Price (MANDATORY ANCHOR — DO NOT GUESS):** The supplied reference price for {ticker} is **R{reference_price_zar:.2f}**. You MUST use `{ref_str}` as the exact `reference_price_zar` in the opening JSON summary block and Markdown summary table. DO NOT guess, hallucinate, or alter this reference price. Only when READY, calculate implied capital upside/downside percentages (`implied_upside_pct`), institutional recommendation (`BUY | HOLD | SELL`), and dynamic rating bands strictly relative to this R{reference_price_zar:.2f} baseline."
        )
    lines.append(
        "   - **Source Documents & Disclosures Considered Table (MANDATORY FIRST TABLE):** Immediately after the JSON block, output the following Markdown table clearly listing every source PDF and SENS notice considered in this valuation:"
    )
    for tbl_line in format_documents_considered_table(source_documents, include_placeholder_roles=True):
        lines.append(f"     {tbl_line}")
    lines.extend([
        "   - **Rating Bands Logic:** Set explicit ZAR price boundary levels anchored to your 12-month target price: Strong Buy (share price giving >30% upside / deep margin of safety), Buy (15% to 30% upside), Hold (-5% to +15% upside), Sell (-5% to -15% downside), and Strong Sell (share price above sell threshold, >15% downside).",
        "   - **Conditional Summary Card:** When WITHHELD, show status and blocking issues only. The price/return/band template below applies only when READY. Follow the Source Documents table immediately with your publication-grade Valuation Summary Card table:",
        "     | Metric | Determination | Basis & Key Commentary |",
        "     | :--- | :---: | :--- |",
        f"     | **Sector** | {table_sec} | [Sub-sector classification] |",
        f"     | **Current Reference Share Price** | {table_ref_val} | {table_ref_comment} |",
        "     | **12-Month JSE Target Price** | R[0.00] | [Target price & primary valuation methodology] |",
        "     | **Implied Capital Upside / (Downside)** | [+/-0.0]% | [Relative to reference price] |",
        "     | **Forward Dividend Yield (FY27E)** | [0.0]% | [Distribution policy & payout ratio] |",
        "     | **Projected 12-Month TSR** | [+/-0.0]% | [Capital return + forward dividend yield] |",
        "     | **Institutional Recommendation** | [BUY | HOLD | SELL] | [Primary investment thesis] |",
        "     | **Dynamic Rating Bands** | Strong Buy: ≤R[0.00], Buy: ≤R[0.00], Hold: ≤R[0.00], Sell: ≤R[0.00], Strong Sell: >R[0.00] | [Live rating adjustment thresholds across price fluctuations] |",
        "   - Followed by the core institutional thesis and structural headwinds/tailwinds.",
    ])
    return lines


def _format_critical_formatting_constraints() -> list[str]:
    """Generates the strict negative formatting rules placed at the very end of the prompt."""
    return [
        "---",
        "",
        "## CRITICAL OUTPUT FORMATTING CONSTRAINTS (STRICTLY ENFORCED)",
        "",
        "To ensure institutional publication quality and 100% deterministic parsing, you MUST follow these formatting rules:",
        "1. **Mandatory JSON Block First:** Section 1 MUST open with the exact ```json ... ``` summary block containing native numeric values when READY and JSON null for derived valuation fields when WITHHELD.",
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
    reference_price_zar: float | None = None,
    source_documents: list[dict] | None = None,
    db_path: str | Path | None = None,
) -> str:
    """Build a conditional valuation prompt from reviewable Stage 1 determinations."""
    md_lines: list[str] = []
    md_lines.append("# STAGE 2: INSTITUTIONAL 2-YEAR VALUATION & FORECAST PROMPT")
    md_lines.append(f"**Target Asset:** {company_title} ({ticker})  ")
    md_lines.append(f"**Sector:** {get_jse_sector_name(detected_sector, ticker=ticker)} ({get_jse_sector_code(detected_sector, ticker=ticker)} / {detected_sector.capitalize()})  ")
    if sens_announcements:
        sens_str = "; ".join(sens_announcements)
        md_lines.append(f"**Input Mode:** Full Company Results PDF + Subsequent SENS Notices ({sens_str}) + Audited Stage 1 Determinations  ")
    else:
        md_lines.append(f"**Input Mode:** Full Company Results PDF (Attached) + Audited Stage 1 Forensic Determinations (Below)  ")
    md_lines.append(f"**Target Deliverable:** 2-Year Forecast Model, Valuation Bridge, and JSE Equity Research Note (ZAR per Share)")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("### INSTRUCTIONS FOR INSTITUTIONAL RESEARCH ANALYST (LLM):")

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
            "1. **Reviewable Stage 1 Working Papers:** Treat the Stage 1 Forensic Determinations provided below "
            "as reviewable working claims to verify against primary evidence (e.g. merchandise vs credit revenue split, gross margin bridges, "
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
        md_lines.append("## STAGE 1 WORKING DETERMINATIONS (REOPEN CONTRADICTIONS)")
        md_lines.append("")
        md_lines.append(stage1_content)
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## REQUIRED SECTIONS OF THE INSTITUTIONAL VALUATION NOTE")
        md_lines.append("")
        md_lines.extend(_format_section1_spec(ticker, company_title, "Retail", "retail", reference_price_zar=reference_price_zar, source_documents=source_documents))
        md_lines.append("2. **Detailed Operational Forecast (Historical Base Period + FY26E, FY27E & FY28E):** Include historical actuals column(s) alongside forecasts for merchandise sales by segment (with exact currency units, e.g. R'm vs EUR'm), credit vs cash mix, gross margin %, debtor cost %, store count, trading space m², and trading density.")
        md_lines.append("3. **Consolidated Financial Statements & Cash Flow Bridge:** Include historical actuals column(s) alongside forecasts for Revenue, Cost of Sales, Gross Profit, Other Revenue/Income, Net Operating Expenses, Operating Profit, Net Finance Costs, PBT, Tax, PAT (Continuing), Discontinued Operations, PAT (Total), Weighted-Average Shares (m), Continuing HEPS (cents), and Free Cash Flow to Equity (FCFE).")
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
            "1. **Reviewable Stage 1 Working Papers:** Treat the Stage 1 Forensic Determinations provided below "
            "as reviewable working claims to verify against primary evidence (e.g. SA REIT distributable income adjustments, like-for-like NPI growth, "
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
        md_lines.append("## STAGE 1 WORKING DETERMINATIONS (REOPEN CONTRADICTIONS)")
        md_lines.append("")
        md_lines.append(stage1_content)
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## REQUIRED SECTIONS OF THE INSTITUTIONAL VALUATION NOTE")
        md_lines.append("")
        md_lines.extend(_format_section1_spec(ticker, company_title, "REIT / Listed Property", "reit", reference_price_zar=reference_price_zar, source_documents=source_documents))
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
            "1. **Reviewable Stage 1 Working Papers:** Treat the Stage 1 Forensic Determinations provided below "
            "as reviewable working claims to verify against primary evidence (e.g. recurring revenue / ARR mix, gross margin by line of business, "
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
        md_lines.append("## STAGE 1 WORKING DETERMINATIONS (REOPEN CONTRADICTIONS)")
        md_lines.append("")
        md_lines.append(stage1_content)
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## REQUIRED SECTIONS OF THE INSTITUTIONAL VALUATION NOTE")
        md_lines.append("")
        md_lines.extend(_format_section1_spec(ticker, company_title, "Technology / IT Services", "it", reference_price_zar=reference_price_zar, source_documents=source_documents))
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
            "1. **Reviewable Stage 1 Working Papers:** Treat the Stage 1 Forensic Determinations provided below "
            "as reviewable working claims to verify against primary evidence (e.g. residential development pipeline units, serviced stands, memorial park plot margins, "
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
        md_lines.append("## STAGE 1 WORKING DETERMINATIONS (REOPEN CONTRADICTIONS)")
        md_lines.append("")
        md_lines.append(stage1_content)
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## REQUIRED SECTIONS OF THE INSTITUTIONAL VALUATION NOTE")
        md_lines.append("")
        md_lines.extend(_format_section1_spec(ticker, company_title, "Construction & Materials", "construction", reference_price_zar=reference_price_zar, source_documents=source_documents))
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
    elif detected_sector == "mining":
        md_lines.append(
            "You are acting as an elite **Managing Director & Head of Mining Equity Research** at a premier institutional investment bank."
        )
        md_lines.append(
            f"You are conducting a definitive 2-year operational and valuation forecast for **{company_title} ({ticker})**."
        )
        md_lines.append("")
        md_lines.append("### CORE OPERATING RULES & EVIDENCE HIERARCHY:")
        md_lines.append(
            "1. **Reviewable Stage 1 Working Papers:** Treat the Stage 1 Forensic Determinations provided below "
            "as reviewable working claims to verify against primary evidence (e.g. share count anchors, net cash reconciliation, EBITDA adjustments, "
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
        md_lines.append("## STAGE 1 WORKING DETERMINATIONS (REOPEN CONTRADICTIONS)")
        md_lines.append("")
        md_lines.append(stage1_content)
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## REQUIRED SECTIONS OF THE INSTITUTIONAL VALUATION NOTE")
        md_lines.append("")
        md_lines.extend(_format_section1_spec(ticker, company_title, "Mining", "mining", reference_price_zar=reference_price_zar, source_documents=source_documents))
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
    elif detected_sector in {"finance", "telcos", "consumer_lending"}:
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
            "1. **Reviewable Stage 1 Working Papers:** Treat the Stage 1 Forensic Determinations provided below "
            "as reviewable working claims to verify against primary evidence. Do not revert to high-level headline narratives from the PDF. "
            "If you identify definitive evidence in the primary PDF financial notes that contradicts or refines a Stage 1 determination, "
            "you may depart from it ONLY by explicitly declaring the disagreement, citing the exact note/table and page from the PDF, "
            "and providing your quantitative justification."
        )
        md_lines.append(
            f"2. **Primary Reporting & Trading Currency:** {ticker} trades on the **Johannesburg Stock Exchange (JSE)**. "
            "All final valuation targets, earnings per share, and dividends per share must be presented in **ZAR (Rands per share or ZAR cents)**."
        )
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## STAGE 1 WORKING DETERMINATIONS (REOPEN CONTRADICTIONS)")
        md_lines.append("")
        md_lines.append(stage1_content)
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## REQUIRED SECTIONS OF THE INSTITUTIONAL VALUATION NOTE")
        md_lines.append("")
        md_lines.extend(_format_section1_spec(ticker, company_title, cfg.display_name, detected_sector, reference_price_zar=reference_price_zar, source_documents=source_documents))
        md_lines.append("2. **Detailed Operational & Segment Forecast (FY27E & FY28E):** Segment drivers, margins, and operational KPIs.")
        md_lines.append("3. **Consolidated Financial Statements & FCFE Bridge:** Income statement, balance sheet, and equity free cash flow.")
        md_lines.append("4. **Institutional Valuation Table:** Intrinsic valuation methodology, multiples, and target price in ZAR.")
        md_lines.append("5. **Forward Valuation Multiples & Sensitivity Matrix:** Target multiples and sensitivity analysis.")
        md_lines.append("6. **Actionable Portfolio Monitoring Triggers & Catalysts:** Red lines, sensitivity impacts, and reporting dates.")
    else:
        raise ValueError(
            f"Sector '{detected_sector}' does not have a dedicated Stage 2 valuation model implemented."
        )
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
            "1. **Reviewable Stage 1 Working Papers:** Treat the Stage 1 Forensic Determinations provided below "
            "as reviewable working claims to verify against primary evidence (e.g. share count anchors, net cash reconciliation, EBITDA adjustments, "
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
        md_lines.append("## STAGE 1 WORKING DETERMINATIONS (REOPEN CONTRADICTIONS)")
        md_lines.append("")
        md_lines.append(stage1_content)
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## REQUIRED SECTIONS OF THE INSTITUTIONAL VALUATION NOTE")
        md_lines.append("")
        cfg = get_sector_config(detected_sector)
        md_lines.extend(_format_section1_spec(ticker, company_title, cfg.display_name, cfg.code, reference_price_zar=reference_price_zar))
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

    guardrails_md = format_sector_guardrails_block(detected_sector, stage="stage2", db_path=db_path)
    if guardrails_md:
        md_lines.append("---")
        md_lines.append("")
        md_lines.append(guardrails_md)
    md_lines.extend(_format_critical_formatting_constraints())
    md_lines.append(valuation_gate_prompt())
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
        if not sector:
            warnings.warn(
                f"Sector for company '{ticker}' could not be automatically detected. Falling back to default 'mining'.",
                UserWarning,
                stacklevel=2,
            )
        detected_sector = (sector or "mining").lower()
        company_dir = PROJECT_ROOT / f"companies/{detected_sector}/{ticker}"

    default_title = (f"{ticker} Properties" if detected_sector == "reit" else (f"{ticker} Technologies" if detected_sector == "it" else (f"{ticker} Construction" if detected_sector == "construction" else (f"{ticker} Group" if detected_sector in {"retail", "consumer_lending"} else f"{ticker} Resources"))))
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
    parser = argparse.ArgumentParser(description="Generate Stage 2 Institutional Valuation Prompt for Institutional Valuation (LLM).")
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
