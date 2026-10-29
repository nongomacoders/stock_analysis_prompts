"""Independent calculations and reconciliations for the Native PDF Extraction Pilot.
Evaluator: Gemini (Google Antigravity IDE)
Run: 20261028T184306Z_gemini
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def run_reconciliations():
    reconciliations = {
        "ntu_financial_assets_note_6_1": {
            "description": "NTU 1H26 Note 6.1 (p. 22) Financial assets subject to credit risk carrying value footing",
            "expression": "5 (Other loans) + 390 (Trade receivables) + 3845 (Principal book) + 644 (Other financial assets)",
            "calculated": 5 + 390 + 3845 + 644,
            "reported": 4884,
            "residual": (5 + 390 + 3845 + 644) - 4884,
            "prior_baseline_error": {
                "expression": "5390 (merged 5 and 390) + 3845 + 644",
                "calculated": 5390 + 3845 + 644,
                "reported": 4884,
                "residual": 9879 - 4884
            },
            "verdict": "PASS"
        },
        "ntu_principal_book_roll_note_1_1": {
            "description": "NTU 1H26 Note 1.1 (p. 13) Principal book portfolio roll-forward H1 2026",
            "expression": "3975 (Opening) + 382 (Additions) - 728 (Net collections) + 383 (CAEIR interest) - 167 (Impairment loss)",
            "calculated": 3975 + 382 - 728 + 383 - 167,
            "reported": 3845,
            "residual": (3975 + 382 - 728 + 383 - 167) - 3845,
            "verdict": "PASS"
        },
        "ntu_other_financial_assets_roll_note_1_2": {
            "description": "NTU 1H26 Note 1.2 (p. 13) Other financial assets roll-forward H1 2026",
            "expression": "702 (Opening) + 28 (Additions) - 116 (Collections) + 30 (Fair value movements)",
            "calculated": 702 + 28 - 116 + 30,
            "reported": 644,
            "residual": (702 + 28 - 116 + 30) - 644,
            "verdict": "PASS"
        },
        "ntu_total_pbd_carrying_value_scope": {
            "description": "NTU 1H26 Note 1 (p. 13) Total Purchased book debts carrying value reconciliation to SoFP line",
            "expression": "3845 (Principal book portfolio) + 644 (Other financial assets)",
            "calculated": 3845 + 644,
            "reported": 4489,
            "residual": (3845 + 644) - 4489,
            "recovery_split": {
                "after_12_months": 2688 + 490,
                "after_12_months_reported": 3178,
                "within_12_months": 1157 + 154,
                "within_12_months_reported": 1311,
                "total_from_splits": 3178 + 1311,
                "total_reported": 4489,
                "residual": 0
            },
            "verdict": "PASS"
        },
        "ntu_ecl_allowance_h1_26_movement_note_6_1": {
            "description": "NTU 1H26 Note 6.1 (p. 24) ECL allowance movement across portfolio segments",
            "expression": "-241 (Unsecured) + 69 (Debt review) + 4 (Retail) + 1 (Secured)",
            "calculated": -241 + 69 + 4 + 1,
            "reported": -167,
            "residual": (-241 + 69 + 4 + 1) - (-167),
            "verdict": "PASS"
        },
        "ntu_ecl_allowance_vintage_breakdown_h1_26": {
            "description": "NTU 1H26 Note 6.1 (p. 24) Acquired vs Historical vintage split of H1 2026 ECL movement",
            "acquired_portfolios": 1 + 23 + 0 + 0,
            "historical_portfolios": -242 + 46 + 4 + 1,
            "net_movement_calculated": 24 - 191,
            "net_movement_reported": -167,
            "residual": (24 - 191) - (-167),
            "economic_interpretation": "167 is an impairment LOSS / reduction in cumulative impairment gain, NOT an impairment release.",
            "verdict": "PASS"
        },
        "ntu_ecl_allowance_closing_balance_mar_26": {
            "description": "NTU 1H26 Note 6.1 (p. 24) Balance roll-forward from Sep-25 to Mar-26",
            "expression": "598 (Opening Sep-25) - 167 (Impairment loss H1-26)",
            "calculated": 598 - 167,
            "reported": 431,
            "residual": (598 - 167) - 431,
            "verdict": "PASS"
        },
        "pan_fy25_gold_produced_disjoint_scope": {
            "description": "PAN FY25 Group gold produced disjoint operational components reconciliation",
            "expression": "92643 (Mining underground) + 2654 (Mining surface) + 98636 (Tailings) + 1081 (Buy-in) + 1513 (Surface feedstock)",
            "calculated": 92643 + 2654 + 98636 + 1081 + 1513,
            "reported": 196527,
            "residual": (92643 + 2654 + 98636 + 1081 + 1513) - 196527,
            "verdict": "PASS"
        },
        "pan_fy25_gold_produced_model_overlap_error": {
            "description": "PAN FY25 Model double-counting error by adding buy-in 1081 twice using Group total underground 93724",
            "expression": "93724 (Underground Group Total, already includes 1081 buy-in) + 2654 + 98636 + 1081 + 1513",
            "calculated": 93724 + 2654 + 98636 + 1081 + 1513,
            "reported": 196527,
            "residual": (93724 + 2654 + 98636 + 1081 + 1513) - 196527,
            "verdict": "FAIL_MODEL_ERROR"
        },
        "pan_fy26_gold_produced_disjoint_scope": {
            "description": "PAN FY26 Group gold produced disjoint components reconciliation",
            "expression": "105478 (Underground Group Total) + 2428 (Surface ops) + 113613 (Tailings) + 18667 (Buy-in) + 32124 (Surface feedstock)",
            "calculated": 105478 + 2428 + 113613 + 18667 + 32124,
            "reported": 272310,
            "residual": (105478 + 2428 + 113613 + 18667 + 32124) - 272310,
            "verdict": "PASS"
        },
        "pan_fy26_source_subtotal_differences": {
            "description": "PAN FY26 Genuine source PDF 1-ounce subtotal differences across tables",
            "underground_mining_components": "Barberton 65233 + Evander 40246",
            "underground_mining_calc": 65233 + 40246,
            "underground_group_total_printed": 105478,
            "underground_diff": (65233 + 40246) - 105478,
            "mining_total_components": "Barberton 71997 + Evander 46855",
            "mining_total_calc": 71997 + 46855,
            "mining_total_printed": 118853,
            "mining_total_diff": (71997 + 46855) - 118853,
            "group_total_sum": 118853 + 153458,
            "group_total_printed": 272310,
            "group_total_diff": (118853 + 153458) - 272310,
            "verdict": "PASS_CONFIRMED_SOURCE_ROUNDING"
        },
        "pan_fy25_tailings_internal_column_variance": {
            "description": "PAN FY25 MTR Tailings internal table variance between Column 6 and Column 14",
            "surface_ops_col6_mtr": 25043,
            "total_ops_col14_mtr": 30806,
            "variance": 30806 - 25043,
            "subtotal_col8_using_col14": 15224 + 52606 + 30806,
            "subtotal_col8_printed": 98636,
            "subtotal_col8_using_col6": 15224 + 52606 + 25043,
            "note": "Column 8 printed total 98636 incorporates 30806 from Column 14. 5763 oz equals FY26 MTR buy-in volume.",
            "verdict": "SOURCE_TABLE_INCONSISTENCY"
        }
    }

    out_path = os.path.join(os.path.dirname(__file__), 'reconciliations.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(reconciliations, f, indent=2)

    print(f"Executed {len(reconciliations)} independent reconciliations. Saved to {out_path}")

if __name__ == '__main__':
    run_reconciliations()
