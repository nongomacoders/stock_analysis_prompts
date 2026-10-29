import copy
import pytest
from companies.sectors import get_all_sector_codes
from section_capture.packages import build_prompt


def manifest(contract=1):
    return dict(package_id='test',heading='Trade receivables',sector='consumer_lending',ledger_contract=contract,
        source=dict(filename='report.pdf',sha256='abc',physical_page_count=2),
        selections=[dict(physical_page=1,selection_mode='area',text='Trade receivables; currency risk begins.')],
        capture_coverage=dict(continuation_cut=True,next_chunk_pages=[2,2],
            heading_observations=[dict(physical_page=1,heading_evidence=[dict(text='Trade receivables'),dict(text='Currency risk')])]))


@pytest.mark.parametrize('sector',get_all_sector_codes())
def test_shared_task_and_sector_notes_reach_every_sector(sector):
    prompt=build_prompt(manifest(),['Trade receivables; currency risk begins.'],sector=sector)
    assert 'useful first-pass reading brief' in prompt
    assert '{sector_notes}' not in prompt
    assert 'not a mandatory checklist' in prompt
    assert '### 1. Key facts and figures' in prompt
    assert '### 4. Updated Open Questions Ledger' in prompt
    assert '### 5.' not in prompt
    assert 'ledger_version' in prompt and 'CURRENT supplied capture' in prompt
    assert 'copy and store for the next section' not in prompt


def test_shared_page_secondary_topic_and_pending_evidence_are_visible():
    prompt=build_prompt(manifest(),['Trade receivables; currency risk begins.'])
    assert 'OBSERVED TOPICS' in prompt and 'Currency risk' in prompt
    assert 'physical pages [2, 2]' in prompt
    assert 'including secondary headings' in prompt
    assert 'BEGIN SELECTED REPORT EVIDENCE\nTrade receivables; currency risk begins.' in prompt


def test_legacy_manual_ledger_remains_supported_without_json_contract():
    prompt=build_prompt(manifest(contract=0),['Evidence'])
    assert 'fenced markdown block' in prompt
    assert 'ledger_version' not in prompt
