from pathlib import Path
import json,re,sys,hashlib
sys.stdout.reconfigure(encoding='utf-8')
review=Path(Path('scratch/ntu_latest_codex_review.txt').read_text().strip())
s=(review/'inputs/fresh_run/outputs/NTU_1H26_stage2_response.md').read_text(encoding='utf-8')
s=s.replace('\u2014','-')
def table(title):
 block=s.split('### '+title,1)[1].split('\n### ',1)[0].split('\n## ',1)[0]
 rows={}
 for line in block.splitlines():
  if line.startswith('|'):
   fields=[v.strip().replace('**','') for v in line.strip('|').split('|')]
   rows[fields[0]]=fields[1:]
 return rows

def nums(row):
 return [float(x.replace(',','').replace('(','-').replace(')','')) for x in row]
bs=table('Table 3.2 - Consolidated Balance Sheet')
cf=table('Table 3.3 - FCFE Bridge and Cash Rollforward')
pbd=table('Table 2.2 - PBD Operational KPIs')
res={'scope':'Independent arithmetic checks; economic assumptions are not validated by reproducing calculations.'}
shares=780.651033
precise_ev=4489*.85+170*4+100*5
precise_eq=precise_ev+87+276+5-4168-340-16
rounded_eq=4995+87+276+5-4168-340-16
res['SOTP']={'EV_unrounded':precise_ev,'pre_discount_unrounded':precise_eq,'post_discount_unrounded':precise_eq*.88,'target_unrounded':precise_eq*.88/shares,'target_from_displayed_738':738/shares,'without_WC_using_unrounded_inputs':(precise_eq-276)*.88/shares,'without_WC_using_rounded_table':(rounded_eq-276)*.88/shares,'WC_increment_after_discount':276*.88/shares,'assessment':'WC add-back lacks surplus/nonoperating allocation. Removal is a conditional scenario, not a validated target.'}
res['historical_CF']={'model_FCFE':nums(cf['FCFE before financing'])[0],'implied_model_OCF_before_capex':nums(cf['FCFE before financing'])[0]+30,'statutory_OCF':-111,'OCF_gap':140+30-(-111),'statutory_OCF_less_capex':-111-17-13,'model_gap_before_lease':140-(-111-17-13),'statutory_OCF_less_capex_lease':-111-17-13-30,'model_gap_after_lease':140-(-111-17-13-30),'actual_net_borrowing_cash':1145-842+3178-3269,'model_net_borrowing_cash':-nums(cf['Net debt repayment/(drawdown)'])[0],'cash_financing_direction_difference':212-(-134),'actual_full_cash_change':-111-61+178,'actual_cash_scope':'107+6=113; excludes 1 held-for-sale cash on BS:106+6=112','comparison_limitation':'Bridge definitions before equating these with distributable FCFE; lease/investing/financing treatment differs.'}
res['FCFE_vertical']={}
add_rows=['Net profit/(loss)','Add: Depreciation and amortisation','Add: Impairment loss','Less: CAEIR imputed interest','Less: Fair value gains','Add: Cash collections (principal + other)','Less: PBD acquisitions','Less: Capex','Less: Working capital and other']
for i,year in enumerate(['1H26','FY26','FY27','FY28']):
 inputs={row:nums(cf[row])[i] for row in add_rows}
 res['FCFE_vertical'][year]={'inputs':inputs,'sum':sum(inputs.values()),'stated':nums(cf['FCFE before financing'])[i]}
res['cash_periods']=[]
for i,year in enumerate(['1H26','FY26','FY27','FY28']):
 reported_open=nums(cf['Opening cash'])[i];change=nums(cf['Net cash increase/(decrease)'])[i];close=nums(cf['Closing cash'])[i]
 proper_open=[106,106,120,130][i]
 res['cash_periods'].append({'period':year,'printed_opening':reported_open,'correct_fiscal_opening':proper_open,'net_change':change,'closing':close,'printed_residual':close-(reported_open+change),'same_period_residual':close-(proper_open+change)})
res['BS_rows']=[]
for i,year in enumerate(['FY25','1H26','FY26','FY27','FY28']):
 assets=sum(nums(bs[k])[i] for k in ['Cash and cash equivalents','Other investments','Trade and other receivables','Purchased book debts','Other assets'])
 liabilities=sum(nums(bs[k])[i] for k in ['Interest-bearing debt','Bank overdrafts','Lease liabilities','Trade and other payables','Other liabilities'])
 res['BS_rows'].append({'period':year,'asset_sum':assets,'stated_assets':nums(bs['Total assets'])[i],'liability_sum':liabilities,'stated_liabilities':nums(bs['Total liabilities'])[i],'equity':nums(bs['Total equity'])[i],'identity_residual':assets-liabilities-nums(bs['Total equity'])[i]})
res['PBD_rollforward']=[]
for i,year in enumerate(['FY25','1H26','FY26','FY27','FY28']):
 inputs={k:nums(pbd[k])[i] for k in ['Principal book opening','Additions','Net cash collections','CAEIR imputed interest','Impairment loss']}
 implied=sum(inputs.values());stated=nums(pbd['Closing principal book'])[i]
 res['PBD_rollforward'].append({'year':year,'inputs':inputs,'implied':implied,'stated':stated,'residual':stated-implied})
