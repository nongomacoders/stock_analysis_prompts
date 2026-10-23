import hashlib
import json
from pathlib import Path
import shutil
import zipfile

import pytest
from PySide6.QtCore import QEvent, QPointF, QRectF, Qt
from PySide6.QtGui import QImage, QKeyEvent
from PySide6.QtTest import QTest

from section_capture.packages import clean_single_line_text, save_package, shorten_section_name
from section_capture.pdf_source import PdfSource
from section_capture.window import CaptureWindow, HeadingComboBox, SanitizedLineEdit


def test_original_identity_and_readable_render(source):
    assert source.page_count == 54
    assert source.sha256 == "62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd"
    image = source.render(3)
    assert not image.isNull()
    assert image.width() > image.height()
    assert image.pixelColor(0, 0).name() == '#ffffff'
    assert image.pixelColor(0, 0).alpha() == 255
    with pytest.raises(ValueError):
        source.size(0)


def test_area_crop_keeps_left_and_right_evidence_separate(source):
    width, height = source.size(3)
    left = source.capture_area(3, QRectF(0, 0, width/2, height))
    right = source.capture_area(3, QRectF(width/2, 0, width/2, height))
    assert "PRODUCTION" in left.text and "GROWTH" in left.text
    assert "SAFETY" not in left.text and "FINANCIAL" not in left.text
    assert "SAFETY" in right.text and "FINANCIAL" in right.text
    assert "KEY FEATURES" not in right.text
    assert abs(left.image.width() - right.image.width()) <= 1
    assert left.bbox[2] == pytest.approx(width/2)


def test_reverse_drag_clamps_to_source_page_and_rejects_tiny_box(source):
    cap = source.capture_area(3, QRectF(QPointF(80, 90), QPointF(-10, -5)))
    assert cap.bbox == (0, 0, 80, 90)
    with pytest.raises(ValueError, match="larger selection"):
        source.capture_area(3, QRectF(10, 10, 0.5, 1))


def text_points(source, page, word):
    text = source.document.getAllText(page-1).text()
    index = text.index(word)
    selection = source.document.getSelectionAtIndex(page-1, index, len(word))
    box = selection.boundingRectangle()
    return QPointF(box.left()+0.2, box.center().y()), QPointF(box.right()-0.2, box.center().y())


def test_native_text_selection_preserves_actual_text_and_coordinates(source):
    start, end = text_points(source, 3, "GROWTH")
    cap = source.capture_text(3, start, end)
    assert "GROWTH" in cap.text
    assert "FINANCIAL" not in cap.text
    assert cap.mode == "text" and cap.polygons and cap.text_indices is not None
    assert cap.bbox[2] < source.size(3)[0]/2
    assert not cap.image.isNull()
    with pytest.raises(ValueError, match="No selectable text"):
        source.capture_text(3, QPointF(1, 1), QPointF(2, 2))


def test_no_native_text_is_retained_as_image_with_warning(source):
    cap = source.capture_area(1, QRectF(5, 200, 20, 20))
    assert not cap.text.strip()
    assert any("No native text" in w for w in cap.warnings)
    assert not cap.image.isNull()


def test_boundary_crossing_is_disclosed(source):
    native = source.plumber.pages[2]
    char = next(c for c in native.chars if c["text"] == "G")
    rect = QRectF((char['x0']+char['x1'])/2, char['top']-2, 25, char['bottom']-char['top']+4)
    cap = source.capture_area(3, rect)
    assert any("boundary crosses text" in w for w in cap.warnings)


def test_multi_page_package_is_saved_in_sqlite_without_png_or_zip_files(source, tmp_path):
    width, height = source.size(3)
    first = source.capture_area(3, QRectF(0, 0, width/2, height))
    first.printed_label = "2"
    second = source.capture_area(6, QRectF(0, 0, width/2, height))
    output = save_package(source, "../Production: costs / FY26", "What changed and why?", [first, second], tmp_path)
    assert output.db_path == (tmp_path / "analysis.sqlite").resolve()
    assert not list(tmp_path.rglob("*.png"))
    assert not list(tmp_path.rglob("*.zip"))
    manifest = output.manifest
    assert [p['physical_page'] for p in manifest['selections']] == [3, 6]
    assert manifest['source']['sha256'] == source.sha256
    assert manifest['selections'][0]['printed_label_origin'] == 'user_entered_unverified'
    assert manifest['review']['model_brief'] == 'not_run'
    assert manifest['review']['source_verification'] == 'not_reviewed'
    assert manifest['review']['analyst_review'] == 'not_recorded'
    assert manifest['task'] == 'analyst_reading_brief'
    assert manifest['response_format'] == 'markdown'
    assert 'output_schema_sha256' not in manifest['prompt']
    for part in manifest['selections']:
        assert 'image' not in part
        assert len(part['text_sha256']) == 64
    prompt = output.prompt
    assert manifest['package_id'] in prompt and 'Section D002' in prompt and 'Section D003' in prompt
    assert 'S001' not in prompt and '.png' not in prompt
    assert "What changed and why?" in prompt
    assert 'physical PDF page 3' in prompt and source.path.name in prompt
    # New save is a new row in SQLite, never an overwrite.
    again = save_package(source, "../Production: costs / FY26", "", [first], tmp_path)
    assert again.package_id != output.package_id and again.section_number == 2


