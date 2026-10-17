import hashlib
import json
import shutil
import zipfile

import pytest
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QImage
from PySide6.QtTest import QTest

from section_capture.packages import save_package
from section_capture.pdf_source import PdfSource
from section_capture.window import CaptureWindow


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


def test_multi_page_package_is_durable_source_linked_and_zip_matches(source, tmp_path):
    width, height = source.size(3)
    first = source.capture_area(3, QRectF(0, 0, width/2, height))
    first.printed_label = "2"
    second = source.capture_area(6, QRectF(0, 0, width/2, height))
    output = save_package(source, "../Production: costs / FY26", "What changed and why?", [first, second], tmp_path)
    assert output.parent == tmp_path.resolve()
    manifest = json.loads((output/'manifest.json').read_text(encoding='utf-8'))
    assert [p['physical_page'] for p in manifest['selections']] == [3, 6]
    assert manifest['source']['sha256'] == source.sha256
    assert manifest['selections'][0]['printed_label_origin'] == 'user_entered_unverified'
    assert manifest['review']['model_brief'] == 'not_run'
    assert manifest['review']['source_verification'] == 'not_reviewed'
    assert manifest['review']['analyst_review'] == 'not_recorded'
    assert manifest['task'] == 'analyst_reading_brief'
    assert manifest['response_format'] == 'markdown'
    assert 'output_schema_sha256' not in manifest['prompt']
    assert not (output/'output.schema.json').exists()
    for part in manifest['selections']:
        assert hashlib.sha256((output/part['image']).read_bytes()).hexdigest() == part['image_sha256']
        assert not QImage(str(output/part['image'])).isNull()
        assert hashlib.sha256((output/part['text']).read_bytes()).hexdigest() == part['text_sha256']
    prompt = (output/'prompt.md').read_text(encoding='utf-8')
    assert manifest['package_id'] in prompt and 'S001' in prompt and 'S002' in prompt
    assert "What changed and why?" in prompt
    assert 'physical PDF page 3' in prompt and source.path.name in prompt
    assert not list(tmp_path.glob('.section-staging-*'))
    with zipfile.ZipFile(output.with_suffix('.zip')) as z:
        assert z.read('prompt.md') == (output/'prompt.md').read_bytes()
        assert z.read('manifest.json') == (output/'manifest.json').read_bytes()
        assert set(z.namelist()) == {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}
    # New save is a new version, never an overwrite.
    again = save_package(source, "../Production: costs / FY26", "", [first], tmp_path)
    assert again != output and output.exists()


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


def test_failed_image_write_leaves_no_completed_pack(source, tmp_path, monkeypatch):
    cap = source.capture_area(3, QRectF(20, 20, 150, 100))
    monkeypatch.setattr(QImage, 'save', lambda *args: False)
    with pytest.raises(OSError, match="image"):
        save_package(source, "Title", "", [cap], tmp_path)
    assert list(tmp_path.iterdir()) == []


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


def test_gui_text_drag_and_save_current_selection(qapp, pdf_path, tmp_path):
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
    assert output is not None and (output/'manifest.json').exists()
    assert not window.captures and window.pending is None
    window.copy_prompt()
    assert qapp.clipboard().text() == (output/'prompt.md').read_text(encoding='utf-8')
    assert window.copy_button.isEnabled()
    window.close()


def test_mixed_types_reach_each_sources_metadata_and_prompt(source, tmp_path):
    captures = []
    for kind in ['commentary', 'table', 'financial_note', 'unspecified']:
        cap = source.capture_area(4, QRectF(20, 160, 385, 165))
        cap.content_type = kind
        captures.append(cap)
    folder = save_package(source, 'Mixed evidence', '', captures, tmp_path)
    manifest = json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    assert manifest['prompt']['stage'] == '12-analyst-reading-brief'
    assert manifest['prompt']['version'] == '1.1.0'
    assert [s['content_type'] for s in manifest['selections']] == [c.content_type for c in captures]
    assert [s['content_type_origin'] for s in manifest['selections']] == ['user_selected'] * 3 + ['not_specified']
    prompt = (folder/'prompt.md').read_text(encoding='utf-8')
    for source_id, label, cap in zip(['S001', 'S002', 'S003', 'S004'],
                                    ['Commentary', 'Table', 'Financial note', 'Mixed / unspecified'], captures):
        assert f'### {source_id} | physical PDF page 4 | {label}' in prompt
        assert f'attached image: evidence/{source_id}.png' in prompt
        assert cap.text in prompt
    assert 'not_reviewed' == manifest['review']['source_verification']
    assert 'Financial note' in (folder/'selected-text.txt').read_text(encoding='utf-8')


def test_data_type_is_explicit_not_inferred_and_invalid_type_rejected(source, tmp_path):
    cap = source.capture_area(4, QRectF(20, 160, 385, 165))
    folder = save_package(source, 'Financial note table', '', [cap], tmp_path)
    part = json.loads((folder/'manifest.json').read_text(encoding='utf-8'))['selections'][0]
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
    folder = window.save_section()
    selections = json.loads((folder/'manifest.json').read_text(encoding='utf-8'))['selections']
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
    folder = window.save_section()
    saved_text = (folder / 'evidence/S001.txt').read_text(encoding='utf-8')
    assert saved_text.startswith('### FY27 Production Guidance')
    assert 'Analyst note: verify H2 ramp-up.' in saved_text
    assert 'Analyst note: verify H2 ramp-up.' in (folder / 'prompt.md').read_text(encoding='utf-8')
    window.close()
