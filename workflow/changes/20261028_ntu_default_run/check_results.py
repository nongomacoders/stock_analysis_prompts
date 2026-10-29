"""Offline independent accounting and selected historical checks; no model calls."""
from decimal import Decimal
import importlib.util
import json
from pathlib import Path
import sqlite3
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('runner',HERE/'rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
run=Path(m.POINTER.read_text(encoding='utf-8').strip())
metrics=m.read(run/'metrics.json');receipts=[m.read(p) for p in (run/'receipts').glob('*.json')]
assert len(receipts)==15 and sum(r['success'] for r in receipts)==11
assert all(r['metadata_status']=='retrieved' for r in receipts)
assert all(r['cost_usd'] is not None for r in receipts)
for r in receipts:
    assert abs(r['cost_usd']-r['generation_metadata']['total_cost'])<1e-9
    payload=m.read(run/'requests'/f'{r["label"]}.json')
    assert payload['model']==m.MODEL
    assert not {'reasoning','reasoning_effort','provider','service_tier'} & payload.keys()
cost=sum(Decimal(str(r['cost_usd'])) for r in receipts)
failed_cost=sum(Decimal(str(r['cost_usd'])) for r in receipts if not r['success'])
assert abs(float(cost)-metrics['totals']['cost_usd'])<1e-12
checks=dict(poci_net=3414+431,principal_close=3975+382-728+383-167,
 other_close=702+28-116+30,portfolio_net_cash=728+116-382-28,
 portfolio_income_before_funding=383-167+30,combined_carrying_decline=(3975+702)-(3845+644),
 statutory_movement_remaining_difference=((728+116-382-28)-(383-167+30))-182,
 nonfinancial_receivables=497-(395-5),effective_tax_rate=(-29)/(-92)*100,
 fy25_historical_impairment=77+182,codm_amortisation=728-383+167+116-30,
 net_asset_value=1329/(780651033/1e6),cash_change=-111-61+178,cash_close=107-111-61+178)
assert checks['poci_net']==checks['principal_close']==3845
assert checks['other_close']==644 and checks['portfolio_net_cash']-checks['portfolio_income_before_funding']==checks['combined_carrying_decline']==188
assert checks['statutory_movement_remaining_difference']==6
assert checks['nonfinancial_receivables']==107 and checks['fy25_historical_impairment']==259
assert checks['codm_amortisation']==598 and checks['cash_close']==113
stage1=(run/'outputs/stage1.md').read_text(encoding='utf-8')
assert '107' in stage1 and '259' in stage1 and '31.5%' in stage1
assert not (run/'outputs/stage2.md').exists()
m.preserve(run)
result=dict(actual_cost_usd=str(cost),failed_calls_cost_usd=str(failed_cost),
 failed_calls=sum(not r['success'] for r in receipts),all15_costs_corrobated_by_generation_metadata=True,
 all_requests_base_model_default_controls=True,selected_source_calculations=checks,
 source_calculation_basis='Inputs transcribed from source physical pp.8,9,12,13,16,22,24,31 and independently inspected in the preserved prior Codex audit; stable PDF hash reverified. No new PDF image inspection claimed.',
 stage1_preliminary_findings=[
 'Correct107 gross/net residual, FY25 historical259, ETR+31.5%, signed POCI/NAV and static-liquidity distinction now present.',
 'Still omits explicit combined434 cash minus246 income equals188 decline and remaining6 bridge.',
 'Contradictory tax pitfall says treating credit as positive ETR is a mistake, despite its correct +31.5% calculation elsewhere.',
 'Says no general-model staging applies to trade receivables while acknowledging policy applicability not established; keep conclusion conditional.',
 'Materiality labels for ECL policy and debt/lease residuals lack quantified valuation sensitivity; not independently validated.'
 ],limits='No completed Stage2 forecast/valuation to validate; not an end-to-end analytical success or isolated routing benchmark.')
m.save(run/'outputs/independent_checks.json',result)
print(json.dumps(dict(total_cost_usd=str(cost),failed_calls_cost_usd=str(failed_cost),accounted_calls=15,checks='passed',paid_calls=0)))
