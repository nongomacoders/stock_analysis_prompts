from pathlib import Path
import shutil

import pytest
from PySide6.QtCore import QPointF, QRectF

from section_capture.packages import clean_single_line_text, save_package, shorten_section_name
from section_capture.pdf_source import PdfSource
from section_capture.window import CaptureWindow, HeadingComboBox, SanitizedLineEdit


def test_original_identity_and_page_size(source):
    assert source.page_count == 54
    assert source.sha256 == "62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd"
    w, h = source.size(3)
    assert w > h > 0
    with pytest.raises(ValueError):
        source.size(0)


def test_area_crop_keeps_left_and_right_evidence_separate(source):
    width, height = source.size(3)
    left = source.capture_area(3, QRectF(0, 0, width / 2, height))
    right = source.capture_area(3, QRectF(width / 2, 0, width / 2, height))
    assert "PRODUCTION" in left.text and "GROWTH" in left.text
    assert "SAFETY" not in left.text and "FINANCIAL" not in left.text
    assert "SAFETY" in right.text and "FINANCIAL" in right.text
    assert "KEY FEATURES" not in right.text
    assert left.bbox[2] == pytest.approx(width / 2)


def test_reverse_drag_clamps_to_source_page_and_rejects_tiny_box(source):
    cap = source.capture_area(3, QRectF(QPointF(80, 90), QPointF(-10, -5)))
    assert cap.bbox == (0, 0, 80, 90)
    with pytest.raises(ValueError, match="larger selection"):
        source.capture_area(3, QRectF(10, 10, 0.5, 1))


def test_no_native_text_warns(source):
    cap = source.capture_area(1, QRectF(5, 200, 20, 20))
    assert not cap.text.strip()
    assert any("No native text" in w for w in cap.warnings)


def test_boundary_crossing_is_disclosed(source):
    native = source.plumber.pages[2]
    char = next(c for c in native.chars if c["text"] == "G")
    rect = QRectF((char["x0"] + char["x1"]) / 2, char["top"] - 2, 25, char["bottom"] - char["top"] + 4)
    cap = source.capture_area(3, rect)
    assert any("boundary crosses text" in w for w in cap.warnings)


def test_multi_page_package_is_saved_in_sqlite_without_png_or_zip_files(source, tmp_path):
    width, height = source.size(3)
    first = source.capture_area(3, QRectF(0, 0, width / 2, height))
    first.printed_label = "2"
    second = source.capture_area(6, QRectF(0, 0, width / 2, height))
    output = save_package(source, "../Production: costs / FY26", "What changed and why?", [first, second], tmp_path)
    assert output.db_path == (tmp_path / "analysis.sqlite").resolve()
    assert not list(tmp_path.rglob("*.png"))
    assert not list(tmp_path.rglob("*.zip"))
    manifest = output.manifest
    assert [p["physical_page"] for p in manifest["selections"]] == [3, 6]
    assert manifest["source"]["sha256"] == source.sha256
    assert manifest["selections"][0]["printed_label_origin"] == "user_entered_unverified"
    assert manifest["review"]["model_brief"] == "not_run"
    assert manifest["review"]["source_verification"] == "not_reviewed"
    assert manifest["review"]["analyst_review"] == "not_recorded"
    assert manifest["task"] == "analyst_reading_brief"
    assert manifest["response_format"] == "markdown"
    assert "output_schema_sha256" not in manifest["prompt"]
    for part in manifest["selections"]:
        assert "image" not in part
        assert len(part["text_sha256"]) == 64
    prompt = output.prompt
    assert manifest["package_id"] in prompt and "Section D002" in prompt and "Section D003" in prompt
    assert "S001" not in prompt and ".png" not in prompt
    assert "What changed and why?" in prompt
    assert "physical PDF page 3" in prompt and source.path.name in prompt
    again = save_package(source, "../Production: costs / FY26", "", [first], tmp_path)
    assert again.package_id != output.package_id and again.section_number == 2


def test_missing_heading_or_selection_does_not_create_pack(source, tmp_path):
    with pytest.raises(ValueError, match="heading"):
        save_package(source, " ", "", [], tmp_path / "new")
    with pytest.raises(ValueError, match="Select"):
        save_package(source, "Heading", "", [], tmp_path / "new")
    assert not (tmp_path / "new").exists()


