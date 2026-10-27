"""Unit and integration tests for Stage 2 Valuation summary extraction,

SQLite persistence, and Portfolio Coverage Dashboard GUI.
"""

from __future__ import annotations

import json
from pathlib import Path
import sqlite3
import pytest

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from section_capture.db import (
    connect_db,
    detect_company_meta,
    get_analyzed_stocks,
    get_stage2_report,
    parse_valuation_summary,
    save_stage2_report,
    upsert_report,
)
from section_capture.portfolio_view import (
    PortfolioCoverageDialog,
    PortfolioView,
    normalize_markdown_for_qt,
)


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    return app


def test_parse_valuation_summary_lewis():
    """Verify parsing of actual Lewis Stage 2 Valuation Note."""
    lewis_note_path = Path("companies/retail/LEW/briefs/FY26/LEW_FY26_stage2_valuation_note.md")
    assert lewis_note_path.exists(), "Lewis Stage 2 valuation note must exist"

    text = lewis_note_path.read_text(encoding="utf-8")
    summary = parse_valuation_summary(text)

    assert summary.get("target_price") == 95.00
    assert summary.get("reference_price") == 90.19
    assert summary.get("recommendation") == "HOLD"
    assert round(summary.get("upside_pct", 0), 2) == 5.33
    assert round(summary.get("dividend_yield_pct", 0), 2) == 9.44
    assert round(summary.get("tsr_pct", 0), 2) == 14.77
    assert summary.get("sector") == "retail"

    triggers = summary.get("monitoring_triggers", "")
    assert "Collection Rate" in triggers
    assert "Gross Margin" in triggers
    assert "Speciality Segment Turnaround" in triggers


def test_parse_valuation_summary_standardized_format():
    """Verify parsing against the standardized Section 1 Summary Card and Section 6 Triggers."""
    simulated_note = """
# STAGE 2: INSTITUTIONAL 2-YEAR VALUATION & FORECAST NOTE

## 1. Executive Investment Thesis & 12-Month JSE Price Target (ZAR/share)

* **Sector:** Mining (Gold)
* **Current Reference Share Price:** R14.50 (1,450 ZAR cents)
* **12-Month JSE Target Price:** **R22.00** (2,200 ZAR cents)
* **Implied Capital Upside:** +51.7%
* **Forward Dividend Yield (FY27E):** +8.5%
* **Projected 12-Month Total Shareholder Return (TSR):** **+60.2%**
* **Institutional Recommendation:** **BUY**

### Core Investment Thesis
Pan African Resources is poised for significant FCF inflection.

## 6. Actionable Portfolio Monitoring Triggers & Catalysts ('What to Watch For That Will Move the Stock')

1. **MTR Commissioning (October 2026):** Track steady-state throughput of 800ktpm.
2. **AISC Cost Ceiling:** AISC must remain below $1,450/oz to protect 45% EBITDA margins.
3. **Capex Cliff Inflection:** Sustaining capex drops from $110m to $42m from FY28E.
"""
    summary = parse_valuation_summary(simulated_note)

    assert summary.get("target_price") == 22.00
    assert summary.get("reference_price") == 14.50
    assert summary.get("recommendation") == "BUY"
    assert summary.get("upside_pct") == 51.7
    assert summary.get("dividend_yield_pct") == 8.5
    assert summary.get("tsr_pct") == 60.2
    assert summary.get("sector") == "mining"

    triggers = summary.get("monitoring_triggers", "")
    assert "MTR Commissioning" in triggers
    assert "AISC Cost Ceiling" in triggers
    assert "Capex Cliff Inflection" in triggers


