from pathlib import Path

def edit(path, substitutions):
 p=Path(path);s=p.read_text(encoding='utf-8-sig')
 for old,new,count in substitutions:
  found=s.count(old)
  if found!=count: raise RuntimeError(f'{path}: expected {count} occurrences, found {found}: {old[:85]}')
  s=s.replace(old,new)
 p.write_text(s,encoding='utf-8')

edit('section_capture/db.py',[
 ('from companies import PACKAGE_DIR, SECTORS', 'from section_capture.valuation_policy import assess_valuation_publication, enforce_valuation_publication\n\nfrom companies import PACKAGE_DIR, SECTORS',1),
 ('    stage2_response TEXT,','    stage2_response TEXT,\n    stage2_candidate_response TEXT,',1),
 ('        ("stage2_response", "TEXT"),','        ("stage2_response", "TEXT"),\n        ("stage2_candidate_response", "TEXT"),',1),
 ('    res: dict[str, Any] = {}\n\n    # ---------------------------------------------------------------------', '''    gate = assess_valuation_publication(text, require_contract=False)
    if gate['valuation_status'] == 'WITHHELD':
        # Do not fall back to prose/scenario prices or regenerate rating bands.
        return {**gate, 'target_price': None, 'reference_price': None,
                'recommendation': None, 'rating_bands': None, 'upside_pct': None,
                'dividend_yield_pct': None, 'tsr_pct': None}
    res: dict[str, Any] = gate if gate['valuation_status'] == 'READY' else {}

    # ---------------------------------------------------------------------''',1),
 ('    sens_updates: list[dict] | None = None,\n    db_path: str | Path | None = None,', '    sens_updates: list[dict] | None = None,\n    db_path: str | Path | None = None,\n    candidate_response: str | None = None,',1),
 ('        if response is not None:\n            # Preserve original baseline', '''        if response is not None:
            original = candidate_response if candidate_response is not None else response
            response = enforce_valuation_publication(original)
            updates.append('stage2_candidate_response = ?')
            params.append(original)
            # Preserve original baseline''',1),
 ('sha256, filename, stage2_prompt, stage2_response, stage2_updated_at,','sha256, filename, stage2_prompt, stage2_response, stage2_candidate_response, stage2_updated_at,',1),
 ('            raw_summary = r["valuation_summary_json"]','            summary_dict = {}\n            raw_summary = r["valuation_summary_json"]',1),
 ('            results.append({\n                "sha256": r["sha256"],', '''            withheld = summary_dict.get('valuation_status') == 'WITHHELD'
            if withheld:
                tp_val = live_upside = rating_bands = None
                static_rec = dynamic_rec = 'VALUATION WITHHELD'
            results.append({
                'valuation_status': summary_dict.get('valuation_status', 'LEGACY'),
                'blocking_issues': summary_dict.get('blocking_issues', []),
                "sha256": r["sha256"],''',1),
 ('                "upside_pct": r["upside_pct"],','                "upside_pct": None if withheld else r["upside_pct"],',1),
 ('                "dividend_yield_pct": r["dividend_yield_pct"],','                "dividend_yield_pct": None if withheld else r["dividend_yield_pct"],',1),
 ('                "tsr_pct": r["tsr_pct"],','                "tsr_pct": None if withheld else r["tsr_pct"],',1),
])
edit('workflow/generate_stage2.py',[
 ('from companies import find_company_dir', 'from section_capture.valuation_policy import enforce_valuation_publication, valuation_gate_prompt\n\nfrom companies import find_company_dir',1),
 ('    if not note_markdown:\n        return note_markdown\n    import json', '    if not note_markdown:\n        return note_markdown\n    note_markdown = enforce_valuation_publication(note_markdown)\n    import json',1),
 ('        repaired = validate_and_repair_rating_bands(data.get("rating_bands"), tp, ref)', '''        if data.get('valuation_status') == 'WITHHELD':
            return note_markdown
        repaired = validate_and_repair_rating_bands(data.get("rating_bands"), tp, ref)''',1),
 ('''        '       "recommendation": "BUY | HOLD | SELL",',''', '''        '       "recommendation": null,',''',1),
 ('''        '       "target_price_zar": 0.00,',''', '''        '       "target_price_zar": null,',''',1),
 ('''        '       "implied_upside_pct": 0.0,',''', '''        '       "implied_upside_pct": null,',''',1),
 ('''        '       "forward_dividend_yield_pct": 0.0,',''', '''        '       "forward_dividend_yield_pct": null,',''',1),
 ('''        '       "projected_12m_tsr_pct": 0.0,',''', '''        '       "projected_12m_tsr_pct": null,',''',1),
 ('"as your 99% confidence baseline', '"as reviewable working claims to verify against primary evidence',7),
 ('1. **High-Confidence Baseline Truth (99% Confidence Prior):**','1. **Reviewable Stage 1 Working Papers:**',7),
 ('AUDITED STAGE 1 FORENSIC DETERMINATIONS (GROUND TRUTH)','STAGE 1 WORKING DETERMINATIONS (REOPEN CONTRADICTIONS)',7),
 ('    return "\\n".join(md_lines)','    md_lines.append(valuation_gate_prompt())\n    return "\\n".join(md_lines)',1),
])
edit('workflow/export_stage1.py',[
 ('from companies import find_company_dir', 'from section_capture.valuation_policy import valuation_gate_prompt\n\nfrom companies import find_company_dir',1),
 ('    return "\\n".join(md_lines)', '''    md_lines.append('## Stage 2 handoff: unresolved material dependencies')
    md_lines.append('List material FAIL/NOT VERIFIED claims with source pages, calculations and evidence needed. '
                    'Carry them forward explicitly; do not declare a 99% confidence baseline. '
                    'Stage 2 must withhold valuation while a material dependency remains unresolved. '
                    'Do not produce a target or recommendation in Stage 1.')
    return "\\n".join(md_lines)''',1),
])
edit('workflow/generate_sens_update.py',[
 ('from companies import find_company_dir','from section_capture.valuation_policy import valuation_gate_prompt\n\nfrom companies import find_company_dir',1),
 ('    return "\\n".join(md_lines)','    md_lines.append(valuation_gate_prompt())\n    return "\\n".join(md_lines)',1),
])
print('Updated central gate, database, Stage 1/2 and SENS prompts.')
