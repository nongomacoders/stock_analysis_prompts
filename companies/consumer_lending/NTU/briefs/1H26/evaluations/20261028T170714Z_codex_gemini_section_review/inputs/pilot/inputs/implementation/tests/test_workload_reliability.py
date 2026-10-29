import json
from types import SimpleNamespace

import pytest

from section_capture import question_ledger as ledger
from section_capture.db import (connect_db, insert_section, prepare_question_ledger,
                                save_section_llm_response, upsert_report)

SHA = 'a' * 64
TEXT = 'Statutory cash flow is minus 111 million for six months.'


def response(updates=None, new=None):
    return '### 4. Updated Open Questions Ledger\n```json\n' + json.dumps(
        dict(ledger_version=1, updates=updates or [], new_questions=new or [])) + '\n```'


def new_question(text='Reconcile the statutory cash subtotal.'):
    return dict(question=text, priority='high', target_document='report.pdf', target_section='D003',
                evidence_required='Physical page, exact subtotal, period and signed components.',
                closure_condition='Components reproduce the subtotal without unexplained residuals.')


def setup_section(tmp_path, sha=SHA, package='s1'):
    selections = [dict(physical_page=1, text=TEXT)]
    manifest = dict(ledger_contract=1, selections=selections,
                    source=dict(filename='report.pdf', original_path='report.pdf', physical_page_count=2))
    return insert_section(package_id=package, report_sha256=sha, section_number=1, section_id='D003',
                          name=package, heading='Cash flow', subheading=None, analyst_question=None,
                          selected_text=TEXT, selections=selections, stored_questions=None,
                          prompt='test', manifest=manifest, db_path=tmp_path)


def test_ledger_omission_retains_questions_and_audit_history(tmp_path):
    setup_section(tmp_path)
    saved, first = save_section_llm_response('s1', response(new=[new_question()]), db_path=tmp_path)
    assert saved.manifest['review']['ledger_validation'] == 'valid'
    with connect_db(tmp_path) as conn:
        qid = ledger.records(conn, SHA)[0]['question_id']
    _, second = save_section_llm_response('s1', response(), db_path=tmp_path)
    assert qid in first and qid in second
    with connect_db(tmp_path) as conn:
        assert conn.execute('SELECT count(*) FROM ledger_events').fetchone()[0] == 1
        assert conn.execute('SELECT count(*) FROM section_response_attempts').fetchone()[0] == 2


@pytest.mark.parametrize('evidence', [[], [dict(source_sha256=SHA, physical_page=2, quote=TEXT)],
                                    [dict(source_sha256='b'*64, physical_page=1, quote=TEXT)],
                                    [dict(source_sha256=SHA, physical_page=1, quote='invented supporting quotation')]])
def test_closure_without_current_page_evidence_is_rejected(tmp_path, evidence):
    setup_section(tmp_path)
    save_section_llm_response('s1', response(new=[new_question()]), db_path=tmp_path)
    with connect_db(tmp_path) as conn:
        qid = ledger.records(conn, SHA)[0]['question_id']
    raw = response([dict(question_id=qid, status='resolved', answer='Claim tested.', evidence=evidence)])
    saved, updated = save_section_llm_response('s1', raw, db_path=tmp_path)
    assert updated is None
    assert saved.manifest['review']['ledger_validation'] == 'rejected'
    assert saved.llm_response == raw
    with connect_db(tmp_path) as conn:
        assert ledger.records(conn, SHA)[0]['status'] == 'open'


