import copy
from types import SimpleNamespace

import pytest
from PySide6.QtCore import QRectF

from section_capture.packages import save_package
from section_capture.report_map import (
    assign_section_ids,
    build_manual_section_map,
    insert_section_into_report_map,
    load_cached_map,
    matching_section_ids,
    preview_inserted_section_id,
    register_subsection,
    report_overview,
    save_map,
    scan_report,
    section_requires_subheading,
    validate_map,
)
from section_capture.window import CaptureWindow


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
    text = report_overview(source.report_map, [left], sector='mining')
    statements = next(line for line in text.splitlines() if '| Primary financial statements |' in line)
    notes = next(line for line in text.splitlines() if '| Financial notes |' in line)
    assert 'Partial selected evidence: D005 (p. 19)' in statements
    assert 'Not included here' in notes
    right = {**left, 'bbox':[width/2,0,width,height]}
    text = report_overview(source.report_map, [right], sector='mining')
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


def test_build_manual_section_map_contiguous(source):
    sections_input = [
        {"title": "Operations Review", "start_page": 10},
        {"title": "Financial Results", "start_page": 30},
    ]
    mapping = build_manual_section_map(source, sections_input)
    assert mapping["status"] == "manual_outline"
    assert len(mapping["sections"]) == 2
    assert not any(s["title"] == "Cover / Overview" for s in mapping["sections"])
    assert mapping["sections"][0]["title"] == "Operations Review"
    assert mapping["sections"][0]["start"]["physical_page"] == 10
    assert mapping["sections"][0]["end"]["physical_page"] == 29
    assert mapping["sections"][1]["title"] == "Financial Results"
    assert mapping["sections"][1]["start"]["physical_page"] == 30
    assert mapping["sections"][1]["end"]["physical_page"] == source.page_count


def test_section_requires_subheading_refinement(source):
    mapping = {
        'sections': [
            {
                'section_id': 'D001',
                'title': 'Operational Review',
                'start': {'physical_page': 1, 'location': 'full'},
                'end': {'physical_page': 20, 'location': 'full'},
                'subsections': [
                    {'subsection_id': 'D001.1', 'title': 'Barberton Mines'}
                ]
            },
            {
                'section_id': 'D002',
                'title': 'Mineral Resources',
                'start': {'physical_page': 21, 'location': 'full'},
                'end': {'physical_page': 54, 'location': 'full'},
                'subsections': []
            }
        ]
    }
    part_in_d002 = [{'physical_page': 30, 'page_size_points': [500, 500], 'bbox': [10, 10, 400, 400]}]
    req = section_requires_subheading(mapping, heading="Mineral Resources", selections=part_in_d002)
    assert req is None

    part_in_d001 = [{'physical_page': 5, 'page_size_points': [500, 500], 'bbox': [10, 10, 400, 400]}]
    req = section_requires_subheading(mapping, heading="Operational Review", selections=part_in_d001)
    assert req == "D001 (D001.1)"


def test_disambiguate_company_vs_consolidated_statements():
    mapping = {
        'sections': [
            {
                'section_id': 'D005',
                'title': 'Consolidated statement of cash flows',
                'start': {'physical_page': 18, 'location': 'full'},
                'end': {'physical_page': 76, 'location': 'full'},
                'subsections': [
                    {'subsection_id': 'D005.1', 'title': 'Note 1'}
                ]
            },
            {
                'section_id': 'D009',
                'title': 'Statement of changes in equity',
                'start': {'physical_page': 78, 'location': 'full'},
                'end': {'physical_page': 78, 'location': 'full'},
                'subsections': []
            },
            {
                'section_id': 'D010',
                'title': 'Statement of cash flows',
                'start': {'physical_page': 78, 'location': 'full'},
                'end': {'physical_page': 78, 'location': 'full'},
                'subsections': []
            }
        ]
    }
    part_on_p78 = [{'physical_page': 78, 'page_size_points': [500, 500], 'bbox': [10, 10, 400, 400]}]
    part_on_p18 = [{'physical_page': 18, 'page_size_points': [500, 500], 'bbox': [10, 10, 400, 400]}]

    req_78 = section_requires_subheading(mapping, heading="Statement of cash flows", selections=part_on_p78)
    assert req_78 is None
    ids_78 = matching_section_ids(mapping, selections=part_on_p78, heading="Statement of cash flows")
    assert ids_78 == ['D010']

    assert section_requires_subheading(mapping, heading="✓ Statement of cash flows", selections=part_on_p78) is None
    assert matching_section_ids(mapping, selections=part_on_p78, heading="✓ Statement of cash flows") == ['D010']

    assert section_requires_subheading(mapping, heading="Statement of cash flows", selections=[]) is None
    assert matching_section_ids(mapping, selections=[], heading="Statement of cash flows") == ['D010']

    req_18 = section_requires_subheading(mapping, heading="Consolidated statement of cash flows", selections=part_on_p18)
    assert req_18 == "D005 (D005.1)"
    ids_18 = matching_section_ids(mapping, selections=part_on_p18, heading="Consolidated statement of cash flows")
    assert ids_18 == ['D005']

    registered = register_subsection(mapping, "Company Cash Note 1", part_on_p78, heading="Statement of cash flows")
    assert registered == ["D010.1"]
    sec_d010 = next(s for s in mapping['sections'] if s['section_id'] == 'D010')
    assert len(sec_d010['subsections']) == 1
    assert sec_d010['subsections'][0]['title'] == "Company Cash Note 1"

    sec_d005 = next(s for s in mapping['sections'] if s['section_id'] == 'D005')
    for i in range(2, 22):
        sec_d005['subsections'].append({'subsection_id': f'D005.{i}', 'title': f'Note {i}'})
    req_many = section_requires_subheading(mapping, heading="Consolidated statement of cash flows", selections=part_on_p18)
    assert req_many == "D005 (D005.1 – D005.21)"


