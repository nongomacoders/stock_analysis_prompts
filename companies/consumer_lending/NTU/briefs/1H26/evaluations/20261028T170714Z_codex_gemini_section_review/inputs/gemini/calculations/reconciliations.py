"""
Independent Reconciliations and Calculations for Section Prompt Pilot Review
Evaluator: Gemini
Date: 2026-10-28
"""
import json
from pathlib import Path

def run_all():
    results = {}

    # 1. NTU Physical Page 13: Purchased Book Debts
    # 1.1 Principal Book Portfolio (Rm)
    # H1 FY26
    ntu_prin_open_1h26 = 3975
    ntu_prin_add_1h26 = 382
    ntu_prin_coll_gross_1h26 = 773
    ntu_prin_coll_cost_1h26 = 45
    ntu_prin_coll_net_1h26 = ntu_prin_coll_gross_1h26 - ntu_prin_coll_cost_1h26 # 728
    ntu_prin_caeir_1h26 = 383
    ntu_prin_imp_1h26 = -167
    ntu_prin_close_1h26 = ntu_prin_open_1h26 + ntu_prin_add_1h26 - ntu_prin_coll_net_1h26 + ntu_prin_caeir_1h26 + ntu_prin_imp_1h26
    assert ntu_prin_close_1h26 == 3845, f"Expected 3845, got {ntu_prin_close_1h26}"

    # Maturity split H1 FY26
    ntu_prin_noncurr_1h26 = 2688
    ntu_prin_curr_1h26 = 1157
    assert ntu_prin_noncurr_1h26 + ntu_prin_curr_1h26 == 3845

    # 1.2 Other Financial Assets (Rm)
    # H1 FY26
    ntu_other_open_1h26 = 702
    ntu_other_add_1h26 = 28
    ntu_other_coll_1h26 = -116
    ntu_other_fv_1h26 = 30
    ntu_other_close_1h26_correct = ntu_other_open_1h26 + ntu_other_add_1h26 + ntu_other_coll_1h26 + ntu_other_fv_1h26
    assert ntu_other_close_1h26_correct == 644, f"Expected 644, got {ntu_other_close_1h26_correct}"

    # Discrepancy in DeepSeek new ledger answer string: "702 + 28 - 116 - 30 FV gain = 644"
    ntu_other_deepseek_string_eval = 702 + 28 - 116 - 30
    ntu_other_string_diff = ntu_other_deepseek_string_eval - 644 # -60

    # Maturity split H1 FY26
    ntu_other_noncurr_1h26 = 490
    ntu_other_curr_1h26 = 154
    assert ntu_other_noncurr_1h26 + ntu_other_curr_1h26 == 644

    # Total Purchased Book Debts
    ntu_total_pbd_1h26 = ntu_prin_close_1h26 + ntu_other_close_1h26_correct
    assert ntu_total_pbd_1h26 == 4489
    assert (ntu_prin_noncurr_1h26 + ntu_other_noncurr_1h26) == 3178
    assert (ntu_prin_curr_1h26 + ntu_other_curr_1h26) == 1311
    assert 3178 + 1311 == 4489

    results["ntu_p13"] = {
        "principal_close_h1_fy26": ntu_prin_close_1h26,
        "other_close_h1_fy26_correct": ntu_other_close_1h26_correct,
        "other_deepseek_string_eval": ntu_other_deepseek_string_eval,
        "other_string_diff_vs_stated": ntu_other_string_diff,
        "total_purchased_book_debts_h1_fy26": ntu_total_pbd_1h26,
        "non_current_total": 3178,
        "current_total": 1311
    }

    # 2. NTU Physical Page 25: Trade Receivables ECL
    ntu_trade_gross_1h26 = 374
    ntu_trade_allow_1h26 = -5
    ntu_trade_net_1h26 = 369
    assert ntu_trade_gross_1h26 + ntu_trade_allow_1h26 == ntu_trade_net_1h26
    ntu_trade_rate_1h26_pct = (-ntu_trade_allow_1h26 / ntu_trade_gross_1h26) * 100

    ntu_trade_gross_1h25 = 419
    ntu_trade_allow_1h25 = -6
    ntu_trade_net_1h25 = 413
    assert ntu_trade_gross_1h25 + ntu_trade_allow_1h25 == ntu_trade_net_1h25
    ntu_trade_rate_1h25_pct = (-ntu_trade_allow_1h25 / ntu_trade_gross_1h25) * 100

    ntu_trade_gross_fy25 = 364
    ntu_trade_allow_fy25 = -10
    ntu_trade_net_fy25 = 354
    assert ntu_trade_gross_fy25 + ntu_trade_allow_fy25 == ntu_trade_net_fy25
    ntu_trade_rate_fy25_pct = (-ntu_trade_allow_fy25 / ntu_trade_gross_fy25) * 100

    results["ntu_p25"] = {
        "trade_receivables_1h26": {
            "gross": ntu_trade_gross_1h26, "allowance": ntu_trade_allow_1h26, "net": ntu_trade_net_1h26,
            "calculated_rate_pct": ntu_trade_rate_1h26_pct, "stated_rate_pct": 1.34
        },
        "trade_receivables_1h25": {
            "gross": ntu_trade_gross_1h25, "allowance": ntu_trade_allow_1h25, "net": ntu_trade_net_1h25,
            "calculated_rate_pct": ntu_trade_rate_1h25_pct, "stated_rate_pct": 1.43
        },
        "trade_receivables_fy25": {
            "gross": ntu_trade_gross_fy25, "allowance": ntu_trade_allow_fy25, "net": ntu_trade_net_fy25,
            "calculated_rate_pct": ntu_trade_rate_fy25_pct, "stated_rate_pct": 2.75
        }
    }

    # 3. PAN Physical Pages 38-39: APM AISC
    pan_aisc_lower_cost_fy26 = 420.686
    pan_gold_sold_lower_fy26 = 247219
    pan_aisc_oz_lower_fy26 = (pan_aisc_lower_cost_fy26 * 1e6) / pan_gold_sold_lower_fy26

    pan_aisc_higher_cost_fy26 = 87.718
    pan_gold_sold_higher_fy26 = 25154
    pan_aisc_oz_higher_fy26 = (pan_aisc_higher_cost_fy26 * 1e6) / pan_gold_sold_higher_fy26

    pan_aisc_group_fy26_stated = 508.405
    pan_aisc_group_fy26_calc = pan_aisc_lower_cost_fy26 + pan_aisc_higher_cost_fy26 # 508.404
    pan_gold_sold_group_fy26 = pan_gold_sold_lower_fy26 + pan_gold_sold_higher_fy26 # 272373
    pan_aisc_oz_group_fy26 = (pan_aisc_group_fy26_stated * 1e6) / pan_gold_sold_group_fy26

    pan_aisc_group_fy25_stated = 315.068
    pan_gold_sold_group_fy25 = 196927
    pan_aisc_oz_group_fy25 = (pan_aisc_group_fy25_stated * 1e6) / pan_gold_sold_group_fy25

    pan_aisc_oz_diff_yoy = 1867 - 1600 # +267 US$/oz
    pan_aisc_oz_pct_yoy = (267 / 1600) * 100 # +16.6875%
    pan_gold_sold_diff_yoy = pan_gold_sold_group_fy26 - pan_gold_sold_group_fy25 # +75446 oz
    pan_gold_sold_pct_yoy = (pan_gold_sold_diff_yoy / pan_gold_sold_group_fy25) * 100 # +38.3116%

    results["pan_p38_39"] = {
        "fy26": {
            "lower_cost_aisc_usd_m": pan_aisc_lower_cost_fy26, "lower_cost_oz": pan_gold_sold_lower_fy26,
            "lower_cost_per_oz_calc": pan_aisc_oz_lower_fy26, "lower_cost_per_oz_stated": 1702,
            "higher_cost_aisc_usd_m": pan_aisc_higher_cost_fy26, "higher_cost_oz": pan_gold_sold_higher_fy26,
            "higher_cost_per_oz_calc": pan_aisc_oz_higher_fy26, "higher_cost_per_oz_stated": 3487,
            "group_aisc_usd_m_calc": pan_aisc_group_fy26_calc, "group_aisc_usd_m_stated": pan_aisc_group_fy26_stated,
            "group_aisc_rounding_residual_m": round(pan_aisc_group_fy26_stated - pan_aisc_group_fy26_calc, 6),
            "group_gold_sold_oz": pan_gold_sold_group_fy26,
            "group_aisc_per_oz_calc": pan_aisc_oz_group_fy26, "group_aisc_per_oz_stated": 1867
        },
        "yoy_trends": {
            "aisc_per_oz_diff_usd": pan_aisc_oz_diff_yoy,
            "aisc_per_oz_growth_pct": pan_aisc_oz_pct_yoy,
            "gold_sold_diff_oz": pan_gold_sold_diff_yoy,
            "gold_sold_growth_pct": pan_gold_sold_pct_yoy
        }
    }

    # 4. PAN Physical Pages 48-50: Production Summary
    # FY26 Gold Produced Components (oz)
    pan_fy26_underground = 105478 # Barberton 65,233 + Evander 40,246 = 105,479 (reported 105,478)
    pan_fy26_barberton_surface = 2428
    pan_fy26_tailings = 113613 # BTRP 10,974 + Elikhulu 56,475 + MTR 46,164
    pan_fy26_buyin = 18667 # Barberton 6,295 + Evander 6,609 + MTR 5,763
    pan_fy26_tennant = 32124
    pan_fy26_total_calc = pan_fy26_underground + pan_fy26_barberton_surface + pan_fy26_tailings + pan_fy26_buyin + pan_fy26_tennant
    assert pan_fy26_total_calc == 272310, f"Expected 272310, got {pan_fy26_total_calc}"

    # FY25 Gold Produced Components (oz)
    pan_fy25_underground_clean = 92643 # Barberton 65,895 + Evander 26,748
    pan_fy25_barberton_surface = 2654
    pan_fy25_tailings = 98636 # BTRP 15,224 + Elikhulu 52,606 + MTR 30,806
    pan_fy25_buyin = 1081 # Evander buy-in
    pan_fy25_tennant = 1513
    pan_fy25_total_calc = pan_fy25_underground_clean + pan_fy25_barberton_surface + pan_fy25_tailings + pan_fy25_buyin + pan_fy25_tennant
    assert pan_fy25_total_calc == 196527, f"Expected 196527, got {pan_fy25_total_calc}"

    # Forensic Reconciliation of DeepSeek's Discrepancy:
    # PDF row "Gold produced – underground", column "Group total" states 93,724 oz.
    # 93,724 = 92,643 (underground clean) + 1,081 (Evander buy-in).
    # DeepSeek took 93,724, missed Barberton surface (2,654 oz), and added buy-in (1,081 oz):
    deepseek_step1_sum = 93724 + 98636 + 1081 + 1513 # 194,954 oz
    deepseek_step1_gap = 196527 - deepseek_step1_sum # 1,573 oz gap
    # In question Q-99e93be7ca7c4594, DeepSeek included Barberton surface (2,654 oz):
    deepseek_step2_sum = 93724 + 2654 + 98636 + 1081 + 1513 # 197,608 oz
    deepseek_step2_excess = deepseek_step2_sum - 196527 # 1,081 oz excess (exact double-count of buy-in!)
    # Mathematical proof:
    assert 2654 - 1081 == 1573, "Barberton surface (2654) minus buy-in (1081) equals 1573 gap"
    assert deepseek_step2_excess == 1081, "Excess over total exactly equals buy-in (1081 oz)"

    results["pan_p48_50"] = {
        "fy26_components": {
            "underground": pan_fy26_underground, "barberton_surface": pan_fy26_barberton_surface,
            "tailings": pan_fy26_tailings, "buy_in": pan_fy26_buyin, "tennant": pan_fy26_tennant,
            "total_calc": pan_fy26_total_calc, "total_stated": 272310
        },
        "fy25_components": {
            "underground_clean": pan_fy25_underground_clean, "barberton_surface": pan_fy25_barberton_surface,
            "tailings": pan_fy25_tailings, "buy_in": pan_fy25_buyin, "tennant": pan_fy25_tennant,
            "total_calc": pan_fy25_total_calc, "total_stated": 196527
        },
        "deepseek_discrepancy_forensic_proof": {
            "underground_row_stated_total": 93724,
            "underground_clean_plus_buyin": 92643 + 1081,
            "missed_barberton_surface_oz": 2654,
            "double_counted_buyin_oz": 1081,
            "apparent_gap_in_initial_text_oz": 1573,
            "apparent_excess_in_ledger_q_oz": 1081,
            "proof_equality": "2654 - 1081 == 1573 and 197608 - 196527 == 1081"
        }
    }

    # 5. Paired Pilot Aggregates
    results["pilot_metrics"] = {
        "old": {
            "proposed_questions": 26, "prompt_chars": 109642, "input_tokens": 31304,
            "completion_tokens": 13655, "elapsed_seconds": 55.522, "cost_usd": 0.0171685668,
            "valid_ledgers": 3
        },
        "new": {
            "proposed_questions": 12, "prompt_chars": 90892, "input_tokens": 26620,
            "completion_tokens": 9165, "elapsed_seconds": 39.280, "cost_usd": 0.0128405676,
            "valid_ledgers": 4
        },
        "reductions": {
            "prompt_chars_diff": 109642 - 90892,
            "prompt_chars_pct": ((109642 - 90892) / 109642) * 100,
            "proposed_questions_diff": 26 - 12,
            "proposed_questions_pct": ((26 - 12) / 26) * 100,
            "completion_tokens_diff": 13655 - 9165,
            "completion_tokens_pct": ((13655 - 9165) / 13655) * 100,
            "elapsed_seconds_diff": 55.522 - 39.280,
            "elapsed_seconds_pct": ((55.522 - 39.280) / 55.522) * 100,
            "cost_usd_diff": 0.0171685668 - 0.0128405676,
            "cost_usd_pct": ((0.0171685668 - 0.0128405676) / 0.0171685668) * 100
        }
    }

    out_file = Path(__file__).parent / "reconciliation_output.json"
    out_file.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("All reconciliations executed and verified successfully. Output written to reconciliation_output.json")

if __name__ == "__main__":
    run_all()
