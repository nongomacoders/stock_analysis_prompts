"""Read-only evidence review; writes only into this versioned audit directory."""
import hashlib
import json
import re
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
RUN = Path(__file__).resolve().parents[1]
ROOT = next(p for p in RUN.parents if (p/'AGENTS.md').exists())
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name, obj):
    (RUN/'calculations'/name).write_bytes((json.dumps(obj, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
def ro(p):
    c = sqlite3.connect(p.resolve().as_uri()+'?mode=ro', uri=True)
    c.row_factory = sqlite3.Row
    return c

# All amounts Rm, except explicitly named shares/per-share/percentage outputs.
# Inputs transcribed from the rendered primary tables: physical pp.8,9,12-18,22,24,25,31.
calc = {
 'poci_gain_plus_gross': 3414+431,
 'poci_gain_to_gross_pct': 431/3414*100,
 'nav_per_share': 1329/(780651033/1e6),
 'goodwill_only_adjusted_nav': (1329-511)/(780651033/1e6),
 'all_intangibles_adjusted_nav': (1329-511-67)/(780651033/1e6),
 'loss_per_share_cents': -63/782.1*100,
 'codm_amortisation_signed': 728-383+167+116-30,
 'codm_rounding_difference': (728-383+167+116-30)-597,
 'core_ebitda': -63-29+68+597+1+216,
 'ifrs_pbd_net_income': 383-177-167+30,
 'operating_cash_before_assets_wc': -50+3-225+2,
 'statutory_operating_cash': -270+182-23,
 'investing_cash': -17-13+6-37,
 'financing_cash': 1145-842+3178-3269-30-4,
 'cash_change': -111-61+178,
 'cash_close': 107-111-61+178,
 'cash_close_including_hfs': 112+1,
 'principal_portfolio_close': 3975+382-728+383-167,
 'other_portfolio_close': 702+28-116+30,
 'combined_portfolio_decline': (3975+702)-(3845+644),
 'combined_portfolio_net_cash': 728+116-382-28,
 'portfolio_accounting_income_before_funding': 383-167+30,
 'cash_less_income_equals_carrying_decline': (728+116-382-28)-(383-167+30),
 'remaining_statutory_movement_difference': ((728+116-382-28)-(383-167+30))-182,
 'invalid_comparison_gap': (728-382)-182,
 'static_maturities_less_cash_and_undrawn': 1396-112-475,
 'overdraft_total_implied_limit': 273+475,
 'approx_800_less_disclosed_undrawn_overdraft': 800-475,
 'debt_including_overdraft': 822+2921+273,
 'debt_maturity_total': 1396+2620,
 'trade_and_other_financial_net': 395-5,
 'trade_net': 374-5,
 'other_financial_receivables': (395-5)-(374-5),
 'nonfinancial_receivables_residual': 497-(395-5),
 'deepseek_gross_net_error': (497-(395-5))-(497-395),
 'conventional_effective_tax_rate_pct': (-29)/(-92)*100,
 'international_share_of_ifrs_revenue_pct': 552/711*100,
 'uk_us_share_of_ifrs_revenue_pct': (303+212)/711*100,
 'international_share_of_codm_total_pct': 552/1599*100,
 'fy25_historical_book_impairment': -77-182,
 'h126_historical_book_impairment': -191,
}
expected={'poci_gain_plus_gross':3845,'codm_amortisation_signed':598,'core_ebitda':790,
 'ifrs_pbd_net_income':69,'statutory_operating_cash':-111,'investing_cash':-61,
 'financing_cash':178,'cash_change':6,'cash_close':113,'principal_portfolio_close':3845,
 'other_portfolio_close':644,'combined_portfolio_decline':188,
 'combined_portfolio_net_cash':434,'portfolio_accounting_income_before_funding':246,
 'cash_less_income_equals_carrying_decline':188,'remaining_statutory_movement_difference':6,
 'nonfinancial_receivables_residual':107,'fy25_historical_book_impairment':-259}
for k,v in expected.items(): assert calc[k]==v, (k,calc[k],v)
save('independent_results.json',dict(calculations=calc, arithmetic_assertions=len(expected),
 limitations=['Arithmetic checks do not validate forecast assumptions, facility availability or fair value.',
 'R6m residual remains unexplained; no FX, scope or rounding explanation assumed.',
 'R809m is a static stock comparison, not a forecast funding deficit.']))

c=ro(RUN/'inputs/experiment_snapshot.sqlite')
questions=[json.loads(r[0]) for r in c.execute('select question_json from ledger_questions')]
attempts=[dict(r) for r in c.execute('select * from section_response_attempts order by id')]
categories=Counter()
for a in attempts:
    a['errors']=json.loads(a.pop('errors_json'))
    if a['validation_status']!='rejected': continue
    message=' '.join(a['errors'])
    category=('quote_absent_or_nonliteral' if 'evidence quote' in message.lower() else
              'unknown_or_duplicate_id' if 'question ID' in message else
              'invalid_ledger_contract' if 'ledger version' in message else 'malformed_json')
    categories[category]+=1
status=read(RUN/'inputs/status.json')
sections=[dict(r) for r in c.execute('select package_id,section_number,manifest_json from sections')]
norm=lambda s: re.sub(r'\s+',' ',s).strip()
quote_checks=[]
for a in attempts:
    blocks=re.findall(r'```json\s*\n(.*?)```',a['response'],re.S|re.I)
    section=next((s for s in sections if s['package_id']==a['package_id']),None)
    if not section: continue
    selections=json.loads(section['manifest_json']).get('selections',[])
    for block in blocks:
        try: payload=json.loads(block)
        except json.JSONDecodeError: continue
        if not isinstance(payload,dict): continue
        for update in payload.get('updates',[]) if isinstance(payload.get('updates'),list) else []:
            if not isinstance(update,dict): continue
            for e in update.get('evidence',[]):
                if not isinstance(e,dict) or not isinstance(e.get('quote'),str): continue
                texts=[s.get('text','') for s in selections if s.get('physical_page')==e.get('physical_page')]
                quote_checks.append(dict(attempt_id=a['id'],status=a['validation_status'],
                    physical_page=e.get('physical_page'),quote=e['quote'],
                    contains_pipe='|' in e['quote'],literal_whitespace_normalized=any(norm(e['quote']) in norm(t) for t in texts)))
c.close()
ledger=dict(attempt_status_counts=dict(Counter(a['validation_status'] for a in attempts)),
 rejection_categories=dict(categories),question_status_counts=dict(Counter(q.get('status') for q in questions)),
 question_count=len(questions),fallback_events=len(status['local_open_only_fallbacks']),
 fallback_unique_sections=len({f['section'] for f in status['local_open_only_fallbacks']}),
 captured_selections_containing_pipe=sum('|' in s.get('text','') for row in sections for s in json.loads(row['manifest_json']).get('selections',[])),
 valid_attempt_quotes_containing_pipes_and_matching=sum(q['status']=='valid' and q['contains_pipe'] and q['literal_whitespace_normalized'] for q in quote_checks),
 limitations='Attempts include local replays/fallbacks. Categories describe first recorded validation error, not all defects or API failure rates.')
save('ledger_results.json',dict(summary=ledger,attempts=attempts,quote_checks=quote_checks))

manifest=read(RUN/'inputs/manifest.json')
checks=[dict(original=f['original'],saved=f['saved'],original_unchanged=sha(Path(f['original']))==f['sha256'],
             copy_unchanged=sha(RUN/f['saved'])==f['sha256']) for f in manifest['files']]
assert all(x['original_unchanged'] and x['copy_unchanged'] for x in checks)
assert all(sha(Path(s['path']))==s['sha256'] for s in manifest['sources'])
baseline=read(RUN/'inputs/production_report_and_guardrails.json')
c=ro(ROOT/'documents/analysis.sqlite')
current=dict(report=dict(c.execute('select * from reports where sha256=?',(baseline['report']['sha256'],)).fetchone()),
             guardrails=[dict(r) for r in c.execute('select * from sector_guardrails order by rule_code')])
c.close()
assert current==baseline, 'Production report or guardrail rows changed since preservation.'
rules=[dict(code=r['rule_code'],sector=r['sector'],title=r['title']) for r in baseline['guardrails']
       if any(s in (r['rule_code']+' '+r['rule_text']).lower() for s in ['trade receivable','simplified','poci','scope','liquidity'])]
save('related_guardrails.json',rules)
save('preservation_results.json',dict(checked_utc=datetime.now(timezone.utc).isoformat(),files=checks,
 source_hashes_unchanged=True,production_report_and_guardrails_logically_unchanged=True))
print(json.dumps(dict(arithmetic_assertions=len(expected),ledger=ledger,preserved_files=len(checks),
 production_unchanged=True,source_unchanged=True),ensure_ascii=True))
