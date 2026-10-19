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

    company_title = company_name or (f"{ticker} Group" if detected_sector == "retail" else f"{ticker} Resources")
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

def build_stage2_prompt_content(
    stage1_content: str,
    company_title: str,
    ticker: str,
    detected_sector: str,
) -> str:
    """Constructs the Stage 2 Markdown prompt text incorporating Stage 1 determinations as 99% confidence prior."""
    md_lines: list[str] = []
    md_lines.append("# STAGE 2: INSTITUTIONAL 2-YEAR VALUATION & FORECAST PROMPT")
    md_lines.append(f"**Target Asset:** {company_title} ({ticker})  ")
    md_lines.append(f"**Sector:** {detected_sector.capitalize()}  ")
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
        md_lines.append("1. **Executive Investment Thesis & 12-Month JSE Price Target (ZAR/share)**")
        md_lines.append("2. **Detailed Operational Forecast (FY27E & FY28E):** Merchandise sales, credit vs cash mix, gross margin %, debtor cost %, store count, trading space m², and trading density.")
        md_lines.append("3. **Consolidated Financial Statements & Cash Flow Bridge:** Revenue, Gross Profit, Operating Expenses, Operating Profit, PAT, HEPS, and Free Cash Flow to Equity (FCFE).")
        md_lines.append("4. **Valuation Multiples & DCF Table:** Forward P/E, EV/EBITDA, dividend yield, and per-share equity value in ZAR.")
        md_lines.append("5. **Sensitivity Matrix:** 2D sensitivity table (Sales Growth vs Debtor Cost % or P/E Multiple).")
        md_lines.append("")
    else:
        md_lines.append(
            "You are acting as an elite **Managing Director & Head of Mining Equity Research** at a premier institutional investment bank."
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
        md_lines.append("1. **Executive Investment Thesis & 12-Month JSE Price Target (ZAR/share)**")
        md_lines.append("2. **Detailed Asset-by-Asset Operational Forecast (FY27E & FY28E):** Throughput, recovered grade, production (oz), cash costs, and AISC per asset.")
        md_lines.append("3. **Consolidated Financial Statements & FCFE Bridge:** Revenue, EBITDA, Section 36 Cash Tax, Net Profit, and Free Cash Flow to Equity.")
        md_lines.append("4. **Sum-of-the-Parts (SOTP) DCF Valuation Table:** Asset-by-asset NAV, unallocated corporate costs, net cash/debt, and per-share equity value in ZAR.")
        md_lines.append("5. **Forward Valuation Multiples & Sensitivity Matrix:** Target P/E, EV/EBITDA, FCF yield, and 2D sensitivity table (Gold Price vs USD/ZAR).")
        md_lines.append("")

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

    company_title = company_name or (f"{ticker} Group" if detected_sector == "retail" else f"{ticker} Resources")
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