def test_parse_valuation_summary_markdown_table_format():
    """Verify parsing when Executive Valuation Summary Card is rendered as a Markdown table (e.g. Orion Minerals)."""
    table_note = """
# ORION MINERALS LIMITED (JSE: ORN | ASX: ORN)

## 1. Executive Investment Thesis & 12-Month JSE Price Target (ZAR/Share)

### Executive Valuation Summary Card

| Valuation & Market Metric | Institutional Determination | Basis / Reference Source |
| --- | --- | --- |
| **Sector** | Base Metals Mining & Development (Cu-Zn) | JSE Basic Materials / ASX Metals & Mining |
| **Current Reference Share Price (JSE / ASX)** | **R0.28 / share** (**28.4 ZAR cents**) | A$0.025 | 30 June 2026 Closing Price |
| **12-Month JSE Target Price (Risked SOTP)** | **R0.21 / share** (**21.0 ZAR cents**) | A$0.0185 | Risked Attributable SOTP NAV |
| **Implied Capital Upside / (Downside)** | **-26.1%** | Relative to R0.284 reference price |
| **Forward Dividend Yield (FY27E & FY28E)** | **0.0%** | Pre-production / peak capital deployment phase |
| **Projected 12-Month Total Shareholder Return (TSR)** | **-26.1%** | Pure capital return |
| **Institutional Recommendation** | **SELL (HIGH RISK / DILUTION OVERHANG)** | Material going-concern cash shortfall |

## 6. Actionable Portfolio Monitoring Triggers & Catalysts ('What to Watch For')
- **Glencore Offtake & Prepayment Facility Drawdown Hurdles**
"""
    summary = parse_valuation_summary(table_note)
    assert summary.get("target_price") == 0.21
    assert summary.get("reference_price") == 0.28
    assert summary.get("recommendation") == "SELL"
    assert summary.get("upside_pct") == -26.1
    assert summary.get("dividend_yield_pct") == 0.0
    assert summary.get("tsr_pct") == -26.1
    assert "Glencore Offtake" in summary.get("monitoring_triggers", "")
    assert summary.get("sector") == "mining"


def test_parse_valuation_summary_json_format():
    """Verify parsing when Section 1 begins with a standardized JSON summary block."""
    json_note = """
# ACCELERATE PROPERTY FUND LIMITED (JSE: APF)

## 1. Executive Investment Thesis & 12-Month JSE Price Target (ZAR/Share)

```json
{
  "ticker": "APF",
  "company_name": "Accelerate Property Fund Limited",
  "sector": "reit",
  "recommendation": "SELL",
  "reference_price_zar": 0.60,
  "target_price_zar": 0.42,
  "implied_upside_pct": -30.0,
  "forward_dividend_yield_pct": 0.0,
  "projected_12m_tsr_pct": -30.0,
  "monitoring_triggers": [
    "KPMG Crescent formal lease exit April 2027",
    "Competition Commission RMA approval",
    "Flanagan & Gerard asset manager shareholder approval"
  ]
}
```

### Executive Valuation Summary Card
| Metric | Determination | Basis |
| :--- | :---: | :--- |
| **Current Reference Share Price** | R0.60 | Closing price |
| **12-Month JSE Target Price** | R0.42 | NAV discount |

## 6. Actionable Portfolio Monitoring Triggers & Catalysts ('What to Watch For')
- **KPMG Crescent formal lease exit April 2027**
"""
    summary = parse_valuation_summary(json_note)
    assert summary.get("target_price") == 0.42
    assert summary.get("reference_price") == 0.60
    assert summary.get("recommendation") == "SELL"
    assert summary.get("upside_pct") == -30.0
    assert summary.get("dividend_yield_pct") == 0.0
    assert summary.get("tsr_pct") == -30.0
    assert "KPMG Crescent" in summary.get("monitoring_triggers", "")
    assert summary.get("sector") == "reit"
    assert summary.get("jse_sector_code") == "JS3512"
    assert summary.get("jse_sector_name") == "Real Estate Investment Trusts"


def test_stage2_prompt_json_specification():
    """Verify Stage 2 prompt generator includes mandatory JSON spec and critical formatting constraints at end."""
    from workflow.generate_stage2 import build_stage2_prompt_content

    prompt = build_stage2_prompt_content(
        stage1_content="# Stage 1 Reconciled Ground Truth",
        company_title="Lewis Group Limited",
        ticker="LEW",
        detected_sector="retail",
    )
    assert "MANDATORY JSON SUMMARY BLOCK" in prompt
    assert '"ticker": "LEW"' in prompt
    assert '"target_price_zar": 0.00' in prompt
    assert '"jse_sector_code": "JS4041"' in prompt
    assert '"jse_sector_name": "Retailers"' in prompt
    assert "CRITICAL OUTPUT FORMATTING CONSTRAINTS (STRICTLY ENFORCED)" in prompt
    # Check that constraints are placed at the end of the prompt
    assert prompt.strip().endswith("Reserve backticks solely for the initial JSON block and formal code/file identifiers.")




def test_detect_company_meta():
    """Verify company ticker, title, and sector inference."""
    t1, name1, sec1 = detect_company_meta("lewis-iar-2026.pdf")
    assert t1 == "LEW"
    assert "Lewis" in name1
    assert sec1 == "retail"

    t2, name2, sec2 = detect_company_meta("Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf")
    assert t2 == "PAN"
    assert "Pan African" in name2
    assert sec2 == "mining"

    t3, name3, sec3 = detect_company_meta("unknown-retail-annual-report.pdf")
    assert sec3 == "retail"

    t4, name4, sec4 = detect_company_meta("ioco_integrated_annual_report_2026.pdf")
    assert t4 == "IOC"
    assert "iOCO" in name4
    assert sec4 == "it"

    t5, name5, sec5 = detect_company_meta("companies/it/IOC/sources/report.pdf")
    assert t5 == "IOC"
    assert sec5 == "it"


