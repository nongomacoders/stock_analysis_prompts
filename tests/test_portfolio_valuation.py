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
from section_capture.audit_dialog import AuditValuationDialog


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

    assert summary.get("target_price") == 84.50
    assert summary.get("reference_price") == 79.00
    assert summary.get("recommendation") == "HOLD"
    assert summary.get("upside_pct") == 6.96
    assert summary.get("dividend_yield_pct") == 11.90
    assert summary.get("tsr_pct") == 18.86
    assert summary.get("sector") == "retail"

    triggers = summary.get("monitoring_triggers", "")
    assert "Debtor Cost Migration" in triggers
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


def test_audit_dialog_with_portfolio_tab(qapp, tmp_path):
    """Test that AuditValuationDialog contains all 3 tabs and supports initial_tab selection."""
    test_db = tmp_path / "test_audit_dialog.sqlite"
    sha = "test_sha_dlg"
    upsert_report(sha256=sha, filename="lewis-iar-2026.pdf", db_path=test_db)

    class DummySource:
        sha256 = sha
        path = Path("companies/retail/LEW/sources/lewis-iar-2026.pdf")
        page_count = 10
        questions_ledger = ""

    dlg = AuditValuationDialog(DummySource(), db_path=test_db, initial_tab=2)
    try:
        assert dlg.tabs.count() == 3
        assert dlg.tabs.tabText(0) == "Stage 1: Cognitive Forensic Audit"
        assert dlg.tabs.tabText(1) == "Stage 2: Institutional Valuation Note"
        assert dlg.tabs.tabText(2) == "Analyzed Stocks & Portfolio Coverage"
        assert dlg.tabs.currentIndex() == 2
    finally:
        dlg.deleteLater()


def test_open_prompt_folder_action(qapp, tmp_path, monkeypatch):
    """Test that open prompt folder actions highlight the prompt markdown file."""
    test_db = tmp_path / "test_open_folder.sqlite"
    sha = "test_sha_folder"
    upsert_report(sha256=sha, filename="lewis-iar-2026.pdf", db_path=test_db)

    class DummySource:
        sha256 = sha
        path = Path("companies/retail/LEW/sources/lewis-iar-2026.pdf")
        page_count = 10
        questions_ledger = ""

    opened_targets = []
    monkeypatch.setattr(
        "section_capture.audit_dialog.open_folder_and_select",
        lambda target: opened_targets.append(str(target)),
    )

    monkeypatch.setattr(
        "PySide6.QtWidgets.QMessageBox.warning",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        "PySide6.QtWidgets.QMessageBox.information",
        lambda *args, **kwargs: None,
    )

    dlg = AuditValuationDialog(DummySource(), db_path=test_db)
    try:
        assert hasattr(dlg, "open_s1_folder_btn")
        assert hasattr(dlg, "open_s2_folder_btn")

        dlg.s1_prompt_edit.setPlainText("Sample prompt text")
        dlg.open_stage1_folder()
        assert len(opened_targets) >= 1
        assert "stage1_forensic_prompt.md" in opened_targets[-1] or "briefs" in opened_targets[-1]

        dlg.s2_prompt_edit.setPlainText("Sample Stage 2 prompt")
        dlg.open_stage2_folder()
        assert len(opened_targets) >= 2
        assert "stage2_valuation_prompt.md" in opened_targets[-1] or "briefs" in opened_targets[-1]

        # Verify chat instruction text boxes and copy actions
        assert hasattr(dlg, "s1_chat_edit")
        assert hasattr(dlg, "s2_chat_edit")
        assert hasattr(dlg, "copy_s1_chat_btn")
        assert hasattr(dlg, "copy_s2_chat_btn")
        assert "Stage 1 Forensic Audit" in dlg.s1_chat_edit.text()
        assert "Stage 2 Institutional Valuation Note" in dlg.s2_chat_edit.text()

        dlg.copy_s1_chat_instruction()
        assert QApplication.clipboard().text() == dlg.s1_chat_edit.text()
        assert "Copied chat instruction" in dlg.s1_prompt_status.text()

        dlg.copy_s2_chat_instruction()
        assert QApplication.clipboard().text() == dlg.s2_chat_edit.text()
        assert "Copied chat instruction" in dlg.s2_prompt_status.text()
    finally:
        dlg.deleteLater()


def test_audit_dialog_run_stage1_deepseek_btn(qapp, tmp_path):
    """Test that AuditValuationDialog provides the one-click DeepSeek Stage 1 execution action."""
    test_db = tmp_path / "test_stage1_btn.sqlite"
    sha = "test_sha_stage1_ds"
    upsert_report(sha256=sha, filename="APF_IAR_2026.pdf", db_path=test_db)

    class DummySource:
        filename = "APF_IAR_2026.pdf"
        sha256 = sha
        detected_sector = "reit"
        def get_all_sections(self):
            return []

    dlg = AuditValuationDialog(DummySource(), db_path=test_db)
    try:
        assert hasattr(dlg, "run_s1_deepseek_btn")
        assert "DeepSeek" in dlg.run_s1_deepseek_btn.text()
        assert hasattr(dlg, "run_s2_deepseek_btn")
        assert "DeepSeek" in dlg.run_s2_deepseek_btn.text()
    finally:
        dlg.deleteLater()


