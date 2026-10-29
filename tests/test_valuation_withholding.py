import json
from pathlib import Path

import pytest
from valuation_examples import ready_note
from section_capture.valuation_policy import assess_valuation_publication, enforce_valuation_publication
from section_capture.db import connect_db, upsert_report, save_stage2_report, get_stage2_report, get_analyzed_stocks, parse_valuation_summary
from workflow.generate_stage2 import build_stage2_prompt_content, sanitize_stage2_valuation_markdown
from workflow.generate_sens_update import build_sens_update_prompt_content


def payload(text):
    return json.loads(text.split('```json',1)[1].split('```',1)[0])


def report(db, sha='parent', parent=None):
    upsert_report(sha256=sha,filename='NTU_1H26.pdf',original_path='companies/consumer_lending/NTU/sources/NTU_1H26.pdf',parent_report_sha256=parent,db_path=db)


def test_ready_requires_completed_checks_and_numeric_consistency():
    note=ready_note('Model analysis',target_price_zar=.95,reference_price_zar=.89)
    assert assess_valuation_publication(note)['valuation_status']=='READY'
    summary=parse_valuation_summary(sanitize_stage2_valuation_markdown(note))
    assert summary['target_price']==.95
    assert summary['rating_bands']
    data=payload(note)
    # A claimed PASS cannot override a numerical failure (the original NTU cash defect).
    data['valuation_checks'][0]['reconciliations']=[{'label':'historical OCF Rm','expected':-111,'actual':170,'tolerance':1}]
    assessment=assess_valuation_publication('```json\n'+json.dumps(data)+'\n```')
    assert assessment['valuation_status']=='WITHHELD'
    assert any('does not reconcile' in x for x in assessment['blocking_issues'])


@pytest.mark.parametrize('mutation', ['missing','unverified','fail','false_material','duplicate','nan','missing_reconciliation','no_evidence','invalid_status'])
def test_gate_fails_closed(mutation):
    data=payload(ready_note(''))
    check=data['valuation_checks'][0]
    if mutation=='missing':data['valuation_checks'].pop()
    elif mutation=='unverified':check['verdict']='NOT VERIFIED'
    elif mutation=='fail':check['verdict']='FAIL'
    elif mutation=='false_material':check['material']=False
    elif mutation=='duplicate':data['valuation_checks'].append(dict(check))
    elif mutation=='nan':check['reconciliations'][0]['actual']=float('nan')
    elif mutation=='missing_reconciliation':check['reconciliations']=[]
    elif mutation=='no_evidence':check['evidence']=''
    elif mutation=='invalid_status':data['valuation_status']='APPROVED'
    assert assess_valuation_publication('```json\n'+json.dumps(data)+'\n```')['valuation_status']=='WITHHELD'


def test_legitimate_exception_and_nonmaterial_issue():
    data=payload(ready_note(''))
    data['valuation_checks'][2].update(verdict='NOT APPLICABLE',evidence='Service business with no purchased debt portfolios.',reconciliations=[])
    data['valuation_checks'].append({'check_id':'minor_rounding','material':False,'verdict':'NOT VERIFIED','evidence':'Immaterial rounding in an unrelated historical table.'})
    assert assess_valuation_publication('```json\n'+json.dumps(data)+'\n```')['valuation_status']=='READY'


def test_withheld_cannot_recover_scenario_prices_or_bands():
    raw='''```json
{"valuation_status":"WITHHELD","blocking_issues":["Material cash-flow gap"],"target_price_zar":0.95,"recommendation":"HOLD"}
```
# Scenario only
Target Price: R0.64
Recommendation: SELL
'''
    public=sanitize_stage2_valuation_markdown(raw,target_price_hint=.95,reference_price_hint=.89)
    assert payload(public)['rating_bands'] is None
    assert payload(public)['target_price_zar'] is None
    assert 'R0.64' not in public
    assert 'R0.95' not in public
    parsed=parse_valuation_summary(public)
    assert parsed['valuation_status']=='WITHHELD'
    for key in ['target_price','recommendation','rating_bands','upside_pct','dividend_yield_pct','tsr_pct']:
        assert parsed[key] is None
    assert parse_valuation_summary(raw)['target_price'] is None


def test_new_legacy_note_withheld_but_legacy_reading_supported(tmp_path):
    legacy='Target Price: R0.95\nRecommendation: HOLD'
    assert parse_valuation_summary(legacy)['target_price']==.95
    db=tmp_path/'analysis.sqlite';report(db)
    save_stage2_report('parent',response=legacy,db_path=db)
    stored=get_stage2_report('parent',db_path=db)
    assert stored['target_price_zar'] is None
    assert stored['stage2_candidate_response']==legacy
    assert 'WITHHELD' in stored['stage2_response']


