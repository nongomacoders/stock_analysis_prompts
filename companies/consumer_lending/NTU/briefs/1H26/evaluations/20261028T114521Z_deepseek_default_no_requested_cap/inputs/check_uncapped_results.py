"""Read-only final accounting/publication checks for the uncapped continuation."""
from decimal import Decimal
import importlib.util
import json
from pathlib import Path
import re
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('runner',HERE/'rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
run=Path(m.POINTER.read_text(encoding='utf-8').strip());metrics=m.read(run/'metrics.json')
receipts=[m.read(p) for p in (run/'receipts').glob('*.json')]
assert len(receipts)==3 and all(r['success'] and r['finish_reason']=='stop' for r in receipts)
assert all(r['metadata_status']=='retrieved' for r in receipts)
for r in receipts:
    payload=m.read(run/'requests'/f'{r["label"]}.json')
    assert payload['model']==m.MODEL
    assert not {'max_tokens','max_completion_tokens','reasoning','reasoning_effort','provider','service_tier'} & payload.keys()
    assert abs(r['cost_usd']-r['generation_metadata']['total_cost'])<1e-9
assert sum(Decimal(str(r['cost_usd'])) for r in receipts)==Decimal('0.04537836')
raw=(run/'outputs/stage2.md').read_text(encoding='utf-8')
summary=json.loads(re.findall(r'```json\s*(.*?)```',raw,re.S|re.I)[0])
assert summary['valuation_status']=='WITHHELD'
for field in ['target_price_zar','recommendation','upside_pct','dividend_yield_pct','tsr_pct','rating_bands']:
    if field in summary: assert summary[field] is None,(field,summary[field])
assert m.read(run/'outputs/publication_assessment.json')['valuation_status']=='WITHHELD'
assert not m.read(run/'outputs/incomplete_section_coverage.json')['incomplete_sections']
historical=dict(principal_net=3414+431,principal_close=3975+382-728+383-167,other_close=702+28-116+30,
 combined_net_cash=728+116-382-28,portfolio_income_before_funding=383-167+30,
 decline=(3975+702)-(3845+644),remaining_statutory_residual=(3975+702)-(3845+644)-182,
 receivables_nonfinancial=497-(395-5),signed_etr=(-29)/(-92)*100,
 fy25_historical_loss=77+182,amortisation=728-383+167+116-30,
 nav=1329/(780651033/1e6),cash_close=107-111-61+178)
assert historical['combined_net_cash']-historical['portfolio_income_before_funding']==historical['decline']==188
assert historical['remaining_statutory_residual']==6 and historical['receivables_nonfinancial']==107
assert historical['fy25_historical_loss']==259 and historical['cash_close']==113
m.preserve(run)
m.save(run/'outputs/independent_checks.json',dict(checked_utc=m.utc(),accounted_calls=3,all_calls_complete=True,
 all_costs_corrobated=True,caller_token_caps_omitted=True,default_thinking_normal_routing_retained=True,
 price_fields_null=True,all_active_captures_have_accepted_analysis=True,historical_arithmetic=historical,
 evidence='Source-transcribed figures from physical pp.8,9,12,13,16,22,24,31, previously visually reviewed against the identical PDF hash. No fresh full-PDF image audit claimed.',
 limitations=['Actual forecasts/DCF/sensitivity were not built; no demonstrated repair of valuation modelling.',
 'Several blockers are source uncertainties or small residuals without demonstrated valuation materiality; Gemini should review proportionality.',
 'The successful new completions fit below prior caps; different prompt/context/provider/generation behavior prevents assigning causation solely to cap omission.']))
print('Uncapped request,3 complete generations,all costs,withheld null fields and preservation checks passed; exit0; no paid calls.')