def test_audit_dialog_without_loading_pdf_sets_ticker_from_dropdown(qapp, tmp_path):
    """Test that opening AuditValuationDialog with source=None automatically populates company dropdown."""
    test_db = tmp_path / "test_dropdown_no_pdf.sqlite"
    sha1 = "sha_orn_test"
    sha2 = "sha_pan_test"
    upsert_report(sha256=sha1, filename="20260917-ORN-ASX-JSE-Annual-Report-2026.pdf", db_path=test_db)
    upsert_report(sha256=sha2, filename="Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", db_path=test_db)

    # Open dialog without loading any PDF (source=None)
    dlg = AuditValuationDialog(source=None, db_path=test_db, initial_tab=1)
    try:
        assert hasattr(dlg, "company_combo")
        assert dlg.company_combo.count() >= 2
        # Verify ticker is automatically set (not generic 'COMPANY')
        assert dlg.ticker in {"ORN", "PAN"}
        assert dlg.sector == "mining"
        assert dlg.tabs.currentIndex() == 1  # Valuation tab
        assert hasattr(dlg, "load_canvas_btn")
    finally:
        dlg.deleteLater()


def test_audit_dialog_company_dropdown_switching(qapp, tmp_path):
    """Test that switching ticker in the company dropdown updates company details and brief paths."""
    test_db = tmp_path / "test_dropdown_switching.sqlite"
    sha_orn = "sha_orn_switch"
    sha_lew = "sha_lew_switch"
    upsert_report(sha256=sha_orn, filename="20260917-ORN-ASX-JSE-Annual-Report-2026.pdf", db_path=test_db)
    upsert_report(sha256=sha_lew, filename="lewis-iar-2026.pdf", db_path=test_db)

    dlg = AuditValuationDialog(source=None, db_path=test_db)
    try:
        # Programmatically select ORN
        assert dlg.select_company_by_ticker("ORN") is True
        assert dlg.ticker == "ORN"
        assert dlg.sector == "mining"
        assert "ORN" in dlg.windowTitle()
        assert "ORN" in dlg.s1_chat_edit.text()
        assert "ORN" in dlg.s2_chat_edit.text()

        # Switch to LEW
        assert dlg.select_company_by_ticker("LEW") is True
        assert dlg.ticker == "LEW"
        assert dlg.sector == "retail"
        assert "LEW" in dlg.windowTitle()
        assert "LEW" in dlg.s1_chat_edit.text()
        assert "LEW" in dlg.s2_chat_edit.text()
    finally:
        dlg.deleteLater()


def test_portfolio_view_go_to_stage2_tab_action(qapp, tmp_path):
    """Test that clicking 'Go to Stage 2 Valuation' in PortfolioView switches dialog ticker and tab."""
    test_db = tmp_path / "test_portfolio_s2_nav.sqlite"
    sha_orn = "sha_orn_nav"
    sha_pan = "sha_pan_nav"
    upsert_report(sha256=sha_orn, filename="20260917-ORN-ASX-JSE-Annual-Report-2026.pdf", db_path=test_db)
    upsert_report(sha256=sha_pan, filename="Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", db_path=test_db)

    dlg = AuditValuationDialog(source=None, db_path=test_db, initial_tab=2)
    try:
        assert dlg.tabs.currentIndex() == 2  # Portfolio tab
        assert hasattr(dlg.tab_portfolio, "go_to_s2_btn")

        # Select second stock in table
        dlg.tab_portfolio.table.selectRow(1)
        selected_stock = dlg.tab_portfolio.current_stock
        assert selected_stock is not None

        # Click Go to Stage 2 Valuation
        dlg.tab_portfolio.go_to_s2_btn.click()
        assert dlg.tabs.currentIndex() == 1  # Switched to Stage 2
        assert dlg.ticker == selected_stock["ticker"]
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


def test_audit_dialog_sens_update_and_auto_archive(qapp, tmp_path, monkeypatch):
    from section_capture.audit_dialog import AuditValuationDialog
    from section_capture.db import upsert_report, save_stage2_report
    from PySide6.QtWidgets import QMessageBox

    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)

    test_db = tmp_path / "test_sens_archive.sqlite"
    sha = "sha_apf_sens_test"
    upsert_report(sha256=sha, filename="APF_IAR_2026.pdf", db_path=test_db)
    save_stage2_report(sha, response="# Baseline APF Note\nTarget: R0.48", db_path=test_db)

    dlg = AuditValuationDialog(source=None, db_path=test_db, initial_tab=1)
    try:
        assert hasattr(dlg, "move_sens_btn")
        # Ensure button click works when no pending files
        dlg.move_sens_to_completed_gui()
    finally:
        dlg.deleteLater()


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

def test_cgr_detection_and_stage1_compile(qapp, monkeypatch):
    from section_capture.db import detect_company_meta, get_analyzed_stocks
    from section_capture.audit_dialog import AuditValuationDialog, discover_available_companies
    from workflow.export_stage1 import export_stage1_prompt
    from PySide6.QtWidgets import QMessageBox

    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)

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

        # 4. AuditValuationDialog compile_stage1_prompt
        dlg = AuditValuationDialog(db_path=real_db)
        try:
            idx = -1
            for i in range(dlg.company_combo.count()):
                if "CGR" in dlg.company_combo.itemText(i):
                    idx = i
                    break
            assert idx != -1
            dlg.company_combo.setCurrentIndex(idx)
            assert dlg.ticker == "CGR"
            assert dlg.source is not None
            assert dlg.source.sha256 == cgr_stock["sha256"]

            dlg.compile_stage1_prompt()
            compiled = dlg.s1_prompt_edit.toPlainText()
            assert len(compiled) > 1000
            assert "STAGE 1: INDEPENDENT COGNITIVE AUDIT" in compiled
            assert "Calgro" in compiled or "CGR" in compiled
        finally:
            dlg.deleteLater()

        # 5. CLI workflow/export_stage1.py
        out_file = export_stage1_prompt("CGR")
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

