from types import SimpleNamespace
import pytest

from section_capture.capture_planner import heading_profile, plan_capture_groups, partition_detected_ranges


def words(*headings):
    result = []
    for y, size, text in headings:
        for i, token in enumerate(text.split()):
            result.append(dict(text=token, top=y, x0=25+i*30, size=size))
    result.extend(dict(text='body', top=400+i, x0=25, size=8) for i in range(30))
    return result


def profile(title=''):
    return dict(heading=title, topic_key=title.lower(), heading_evidence=[], mixed_topics_on_page=False)


def caps(n, chars=1000):
    return [SimpleNamespace(page=i+1, text='x'*chars) for i in range(n)]


def test_specific_note_heading_and_continued_header_are_same_topic():
    first = heading_profile(words((100,15,'6 Financial risk management'),(125,11.5,'6.1 Credit risk'),(160,10,'Purchased book debts')),800)
    next_page = heading_profile(words((100,15,'6 Financial risk management continued'),(125,11.5,'6.1 Credit risk continued'),(160,10,'Purchased book debts continued')),800)
    assert first['heading'] == 'Purchased book debts'
    assert first['topic_key'] == next_page['topic_key']
    assert '6 1 credit risk' in first['topic_key']


def test_running_header_dates_and_footer_do_not_replace_note_heading():
    p = heading_profile(words((10,11,'Nutun report'),(100,15,'2 Borrowings'),(200,12,'31 March 2026'),(780,15,'Company information')),800)
    assert p['heading'] == '2 Borrowings'
    assert [h['text'] for h in p['heading_evidence']] == ['2 Borrowings']


def test_small_font_continued_suffix_does_not_hide_numbered_subnote():
    ws=words((100,15,'6 Financial risk management'),(125,11.5,'6.2 Currency risk continued'))
    next(w for w in ws if w['text']=='continued')['size']=8
    result=heading_profile(ws,800)
    assert result['note_id']=='6.2'


def test_mixed_page_notes_are_retained_as_a_page_warning():
    p = heading_profile(words((100,15,'7 Segment report'),(140,11.5,'Geographical information'),(430,15,'8 Going concern')),800)
    assert p['heading'] == 'Geographical information'
    assert p['mixed_topics_on_page']


def test_subnote_on_shared_page_links_to_its_next_page_continuation():
    first=heading_profile(words((100,15,'6 Financial risk management'),(125,11.5,'6.1 Credit risk'),
                                (160,10,'Trade receivables'),(500,11.5,'6.2 Currency risk')),800)
    second=heading_profile(words((100,15,'6 Financial risk management'),(125,11.5,'6.2 Currency risk continued')),800)
    groups=plan_capture_groups(caps(2),[first,second])
    assert len(groups)==2 and first['mixed_topics_on_page']
    assert groups[0]['continuation_cut']
    assert groups[0]['continuation_reason']=='note_starts_on_shared_page'


def test_heading_changes_split_statements_but_continuation_stays_together():
    pages = caps(5)
    profiles = [profile('Cash flows')]*4+[profile('Borrowings')]
    groups = plan_capture_groups(pages,profiles,max_pages=6)
    assert [g['pages'] for g in groups] == [[1,4],[5,5]]
    assert groups[1]['start_reason'] == 'observed_topic_change'
    assert not groups[0]['continuation_cut']


def test_hard_limit_flags_continuation_without_losing_text():
    pages = caps(8)
    groups = plan_capture_groups(pages,[profile('ECL')]*8,max_pages=3)
    assert [g['pages'] for g in groups] == [[1,3],[4,6],[7,8]]
    assert [g['continuation_cut'] for g in groups] == [True,True,False]
    assert [c for g in groups for c in g['captures']] == pages


def test_unknown_heading_uses_smaller_fallback_and_oversized_page_survives():
    groups = plan_capture_groups(caps(7),[profile()]*7)
    assert [g['pages'] for g in groups] == [[1,3],[4,6],[7,7]]
    oversized = caps(1,30000)
    assert plan_capture_groups(oversized,[profile()])[0]['captures'] == oversized


def test_short_divider_stays_with_following_material():
    pages = caps(2);pages[0].text = 'Financial notes'
    groups = plan_capture_groups(pages,[profile('Financial notes'),profile('1 Borrowings')])
    assert len(groups) == 1


def test_related_note_parent_and_child_keep_small_tables_together():
    first=profile('2 Borrowings');first['note_id']='2'
    second=profile('2.1 Facilities');second['note_id']='2.1'
    groups=plan_capture_groups(caps(2),[first,second])
    assert [g['pages'] for g in groups]==[[1,2]]


def test_related_note_separates_principal_and_trade_ecl():
    first=profile('Principal portfolios');first.update(note_id='6.1',instrument='principal_portfolios')
    second=profile('Trade receivables');second.update(note_id='6.1',instrument='trade_receivables')
    assert len(plan_capture_groups(caps(2),[first,second]))==2


