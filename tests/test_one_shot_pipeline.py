from __future__ import annotations

from pathlib import Path
import shutil
import time

from PySide6.QtCore import QThread, Qt, Signal
from PySide6.QtWidgets import QMessageBox

from section_capture.db import connect_db, get_stage1_report, get_stage2_report, list_sections
from section_capture.one_shot_view import OneShotView, discover_company_documents
from section_capture.window import CaptureWindow


def test_discover_company_documents_ordering(pdf_path, tmp_path):
    comp_dir = tmp_path / "companies" / "retail" / "TST"
    sources_dir = comp_dir / "sources"
    sens_dir = sources_dir / "sens"
    sens_dir.mkdir(parents=True, exist_ok=True)

    # Create a presentation PDF, an AFS PDF, and a SENS text notice
    afs_pdf = sources_dir / "TST_FY26_audited_financial_statements.pdf"
    pres_pdf = sources_dir / "TST_FY26_results_presentation.pdf"
    shutil.copy(pdf_path, afs_pdf)
    pres_pdf.write_bytes(pdf_path.read_bytes() + b"\n%pres_dummy\n")

    sens_txt = sens_dir / "20261020_sens_trading_update.txt"
    sens_txt.write_text("Trading statement: HEPS up 20%.", encoding="utf-8")

    docs, period = discover_company_documents(comp_dir, db_path=tmp_path)
    assert len(docs) == 3
    assert period == "FY26"
    # Presentation should be ordered first, AFS second, SENS last
    assert docs[0]["doc_type"] == "presentation"
    assert docs[0]["badge"] == "[PRES]"
    assert docs[1]["doc_type"] == "afs"
    assert docs[1]["badge"] == "[AFS]"
    assert docs[2]["is_sens"] is True
    assert docs[2]["badge"] == "[SENS]"


def test_one_shot_view_in_capture_window_and_reordering(pdf_path, qapp, tmp_path):
    win = CaptureWindow(output_root=tmp_path)
    assert hasattr(win, "one_shot_view")
    assert win.workspace_tabs.currentIndex() == 0

    view: OneShotView = win.one_shot_view
    # Populate custom test company
    comp_dir = tmp_path / "companies" / "mining" / "TST"
    sources_dir = comp_dir / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    pdf1 = sources_dir / "TST_presentation_2026.pdf"
    pdf2 = sources_dir / "TST_afs_2026.pdf"
    shutil.copy(pdf_path, pdf1)
    pdf2.write_bytes(pdf_path.read_bytes() + b"\n%afs_dummy\n")

    docs, period = discover_company_documents(comp_dir, db_path=tmp_path)
    view.discovered_docs = docs
    view._populate_docs_table()
    assert view.docs_table.rowCount() == 2

    # Move row 0 down
    first_fn = view.discovered_docs[0]["filename"]
    second_fn = view.discovered_docs[1]["filename"]
    view.docs_table.selectRow(0)
    view._on_move_doc_down()
    selected = view.get_selected_ordered_documents()
    assert selected[0]["filename"] == second_fn
    assert selected[1]["filename"] == first_fn

    win.close()
    win.deleteLater()


