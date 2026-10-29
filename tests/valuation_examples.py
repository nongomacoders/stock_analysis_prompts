"""Explicit readiness evidence for synthetic positive-path test notes."""
import json
import re

def ready_note(text, **overrides):
    match = re.search(r'```json\s*(\{[\s\S]*?\})\s*```', text)
    data = json.loads(match.group(1)) if match else {}
    # Numeric fixture values have no meaning outside these synthetic tests.
    checks = []
    for code in ['historical_cash_flow','forecast_cash_and_debt','portfolio_rollforward','valuation_bridge','sensitivity','earnings_and_shares','financing_and_terminal']:
        checks.append({'check_id':code,'material':True,'verdict':'PASS',
                       'evidence':'Synthetic test evidence: opening 100 + change 15 = closing 115, same period and scope.',
                       'reconciliations':[{'label':'fixture identity','expected':115,'actual':115,'tolerance':0}]})
    data.update(valuation_status='READY',blocking_issues=[],valuation_checks=checks)
    data.setdefault('target_price_zar',84.50)
    data.setdefault('recommendation','HOLD')
    data.update(overrides)
    block='```json\n'+json.dumps(data)+'\n```'
    if match:return text[:match.start()]+block+text[match.end():]
    return block+'\n'+text