def test_changed_source_is_rejected_before_any_export(qapp, pdf_path, tmp_path):
    copied = tmp_path / "source.pdf"
    shutil.copyfile(pdf_path, copied)
    opened = PdfSource(copied)
    try:
        cap = opened.capture_area(3, QRectF(20, 20, 100, 100))
        with copied.open("ab") as stream:
            stream.write(b"\nchanged after opening\n")
        with pytest.raises(ValueError, match="changed"):
            save_package(opened, "Title", "", [cap], tmp_path / "out")
        assert not (tmp_path / "out").exists()
    finally:
        opened.close()


def test_mixed_types_reach_each_sources_metadata_and_prompt(source, tmp_path):
    captures = []
    for kind in ["commentary", "table", "financial_note", "unspecified"]:
        cap = source.capture_area(4, QRectF(20, 160, 385, 165))
        cap.content_type = kind
        captures.append(cap)
    saved = save_package(source, "Mixed evidence", "", captures, tmp_path)
    manifest = saved.manifest
    assert manifest["prompt"]["stage"] == "12-analyst-reading-brief"
    assert manifest["prompt"]["version"] == "1.1.0"
    assert [s["content_type"] for s in manifest["selections"]] == [c.content_type for c in captures]
    assert [s["content_type_origin"] for s in manifest["selections"]] == ["user_selected"] * 3 + ["not_specified"]
    prompt = saved.prompt
    for source_id, label, cap in zip(
        ["S001", "S002", "S003", "S004"],
        ["Commentary", "Table", "Financial note", "Mixed / unspecified"],
        captures,
    ):
        assert f"### Section D002 | physical PDF page 4 | {label}" in prompt
        assert "Section ID: D002; physical PDF page: 4" in prompt
        assert source_id not in prompt
        assert f"evidence/{source_id}.png" not in prompt
        assert cap.text in prompt
    assert "not_reviewed" == manifest["review"]["source_verification"]
    assert "Financial note" in saved.selected_text


def test_data_type_is_explicit_not_inferred_and_invalid_type_rejected(source, tmp_path):
    cap = source.capture_area(4, QRectF(20, 160, 385, 165))
    saved = save_package(source, "Financial note table", "", [cap], tmp_path)
    part = saved.manifest["selections"][0]
    assert part["content_type"] == "unspecified"
    assert part["content_type_origin"] == "not_specified"
    cap.content_type = "guessed_from_heading"
    with pytest.raises(ValueError, match="data type"):
        save_package(source, "Title", "", [cap], tmp_path / "invalid")
    assert not (tmp_path / "invalid").exists()


def test_table_crop_formats_markdown_columns_and_superscript_footnotes(source):
    prod_table = source.capture_area(4, QRectF(20, 175, 385, 153))
    assert "| Operation | Production range oz | FY27H1 oz | FY27H2 oz |" in prod_table.text
    assert "| MTR operation[^1] | 49,000 – 54,000 | 19,000 – 22,000 | 30,000 – 32,000 |" in prod_table.text
    assert "[^1] Expected production from MTR takes into account treatment of final calcine elements" in prod_table.text

    salient = source.capture_area(4, QRectF(438, 175, 383, 373))
    assert "| Salient features | Unit | FY26 | FY25 | Movement change % |" in salient.text
    assert "|  | ZAR/kg | 2,308,329 | 1,595,761 | 44.7 |" in salient.text


def test_clean_single_line_text():
    assert clean_single_line_text(None) == ""
    assert clean_single_line_text("") == ""
    assert clean_single_line_text("   ") == ""
    assert clean_single_line_text("STRATEGY AND \nTARGETS") == "STRATEGY AND TARGETS"
    assert clean_single_line_text("Some\tSubheading\r\nwith\t\tbreaks  ") == "Some Subheading with breaks"
    assert clean_single_line_text("Non-breaking\xa0space\xa0\xa0test") == "Non-breaking space test"