def test_stage2_prompt_it_sector():
    from workflow.generate_stage2 import build_stage2_prompt_content
    prompt = build_stage2_prompt_content(
        stage1_content="# Stage 1 IT Audit Determinations",
        company_title="iOCO Limited",
        ticker="IOC",
        detected_sector="it",
    )
    assert "Technology & IT Services" in prompt
    assert "recurring revenue" in prompt.lower()
    assert '"sector": "it"' in prompt
    assert "CRITICAL OUTPUT FORMATTING CONSTRAINTS (STRICTLY ENFORCED)" in prompt


def test_db_save_and_auto_extract(tmp_path):
    """Verify that saving a Stage 2 response in SQLite automatically populates valuation metrics."""
    test_db = tmp_path / "test_analysis.sqlite"
    sha = "test_sha_12345"

    upsert_report(
        sha256=sha,
        filename="lewis-annual-report-2026.pdf",
        original_path="companies/retail/LEW/sources/lewis-iar-2026.pdf",
        db_path=test_db,
    )

    sample_stage2 = """
## 1. Executive Investment Thesis & 12-Month JSE Price Target
* **Current Reference Share Price:** R79.00
* **12-Month JSE Target Price:** **R84.50**
* **Implied Capital Upside:** +6.96%
* **Forward Dividend Yield (FY27E):** +11.90%
* **Projected 12-Month Total Shareholder Return (TSR):** **+18.86%**
* **Institutional Recommendation:** **HOLD**

### Institutional Action Plan & Monitoring Triggers for Portfolio Managers
1. Monitor collection rates above 77.0%.
2. Track gross margin within 40-42%.
"""

    ok = save_stage2_report(sha, prompt="# Prompt", response=sample_stage2, db_path=test_db)
    assert ok is True

    rep = get_stage2_report(sha, db_path=test_db)
    assert rep is not None
    assert rep["target_price_zar"] == 84.50
    assert rep["reference_price_zar"] == 79.00
    assert rep["recommendation"] == "HOLD"
    assert rep["upside_pct"] == 6.96
    assert rep["dividend_yield_pct"] == 11.90
    assert rep["tsr_pct"] == 18.86
    assert "Monitor collection rates" in rep["monitoring_triggers"]

    # Verify get_analyzed_stocks returns parsed item
    stocks = get_analyzed_stocks(db_path=test_db)
    assert len(stocks) == 1
    s = stocks[0]
    assert s["ticker"] == "LEW"
    assert s["target_price_zar"] == 84.50
    assert s["has_stage2"] is True


def test_portfolio_view_widget(qapp, tmp_path):
    """Test PortfolioView widget loading, filtering, selection, and disposal."""
    test_db = tmp_path / "test_gui_analysis.sqlite"

    # Add one valued company and one captured company
    upsert_report(
        sha256="sha_lew",
        filename="lewis-iar-2026.pdf",
        original_path="companies/retail/LEW/sources/lewis-iar-2026.pdf",
        db_path=test_db,
    )
    save_stage2_report(
        "sha_lew",
        prompt="Stage 2 Prompt",
        response="""
## 1. Executive Investment Thesis & 12-Month JSE Price Target
* **Current Reference Share Price:** R79.00
* **12-Month JSE Target Price:** **R84.50**
* **Implied Capital Upside:** +6.96%
* **Forward Dividend Yield (FY27E):** +11.90%
* **Projected 12-Month Total Shareholder Return (TSR):** **+18.86%**
* **Institutional Recommendation:** **HOLD**

## 6. Actionable Portfolio Monitoring Triggers
1. Monitor H1 debtor costs.
""",
        db_path=test_db,
    )

    upsert_report(
        sha256="sha_pan",
        filename="Pan-African-Results-2026.pdf",
        original_path="companies/mining/PAN/sources/pan.pdf",
        db_path=test_db,
    )

    view = PortfolioView(db_path=test_db)
    try:
        assert view.table.rowCount() == 2
        # First row should be LEW (active valuation sorted first)
        assert view.current_stock is not None
        assert view.current_stock["ticker"] == "LEW"
        assert "LEW" in view.stock_title_label.text()
        assert "R84.50" in view.kpi_metrics_label.text()
        assert "Monitor H1 debtor costs" in view.triggers_browser.toPlainText()

        # Test Search Filter
        view.search_edit.setText("PAN")
        assert view.table.rowCount() == 1
        assert view.current_stock["ticker"] == "PAN"

        # Clear filter
        view.search_edit.clear()
        assert view.table.rowCount() == 2
    finally:
        view.deleteLater()