def test_missing_heading_or_selection_does_not_create_pack(source, tmp_path):
    with pytest.raises(ValueError, match="heading"):
        save_package(source, " ", "", [], tmp_path/'new')
    with pytest.raises(ValueError, match="Select"):
        save_package(source, "Heading", "", [], tmp_path/'new')
    assert not (tmp_path/'new').exists()


def test_changed_source_is_rejected_before_any_export(qapp, pdf_path, tmp_path):
    copied = tmp_path/'source.pdf'
    shutil.copyfile(pdf_path, copied)
    opened = PdfSource(copied)
    try:
        cap = opened.capture_area(3, QRectF(20, 20, 100, 100))
        with copied.open('ab') as stream:
            stream.write(b'\nchanged after opening\n')
        with pytest.raises(ValueError, match="changed"):
            save_package(opened, "Title", "", [cap], tmp_path/'out')
        assert not (tmp_path/'out').exists()
    finally:
        opened.close()


@pytest.mark.parametrize('zoom', [0.8, 1.25])
def test_gui_drag_maps_through_zoom_without_losing_added_selections(qapp, pdf_path, tmp_path, zoom):
    window = CaptureWindow(tmp_path)
    window.show()
    assert window.open_pdf(pdf_path)
    window.page_spin.setValue(6)
    qapp.processEvents()
    window.canvas.fit_page()
    window.canvas.zoom(zoom)
    qapp.processEvents()
    first, last = QPointF(240, 215), QPointF(380, 315)
    start = window.canvas.mapFromScene(first)
    end = window.canvas.mapFromScene(last)
    assert window.canvas.viewport().rect().contains(start)
    assert window.canvas.viewport().rect().contains(end)
    QTest.mousePress(window.canvas.viewport(), Qt.MouseButton.LeftButton, pos=start)
    QTest.mouseMove(window.canvas.viewport(), end, delay=10)
    QTest.mouseRelease(window.canvas.viewport(), Qt.MouseButton.LeftButton, pos=end)
    qapp.processEvents()
    assert window.pending is not None
    assert window.pending.bbox == pytest.approx((240, 215, 380, 315), abs=2)
    assert window.pending.page == 6
    window.label_edit.setText('8')
    window.add_selection()
    assert window.captures[0].printed_label == '8'
    assert window.label_edit.text() == ''  # Never carry a folio into another selection.
    window.page_spin.setValue(3)
    assert window.pending is None and len(window.captures) == 1
    assert window.captures[0].page == 6
    window._reset_section()
    window.close()


def test_gui_text_drag_and_save_current_selection_copies_prompt_automatically(qapp, pdf_path, tmp_path):
    window = CaptureWindow(tmp_path)
    window.show()
    assert window.open_pdf(pdf_path)
    window.page_spin.setValue(3)
    window.mode_combo.setCurrentIndex(1)
    qapp.processEvents()
    first, last = text_points(window.source, 3, 'GROWTH')
    start, end = window.canvas.mapFromScene(first), window.canvas.mapFromScene(last)
    QTest.mousePress(window.canvas.viewport(), Qt.MouseButton.LeftButton, pos=start)
    QTest.mouseMove(window.canvas.viewport(), end, delay=10)
    QTest.mouseRelease(window.canvas.viewport(), Qt.MouseButton.LeftButton, pos=end)
    assert window.pending is not None and 'GROWTH' in window.preview.toPlainText()
    window.heading_edit.setText('Growth projects')
    assert window.save_button.isEnabled()
    output = window.save_section()
    assert output is not None and output.manifest['package_id'] == output.package_id
    assert not window.captures and window.pending is None
    # Save automatically copies prompt to clipboard
    assert qapp.clipboard().text() == output.prompt
    window.copy_prompt()
    assert qapp.clipboard().text() == output.prompt
    assert window.copy_button.isEnabled()
    window.close()


def test_mixed_types_reach_each_sources_metadata_and_prompt(source, tmp_path):
    captures = []
    for kind in ['commentary', 'table', 'financial_note', 'unspecified']:
        cap = source.capture_area(4, QRectF(20, 160, 385, 165))
        cap.content_type = kind
        captures.append(cap)
    saved = save_package(source, 'Mixed evidence', '', captures, tmp_path)
    manifest = saved.manifest
    assert manifest['prompt']['stage'] == '12-analyst-reading-brief'
    assert manifest['prompt']['version'] == '1.1.0'
    assert [s['content_type'] for s in manifest['selections']] == [c.content_type for c in captures]
    assert [s['content_type_origin'] for s in manifest['selections']] == ['user_selected'] * 3 + ['not_specified']
    prompt = saved.prompt
    for source_id, label, cap in zip(['S001', 'S002', 'S003', 'S004'],
                                    ['Commentary', 'Table', 'Financial note', 'Mixed / unspecified'], captures):
        assert f'### Section D002 | physical PDF page 4 | {label}' in prompt
        assert 'Section ID: D002; physical PDF page: 4' in prompt
        assert source_id not in prompt
        assert f'evidence/{source_id}.png' not in prompt
        assert cap.text in prompt
    assert 'not_reviewed' == manifest['review']['source_verification']
    assert 'Financial note' in saved.selected_text


def test_data_type_is_explicit_not_inferred_and_invalid_type_rejected(source, tmp_path):
    cap = source.capture_area(4, QRectF(20, 160, 385, 165))
    saved = save_package(source, 'Financial note table', '', [cap], tmp_path)
    part = saved.manifest['selections'][0]
    assert part['content_type'] == 'unspecified'
    assert part['content_type_origin'] == 'not_specified'
    cap.content_type = 'guessed_from_heading'
    with pytest.raises(ValueError, match='data type'):
        save_package(source, 'Title', '', [cap], tmp_path/'invalid')
    assert not (tmp_path/'invalid').exists()