def test_one_shot_end_to_end_autonomous_pipeline(pdf_path, qapp, tmp_path, monkeypatch):
    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(QMessageBox, "critical", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)

    # Mock API key
    import section_capture.one_shot_view as osv
    monkeypatch.setattr(osv, "get_openrouter_api_key", lambda: "mock-test-api-key")

    # Mock extract_all_app_sections to return 2 fast sections for deterministic speed
    monkeypatch.setattr(
        osv,
        "extract_all_app_sections",
        lambda source, use_llm=True: [
            {"title": "Executive Highlights", "start_page": 1, "end_page": 2},
            {"title": "Financial Statements", "start_page": 3, "end_page": 4},
        ],
    )

    # Mock OpenRouterWorker to emit deterministic section, Stage 1, and Stage 2 responses
    class DummyOpenRouterWorker(QThread):
        finished_query = Signal(str, float, dict)
        error_query = Signal(str)

        def __init__(self, prompt: str, model: str | None = None, parent=None, timeout: int = 180, max_tokens=None):
            super().__init__(parent)
            self.prompt = prompt

        def run(self):
            if "STAGE 1: INDEPENDENT COGNITIVE AUDIT" in self.prompt:
                resp = "# Stage 1 Forensic Audit Determinations\n\nAll balance sheet junctions verified."
            elif "STAGE 2" in self.prompt:
                resp = (
                    "# Stage 2 Institutional Valuation Note\n\n"
                    "```json\n"
                    "{\n"
                    '  "ticker": "TST",\n'
                    '  "company_name": "Test Mining Corp",\n'
                    '  "sector": "mining",\n'
                    '  "reporting_period": "FY26",\n'
                    '  "recommendation": "BUY",\n'
                    '  "current_price_zar": 10.0,\n'
                    '  "target_price_zar": 13.0,\n'
                    '  "upside_pct": 30.0,\n'
                    '  "rating_bands": {\n'
                    '    "strong_buy_max_zar": 10.0,\n'
                    '    "buy_max_zar": 11.3,\n'
                    '    "hold_max_zar": 13.68,\n'
                    '    "sell_max_zar": 15.29,\n'
                    '    "strong_sell_above_zar": 15.29\n'
                    "  }\n"
                    "}\n"
                    "```\n"
                )
            else:
                resp = (
                    "### 1. Summary\nKey points noted.\n\n"
                    "### 4. Updated Open Questions Ledger\n"
                    "- Q1 [High]: Verify capex reconciliation [p. 2].\n"
                )
            self.finished_query.emit(resp, 0.2, {"total_tokens": 500, "cost_usd": 0.001})

    monkeypatch.setattr(osv, "OpenRouterWorker", DummyOpenRouterWorker)
    monkeypatch.setattr(
        osv,
        "fetch_jse_quote",
        lambda ticker: {
            "ticker": ticker,
            "symbol": f"{ticker}.JO",
            "price_zar": 10.00,
            "raw_price": 1000.0,
            "currency": "ZAc",
        },
    )

    # Set up company folder in tmp_path
    comp_dir = tmp_path / "companies" / "mining" / "TST"
    sources_dir = comp_dir / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    test_pdf = sources_dir / "TST_FY26_results.pdf"
    shutil.copy(pdf_path, test_pdf)

    monkeypatch.setattr(osv, "find_company_dir", lambda ticker, sector=None: (sector or "mining", comp_dir))

    view = OneShotView(db_path=tmp_path)
    view.current_company = {
        "ticker": "TST",
        "company_title": "Test Mining Corp",
        "sector": "mining",
        "period": "FY26",
    }
    view.scan_current_company_files()
    assert view.docs_table.rowCount() == 1
    view.period_combo.setEditText("FY26")

    # Launch autonomous pipeline
    view.start_pipeline(use_llm_clustering=False)

    # Wait for background workers to complete all 5 phases
    deadline = time.time() + 15.0
    while view._is_running and time.time() < deadline:
        qapp.processEvents()
        time.sleep(0.05)
    for _ in range(10):
        qapp.processEvents()

    assert not view._is_running
    assert view.overall_progress.value() == 100
    assert "TST_FY26_results.pdf" in view.log_view.toPlainText()
    assert "AUTONOMOUS ANALYSIS COMPLETE" in view.log_view.toPlainText()
    assert "Q1 [High]" in view.ledger_preview.toPlainText()
    assert "Stage 1 Forensic Audit Determinations" in view.stage1_preview.toPlainText()
    assert "Stage 2 Institutional Valuation Note" in view.stage2_preview.toPlainText()

    # Check briefs saved on disk
    s1_file = comp_dir / "briefs" / "FY26" / "TST_FY26_stage1_audit_response.md"
    s2_file = comp_dir / "briefs" / "FY26" / "TST_FY26_stage2_valuation_note.md"
    assert s1_file.exists()
    assert s2_file.exists()

    view.close()
    view.deleteLater()


def test_obtain_reference_price_live_success(tmp_path, monkeypatch):
    import section_capture.one_shot_view as osv
    from section_capture.one_shot_view import OneShotView

    view = OneShotView(db_path=tmp_path)
    monkeypatch.setattr(
        osv,
        "fetch_jse_quote",
        lambda ticker: {
            "ticker": ticker,
            "symbol": f"{ticker}.JO",
            "price_zar": 48.23,
            "raw_price": 4823.0,
            "currency": "ZAc",
        },
    )

    price = view._obtain_reference_price("SPP")
    assert price == 48.23
    assert "Live Closing Price" in view.log_view.toPlainText()
    assert "SPP.JO" in view.log_view.toPlainText()


def test_obtain_reference_price_yfinance_fail_user_input(tmp_path, monkeypatch):
    import section_capture.one_shot_view as osv
    from section_capture.one_shot_view import OneShotView
    from PySide6.QtWidgets import QInputDialog

    view = OneShotView(db_path=tmp_path)
    # yfinance fails
    monkeypatch.setattr(osv, "fetch_jse_quote", lambda ticker: None)
    # User inputs 52.50
    monkeypatch.setattr(QInputDialog, "getDouble", lambda *args, **kwargs: (52.50, True))

    price = view._obtain_reference_price("UNKNOWN")
    assert price == 52.50
    assert "User Input Received" in view.log_view.toPlainText()


def test_obtain_reference_price_yfinance_fail_user_cancel(tmp_path, monkeypatch):
    import section_capture.one_shot_view as osv
    from section_capture.one_shot_view import OneShotView
    from PySide6.QtWidgets import QInputDialog

    view = OneShotView(db_path=tmp_path)
    # yfinance fails
    monkeypatch.setattr(osv, "fetch_jse_quote", lambda ticker: None)
    # User cancels
    monkeypatch.setattr(QInputDialog, "getDouble", lambda *args, **kwargs: (0.00, False))

    price = view._obtain_reference_price("UNKNOWN")
    assert price is None
    assert "Closing price was not provided" in view.log_view.toPlainText()
