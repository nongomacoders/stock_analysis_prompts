from pathlib import Path
from decimal import Decimal as D
import hashlib,json,sys
import pypdfium2 as pdfium
from PySide6.QtGui import QImage
sys.stdout.reconfigure(encoding='utf-8')
run=Path(__file__).resolve().parent.parent
root=Path.cwd()
gem=run/'inputs/gemini'
manifest=json.loads((gem/'inputs/manifest.json').read_text('utf-8'))
checks=[]
for row in manifest['preserved_inputs']:
    p=gem/'inputs'/Path(row['original_path']).name
    checks.append({'name':p.name,'hash_match':hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],'current_matches_snapshot':hashlib.sha256((root/row['original_path']).read_bytes()).hexdigest()==row['sha256']})
# Read the original script; do not execute it: its hard-coded writes overwrite Gemini's files.
gscript=(gem/'calculations/reconciliations.py').read_text('utf-8')
shares=D('780.7')
ev=D('3845')*D('.55')+D('644')*D('.70')+D('250')*3+D('180')*4
netdebt=D('3850')+310+335-95
plug=D('1479')
book_gap=plug-(D('1315')-765)
single=(ev-netdebt+plug)*D('.75')/shares
without_plug=(ev-netdebt)*D('.75')/shares
using_model_net_other=(ev-netdebt+D('550'))*D('.75')/shares
cash_roll=[]
for year,opening,closing,change in [('FY26E',106,100,-538),('FY27E',100,95,-815),('FY28E',95,90,-845)]:
    cash_roll.append({'year':year,'opening':opening,'stated_closing':closing,'stated_change':change,'implied_closing':opening+change,'unexplained_reconciling_inflow':closing-opening-change})
# Cash collections reduce the loan asset and ADD cash. Principal run-off is not a cash outflow.
fcfe27_stated=D('-880')
fcfe27_sign_flip=fcfe27_stated+2*1200
# Merely flipping the sign is illustrative, not a corrected FCFE forecast: CODM amortisation is not automatically an IFRS PAT expense.
historical={'operations':-50,'interest_received':3,'interest_paid':-225,'tax':2,'pbd_change':182,'working_capital':-23}
cf_sum=sum(historical.values())
rebuild_ebitda= -63-29+68+597+1+216
geo={'uk_us':303+212,'statutory_services_revenue':711,'mixed_codm_total_revenue':1599}
results={
 'input_hash_checks':checks,
 'gemini_script_overwrites_original_files':('20261027T163950Z_gemini' in gscript and 'write_text' in gscript),
 'sotp':{'ev':str(ev),'net_debt':str(netdebt),'pre_addback_equity':str(ev-netdebt),'model_addback':str(plug),'model_net_other_assets':550,'unexplained_addback_excess':str(book_gap),'one_discount_retaining_invalid_plug':str(single),'one_discount_with_no_addback_arithmetic_only':str(without_plug),'one_discount_using_550_arithmetic_only':str(using_model_net_other),'additional_haircut_after_two_discounts_pct':str((1-D('.55')/(single*D('.75')))*100),'cumulative_haircut_pct':str((1-D('.55')/((ev-netdebt+plug)/shares))*100)},
 'cash_rollforward':cash_roll,
 'fcfe27':{'stated_pre_funding':str(fcfe27_stated),'sign_flip_illustration_not_validated_forecast':str(fcfe27_sign_flip),'missing_runoff_inflow_vs_zero_cancellation':1200},
 'historical_ocf':{'inputs':historical,'sum':cf_sum,'reported':-111,'reconciles':cf_sum==-111,'capex_ppe_and_intangibles':30,'lease_principal':30,'ocf_less_capex_and_leases':-171,'ebitda_rebuilt':rebuild_ebitda,'ebitda_to_ocf_difference':790-(-111),'ebitda_plus_diff_does_not_explain_bridge':True},
 'pbd_runoff':{'principal':728-383+167,'other':116-30,'sum':728-383+167+116-30,'reported':597,'residual_possible_rounding_not_verified':1},
 'gemini_cash_bridge':{'collections_less_acquisitions_less_non_cash_income':844-410-246,'reported_asset_decrease':182,'unexplained_residual':844-410-246-182},
 'poci':{'gross':3414,'cumulative_gain':431,'net':3414+431,'prior_cumulative_gain':598,'current_change':431-598,'new_portfolio_gain':24,'historical_portfolio_loss':-191},
 'nav':{'shares_net_m':780.651033,'parent_equity_m':1329,'nav':1329/780.651033,'contributed_capital_per_net_share':5410/780.651033},
 'geographic_revenue':{**geo,'uk_us_fraction_of_statutory_services':515/711,'uk_us_fraction_of_codm_total':515/1599},
 'sensitivity':{'pbd_multiple_step':'.05','intl_multiple_step':'.5','table_claimed_steps_pbd':'.07','table_claimed_steps_intl':'.05'},
 'liquidity':{'maturities':1396,'cash':112,'undrawn_overdraft':475,'partial_static_gap':1396-112-475,'management_total_undrawn_approx':800,'gap_if_management_total_fully_available':1396-112-800,'unreconciled_facility_difference':800-475,'actual_future_cash_shortfall':'NOT VERIFIED'},
 'market':{'gemini_quote':'.90','independently_verified_current_quote':False,'conditional_target_upside_pct':str((D('.55')/D('.90')-1)*100),'ref_upside_pct':str((D('.55')/D('.89')-1)*100),'one_discount_invalid_plug_conditional_upside_pct':str((single/D('.90')-1)*100)}
}
# Give each sensitivity derivative a distinct label.
results['sensitivity']['pbd_implied_price_step']=str(D('3845')*D('.05')*D('.75')/shares)
results['sensitivity']['intl_implied_price_step']=str(D('180')*D('.5')*D('.75')/shares)
(run/'calculations/reconciliations_output.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
pdf=root/'companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf'
doc=pdfium.PdfDocument(str(pdf))
for n in (23,31):
    page=doc[n-1]; bitmap=page.render(scale=1.6,rev_byteorder=True)
    fmt=QImage.Format.Format_RGBA8888 if bitmap.n_channels==4 else QImage.Format.Format_RGB888
    img=QImage(bytes(bitmap.buffer),bitmap.width,bitmap.height,bitmap.stride,fmt).copy()
    if not img.save(str(run/f'calculations/page_{n:02}.png')): raise RuntimeError('Render save failed')
    bitmap.close();page.close()
doc.close()