def test_portfolio_coverage_dialog(qapp, tmp_path):
    """Test standalone PortfolioCoverageDialog rendering and cleanup."""
    test_db = tmp_path / "test_portfolio_dlg.sqlite"
    sha = "test_sha_dlg"
    upsert_report(sha256=sha, filename="lewis-iar-2026.pdf", db_path=test_db)

    dlg = PortfolioCoverageDialog(db_path=test_db)
    try:
        assert hasattr(dlg, "portfolio_view")
        assert dlg.portfolio_view.table.rowCount() == 1
    finally:
        dlg.deleteLater()


def test_sens_txt_format_and_completed_archive(tmp_path):
    from workflow.generate_sens_update import (
        get_sens_completed_dir,
        move_analyzed_sens_files,
        build_sens_update_prompt_content,
    )

    # Setup mock company dir
    comp_dir = tmp_path / "companies/reit/APF"
    sens_dir = comp_dir / "sources/sens"
    sens_dir.mkdir(parents=True)

    # Create .txt SENS files
    txt1 = sens_dir / "20260806_sens_4901_Notification.txt"
    txt1.write_text("Notice 1: Capital reduction of R30m", encoding="utf-8")
    txt2 = sens_dir / "20260925_sens_8265_Disposal.txt"
    txt2.write_text("Notice 2: Disposal of KPMG Crescent for R385m", encoding="utf-8")

    # Verify get_sens_completed_dir
    comp_target = get_sens_completed_dir(comp_dir)
    assert comp_target == sens_dir / "completed"

    # Build prompt content with text entries
    entries = [
        {"filename": txt1.name, "path": txt1, "is_text": True, "content": txt1.read_text(encoding="utf-8")},
        {"filename": txt2.name, "path": txt2, "is_text": True, "content": txt2.read_text(encoding="utf-8")},
    ]
    prompt_str = build_sens_update_prompt_content(
        baseline_valuation_report="# Baseline Report\nRecommendation: HOLD",
        company_title="APF Properties",
        ticker="APF",
        detected_sector="reit",
        sens_entries=entries,
    )
    assert "Listed Property & REIT" in prompt_str
    assert "Disposal of KPMG Crescent" in prompt_str
    assert "SUBSEQUENT SENS CONTINUOUS DISCLOSURE EVIDENCE" in prompt_str
    assert "Capital reduction of R30m" in prompt_str

    # Test move_analyzed_sens_files
    moved = move_analyzed_sens_files(comp_dir)
    assert len(moved) == 2
    assert not txt1.exists()
    assert not txt2.exists()
    assert (comp_target / txt1.name).exists()
    assert (comp_target / txt2.name).exists()
    assert (comp_target / txt2.name).read_text(encoding="utf-8") == "Notice 2: Disposal of KPMG Crescent for R385m"


def test_normalize_markdown_for_qt(qapp):
    from PySide6.QtWidgets import QTextBrowser

    # 1. Unclosed <br> tag and fragmented table rows
    broken_md = (
        "| Metric | Value | Commentary |\n"
        "| --- | --- | --- |\n"
        "| **Price** | R0.60\n\n"
        " | Base |\n"
        "| **Rating** | **SELL**<br> | High Conviction |\n\n"
        "---\n\n"
        "### Summary of SENS\n\n"
        "Following disclosure, (`APF` or `APFE`) announced agreement with (`RMA`).\n"
    )

    # In raw form, QTextBrowser swallows text after unclosed <br> in certain table contexts
    raw_tb = QTextBrowser()
    raw_tb.setMarkdown(broken_md)
    # Notice that broken_md raw might swallow paragraphs or break tables

    cleaned = normalize_markdown_for_qt(broken_md)
    assert "<br/>" in cleaned
    assert "\n\n | Base |" not in cleaned

    clean_tb = QTextBrowser()
    clean_tb.setMarkdown(cleaned)
    clean_text = clean_tb.toPlainText()

    assert "Price" in clean_text
    assert "Base" in clean_text
    assert "Rating" in clean_text
    assert "SELL" in clean_text
    assert "Summary of SENS" in clean_text
    assert "Following disclosure" in clean_text