def test_save_package_sanitizes_heading_and_subheadings(source, tmp_path):
    width, height = source.size(3)
    cap = source.capture_area(3, QRectF(0, 0, width / 2, height))
    cap.subheading = "Subheading\twith\nnewlines  "
    output = save_package(
        source,
        "\tSTRATEGY AND \nTARGETS\r\n",
        "Question",
        [cap],
        tmp_path,
        subheading="Subheading\twith\nnewlines  ",
    )
    assert output.manifest["heading"] == "STRATEGY AND TARGETS"
    assert output.manifest["subheading"] == "Subheading with newlines"
    assert "STRATEGY AND TARGETS" in output.prompt
    assert "STRATEGY AND \nTARGETS" not in output.prompt


def test_sanitized_line_edit_and_heading_combo_box(qapp):
    from PySide6.QtWidgets import QApplication

    edit = SanitizedLineEdit()
    QApplication.clipboard().setText("Pasted\tText\r\nWith\nLine Breaks   ")
    edit.paste()
    assert edit.text() == "Pasted Text With Line Breaks"
    edit.deleteLater()

    combo = HeadingComboBox()
    QApplication.clipboard().setText("  Main \nHeading\tOptions  ")
    combo.lineEdit().paste()
    assert combo.lineEdit().text() == "Main Heading Options"
    assert combo.currentText() == "Main Heading Options"
    combo.deleteLater()


def test_shorten_section_name():
    assert shorten_section_name("") == ""
    assert shorten_section_name(None) == ""
    short = "01-D001-KEY-FEATURES"
    assert shorten_section_name(short, 32) == short
    long_name = "04-D002.3-D002.4-D002.5-D002.6-D002.7-D002.8-D002.9-MATERIAL-ISSUES-AND-RISKS-20261019-121220-b7c945b6"
    shortened = shorten_section_name(long_name, 32)
    assert len(shortened) <= 32
    assert shortened.endswith("...")
    assert shortened == "04-D002.3-D002.4-D002.5-D002..."


def test_sector_detection_and_prompts():
    from companies import find_company_dir
    from section_capture.packages import detect_sector_from_path, get_prompt_path
    from section_capture.report_map import get_orientation_path

    assert detect_sector_from_path("companies/mining/PAN/sources/doc.pdf") == "mining"
    assert detect_sector_from_path("companies/retail/LEW/sources/lewis-iar-2026.pdf") == "retail"
    assert detect_sector_from_path("C:\\Projects\\companies\\retail\\TRU\\sources\\TRU.pdf") == "retail"
    assert detect_sector_from_path("companies/finance/SBK/sources/report.pdf") == "finance"
    assert detect_sector_from_path("companies/reit/GRT/sources/report.pdf") == "reit"
    assert detect_sector_from_path("companies/property/RDF/sources/report.pdf") == "reit"
    assert detect_sector_from_path("random/path/report.pdf") is None

    pan_res = find_company_dir("PAN")
    assert pan_res is not None
    assert pan_res[0] == "mining"
    assert pan_res[1].name == "PAN"

    lew_res = find_company_dir("LEW")
    assert lew_res is not None
    assert lew_res[0] == "retail"
    assert lew_res[1].name == "LEW"

    mining_prompt = get_prompt_path("mining")
    assert mining_prompt.exists()
    assert "mining company" in mining_prompt.read_text(encoding="utf-8")

    retail_prompt = get_prompt_path("retail")
    assert retail_prompt.exists()
    retail_content = retail_prompt.read_text(encoding="utf-8")
    assert "retail and consumer credit company" in retail_content
    assert "merchandise sales" in retail_content.lower()

    retail_orient = get_orientation_path("retail")
    assert retail_orient.exists()
    assert "retail and consumer goods" in retail_orient.read_text(encoding="utf-8")

    reit_prompt = get_prompt_path("reit")
    assert reit_prompt.exists()
    reit_content = reit_prompt.read_text(encoding="utf-8")
    assert "Real Estate Investment Trust" in reit_content
    assert "DIPS" in reit_content or "distributable" in reit_content.lower()

    reit_orient = get_orientation_path("reit")
    assert reit_orient.exists()
    assert "Real Estate Investment Trust" in reit_orient.read_text(encoding="utf-8")

    it_prompt = get_prompt_path("it")
    assert it_prompt.exists()
    it_content = it_prompt.read_text(encoding="utf-8")
    assert "Information Technology" in it_content
    assert "recurring revenue" in it_content.lower()

    it_orient = get_orientation_path("it")
    assert it_orient.exists()
    assert "Information Technology" in it_orient.read_text(encoding="utf-8")


