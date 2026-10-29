from pathlib import Path
p=Path('section_capture/db.py');s=p.read_text(encoding='utf-8')
old="    res: dict[str, Any] = gate if gate['valuation_status'] == 'READY' else {}\n"
assert s.count(old)==1
s=s.replace(old,old+"    if res.get('reference_price') is None:\n        res.pop('reference_price', None)\n",1);p.write_text(s,encoding='utf-8')
p=Path('tests/test_portfolio_valuation.py');s=p.read_text(encoding='utf-8')
s=s.replace('assert prompt.strip().endswith("Reserve backticks solely for the initial JSON block and formal code/file identifiers.")','assert prompt.strip().endswith("Passing this application gate is not independent financial validation.")',1);p.write_text(s,encoding='utf-8')
p=Path('workflow/generate_sens_update.py');s=p.read_text(encoding='utf-8')
for old,new in [('"recommendation": "BUY | HOLD | SELL"','"recommendation": null'),('"target_price_zar": 0.00','"target_price_zar": null'),('"implied_upside_pct": 0.0','"implied_upside_pct": null'),('"forward_dividend_yield_pct": 0.0','"forward_dividend_yield_pct": null'),('"projected_12m_tsr_pct": 0.0','"projected_12m_tsr_pct": null')]:s=s.replace(old,new)
a=s.index('        \'       "rating_bands": {\\n\'');b=s.index('        "     }\\n"',a)
s=s[:a]+'''        '       "valuation_status": "WITHHELD",\\n'
        '       "blocking_issues": [],\\n'
        '       "valuation_checks": [],\\n'
        '       "rating_bands": null\\n'
'''+s[b:]
s=s.replace('Anchored to Stage 1 Forensic Ground Truth','Reopening Stage 1 Working Claims').replace('AUDITED STAGE 1 FORENSIC DETERMINATIONS (GROUND TRUTH FROM SQLITE)','STAGE 1 WORKING DETERMINATIONS (REOPEN CONTRADICTIONS FROM SQLITE)')
s=s.replace('containing native float numbers (e.g. `0.42`, `-30.0`), not text descriptions.','containing numbers when READY and JSON null for derived valuation fields when WITHHELD.')
p.write_text(s,encoding='utf-8')
p=Path('workflow/generate_stage2.py');s=p.read_text(encoding='utf-8')
s=s.replace('1. **Executive Investment Thesis & 12-Month JSE Price Target (ZAR/share):**','1. **Research Summary & Conditional Valuation (Target Only When READY):**',1)
s=s.replace('   - **Executive Valuation Summary Card Table:** Follow', '   - **Conditional Summary Card:** When WITHHELD, show status and blocking issues only. The price/return/band template below applies only when READY. Follow',1)
s=s.replace('Confirmed JSE Market Closing Price (MANDATORY ANCHOR - DO NOT GUESS)', 'Supplied Reference Price (KEEP ITS SOURCE/TIMESTAMP BASIS)').replace('The verified market closing price for {ticker} on the JSE is', 'The supplied reference price for {ticker} is').replace('You MUST calculate all implied capital upside/downside percentages','Only when READY, calculate implied capital upside/downside percentages')
p.write_text(s,encoding='utf-8')
p=Path('tests/test_one_shot_pipeline.py');s=p.read_text(encoding='utf-8').replace('AUDITED STAGE 1 FORENSIC DETERMINATIONS (GROUND TRUTH FROM SQLITE)','STAGE 1 WORKING DETERMINATIONS (REOPEN CONTRADICTIONS FROM SQLITE)');p.write_text(s,encoding='utf-8')
p=Path('section_capture/portfolio_view.py');s=p.read_text(encoding='utf-8').replace('"STRONG SELL", "IN PROGRESS"])','"STRONG SELL", "VALUATION WITHHELD", "IN PROGRESS"])',1);p.write_text(s,encoding='utf-8')
print('Applied reference fallback fix, updated prompt expectations and consistent SENS withholding template.')