res['total_book_rollforward']=[]
for col,cfcol,year,opening in [(2,1,'FY26',4677),(3,2,'FY27',4226),(4,3,'FY28',3966)]:
 additions=-nums(cf['Less: PBD acquisitions'])[cfcol];collections=nums(cf['Add: Cash collections (principal + other)'])[cfcol]
 imputed=-nums(cf['Less: CAEIR imputed interest'])[cfcol];impairment=nums(cf['Add: Impairment loss'])[cfcol];FV=-nums(cf['Less: Fair value gains'])[cfcol]
 implied=opening+additions-collections+imputed-impairment+FV
 close=nums(pbd['Total PBD carrying value'])[col]
 res['total_book_rollforward'].append({'year':year,'formula':f'{opening}+{additions}-{collections}+{imputed}-{impairment}+{FV}','implied':implied,'stated':close,'residual':close-implied})
res['debt_stock_cashflow']=[]
for i,year in [(1,'FY26'),(2,'FY27'),(3,'FY28')]:
 a=i;b=i+1
 opening=sum(nums(bs[k])[a] for k in ['Interest-bearing debt','Bank overdrafts','Lease liabilities'])
 closing=sum(nums(bs[k])[b] for k in ['Interest-bearing debt','Bank overdrafts','Lease liabilities'])
 repayment=nums(cf['Net debt repayment/(drawdown)'])[i]
 res['debt_stock_cashflow'].append({'year':year,'opening_borrowings_and_leases':opening,'closing':closing,'reduction':opening-closing,'cash_repayment':repayment,'unexplained_non_cash_or_other':repayment-(opening-closing),'limitation':'New leases, FX, fees or scope may reconcile if explicitly supplied; not assumed error magnitude in economic value.'})
res['FY26_debt_period_check']={'full_year_opening_including_leases':3443+364+364,'full_year_closing_including_leases':3575+275+330,'cash_repayment_full_year':188,'unexplained_with_full_year_opening':188-((3443+364+364)-(3575+275+330)),'limitation':'197m requires explicit noncash/FX/new-lease/scope bridge. Gemini 7m uses March opening against full-year cash repayment.'}
res['net_debt_table']={}
for i,year,stated in [(2,'FY26',3980),(3,'FY27',3730),(4,'FY28',3410)]:
 value=sum(nums(bs[k])[i] for k in ['Interest-bearing debt','Bank overdrafts','Lease liabilities'])-nums(bs['Cash and cash equivalents'])[i]-nums(bs['Other investments'])[i]
 res['net_debt_table'][year]={'formula_basis':'borrowings+overdraft+leases-cash-investments','calculated':value,'stated':stated,'residual':stated-value}
res['sensitivity']=[]
published=[[1.01,1.20,1.39],[.76,.95,1.14],[.50,.69,.89]]
for i,hc in enumerate([.10,.15,.20]):
 for j,multiple in enumerate([3,4,5]):
  value=(4489*(1-hc)+170*multiple+500+87+276+5-4168-340-16)*.88/shares
  res['sensitivity'].append({'haircut':hc,'BPO_multiple':multiple,'calculated':value,'round_two_decimals':round(value,2),'published':published[i][j],'absolute_difference':abs(value-published[i][j]),'within_declared_001':abs(value-published[i][j])<=.01})
res['DCF']=[]
for ke in [.18,.25,.30]:
 tv=330*1.02/(ke-.02);pv1=260/(1+ke);pv2=330/(1+ke)**2;pvtv=tv/(1+ke)**2
 res['DCF'].append({'Ke':ke,'TV':tv,'PV1':pv1,'PV2':pv2,'PV_TV':pvtv,'equity':pv1+pv2+pvtv,'per_share':(pv1+pv2+pvtv)/shares,'terminal_fraction':pvtv/(pv1+pv2+pvtv)})
res['DCF_explicit_debt_cash_difference']={'formula':'250/1.18+320/1.18**2','PV':250/1.18+320/1.18**2,'per_share':(250/1.18+320/1.18**2)/shares,'limitation':'Illustrates differing financing assumptions for two years only; not corrected DCF or perpetual debt policy.'}
res['NAV']={'statutory':1329/shares,'excluding_goodwill_only':(1329-511)/shares,'excluding_goodwill_and_intangibles':(1329-511-67)/shares,'fresh_note_description':'0.96 ex-goodwill; actually excludes intangibles too'}
res['rating']={'reference':.89,'frozen_reference_only':True,'published_target':.95,'upside_pct':(.95/.89-1)*100,'counterfactual_064_strong_sell_threshold':.64/.85,'counterfactual_rating_if_existing_method_used':'STRONG SELL, not Gemini SELL; valuation still not validated'}
res['metadata']={}
for i in [1,2]:
 a=json.loads((review/f'inputs/fresh_run/outputs/NTU_1H26_stage{i}_response.run.json').read_text())
 b=json.loads((review/f'inputs/fresh_run/outputs/stage{i}_generation_stats.json').read_text())
 res['metadata'][str(i)]={'generation_ids_match':a['generation_id']==b['id'],'requested_model':a['model'],'reported_model':b['model'],'provider':b['provider_name'],'finish_reason':a['finish_reason'],'reasoning_tokens':a['reasoning_tokens'],'native_completion_tokens':a['completion_tokens'],'native_total_tokens':a['total_tokens'],'cost_usd':b['total_cost'],'elapsed_seconds':a['elapsed_seconds']}
res['metadata_totals']={'reasoning_tokens':sum(x['reasoning_tokens'] for x in res['metadata'].values()),'native_tokens':sum(x['native_total_tokens'] for x in res['metadata'].values()),'cost_usd':sum(x['cost_usd'] for x in res['metadata'].values())}
(review/'calculations/reconciliations_output.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps({k:res[k] for k in ['SOTP','historical_CF','cash_periods','PBD_rollforward','total_book_rollforward','debt_stock_cashflow','net_debt_table','metadata_totals']},indent=2))
