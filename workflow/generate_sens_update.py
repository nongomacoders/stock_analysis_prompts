"""Script to generate a simplified SENS Valuation Update Prompt for Valuation Model (LLM).

Combines the established Final Institutional Valuation Report with SENS continuous disclosure notices
(in PDF or plain text format), directing the LLM to generate a new updated valuation report and re-rated monitoring triggers.
Also provides utility functions to archive analyzed SENS notices into a completed directory.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from companies import find_company_dir
from companies.sectors import get_sector_config, get_jse_sector_code, get_jse_sector_name
from section_capture.db import (
    connect_db,
    detect_company_meta,
    resolve_db_path,
)


def get_sens_completed_dir(company_dir: Path) -> Path:
    """Returns the directory where analyzed SENS files are moved."""
    sens_dir = company_dir / "sources/sens"
    for candidate in [
        company_dir / "sources/sens/completed",
        company_dir / "sources/sens_completed",
        company_dir / "sources/sens completed",
    ]:
        if candidate.exists():
            return candidate
    target = sens_dir / "completed"
    target.mkdir(parents=True, exist_ok=True)
    return target


def move_analyzed_sens_files(
    company_dir: Path,
    filenames: list[str] | None = None,
) -> list[Path]:
    """Moves analyzed SENS files from sources/sens to the completed folder."""
    sens_dir = company_dir / "sources/sens"
    if not sens_dir.exists():
        return []

    completed_dir = get_sens_completed_dir(company_dir)
    completed_dir.mkdir(parents=True, exist_ok=True)

    moved: list[Path] = []
    if filenames:
        targets = [sens_dir / fn for fn in filenames]
    else:
        # Move all non-directory files in sens_dir with supported extensions
        targets = [
            f for f in sens_dir.iterdir()
            if f.is_file() and f.suffix.lower() in {".pdf", ".txt", ".text", ".md"} and f.name.lower() != "readme.md"
        ]

    for f in targets:
        if f.exists() and f.is_file():
            dest = completed_dir / f.name
            if dest.exists():
                dest.unlink()
            shutil.move(str(f), str(dest))
            moved.append(dest)

    return moved


def build_sens_update_prompt_content(
    baseline_valuation_report: str,
    company_title: str,
    ticker: str,
    detected_sector: str,
    sens_filename: str | None = None,
    sens_entries: list[dict] | None = None,
    reference_price_zar: float | None = None,
) -> str:
    """Constructs the simplified SENS Valuation Update prompt with PDF and/or embedded text notices."""
    md_lines: list[str] = []

    text_entries = [e for e in (sens_entries or []) if e.get("is_text") and e.get("content")]
    pdf_entries = [e for e in (sens_entries or []) if not e.get("is_text")]

    md_lines.append("# STAGE 2-U: INSTITUTIONAL VALUATION SENS UPDATE & RE-RATING")
    md_lines.append(f"**Target Asset:** {company_title} ({ticker})  ")
    md_lines.append(f"**Sector:** {detected_sector.capitalize()}  ")

    if text_entries and not pdf_entries:
        s_names = ", ".join(f"`{e['filename']}`" for e in text_entries)
        md_lines.append(f"**Subsequent Disclosures:** {len(text_entries)} SENS text announcement(s) (Full text embedded in Section 2 below): {s_names}  ")
    elif pdf_entries and not text_entries:
        s_names = ", ".join(f"`{e['filename']}`" for e in pdf_entries)
        md_lines.append(f"**Attached Document(s):** {s_names} (SENS / ASX Announcement PDF attached in chat)  ")
    elif pdf_entries and text_entries:
        t_names = ", ".join(f"`{e['filename']}`" for e in text_entries)
        p_names = ", ".join(f"`{e['filename']}`" for e in pdf_entries)
        md_lines.append(f"**Subsequent Disclosures:** Embedded text: {t_names} | Attached PDF: {p_names}  ")
    elif sens_filename:
        md_lines.append(f"**Attached Document:** `{sens_filename}` (SENS / ASX Announcement attached in chat)  ")
    else:
        md_lines.append("**Attached Document:** SENS / ASX Announcement (attached in chat)  ")

    md_lines.append(f"**Base Document:** Established Final Institutional Valuation Report (Provided Below)  ")
    md_lines.append(f"**Task Directive:** SENS Evidence Integration & Generation of New Updated Institutional Valuation Report  ")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("### INSTRUCTIONS FOR INSTITUTIONAL RESEARCH ANALYST (LLM):")

    jse_code = get_jse_sector_code(detected_sector, ticker=ticker)
    jse_name = get_jse_sector_name(detected_sector, ticker=ticker)
    persona = get_sector_config(detected_sector).sens_persona
    md_lines.append(
        f"You are acting as an elite **{persona}** at a premier institutional investment bank."
    )

    md_lines.append("")
    if text_entries and not pdf_entries:
        md_lines.append(
            f"We are adding {len(text_entries)} subsequent **SENS continuous disclosure announcement(s) (full text embedded in Section 2 below)** "
            "together with our established **Final Institutional Valuation Report** (provided in full below).\n\n"
            "A **new updated valuation report** needs to be generated reflecting these subsequent disclosures."
        )
    else:
        md_lines.append(
            "We are adding a subsequent **SENS / continuous disclosure announcement (PDF attached in chat)** "
            "together with our established **Final Institutional Valuation Report** (provided in full below).\n\n"
            "A **new updated valuation report** needs to be generated reflecting this new disclosure."
        )

    md_lines.append("")
    md_lines.append("### CORE OPERATING DIRECTIVES:")
    if text_entries and not pdf_entries:
        md_lines.append(
            "1. **Analyze the Embedded SENS Text Announcement(s):**\n"
            "   - Read the subsequent SENS continuous disclosure text provided below in Section 2, and extract key transaction terms, "
            "property/asset disposals, debt redemptions/reductions, governance/censure findings, AGM results, condition precedents (CPs), and revised cash runway."
        )
    elif pdf_entries and not text_entries:
        md_lines.append(
            "1. **Analyze the Attached SENS PDF(s):**\n"
            "   - Read the attached SENS / ASX PDF and extract the key terms, funding milestones, condition precedents (CPs) satisfied, "
            "offtake agreements, cash movements, and revised commissioning/production dates."
        )
    else:
        md_lines.append(
            "1. **Analyze the Subsequent SENS Disclosures:**\n"
            "   - Review the continuous disclosure announcements (embedded text below and/or attached PDF), extracting all key transaction terms, "
            "asset disposals, debt repayments, CPs satisfied, and balance sheet movements."
        )

    md_lines.append("")
    md_lines.append(
        "2. **Evaluate the Valuation & Balance Sheet Impact:**\n"
        "   - Cross-examine the new evidence against the established Final Valuation Report below.\n"
        "   - Determine whether the **12-Month Target Price (ZAR)**, **Current Reference Price**, or **Recommendation (BUY / HOLD / SELL)** "
        "should be revised or reaffirmed. Quantify the exact financial impact."
    )
    md_lines.append("")
    md_lines.append(
        "3. **Re-Rate Actionable Portfolio Monitoring Triggers:**\n"
        "   - Review Section 6 ('Actionable Portfolio Monitoring Triggers & Catalysts') of the established report.\n"
        "   - Mark which triggers have **[FIRED / RESOLVED]** citing the SENS release.\n"
        "   - Update remaining active triggers and add any new catalysts or operational red lines established by this notice."
    )
    md_lines.append("")
    sector_display = (
        "Technology / IT Services" if detected_sector == "it"
        else ("REIT / Listed Property" if detected_sector == "reit"
        else ("Retail" if detected_sector == "retail" else "Mining"))
    )

    md_lines.append(
        "4. **Generate the New Updated Valuation Report:**\n"
        "   - Produce the complete, publication-grade new report incorporating this post-SENS reality.\n"
        "   - **MANDATORY JSON SUMMARY BLOCK:** You MUST open Section 1 with the following exact machine-readable JSON block containing your updated metrics:\n"
        "     ```json\n"
        "     {\n"
        f'       "ticker": "{ticker}",\n'
        f'       "company_name": "{company_title}",\n'
        f'       "sector": "{detected_sector}",\n'
        f'       "jse_sector_code": "{jse_code}",\n'
        f'       "jse_sector_name": "{jse_name}",\n'
        '       "recommendation": "BUY | HOLD | SELL",\n'
        f'       "reference_price_zar": {reference_price_zar:.2f},\n' if (reference_price_zar and reference_price_zar > 0) else '       "reference_price_zar": 0.00,\n'
        '       "target_price_zar": 0.00,\n'
        '       "implied_upside_pct": 0.0,\n'
        '       "forward_dividend_yield_pct": 0.0,\n'
        '       "projected_12m_tsr_pct": 0.0,\n'
        '       "rating_bands": {\n'
        '         "strong_buy_max_zar": 0.00,\n'
        '         "buy_max_zar": 0.00,\n'
        '         "hold_max_zar": 0.00,\n'
        '         "sell_max_zar": 0.00,\n'
        '         "strong_sell_above_zar": 0.00\n'
        '       }\n'
        "     }\n"
        "     ```\n"
        "   - **Source Documents & Disclosures Considered Table (MANDATORY FIRST TABLE):** Immediately after the JSON block, output a Markdown table (`### Source Documents & Disclosures Considered`) listing all baseline report documents and the newly incorporated SENS announcement(s) with their filename, document type, period/date, and key evidence considered.\n"
        "   - **Rating Bands Logic:** Set explicit ZAR price boundary levels re-rated for this post-SENS reality: Strong Buy (>30% upside / margin of safety), Buy (15% to 30% upside), Hold (-5% to +15% upside), Sell (-5% to -15% downside), and Strong Sell (>15% downside).\n"
        "   - **Executive Valuation Summary Card Table:** Follow the JSON block immediately with your updated 4-column comparison table:\n"
        "     | Metric | Prior (Stage 2) | Updated (Stage 2-U) | Basis & Post-SENS Commentary |\n"
        "     | :--- | :---: | :---: | :--- |\n"
        f"     | **Sector** | {sector_display} | {sector_display} | [Classification] |\n"
        f"     | **Current Reference Share Price** | R[0.00] | R{reference_price_zar:.2f} | [Verified closing price via Yahoo Finance / user input] |\n" if (reference_price_zar and reference_price_zar > 0) else "     | **Current Reference Share Price** | R[0.00] | R[0.00] | [Closing date & price] |\n"
        "     | **12-Month JSE Target Price** | R[0.00] | R[0.00] | [Target price & revision basis] |\n"
        "     | **Implied Capital Upside / (Downside)** | [+/-0.0]% | [+/-0.0]% | [Relative to reference price] |\n"
        "     | **Forward Dividend Yield (FY27E)** | [0.0]% | [0.0]% | [Distribution policy & payout] |\n"
        "     | **Projected 12-Month TSR** | [+/-0.0]% | [+/-0.0]% | [Capital return + dividend yield] |\n"
        "     | **Institutional Recommendation** | [BUY | HOLD | SELL] | [BUY | HOLD | SELL] | [Primary rating thesis] |\n"
        "     | **Dynamic Rating Bands** | Strong Buy: ≤R[0.00], Buy: ≤R[0.00], Hold: ≤R[0.00], Sell: ≤R[0.00], Strong Sell: >R[0.00] | Strong Buy: ≤R[0.00], Buy: ≤R[0.00], Hold: ≤R[0.00], Sell: ≤R[0.00], Strong Sell: >R[0.00] | [Re-rated price triggers across share price fluctuations] |"
    )
    md_lines.append("")

    if text_entries:
        md_lines.append("---")
        md_lines.append("")
        md_lines.append(f"## 2. SUBSEQUENT SENS CONTINUOUS DISCLOSURE EVIDENCE ({len(text_entries)} ANNOUNCEMENT{'S' if len(text_entries) > 1 else ''})")
        md_lines.append("")
        for i, te in enumerate(text_entries, 1):
            md_lines.append(f"### SENS Announcement {i}: `{te['filename']}`")
            md_lines.append("```text")
            md_lines.append(te["content"].strip())
            md_lines.append("```")
            md_lines.append("")

    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## ESTABLISHED FINAL INSTITUTIONAL VALUATION REPORT (GROUND TRUTH)")
    md_lines.append("")
    md_lines.append(baseline_valuation_report.strip())
    md_lines.append("")

    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## CRITICAL OUTPUT FORMATTING CONSTRAINTS (STRICTLY ENFORCED)")
    md_lines.append("")
    md_lines.append("To ensure institutional publication quality and 100% deterministic parsing, you MUST follow these formatting rules:")
    md_lines.append("1. **Mandatory JSON Block First:** Section 1 MUST open with the exact ```json ... ``` summary block containing native float numbers (e.g. `0.42`, `-30.0`), not text descriptions.")
    md_lines.append("2. **Zero HTML Tags:** DO NOT use any HTML tags (`<br>`, `<br/>`, `<span>`, `<div>`, etc.). Use standard Markdown newlines.")
    md_lines.append("3. **Single-Line Table Rows:** Every Markdown table row MUST be on a single continuous line starting and ending with `|`. DO NOT insert blank lines (`\\n\\n`) within table rows or split cells across multiple lines.")
    md_lines.append("4. **Isolated Determination Cells:** In the Valuation Summary Card, keep determination columns strictly limited to the metric value (e.g. `R0.42` or `-30.0%`). Reserve all commentary and secondary notes strictly for the Commentary column.")
    md_lines.append("5. **No Special Symbols or Arbitrary Code Blocks:** DO NOT wrap ordinary numbers or percentages in backticks (`). Reserve backticks solely for the initial JSON block and formal code/file identifiers.")
    md_lines.append("")

    return "\n".join(md_lines)


def generate_sens_update_prompt(
    ticker: str,
    company_name: str | None = None,
    sector: str | None = None,
    period: str | None = None,
    sens_filename: str | None = None,
    output_path: Path | None = None,
    db_path: str | Path | None = None,
) -> Path:
    """Generates the simplified SENS Valuation Update prompt for Valuation Model (LLM)."""
    ticker = ticker.upper().strip()
    resolved_db = resolve_db_path(db_path)
    if not resolved_db.exists():
        raise FileNotFoundError(f"Database {resolved_db} not found.")

    found = find_company_dir(ticker, sector=sector)
    if found:
        detected_sector, company_dir = found
    else:
        detected_sector = (sector or "mining").lower()
        company_dir = PROJECT_ROOT / f"companies/{detected_sector}/{ticker}"

    company_title = company_name or (
        f"{ticker} Group" if detected_sector == "retail"
        else f"{ticker} Properties" if detected_sector == "reit"
        else f"{ticker} Technologies" if detected_sector == "it"
        else f"{ticker} Resources"
    )
    period_tag = (period or "FY26").upper()

    with connect_db(resolved_db) as conn:
        cur = conn.cursor()
        rows = cur.execute(
            """
            SELECT sha256, filename, stage2_response
            FROM reports
            WHERE (filename LIKE ? OR original_path LIKE ?) AND parent_report_sha256 IS NULL
            ORDER BY CASE WHEN stage2_response IS NOT NULL THEN 1 ELSE 2 END ASC, updated_at DESC
            """,
            (f"%{ticker}%", f"%{ticker}%"),
        ).fetchall()

        if not rows or not rows[0]["stage2_response"]:
            raise RuntimeError(f"No existing Stage 2 valuation report found in database for ticker {ticker}.")

        baseline_report = rows[0]["stage2_response"]

    sens_dir = company_dir / "sources/sens"
    sens_entries: list[dict] = []

    if sens_dir.exists():
        if sens_filename:
            # Explicit single file requested
            target = sens_dir / sens_filename
            if target.exists() and target.is_file():
                pending_files = [target]
            else:
                pending_files = []
        else:
            # Discover all pending SENS files (exclude subdirectories like completed/)
            pending_files = sorted(
                [f for f in sens_dir.iterdir() if f.is_file() and f.suffix.lower() in {".pdf", ".txt", ".text", ".md"} and f.name.lower() != "readme.md"],
                key=lambda p: p.name,
            )

        for pf in pending_files:
            is_txt = pf.suffix.lower() in {".txt", ".text", ".md"}
            txt_content = None
            if is_txt:
                try:
                    txt_content = pf.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    pass
            sens_entries.append({
                "filename": pf.name,
                "path": pf,
                "is_text": is_txt,
                "content": txt_content,
            })

    if not sens_entries and not sens_filename:
        comp_dir = get_sens_completed_dir(company_dir)
        has_completed = comp_dir.exists() and any(comp_dir.iterdir())
        if has_completed:
            raise RuntimeError(f"No pending SENS notices found in {sens_dir}. Notice(s) have already been moved to {comp_dir.name}/.")
        else:
            raise RuntimeError(f"No SENS notices (*.pdf, *.txt) found in {sens_dir}.")

    effective_sens_file = sens_filename
    if not effective_sens_file and sens_entries:
        effective_sens_file = sens_entries[-1]["filename"]

    content = build_sens_update_prompt_content(
        baseline_valuation_report=baseline_report,
        company_title=company_title,
        ticker=ticker,
        detected_sector=detected_sector,
        sens_filename=effective_sens_file,
        sens_entries=sens_entries,
    )

    if output_path is None:
        target_dir = company_dir / f"briefs/{period_tag}"
        target_dir.mkdir(parents=True, exist_ok=True)
        output_path = target_dir / f"{ticker}_{period_tag}_stage2_sens_update_prompt.md"

    output_path.write_text(content, encoding="utf-8")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate simplified SENS Valuation Update Prompt.")
    parser.add_argument("ticker", help="Company ticker (e.g. ORN, PAN, LEW, APF)")
    parser.add_argument("--sector", help="Sector (mining, retail, reit, finance, telcos)", default=None)
    parser.add_argument("--name", help="Company name", default=None)
    parser.add_argument("--period", help="Financial period (e.g. FY26)", default="FY26")
    parser.add_argument("--sens", help="Filename of specific SENS file", default=None)
    parser.add_argument("--output", help="Custom output path", default=None)
    parser.add_argument("--archive", action="store_true", help="Move analyzed SENS notices into completed/ folder.")

    args = parser.parse_args()
    out = generate_sens_update_prompt(
        ticker=args.ticker.upper(),
        company_name=args.name,
        sector=args.sector,
        period=args.period,
        sens_filename=args.sens,
        output_path=Path(args.output) if args.output else None,
    )
    print(f"Successfully generated SENS Valuation Update Prompt at: {out}")

    if args.archive:
        found = find_company_dir(args.ticker.upper(), sector=args.sector)
        if found:
            moved = move_analyzed_sens_files(found[1])
            print(f"Archived {len(moved)} SENS file(s) into completed/ directory.")


if __name__ == "__main__":
    main()
