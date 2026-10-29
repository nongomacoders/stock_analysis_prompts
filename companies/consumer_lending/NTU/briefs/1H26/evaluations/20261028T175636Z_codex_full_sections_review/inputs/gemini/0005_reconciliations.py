import json
from pathlib import Path

def run_reconciliations():
    results = {}
    
    # 1. Page 13: Principal book roll-forward H1 26
    p_open = 3975
    p_add = 382
    p_coll = 728
    p_caeir = 383
    p_imp = 167
    p_close = p_open + p_add - p_coll + p_caeir - p_imp
    assert p_close == 3845, f"Expected 3845, got {p_close}"
    results["p13_principal_book_close_H126"] = p_close
    
    # Page 13: Other financial assets roll-forward H1 26
    o_open = 702
    o_add = 28
    o_coll = 116
    o_fv = 30
    o_close = o_open + o_add - o_coll + o_fv
    assert o_close == 644, f"Expected 644, got {o_close}"
    results["p13_other_fin_assets_close_H126"] = o_close
    
    # Page 13: Total PBD H1 26
    total_pbd = p_close + o_close
    assert total_pbd == 4489, f"Expected 4489, got {total_pbd}"
    results["p13_total_pbd_H126"] = total_pbd
    
    # Page 13: Net collections check
    assert 773 - 45 == 728
    results["p13_net_collections_H126"] = 728
    
    # 2. Page 22: Financial assets subject to risk at 31 Mar 2026
    other_loans = 5
    trade_rec = 390
    principal_book = 3845
    other_fin = 644
    total_assets = other_loans + trade_rec + principal_book + other_fin
    assert total_assets == 4884, f"Expected 4884, got {total_assets}"
    results["p22_total_carrying_value_exact"] = total_assets
    
    # Model merged cell error:
    model_merged = 5390
    model_sum = model_merged + principal_book + other_fin
    assert model_sum == 9879
    results["p22_model_merged_cell_sum"] = model_sum
    results["p22_model_error_delta"] = model_sum - total_assets  # 4995
    assert model_sum - total_assets == 4995
    
    # 3. Page 24: Reconciliation of ECL allowance on principal book
    # Balances at 30 Sep 2025
    b_sep25 = {"unsecured": 468, "debt_review": 72, "retail": 47, "secured": 11, "total": 598}
    assert sum([468, 72, 47, 11]) == 598
    
    # Movements H1 26
    mov_h126 = {"unsecured": -241, "debt_review": 69, "retail": 4, "secured": 1, "total": -167}
    assert sum([-241, 69, 4, 1]) == -167
    
    # Balances at 31 Mar 2026
    b_mar26 = {
        "unsecured": b_sep25["unsecured"] + mov_h126["unsecured"],
        "debt_review": b_sep25["debt_review"] + mov_h126["debt_review"],
        "retail": b_sep25["retail"] + mov_h126["retail"],
        "secured": b_sep25["secured"] + mov_h126["secured"],
        "total": b_sep25["total"] + mov_h126["total"],
    }
    assert b_mar26["unsecured"] == 227
    assert b_mar26["debt_review"] == 141
    assert b_mar26["retail"] == 51
    assert b_mar26["secured"] == 12
    assert b_mar26["total"] == 431
    assert sum([227, 141, 51, 12]) == 431
    results["p24_balances_31mar2026"] = b_mar26
    
    # Full year 2025 historical book loss
    loss_1h25 = 77
    loss_2h25 = 182
    loss_fy25 = loss_1h25 + loss_2h25
    assert loss_fy25 == 259
    results["p24_historical_fy25_loss"] = loss_fy25
    
    # 4. Page 25: Trade receivables ECL
    tr_gross = 339 + 25 + 5 + 5
    assert tr_gross == 374
    tr_loss = 5
    tr_net = tr_gross - tr_loss
    assert tr_net == 369
    tr_rate = (tr_loss / tr_gross) * 100
    results["p25_trade_receivables_loss_rate_pct"] = tr_rate
    
    # Page 25 FX rates
    fx_rates = {
        "usd_closing_mar26": 17.2,
        "usd_closing_mar25": 18.4,
        "usd_closing_sep25": 17.3,
        "gbp_closing_mar26": 22.7,
        "gbp_closing_mar25": 23.9,
        "gbp_closing_sep25": 23.2,
    }
    results["p25_fx_rates"] = fx_rates
    
    # 5. Page 31: Core EBITDA reconciliation H1 26
    # Group:
    loss_cont = -63
    tax_exp = -29  # printed (29)
    da = 68
    pbd_amort = 597
    eq_loss = 1
    fin_charge = 216
    group_ebitda = loss_cont + tax_exp + da + pbd_amort + eq_loss + fin_charge
    assert group_ebitda == 790, f"Expected 790, got {group_ebitda}"
    results["p31_group_core_ebitda"] = group_ebitda
    
    # Nutun SA:
    sa_ebitda = -86 + (-37) + 32 + 597 + 1 + 203
    assert sa_ebitda == 710, f"Expected 710, got {sa_ebitda}"
    results["p31_nutun_sa_core_ebitda"] = sa_ebitda
    
    # Nutun International:
    intl_ebitda = 23 + 8 + 36 + 13
    assert intl_ebitda == 80, f"Expected 80, got {intl_ebitda}"
    results["p31_nutun_intl_core_ebitda"] = intl_ebitda
    assert sa_ebitda + intl_ebitda == group_ebitda
    
    # Model sign error on tax:
    model_wrong_ebitda = loss_cont + abs(tax_exp) + da + pbd_amort + eq_loss + fin_charge
    assert model_wrong_ebitda == 848
    results["p31_model_wrong_ebitda"] = model_wrong_ebitda
    results["p31_false_ebitda_gap"] = model_wrong_ebitda - group_ebitda  # 58
    assert model_wrong_ebitda - group_ebitda == 58
    
    # Footnote signed amortisation reconstruction:
    # Note 1.1: collections 728 - income 216 (383 CAEIR - 167 impairment) = 512
    # Note 1.2: collections 116 - FV gain 30 = 86
    # Total = 512 + 86 = 598
    signed_amort = (728 - (383 - 167)) + (116 - 30)
    assert signed_amort == 598
    results["p31_signed_amortisation_reconstruction"] = signed_amort
    results["p31_amortisation_residual"] = signed_amort - 597  # 1
    
    # 6. Portfolio cash vs carrying decline & R6m statutory residual
    port_cash = (773 + 116) - (382 + 28) - 45  # 434
    assert port_cash == 434
    port_income = (383 - 167) + 30  # 246
    assert port_income == 246
    carrying_decline = port_cash - port_income  # 188
    assert carrying_decline == 188
    statutory_cf_amort = 182
    residual_statutory = carrying_decline - statutory_cf_amort
    assert residual_statutory == 6
    results["portfolio_net_cash"] = port_cash
    results["portfolio_income"] = port_income
    results["carrying_decline"] = carrying_decline
    results["statutory_cf_amort"] = statutory_cf_amort
    results["residual_statutory_gap"] = residual_statutory
    
    print("All independent calculations passed successfully!")
    return results

if __name__ == "__main__":
    res = run_reconciliations()
    out_path = Path(__file__).parent / "reconciliation_output.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print(f"Saved results to {out_path}")