def test_valid_closure_keeps_record_and_explicit_empty_state(tmp_path):
    setup_section(tmp_path)
    save_section_llm_response('s1', response(new=[new_question()]), db_path=tmp_path)
    with connect_db(tmp_path) as conn:
        qid = ledger.records(conn, SHA)[0]['question_id']
    evidence = [dict(source_sha256=SHA, physical_page=1, quote=TEXT)]
    saved, updated = save_section_llm_response('s1', response([
        dict(question_id=qid, status='resolved', answer='Signed subtotal reproduced for the six-month period.', evidence=evidence)
    ]), db_path=tmp_path)
    assert saved.manifest['review']['ledger_validation'] == 'valid'
    assert updated.startswith('No open questions.')
    assert prepare_question_ledger(SHA, tmp_path) == updated
    with connect_db(tmp_path) as conn:
        assert ledger.records(conn, SHA)[0]['status'] == 'resolved'
        assert conn.execute('SELECT count(*) FROM ledger_events').fetchone()[0] == 2


def test_quote_whitespace_is_allowed_but_sign_change_is_rejected(tmp_path):
    setup_section(tmp_path)
    save_section_llm_response('s1', response(new=[new_question()]), db_path=tmp_path)
    with connect_db(tmp_path) as conn:
        qid = ledger.records(conn, SHA)[0]['question_id']
    update = dict(question_id=qid, status='partial', answer='Subtotal found; bridge remains open.',
                  evidence=[dict(source_sha256=SHA,physical_page=1,quote=TEXT.replace(' ', '\n'))])
    saved, _ = save_section_llm_response('s1', response([update]), db_path=tmp_path)
    assert saved.manifest['review']['ledger_validation'] == 'valid'
    update['evidence'][0]['quote'] = TEXT.replace('minus', 'plus')
    saved, _ = save_section_llm_response('s1', response([update]), db_path=tmp_path)
    assert saved.manifest['review']['ledger_validation'] == 'rejected'


def test_linked_report_uses_same_stable_questions(tmp_path):
    setup_section(tmp_path)
    save_section_llm_response('s1', response(new=[new_question()]), db_path=tmp_path)
    child = 'b' * 64
    setup_section(tmp_path, child, 's2')
    with connect_db(tmp_path) as conn:
        conn.execute('UPDATE reports SET parent_report_sha256=? WHERE sha256=?', (SHA, child))
    assert prepare_question_ledger(SHA, tmp_path) == prepare_question_ledger(child, tmp_path)
    _, merged = save_section_llm_response('s2', response(new=[new_question('Check debt maturity.')]), db_path=tmp_path)
    assert 'Check debt maturity.' in merged and 'Reconcile the statutory cash subtotal.' in merged
    with connect_db(tmp_path) as conn:
        texts = [r[0] for r in conn.execute('SELECT questions_ledger FROM reports')]
        assert texts[0] == texts[1]


def test_invalid_update_is_atomic_and_legacy_text_preserved(tmp_path):
    setup_section(tmp_path)
    upsert_report(sha256=SHA, questions_ledger='- Q1 Verify old disclosure.\n- Q2 Check shares.', db_path=tmp_path)
    imported = prepare_question_ledger(SHA, tmp_path)
    assert 'Q1 Verify old disclosure.' in imported and 'Q2 Check shares.' in imported
    bad = response(updates=[dict(question_id='Q-missing', status='resolved', answer='done', evidence=[])],
                   new=[new_question()])
    saved, _ = save_section_llm_response('s1', bad, db_path=tmp_path)
    assert saved.manifest['review']['ledger_validation'] == 'rejected'
    with connect_db(tmp_path) as conn:
        assert len(ledger.records(conn, SHA)) == 1


@pytest.mark.parametrize('raw', ['Everything looks fine.', '### 4. Updated Open Questions Ledger\n```json\n{}\n```'])
def test_missing_or_malformed_delta_is_rejected_even_on_first_section(tmp_path, raw):
    setup_section(tmp_path)
    saved, text = save_section_llm_response('s1', raw, db_path=tmp_path)
    assert text is None and saved.manifest['review']['ledger_validation'] == 'rejected'


