"""
Independent Forensic Calculations & Reconciliations
Target: Nutun Limited (NTU) 1H26
Evaluator: Gemini
Date: 2026-10-28
"""

import json
import hashlib
from pathlib import Path

def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    root = Path.cwd()
    pdf_path = root / "companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf"
    comparison_dir = root / "companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T081850Z_codex_workload_comparison"
    
    # 1. Source Hash Verification
    pdf_sha = compute_sha256(pdf_path)
    expected_sha = "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc"
    assert pdf_sha == expected_sha, f"PDF SHA mismatch: {pdf_sha} vs {expected_sha}"
    
    results = {
        "source_pdf": {
            "path": str(pdf_path),
            "sha256": pdf_sha,
            "hash_verified": pdf_sha == expected_sha,
            "physical_pages": 38
        }
    }
    
    # 2. PBD & Portfolio Reconciliation (Note 1.1 & Note 1.2, physical p. 13)
    pbd_opening_principal = 3975.0
    pbd_additions_principal = 382.0
    pbd_net_collections_principal = -728.0
    pbd_caeir_principal = 383.0
    pbd_impairment_principal = -167.0
    pbd_closing_principal_calc = (
        pbd_opening_principal + pbd_additions_principal + 
        pbd_net_collections_principal + pbd_caeir_principal + pbd_impairment_principal
    )
    pbd_closing_principal_stated = 3845.0
    
    pbd_other_opening = 702.0
    pbd_other_additions = 28.0
    pbd_other_collections = -116.0
    pbd_other_fv = 30.0
    pbd_closing_other_calc = pbd_other_opening + pbd_other_additions + pbd_other_collections + pbd_other_fv
    pbd_closing_other_stated = 644.0
    
    total_pbd_stated = 4489.0
    total_pbd_calc = pbd_closing_principal_calc + pbd_closing_other_calc
    
    # Note 6.2 (physical p. 22) - Gross carrying value vs impairment gain
    principal_gross = 3414.0
    principal_gain = 431.0
    principal_net = principal_gross + principal_gain
    gain_pct_of_gross = (principal_gain / principal_gross) * 100.0
    
    # Note 6.1 (physical p. 24) - Impairment breakdown
    impairment_acquired = 24.0
    impairment_historical = -191.0
    impairment_net_calc = impairment_acquired + impairment_historical
    impairment_net_stated = -167.0
    
    # ERC Runoff (physical p. 3)
    erc_stated = 8366.0
    erc_coverage_multiple = erc_stated / total_pbd_stated
    h1_gross_collections = 773.0
    annualised_collections = h1_gross_collections * 2.0
    implied_runoff_years = erc_stated / annualised_collections
    
    results["portfolio"] = {
        "principal_book": {
            "opening": pbd_opening_principal,
            "additions": pbd_additions_principal,
            "net_collections": pbd_net_collections_principal,
            "caeir": pbd_caeir_principal,
            "impairment": pbd_impairment_principal,
            "closing_calculated": pbd_closing_principal_calc,
            "closing_stated": pbd_closing_principal_stated,
            "ties": pbd_closing_principal_calc == pbd_closing_principal_stated
        },
        "other_financial_assets": {
            "opening": pbd_other_opening,
            "additions": pbd_other_additions,
            "collections": pbd_other_collections,
            "fv_gain": pbd_other_fv,
            "closing_calculated": pbd_closing_other_calc,
            "closing_stated": pbd_closing_other_stated,
            "ties": pbd_closing_other_calc == pbd_closing_other_stated
        },
        "total_pbd": {
            "calculated": total_pbd_calc,
            "stated": total_pbd_stated,
            "ties": total_pbd_calc == total_pbd_stated
        },
        "poci_accounting": {
            "gross_carrying": principal_gross,
            "cumulative_gain": principal_gain,
            "net_carrying": principal_net,
            "ties": principal_net == pbd_closing_principal_stated,
            "gain_to_gross_pct": round(gain_pct_of_gross, 3),
            "is_loss_reserve": False
        },
        "impairment_decomposition": {
            "acquired": impairment_acquired,
            "historical": impairment_historical,
            "net_calculated": impairment_net_calc,
            "net_stated": impairment_net_stated,
            "ties": impairment_net_calc == impairment_net_stated
        },
        "erc": {
            "erc_stated": erc_stated,
            "multiple_of_carrying": round(erc_coverage_multiple, 4),
            "implied_runoff_years": round(implied_runoff_years, 2)
        }
    }
    
    # 3. IFRS Income Statement & Net PBD Income (physical p. 9)
    rev = 711.0
    cost_rev = -385.0
    gross_profit = rev + cost_rev
    
    caeir_rev = 383.0
    funding_interest = -177.0
    impairment_loss = -167.0
    other_fv_gain = 30.0
    net_pbd_income_calc = caeir_rev + funding_interest + impairment_loss + other_fv_gain
    net_pbd_income_stated = 69.0
    
    opex = -445.0
    net_fin = -39.0
    other_inc = 11.0
    equity_acc_loss = -1.0
    op_loss_calc = gross_profit + net_pbd_income_calc + opex + net_fin + other_inc + equity_acc_loss
    op_loss_stated = -79.0
    
    non_op_loss = -13.0
    pbt_calc = op_loss_calc + non_op_loss
    pbt_stated = -92.0
    
    tax_credit = 29.0
    loss_period_calc = pbt_calc + tax_credit
    loss_period_stated = -63.0
    
    results["income_statement"] = {
        "gross_profit_calc": gross_profit,
        "net_pbd_income_calc": net_pbd_income_calc,
        "net_pbd_income_stated": net_pbd_income_stated,
        "net_pbd_ties": net_pbd_income_calc == net_pbd_income_stated,
        "operating_loss_calc": op_loss_calc,
        "operating_loss_stated": op_loss_stated,
        "pbt_calc": pbt_calc,
        "pbt_stated": pbt_stated,
        "loss_continuing_calc": loss_period_calc,
        "loss_continuing_stated": loss_period_stated,
        "vertical_ties": loss_period_calc == loss_period_stated
    }
    
    # 4. CODM Amortisation Footnote (physical p. 31)
    codm_net_collections = 728.0
    codm_caeir = 383.0
    codm_impairment = 167.0
    codm_other_collections = 116.0
    codm_other_fv = 30.0
    codm_amort_calc = codm_net_collections - codm_caeir + codm_impairment + codm_other_collections - codm_other_fv
    codm_amort_stated = 597.0
    results["codm_amortisation"] = {
        "formula": "728 - 383 + 167 + 116 - 30",
        "calculated": codm_amort_calc,
        "stated": codm_amort_stated,
        "rounding_delta": codm_amort_calc - codm_amort_stated
    }
    
    # 5. Cash Flow Statement & Reconciliations (physical p. 12)
    ocf_before_wc_int_tax = -50.0
    cf_fin_inc = 3.0
    cf_fin_costs = -225.0
    cf_tax = 2.0
    cf_pbd_movement = 182.0
    cf_wc = -23.0
    statutory_ocf_calc = ocf_before_wc_int_tax + cf_fin_inc + cf_fin_costs + cf_tax + cf_pbd_movement + cf_wc
    statutory_ocf_stated = -111.0
    
    borrowings_raised = 1145.0
    borrowings_repaid = -842.0
    od_drawn = 3178.0
    od_settled = -3269.0
    net_borrowings_calc = borrowings_raised + borrowings_repaid + od_drawn + od_settled # 212.0
    
    lease_repayment = -30.0
    treasury_shares = -4.0
    net_financing_calc = net_borrowings_calc + lease_repayment + treasury_shares # 178.0
    net_financing_stated = 178.0 # Mislabelled on p. 12 as "Net cash generated/(utilised) by investing activities"
    
    # Investing activities
    capex_ppe = -17.0
    capex_intangibles = -13.0
    total_capex = capex_ppe + capex_intangibles # -30.0
    cash_after_capex = statutory_ocf_calc + total_capex # -141.0
    cash_after_capex_and_leases = cash_after_capex + lease_repayment # -171.0
    
    divs_equity_acc = 6.0
    deposits_other_inv = -37.0
    net_investing_calc = total_capex + divs_equity_acc + deposits_other_inv # -61.0
    net_investing_stated = -61.0
    
    net_change_cash_calc = statutory_ocf_calc + net_investing_calc + net_financing_calc # -111 - 61 + 178 = +6.0
    opening_cash = 107.0
    fx_cash = 0.0
    closing_cash_calc = opening_cash + net_change_cash_calc + fx_cash # 113.0
    closing_cash_stated = 113.0
    sofp_cash = 112.0
    sofp_hfs_cash = 1.0
    sofp_total_cash = sofp_cash + sofp_hfs_cash # 113.0
    
    # PBD Cash Flow gap
    note_net_collections_less_additions = 728.0 - 382.0 # 346.0
    pbd_cash_flow_gap = note_net_collections_less_additions - cf_pbd_movement # 346 - 182 = 164.0
    
    results["cash_flow"] = {
        "statutory_ocf_calc": statutory_ocf_calc,
        "statutory_ocf_stated": statutory_ocf_stated,
        "ocf_ties": statutory_ocf_calc == statutory_ocf_stated,
        "total_capex": total_capex,
        "cash_after_capex": cash_after_capex,
        "lease_repayment": lease_repayment,
        "cash_after_capex_and_leases": cash_after_capex_and_leases,
        "net_borrowings": net_borrowings_calc,
        "net_financing_stated_as_investing_label": net_financing_stated,
        "net_financing_calc": net_financing_calc,
        "net_change_cash_calc": net_change_cash_calc,
        "closing_cash_calc": closing_cash_calc,
        "closing_cash_stated": closing_cash_stated,
        "sofp_cash_match": closing_cash_calc == sofp_total_cash,
        "pbd_cf_movement_stated": cf_pbd_movement,
        "note1_net_cash_pbd": note_net_collections_less_additions,
        "pbd_cash_flow_unexplained_gap": pbd_cash_flow_gap
    }
    
    # 6. Debt & Liquidity Runway (physical pp. 5, 8, 14-15)
    senior_debt = 3547.0
    sub_debt = 196.0
    overdraft = 273.0
    total_debt_calc = senior_debt + sub_debt + overdraft
    total_debt_stated = 4016.0
    
    due_within_12m = 927.0 + 196.0 + 273.0 # 1396.0
    due_after_12m = 2620.0
    
    od_facility_limit = 748.0
    od_drawn_stated = 273.0
    od_undrawn_calc = od_facility_limit - od_drawn_stated # 475.0
    
    cash_available = sofp_cash # 112.0
    total_disclosed_liquidity = cash_available + od_undrawn_calc # 587.0
    liquidity_shortfall_12m = due_within_12m - total_disclosed_liquidity # 1396 - 587 = 809.0
    
    management_claimed_unutilised = 800.0
    unreconciled_facility_claim = management_claimed_unutilised - od_undrawn_calc # 325.0
    
    results["debt_and_liquidity"] = {
        "total_debt_calc": total_debt_calc,
        "total_debt_stated": total_debt_stated,
        "ties": total_debt_calc == total_debt_stated,
        "due_within_12m": due_within_12m,
        "due_after_12m": due_after_12m,
        "undrawn_overdraft": od_undrawn_calc,
        "cash_on_balance_sheet": cash_available,
        "total_disclosed_liquidity": total_disclosed_liquidity,
        "refinancing_deficit_12m": liquidity_shortfall_12m,
        "management_claim_unutilised": management_claimed_unutilised,
        "unreconciled_management_facility_gap": unreconciled_facility_claim,
        "encumbrance_pct_principal_book": 100.0
    }
    
    # 7. Shares & NAV per Share (physical pp. 8, 16, 18)
    shares_issued = 784313242
    treasury_shares = 3662209
    net_shares = shares_issued - treasury_shares
    stated_net_shares = 780651033
    assert net_shares == stated_net_shares
    
    total_equity_zar = 1329000000.0
    nav_per_share_zar = total_equity_zar / net_shares
    
    stated_capital_zar = 5410000000.0
    stated_capital_per_share_zar = stated_capital_zar / net_shares
    
    weighted_avg_shares = 782143767.0
    continuing_headline_loss_zar = -63000000.0
    heps_cents_calc = (continuing_headline_loss_zar / weighted_avg_shares) * 100.0
    heps_cents_stated = -8.1
    
    results["shares_and_nav"] = {
        "shares_issued": shares_issued,
        "treasury_shares": treasury_shares,
        "net_shares_in_issue": net_shares,
        "total_equity_rm": 1329.0,
        "nav_per_share_zar": round(nav_per_share_zar, 4),
        "nav_per_share_display": round(nav_per_share_zar, 2),
        "stated_capital_rm": 5410.0,
        "stated_capital_per_share_zar": round(stated_capital_per_share_zar, 4),
        "weighted_avg_shares_m": round(weighted_avg_shares / 1e6, 4),
        "heps_cents_calculated": round(heps_cents_calc, 4),
        "heps_cents_stated": heps_cents_stated,
        "heps_ties": round(heps_cents_calc, 1) == heps_cents_stated
    }
    
    # 8. Workload Trial Metrics (comparison_metrics.json & status.json)
    with open(comparison_dir / "comparison_metrics.json", "r", encoding="utf-8") as f:
        comp_metrics = json.load(f)
    with open(comparison_dir / "status.json", "r", encoding="utf-8") as f:
        status_data = json.load(f)
        
    results["workload_trial_evaluation"] = {
        "source_pages": comp_metrics.get("source_pages"),
        "captures": comp_metrics.get("captures"),
        "successful_receipts": comp_metrics.get("successful_generation_receipts"),
        "reported_prompt_tokens": comp_metrics.get("reported_prompt_tokens"),
        "reported_completion_tokens": comp_metrics.get("reported_completion_tokens"),
        "reported_reasoning_tokens": comp_metrics.get("reported_reasoning_tokens"),
        "question_records": comp_metrics.get("question_records"),
        "open_question_records": comp_metrics.get("open_question_records"),
        "validation_attempts": comp_metrics.get("validation_attempt_counts_including_local_replays"),
        "local_open_only_fallbacks_count": comp_metrics.get("local_open_only_fallbacks"),
        "stage2_result_kind": comp_metrics.get("stage2_result_kind"),
        "stage2_completion_budget_retries": status_data.get("comparison_stage_headroom_retries"),
        "prior_interruption_error": status_data.get("prior_interruption_error")
    }
    
    output_path = Path(__file__).resolve().parent / "reconciliations.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Reconciliations saved successfully to {output_path}")

if __name__ == "__main__":
    main()