def test_cgr_detection_and_stage1_compile(qapp, monkeypatch, tmp_path):
    from section_capture.db import detect_company_meta, get_analyzed_stocks
    from section_capture.one_shot_view import discover_available_companies
    from workflow.export_stage1 import export_stage1_prompt

    # 1. detect_company_meta
    orig_path = "companies/construction/CGR/sources/10023_Calgro-IR-2026_WEB-FA3.pdf"
    fname = "10023_Calgro-IR-2026_WEB-FA3.pdf"
    t1, n1, s1 = detect_company_meta(orig_path)
    assert t1 == "CGR"
    assert "Calgro" in n1
    assert s1 == "construction"

    t2, n2, s2 = detect_company_meta(fname)
    assert t2 == "CGR"
    assert "Calgro" in n2
    assert s2 == "construction"

    real_db = Path("documents/analysis.sqlite")
    if real_db.exists():
        # 2. get_analyzed_stocks
        stocks = get_analyzed_stocks(real_db)
        cgr_stock = next((s for s in stocks if s["ticker"] == "CGR"), None)
        assert cgr_stock is not None
        assert cgr_stock["section_count"] >= 5
        assert cgr_stock["sha256"] != ""

        # 3. discover_available_companies
        companies = discover_available_companies(real_db)
        cgr_comp = next((c for c in companies if c["ticker"] == "CGR"), None)
        assert cgr_comp is not None
        assert cgr_comp["sha256"] == cgr_stock["sha256"]

        # 4. CLI workflow/export_stage1.py
        out_file = export_stage1_prompt("CGR", output_path=tmp_path / "CGR_FY26_stage1_forensic_prompt.md")
        assert out_file.exists()
        assert out_file.stat().st_size > 1000

def test_create_company_scaffolds_sens_folder(tmp_path, monkeypatch):
    import new_company
    monkeypatch.setattr(new_company, "COMPANIES_DIR", tmp_path / "companies")
    company_dir = new_company.create_company("TEST", "mining", "Test Mining Co Ltd")
    assert company_dir.exists()
    sens_dir = company_dir / "sources/sens"
    assert sens_dir.exists()
    assert (sens_dir / "completed").exists()
    assert (sens_dir / "README.md").exists()
    content = (sens_dir / "README.md").read_text(encoding="utf-8")
    assert "SENS Continuous Disclosures: Test Mining Co Ltd (TEST)" in content

def test_detect_reporting_period():
    from section_capture.db import detect_reporting_period

    assert detect_reporting_period("fy26-audited-annual-financial-statements-2026.pdf") == "FY26"
    assert detect_reporting_period("PIK_1H27_results_presentation.pdf") == "1H27"
    assert detect_reporting_period("PIK_HY2027_interim.pdf") == "1H27"
    assert detect_reporting_period("interim_report_26.pdf") == "1H26"
    assert detect_reporting_period("2H26_results.pdf") == "2H26"
    assert detect_reporting_period("2027-annual-report.pdf") == "FY27"
    assert detect_reporting_period("generic.pdf", text_sample="for the six months ended 31 August 2026") == "1H26"
    assert detect_reporting_period("generic.pdf") == "FY26"


def test_archive_source_pdfs(tmp_path):
    from section_capture.db import archive_source_pdfs, connect_db, upsert_report

    comp_dir = tmp_path / "companies/retail/TST"
    sources_dir = comp_dir / "sources"
    sources_dir.mkdir(parents=True)
    pdf1 = sources_dir / "TST_FY26_AFS.pdf"
    pdf1.write_bytes(b"%PDF-1.4 test AFS")
    pdf2 = sources_dir / "TST_FY26_Presentation.pdf"
    pdf2.write_bytes(b"%PDF-1.4 test Pres")

    # SENS file in sens/ should NOT be moved by archive_source_pdfs
    sens_dir = sources_dir / "sens"
    sens_dir.mkdir()
    sens_file = sens_dir / "notice.txt"
    sens_file.write_text("SENS notice", encoding="utf-8")

    db_path = tmp_path / "test_archive.sqlite"
    upsert_report(sha256="sha_afs_1", filename=pdf1.name, original_path=str(pdf1), db_path=db_path)
    upsert_report(sha256="sha_pres_2", filename=pdf2.name, original_path=str(pdf2), db_path=db_path)

    moved = archive_source_pdfs(comp_dir, period="FY26", db_path=db_path)
    assert len(moved) == 2
    assert (sources_dir / "completed/FY26/TST_FY26_AFS.pdf").exists()
    assert (sources_dir / "completed/FY26/TST_FY26_Presentation.pdf").exists()
    assert not pdf1.exists()
    assert not pdf2.exists()
    assert sens_file.exists()  # SENS notice remains intact

    # Verify SQLite original_path updated
    with connect_db(db_path) as conn:
        row = conn.execute("SELECT original_path FROM reports WHERE sha256 = 'sha_afs_1'").fetchone()
        assert "completed" in row["original_path"]
        assert "FY26" in row["original_path"]