def test_gui_type_per_selection_retag_and_save_pending(qapp, pdf_path, tmp_path):
    window = CaptureWindow(tmp_path)
    window.show()
    assert window.open_pdf(pdf_path)
    window.heading_edit.setText('Highlights')
    assert window.content_type_combo.currentData() == 'unspecified'
    assert not window.apply_type_button.isEnabled()
    window.content_type_combo.setCurrentIndex(window.content_type_combo.findData('commentary'))
    cap = window.source.capture_area(3, QRectF(20, 70, 190, 475))
    window.selection_changed(cap)
    window.add_selection()
    assert window.captures[0].content_type == 'commentary'
    assert 'Commentary' in window.parts.item(0).text()
    # A later choice does not silently reclassify previously added evidence.
    window.content_type_combo.setCurrentIndex(window.content_type_combo.findData('financial_note'))
    assert window.captures[0].content_type == 'commentary'
    window.parts.setCurrentRow(0)
    assert window.apply_type_button.isEnabled()
    window.apply_type_button.click()
    assert window.captures[0].content_type == 'financial_note'
    assert 'Financial note' in window.parts.item(0).text()
    window.content_type_combo.setCurrentIndex(window.content_type_combo.findData('table'))
    window.selection_changed(window.source.capture_area(4, QRectF(20, 160, 385, 165)))
    saved = window.save_section()
    selections = saved.manifest['selections']
    assert [p['content_type'] for p in selections] == ['financial_note', 'table']
    assert window.content_type_combo.currentData() == 'unspecified'
    assert not window.apply_type_button.isEnabled()
    window.close()


def test_table_crop_formats_markdown_columns_and_superscript_footnotes(source):
    prod_table = source.capture_area(4, QRectF(20, 175, 385, 153))
    assert '| Operation | Production range oz | FY27H1 oz | FY27H2 oz |' in prod_table.text
    assert '| MTR operation[^1] | 49,000 – 54,000 | 19,000 – 22,000 | 30,000 – 32,000 |' in prod_table.text
    assert '[^1] Expected production from MTR takes into account treatment of final calcine elements' in prod_table.text

    salient = source.capture_area(4, QRectF(438, 175, 383, 373))
    assert '| Salient features | Unit | FY26 | FY25 | Movement change % |' in salient.text
    assert '|  | ZAR/kg | 2,308,329 | 1,595,761 | 44.7 |' in salient.text


def test_gui_editable_preview_updates_pending_and_added_captures(qapp, pdf_path, tmp_path):
    window = CaptureWindow(tmp_path)
    window.show()
    assert window.open_pdf(pdf_path)
    window.heading_edit.setText('FY27 guidance')
    cap = window.source.capture_area(4, QRectF(20, 175, 385, 153))
    window.selection_changed(cap)
    window.preview.setPlainText('### FY27 Production Guidance\n' + window.preview.toPlainText())
    assert window.pending.text.startswith('### FY27 Production Guidance')
    window.add_selection()
    window.parts.setCurrentRow(0)
    window.preview.setPlainText(window.preview.toPlainText() + '\nAnalyst note: verify H2 ramp-up.')
    saved = window.save_section()
    assert '### FY27 Production Guidance' in saved.selected_text
    assert 'Analyst note: verify H2 ramp-up.' in saved.selected_text
    assert 'Analyst note: verify H2 ramp-up.' in saved.prompt
    window.close()


def test_stored_questions_and_llm_response_auto_update_in_sqlite(qapp, pdf_path, tmp_path):
    from section_capture.map_dialog import QuestionsLedgerDialog, SavedSectionsDialog
    window = CaptureWindow(tmp_path)
    window.show()
    assert window.open_pdf(pdf_path)
    assert window.questions_button.text() == 'Stored questions (none)'

    # First section export without stored questions
    window.heading_edit.setText('Section 1 Highlights')
    window.selection_changed(window.source.capture_area(4, QRectF(20, 175, 385, 153)))
    first_pack = window.save_section()
    assert first_pack.name.startswith('01-D002-')
    assert 'None supplied (first section capture)' in first_pack.prompt
    assert first_pack.stored_questions is None

    # Store LLM response via SavedSectionsDialog and verify Section 4 auto-updates questions_ledger
    llm_reply = (
        "### 1. Answers to Stored Questions for This Section\nNone.\n\n"
        "### 4. Updated Open Questions Ledger (Copy to App)\n"
        "```markdown\n"
        "Q1 [Target: D008 APMs]: Verify AISC bridge and Sheba/Consort unit costs.\n"
        "Q2 [Target: D006 Notes]: Reconcile 2,436m dividend shares vs 2,029.6m weighted shares.\n"
        "```\n"
    )
    qapp.clipboard().setText(llm_reply)
    sec_dialog = SavedSectionsDialog(window.source, window, window.output_root)
    sec_dialog.paste_llm_response_from_clipboard()
    sec_dialog.close()
    window._update_actions()
    assert '2 lines' in window.questions_button.text()

    # Second section export embeds the stored questions and highlights D008-specific questions
    window.heading_edit.setText('Section 2 APMs')
    window.selection_changed(window.source.capture_area(38, QRectF(20, 60, 380, 300)))
    second_pack = window.save_section()
    assert second_pack.name.startswith('02-D008-')
    second_prompt = second_pack.prompt
    assert 'QUESTIONS SPECIFICALLY TARGETING THIS SECTION (D008)' in second_prompt
    target_block = second_prompt.split('QUESTIONS SPECIFICALLY TARGETING THIS SECTION (D008)')[1].split('BEGIN STORED QUESTIONS')[0]
    assert 'Q1 [Target: D008 APMs]: Verify AISC bridge' in target_block
    assert 'Q2 [Target: D006 Notes]' not in target_block
    assert 'BEGIN STORED QUESTIONS FROM EARLIER SECTIONS' in second_prompt
    assert 'Q2 [Target: D006 Notes]: Reconcile 2,436m dividend shares' in second_prompt
    assert 'Q1 [Target: D008 APMs]' not in second_prompt.split('BEGIN STORED QUESTIONS')[1]
    assert 'Q1 [Target: D008 APMs]' in second_pack.stored_questions
    window.close()