def test_assign_section_ids_preserves_existing_and_generates_ins_suffix():
    initial_items = [
        {"title": "Overview", "start_page": 1, "section_id": None},
        {"title": "Operations", "start_page": 10, "section_id": None},
        {"title": "Financials", "start_page": 30, "section_id": None},
    ]
    ids = assign_section_ids(initial_items)
    assert ids == ["D001", "D002", "D003"]

    in_flight_items = [
        {"title": "Overview", "start_page": 1, "section_id": "D001"},
        {"title": "Operations", "start_page": 10, "section_id": "D002"},
        {"title": "Mineral Resources (Inserted)", "start_page": 20, "section_id": None},
        {"title": "Financials", "start_page": 30, "section_id": "D003"},
    ]
    ids2 = assign_section_ids(in_flight_items)
    assert ids2 == ["D001", "D002", "D002-ins", "D003"]

    multi_insert = [
        {"title": "Overview", "start_page": 1, "section_id": "D001"},
        {"title": "Operations", "start_page": 10, "section_id": "D002"},
        {"title": "Mineral Resources", "start_page": 15, "section_id": "D002-ins"},
        {"title": "Consort Mine (Second Insert)", "start_page": 20, "section_id": None},
        {"title": "Financials", "start_page": 30, "section_id": "D003"},
    ]
    ids3 = assign_section_ids(multi_insert)
    assert ids3 == ["D001", "D002", "D002-ins", "D002-ins2", "D003"]


def test_build_manual_section_map_with_inserted_section(source):
    existing_sections = [
        {"title": "Highlights", "start_page": 1},
        {"title": "CEO Statement", "start_page": 5},
        {"title": "Mineral Resources", "start_page": 15, "section_id": "D002-ins"},
        {"title": "Financial Statements", "start_page": 25},
    ]
    mapping = build_manual_section_map(source, existing_sections)
    assert mapping["status"] == "manual_outline"
    assert len(mapping["sections"]) == 4
    sec_ids = [s["section_id"] for s in mapping["sections"]]
    assert sec_ids == ["D001", "D002", "D002-ins", "D003"]
    assert mapping["sections"][0]["start"]["physical_page"] == 1
    assert mapping["sections"][0]["end"]["physical_page"] == 4
    assert mapping["sections"][1]["start"]["physical_page"] == 5
    assert mapping["sections"][1]["end"]["physical_page"] == 14
    assert mapping["sections"][2]["start"]["physical_page"] == 15
    assert mapping["sections"][2]["end"]["physical_page"] == 24
    assert mapping["sections"][3]["start"]["physical_page"] == 25
    assert mapping["sections"][3]["end"]["physical_page"] == source.page_count


def test_multiple_sections_sharing_same_start_page(source):
    sections = [
        {"title": "Overview", "start_page": 1},
        {"title": "Consolidated Statement of Profit or Loss and Other Comprehensive Income", "start_page": 45},
        {"title": "Consolidated Statement of Financial Position", "start_page": 45},
        {"title": "Notes to Financial Statements", "start_page": 50},
    ]
    mapping = build_manual_section_map(source, sections)
    assert len(mapping["sections"]) == 4
    assert mapping["sections"][1]["title"] == "Consolidated Statement of Profit or Loss and Other Comprehensive Income"
    assert mapping["sections"][1]["start"]["physical_page"] == 45
    assert mapping["sections"][1]["end"]["physical_page"] == 49
    assert mapping["sections"][2]["title"] == "Consolidated Statement of Financial Position"
    assert mapping["sections"][2]["start"]["physical_page"] == 45
    assert mapping["sections"][2]["end"]["physical_page"] == 49
    assert mapping["sections"][3]["start"]["physical_page"] == 50

    cand_id, desc = preview_inserted_section_id(mapping, start_page=45, page_count=source.page_count)
    assert "Shares start page 45" in desc
    assert cand_id == "D002-ins"

    updated, new_id = insert_section_into_report_map(
        mapping,
        title="Consolidated Statement of Cash Flows",
        start_page=45,
        page_count=source.page_count,
    )
    assert new_id == "D002-ins"
    assert any(s["title"] == "Consolidated Statement of Cash Flows" and s["start"]["physical_page"] == 45 for s in updated["sections"])


def test_capture_window_model_status_bar(qapp, tmp_path, monkeypatch):
    monkeypatch.delenv("OPENROUTER_MODEL", raising=False)
    window = CaptureWindow(tmp_path / "packs")
    try:
        assert hasattr(window, "model_status_label")
        assert "DeepSeek Flash" in window.model_status_label.text()
        assert window.centralWidget() is window.one_shot_view
        assert not hasattr(window, "canvas")
    finally:
        window.close()
        window.deleteLater()
