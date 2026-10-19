"""Script to compile sequential section extractions and question ledgers into a Stage 1 Forensic Audit Prompt.

Queries documents/analysis.sqlite and packages the full chronological working paper
dossier for Gemini 4 Argon to evaluate without an attached PDF.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sqlite3
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from companies import find_company_dir

DB_PATH = Path("documents/analysis.sqlite")


def get_latest_report_sha(conn: sqlite3.Connection) -> tuple[str, str] | None:
    cur = conn.cursor()
    row = cur.execute(
        "SELECT sha256, filename FROM reports ORDER BY updated_at DESC LIMIT 1"
    ).fetchone()
    if row:
        return row[0], row[1]
    return None


def export_stage1_prompt(
    ticker: str,
    company_name: str | None = None,
    sector: str | None = None,
    report_sha: str | None = None,
    period: str | None = None,
    output_path: Path | None = None,
) -> Path:
    ticker = ticker.upper().strip()

    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database {DB_PATH} not found.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if not report_sha:
        latest = get_latest_report_sha(conn)
        if not latest:
            raise RuntimeError("No reports found in documents/analysis.sqlite.")
        report_sha, filename = latest
    else:
        row = cur.execute(
            "SELECT filename FROM reports WHERE sha256 = ?", (report_sha,)
        ).fetchone()
        filename = row["filename"] if row else "Company Report"

    # Resolve company directory and sector
    found = find_company_dir(ticker, sector=sector)
    if found:
        detected_sector, company_dir = found
    else:
        detected_sector = (sector or "mining").lower()
        company_dir = PROJECT_ROOT / f"companies/{detected_sector}/{ticker}"

    company_title = company_name or (f"{ticker} Group" if detected_sector == "retail" else f"{ticker} Resources")

    # Query all sections
    sections = cur.execute(
        """
        SELECT section_number, section_id, heading, subheading, analyst_question,
               selected_text, stored_questions_snapshot, llm_response
        FROM sections
        WHERE report_sha256 = ?
        ORDER BY section_number ASC, id ASC
        """,
        (report_sha,),
    ).fetchall()

    if not sections:
        raise RuntimeError(f"No sections captured for report SHA: {report_sha}")

def build_stage1_prompt_content(
    sections: list,
    company_title: str,
    ticker: str,
    detected_sector: str,
    filename: str,
) -> str:
    """Constructs the Stage 1 Markdown prompt text from section rows."""
    md_lines: list[str] = []
    md_lines.append("# STAGE 1: INDEPENDENT COGNITIVE AUDIT VIA SEQUENTIAL EXTRACTION & QUESTION LEDGER")
    md_lines.append(f"**Target Asset:** {company_title} ({ticker})  ")
    md_lines.append(f"**Sector:** {detected_sector.capitalize()}  ")
    md_lines.append(f"**Source Document:** `{filename}`  ")
    md_lines.append(f"**Input Mode:** Sequential Forensic Working Paper & Dynamic Questions Ledger (No PDF Attached)  ")
    md_lines.append(f"**Task Directive:** Forensic Reasoning & Conflict Reconciliation Only (No Full Forward Valuation Model Required)")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("### INSTRUCTIONS FOR GEMINI 4 ARGON:")

    if detected_sector == "retail":
        md_lines.append(
            "You are acting as an independent **Managing Director and Senior Forensic Retail & Consumer Credit Accounting Auditor**. "
        )
        md_lines.append(
            f"You have been provided with the complete, chronological working paper compiled during a section-by-section "
            f"forensic capture of {company_title}'s financial results announcement ({len(sections)} sections)."
        )
    else:
        md_lines.append(
            "You are acting as an independent **Managing Director and Senior Forensic Mining Accounting Auditor**. "
        )
        md_lines.append(
            f"You have been provided with the complete, chronological working paper compiled during a section-by-section "
            f"forensic capture of {company_title}'s financial results announcement ({len(sections)} sections)."
        )

    md_lines.append("")
    md_lines.append("Notice how this working paper is constructed:")
    md_lines.append(
        "1. At each stage, specific text, accounting notes, APMs, and operational tables were extracted directly from the report."
    )
    md_lines.append(
        "2. Across the sections, an **Open Questions Ledger** evolved dynamically: anomalies and high-level management claims "
        "in early sections were flagged with priority levels, specific verification instructions, and carried forward as "
        "`Pending` until verified against primary financial statements, detailed accounting notes, and segmental summaries."
    )
    md_lines.append("")
    md_lines.append("**YOUR MANDATE:**")
    md_lines.append(
        "Review the sequential evidence trail below. Trace how the questions evolved from initial anomalies to audited reconciliation. "
        "**Do not produce a forward equity research forecast or valuation report.** Your role is **forensic reasoning only**: you must "
        "evaluate the working papers and independently reach your own definitive determinations on the core accounting, operational, "
        "and balance sheet junctions."
    )
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## REQUIRED STRUCTURE OF YOUR AUDIT REPORT")
    md_lines.append("")
    md_lines.append("Please format your response into the following four clear sections:")
    md_lines.append("1. **Executive Forensic Audit Summary:** Concise synthesis of the group's true economic performance, balance sheet health, and key findings.")

    if detected_sector == "retail":
        md_lines.append(
            "2. **Detailed Forensic Reasoning & Determinations:** Step-by-step walkthrough of each key retail junction "
            "(merchandise vs credit/other revenue, gross profit margin bridge, debtors book health & IFRS 9 ECL provisioning, "
            "store network capex and trading density, IFRS 16 lease liability structure, and cash conversion / dividend payout), "
            "citing specific notes, tables, and calculations."
        )
    else:
        md_lines.append(
            "2. **Detailed Forensic Reasoning & Determinations:** Step-by-step walkthrough of each key forensic junction "
            "(share count, net debt/cash, EBITDA adjustments, unit costs, capex trajectory, tax mechanics), "
            "citing specific notes, tables, and calculations."
        )

    md_lines.append("3. **Audit of Common Surface-Reading Pitfalls:** Contrast your findings against the common errors made by naive readers.")
    md_lines.append("4. **Final Forensic Verification Matrix:** A clean markdown summary table listing each Junction, the Raw Initial Claim, the Resolving Note/APM, and your Final Verified Determination.")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append(f"# THE SEQUENTIAL EXTRACTION & WORKING PAPER DOSSIER ({len(sections)} SECTIONS)")
    md_lines.append("")

    for sec in sections:
        sec_num = sec["section_number"] or "?"
        sec_id = sec["section_id"] or ""
        heading = sec["heading"] or ""
        subheading = sec["subheading"] or ""
        title = f"[{sec_id}] {heading}" if sec_id else heading
        if subheading:
            title += f" — {subheading}"

        md_lines.append("=" * 80)
        md_lines.append(f"## SECTION {sec_num}: {title}")
        md_lines.append("=" * 80)
        md_lines.append("")

        if sec["stored_questions_snapshot"] and sec["stored_questions_snapshot"].strip():
            md_lines.append("### [WORKING PAPER: OPEN QUESTIONS LEDGER AT THIS STAGE]")
            md_lines.append(sec["stored_questions_snapshot"].strip())
            md_lines.append("")

        if sec["selected_text"] and sec["selected_text"].strip():
            md_lines.append("### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]")
            md_lines.append(sec["selected_text"].strip())
            md_lines.append("")

        if sec["analyst_question"] and sec["analyst_question"].strip():
            md_lines.append("### [ANALYST QUERY / EMPHASIS]")
            md_lines.append(sec["analyst_question"].strip())
            md_lines.append("")

        if sec["llm_response"] and sec["llm_response"].strip():
            md_lines.append("### [SECTION READING RESPONSE / DETERMINATION]")
            md_lines.append(sec["llm_response"].strip())
            md_lines.append("")

    return "\n".join(md_lines)


def export_stage1_prompt(
    ticker: str,
    company_name: str | None = None,
    sector: str | None = None,
    report_sha: str | None = None,
    period: str | None = None,
    output_path: Path | None = None,
) -> Path:
    ticker = ticker.upper().strip()

    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database {DB_PATH} not found.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if not report_sha:
        latest = get_latest_report_sha(conn)
        if not latest:
            raise RuntimeError("No reports found in documents/analysis.sqlite.")
        report_sha, filename = latest
    else:
        row = cur.execute(
            "SELECT filename FROM reports WHERE sha256 = ?", (report_sha,)
        ).fetchone()
        filename = row["filename"] if row else "Company Report"

    # Resolve company directory and sector
    found = find_company_dir(ticker, sector=sector)
    if found:
        detected_sector, company_dir = found
    else:
        detected_sector = (sector or "mining").lower()
        company_dir = PROJECT_ROOT / f"companies/{detected_sector}/{ticker}"

    company_title = company_name or (f"{ticker} Group" if detected_sector == "retail" else f"{ticker} Resources")

    # Query all sections
    sections = cur.execute(
        """
        SELECT section_number, section_id, heading, subheading, analyst_question,
               selected_text, stored_questions_snapshot, llm_response
        FROM sections
        WHERE report_sha256 = ?
        ORDER BY section_number ASC, id ASC
        """,
        (report_sha,),
    ).fetchall()

    if not sections:
        raise RuntimeError(f"No sections captured for report SHA: {report_sha}")

    content = build_stage1_prompt_content(
        sections=sections,
        company_title=company_title,
        ticker=ticker,
        detected_sector=detected_sector,
        filename=filename,
    )

    if output_path is None:
        period_tag = period or "FY26"
        target_dir = company_dir / f"briefs/{period_tag}"
        target_dir.mkdir(parents=True, exist_ok=True)
        output_path = target_dir / f"{ticker}_{period_tag}_stage1_forensic_prompt.md"

    output_path.write_text(content, encoding="utf-8")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Export Stage 1 Cognitive Forensic Audit Prompt from SQLite.")
    parser.add_argument("ticker", help="Company ticker (e.g. PAN, HAR, LEW, TRU)")
    parser.add_argument("--sector", help="Company sector (mining, retail, finance, telcos)", default=None)
    parser.add_argument("--name", help="Full company name", default=None)
    parser.add_argument("--period", help="Financial period (e.g. FY26, FY27)", default="FY26")
    parser.add_argument("--sha", help="Specific report SHA-256 (defaults to latest)", default=None)
    parser.add_argument("--output", help="Custom output path", default=None)

    args = parser.parse_args()
    out = export_stage1_prompt(
        ticker=args.ticker.upper(),
        company_name=args.name,
        sector=args.sector,
        period=args.period.upper() if args.period else None,
        report_sha=args.sha,
        output_path=Path(args.output) if args.output else None,
    )
    print(f"Successfully generated Stage 1 Forensic Audit Prompt at: {out}")


if __name__ == "__main__":
    main()
