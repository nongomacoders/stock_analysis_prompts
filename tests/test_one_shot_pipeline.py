from __future__ import annotations

from valuation_examples import ready_note

from pathlib import Path
import json
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
    assert win.centralWidget() is win.one_shot_view
    assert not hasattr(win, 'canvas')

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

    # Isolate orchestration from full-document coverage planning, tested separately.
    monkeypatch.setattr('section_capture.capture_planner.partition_detected_ranges', lambda sections, total_pages: sections)
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
    worker_options = []
    class DummyOpenRouterWorker(QThread):
        finished_query = Signal(str, float, dict)
        error_query = Signal(str)

        def __init__(self, prompt: str, model: str | None = None, parent=None, timeout: int = 180, max_tokens=None, reasoning_effort="none"):
            super().__init__(parent)
            self.prompt = prompt
            worker_options.append((reasoning_effort, max_tokens, timeout))

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
                    "```json\n" + json.dumps(dict(ledger_version=1, updates=[], new_questions=[dict(
                        question='Verify capex reconciliation.', priority='high', target_document='TST_FY26_results.pdf',
                        target_section='D003', evidence_required='Signed capex components and source rows.',
                        closure_condition='Components reproduce the statutory total.'
                    )])) + "\n```\n"
                )
            self.finished_query.emit(ready_note(resp) if 'target_price_zar' in resp else resp, 0.2, {"total_tokens": 500, "cost_usd": 0.001})

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
    assert "Verify capex reconciliation." in view.ledger_preview.toPlainText()
    assert "Stage 1 Forensic Audit Determinations" in view.stage1_preview.toPlainText()
    assert "Stage 2 Institutional Valuation Note" in view.stage2_preview.toPlainText()

    # Check briefs saved on disk
    s1_file = comp_dir / "briefs" / "FY26" / "TST_FY26_stage1_audit_response.md"
    s2_file = comp_dir / "briefs" / "FY26" / "TST_FY26_stage2_valuation_note.md"
    assert s1_file.exists()
    assert s2_file.exists()
    assert worker_options.count(("max", 65536, 900)) == 2
    assert any(effort == "none" for effort, _, _ in worker_options)

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


def test_sector_guardrails_table_and_prompt_injection(tmp_path):
    from section_capture.db import (
        format_sector_guardrails_block,
        get_sector_guardrails,
        upsert_sector_guardrail,
    )
    from workflow.export_stage1 import build_stage1_prompt_content
    from workflow.generate_sens_update import build_sens_update_prompt_content
    from workflow.generate_stage2 import build_stage2_prompt_content

    rules = get_sector_guardrails(sector="retail", stage="stage2", db_path=tmp_path)
    codes = {r["rule_code"] for r in rules}
    assert "ALL-IFRS16-EV-BRIDGE" in codes
    assert "ALL-PNL-VERTICAL-ARITHMETIC" in codes
    assert "ALL-CROSS-SECTION-METRIC-SYNC" in codes
    assert "ALL-RATING-BANDS-MONOTONIC" in codes
    assert "RETAIL-IFRS16-HEADLEASE-SUBLEASE" in codes

    # Add a custom error-derived guardrail dynamically
    upsert_sector_guardrail(
        rule_code="RETAIL-CUSTOM-TEST-RULE",
        sector="retail",
        stage="all",
        title="Custom Retail Working Capital Cutoff",
        rule_text="Always verify 52-week vs 53-week retail calendar cutoff on trade payables.",
        origin_ticker="SPP",
        db_path=tmp_path,
    )
    updated_block = format_sector_guardrails_block(sector="retail", stage="stage2", db_path=tmp_path)
    assert "RETAIL-CUSTOM-TEST-RULE" in updated_block
    assert "Custom Retail Working Capital Cutoff" in updated_block

    s1_prompt = build_stage1_prompt_content(
        sections=[],
        company_title="The SPAR Group Ltd",
        ticker="SPP",
        detected_sector="retail",
        filename="SPAR_1H26.pdf",
        db_path=tmp_path,
    )
    assert "MANDATORY ACCOUNTING & VALUATION GUARDRAILS REGISTRY (SECTOR: RETAIL)" in s1_prompt
    assert "ALL-IFRS16-EV-BRIDGE" in s1_prompt

    s2_prompt = build_stage2_prompt_content(
        stage1_content="Stage 1 Ground Truth",
        company_title="The SPAR Group Ltd",
        ticker="SPP",
        detected_sector="retail",
        reference_price_zar=48.31,
        db_path=tmp_path,
    )
    assert "MANDATORY ACCOUNTING & VALUATION GUARDRAILS REGISTRY (SECTOR: RETAIL)" in s2_prompt
    assert "RETAIL-IFRS16-HEADLEASE-SUBLEASE" in s2_prompt

    sens_prompt = build_sens_update_prompt_content(
        baseline_valuation_report="# Prior Stage 2 Note",
        company_title="The SPAR Group Ltd",
        ticker="SPP",
        detected_sector="retail",
        reference_price_zar=48.31,
        stage1_audit_report="# Audited Stage 1 Determinations from SQLite",
        db_path=tmp_path,
    )
    assert "STAGE 1 WORKING DETERMINATIONS (REOPEN CONTRADICTIONS FROM SQLITE)" in sens_prompt
    assert "# Audited Stage 1 Determinations from SQLite" in sens_prompt
    assert "MANDATORY ACCOUNTING & VALUATION GUARDRAILS REGISTRY (SECTOR: RETAIL)" in sens_prompt