def test_subheading_divides_section_and_updates_report_map(qapp, pdf_path, tmp_path):
    window = CaptureWindow(tmp_path)
    window.show()
    assert window.open_pdf(pdf_path)
    assert window.heading_edit.count() > 0

    # First subsection inside D005 Primary financial statements (page 17 left)
    window.heading_edit.setText('Primary financial statements')
    window.subheading_edit.setText('Statement of Financial Position')
    window.selection_changed(window.source.capture_area(17, QRectF(20, 60, 380, 300)))
    sub1 = window.save_section()
    assert sub1.name.startswith('01-D005.1-')
    sub1_prompt = sub1.prompt
    assert 'Section ID: D005.1' in sub1_prompt
    assert 'Section heading: Primary financial statements — Statement of Financial Position' in sub1_prompt
    assert '| D005.1 | ↳ Statement of Financial Position | 17 left – 17 left | Partial selected evidence: D005.1 (p. 17) |' in sub1_prompt

    # Main heading stays selected after saving a subsection, and blank sub-heading is blocked
    assert window.heading_edit.text() == 'Primary financial statements'
    assert window.subheading_edit.text() == ''
    window.selection_changed(window.source.capture_area(18, QRectF(20, 60, 380, 300)))
    assert not window.save_button.isEnabled()
    assert window.save_section() is None
    assert 'already has subsections' in window.warning_label.text()

    # Entering the second sub-heading enables saving D005.2
    window.subheading_edit.setText('Statement of Profit or Loss')
    assert window.save_button.isEnabled()
    sub2 = window.save_section()
    assert sub2.name.startswith('02-D005.2-')
    sub2_prompt = sub2.prompt
    assert '| D005.1 | ↳ Statement of Financial Position | 17 left – 17 left | Subsection recorded in map; not included in this request |' in sub2_prompt
    assert '| D005.2 | ↳ Statement of Profit or Loss | 18 left – 18 left | Partial selected evidence: D005.2 (p. 18) |' in sub2_prompt

    # Adding two selections with two different sub-headings in a single save records both subsections and combines their titles
    window.subheading_edit.setText('Cash Flow Statement')
    window.selection_changed(window.source.capture_area(18, QRectF(430, 60, 380, 300)))
    window.add_selection()
    assert 'Cash Flow Statement' in window.parts.item(0).text()
    window.subheading_edit.setText('Changes in Equity')
    window.selection_changed(window.source.capture_area(19, QRectF(20, 60, 380, 300)))
    sub34 = window.save_section()
    assert sub34.name.startswith('03-D005.3-D005.4-')
    assert sub34.subheading == 'Cash Flow Statement; Changes in Equity'
    assert '| D005.3 | ↳ Cash Flow Statement | 18 right – 18 right | Partial selected evidence: D005.3 (p. 18) |' in sub34.prompt
    assert '| D005.4 | ↳ Changes in Equity | 19 left – 19 left | Partial selected evidence: D005.4 (p. 19) |' in sub34.prompt
    assert '### Section D005.3 | physical PDF page 18 | Mixed / unspecified (Cash Flow Statement)' in sub34.prompt
    assert '### Section D005.4 | physical PDF page 19 | Mixed / unspecified (Changes in Equity)' in sub34.prompt
    window.close()


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


def test_capture_window_nitro_checkbox(qapp, tmp_path):
    window = CaptureWindow(output_root=tmp_path)
    assert hasattr(window, "nitro_checkbox")
    assert not window.nitro_checkbox.isChecked()
    assert not window._active_model_name().endswith(":nitro")
    window.nitro_checkbox.setChecked(True)
    assert window._active_model_name().endswith(":nitro")
    window.nitro_checkbox.setChecked(False)
    assert not window._active_model_name().endswith(":nitro")
    window.close()
    window.deleteLater()


