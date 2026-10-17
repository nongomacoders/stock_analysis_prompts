import copy
import hashlib
import json
from types import SimpleNamespace

import pytest
from PySide6.QtCore import QRectF

from section_capture.map_dialog import ReportMapDialog
from section_capture.packages import save_package
from section_capture.report_map import load_cached_map, report_overview, save_map, scan_report, validate_map
from section_capture.window import CaptureWindow
from section_capture.pdf_source import PdfSource


def test_real_scan_keeps_shared_page_boundaries_and_all_primary_statements(source):
    mapping = scan_report(source)
    by_kind = {s['kind']: s for s in mapping['sections']}
    assert mapping['scanned_physical_pages'] == list(range(1, 55))
    assert mapping['status'] == 'automatic_draft'
    assert mapping['source_sha256'] == source.sha256
    assert by_kind['highlights']['start']['physical_page'] == 2
    assert by_kind['ceo_commentary']['start']['physical_page'] == 5
    assert by_kind['financial_statements']['end']['physical_page'] == 19
    assert by_kind['financial_statements']['end']['location'] == 'left'
    assert by_kind['financial_notes']['start']['physical_page'] == 19
    assert by_kind['financial_notes']['start']['location'] == 'right'
    assert by_kind['financial_notes']['end']['physical_page'] == 36
    assert by_kind['glossary']['end']['location'] == 'left'
    assert by_kind['corporate_information']['start']['location'] == 'right'
    assert {s['kind'] for s in mapping['primary_statement_sightings']} == {
        'financial_position', 'profit_or_loss', 'other_comprehensive_income', 'cash_flows', 'changes_in_equity'}
    assert {'kind':'changes_in_equity','physical_page':19,'location':'left'} in mapping['primary_statement_sightings']
    assert mapping['unclassified_physical_pages'] == [1, 54]
    assert all(s['start']['printed_label'] is None for s in mapping['sections'])


def fake_source(pages):
    return SimpleNamespace(plumber=SimpleNamespace(pages=pages), page_count=len(pages),
                           sha256='a'*64, path=SimpleNamespace(name='unknown.pdf'))


def test_body_references_and_image_only_pages_do_not_invent_sections():
    words = [{'text':w,'size':8,'top':40,'x0':10,'x1':100} for w in
             'NOTES TO THE SUMMARISED CONSOLIDATED ANNUAL FINANCIAL STATEMENTS'.split()]
    page = SimpleNamespace(width=800, extract_words=lambda **kwargs: words)
    blank = SimpleNamespace(width=800, extract_words=lambda **kwargs: [])
    mapping = scan_report(fake_source([page, blank]))
    assert len(mapping['sections']) == 1
    assert mapping['sections'][0]['kind'] == 'unclassified'
    assert mapping['unclassified_physical_pages'] == [1, 2]
    assert mapping['primary_statement_sightings'] == []


def test_cancelled_scan_does_not_claim_complete_coverage():
    page = SimpleNamespace(width=800, extract_words=lambda **kwargs: [])
    with pytest.raises(InterruptedError, match='cancelled'):
        scan_report(fake_source([page, page]), lambda done, total: False)


def test_cache_rejects_wrong_document_incomplete_ranges_and_false_confirmation(source, tmp_path):
    mapping = copy.deepcopy(source.report_map)
    assert mapping is not None
    db_file = save_map(mapping, tmp_path)
    assert db_file.name == 'analysis.sqlite'
    assert load_cached_map(source.sha256, source.page_count, tmp_path)['map_id'] == mapping['map_id']
    assert load_cached_map('b'*64, source.page_count, tmp_path) is None
    assert load_cached_map(source.sha256, source.page_count-1, tmp_path) is None
    bad = copy.deepcopy(mapping)
    bad['sections'][1]['start']['physical_page'] = 3
    with pytest.raises(ValueError, match='gaps'):
        validate_map(bad, source.sha256, source.page_count)
    bad = copy.deepcopy(mapping)
    bad['status'] = 'source_verified'
    with pytest.raises(ValueError, match='status'):
        validate_map(bad, source.sha256, source.page_count)


