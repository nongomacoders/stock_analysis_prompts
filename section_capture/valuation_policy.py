"""Publication gate for new valuations; this is not independent financial validation."""
from __future__ import annotations

import json
import math
import re
from typing import Any

WITHHELD = 'WITHHELD'
READY = 'READY'
WITHHELD_TITLE = 'VALUATION WITHHELD - MATERIAL ISSUES UNRESOLVED'
REQUIRED_CHECKS = (
    'historical_cash_flow', 'forecast_cash_and_debt', 'portfolio_rollforward',
    'valuation_bridge', 'sensitivity', 'earnings_and_shares', 'financing_and_terminal',
)
NUMERIC_CHECKS = set(REQUIRED_CHECKS) - {'financing_and_terminal'}
DERIVED_FIELDS = (
    'target_price_zar', 'target_price', 'recommendation', 'rating_bands',
    'implied_upside_pct', 'upside_pct', 'forward_dividend_yield_pct',
    'dividend_yield_pct', 'projected_12m_tsr_pct', 'tsr_pct',
)


def _objects(text: str) -> list[dict]:
    objects = []
    for block in re.findall(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', text, re.I):
        try:
            item = json.loads(block)
        except (ValueError, TypeError):
            continue
        if isinstance(item, dict):
            objects.append(item)
    return objects


def _finite(value: Any) -> bool:
    try:
        return isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value)
    except OverflowError:
        return False


def assess_valuation_publication(text: str | None, *, require_contract: bool = True) -> dict:
    """Block declared material failures, missing readiness evidence and inconsistent numbers.

    Legacy reading is allowed only with require_contract=False; new publication must
    use the default. Evidence/source truth still requires an independent review.
    """
    text = text or ''
    objects = _objects(text)
    policy_objects = [x for x in objects if any(k in x for k in ('valuation_status', 'valuation_checks', 'blocking_issues'))]
    data = objects[0] if objects and objects[0] in policy_objects else {}
    issues: list[str] = []
    if len(policy_objects) > 1 or (policy_objects and not data):
        issues.append('Readiness must be declared once in the first JSON summary, not a later or conflicting block.')
    explicit_withheld = bool(re.search(r'(?im)^\s*(?:#{1,6}\s*)?(?:\*\*)?VALUATION WITHHELD\b', text))
    has_contract = bool(policy_objects) or explicit_withheld
    if not has_contract and not require_contract:
        # A malformed/unsupported readiness block is never a legacy exception.
        if not re.search(r'"(?:valuation_status|valuation_checks|blocking_issues)"\s*:', text):
            return {'valuation_status': 'LEGACY', 'blocking_issues': [], 'valuation_checks': []}
    status = str(data.get('valuation_status', '')).strip().upper()
    if explicit_withheld or status == WITHHELD:
        issues.append('The analysis withholds valuation pending resolution of material issues.')
    elif status != READY:
        issues.append('Explicit READY status and completed valuation checks are missing or invalid.')
    blockers = data.get('blocking_issues', [])
    if not isinstance(blockers, list):
        issues.append('blocking_issues must be a list.')
    else:
        for item in blockers:
            if isinstance(item, dict):
                item = item.get('issue') or item.get('reason') or str(item)
            if str(item).strip():
                issues.append(str(item).strip())
    checks = data.get('valuation_checks', [])
    if not isinstance(checks, list):
        issues.append('valuation_checks must be a list.')
        checks = []
    seen = set()
    for check in checks:
        if not isinstance(check, dict):
            issues.append('Invalid valuation check entry.')
            continue
        code = check.get('check_id')
        if not isinstance(code, str) or not code.strip() or code in seen:
            issues.append('Valuation checks require unique nonempty check_id values.')
            continue
        seen.add(code)
        verdict = str(check.get('verdict', '')).strip().upper()
        material = check.get('material', True)
        evidence = check.get('evidence')
        if not isinstance(material, bool):
            issues.append(f'{code}: material must be a boolean.')
        if code in REQUIRED_CHECKS and material is not True:
            issues.append(f'{code}: a required dependency cannot be bypassed as immaterial.')
        if verdict not in {'PASS', 'FAIL', 'NOT VERIFIED', 'NOT APPLICABLE'}:
            issues.append(f'{code}: missing or invalid evidence verdict.')
        elif (material is not False or code in REQUIRED_CHECKS) and verdict in {'FAIL', 'NOT VERIFIED'}:
            issues.append(f'{code}: {verdict}; {evidence or "evidence/correction needed"}')
        if not isinstance(evidence, str) or not evidence.strip():
            issues.append(f'{code}: source evidence or a justified exception is missing.')
        rows = check.get('reconciliations', [])
        if not isinstance(rows, list):
            issues.append(f'{code}: reconciliations must be a list.')
            rows = []
        if code in NUMERIC_CHECKS and verdict == 'PASS' and not rows:
            issues.append(f'{code}: numerical reconciliation inputs are missing.')
        for row in rows:
            if not isinstance(row, dict):
                issues.append(f'{code}: invalid reconciliation.')
                continue
            expected, actual, tolerance = (row.get(k) for k in ('expected', 'actual', 'tolerance'))
            if not all(_finite(x) for x in (expected, actual, tolerance)) or tolerance < 0:
                issues.append(f'{code}: reconciliation requires finite numbers and a nonnegative tolerance.')
            elif abs(actual - expected) > tolerance + 1e-9 and (material is not False or code in REQUIRED_CHECKS):
                issues.append(f'{code}: {row.get("label", "reconciliation")} does not reconcile ({actual} vs {expected}; tolerance {tolerance}).')
    missing = sorted(set(REQUIRED_CHECKS) - seen)
    if missing:
        issues.append('Required checks missing: ' + ', '.join(missing) + '.')
    if status == READY:
        target = data.get('target_price_zar', data.get('target_price'))
        if not _finite(target) or target <= 0:
            issues.append('READY requires a finite positive target price.')
        if str(data.get('recommendation', '')).upper() not in {'STRONG BUY', 'BUY', 'HOLD', 'SELL', 'STRONG SELL', 'OVERWEIGHT', 'UNDERWEIGHT', 'NEUTRAL'}:
            issues.append('READY requires an explicit investment recommendation.')
    return {
        'valuation_status': WITHHELD if issues else READY,
        'blocking_issues': list(dict.fromkeys(issues)),
        'valuation_checks': checks,
        'reference_price': data.get('reference_price_zar') if _finite(data.get('reference_price_zar')) else None,
    }