def test_clear_and_delete_section_in_db(tmp_path):
    from section_capture.db import (
        clear_section_llm_response,
        delete_section,
        get_section,
        insert_section,
        save_section_llm_response,
    )

    db_file = tmp_path / "analysis.sqlite"
    insert_section(
        package_id="test-pkg-clear",
        report_sha256="test-sha",
        section_number=1,
        section_id="01",
        name="01-test",
        heading="Test Heading",
        subheading=None,
        analyst_question=None,
        selected_text="Sample text",
        selections=[{"text": "Sample text"}],
        stored_questions=None,
        prompt="Sample prompt",
        manifest={"package_id": "test-pkg-clear", "review": {"model_brief": "not_run"}},
        db_path=db_file,
    )
    saved, _ = save_section_llm_response(
        "test-pkg-clear",
        "LLM Response text",
        response_time_seconds=12.5,
        cost_usd=0.005,
        db_path=db_file,
    )
    assert saved.llm_response == "LLM Response text"
    assert saved.response_time_seconds == 12.5

    cleared = clear_section_llm_response("test-pkg-clear", db_path=db_file)
    assert cleared is not None
    assert cleared.llm_response is None
    assert cleared.manifest["review"]["model_brief"] == "not_run"

    assert delete_section("test-pkg-clear", db_path=db_file) is True
    assert get_section("test-pkg-clear", db_path=db_file) is None


def test_stage1_and_stage2_db_persistence(tmp_path):
    from section_capture.db import (
        get_stage1_report,
        get_stage2_report,
        save_stage1_report,
        save_stage2_report,
        upsert_report,
    )

    db_file = tmp_path / "analysis.sqlite"
    upsert_report(
        sha256="test-sha-pipeline",
        filename="company-report.pdf",
        original_path="companies/retail/LEW/sources/company-report.pdf",
        db_path=db_file,
    )

    s1_init = get_stage1_report("test-sha-pipeline", db_path=db_file)
    assert s1_init is not None
    assert s1_init["stage1_prompt"] is None
    assert s1_init["stage1_response"] is None

    ok1 = save_stage1_report(
        "test-sha-pipeline",
        prompt="Stage 1 Forensic Prompt",
        response="Stage 1 Audit Determinations: Net Cash US$185.7m, Diluted 2,129.95m",
        db_path=db_file,
    )
    assert ok1 is True
    s1_saved = get_stage1_report("test-sha-pipeline", db_path=db_file)
    assert s1_saved["stage1_prompt"] == "Stage 1 Forensic Prompt"
    assert "Net Cash US$185.7m" in s1_saved["stage1_response"]
    assert s1_saved["stage1_updated_at"] is not None

    ok2 = save_stage2_report(
        "test-sha-pipeline",
        prompt="Stage 2 Valuation Prompt",
        response="Stage 2 Valuation Note: Target ZAR 112/share, Buy recommendation",
        db_path=db_file,
    )
    assert ok2 is True
    s2_saved = get_stage2_report("test-sha-pipeline", db_path=db_file)
    assert s2_saved["stage2_prompt"] == "Stage 2 Valuation Prompt"
    assert "Target ZAR 112/share" in s2_saved["stage2_response"]
    assert s2_saved["stage2_updated_at"] is not None


