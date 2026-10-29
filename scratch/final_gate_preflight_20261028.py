from pathlib import Path
p=Path('section_capture/valuation_policy.py');s=p.read_text(encoding='utf-8')
s+='''\n\ndef withhold_for_material_issues(text: str, issues: list[str]) -> str:
    """Apply failures found by application checks without losing the raw candidate."""
    objects = _objects(text)
    data = dict(objects[0]) if objects else {}
    data['valuation_status'] = WITHHELD
    data['blocking_issues'] = list(issues)
    return enforce_valuation_publication('```json\\n' + json.dumps(data, ensure_ascii=False) + '\\n```')
'''
p.write_text(s,encoding='utf-8')
p=Path('section_capture/db.py');s=p.read_text(encoding='utf-8')
old='            response = enforce_valuation_publication(original)\n'
new="            # A publication already blocked by an evaluator cannot be promoted\n            # merely because the preserved candidate claims READY.\n            submitted_gate = assess_valuation_publication(response)\n            response = enforce_valuation_publication(response if submitted_gate['valuation_status'] == 'WITHHELD' else original)\n"
assert s.count(old)==1;s=s.replace(old,new,1);p.write_text(s,encoding='utf-8')
p=Path('evaluate_stock.py');s=p.read_text(encoding='utf-8')
s=s.replace('assess_valuation_publication, preserve_candidate','assess_valuation_publication, preserve_candidate, withhold_for_material_issues',1)
s=s.replace('    def audit(self) -> dict[str, Any]:','    def audit(self, note_path: Path | None = None) -> dict[str, Any]:',1)
a=s.index('    def audit(');b=s.index('    def rerun(',a)
chunk=s[a:b]
chunk=chunk.replace('        quote = {}','        note_file = note_path if note_path is not None else self.s2_note_file\n        quote = {}',1)
chunk=chunk.replace('self.s2_note_file.exists()', 'note_file.exists()').replace('self.s2_note_file.read_text(', 'note_file.read_text(')
marker='        return {\n            "status": "PASSED" if overall_passed else "WARNINGS_FOUND",'
assert chunk.count(marker)==1
chunk=chunk.replace(marker,'''        material_issues = []
        for check_name, check in [('CHK-SOTP-MATH', sotp_check), ('CHK-GUARDRAILS', guardrail_check)]:
            if not check['passed']:
                material_issues.extend(f'{check_name}: {detail}' for detail in check['details'])
        if material_issues:
            target_price = static_rec = dynamic_rec = live_upside_pct = live_tsr_pct = div_yield = None
            rating_bands = None
        return {
            'valuation_status': 'WITHHELD' if material_issues else gate['valuation_status'],
            'blocking_issues': material_issues,
            "status": "VALUATION_WITHHELD" if material_issues else ("PASSED" if overall_passed else "WARNINGS_FOUND"),''',1)
chunk=chunk.replace('live_upside_pct if live_upside_pct is not None else parsed_summary.get("upside_pct")','None if material_issues else (live_upside_pct if live_upside_pct is not None else parsed_summary.get("upside_pct"))',1)
chunk=chunk.replace('live_tsr_pct if live_tsr_pct is not None else parsed_summary.get("tsr_pct")','None if material_issues else (live_tsr_pct if live_tsr_pct is not None else parsed_summary.get("tsr_pct"))',1)
s=s[:a]+chunk+s[b:]
old='        preserve_candidate(self.s2_note_file, response)\n        sanitized_md = sanitize_stage2_valuation_markdown(response)'
new='''        candidate_path = preserve_candidate(self.s2_note_file, response)
        sanitized_md = sanitize_stage2_valuation_markdown(response)
        if assess_valuation_publication(sanitized_md)['valuation_status'] == 'READY':
            preflight = self.audit(note_path=candidate_path)
            if preflight.get('valuation_status') == 'WITHHELD':
                sanitized_md = withhold_for_material_issues(response, preflight['blocking_issues'])'''
assert s.count(old)==1;s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
p=Path('tests/test_valuation_withholding.py');s=p.read_text(encoding='utf-8')
s+='''

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
    body='## 4. Sum-of-the-Parts\\nBlended Target Price: (0.5 * 20.0) + (0.5 * 20.0) = ZAR 35.00.'
    note.write_text(ready_note(body,target_price_zar=35,reference_price_zar=25),encoding='utf-8')
    monkeypatch.setattr(evaluator,'fetch_market_quote',lambda:{'price_zar':25})
    result=evaluator.audit(note_path=note)
    assert result['status']=='VALUATION_WITHHELD'
    assert not result['checks']['CHK-SOTP-MATH']['passed']
    assert result['target_price_zar'] is None
    assert result['dynamic_recommendation'] is None
    assert result['implied_upside_pct'] is None
'''
p.write_text(s,encoding='utf-8')
print('Application audit failures now override a model READY declaration before CLI promotion.')