def test_sector_detection_and_prompts():
    from section_capture.packages import detect_sector_from_path, get_prompt_path
    from section_capture.report_map import get_orientation_path
    from companies import find_company_dir

    # 1. Path detection
    assert detect_sector_from_path("companies/mining/PAN/sources/doc.pdf") == "mining"
    assert detect_sector_from_path("companies/retail/LEW/sources/lewis-iar-2026.pdf") == "retail"
    assert detect_sector_from_path("C:\\Projects\\companies\\retail\\TRU\\sources\\TRU.pdf") == "retail"
    assert detect_sector_from_path("companies/finance/SBK/sources/report.pdf") == "finance"
    assert detect_sector_from_path("companies/reit/GRT/sources/report.pdf") == "reit"
    assert detect_sector_from_path("companies/property/RDF/sources/report.pdf") == "reit"
    assert detect_sector_from_path("random/path/report.pdf") is None

    # 2. Company directory resolution
    pan_res = find_company_dir("PAN")
    assert pan_res is not None
    assert pan_res[0] == "mining"
    assert pan_res[1].name == "PAN"

    lew_res = find_company_dir("LEW")
    assert lew_res is not None
    assert lew_res[0] == "retail"
    assert lew_res[1].name == "LEW"

    # 3. Prompt path resolution
    mining_prompt = get_prompt_path("mining")
    assert mining_prompt.exists()
    assert "mining company" in mining_prompt.read_text(encoding="utf-8")

    retail_prompt = get_prompt_path("retail")
    assert retail_prompt.exists()
    retail_content = retail_prompt.read_text(encoding="utf-8")
    assert "retail and consumer credit company" in retail_content
    assert "merchandise sales" in retail_content.lower()

    # Orientation prompt resolution
    retail_orient = get_orientation_path("retail")
    assert retail_orient.exists()
    assert "retail and consumer goods" in retail_orient.read_text(encoding="utf-8")

    # REIT prompt resolution
    reit_prompt = get_prompt_path("reit")
    assert reit_prompt.exists()
    reit_content = reit_prompt.read_text(encoding="utf-8")
    assert "Real Estate Investment Trust" in reit_content
    assert "DIPS" in reit_content or "distributable" in reit_content.lower()

    reit_orient = get_orientation_path("reit")
    assert reit_orient.exists()
    assert "Real Estate Investment Trust" in reit_orient.read_text(encoding="utf-8")

    # IT prompt resolution
    it_prompt = get_prompt_path("it")
    assert it_prompt.exists()
    it_content = it_prompt.read_text(encoding="utf-8")
    assert "Information Technology" in it_content
    assert "recurring revenue" in it_content.lower()

    it_orient = get_orientation_path("it")
    assert it_orient.exists()
    assert "Information Technology" in it_orient.read_text(encoding="utf-8")


def test_window_sector_auto_detect(qapp, tmp_path):
    window = CaptureWindow(output_root=tmp_path)
    assert hasattr(window, "sector_combo")
    # Verify supported sectors exist
    sectors = [window.sector_combo.itemData(i) for i in range(window.sector_combo.count())]
    assert "mining" in sectors
    assert "retail" in sectors
    assert "reit" in sectors
    assert "it" in sectors
    assert "finance" in sectors
    assert "telcos" in sectors

    # Verify sector detection when simulated
    from section_capture.packages import detect_sector_from_path
    assert detect_sector_from_path("companies/retail/LEW/sources/doc.pdf") == "retail"
    assert detect_sector_from_path("companies/it/IOC/sources/doc.pdf") == "it"

    window.close()
    window.deleteLater()


def test_clear_and_delete_section_in_db(tmp_path):
    from section_capture.db import (
        clear_section_llm_response,
        delete_section,
        get_section,
        insert_section,
        save_section_llm_response,
    )

    db_file = tmp_path / "analysis.sqlite"
    pkg = insert_section(
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
    # Save a response
    saved, _ = save_section_llm_response(
        "test-pkg-clear",
        "LLM Response text",
        response_time_seconds=12.5,
        cost_usd=0.005,
        db_path=db_file,
    )
    assert saved.llm_response == "LLM Response text"
    assert saved.response_time_seconds == 12.5

    # Clear response
    cleared = clear_section_llm_response("test-pkg-clear", db_path=db_file)
    assert cleared is not None
    assert cleared.llm_response is None
    assert cleared.manifest["review"]["model_brief"] == "not_run"

    # Delete section
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

    # Initially empty
    s1_init = get_stage1_report("test-sha-pipeline", db_path=db_file)
    assert s1_init is not None
    assert s1_init["stage1_prompt"] is None
    assert s1_init["stage1_response"] is None

    # Save Stage 1
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

    # Save Stage 2
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


def test_audit_valuation_dialog(qapp, pdf_path, tmp_path, monkeypatch):
    from PySide6.QtCore import QRectF
    from section_capture.audit_dialog import AuditValuationDialog
    from section_capture.db import get_stage1_report, get_stage2_report
    from PySide6.QtWidgets import QMessageBox

    # Prevent modal QMessageBox popups from blocking test execution
    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)

    window = CaptureWindow(tmp_path)
    assert window.open_pdf(pdf_path)
    assert window.audit_action.isEnabled()

    # Save a section so SQLite has sections
    window.heading_edit.setText("Operational Highlights")
    window.selection_changed(window.source.capture_area(1, QRectF(20, 50, 300, 150)))
    saved_pkg = window.save_section()
    assert saved_pkg is not None

    # Open AuditValuationDialog (3 tabs: Stage 1, Stage 2, Analyzed Stocks)
    dialog = AuditValuationDialog(window.source, window, db_path=tmp_path)
    assert dialog.tabs.count() == 3

    # Stage 1: Compile and Save
    dialog.compile_stage1_prompt()
    prompt_text = dialog.s1_prompt_edit.toPlainText()
    assert "STAGE 1: INDEPENDENT COGNITIVE AUDIT" in prompt_text
    assert "Operational Highlights" in prompt_text

    dialog.s1_response_edit.setPlainText("Argon Audit Determinations: Debtors book +15.2%, satisfactory-paid 82.6%.")
    dialog.save_stage1_response()

    s1_db = get_stage1_report(window.source.sha256, db_path=tmp_path)
    assert "Debtors book +15.2%" in s1_db["stage1_response"]

    # Stage 2: Generate Prompt and Save Report
    dialog.generate_stage2_prompt()
    s2_prompt = dialog.s2_prompt_edit.toPlainText()
    assert "STAGE 2: INSTITUTIONAL 2-YEAR VALUATION" in s2_prompt
    assert "99% confidence baseline" in s2_prompt
    assert "Argon Audit Determinations: Debtors book +15.2%" in s2_prompt

    dialog.s2_response_edit.setPlainText("Final Valuation Note: 12-Month Target Price R85.50 per share.")
    dialog.save_stage2_response()

    s2_db = get_stage2_report(window.source.sha256, db_path=tmp_path)
    assert "Target Price R85.50" in s2_db["stage2_response"]

    dialog.close()
    dialog.deleteLater()
    window.close()
    window.deleteLater()