def test_new_company_dialog(qapp, tmp_path, pdf_path, monkeypatch):
    from section_capture.new_company_dialog import NewCompanyDialog
    from PySide6.QtWidgets import QDialog, QMessageBox
    import new_company

    tmp_companies = tmp_path / "companies"
    monkeypatch.setattr(new_company, "COMPANIES_DIR", tmp_companies)
    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)

    window = CaptureWindow(tmp_path)
    try:
        dummy_pdf = tmp_path / "Sample_Bank_FY26.pdf"
        dummy_pdf.write_bytes(pdf_path.read_bytes())

        dlg = NewCompanyDialog(window)
        assert dlg.create_btn.isEnabled() is False

        dlg.ticker_edit.setText("sbk")
        assert dlg.ticker_edit.text() == "SBK"
        assert dlg.create_btn.isEnabled() is True
        assert dlg.create_btn.text() == "Create Company Hub"

        dlg.name_edit.setText("Standard Bank Group Ltd")
        sec_idx = dlg.sector_combo.findData("finance")
        assert sec_idx >= 0
        dlg.sector_combo.setCurrentIndex(sec_idx)

        dlg.pdf_path_edit.setText(str(dummy_pdf))
        assert dlg.create_btn.text() == "Create & Open PDF"

        dlg._on_create()
        assert dlg.created_ticker == "SBK"
        assert dlg.created_sector == "finance"
        assert dlg.created_company_dir.exists()
        assert dlg.created_pdf_path.exists()
        assert dlg.created_pdf_path.name == "Sample_Bank_FY26.pdf"
        assert (dlg.created_company_dir / "models" / "config.py").exists()
        assert (dlg.created_company_dir / "models" / "sbk_sandbox.ipynb").exists()

        class MockDialogNoPdf:
            created_ticker = "MTN"
            created_sector = "telcos"
            created_company_dir = tmp_companies / "telcos" / "MTN"
            created_pdf_path = None
            def __init__(self, parent=None): pass
            def exec(self):
                return QDialog.DialogCode.Accepted

        monkeypatch.setattr("section_capture.new_company_dialog.NewCompanyDialog", MockDialogNoPdf)
        window.show_new_company_dialog()
        dlg.deleteLater()
    finally:
        window.close()
        window.deleteLater()


def test_sens_detection_and_date_parsing():
    from section_capture.db import detect_doc_type_and_date

    dt, d = detect_doc_type_and_date("companies/mining/ORN/sources/sens/20261019-ORN-ASX-JSE-Finalisation-of-Glencore.pdf")
    assert dt == "sens"
    assert d == "2026-10-19"

    dt, d = detect_doc_type_and_date("2026-10-28-ORN-SENS-Glencore-Drawdown.pdf")
    assert dt == "sens"
    assert d == "2026-10-28"

    dt, d = detect_doc_type_and_date("companies/mining/ORN/sources/20260917-ORN-ASX-JSE-Annual-Report-2026.pdf")
    assert dt == "annual_report"
    assert d == "2026-09-17"

    dt, d = detect_doc_type_and_date("Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf")
    assert dt == "annual_report"


def test_sens_parent_linking_and_questions_ledger_sync(tmp_path):
    from section_capture.db import (
        connect_db,
        get_linked_sens_reports,
        get_parent_report,
        insert_section,
        save_section_llm_response,
        upsert_report,
    )

    db_file = tmp_path / "test_sens.sqlite"
    parent_sha = "parent" + "0" * 58
    child_sha = "child1" + "0" * 58

    upsert_report(
        sha256=parent_sha,
        filename="Annual-Report-2026.pdf",
        original_path="/sources/Annual-Report-2026.pdf",
        questions_ledger="### Pending: Glencore facility CP satisfaction",
        db_path=db_file,
    )

    upsert_report(
        sha256=child_sha,
        filename="20261019-SENS-Glencore.pdf",
        original_path="/sources/sens/20261019-SENS-Glencore.pdf",
        parent_report_sha256=parent_sha,
        doc_type="sens",
        announcement_date="2026-10-19",
        db_path=db_file,
    )

    linked = get_linked_sens_reports(parent_sha, db_path=db_file)
    assert len(linked) == 1
    assert linked[0]["sha256"] == child_sha
    assert linked[0]["announcement_date"] == "2026-10-19"
    assert linked[0]["questions_ledger"] == "### Pending: Glencore facility CP satisfaction"

    parent_info = get_parent_report(child_sha, db_path=db_file)
    assert parent_info is not None
    assert parent_info["sha256"] == parent_sha

    sec = insert_section(
        package_id="sec-sens-001",
        report_sha256=child_sha,
        section_number=1,
        section_id="SENS-01",
        name="SENS-01-Glencore",
        heading="SENS: Finalisation of Glencore Funding",
        subheading=None,
        analyst_question=None,
        selected_text="US$40M Glencore facility now unconditional.",
        selections=[{"physical_page": 1, "bbox": [0, 0, 100, 100], "page_size_points": [500, 700]}],
        stored_questions="### Pending: Glencore facility CP satisfaction",
        prompt="prompt text",
        manifest={"schema_version": "1.0"},
        db_path=db_file,
    )

    llm_resp = (
        "## 1. Footnote Verification\n"
        "All CPs satisfied.\n\n"
        "## 4. Updated Open Questions Ledger\n\n"
        "- Q169 [Resolved]: Glencore facility unconditional on 19 Oct 2026.\n"
        "- Q172 [Resolved]: No covenant breach.\n\n"
        "## 5. Baseline Forecast Inputs\n"
        "US$40m debt added."
    )
    save_section_llm_response(sec.package_id, llm_resp, db_path=db_file)

    with connect_db(db_file) as conn:
        parent_q = conn.execute("SELECT questions_ledger FROM reports WHERE sha256 = ?", (parent_sha,)).fetchone()[0]
        assert "Q169 [Resolved]: Glencore facility unconditional" in parent_q


