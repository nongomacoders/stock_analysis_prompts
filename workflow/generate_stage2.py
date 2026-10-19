"""Script to generate the Stage 2 Institutional Valuation Prompt for Gemini 4 Argon.

Combines the source PDF report with the Stage 1 Forensic Audit Determinations as ground truth,
directing Argon to produce the final 2-year forecast, SOTP DCF, and JSE equity research valuation note (ZAR per share).
"""

from __future__ import annotations

import argparse
from pathlib import Path


def generate_stage2_prompt(
    ticker: str,
    company_name: str | None = None,
    period: str | None = None,
    stage1_response_path: Path | None = None,
    output_path: Path | None = None,
) -> Path:
    ticker = ticker.upper()
    period_tag = (period or "FY26").upper()
    company_title = company_name or f"{ticker} Resources"

    briefs_dir = Path(f"companies/{ticker}/briefs/{period_tag}")
    root_briefs_dir = Path(f"companies/{ticker}/briefs")

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
            "NET CASH POSITION, SBP EBITDA ADJUSTMENTS, ORGANIC AISC, CAPEX SCENARIOS, AND SECTION 36 CASH TAX MECHANICS]"
        )

    md_lines: list[str] = []
    md_lines.append(f"# STAGE 2: INSTITUTIONAL 2-YEAR VALUATION & FORECAST PROMPT")
    md_lines.append(f"**Target Asset:** {company_title} ({ticker})  ")
    md_lines.append(f"**Input Mode:** Full Company Results PDF (Attached) + Audited Stage 1 Forensic Determinations (Below)  ")
    md_lines.append(f"**Target Deliverable:** 2-Year Forecast Model, SOTP DCF Valuation, and JSE Equity Research Note (ZAR per Share)")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("### INSTRUCTIONS FOR GEMINI 4 ARGON:")
    md_lines.append(
        "You are acting as an elite **Managing Director & Head of Mining Equity Research** at a premier institutional investment bank."
    )
    md_lines.append(
        f"You are conducting a definitive 2-year operational and valuation forecast for **{company_title} ({ticker})**."
    )
    md_lines.append("")
    md_lines.append("### CORE OPERATING RULES & EVIDENCE HIERARCHY:")
    md_lines.append(
        "1. **Audited Ground Truth:** The Stage 1 Forensic Determinations provided below are audited and verified. "
        "Treat them as authoritative ground truth (e.g. share count anchors, net cash reconciliation, EBITDA adjustments, "
        "organic unit costs, and Section 36 cash tax step-up curve). Do not revert to high-level headline narratives from the PDF "
        "where Stage 1 has established an audited reconciliation."
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
    md_lines.append("1. **Executive Investment Thesis & 12-Month JSE Price Target (ZAR/share)**")
    md_lines.append("2. **Detailed Asset-by-Asset Operational Forecast (FY27E & FY28E):** Throughput, recovered grade, production (oz), cash costs, and AISC per asset.")
    md_lines.append("3. **Consolidated Financial Statements & FCFE Bridge:** Revenue, EBITDA, Section 36 Cash Tax, Net Profit, and Free Cash Flow to Equity.")
    md_lines.append("4. **Sum-of-the-Parts (SOTP) DCF Valuation Table:** Asset-by-asset NAV, unallocated corporate costs, net cash/debt, and per-share equity value in ZAR.")
    md_lines.append("5. **Forward Valuation Multiples & Sensitivity Matrix:** Target P/E, EV/EBITDA, FCF yield, and 2D sensitivity table (Gold Price vs USD/ZAR).")
    md_lines.append("")

    content = "\n".join(md_lines)

    if output_path is None:
        briefs_dir.mkdir(parents=True, exist_ok=True)
        output_path = briefs_dir / f"{ticker}_{period_tag}_stage2_valuation_prompt.md"

    output_path.write_text(content, encoding="utf-8")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate Stage 2 Institutional Valuation Prompt for Gemini 4 Argon.")
    parser.add_argument("ticker", help="Company ticker (e.g. PAN, HAR)")
    parser.add_argument("--name", help="Full company name (e.g. 'Pan African Resources PLC')", default=None)
    parser.add_argument("--period", help="Financial period (e.g. FY26, FY27)", default="FY26")
    parser.add_argument("--stage1", help="Path to Stage 1 audit response markdown file", default=None)
    parser.add_argument("--output", help="Custom output path", default=None)

    args = parser.parse_args()
    out = generate_stage2_prompt(
        ticker=args.ticker.upper(),
        company_name=args.name,
        period=args.period.upper() if args.period else None,
        stage1_response_path=Path(args.stage1) if args.stage1 else None,
        output_path=Path(args.output) if args.output else None,
    )
    print(f"Successfully generated Stage 2 Valuation Prompt at: {out}")



if __name__ == "__main__":
    main()
