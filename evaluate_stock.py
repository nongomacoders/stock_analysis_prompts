"""Automated Stock Valuation Evaluator & Autonomous Rerun Engine.

Standardizes forensic auditing of company valuation notes across JSE tickers.
Provides both a Python API (StockEvaluator) and a CLI interface.

Usage:
    python evaluate_stock.py <TICKER> [--period <PERIOD>] [--rerun] [--json] [--db <PATH>]
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import sys
import time
from typing import Any

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Safe Windows stdout utf-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from companies import find_company_dir
from companies.sectors import (
    get_jse_sector_code,
    get_jse_sector_name,
)
from section_capture.db import (
    connect_db,
    get_sector_guardrails,
    parse_valuation_summary,
    resolve_db_path,
    save_stage2_report,
    validate_and_repair_rating_bands,
)
from section_capture.market_data import fetch_jse_quote
from section_capture.openrouter import (
    get_openrouter_api_key,
    get_openrouter_model,
    query_openrouter,
)
from workflow.generate_stage2 import (
    build_stage2_prompt_content,
    sanitize_stage2_valuation_markdown,
)


class StockEvaluator:
    """Evaluates company Stage 2 valuation notes and provides autonomous rerun capability."""

    def __init__(
        self,
        ticker: str,
        period: str | None = None,
        db_path: str | Path | None = None,
    ) -> None:
        self.ticker = ticker.strip().upper()
        self.specified_period = period.strip().upper() if period else None
        self.db_path = resolve_db_path(db_path)

        # Discovered metadata
        self.sector, self.comp_dir = find_company_dir(self.ticker)
        if not self.comp_dir or not self.comp_dir.exists():
            raise FileNotFoundError(f"Company directory for ticker '{self.ticker}' not found.")

        self.period = self._resolve_period()
        self.briefs_dir = self.comp_dir / "briefs" / self.period
        self.s1_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage1_audit_response.md"
        self.s2_note_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage2_valuation_note.md"
        self.s2_prompt_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage2_valuation_prompt.md"

    def _resolve_period(self) -> str:
        """Determines active reporting period if not explicitly specified."""
        if self.specified_period:
            return self.specified_period

        # 1. Check briefs subdirectories
        briefs_base = self.comp_dir / "briefs"
        if briefs_base.exists():
            periods = [p.name for p in briefs_base.iterdir() if p.is_dir() and not p.name.startswith(".")]
            if periods:
                # Prefer latest periods like FY26, 1H26
                periods.sort(reverse=True)
                return periods[0]

        # 2. Check SQLite reports table
        if self.db_path.exists():
            with connect_db(self.db_path) as conn:
                row = conn.execute(
                    "SELECT period FROM reports WHERE original_path LIKE ? OR filename LIKE ? ORDER BY created_at DESC LIMIT 1",
                    (f"%{self.ticker}%", f"%{self.ticker}%"),
                ).fetchone()
                if row and row["period"]:
                    return row["period"]

        # Default fallback
        return "FY26"

    def discover_documents(self) -> dict[str, list[Path]]:
        """Discovers active and completed source PDFs and SENS notices."""
        sources_dir = self.comp_dir / "sources"
        active_pdfs = sorted(f for f in sources_dir.glob("*.pdf") if f.is_file() and "sens" not in f.name.lower())
        completed_pdfs = sorted((sources_dir / "completed" / self.period).glob("*.pdf")) if (sources_dir / "completed" / self.period).exists() else []

        sens_dir = sources_dir / "sens"
        active_sens = sorted(f for f in sens_dir.glob("*") if f.is_file() and f.suffix.lower() in {".pdf", ".txt", ".md"} and f.name.lower() != "readme.md") if sens_dir.exists() else []
        completed_sens = sorted((sens_dir / "completed").glob("*")) if (sens_dir / "completed").exists() else []

        return {
            "active_pdfs": active_pdfs,
            "completed_pdfs": completed_pdfs,
            "active_sens": active_sens,
            "completed_sens": completed_sens,
        }

    def fetch_market_quote(self) -> dict[str, Any]:
        """Fetches live JSE closing quote via Yahoo Finance, with cached fallback."""
        quote = fetch_jse_quote(self.ticker)
        if quote and quote.get("price_zar") is not None:
            return quote

        # Fallback to DB cached reference price
        if self.db_path.exists():
            with connect_db(self.db_path) as conn:
                row = conn.execute(
                    "SELECT reference_price_zar FROM reports WHERE original_path LIKE ? OR filename LIKE ? ORDER BY created_at DESC LIMIT 1",
                    (f"%{self.ticker}%", f"%{self.ticker}%"),
                ).fetchone()
                if row and row["reference_price_zar"] is not None:
                    return {
                        "ticker": self.ticker,
                        "symbol": f"{self.ticker}.JO",
                        "price_zar": float(row["reference_price_zar"]),
                        "is_cached_fallback": True,
                    }

        return {"ticker": self.ticker, "symbol": f"{self.ticker}.JO", "price_zar": None}

    def audit(self) -> dict[str, Any]:
        """Runs comprehensive forensic audit on the existing Stage 2 valuation note."""
        quote = self.fetch_market_quote()
        live_price = quote.get("price_zar")

        if not self.s2_note_file.exists():
            return {
                "status": "MISSING_NOTE",
                "ticker": self.ticker,
                "period": self.period,
                "sector": self.sector,
                "live_price_zar": live_price,
                "error": f"Valuation note not found at {self.s2_note_file}",
                "checks": {},
            }

        note_content = self.s2_note_file.read_text(encoding="utf-8")
        parsed_summary = parse_valuation_summary(note_content) or {}

        # 1. Parse JSON root block directly
        json_meta = {}
        m_json = re.search(r"```json\s*(\{.*?\})\s*```", note_content, re.DOTALL)
        if m_json:
            try:
                json_meta = json.loads(m_json.group(1))
            except Exception:
                pass

        target_price = json_meta.get("target_price_zar") or parsed_summary.get("target_price")
        ref_price = json_meta.get("reference_price_zar") or parsed_summary.get("reference_price")
        static_rec = (json_meta.get("recommendation") or parsed_summary.get("recommendation") or "HOLD").upper()
        div_yield = json_meta.get("forward_dividend_yield_pct") or parsed_summary.get("dividend_yield_pct") or 0.0

        raw_bands = json_meta.get("rating_bands") or parsed_summary.get("rating_bands")

        # Check 1: CHK-PRICE-SYNC
        price_check = {"passed": True, "details": []}
        live_upside_pct = None
        live_tsr_pct = None
        if target_price and live_price:
            live_upside_pct = round(((target_price - live_price) / live_price) * 100, 1)
            live_tsr_pct = round(live_upside_pct + (div_yield or 0.0), 1)
            if ref_price:
                diff_pct = abs(live_price - ref_price) / ref_price * 100
                if diff_pct > 5.0:
                    price_check["details"].append(
                        f"Live price R{live_price:.2f} differs by {diff_pct:.1f}% from note reference price R{ref_price:.2f}."
                    )
        else:
            price_check["passed"] = False
            price_check["details"].append("Missing target price or live price.")

        # Check 2: CHK-BANDS-MONO
        bands_check = {"passed": True, "details": []}
        dynamic_rec = static_rec
        if raw_bands:
            sb = raw_bands.get("strong_buy_max_zar")
            b = raw_bands.get("buy_max_zar")
            h = raw_bands.get("hold_max_zar")
            s = raw_bands.get("sell_max_zar")
            ss = raw_bands.get("strong_sell_above_zar")

            if sb is not None and b is not None and h is not None and s is not None and ss is not None:
                if not (float(sb) < float(b) < float(h) < float(s) <= float(ss)):
                    bands_check["passed"] = False
                    bands_check["details"].append(
                        f"Non-monotonic rating bands: SB={sb}, B={b}, H={h}, S={s}, SS={ss}"
                    )

            rating_bands = validate_and_repair_rating_bands(raw_bands, target_price=target_price) if target_price else {}

            if live_price is not None and rating_bands:
                r_sb = rating_bands.get("strong_buy_max_zar")
                r_b = rating_bands.get("buy_max_zar")
                r_h = rating_bands.get("hold_max_zar")
                r_s = rating_bands.get("sell_max_zar")
                if r_sb is not None and live_price <= r_sb:
                    dynamic_rec = "STRONG BUY"
                elif r_b is not None and live_price <= r_b:
                    dynamic_rec = "BUY"
                elif r_h is not None and live_price <= r_h:
                    dynamic_rec = "HOLD"
                elif r_s is not None and live_price <= r_s:
                    dynamic_rec = "SELL"
                else:
                    dynamic_rec = "STRONG SELL"

            if dynamic_rec != static_rec:
                bands_check["details"].append(
                    f"Dynamic rating at live price ({dynamic_rec}) diverges from static note rating ({static_rec})."
                )
        else:
            rating_bands = validate_and_repair_rating_bands({}, target_price=target_price) if target_price else {}
            bands_check["passed"] = False
            bands_check["details"].append("Rating bands missing from note metadata.")

        # Check 3: CHK-SOTP-MATH
        sotp_check = {"passed": True, "details": []}
        # Look for obvious arithmetic hallucinations in Section 4
        blend_match = re.search(r"\(\s*0\.\d+\s*\*\s*[\d\.]+\s*\)\s*\+\s*\(\s*0\.\d+\s*\*\s*[\d\.]+\s*\)[^=\n]*=\s*(?:ZAR\s*|R\s*)?([\d\.]+)", note_content)
        if blend_match:
            stated_str = blend_match.group(1).rstrip(".")
            try:
                stated_res = float(stated_str)
                formula_str = blend_match.group(0).split("=")[0]
                clean_formula = re.sub(r"[^0-9\+\*\.\(\)\s]", "", formula_str)
                calc_res = eval(clean_formula)
                if abs(calc_res - stated_res) > 0.5:
                    sotp_check["passed"] = False
                    sotp_check["details"].append(
                        f"Blend formula hallucination: {formula_str.strip()} calculates to {calc_res:.2f}, but note states {stated_res:.2f}."
                    )
            except Exception:
                pass

        # Check 4: CHK-GUARDRAILS
        guardrails = get_sector_guardrails(self.sector, db_path=self.db_path)
        guardrail_check = {"passed": True, "active_count": len(guardrails), "details": []}
        # Check specific sector assertions
        if self.sector == "mining":
            if "Section 36" not in note_content and "Sec 36" not in note_content:
                guardrail_check["details"].append("Note does not explicitly cite Section 36 capital allowance tax shields.")
        elif self.sector == "retail":
            if "headlease" in note_content.lower() and "sublease" not in note_content.lower():
                guardrail_check["details"].append("Retail note mentions headlease without sublease netting analysis.")

        # Check 5: CHK-TEXT-CLEAN
        text_check = {"passed": True, "details": []}
        if "<br>" in note_content or "<br/>" in note_content or "<span>" in note_content:
            text_check["passed"] = False
            text_check["details"].append("Illegal HTML tags (<br>, <span>) found in markdown.")

        # Check for unparsed placeholders
        if "[+/-0.0]%" in note_content or "R[0.00]" in note_content:
            text_check["passed"] = False
            text_check["details"].append("Unparsed template placeholders found in note.")

        # Check for token repetition glitch (e.g. word repetitions of 4+ times)
        token_stutter = re.search(r"\b(\w{3,})\b(?:\s+\1){3,}", note_content, re.IGNORECASE)
        if token_stutter:
            text_check["passed"] = False
            text_check["details"].append(f"Token sampling stutter detected: '{token_stutter.group(0)}'")

        overall_passed = all([
            price_check["passed"],
            bands_check["passed"],
            sotp_check["passed"],
            guardrail_check["passed"],
            text_check["passed"],
        ])

        return {
            "status": "PASSED" if overall_passed else "WARNINGS_FOUND",
            "ticker": self.ticker,
            "period": self.period,
            "sector": self.sector,
            "live_price_zar": live_price,
            "reference_price_zar": ref_price,
            "target_price_zar": target_price,
            "static_recommendation": static_rec,
            "dynamic_recommendation": dynamic_rec,
            "implied_upside_pct": live_upside_pct if live_upside_pct is not None else parsed_summary.get("upside_pct"),
            "dividend_yield_pct": div_yield,
            "projected_12m_tsr_pct": live_tsr_pct if live_tsr_pct is not None else parsed_summary.get("tsr_pct"),
            "rating_bands": rating_bands,
            "checks": {
                "CHK-PRICE-SYNC": price_check,
                "CHK-BANDS-MONO": bands_check,
                "CHK-SOTP-MATH": sotp_check,
                "CHK-GUARDRAILS": guardrail_check,
                "CHK-TEXT-CLEAN": text_check,
            },
        }

    def rerun(self) -> dict[str, Any]:
        """Assembles dossier, calls OpenRouter DeepSeek Flash, updates SQLite, and re-audits."""
        import pypdfium2 as pdfium

        # 1. Verify Stage 1 exists
        if not self.s1_file.exists():
            raise FileNotFoundError(f"Cannot rerun Stage 2: Stage 1 Forensic Audit missing at {self.s1_file}")

        s1_text = self.s1_file.read_text(encoding="utf-8")

        # 2. Get verified live market price
        quote = self.fetch_market_quote()
        ref_price = quote.get("price_zar")
        if ref_price is None:
            raise RuntimeError(f"Verified live JSE closing price required for {self.ticker}. Could not fetch quote.")

        # 3. Discover source documents
        docs = self.discover_documents()
        all_pdfs = docs["active_pdfs"] or docs["completed_pdfs"]
        if not all_pdfs:
            raise FileNotFoundError(f"No source PDFs found for {self.ticker} in sources/ or completed/")

        all_sens = docs["active_sens"] + docs["completed_sens"]

        source_documents_meta: list[dict[str, Any]] = []
        all_pdf_blocks: list[str] = []

        for pdf_p in all_pdfs:
            doc = pdfium.PdfDocument(str(pdf_p))
            page_count = len(doc)
            pages_txt = [
                f"--- [{pdf_p.name} | Page {i + 1} of {page_count}] ---\n"
                + page.get_textpage().get_text_range().strip()
                for i, page in enumerate(doc)
            ]
            doc.close()

            source_documents_meta.append({
                "filename": pdf_p.name,
                "doc_type": "annual_report",
                "badge": "[AR]",
                "page_count": page_count,
                "period": self.period,
                "is_sens": False,
            })
            all_pdf_blocks.append(
                f"## SOURCE DISCLOSURE FILE: {pdf_p.name} ({page_count} Pages)\n\n"
                + "\n\n".join(pages_txt)
            )

        sens_blocks: list[str] = []
        sens_labels: list[str] = []
        for sf in all_sens:
            sens_labels.append(f"`{sf.name}`")
            source_documents_meta.append({
                "filename": sf.name,
                "doc_type": "sens",
                "badge": "[SENS]",
                "page_count": 1,
                "is_sens": True,
            })
            if sf.suffix.lower() == ".pdf":
                doc_s = pdfium.PdfDocument(str(sf))
                s_pages = [page.get_textpage().get_text_range().strip() for page in doc_s]
                doc_s.close()
                sens_blocks.append(f"### SENS ANNOUNCEMENT (PDF): {sf.name}\n\n" + "\n\n".join(s_pages))
            else:
                sens_blocks.append(f"### SENS ANNOUNCEMENT: {sf.name}\n\n{sf.read_text(encoding='utf-8').strip()}")

        company_title = self.ticker
        if self.db_path.exists():
            with connect_db(self.db_path) as conn:
                r = conn.execute("SELECT filename FROM reports WHERE original_path LIKE ? LIMIT 1", (f"%{self.ticker}%",)).fetchone()
                if r:
                    company_title = r["filename"].replace(".pdf", "").replace("-", " ")

        base_s2_prompt = build_stage2_prompt_content(
            stage1_content=s1_text,
            company_title=company_title,
            ticker=self.ticker,
            detected_sector=self.sector,
            sens_announcements=sens_labels if sens_labels else None,
            reference_price_zar=ref_price,
            source_documents=source_documents_meta,
            db_path=self.db_path,
        )

        dossier_parts = [base_s2_prompt]
        if sens_blocks:
            dossier_parts.append("# SUBSEQUENT SENS ANNOUNCEMENTS\n\n" + "\n\n---\n\n".join(sens_blocks))
        dossier_parts.append(
            "# COMPLETE PRIMARY SOURCE FINANCIAL REPORT DISCLOSURES & AUDITED NOTES\n"
            + "\n\n---\n\n".join(all_pdf_blocks)
        )
        full_dossier = "\n\n---\n\n".join(dossier_parts)

        # Write prompt
        self.briefs_dir.mkdir(parents=True, exist_ok=True)
        self.s2_prompt_file.write_text(base_s2_prompt, encoding="utf-8")

        # 4. Query OpenRouter
        model = get_openrouter_model()
        response = query_openrouter(full_dossier, model=model, timeout=300, max_tokens=16384)

        # 5. Sanitize and save
        sanitized_md = sanitize_stage2_valuation_markdown(response)
        self.s2_note_file.write_text(sanitized_md, encoding="utf-8")

        # 6. Save to SQLite
        primary_sha = None
        if self.db_path.exists():
            with connect_db(self.db_path) as conn:
                # Prioritize top-level primary report (parent_report_sha256 IS NULL)
                r = conn.execute(
                    """
                    SELECT sha256 FROM reports 
                    WHERE (original_path LIKE ? OR filename LIKE ?) AND parent_report_sha256 IS NULL
                    ORDER BY created_at DESC LIMIT 1
                    """,
                    (f"%{self.ticker}%", f"%{self.ticker}%"),
                ).fetchone()
                if not r:
                    r = conn.execute(
                        "SELECT sha256 FROM reports WHERE original_path LIKE ? OR filename LIKE ? ORDER BY created_at DESC LIMIT 1",
                        (f"%{self.ticker}%", f"%{self.ticker}%"),
                    ).fetchone()
                if r:
                    primary_sha = r["sha256"]

        if primary_sha is None and all_pdfs:
            import hashlib
            primary_sha = hashlib.sha256(all_pdfs[0].read_bytes()).hexdigest()

        if primary_sha:
            save_stage2_report(primary_sha, prompt=base_s2_prompt, response=sanitized_md, db_path=self.db_path)

        # 7. Archive active PDFs
        archive_dir = self.comp_dir / "sources" / "completed" / self.period
        archive_dir.mkdir(parents=True, exist_ok=True)
        for pdf_p in docs["active_pdfs"]:
            shutil.copy2(pdf_p, archive_dir / pdf_p.name)
            try:
                pdf_p.unlink()
            except Exception:
                pass

        # 8. Re-audit and return result
        return self.audit()

    def format_markdown(self, result: dict[str, Any]) -> str:
        """Formats the evaluation result into a publication-grade Markdown scorecard."""
        if result.get("status") == "MISSING_NOTE":
            return (
                f"### {self.ticker} Evaluation Scorecard\n\n"
                f"❌ **Valuation Note Not Found** for reporting period `{result.get('period')}`.\n"
                f"Path: `{self.s2_note_file}`\n\n"
                f"Use `--rerun` to generate Stage 2 from existing Stage 1 audit."
            )

        status_emoji = "✓" if result.get("status") == "PASSED" else "⚠️"
        live_price = result.get("live_price_zar")
        ref_price = result.get("reference_price_zar")
        target_price = result.get("target_price_zar")
        static_rec = result.get("static_recommendation")
        dyn_rec = result.get("dynamic_recommendation")
        upside = result.get("implied_upside_pct")
        div_y = result.get("dividend_yield_pct")
        tsr = result.get("projected_12m_tsr_pct")
        bands = result.get("rating_bands") or {}

        bands_str = (
            f"Strong Buy ≤ R{bands.get('strong_buy_max_zar', 0):.2f} | "
            f"Buy ≤ R{bands.get('buy_max_zar', 0):.2f} | "
            f"Hold ≤ R{bands.get('hold_max_zar', 0):.2f} | "
            f"Sell ≤ R{bands.get('sell_max_zar', 0):.2f} | "
            f"Strong Sell > R{bands.get('strong_sell_above_zar', 0):.2f}"
            if bands
            else "Missing"
        )

        md = [
            f"### {self.ticker} — Institutional Valuation Scorecard ({result.get('period')})",
            "",
            f"**Audit Status:** {status_emoji} `{result.get('status')}` &nbsp;|&nbsp; "
            f"**Sector:** `{result.get('sector', '').upper()}` &nbsp;|&nbsp; "
            f"**Dynamic Rating:** **`{dyn_rec}`**",
            "",
            "| Metric | Valuation Determination | Live Market Comparison & Basis |",
            "| :--- | :---: | :--- |",
            f"| **Live JSE Price (`{self.ticker}.JO`)** | **R{live_price:.2f}** | Sourced via live market data feed |" if live_price else "| **Live JSE Price** | — | Market quote unavailable |",
            f"| **Note Reference Price** | R{ref_price:.2f} | Baseline reference price in valuation note |" if ref_price else "| **Note Reference Price** | — | — |",
            f"| **12-Month Target Price** | **R{target_price:.2f}** | Institutional valuation target |" if target_price else "| **12-Month Target Price** | — | — |",
            f"| **Live Implied Upside** | **{upside:+.1f}%** | Relative to live price R{live_price:.2f} |" if upside is not None and live_price else "| **Live Implied Upside** | — | — |",
            f"| **Forward Dividend Yield** | {div_y:.1f}% | 12-month forward cash distribution yield |" if div_y is not None else "| **Forward Dividend Yield** | — | — |",
            f"| **12-Month Expected TSR** | **{tsr:+.1f}%** | Capital upside + forward dividend yield |" if tsr is not None else "| **12-Month Expected TSR** | — | — |",
            f"| **Recommendation** | **`{dyn_rec}`** | Note static: `{static_rec}` (Bands: {dyn_rec}) |",
            f"| **Dynamic Rating Bands** | {bands_str} | Strictly monotonic ZAR thresholds |",
            "",
            "#### Forensic Audit Checks",
            "| Check Code | Check Description | Result | Details / Observations |",
            "| :--- | :--- | :---: | :--- |",
        ]

        check_descs = {
            "CHK-PRICE-SYNC": "Market Price & Upside Alignment",
            "CHK-BANDS-MONO": "Rating Bands Monotonicity",
            "CHK-SOTP-MATH": "SOTP Vertical Arithmetic & Sign Integrity",
            "CHK-GUARDRAILS": "Active Sector Guardrails Compliance",
            "CHK-TEXT-CLEAN": "LLM Stutter & Format Cleanliness",
        }

        for code, data in result.get("checks", {}).items():
            c_res = "✓ PASS" if data.get("passed") else "⚠️ FLAG"
            details = "; ".join(data.get("details", [])) or "All checks passed cleanly."
            desc = check_descs.get(code, code)
            md.append(f"| **`{code}`** | {desc} | **{c_res}** | {details} |")

        return "\n".join(md)


def main() -> None:
    parser = argparse.ArgumentParser(description="Automated Stock Valuation Evaluator & Autonomous Rerun Engine")
    parser.add_argument("ticker", help="Company JSE ticker symbol (e.g. PAN, SSK, CGR, SPP)")
    parser.add_argument("--period", help="Reporting period override (e.g. FY26, 1H26)")
    parser.add_argument("--rerun", action="store_true", help="Execute autonomous Stage 2 valuation rerun before audit")
    parser.add_argument("--json", action="store_true", help="Output raw JSON evaluation result")
    parser.add_argument("--db", help="Path to SQLite analysis database")

    args = parser.parse_args()

    evaluator = StockEvaluator(ticker=args.ticker, period=args.period, db_path=args.db)

    if args.rerun:
        res = evaluator.rerun()
    else:
        res = evaluator.audit()

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(evaluator.format_markdown(res))


if __name__ == "__main__":
    main()