def test_withholding_clears_stale_metrics_parent_child_and_backfill(tmp_path):
    db=tmp_path/'analysis.sqlite';report(db);report(db,'child','parent')
    prior=ready_note('Historical analysis',reference_price_zar=79,implied_upside_pct=6.96)
    save_stage2_report('parent',response=prior,db_path=db)
    assert get_stage2_report('parent',db_path=db)['target_price_zar']==84.5
    raw=ready_note('A candidate must not be promoted',blocking_issues=['Portfolio stock does not reconcile'])
    public=enforce_valuation_publication(raw)
    save_stage2_report('child',response=public,candidate_response=raw,db_path=db)
    for sha in ['parent','child']:
        row=get_stage2_report(sha,db_path=db)
        for field in ['target_price_zar','recommendation','upside_pct','dividend_yield_pct','tsr_pct']:
            assert row[field] is None
        assert row['stage2_candidate_response']==raw
        assert 'WITHHELD' in row['stage2_response']
    assert get_stage2_report('parent',db_path=db)['stage2_baseline_response']==prior
    # Even an inconsistent old database row must not regenerate a portfolio rating.
    with connect_db(db) as con:
        con.execute("UPDATE reports SET target_price_zar=99,recommendation='BUY' WHERE sha256='parent'")
    stock=get_analyzed_stocks(db_path=db)[0]
    assert stock['valuation_status']=='WITHHELD'
    assert stock['target_price_zar'] is None
    assert stock['rating_bands'] is None
    assert stock['dynamic_recommendation']=='VALUATION WITHHELD'


@pytest.mark.parametrize('sector',['mining','retail','consumer_lending','reit','it','construction','finance','telcos'])
def test_all_sector_and_sens_prompts_allow_withholding(tmp_path,sector):
    stage2=build_stage2_prompt_content('Unresolved material cash gap','Example','ABC',sector,db_path=tmp_path)
    sens=build_sens_update_prompt_content('Old target','Example','ABC',sector,sens_filename='notice.pdf',db_path=tmp_path)
    for prompt in [stage2,sens]:
        assert 'MATERIAL-ISSUE VALUATION GATE' in prompt
        assert 'VALUATION WITHHELD - MATERIAL ISSUES UNRESOLVED' in prompt
        assert '"valuation_checks"' in prompt
        assert '"target_price_zar": null' in prompt


def test_cli_does_not_bypass_gate_using_raw_json(tmp_path,monkeypatch):
    from evaluate_stock import StockEvaluator
    evaluator=StockEvaluator('NTU',period='1H26',db_path=tmp_path/'analysis.sqlite')
    note=tmp_path/'candidate.md'
    note.write_text(ready_note('Scenario target R0.64',blocking_issues=['Material unresolved funding']),encoding='utf-8')
    evaluator.s2_note_file=note
    monkeypatch.setattr(evaluator,'fetch_market_quote',lambda:{'price_zar':.89})
    result=evaluator.audit()
    assert result['status']=='VALUATION_WITHHELD'
    assert result['target_price_zar'] is None
    assert result['dynamic_recommendation'] is None
    assert result['rating_bands'] is None
    markdown=evaluator.format_markdown(result)
    assert 'WITHHELD' in markdown
    assert 'R0.64' not in markdown


def test_withheld_company_display_and_portfolio(qapp,tmp_path):
    from section_capture.one_shot_view import discover_available_companies
    from section_capture.portfolio_view import PortfolioView
    db=tmp_path/'analysis.sqlite';report(db)
    save_stage2_report('parent',response='VALUATION WITHHELD - MATERIAL ISSUES UNRESOLVED',db_path=db)
    stock=get_analyzed_stocks(db_path=db)[0]
    items=[x for x in discover_available_companies(db_path=db) if x['ticker']=='NTU']
    assert 'withheld' in items[0]['display_text'].lower()
    view=PortfolioView(db_path=db)
    try:
        assert 'WITHHELD' in view.kpi_metrics_label.text()
        assert 'withheld' in view.triggers_browser.toPlainText().lower()
        assert 'Valuation withheld' in view.table.item(0,9).text()
    finally:
        view.close();view.deleteLater();qapp.processEvents()


def test_later_or_conflicting_readiness_cannot_promote_first_scenario():
    ready=ready_note('')
    first='```json\n{"target_price_zar":99,"recommendation":"BUY"}\n```\n'
    second='```json\n{"valuation_status":"WITHHELD","blocking_issues":["Material failure"]}\n```'
    for note in [first+ready, ready+'\n'+second]:
        assert assess_valuation_publication(note)['valuation_status']=='WITHHELD'
        assert parse_valuation_summary(note)['target_price'] is None


def test_evaluator_failure_overrides_ready_candidate_on_save(tmp_path):
    from section_capture.valuation_policy import withhold_for_material_issues
    db=tmp_path/'analysis.sqlite';report(db)
    raw=ready_note('Unsupported valuation')
    public=withhold_for_material_issues(raw,['Independent cash reconciliation failed'])
    save_stage2_report('parent',response=public,candidate_response=raw,db_path=db)
    row=get_stage2_report('parent',db_path=db)
    assert row['target_price_zar'] is None
    assert row['stage2_candidate_response']==raw
    assert 'Independent cash reconciliation failed' in row['stage2_response']


def test_cli_arithmetic_failure_withholds_even_if_model_claims_ready(tmp_path,monkeypatch):
    from evaluate_stock import StockEvaluator
    evaluator=StockEvaluator('NTU',period='1H26',db_path=tmp_path/'analysis.sqlite')
    note=tmp_path/'candidate.md'
    body='## 4. Sum-of-the-Parts\nBlended Target Price: (0.5 * 20.0) + (0.5 * 20.0) = ZAR 35.00.'
    note.write_text(ready_note(body,target_price_zar=35,reference_price_zar=25),encoding='utf-8')
    monkeypatch.setattr(evaluator,'fetch_market_quote',lambda:{'price_zar':25})
    result=evaluator.audit(note_path=note)
    assert result['status']=='VALUATION_WITHHELD'
    assert not result['checks']['CHK-SOTP-MATH']['passed']
    assert result['target_price_zar'] is None
    assert result['dynamic_recommendation'] is None
    assert result['implied_upside_pct'] is None