def test_sanitize_stage2_valuation_markdown_repairs_degenerate_bands():
    from workflow.generate_stage2 import sanitize_stage2_valuation_markdown
    import json
    import re

    bad_note = (
        "```json\n"
        "{\n"
        '  "ticker": "SPP",\n'
        '  "target_price_zar": 38.50,\n'
        '  "reference_price_zar": 48.31,\n'
        '  "rating_bands": {\n'
        '    "strong_buy_max_zar": 29.62,\n'
        '    "buy_max_zar": 33.48,\n'
        '    "hold_max_zar": 44.28,\n'
        '    "sell_max_zar": 44.28,\n'
        '    "strong_sell_above_zar": 44.28\n'
        "  }\n"
        "}\n"
        "```\n\n"
        "## 1. Executive Summary\n"
    )
    fixed = sanitize_stage2_valuation_markdown(ready_note(bad_note), reference_price_hint=48.31)
    m = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", fixed)
    assert m is not None
    data = json.loads(m.group(1))
    rb = data["rating_bands"]
    assert rb["strong_buy_max_zar"] < rb["buy_max_zar"] < rb["hold_max_zar"] < rb["sell_max_zar"]
    assert rb["sell_max_zar"] == rb["strong_sell_above_zar"]


def test_discover_archived_pdfs_and_sens_in_place_and_smart_sens_update(pdf_path, qapp, tmp_path, monkeypatch):
    import section_capture.one_shot_view as osv
    from section_capture.db import get_stage2_report, save_stage1_report, save_stage2_report, upsert_report
    from section_capture.one_shot_view import OneShotView, discover_company_documents

    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(QMessageBox, "critical", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(osv, "get_openrouter_api_key", lambda: "mock-test-api-key")
    monkeypatch.setattr(
        osv,
        "fetch_jse_quote",
        lambda ticker: {
            "ticker": ticker,
            "symbol": f"{ticker}.JO",
            "price_zar": 48.31,
            "raw_price": 4831.0,
            "currency": "ZAc",
        },
    )

    # Set up SPP with PDFs ALREADY in sources/completed/1H26/ and prior SENS in sources/sens/completed/
    comp_dir = tmp_path / "companies" / "retail" / "SPP"
    comp_pdf_dir = comp_dir / "sources" / "completed" / "1H26"
    comp_pdf_dir.mkdir(parents=True, exist_ok=True)
    sens_dir = comp_dir / "sources" / "sens"
    sens_comp_dir = sens_dir / "completed"
    sens_comp_dir.mkdir(parents=True, exist_ok=True)

    archived_afs = comp_pdf_dir / "SPP_1H26_afs.pdf"
    shutil.copy(pdf_path, archived_afs)
    prior_sens = sens_comp_dir / "SENS_20260601_prior.txt"
    prior_sens.write_text("Prior SENS: Initial trading update.", encoding="utf-8")

    # Drop a NEW SENS in sources/sens/ without pulling PDFs out of completed/1H26/
    new_sens = sens_dir / "SENS_20260928_preclose.txt"
    new_sens.write_text("New SENS: Revised lender covenants and H2 wholesale moderation.", encoding="utf-8")

    # Register report & Stage 1 + Stage 2 in SQLite and briefs/1H26/
    docs, detected_period = discover_company_documents(comp_dir, db_path=tmp_path)
    assert detected_period == "1H26"
    assert len(docs) == 3
    assert docs[0]["filename"] == "SPP_1H26_afs.pdf"
    assert docs[0]["is_archived"] is True
    assert docs[1]["filename"] == "SENS_20260601_prior.txt"
    assert docs[1]["is_sens"] is True and docs[1]["is_archived"] is True
    assert docs[2]["filename"] == "SENS_20260928_preclose.txt"
    assert docs[2]["is_sens"] is True and docs[2]["is_archived"] is False

    primary_sha = docs[0]["sha256"]
    upsert_report(
        sha256=primary_sha,
        filename=archived_afs.name,
        original_path=str(archived_afs),
        physical_page_count=docs[0]["page_count"],
        doc_type="afs",
        period="1H26",
        db_path=tmp_path,
    )
    save_stage1_report(
        primary_sha,
        prompt="S1 prompt",
        response="# Stage 1 Forensic Audit from SQLite\nNet lease liability R3.4bn vs Pre-IFRS 16 EBITDA R976.4m.",
        db_path=tmp_path,
    )
    briefs_dir = comp_dir / "briefs" / "1H26"
    briefs_dir.mkdir(parents=True, exist_ok=True)
    s2_note_file = briefs_dir / "SPP_1H26_stage2_valuation_note.md"
    s2_note_file.write_text("# Baseline Stage 2 Valuation Note\nTarget R50.00.", encoding="utf-8")
    save_stage2_report(primary_sha, response=ready_note(s2_note_file.read_text(encoding="utf-8")), db_path=tmp_path)

    captured_prompts: list[str] = []

    class DummySensWorker(QThread):
        finished_query = Signal(str, float, dict)
        error_query = Signal(str)

        def __init__(self, prompt: str, model: str | None = None, parent=None, timeout: int = 180, max_tokens=None, reasoning_effort="none"):
            super().__init__(parent)
            self.prompt = prompt
            assert (reasoning_effort, max_tokens, timeout) == ("max", 65536, 900)
            captured_prompts.append(prompt)

        def run(self):
            resp = (
                "```json\n"
                "{\n"
                '  "ticker": "SPP",\n'
                '  "company_name": "The SPAR Group Ltd",\n'
                '  "sector": "retail",\n'
                '  "recommendation": "HOLD",\n'
                '  "reference_price_zar": 48.31,\n'
                '  "target_price_zar": 49.30,\n'
                '  "implied_upside_pct": 2.0,\n'
                '  "rating_bands": {\n'
                '    "strong_buy_max_zar": 44.28,\n'
                '    "buy_max_zar": 44.28,\n'
                '    "hold_max_zar": 44.28,\n'
                '    "sell_max_zar": 44.28,\n'
                '    "strong_sell_above_zar": 44.28\n'
                "  }\n"
                "}\n"
                "```\n\n"
                "## 1. Executive Summary\nUpdated post-SENS note.\n"
            )
            self.finished_query.emit(ready_note(resp) if 'target_price_zar' in resp else resp, 0.1, {"total_tokens": 400, "cost_usd": 0.001})

    monkeypatch.setattr(osv, "OpenRouterWorker", DummySensWorker)
    monkeypatch.setattr(osv, "find_company_dir", lambda ticker, sector=None: ("retail", comp_dir))

    view = OneShotView(db_path=tmp_path)
    view.current_company = {
        "ticker": "SPP",
        "company_title": "The SPAR Group Ltd",
        "sector": "retail",
        "period": "1H26",
    }
    view.scan_current_company_files()
    assert view.docs_table.rowCount() == 3

    view.period_combo.setEditText("1H26")
    view.start_pipeline(use_llm_clustering=False)
    deadline = time.time() + 10.0
    while view._is_running and time.time() < deadline:
        qapp.processEvents()
        time.sleep(0.05)
    for _ in range(10):
        qapp.processEvents()

    assert not view._is_running
    assert len(captured_prompts) == 1
    # Verify Stage 1 from SQLite + prior & new SENS + guardrails were injected into the SENS update prompt
    sent_prompt = captured_prompts[0]
    assert "Stage 1 Forensic Audit from SQLite" in sent_prompt
    assert "SENS_20260601_prior.txt" in sent_prompt
    assert "SENS_20260928_preclose.txt" in sent_prompt
    assert "ALL-IFRS16-EV-BRIDGE" in sent_prompt

    # Verify baseline backup created, documents table injected, degenerate rating bands repaired, and new SENS archived
    assert (briefs_dir / "SPP_1H26_stage2_valuation_note_baseline.md").exists()
    updated_note = s2_note_file.read_text(encoding="utf-8")
    assert "Source Documents & Disclosures Considered" in updated_note
    assert "SPP_1H26_afs.pdf" in updated_note
    assert (sens_comp_dir / "SENS_20260928_preclose.txt").exists()
    assert not new_sens.exists()

    s2_db = get_stage2_report(primary_sha, db_path=tmp_path)
    assert s2_db is not None
    assert s2_db["target_price_zar"] == 49.30

    view.close()
    view.deleteLater()


def test_resubmit_stage2_from_completed_pdfs_and_sqlite_stage1(pdf_path, qapp, tmp_path, monkeypatch):
    import section_capture.one_shot_view as osv
    from section_capture.db import save_stage1_report, upsert_report
    from section_capture.one_shot_view import OneShotView
    from section_capture.pdf_source import PdfSource
    from section_capture.section_matcher import auto_capture_section

    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(QMessageBox, "critical", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(osv, "get_openrouter_api_key", lambda: "mock-test-api-key")
    monkeypatch.setattr(
        osv,
        "fetch_jse_quote",
        lambda ticker: {
            "ticker": ticker,
            "symbol": f"{ticker}.JO",
            "price_zar": 48.31,
            "raw_price": 4831.0,
            "currency": "ZAc",
        },
    )

    comp_dir = tmp_path / "companies" / "retail" / "SPP"
    comp_pdf_dir = comp_dir / "sources" / "completed" / "1H26"
    comp_pdf_dir.mkdir(parents=True, exist_ok=True)
    sens_comp_dir = comp_dir / "sources" / "sens" / "completed"
    sens_comp_dir.mkdir(parents=True, exist_ok=True)

    archived_afs = comp_pdf_dir / "SPP_1H26_afs.pdf"
    shutil.copy(pdf_path, archived_afs)
    archived_sens = sens_comp_dir / "SENS_20260928_S603859.txt"
    archived_sens.write_text("48-week pre-close update: revised lender covenants.", encoding="utf-8")

    # Pre-populate SQLite with 1 audited section and Stage 1 response (NO markdown files in briefs/ yet)
    src = PdfSource(archived_afs)
    sha = src.sha256
    upsert_report(
        sha256=sha,
        filename=archived_afs.name,
        original_path=str(archived_afs),
        physical_page_count=src.page_count,
        doc_type="afs",
        period="1H26",
        db_path=tmp_path,
    )
    pkg = auto_capture_section(
        source=src,
        title="Financial Statements",
        start_page=1,
        end_page=2,
        sector="retail",
        output_root=tmp_path,
    )
    src.close()
    from section_capture.db import save_section_llm_response, list_sections
    # A logical capture request can create several packages; every cached package is done.
    for saved in list_sections(sha, db_path=tmp_path):
        save_section_llm_response(saved.package_id, '### 4. Updated Open Questions Ledger\n```json\n'
                                 '{"ledger_version":1,"updates":[],"new_questions":[]}\n```', db_path=tmp_path)
    save_stage1_report(
        sha,
        prompt="S1 prompt",
        response="# Stage 1 Forensic Audit Stored Only in SQLite\nVerified OP R740.5m.",
        db_path=tmp_path,
    )

    captured_s2_prompts: list[str] = []

    class DummyStage2OnlyWorker(QThread):
        finished_query = Signal(str, float, dict)
        error_query = Signal(str)

        def __init__(self, prompt: str, model: str | None = None, parent=None, timeout: int = 180, max_tokens=None, reasoning_effort="none"):
            super().__init__(parent)
            self.prompt = prompt
            assert (reasoning_effort, max_tokens, timeout) == ("max", 65536, 900)
            captured_s2_prompts.append(prompt)

        def run(self):
            resp = (
                "```json\n"
                "{\n"
                '  "ticker": "SPP",\n'
                '  "company_name": "The SPAR Group Ltd",\n'
                '  "sector": "retail",\n'
                '  "recommendation": "HOLD",\n'
                '  "reference_price_zar": 48.31,\n'
                '  "target_price_zar": 49.30,\n'
                '  "implied_upside_pct": 2.0\n'
                "}\n"
                "```\n\n"
                "## 1. Executive Summary\nRebuilt Stage 2 from completed PDFs and SQLite Stage 1.\n"
            )
            self.finished_query.emit(ready_note(resp) if 'target_price_zar' in resp else resp, 0.1, {"total_tokens": 500, "cost_usd": 0.001})

    monkeypatch.setattr(osv, "OpenRouterWorker", DummyStage2OnlyWorker)
    monkeypatch.setattr(osv, "find_company_dir", lambda ticker, sector=None: ("retail", comp_dir))

    view = OneShotView(db_path=tmp_path)
    view.current_company = {
        "ticker": "SPP",
        "company_title": "The SPAR Group Ltd",
        "sector": "retail",
        "period": "1H26",
    }
    view.scan_current_company_files()
    assert view.docs_table.rowCount() == 2

    view.period_combo.setEditText("1H26")
    view.start_pipeline(use_llm_clustering=False)
    deadline = time.time() + 10.0
    while view._is_running and time.time() < deadline:
        qapp.processEvents()
        time.sleep(0.05)
    for _ in range(10):
        qapp.processEvents()

    assert not view._is_running
    # Only Stage 2 worker should have been invoked (Tier 1 & Stage 1 reused from SQLite!)
    assert len(captured_s2_prompts) == 1
    assert "Stage 1 Forensic Audit Stored Only in SQLite" in captured_s2_prompts[0]
    assert "SENS_20260928_S603859.txt" in captured_s2_prompts[0]
    assert "SPP_1H26_afs.pdf" in captured_s2_prompts[0]
    assert "ALL-IFRS16-EV-BRIDGE" in captured_s2_prompts[0]

    # Verify Stage 1 was also restored to briefs/1H26/ on disk
    assert (comp_dir / "briefs" / "1H26" / "SPP_1H26_stage1_audit_response.md").exists()
    assert (comp_dir / "briefs" / "1H26" / "SPP_1H26_stage2_valuation_note.md").exists()

    view.close()
    view.deleteLater()


def test_period_combo_blank_by_default_blocks_auto_pipeline(pdf_path, qapp, tmp_path, monkeypatch):
    """Ensures period_combo is left blank by default, does not auto-populate on scan, and blocks pipeline with critical error."""
    import section_capture.one_shot_view as osv
    from section_capture.one_shot_view import OneShotView

    critical_dialogs: list[tuple[str, str]] = []
    monkeypatch.setattr(
        QMessageBox,
        "critical",
        lambda parent, title, text, *args, **kwargs: critical_dialogs.append((title, text)) or QMessageBox.StandardButton.Ok,
    )
    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda parent, title, text, *args, **kwargs: QMessageBox.StandardButton.Ok,
    )
    monkeypatch.setattr(osv, "get_openrouter_api_key", lambda: "mock-test-api-key")

    comp_dir = tmp_path / "companies" / "retail" / "TST"
    sources_dir = comp_dir / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    test_pdf = sources_dir / "TST_results_2026.pdf"
    shutil.copy(pdf_path, test_pdf)

    monkeypatch.setattr(osv, "find_company_dir", lambda ticker, sector=None: ("retail", comp_dir))

    view = OneShotView(db_path=tmp_path)
    # 1. Check initial period combo state is blank
    assert view.period_combo.currentText().strip() == ""

    view.current_company = {
        "ticker": "TST",
        "company_title": "Test Retail",
        "sector": "retail",
    }
    view.scan_current_company_files()

    # 2. Check period combo remains blank after scanning files
    assert view.period_combo.currentText().strip() == ""

    # 3. Attempt to run pipeline without selecting a period
    view.start_pipeline(use_llm_clustering=False)

    # 4. Must NOT start and must pop up critical error dialog
    assert not view._is_running
    assert len(critical_dialogs) == 1
    assert "Reporting Period Required" in critical_dialogs[0][0]
    assert "Please select or enter the reporting period" in critical_dialogs[0][1]

    # 5. Setting period allows pipeline to proceed past validation
    view.period_combo.setEditText("1H26")
    critical_dialogs.clear()

    # Stub workers so it doesn't need external LLM
    class DummyIngestion(QThread):
        log_message = Signal(str)
        doc_status_updated = Signal(str, str, str)
        step_progress = Signal(int, int, str)
        ingestion_finished = Signal(list)
        ingestion_error = Signal(str)

        def __init__(self, *args, **kwargs):
            super().__init__()

        def run(self):
            pass

        def cancel(self):
            pass

    monkeypatch.setattr(osv, "IngestionWorker", DummyIngestion)

    view.start_pipeline(use_llm_clustering=False)
    assert len(critical_dialogs) == 0
    assert view._is_running

    view.stop_pipeline()
    view.close()
    view.deleteLater()