def test_stage1_multi_document_prompt_compilation():
    from workflow.export_stage1 import build_stage1_prompt_content

    primary_sections = [
        {
            "section_number": 1,
            "section_id": "D001",
            "heading": "Market context",
            "subheading": None,
            "analyst_question": None,
            "selected_text": "Overview of copper market.",
            "stored_questions_snapshot": "No questions yet.",
            "llm_response": "DeepSeek analysis of D001.",
        }
    ]

    sens_reports = [
        {
            "filename": "20261019-ORN-ASX-JSE-Finalisation-of-Glencore.pdf",
            "announcement_date": "2026-10-19",
            "sections": [
                {
                    "section_number": 1,
                    "section_id": "SENS-01",
                    "heading": "SENS: Glencore Funding Unconditional",
                    "subheading": None,
                    "analyst_question": "Check CP satisfaction.",
                    "selected_text": "US$40 million funding now unconditional.",
                    "stored_questions_snapshot": "Pending questions from AR.",
                    "llm_response": "DeepSeek analysis of SENS 1.",
                }
            ],
        }
    ]

    prompt = build_stage1_prompt_content(
        sections=primary_sections,
        company_title="Orion Minerals (ORN)",
        ticker="ORN",
        detected_sector="mining",
        filename="ORN-Annual-Report-2026.pdf",
        sens_reports=sens_reports,
    )

    assert "PART 1: PRIMARY FINANCIAL DISCLOSURE (`ORN-Annual-Report-2026.pdf` — 1 Sections)" in prompt
    assert "PART 2: SUBSEQUENT SENS & CONTINUOUS DISCLOSURE ANNOUNCEMENTS (1 Announcements)" in prompt
    assert "SENS ANNOUNCEMENT 1: `20261019-ORN-ASX-JSE-Finalisation-of-Glencore.pdf` (Date: 2026-10-19 — 1 Sections)" in prompt
    assert "US$40 million funding now unconditional" in prompt
    assert "Subsequent SENS Disclosures" in prompt


