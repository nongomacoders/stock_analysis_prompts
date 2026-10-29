from pathlib import Path

def edit(path, pairs):
 p=Path(path);s=p.read_text(encoding='utf-8-sig')
 for old,new,count in pairs:
  if s.count(old)!=count:raise RuntimeError(f'{path}: {s.count(old)} not {count}: {old[:65]}')
  s=s.replace(old,new)
 p.write_text(s,encoding='utf-8')

gui = Path('section_capture/one_shot_view.py').read_text(encoding='utf-8')
edit('section_capture/one_shot_view.py',[
 ('from datetime import datetime','from section_capture.valuation_policy import preserve_candidate\n\nfrom datetime import datetime',1),
 ('        if s.get("target_price_zar") is not None:', '''        if s.get('valuation_status') == 'WITHHELD':
            status = f'Valuation withheld{sens_str}'
        elif s.get("target_price_zar") is not None:''',1),
 ('            resp_text = sanitize_stage2_valuation_markdown(resp_text, reference_price_hint=ref_price)', '''            candidate_response = resp_text
            preserve_candidate(briefs_dir / f'{ticker}_{period}_stage2_valuation_note.md', candidate_response)
            resp_text = sanitize_stage2_valuation_markdown(resp_text, reference_price_hint=ref_price)''',2),
 ('save_stage2_report(primary_sha, response=resp_text, db_path=self.db_path)', 'save_stage2_report(primary_sha, response=resp_text, candidate_response=candidate_response, db_path=self.db_path)',1),
 ('save_stage2_report(primary_sha, prompt=sens_prompt, response=resp_text, db_path=self.db_path)', 'save_stage2_report(primary_sha, prompt=sens_prompt, response=resp_text, candidate_response=candidate_response, db_path=self.db_path)',1),
 (next(line for line in gui.splitlines() if 'self.set_phase_state(3,' in line and 'Valued in ' in line), '''            disposition = 'Valuation withheld' if parse_valuation_summary(resp_text).get('valuation_status') == 'WITHHELD' else 'Valued'
            self.set_phase_state(3, f'{disposition} in {elapsed:.1f}s ({tok:,} tok)', 'done')''',1),
 (next(line for line in gui.splitlines() if 'self.set_phase_state(3,' in line and 'SENS Updated in ' in line), '''            disposition = 'Valuation withheld' if parse_valuation_summary(resp_text).get('valuation_status') == 'WITHHELD' else 'SENS Updated'
            self.set_phase_state(3, f'{disposition} in {elapsed:.1f}s', 'done')''',1),
 ('        rec = summary.get("recommendation") or "RATED"', '''        if summary.get('valuation_status') == 'WITHHELD':
            self.set_phase_state(4, 'Valuation withheld', 'done')
            self.overall_progress.setValue(100)
            self._set_running_ui(False)
            self.live_banner_label.setText(f'{ticker} ({period}): Valuation withheld - material issues unresolved')
            self.append_log('Analysis saved. Valuation withheld; resolve the listed issues before publishing a target or recommendation.')
            self.refresh_companies(select_ticker=ticker)
            return
        rec = summary.get("recommendation") or "RATED"''',1),
])
edit('section_capture/portfolio_view.py',[
 ('            if s["has_stage2"]:\n                status_str', '''            if s.get('valuation_status') == 'WITHHELD':
                status_str = 'Valuation withheld'
            elif s["has_stage2"]:
                status_str''',1),
 ('        if not trig_text:\n', '''        if s.get('valuation_status') == 'WITHHELD':
            trig_text = '### Valuation withheld\n\n' + '\n'.join('- ' + str(x) for x in s.get('blocking_issues', []))
        if not trig_text:
'''.replace("'### Valuation withheld\n\n'", "'### Valuation withheld\\n\\n'").replace("+ '\n'.join", "+ '\\n'.join"),1),
])
edit('evaluate_stock.py',[
 ('from companies import find_company_dir','from section_capture.valuation_policy import assess_valuation_publication, preserve_candidate\n\nfrom companies import find_company_dir',1),
 ('        # 1. Parse JSON root block directly', '''        gate = assess_valuation_publication(note_content, require_contract=False)
        if gate['valuation_status'] == 'WITHHELD':
            return {
                'status': 'VALUATION_WITHHELD', 'valuation_status': 'WITHHELD',
                'ticker': self.ticker, 'period': self.period, 'sector': self.sector,
                'blocking_issues': gate['blocking_issues'],
                'target_price_zar': None, 'reference_price_zar': parsed_summary.get('reference_price'),
                'live_price_zar': live_price, 'static_recommendation': None,
                'dynamic_recommendation': None, 'implied_upside_pct': None,
                'dividend_yield_pct': None, 'projected_12m_tsr_pct': None, 'rating_bands': None,
                'checks': {'CHK-VALUATION-READINESS': {'passed': False, 'details': gate['blocking_issues']}},
            }
        # 1. Parse JSON root block directly''',1),
 ('        sanitized_md = sanitize_stage2_valuation_markdown(response)', '        preserve_candidate(self.s2_note_file, response)\n        sanitized_md = sanitize_stage2_valuation_markdown(response)',1),
 ('save_stage2_report(primary_sha, prompt=base_s2_prompt, response=sanitized_md, db_path=self.db_path)', 'save_stage2_report(primary_sha, prompt=base_s2_prompt, response=sanitized_md, candidate_response=response, db_path=self.db_path)',1),
 ('    def format_markdown(self, result: dict[str, Any]) -> str:\n', '''    def format_markdown(self, result: dict[str, Any]) -> str:
        if result.get('valuation_status') == 'WITHHELD':
            return (f"### {self.ticker} - Valuation withheld ({self.period})\\n\\n"
                    "**VALUATION WITHHELD - MATERIAL ISSUES UNRESOLVED**\\n\\n"
                    + '\\n'.join('- ' + str(x) for x in result.get('blocking_issues', []))
                    + '\\n\\nNo target price or investment recommendation is published.\\n')
''',1),
])
print('Updated GUI, portfolio display, CLI audit and rerun paths.')