def test_document_classify_dialog_period_selection(qapp):
    from section_capture.window import DocumentClassifyDialog

    dlg = DocumentClassifyDialog("PIK_1H27_Interim.pdf", initial_type="interim", initial_period="1H27")
    try:
        assert hasattr(dlg, "period_combo")
        assert dlg.period_combo.currentText() == "1H27"
        assert dlg.selected_period == "1H27"

        # Change period
        dlg.period_combo.setEditText("FY27")
        dlg._on_accept()
        assert dlg.selected_period == "FY27"
    finally:
        dlg.deleteLater()



def test_parse_valuation_summary_rating_bands():
    """Verify parsing when Section 1 JSON block includes explicit rating_bands."""
    from section_capture.db import parse_valuation_summary

    note = """
# SHOPRITE HOLDINGS LIMITED (JSE: SHP)

## 1. Executive Investment Thesis & 12-Month JSE Price Target (ZAR/Share)

```json
{
  "ticker": "SHP",
  "company_name": "Shoprite Holdings Limited",
  "sector": "retail",
  "recommendation": "BUY",
  "reference_price_zar": 280.00,
  "target_price_zar": 350.00,
  "implied_upside_pct": 25.0,
  "forward_dividend_yield_pct": 3.8,
  "projected_12m_tsr_pct": 28.8,
  "rating_bands": {
    "strong_buy_max_zar": 269.23,
    "buy_max_zar": 304.35,
    "hold_max_zar": 368.42,
    "sell_max_zar": 411.76,
    "strong_sell_above_zar": 411.76
  }
}
```
"""
    summary = parse_valuation_summary(note)
    assert summary.get("target_price") == 350.00
    assert summary.get("reference_price") == 280.00
    assert summary.get("recommendation") == "BUY"
    assert "rating_bands" in summary
    bands = summary["rating_bands"]
    assert bands["strong_buy_max_zar"] == 269.23
    assert bands["buy_max_zar"] == 304.35
    assert bands["hold_max_zar"] == 368.42
    assert bands["sell_max_zar"] == 411.76
    assert bands["strong_sell_above_zar"] == 411.76


def test_compute_rating_bands_fallback():
    """Verify fallback institutional rating bands computation from target price."""
    from section_capture.db import compute_rating_bands_fallback

    # Test invalid / empty
    assert compute_rating_bands_fallback(None) is None
    assert compute_rating_bands_fallback(0) is None
    assert compute_rating_bands_fallback(-50) is None

    # Test valid target price R100.00
    bands = compute_rating_bands_fallback(100.00)
    assert bands is not None
    assert bands["strong_buy_max_zar"] == 76.92  # 100 / 1.30
    assert bands["buy_max_zar"] == 86.96        # 100 / 1.15
    assert bands["hold_max_zar"] == 105.26      # 100 / 0.95
    assert bands["sell_max_zar"] == 117.65      # 100 / 0.85
    assert bands["strong_sell_above_zar"] == 117.65


def test_evaluate_dynamic_rating():
    """Verify dynamic rating transitions across live share prices."""
    from section_capture.db import evaluate_dynamic_rating

    bands = {
        "strong_buy_max_zar": 50.00,
        "buy_max_zar": 65.00,
        "hold_max_zar": 80.00,
        "sell_max_zar": 95.00,
        "strong_sell_above_zar": 95.00,
    }

    # Deep value / strong upside
    assert evaluate_dynamic_rating(45.00, bands, fallback_rec="BUY") == "STRONG BUY"
    assert evaluate_dynamic_rating(50.00, bands, fallback_rec="BUY") == "STRONG BUY"

    # Attractive upside
    assert evaluate_dynamic_rating(55.00, bands, fallback_rec="BUY") == "BUY"
    assert evaluate_dynamic_rating(65.00, bands, fallback_rec="BUY") == "BUY"

    # Fair value
    assert evaluate_dynamic_rating(70.00, bands, fallback_rec="BUY") == "HOLD"
    assert evaluate_dynamic_rating(80.00, bands, fallback_rec="BUY") == "HOLD"

    # Modest downside
    assert evaluate_dynamic_rating(85.00, bands, fallback_rec="BUY") == "SELL"
    assert evaluate_dynamic_rating(95.00, bands, fallback_rec="BUY") == "SELL"

    # Extreme downside / overvalued
    assert evaluate_dynamic_rating(100.00, bands, fallback_rec="BUY") == "STRONG SELL"

    # Fallback when live price is missing or invalid
    assert evaluate_dynamic_rating(None, bands, fallback_rec="BUY") == "BUY"
    assert evaluate_dynamic_rating(0, bands, fallback_rec="BUY") == "BUY"
    assert evaluate_dynamic_rating(55.00, None, fallback_rec="HOLD") == "HOLD"