def test_sens_valuation_update_prompt_generation(tmp_path):
    from workflow.generate_sens_update import generate_sens_update_prompt
    from section_capture.db import save_stage2_report, upsert_report

    db_file = tmp_path / "analysis.sqlite"
    sha = "testorn" + "0" * 57

    baseline_note = (
        "# ORION MINERALS (ORN) - FINAL VALUATION NOTE\n"
        "| **12-Month JSE Target Price** | **R0.21** |\n"
        "| **Institutional Recommendation** | **SELL** |\n\n"
        "### Section 6: Actionable Portfolio Monitoring Triggers\n"
        "- Trigger 1: Glencore US$40M facility closing\n"
    )

    upsert_report(
        sha256=sha,
        filename="20260917-ORN-ASX-JSE-Annual-Report-2026.pdf",
        original_path="companies/mining/ORN/sources/20260917-ORN-ASX-JSE-Annual-Report-2026.pdf",
        db_path=db_file,
    )
    save_stage2_report(sha, response=baseline_note, db_path=db_file)

    sens_sha = "testsens" + "0" * 56
    upsert_report(
        sha256=sens_sha,
        filename="20261019-ORN-ASX-JSE-Finalisation-of-Glencore.pdf",
        original_path="companies/mining/ORN/sources/sens/20261019-ORN-ASX-JSE-Finalisation-of-Glencore.pdf",
        parent_report_sha256=sha,
        doc_type="sens",
        announcement_date="2026-10-19",
        db_path=db_file,
    )

    out_prompt = tmp_path / "ORN_FY26_stage2_sens_update_prompt.md"
    generate_sens_update_prompt(
        ticker="ORN",
        output_path=out_prompt,
        db_path=db_file,
    )

    assert out_prompt.exists()
    content = out_prompt.read_text(encoding="utf-8")
    assert "STAGE 2-U: INSTITUTIONAL VALUATION SENS UPDATE & RE-RATING" in content
    assert "20261019-ORN-ASX-JSE-Finalisation-of-Glencore.pdf" in content
    assert "| **12-Month JSE Target Price** | **R0.21** |" in content
    assert "We are adding a subsequent" in content
    assert "new updated valuation report" in content


def test_heading_combo_box_checkmark_and_clean_text():
    combo = HeadingComboBox()
    combo.set_options(["Highlights", "01. Financial Review", "02. Operational Review"])
    assert combo.count() == 3

    combo.set_options([("✓ Highlights", "Highlights"), "01. Financial Review", ("✓ 02. Operational Review", "02. Operational Review")])
    assert combo.itemText(0) == "✓ Highlights"
    assert combo.itemData(0) == "Highlights"

    combo.setCurrentIndex(0)
    combo._on_item_activated(0)
    assert combo.text() == "Highlights"

    combo.setCurrentIndex(1)
    combo._on_item_activated(1)
    assert combo.text() == "01. Financial Review"

    combo.setCurrentIndex(2)
    combo._on_item_activated(2)
    assert combo.text() == "02. Operational Review"

    combo.setText("✓ Capital Structure")
    assert combo.text() == "Capital Structure"


def test_smaller_font_words_not_corrupted_into_superscripts():
    cgr_pdf = Path("companies/construction/CGR/sources/Calgro-AFS-2026.pdf")
    if cgr_pdf.exists():
        src = PdfSource(cgr_pdf)
        try:
            cap = src.capture_area(21, QRectF(20, 60, 400, 500))
            assert "1. Segment information (continued)" in cap.text
            assert "[^co]" not in cap.text
            assert "[^continued]" not in cap.text
        finally:
            src.close()


def test_partition_stored_questions_eliminates_duplicates():
    from section_capture.packages import partition_stored_questions

    sample_ledger = (
        "## Open Questions Ledger — after D002\n\n"
        "### Pending: D003 (Balance Sheet)\n"
        "- Q1 [High]: Agree actual Total Equity to implied R1,546m. [D002, p.12]\n"
        "- Q2 [High]: Extract total interest-bearing borrowings. [D002, p.12]\n\n"
        "### Pending: D005 (Cash Flow)\n"
        "- Q9 [Medium]: Verify operating cash flow conversion. [D002, p.15]\n"
        "- Q10 [Low]: Check debt covenants. [D002, p.16]\n"
    )

    relevant, other = partition_stored_questions(sample_ledger, ["D003"])
    assert len(relevant) == 2
    assert "Q1 [High]: Agree actual Total Equity" in relevant[0]
    assert "Q2 [High]: Extract total interest-bearing borrowings" in relevant[1]

    assert "Q1 [High]: Agree actual Total Equity" not in other
    assert "Q2 [High]: Extract total interest-bearing borrowings" not in other
    assert "### Pending: D003" not in other
    assert "### Pending: D005 (Cash Flow)" in other
    assert "Q9 [Medium]: Verify operating cash flow conversion" in other
    assert "Q10 [Low]: Check debt covenants" in other