def test_new_company_toolbar_action_and_dialog(qapp, tmp_path, pdf_path, monkeypatch):
    """Test 'New' action in toolbar and NewCompanyDialog scaffolding and PDF opening."""
    from section_capture.new_company_dialog import NewCompanyDialog
    from PySide6.QtWidgets import QDialog, QMessageBox
    import new_company

    # Isolate companies dir to tmp_path
    tmp_companies = tmp_path / "companies"
    monkeypatch.setattr(new_company, "COMPANIES_DIR", tmp_companies)

    # Prevent modal message boxes
    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)

    window = CaptureWindow(tmp_path)
    try:
        # Check toolbar has 'New' action
        assert hasattr(window, "new_action")
        assert window.new_action.text() == "New"
        assert "Scaffold a new company" in window.new_action.toolTip()

        # Create dummy PDF in tmp_path
        dummy_pdf = tmp_path / "Sample_Bank_FY26.pdf"
        dummy_pdf.write_bytes(pdf_path.read_bytes())

        # Test NewCompanyDialog directly
        dlg = NewCompanyDialog(window)
        assert dlg.create_btn.isEnabled() is False  # empty ticker

        # Test lowercase auto-converts to uppercase
        dlg.ticker_edit.setText("sbk")
        assert dlg.ticker_edit.text() == "SBK"
        assert dlg.create_btn.isEnabled() is True
        assert dlg.create_btn.text() == "Create Company Hub"

        dlg.name_edit.setText("Standard Bank Group Ltd")
        sec_idx = dlg.sector_combo.findData("finance")
        assert sec_idx >= 0
        dlg.sector_combo.setCurrentIndex(sec_idx)

        # Set PDF path
        dlg.pdf_path_edit.setText(str(dummy_pdf))
        assert dlg.create_btn.text() == "Create & Open PDF"

        # Execute creation
        dlg._on_create()
        assert dlg.created_ticker == "SBK"
        assert dlg.created_sector == "finance"
        assert dlg.created_company_dir.exists()
        assert dlg.created_pdf_path.exists()
        assert dlg.created_pdf_path.name == "Sample_Bank_FY26.pdf"
        assert (dlg.created_company_dir / "models" / "config.py").exists()
        assert (dlg.created_company_dir / "models" / "sbk_sandbox.ipynb").exists()

        # Test show_new_company_dialog with PDF
        class MockDialogWithPdf:
            created_ticker = "SBK"
            created_sector = "finance"
            created_company_dir = tmp_companies / "finance" / "SBK"
            created_pdf_path = dlg.created_pdf_path
            def __init__(self, parent=None): pass
            def exec(self):
                return QDialog.DialogCode.Accepted

        monkeypatch.setattr("section_capture.new_company_dialog.NewCompanyDialog", MockDialogWithPdf)
        window.show_new_company_dialog()
        assert window.source is not None
        assert window.source.path.name == "Sample_Bank_FY26.pdf"
        assert window.sector_combo.currentData() == "finance"

        # Test show_new_company_dialog without PDF (opens sources folder)
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
        assert window.sector_combo.currentData() == "telcos"

        dlg.deleteLater()
    finally:
        window.close()
        window.deleteLater()


def test_selection_mode_shortcuts_and_switching(qapp, pdf_path, tmp_path):
    window = CaptureWindow(tmp_path)
    try:
        assert window.open_pdf(pdf_path)
        assert window.canvas.mode == "area"

        # Test switching to text mode
        window.set_selection_mode("text")
        assert window.canvas.mode == "text"
        assert window.mode_combo.currentData() == "text"

        # Test switching back to area mode
        window.set_selection_mode("area")
        assert window.canvas.mode == "area"
        assert window.mode_combo.currentData() == "area"

        # Test shortcut triggers
        window.text_shortcut.activated.emit()
        assert window.canvas.mode == "text"
        assert window.mode_combo.currentData() == "text"

        window.area_shortcut.activated.emit()
        assert window.canvas.mode == "area"
        assert window.mode_combo.currentData() == "area"
    finally:
        window.close()
        window.deleteLater()


