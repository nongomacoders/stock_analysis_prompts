import hashlib
import json
import shutil
import zipfile

import pytest
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QImage
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
