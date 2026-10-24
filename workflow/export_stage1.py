"""Script to compile sequential section extractions and question ledgers into a Stage 1 Forensic Audit Prompt.

Queries documents/analysis.sqlite and packages the full chronological working paper
dossier for the Auditing LLM to evaluate without an attached PDF.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sqlite3
import sys
import warnings

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from companies import find_company_dir
from companies.sectors import get_sector_config
from section_capture.db import KNOWN_COMPANIES

DB_PATH = Path("documents/analysis.sqlite")


def get_latest_report_sha(conn: sqlite3.Connection, ticker: str | None = None) -> tuple[str, str] | None:
    cur = conn.cursor()
    if ticker:
        # Prefer primary report for this ticker
        row = cur.execute(
            "SELECT sha256, filename FROM reports WHERE (original_path LIKE ? OR filename LIKE ?) AND parent_report_sha256 IS NULL ORDER BY updated_at DESC LIMIT 1",
            (f"%{ticker}%", f"%{ticker}%"),
        ).fetchone()
        if not row:
            row = cur.execute(
                "SELECT sha256, filename FROM reports WHERE original_path LIKE ? OR filename LIKE ? ORDER BY updated_at DESC LIMIT 1",
                (f"%{ticker}%", f"%{ticker}%"),
            ).fetchone()
        if row:
            return row[0], row[1]

    row = cur.execute(
        "SELECT sha256, filename FROM reports ORDER BY updated_at DESC LIMIT 1"
    ).fetchone()
    if row:
        return row[0], row[1]
    return None


def clean_reading_brief(text: str) -> str:
    """Strips the redundant Section 4 (Updated Open Questions Ledger) copy-paste block
    from intermediate section reading briefs when compiling the stage 1 cognitive prompt.
    Preserves all section observations, financial reconciliations, accounting notes,
    baseline forecast inputs, and red flags.
    """
    if not text:
        return ""
    # Matches "### 4. Updated Open Questions Ledger..." up to "### 5." or end of string
    cleaned = re.sub(
        r"(?ms)^#{1,4}\s*4\.\s*(?:Updated\s*)?Open Questions Ledger.*?(?=^#{1,4}\s*5\b|\Z)",
        "",
        text,
    )
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip()


def build_stage1_prompt_content(
    sections: list,
    company_title: str,
    ticker: str,
    detected_sector: str,
    filename: str,
    companion_reports: list[dict] | None = None,
    sens_reports: list[dict] | None = None,
    final_questions_ledger: str | None = None,
    compact: bool = True,
) -> str:
    """Constructs the Stage 1 Markdown prompt text from primary sections, companion annual reports (AFS), and SENS notices."""
    md_lines: list[str] = []
    comp_sec_count = sum(len(cr.get("sections", [])) for cr in (companion_reports or []))
    sens_sec_count = sum(len(sr.get("sections", [])) for sr in (sens_reports or []))
    total_sections = len(sections) + comp_sec_count + sens_sec_count

    md_lines.append("# STAGE 1: INDEPENDENT COGNITIVE AUDIT VIA SEQUENTIAL EXTRACTION & QUESTION LEDGER")
    md_lines.append(f"**Target Asset:** {company_title} ({ticker})  ")
    md_lines.append(f"**Sector:** {detected_sector.capitalize()}  ")
    md_lines.append(f"**Primary Document:** `{filename}` (Integrated Annual Report [IAR] — {len(sections)} sections)  ")
    if companion_reports:
        for cr in companion_reports:
            c_name = cr.get("filename")
            c_type = cr.get("doc_type", "afs").upper()
            c_cnt = len(cr.get("sections", []))
            md_lines.append(f"**Companion Financial Document:** `{c_name}` ({c_type} — {c_cnt} sections)  ")
    if sens_reports:
        sens_desc = ", ".join(
            f"`{sr.get('filename')}` ({sr.get('announcement_date') or 'SENS'}, {len(sr.get('sections', []))} sections)"
            for sr in sens_reports
        )
        md_lines.append(f"**Subsequent SENS Disclosures:** {len(sens_reports)} announcement(s) attached: {sens_desc}  ")
    md_lines.append(f"**Input Mode:** Sequential Forensic Working Paper & Dynamic Questions Ledger (No PDF Attached)  ")
    md_lines.append(f"**Task Directive:** Forensic Reasoning, Conflict Reconciliation & Post-Balance-Sheet Determinations (No Full Forward Valuation Model Required)")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("### INSTRUCTIONS FOR FORENSIC AUDITOR (LLM):")

    persona = get_sector_config(detected_sector).stage1_persona
    md_lines.append(
        f"You are acting as an independent **{persona}**. "
    )
    md_lines.append(
        f"You have been provided with the complete, chronological working paper compiled during a section-by-section "
        f"forensic capture of {company_title}'s financial disclosures ({total_sections} total sections across primary report and companion disclosures)."
    )

    md_lines.append("")
    md_lines.append("Notice how this working paper is constructed:")
    md_lines.append(
        "1. At each stage, specific text, accounting notes, APMs, and operational tables were extracted directly from the report."
    )
    md_lines.append(
        "2. Across the sections, an **Open Questions Ledger** evolved dynamically: anomalies and high-level management claims "
        "in early sections were flagged with priority levels, specific verification instructions, and carried forward as "
        "`Pending` until verified against primary financial statements, detailed accounting notes, and subsequent continuous disclosures."
    )
    if sens_reports:
        md_lines.append(
            "3. **Crucial Post-Year-End SENS Updates:** Material disclosures (Part 2) released subsequent to the financial year-end "
            "provide decisive evidence resolving or altering key pending questions from the Annual Report (e.g. debt facility execution/drawdown, "
            "cash runway, project development milestones, and operational permits)."
        )
    md_lines.append("")
    md_lines.append("**YOUR MANDATE:**")
    md_lines.append(
        "Review the sequential evidence trail below. Trace how the questions evolved from initial anomalies to audited reconciliation. "
        "**Do not produce a forward equity research forecast or valuation report.** Your role is **forensic reasoning only**: you must "
        "evaluate the working papers and independently reach your own definitive determinations on the core accounting, operational, "
        "and balance sheet junctions, explicitly factoring in subsequent SENS disclosures."
    )
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## REQUIRED STRUCTURE OF YOUR AUDIT REPORT")
    md_lines.append("")
    md_lines.append("Please format your response into the following four clear sections:")
    md_lines.append("1. **Executive Forensic Audit Summary:** Concise synthesis of the group's true economic performance, balance sheet health, post-balance-sheet liquidity runway, and key findings.")

    if detected_sector == "retail":
        md_lines.append(
            "2. **Detailed Forensic Reasoning & Determinations:** Step-by-step walkthrough of each key retail junction "
            "(merchandise vs credit/other revenue, gross profit margin bridge, debtors book health & IFRS 9 ECL provisioning, "
            "store network capex and trading density, IFRS 16 lease liability structure, post-year-end trading, and cash conversion / dividend payout), "
            "citing specific notes, tables, and calculations."
        )
    elif detected_sector == "reit":
        md_lines.append(
            "2. **Detailed Forensic Reasoning & Determinations:** Step-by-step walkthrough of each key REIT junction "
            "(reconciliation of IFRS profit to SA REIT distributable income/DIPS, contractual rental escalations vs renewal reversions, "
            "GLA vacancy dynamics across sub-sectors, nominal vs look-through LTV and ICR covenant headroom, "
            "interest rate hedging profile and debt maturity cliff, property fair value cap rates & discount rates, and dividend payout sustainability), "
            "citing specific notes, tables, and calculations."
        )
    elif detected_sector == "it":
        md_lines.append(
            "2. **Detailed Forensic Reasoning & Determinations:** Step-by-step walkthrough of each key technology junction "
            "(contract revenue mix across recurring ARR/managed services vs lumpy system integration/hardware resale, "
            "gross profit margin by line of business, direct technical headcount utilization and labor costs, "
            "contract assets / WIP unbilled revenue and deferred revenue recognition, capitalized software development & IP amortization, "
            "legacy dispute / litigation provisions & contingent liabilities, debt restructuring / deleveraging milestones, and FCFE conversion), "
            "citing specific notes, tables, and calculations."
        )
    elif detected_sector == "construction":
        md_lines.append(
            "2. **Detailed Forensic Reasoning & Determinations:** Step-by-step walkthrough of each key construction and infrastructure junction "
            "(percentage-of-completion [POC] revenue recognition & IFRS 15 timing, gross margin bridge across residential property development vs memorial parks vs infrastructure contracting, "
            "contract assets / unbilled WIP days vs contract liabilities & customer advances, retentions receivable and trade debtors aging/IFRS 9 ECL, "
            "joint ventures vs proportionately consolidated joint operations [e.g. BDC / Bankenveld District City], borrowing costs capitalised into construction assets, "
            "onerous contract provisions & performance guarantee/bonding facilities, DMTN corporate bond and bank debt covenant headroom, and cash tax vs deferred tax), "
            "citing specific notes, tables, and calculations."
        )
    elif detected_sector == "mining":
        md_lines.append(
            "2. **Detailed Forensic Reasoning & Determinations:** Step-by-step walkthrough of each key mining junction "
            "(diluted share count, net debt/cash & SOTP corporate adjustments, organic unit cash costs vs AISC, capex trajectory [sustaining vs growth], "
            "South African Section 36 capital expenditure deductions & Gold Mining Tax Formula curve, and post-year-end SENS financing milestones), "
            "citing specific notes, tables, and calculations."
        )
    elif detected_sector == "finance":
        md_lines.append(
            "2. **Detailed Forensic Reasoning & Determinations:** Step-by-step walkthrough of each key banking and financial services junction "
            "(net interest margin [NIM] vs credit impairment charges, stage 3 ECL coverage & non-performing loans [NPL], CET1 regulatory capital ratio & CAR, "
            "trading vs non-interest revenue, and Basel III liquidity coverage/NSFR ratios), citing specific notes, tables, and calculations."
        )
    elif detected_sector == "telcos":
        md_lines.append(
            "2. **Detailed Forensic Reasoning & Determinations:** Step-by-step walkthrough of each key telecommunications junction "
            "(service revenue vs device financing, ARPU trajectory & subscriber churn, tower lease commitments & IFRS 16 liabilities, "
            "spectrum auction capex vs network modernization capex, and foreign exchange remeasurement/hyperinflation adjustments), "
            "citing specific notes, tables, and calculations."
        )
    else:
        raise ValueError(
            f"Sector '{detected_sector}' does not have dedicated Stage 1 forensic audit rules implemented."
        )

    md_lines.append("3. **Audit of Common Surface-Reading Pitfalls:** Contrast your findings against the common errors made by naive readers.")
    md_lines.append("4. **Final Forensic Verification Matrix:** A clean markdown summary table listing each Junction, the Raw Initial Claim, the Resolving Note/SENS Announcement, and your Final Verified Determination.")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

    if compact:
        # Fallback to last stored_questions_snapshot if final_questions_ledger was not explicitly supplied
        effective_ledger = (final_questions_ledger or "").strip()
        if not effective_ledger:
            all_candidate_secs = list(sections)
            if companion_reports:
                for cr in companion_reports:
                    all_candidate_secs.extend(cr.get("sections", []))
            if sens_reports:
                for sr in sens_reports:
                    all_candidate_secs.extend(sr.get("sections", []))
            for sec in reversed(all_candidate_secs):
                snap = sec.get("stored_questions_snapshot") if isinstance(sec, dict) else sec["stored_questions_snapshot"]
                if snap and str(snap).strip():
                    effective_ledger = str(snap).strip()
                    break

        if effective_ledger:
            md_lines.append("## MASTER WORKING PAPER: CUMULATIVE OPEN QUESTIONS LEDGER")
            md_lines.append(
                "> **Cognitive Audit Anchor:** The authoritative ledger below consolidates all priority questions, "
                "forensic hypotheses, and cross-reference resolutions developed across the entire disclosure set. "
                "Use this ledger as your reference matrix when auditing the sequential section extractions that follow."
            )
            md_lines.append("")
            md_lines.append(effective_ledger)
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")

    def _render_sections(sec_list: list, prefix_title: str = ""):
        for sec in sec_list:
            sec_num = sec["section_number"] or "?"
            sec_id = sec["section_id"] or ""
            heading = sec["heading"] or ""
            subheading = sec["subheading"] or ""
            title = f"[{sec_id}] {heading}" if sec_id else heading
            if subheading:
                title += f" — {subheading}"

            md_lines.append("=" * 80)
            md_lines.append(f"## {prefix_title}SECTION {sec_num}: {title}")
            md_lines.append("=" * 80)
            md_lines.append("")

            if not compact:
                if sec["stored_questions_snapshot"] and str(sec["stored_questions_snapshot"]).strip():
                    md_lines.append("### [WORKING PAPER: OPEN QUESTIONS LEDGER AT THIS STAGE]")
                    md_lines.append(str(sec["stored_questions_snapshot"]).strip())
                    md_lines.append("")

            if sec["selected_text"] and str(sec["selected_text"]).strip():
                md_lines.append("### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]")
                md_lines.append(str(sec["selected_text"]).strip())
                md_lines.append("")

            if sec["analyst_question"] and str(sec["analyst_question"]).strip():
                md_lines.append("### [ANALYST QUERY / EMPHASIS]")
                md_lines.append(str(sec["analyst_question"]).strip())
                md_lines.append("")

            if sec["llm_response"] and str(sec["llm_response"]).strip():
                resp_text = str(sec["llm_response"]).strip()
                if compact:
                    resp_text = clean_reading_brief(resp_text)
                if resp_text:
                    md_lines.append("### [SECTION READING RESPONSE / DETERMINATION]")
                    md_lines.append(resp_text)
                    md_lines.append("")

    part_idx = 1
    if companion_reports or sens_reports:
        md_lines.append(f"# THE SEQUENTIAL EXTRACTION & WORKING PAPER DOSSIER ({total_sections} TOTAL SECTIONS)")
        md_lines.append("")
        md_lines.append("=" * 80)
        md_lines.append(f"## PART {part_idx}: PRIMARY FINANCIAL DISCLOSURE (`{filename}` — {len(sections)} Sections)")
        md_lines.append("=" * 80)
        md_lines.append("")
        _render_sections(sections, prefix_title=f"PART {part_idx} - ")
        part_idx += 1

        if companion_reports:
            for cr in companion_reports:
                c_file = cr.get("filename", "Financial Statements")
                c_type = cr.get("doc_type", "afs").upper()
                c_secs = cr.get("sections", [])
                md_lines.append("=" * 80)
                md_lines.append(f"## PART {part_idx}: {c_type} FINANCIAL STATEMENTS & NOTES (`{c_file}` — {len(c_secs)} Sections)")
                md_lines.append("=" * 80)
                md_lines.append("")
                _render_sections(c_secs, prefix_title=f"PART {part_idx} ({c_type}) - ")
                part_idx += 1

        if sens_reports:
            md_lines.append("=" * 80)
            md_lines.append(f"## PART {part_idx}: SUBSEQUENT SENS & CONTINUOUS DISCLOSURE ANNOUNCEMENTS ({len(sens_reports)} Announcements)")
            md_lines.append("=" * 80)
            md_lines.append("")

            for i, sr in enumerate(sens_reports, 1):
                s_file = sr.get("filename", "SENS Announcement")
                s_date = sr.get("announcement_date", "Post-Year-End")
                s_secs = sr.get("sections", [])
                md_lines.append("-" * 80)
                md_lines.append(f"### SENS ANNOUNCEMENT {i}: `{s_file}` (Date: {s_date} — {len(s_secs)} Sections)")
                md_lines.append("-" * 80)
                md_lines.append("")
                _render_sections(s_secs, prefix_title=f"SENS {i} - ")
    else:
        md_lines.append(f"# THE SEQUENTIAL EXTRACTION & WORKING PAPER DOSSIER ({len(sections)} SECTIONS)")
        md_lines.append("")
        _render_sections(sections)

    return "\n".join(md_lines)


def export_stage1_prompt(
    ticker: str,
    company_name: str | None = None,
    sector: str | None = None,
    report_sha: str | None = None,
    period: str | None = None,
    output_path: Path | None = None,
    compact: bool = True,
) -> Path:
    ticker = ticker.upper().strip()

    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database {DB_PATH} not found.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if not report_sha:
        latest = get_latest_report_sha(conn, ticker=ticker)
        if not latest:
            raise RuntimeError(f"No reports found in documents/analysis.sqlite for {ticker}.")
        report_sha, filename = latest
        row = cur.execute(
            "SELECT parent_report_sha256, filename, questions_ledger FROM reports WHERE sha256 = ?", (report_sha,)
        ).fetchone()
    else:
        row = cur.execute(
            "SELECT parent_report_sha256, filename, questions_ledger FROM reports WHERE sha256 = ?", (report_sha,)
        ).fetchone()
        filename = row["filename"] if row else "Company Report"

    final_questions_ledger = row["questions_ledger"] if row else None

    # If this is a SENS report pointing to a parent Annual Report, resolve parent as primary
    if row and row["parent_report_sha256"]:
        primary_sha = row["parent_report_sha256"]
        p_row = cur.execute("SELECT filename, questions_ledger FROM reports WHERE sha256 = ?", (primary_sha,)).fetchone()
        if p_row:
            filename = p_row["filename"]
            if p_row["questions_ledger"]:
                final_questions_ledger = p_row["questions_ledger"]
    else:
        primary_sha = report_sha

    # Resolve company directory and sector
    found = find_company_dir(ticker, sector=sector)
    if found:
        detected_sector, company_dir = found
    elif sector:
        detected_sector = sector.lower()
        company_dir = PROJECT_ROOT / f"companies/{detected_sector}/{ticker}"
    else:
        raise ValueError(
            f"Sector for company '{ticker}' could not be automatically detected and was not specified."
        )

    company_title = company_name or KNOWN_COMPANIES.get(ticker, (f"{ticker} Group", detected_sector))[0]

    # Query primary sections
    sections = cur.execute(
        """
        SELECT section_number, section_id, heading, subheading, analyst_question,
               selected_text, stored_questions_snapshot, llm_response
        FROM sections
        WHERE report_sha256 = ?
        ORDER BY section_number ASC, id ASC
        """,
        (primary_sha,),
    ).fetchall()

    # Query companion reports (AFS, Presentation) linked to primary report
    comp_rows = cur.execute(
        """
        SELECT sha256, filename, doc_type
        FROM reports
        WHERE parent_report_sha256 = ? AND doc_type IN ('afs', 'presentation')
        ORDER BY created_at ASC
        """,
        (primary_sha,),
    ).fetchall()

    companion_reports: list[dict] = []
    for cr in comp_rows:
        c_sections = cur.execute(
            """
            SELECT section_number, section_id, heading, subheading, analyst_question,
                   selected_text, stored_questions_snapshot, llm_response
            FROM sections
            WHERE report_sha256 = ?
            ORDER BY section_number ASC, id ASC
            """,
            (cr["sha256"],),
        ).fetchall()
        if c_sections:
            companion_reports.append({
                "sha256": cr["sha256"],
                "filename": cr["filename"],
                "doc_type": cr["doc_type"],
                "sections": c_sections,
            })

    # Query linked SENS notices
    sens_rows = cur.execute(
        """
        SELECT sha256, filename, announcement_date
        FROM reports
        WHERE parent_report_sha256 = ? AND doc_type = 'sens'
        ORDER BY COALESCE(announcement_date, '9999-99-99') ASC, created_at ASC
        """,
        (primary_sha,),
    ).fetchall()

    sens_reports: list[dict] = []
    for sr in sens_rows:
        s_sections = cur.execute(
            """
            SELECT section_number, section_id, heading, subheading, analyst_question,
                   selected_text, stored_questions_snapshot, llm_response
            FROM sections
            WHERE report_sha256 = ?
            ORDER BY section_number ASC, id ASC
            """,
            (sr["sha256"],),
        ).fetchall()
        if s_sections:
            sens_reports.append({
                "sha256": sr["sha256"],
                "filename": sr["filename"],
                "announcement_date": sr["announcement_date"],
                "sections": s_sections,
            })

    total_secs = len(sections) + sum(len(cr["sections"]) for cr in companion_reports) + sum(len(sr["sections"]) for sr in sens_reports)
    if total_secs == 0:
        raise RuntimeError(f"No sections captured for report SHA: {primary_sha}")

    content = build_stage1_prompt_content(
        sections=sections,
        company_title=company_title,
        ticker=ticker,
        detected_sector=detected_sector,
        filename=filename,
        companion_reports=companion_reports if companion_reports else None,
        sens_reports=sens_reports if sens_reports else None,
        final_questions_ledger=final_questions_ledger,
        compact=compact,
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
    parser.add_argument("ticker", help="Company ticker (e.g. PAN, HAR, LEW, TRU, CGR)")
    parser.add_argument("--sector", help="Company sector (mining, retail, finance, telcos, construction, it, reit)", default=None)
    parser.add_argument("--name", help="Full company name", default=None)
    parser.add_argument("--period", help="Financial period (e.g. FY26, FY27)", default="FY26")
    parser.add_argument("--sha", help="Specific report SHA-256 (defaults to latest)", default=None)
    parser.add_argument("--output", help="Custom output path", default=None)
    parser.add_argument("--full", action="store_true", help="Generate uncompacted prompt retaining intermediate copy-paste ledgers and snapshots")

    args = parser.parse_args()
    out = export_stage1_prompt(
        ticker=args.ticker.upper(),
        company_name=args.name,
        sector=args.sector,
        period=args.period.upper() if args.period else None,
        report_sha=args.sha,
        output_path=Path(args.output) if args.output else None,
        compact=not args.full,
    )
    print(f"Successfully generated Stage 1 Forensic Audit Prompt at: {out}")


if __name__ == "__main__":
    main()