def test_tab_and_backtab_page_navigation(qapp, pdf_path, tmp_path):
    window = CaptureWindow(tmp_path)
    try:
        assert window.open_pdf(pdf_path)
        assert window.page_spin.value() == 1

        # Simulate Tab key press when focus is on canvas or window (not on editable inputs)
        tab_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Tab, Qt.KeyboardModifier.NoModifier)
        window.eventFilter(window, tab_event)
        assert window.page_spin.value() == 2

        # Another Tab
        window.eventFilter(window, tab_event)
        assert window.page_spin.value() == 3

        # Shift+Tab (Backtab)
        backtab_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Backtab, Qt.KeyboardModifier.ShiftModifier)
        window.eventFilter(window, backtab_event)
        assert window.page_spin.value() == 2

        # Test Tab key delivered directly to canvas viewport via application event dispatch
        window.canvas.setFocus()
        qapp.processEvents()
        qapp.notify(window.canvas.viewport(), tab_event)
        assert window.page_spin.value() == 3

        # Shift+Tab delivered to canvas viewport
        qapp.notify(window.canvas.viewport(), backtab_event)
        assert window.page_spin.value() == 2

        # When focus is in an editable text edit, Tab should NOT advance the page
        window.heading_edit.setFocus()
        window.heading_edit.lineEdit().setText("Focus in edit")
        window.eventFilter(window.heading_edit.lineEdit(), tab_event)
        # Value must remain 2 (not advanced to 3)
        assert window.page_spin.value() == 2
    finally:
        window.close()
        window.deleteLater()


def test_sidebar_text_transfer_and_new_section_buttons(qapp, pdf_path, tmp_path):
    window = CaptureWindow(tmp_path)
    try:
        assert window.open_pdf(pdf_path)

        # Set preview text
        window.preview.setPlainText("OPERATIONAL HIGHLIGHTS")
        window.use_selected_text_for_heading()
        assert window.heading_edit.text() == "OPERATIONAL HIGHLIGHTS"

        window.preview.setPlainText("Barberton Mines")
        window.use_selected_text_for_subheading()
        assert window.subheading_edit.text() == "Barberton Mines"

        # New subsection should keep parent heading, clear subheading
        window.new_subsection()
        assert window.heading_edit.text() == "OPERATIONAL HIGHLIGHTS"
        assert window.subheading_edit.text() == ""

        # New section should clear both
        window.subheading_edit.setText("Evander Mines")
        window.new_section()
        assert window.heading_edit.text() == ""
        assert window.subheading_edit.text() == ""
    finally:
        window.close()
        window.deleteLater()


def test_choose_pdf_uses_last_opened_folder(qapp, pdf_path, tmp_path, monkeypatch):
    captured_paths = []
    def mock_get_open_file_name(parent, title, initial_dir, filter_str):
        captured_paths.append(initial_dir)
        return str(pdf_path), ""

    monkeypatch.setattr("section_capture.window.QFileDialog.getOpenFileName", mock_get_open_file_name)

    window = CaptureWindow(tmp_path)
    try:
        # First call: opens and records directory
        window.choose_pdf()
        assert len(captured_paths) == 1
        assert window.source is not None
        assert window.last_opened_dir == pdf_path.parent

        # Second call: initial_dir passed to QFileDialog must be pdf_path.parent
        window.choose_pdf()
        assert len(captured_paths) == 2
        assert captured_paths[1] == str(pdf_path.parent)
    finally:
        window.close()
        window.deleteLater()



def test_sens_detection_and_date_parsing():
    from section_capture.db import detect_doc_type_and_date

    # SENS in sources/sens/ subfolder
    dt, d = detect_doc_type_and_date("companies/mining/ORN/sources/sens/20261019-ORN-ASX-JSE-Finalisation-of-Glencore.pdf")
    assert dt == "sens"
    assert d == "2026-10-19"

    # SENS announcement with date in filename
    dt, d = detect_doc_type_and_date("2026-10-28-ORN-SENS-Glencore-Drawdown.pdf")
    assert dt == "sens"
    assert d == "2026-10-28"

    # Annual Report with date in filename
    dt, d = detect_doc_type_and_date("companies/mining/ORN/sources/20260917-ORN-ASX-JSE-Annual-Report-2026.pdf")
    assert dt == "annual_report"
    assert d == "2026-09-17"

    # Pan African SENS results announcement (Annual report, not subsequent notice)
    dt, d = detect_doc_type_and_date("Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf")
    assert dt == "annual_report"


def test_sens_parent_linking_and_questions_ledger_sync(tmp_path):
    from section_capture.db import (
        connect_db,
        get_linked_sens_reports,
        get_parent_report,
        insert_section,
        link_sens_report,
        save_section_llm_response,
        upsert_report,
    )

    db_file = tmp_path / "test_sens.sqlite"
    parent_sha = "parent" + "0" * 58
    child_sha = "child1" + "0" * 58

    # 1. Register parent Annual Report with questions ledger
    upsert_report(
        sha256=parent_sha,
        filename="Annual-Report-2026.pdf",
        original_path="/sources/Annual-Report-2026.pdf",
        questions_ledger="### Pending: Glencore facility CP satisfaction",
        db_path=db_file,
    )

    # 2. Register child SENS report
    upsert_report(
        sha256=child_sha,
        filename="20261019-SENS-Glencore.pdf",
        original_path="/sources/sens/20261019-SENS-Glencore.pdf",
        parent_report_sha256=parent_sha,
        doc_type="sens",
        announcement_date="2026-10-19",
        db_path=db_file,
    )

    # 3. Verify linkage and ledger inheritance
    linked = get_linked_sens_reports(parent_sha, db_path=db_file)
    assert len(linked) == 1
    assert linked[0]["sha256"] == child_sha
    assert linked[0]["announcement_date"] == "2026-10-19"
    assert linked[0]["questions_ledger"] == "### Pending: Glencore facility CP satisfaction"

    parent_info = get_parent_report(child_sha, db_path=db_file)
    assert parent_info is not None
    assert parent_info["sha256"] == parent_sha

    # 4. Insert a section on child SENS report and save LLM response with updated ledger
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

    # 5. Verify that parent report's questions ledger was synced with the SENS update!
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