def test_long_capture_has_no_lost_pages_and_warns_on_sparse_text(monkeypatch):
    from section_capture.section_matcher import auto_capture_section
    import section_capture.packages as packages
    saved = []

    def capture(page, area):
        return SimpleNamespace(page=page, text=('x' * 4000 if page != 40 else ''), warnings=[], content_type=None)

    source = SimpleNamespace(page_count=40, size=lambda page: (600, 800), capture_area=capture)

    def save(**kwargs):
        obj = SimpleNamespace(manifest=dict(capture_coverage=kwargs['capture_coverage']), captures=kwargs['captures'])
        saved.append(obj)
        return obj

    monkeypatch.setattr(packages, 'save_package', save)
    first = auto_capture_section(source, 'Large statement', 1, 40, max_pages=25, max_chars=8000)
    assert first is saved[0]
    assert [c.page for s in saved for c in s.captures] == list(range(1, 41))
    assert len(saved) == 20
    assert saved[-1].manifest['capture_coverage']['chunk_pages'] == [39, 40]
    assert saved[-1].captures[-1].warnings


def test_interrupted_capture_prefix_cannot_be_reused_as_complete(tmp_path):
    from section_capture.capture_coverage import save_capture_plan, assert_capture_plan_complete
    save_capture_plan(SHA,[dict(start_page=1,end_page=40)],40,tmp_path)
    prefix = SimpleNamespace(selections=[dict(physical_page=p) for p in range(1,26)])
    with pytest.raises(ValueError,match='missing physical pages 26'):
        assert_capture_plan_complete(SHA,[prefix],tmp_path)
    remainder = SimpleNamespace(selections=[dict(physical_page=p) for p in range(26,41)])
    assert_capture_plan_complete(SHA,[prefix,remainder],tmp_path)


def test_legacy_manual_selection_does_not_claim_whole_report_coverage(tmp_path):
    from section_capture.capture_coverage import assert_capture_plan_complete
    assert_capture_plan_complete(SHA,[SimpleNamespace(selections=[dict(physical_page=3)])],tmp_path)


def test_contract_replaces_full_copy_instruction_for_every_sector():
    from section_capture.packages import COMMON_PROMPT_PATH, get_prompt_path, SUPPORTED_SECTORS
    for sector in SUPPORTED_SECTORS:
        path = get_prompt_path(sector)
        template = COMMON_PROMPT_PATH.read_text(encoding='utf-8').replace('{sector_notes}', path.read_text(encoding='utf-8'))
        result = ledger.contract_prompt(template)
        assert '"ledger_version": 1' in result, path
        assert 'containing **all currently open questions**' not in result, path


def test_prompt_state_omits_answer_narrative_but_preserves_evidence_requests(tmp_path):
    setup_section(tmp_path)
    save_section_llm_response('s1', response(new=[new_question()]), db_path=tmp_path)
    with connect_db(tmp_path) as conn:
        question = ledger.records(conn, SHA)[0]
        question['answer'] = 'Lengthy answer narrative that should not be copied into each later request.'
        ledger.store(conn, SHA, SHA, question, 's1', 'test')
        rendered = ledger.render([question])
        conn.execute('UPDATE reports SET questions_ledger=? WHERE sha256=?', (rendered,SHA))
    compact = prepare_question_ledger(SHA, tmp_path, for_prompt=True)
    assert question['answer'] not in compact
    assert question['question_id'] in compact
    assert question['evidence_required'] in compact
    assert question['closure_condition'] in compact


def test_prompt_question_subset_is_bounded_and_does_not_remove_state():
    questions = [dict(new_question('Question '+str(i)), question_id='Q-'+str(i), status='open', answer='') for i in range(30)]
    questions[-1]['question'] = 'Cash collections and principal portfolio reconciliation.'
    context = dict(source=dict(filename='report.pdf'), section_ids=['D003'], heading='Cash collections portfolio')
    compact = ledger.render_prompt(questions,context)
    assert compact.count('"question_id"') == 12
    assert 'Q-29' in compact
    assert '12 of 30 open records' in compact
    assert len(questions) == 30 and all(q['status']=='open' for q in questions)