def test_identical_heading_different_reporting_periods_does_not_merge():
    first=profile('Group results');first.update(note_id='7',period='31 march 2026')
    second=profile('Group results');second.update(note_id='7',period='31 march 2025')
    assert len(plan_capture_groups(caps(2),[first,second]))==2


def test_period_label_below_heading_is_observed_without_guessing_dates():
    p=heading_profile(words((100,15,'7 Segment report'),(160,11,'Summarised income statement'),
                            (185,10,'for the half year ended'),(200,10,'31 March 2025 Unaudited')),800)
    assert p['period']=='31 march 2025'


def test_prompt_keeps_continuation_request_but_not_verbose_font_observations():
    from section_capture.packages import build_prompt
    manifest=dict(package_id='example',heading='Credit risk',source=dict(filename='report.pdf',sha256='a'*64,physical_page_count=3),
      selections=[dict(physical_page=1,selection_mode='area',content_type='financial_note',text='Source evidence')],
      ledger_contract=1,capture_coverage=dict(continuation_cut=True,next_chunk_pages=[2,3],
      heading_observations=[dict(text='FONT_OBSERVATION_SENTINEL',size=15)]))
    prompt=build_prompt(manifest,['Source evidence'],'consumer_lending')
    assert 'Possible table/note continuation' in prompt and '[2, 3]' in prompt
    assert 'FONT_OBSERVATION_SENTINEL' not in prompt


def test_overlap_partition_includes_unmapped_pages_once_and_preserves_titles():
    plan = partition_detected_ranges([
        dict(title='Statements',start_page=2,end_page=8),
        dict(title='Note 1',start_page=4,end_page=5,level=2),
    ],10)
    assert [p for s in plan for p in range(s['start_page'],s['end_page']+1)] == list(range(1,11))
    narrow = next(s for s in plan if s['title']=='Note 1')
    assert (narrow['start_page'],narrow['end_page']) == (4,5)
    assert narrow['overlapping_titles'] == ['Statements','Note 1']
    assert plan[0]['source'] == plan[-1]['source'] == 'coverage_remainder'


@pytest.mark.parametrize('max_pages,max_chars',[(0,1000),(3,0)])
def test_invalid_limits_rejected(max_pages,max_chars):
    with pytest.raises(ValueError):
        plan_capture_groups(caps(1),[profile()],max_pages,max_chars)


def test_auto_capture_saves_logical_names_observations_and_neighbour_pages(monkeypatch):
    from section_capture.section_matcher import auto_capture_section
    import section_capture.packages as packages
    saved=[]
    def capture(page,area):
        return SimpleNamespace(page=page,text='x'*1000,warnings=[],content_type=None)
    natives=[SimpleNamespace(height=800,extract_words=lambda **kwargs: words((100,15,'1 Borrowings')))]*2
    natives.append(SimpleNamespace(height=800,extract_words=lambda **kwargs: words((100,15,'2 Revenue'))))
    source=SimpleNamespace(page_count=3,size=lambda p:(600,800),capture_area=capture,plumber=SimpleNamespace(pages=natives))
    def save(**kwargs):
        obj=SimpleNamespace(manifest=dict(capture_coverage=kwargs['capture_coverage']),**{k:kwargs[k] for k in ['heading','captures','subheading']})
        saved.append(obj);return obj
    monkeypatch.setattr(packages,'save_package',save)
    auto_capture_section(source,'Financial notes',1,3)
    assert len(saved)==2 and saved[0].subheading=='1 Borrowings'
    coverage=saved[0].manifest['capture_coverage']
    assert coverage['next_chunk_pages']==[3,3] and len(coverage['heading_observations'])==2
    assert '2 Revenue' in saved[1].heading


def test_real_ntu_capture_preserves_every_page_and_source_hash(tmp_path):
    from pathlib import Path
    from section_capture.pdf_source import PdfSource
    from section_capture.report_map import scan_report
    from section_capture.section_matcher import auto_capture_section
    from section_capture.db import list_sections
    path=Path(__file__).resolve().parents[1]/'companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf'
    source=PdfSource(path)
    try:
        source.report_map=scan_report(source)
        auto_capture_section(source,'NTU report',1,38,'consumer_lending',tmp_path)
        sections=list_sections(source.sha256,tmp_path)
        pages=[s['physical_page'] for sec in sections for s in sec.selections]
        assert pages==list(range(1,39))
        assert all(len(sec.selections)<=6 for sec in sections)
        assert any('trade receivables' in sec.heading.lower() for sec in sections)
        assert any('cash flows' in sec.heading.lower() for sec in sections)
        assert all(sec.manifest['capture_coverage']['planner']=='native_logical_pages_v1' for sec in sections)
        source.verify_unchanged()
    finally:
        source.close()