def test_get_analyzed_stocks_dynamic_ratings(tmp_path):
    """Verify get_analyzed_stocks calculates dynamic recommendation from live quotes and rating bands."""
    import json
    from section_capture.db import connect_db, get_analyzed_stocks, save_stage2_report

    test_db = tmp_path / "test_dyn.sqlite"

    note = """
# LEWIS GROUP LIMITED (JSE: LEW)
## 1. Executive Investment Thesis & 12-Month JSE Price Target
```json
{
  "ticker": "LEW",
  "company_name": "Lewis Group Limited",
  "sector": "retail",
  "recommendation": "BUY",
  "reference_price_zar": 55.00,
  "target_price_zar": 70.00,
  "implied_upside_pct": 27.3,
  "forward_dividend_yield_pct": 5.0,
  "projected_12m_tsr_pct": 32.3,
  "rating_bands": {
    "strong_buy_max_zar": 45.00,
    "buy_max_zar": 60.00,
    "hold_max_zar": 75.00,
    "sell_max_zar": 85.00,
    "strong_sell_above_zar": 85.00
  }
}
```
"""
    sha = "test_sha_lew_dynamic"
    from section_capture.db import upsert_report
    upsert_report(sha256=sha, filename="LEW_FY26.pdf", original_path="companies/retail/LEW/sources/LEW_FY26.pdf", period="FY26", db_path=test_db)
    save_stage2_report(sha, "# Stage 2 Prompt", note, db_path=test_db)

    # 1. No market quote yet -> static recommendation BUY
    stocks = get_analyzed_stocks(db_path=test_db)
    assert len(stocks) == 1
    s = stocks[0]
    assert s["ticker"] == "LEW"
    assert s["target_price_zar"] == 70.00
    assert s["static_recommendation"] == "BUY"
    assert s["dynamic_recommendation"] == "BUY"
    assert s["rating_bands"]["buy_max_zar"] == 60.00

    # 2. Market quote drops to R42.00 -> Dynamic rating becomes STRONG BUY
    with connect_db(test_db) as conn:
        conn.execute(
            """INSERT OR REPLACE INTO market_quotes (ticker, price_zar, prev_close_zar, currency, raw_price, change_pct, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, datetime('now'))""",
            ("LEW", 42.00, 45.00, "ZAC", 4200.0, -6.6, )
        )
    stocks = get_analyzed_stocks(db_path=test_db)
    s = stocks[0]
    assert s["live_price_zar"] == 42.00
    assert s["dynamic_recommendation"] == "STRONG BUY"
    assert s["recommendation"] == "STRONG BUY"
    assert s["static_recommendation"] == "BUY"

    # 3. Market quote surges to R88.00 -> Dynamic rating becomes STRONG SELL
    with connect_db(test_db) as conn:
        conn.execute(
            """UPDATE market_quotes SET price_zar = 88.00 WHERE ticker = 'LEW'"""
        )
    stocks = get_analyzed_stocks(db_path=test_db)
    s = stocks[0]
    assert s["live_price_zar"] == 88.00
    assert s["dynamic_recommendation"] == "STRONG SELL"
    assert s["static_recommendation"] == "BUY"


