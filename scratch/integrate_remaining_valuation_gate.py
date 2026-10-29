from pathlib import Path

def edit(path, pairs):
 p=Path(path);s=p.read_text(encoding='utf-8-sig')
 for old,new,count in pairs:
  if s.count(old)!=count:raise RuntimeError(f'{path}: {s.count(old)} not {count}: {old[:65]}')
  s=s.replace(old,new)
 p.write_text(s,encoding='utf-8')

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