def enforce_valuation_publication(text: str, *, require_contract: bool = True) -> str:
    """Return the publication note; preserve the input separately before calling."""
    assessment = assess_valuation_publication(text, require_contract=require_contract)
    if assessment['valuation_status'] != WITHHELD:
        return text
    identity = next(iter(_objects(text)), {})
    data = {k: identity[k] for k in ('ticker', 'company_name', 'sector', 'jse_sector_code', 'jse_sector_name', 'reference_price_zar') if k in identity}
    data.update(assessment)
    data.update({key: None for key in DERIVED_FIELDS})
    bullets = '\n'.join('- ' + issue.replace('\n', ' ') for issue in assessment['blocking_issues'])
    return ('```json\n' + json.dumps(data, indent=2, ensure_ascii=False) + '\n```\n\n'
            '# ' + WITHHELD_TITLE + '\n\n'
            'A target price and investment recommendation are withheld. Resolve the following issues before valuation:\n\n'
            + bullets + '\n\n'
            'The original analysis is preserved separately for evidence review. Any numbers in that analysis are not a published valuation.\n')


def valuation_gate_prompt() -> str:
    checks = [
        {'check_id': code, 'material': True, 'verdict': 'NOT VERIFIED',
         'evidence': 'Identify primary source, physical page, period, scope and calculation; or justify NOT APPLICABLE.',
         'reconciliations': []}
        for code in REQUIRED_CHECKS
    ]
    contract = {
        'valuation_status': 'WITHHELD', 'blocking_issues': ['State each blocking issue and the evidence/correction needed.'],
        'valuation_checks': checks, 'target_price_zar': None, 'recommendation': None,
        'rating_bands': None, 'implied_upside_pct': None, 'forward_dividend_yield_pct': None,
        'projected_12m_tsr_pct': None,
    }
    return '''## MATERIAL-ISSUE VALUATION GATE (OVERRIDES ANY DEMAND FOR A PRICE)
A defensible valuation is optional. If any material cash-flow, forecast, financing,
share-count, portfolio or valuation dependency fails reconciliation or remains
unsupported, output VALUATION WITHHELD - MATERIAL ISSUES UNRESOLVED. Retain verified
historical analysis and risk discussion, and list the evidence/corrections needed.
Do not invent inputs, use unexplained plugs, fix a target by a mechanical adjustment,
or issue a replacement recommendation simply to finish the report. Reopen Stage 1
claims against primary evidence; Stage 1 is not authoritative ground truth.

The FIRST JSON summary must include this readiness contract (merge ticker/company/
sector/reference fields into the SAME object). This example is deliberately WITHHELD:
''' + '```json\n' + json.dumps(contract, indent=2) + '\n```\n' + '''
Set READY only after every required applicable check passes with source evidence.
NOT APPLICABLE needs a specific legitimate explanation; never use it to skip an
applicable check. Required checks remain material=true. A material FAIL or NOT VERIFIED
blocks valuation. Routine forecast uncertainty is allowed when assumptions are explicit
and supported; unresolved material inputs are not routine uncertainty.
For every PASS numerical check, supply reconciliations containing label, expected,
actual and tolerance (finite numeric values in the same units, period and scope).
Include every forecast period and reconcile both cash and debt, statutory historical
cash to the chosen FCFE/FCFF definition, portfolio stocks, valuation bridge, shares,
and all sensitivity cells. Example: {"label":"FY27 closing cash Rm", "expected":115,
"actual":115, "tolerance":1}. Tolerances must be justified rounding, not devices to
hide material differences. For financing_and_terminal, explain borrowing, leases,
refinancing, equity dilution and terminal debt policy consistent with cash and stocks.

While WITHHELD, all derived valuation fields above MUST be JSON null, never zero,
HOLD, a distress target, or fabricated bands. Do not publish target, upside, dividend
yield, TSR, rating bands or an investment recommendation elsewhere in prose. Clearly
label any illustrative scenario as non-published and conditional; it must never become
the headline valuation. Sources, verified facts and unresolved questions remain useful.
When READY, supply the actual target/recommendation/bands/returns in the same object.
Passing this application gate is not independent financial validation.
'''


def preserve_candidate(note_path, text: str):
    """Preserve exact model text before sanitizing a production note."""
    from pathlib import Path
    from datetime import datetime, timezone
    folder = Path(note_path).parent / 'candidates' / Path(note_path).stem
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.md')
    path.write_bytes(text.encode('utf-8'))
    return path


def withhold_for_material_issues(text: str, issues: list[str]) -> str:
    """Apply failures found by application checks without losing the raw candidate."""
    objects = _objects(text)
    data = dict(objects[0]) if objects else {}
    data['valuation_status'] = WITHHELD
    data['blocking_issues'] = list(issues)
    return enforce_valuation_publication('```json\n' + json.dumps(data, ensure_ascii=False) + '\n```')