def test_portfolio_view_dynamic_rating_badges_and_filter(qapp, tmp_path):
    """Verify PortfolioView table displays dynamic rating badges and filter works."""
    from section_capture.db import connect_db, save_stage2_report
    from section_capture.portfolio_view import PortfolioView

    test_db = tmp_path / "test_pv.sqlite"

    note = """
```json
{
  "ticker": "APF",
  "company_name": "Accelerate Property Fund",
  "sector": "reit",
  "recommendation": "SELL",
  "reference_price_zar": 0.60,
  "target_price_zar": 0.42,
  "implied_upside_pct": -30.0,
  "forward_dividend_yield_pct": 0.0,
  "projected_12m_tsr_pct": -30.0,
  "rating_bands": {
    "strong_buy_max_zar": 0.32,
    "buy_max_zar": 0.37,
    "hold_max_zar": 0.44,
    "sell_max_zar": 0.49,
    "strong_sell_above_zar": 0.49
  }
}
```
"""
    sha = "test_sha_apf_view"
    from section_capture.db import upsert_report
    upsert_report(sha256=sha, filename="APF_FY26.pdf", original_path="companies/reit/APF/sources/APF_FY26.pdf", period="FY26", db_path=test_db)
    with connect_db(test_db) as conn:
        conn.execute(
            """INSERT OR REPLACE INTO market_quotes (ticker, price_zar, prev_close_zar, currency, raw_price, change_pct, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, datetime('now'))""",
            ("APF", 0.55, 0.58, "ZAC", 55.0, -5.1),
        )
    save_stage2_report(sha, "# Stage 2 Prompt", note, db_path=test_db)

    pv = PortfolioView(db_path=test_db)
    try:
        assert pv.table.rowCount() == 1
        assert pv.table.columnCount() == 11
        rec_item = pv.table.item(0, 8)
        assert rec_item is not None
        assert rec_item.text() == "STRONG SELL"
        tooltip = rec_item.toolTip()
        assert "Dynamic Live Rating: STRONG SELL" in tooltip
        assert "Note Original Rating: SELL" in tooltip
        assert "Valuation Rating Bands:" in tooltip

        # Test Filter
        # 1. Filter "BUY" -> 0 rows
        pv.rec_combo.setCurrentText("BUY")
        assert pv.table.rowCount() == 0

        # 2. Filter "STRONG SELL" -> 1 row
        pv.rec_combo.setCurrentText("STRONG SELL")
        assert pv.table.rowCount() == 1

        # 3. Filter "All Ratings" -> 1 row
        pv.rec_combo.setCurrentText("All Ratings")
        assert pv.table.rowCount() == 1
    finally:
        pv.deleteLater()


def test_stage2_documents_considered_table():
    """Verify Stage 2 prompt and valuation note include the Source Documents & Disclosures Considered table."""
    from section_capture.db import parse_valuation_summary
    from workflow.generate_stage2 import (
        build_stage2_prompt_content,
        ensure_documents_considered_table,
    )

    docs = [
        {
            "filename": "SPAR_GROUP_H1 2026_Results.pdf",
            "doc_type": "presentation",
            "badge": "[PRES]",
            "page_count": 58,
            "period": "1H26",
        },
        {
            "filename": "Unaudited_interim_results_for_the_26_weeks_ended_27_March_2026.pdf",
            "doc_type": "afs",
            "badge": "[AFS]",
            "page_count": 22,
            "period": "1H26",
        },
        {
            "filename": "SENS_20260928_S603859.pdf",
            "doc_type": "sens",
            "badge": "[SENS]",
            "page_count": 3,
            "announcement_date": "2026-09-28",
            "is_sens": True,
        },
    ]

    prompt = build_stage2_prompt_content(
        stage1_content="# Stage 1 Ground Truth",
        company_title="SPP Group",
        ticker="SPP",
        detected_sector="retail",
        reference_price_zar=48.31,
        source_documents=docs,
    )
    assert "### Source Documents & Disclosures Considered" in prompt
    assert "`SPAR_GROUP_H1 2026_Results.pdf`" in prompt
    assert "`Unaudited_interim_results_for_the_26_weeks_ended_27_March_2026.pdf`" in prompt
    assert "`SENS_20260928_S603859.pdf`" in prompt

    raw_note = """```json
{
  "ticker": "SPP",
  "company_name": "SPP Group",
  "sector": "retail",
  "recommendation": "SELL",
  "reference_price_zar": 48.31,
  "target_price_zar": 38.50,
  "implied_upside_pct": -20.3,
  "forward_dividend_yield_pct": 0.0,
  "projected_12m_tsr_pct": -20.3
}
```

| Metric | Determination | Basis & Key Commentary |
| :--- | :---: | :--- |
| **Current Reference Share Price** | R48.31 | Verified JSE closing price |
| **12-Month JSE Target Price** | R38.50 | DCF |
| **Institutional Recommendation** | SELL | Downside |
"""
    enriched = ensure_documents_considered_table(raw_note, docs)
    assert "### Source Documents & Disclosures Considered" in enriched
    assert "`SPAR_GROUP_H1 2026_Results.pdf`" in enriched
    assert "`SENS_20260928_S603859.pdf`" in enriched

    # Ensure parse_valuation_summary remains 100% accurate when Documents Considered table is present
    parsed = parse_valuation_summary(enriched)
    assert parsed["reference_price"] == 48.31
    assert parsed["target_price"] == 38.50
    assert parsed["recommendation"] == "SELL"
