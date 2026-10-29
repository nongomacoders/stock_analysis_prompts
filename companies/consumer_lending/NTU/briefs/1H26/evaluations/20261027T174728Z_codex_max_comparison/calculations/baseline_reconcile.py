"""Independent baseline calculations only; no network or production writes."""
import json
from pathlib import Path
run=Path(Path('scratch/ntu_comparison_latest.txt').read_text(encoding='utf-8').strip())
shares=780.651033
enterprise=3845*.55+644*.70+250*3+180*4
netdebt=3850+310+335-95
adjusted=enterprise-netdebt+1479
once=adjusted*.75/780.7
twice=once*.75
results={
 'scope':'Preserved original outputs and primary-source numerical checks. No fresh model outputs available.',
 'primary_source':{
  'POCI_net_carrying':{'formula':'3414+431','result':3414+431,'reported':3845},
  'cumulative_gain_rollforward':{'formula':'598+24-191','result':598+24-191,'reported':431},
  'principal_book_rollforward':{'formula':'3975+382-728+383-167','result':3975+382-728+383-167,'reported':3845},
  'other_book_rollforward':{'formula':'702+28-116+30','result':702+28-116+30,'reported':644},
  'ordinary_NAV_zar':{'formula':'1329/780.651033','result':1329/shares},
  'contributed_capital_per_share_not_NAV':{'formula':'5410/780.651033','result':5410/shares},
  'amortisation_signed_reconstruction':{'formula':'(728-383+167)+(116-30)','result':(728-383+167)+(116-30),'reported':597,'unexplained_residual':1},
  'OCF':{'formula':'-50+3-225+2+182-23','result':-50+3-225+2+182-23,'reported':-111},
  'historical_cash_after_capex_and_lease_before_borrowing':{'formula':'-111-17-13-30','result':-111-17-13-30,'limitation':'Not forecast FCFE; cash interest/tax already in OCF, excludes other financing/investing.'},
  'full_cash_change':{'formula':'-111-61+178','result':-111-61+178,'reported':6},
  'financing_subtotal':{'formula':'1145-842+3178-3269-30-4','result':1145-842+3178-3269-30-4,'reported':178},
  'cash_scope':{'formula':'107+6=112+1','result':107+6,'reported':113},
  'net_debt_ex_leases':{'formula':'3743+273-112','result':3743+273-112},
  'net_debt_incl_leases':{'formula':'3743+273+345-112','result':3743+273+345-112},
  'liquidity_partial_static_comparison':{'formula':'1396-112-475','result':1396-112-475,'limitation':'Not a proven forward funding deficit; facilities/refinancing/future cash flows unresolved.'},
  'UK_US_IFRS_services_share_pct':{'formula':'(303+212)/711*100','result':(303+212)/711*100},
  'UK_US_CODM_total_share_pct':{'formula':'(303+212)/1599*100','result':(303+212)/1599*100},
  'IFRS_EPS_cents':{'formula':'-63/782.1*100','result':-63/782.1*100,'reported':-8.1},
  'Gemini_PBD_cash_bridge_residual':{'formula':'844-410-246-182','result':844-410-246-182,'limitation':'6m unexplained, no full cash bridge established.'}
 },
 'original_SOTP':{'formula':'(3845*.55+644*.70+250*3+180*4-(3850+310+335-95)+1479)*.75/780.7','enterprise':enterprise,'net_debt':netdebt,'before_disputed_addback':enterprise-netdebt,'disputed_addback':1479,'forecast_net_other_assets':1315-765,'unexplained_excess_addback':1479-(1315-765),'equity_after_addback':adjusted,'single_discount_conditional_zar':once,'twice_discounted_zar':twice,'additional_haircut_to_055_pct':(1-.55/twice)*100,'total_discount_to_055_pct':(1-.55/(adjusted/780.7))*100,'limitation':'Arithmetic does not validate inputs, economic value, R0.55 or R1.07.'},
 'original_cash_forecast':[],
 'original_sensitivity':{'PBD_005_step_formula':'3845*.05*.75/780.7','PBD_005_step':3845*.05*.75/780.7,'Intl_05_step_formula':'180*.5*.75/780.7','Intl_05_step':180*.5*.75/780.7,'published_steps_approx':[.07,.05]},
 'reference_only_return':{'formula':'.55/.89-1','capital_pct':(.55/.89-1)*100,'current_quote_verified':False}
}
for year,opening,change,closing in [('FY26',106,-538,100),('FY27',100,-815,95),('FY28',95,-845,90)]:
 results['original_cash_forecast'].append({'year':year,'formula':f'{opening}+({change})','implied_closing':opening+change,'published_closing':closing,'unexplained_inflow':closing-(opening+change)})
path=run/'calculations/baseline_reconciliations.json'
path.write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