def test_request_context_uses_crop_region_not_page_alone(source):
    width, height = source.size(19)
    left = {'source_id':'S001','physical_page':19,'page_size_points':[width,height],
            'bbox':[0,0,width/2,height]}
    text = report_overview(source.report_map, [left])
    statements = next(line for line in text.splitlines() if '| Primary financial statements |' in line)
    notes = next(line for line in text.splitlines() if '| Financial notes |' in line)
    assert 'Partial selected evidence: D005 (p. 19)' in statements
    assert 'Not included here' in notes
    right = {**left, 'bbox':[width/2,0,width,height]}
    text = report_overview(source.report_map, [right])
    notes = next(line for line in text.splitlines() if '| Financial notes |' in line)
    assert 'Partial selected evidence: D006 (p. 19)' in notes


def test_export_snapshots_map_and_marks_later_content_not_supplied(source, tmp_path):
    cap = source.capture_area(3, QRectF(20, 65, 190, 475))
    saved = save_package(source, 'Highlights', '', [cap], tmp_path)
    manifest = saved.manifest
    assert manifest['document_map']['source_sha256'] == source.sha256
    assert len(manifest['prompt']['report_map_sha256']) == 64
    assert len(manifest['prompt']['report_overview_sha256']) == 64
    prompt = saved.prompt
    assert '| Highlights | 2 full – 4 full | Partial selected evidence: D002 (p. 3)' in prompt
    assert '| Financial notes | 19 right – 36 full | Not included here' in prompt
    assert manifest['review']['model_brief'] == 'not_run'
    assert manifest['review']['source_verification'] == 'not_reviewed'


def test_export_without_map_is_explicit_not_a_fake_outline(source, tmp_path):
    source.report_map = None
    cap = source.capture_area(3, QRectF(20, 65, 190, 475))
    saved = save_package(source, 'Highlights', '', [cap], tmp_path)
    assert saved.manifest['document_map'] is None
    assert 'No report map is supplied' in saved.prompt


def test_map_dialog_copy_is_navigation_only_and_preserves_pending_capture(qapp, pdf_path, tmp_path):
    window = CaptureWindow(tmp_path)
    window.show()
    assert not window.map_action.isEnabled()
    assert window.open_pdf(pdf_path)
    cap = window.source.capture_area(3, QRectF(20, 65, 190, 475))
    window.selection_changed(cap)
    before = copy.deepcopy(window.source.report_map)
    dialog = ReportMapDialog(window.source, window.scan_report_map, window)
    dialog.show()
    dialog.copy_button.click()
    assert 'CEO' in qapp.clipboard().text()
    assert 'Pending:' in qapp.clipboard().text()
    assert window.pending is cap
    assert window.source.report_map == before
    dialog.close()
    window._reset_section()
    window.close()


def test_cancelled_rescan_preserves_previous_cached_map(qapp, pdf_path, tmp_path, monkeypatch):
    window = CaptureWindow(tmp_path)
    assert window.open_pdf(pdf_path)
    before = copy.deepcopy(window.source.report_map)
    def cancel(*args):
        raise InterruptedError('cancelled')
    monkeypatch.setattr('section_capture.window.scan_report', cancel)
    assert window.scan_report_map() is False
    assert window.source.report_map == before
    window.close()


def test_open_uncached_report_scans_before_export(qapp, pdf_path, tmp_path, monkeypatch):
    calls = []
    def opened_without_cache(path):
        source = PdfSource(path)
        source.report_map = None
        return source
    reference = load_cached_map('62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd', 54)
    def scanned(source, progress):
        assert progress(0, 54)
        calls.append(source.sha256)
        return copy.deepcopy(reference)
    monkeypatch.setattr('section_capture.window.PdfSource', opened_without_cache)
    monkeypatch.setattr('section_capture.window.scan_report', scanned)
    monkeypatch.setattr('section_capture.window.save_map', lambda mapping, root=None: save_map(mapping, tmp_path/'maps'))
    window = CaptureWindow(tmp_path/'packs')
    assert window.open_pdf(pdf_path)
    assert calls == [window.source.sha256]
    assert window.source.report_map['status'] == 'automatic_draft'
    assert (tmp_path/'maps'/'analysis.sqlite').exists()
    window.close()