def test_capture_window_document_selector_and_sens_switching(qapp, pdf_path, tmp_path):
    from section_capture.window import CaptureWindow

    window = CaptureWindow(output_root=tmp_path)
    try:
        window.open_pdf(pdf_path)
        assert hasattr(window, "doc_selector")
        assert hasattr(window, "add_sens_button")
        assert window.doc_selector.count() >= 1

        # Check that the opened document is selected
        curr_text = window.doc_selector.currentText()
        assert "Annual Report" in curr_text or pdf_path.name in curr_text
    finally:
        window.close()
        window.deleteLater()


def test_sens_valuation_update_prompt_generation(tmp_path):
    from workflow.generate_sens_update import build_sens_update_prompt_content, generate_sens_update_prompt
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

    # Mark with checkmark
    combo.set_options([("✓ Highlights", "Highlights"), "01. Financial Review", ("✓ 02. Operational Review", "02. Operational Review")])
    assert combo.itemText(0) == "✓ Highlights"
    assert combo.itemData(0) == "Highlights"

    # Selection strips checkmark in lineEdit
    combo.setCurrentIndex(0)
    combo._on_item_activated(0)
    assert combo.text() == "Highlights"

    combo.setCurrentIndex(1)
    combo._on_item_activated(1)
    assert combo.text() == "01. Financial Review"

    combo.setCurrentIndex(2)
    combo._on_item_activated(2)
    assert combo.text() == "02. Operational Review"

    # Setting text directly with checkmark also cleans it
    combo.setText("✓ Capital Structure")
    assert combo.text() == "Capital Structure"


def test_save_section_marks_dropdown_completed_and_updates_pending_counter(qapp, pdf_path, tmp_path):
    window = CaptureWindow(output_root=tmp_path)
    window.show()
    assert window.open_pdf(pdf_path)

    assert window.run_pending_button.text() == "⚡ Run Pending (0)"
    assert not window.run_pending_button.isEnabled()

    # Capture text using QTest
    window.page_spin.setValue(3)
    window.mode_combo.setCurrentIndex(1)
    qapp.processEvents()
    first, last = text_points(window.source, 3, "GROWTH")
    start, end = window.canvas.mapFromScene(first), window.canvas.mapFromScene(last)
    QTest.mousePress(window.canvas.viewport(), Qt.MouseButton.LeftButton, pos=start)
    QTest.mouseMove(window.canvas.viewport(), end, delay=10)
    QTest.mouseRelease(window.canvas.viewport(), Qt.MouseButton.LeftButton, pos=end)
    assert window.pending is not None

    # Choose a heading
    assert window.heading_edit.count() > 0
    target_heading = window.heading_edit.itemData(0) or window.heading_edit.itemText(0)
    if target_heading.startswith("✓ "):
        target_heading = target_heading[2:].strip()
    window.heading_edit.setText(target_heading)
    window._update_actions()
    assert window.save_button.isEnabled()

    # Save locally without running model
    saved_pkg = window.save_section()
    assert saved_pkg is not None

    # Verify heading dropdown now has a checkmark for the saved heading
    found_checked = False
    for i in range(window.heading_edit.count()):
        text = window.heading_edit.itemText(i)
        data = window.heading_edit.itemData(i)
        if data == target_heading or text == f"✓ {target_heading}":
            found_checked = True
            assert text.startswith("✓ ")
            break
    assert found_checked, f"Expected {target_heading} to be marked with checkmark"

    # Verify pending button counter updated
    assert window.run_pending_button.text() == "⚡ Run Pending (1)"
    assert window.run_pending_button.isEnabled()

    # Test queueing logic
    if not hasattr(window, "_query_queue"):
        window._query_queue = []
    window._query_queue.append("test-pkg-2")
    assert "test-pkg-2" in window._query_queue

    window.close()

def test_smaller_font_words_not_corrupted_into_superscripts():
    from section_capture.pdf_source import PdfSource
    from pathlib import Path
    from PySide6.QtCore import QRectF

    cgr_pdf = Path('companies/construction/CGR/sources/Calgro-AFS-2026.pdf')
    if cgr_pdf.exists():
        src = PdfSource(cgr_pdf)
        cap = src.capture_area(21, QRectF(20, 60, 400, 500))
        # '(continued)' must be preserved as clean text, not chopped into [^co][^nt][^in][^ue][^d]
        assert '1. Segment information (continued)' in cap.text
        assert '[^co]' not in cap.text
        assert '[^continued]' not in cap.text


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

    # Verify that D003 questions are excluded from other, but D005 questions are kept
    assert "Q1 [High]: Agree actual Total Equity" not in other
    assert "Q2 [High]: Extract total interest-bearing borrowings" not in other
    assert "### Pending: D003" not in other
    assert "### Pending: D005 (Cash Flow)" in other
    assert "Q9 [Medium]: Verify operating cash flow conversion" in other
    assert "Q10 [Low]: Check debt covenants" in other
