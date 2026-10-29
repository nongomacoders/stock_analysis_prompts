import json

reconciliations = {
    "valuation_arithmetic": {
        "ev_zar_m": 15995.0,
        "associates_zar_m": 600.0,
        "cash_zar_m": 500.0,
        "borrowings_zar_m": -3694.0,
        "nci_zar_m": -200.0,
        "equity_value_calc_zar_m": 15995.0 + 600.0 + 500.0 - 3694.0 - 200.0,
        "wanos_m": 857.0,
        "per_share_calc_zar": (15995.0 + 600.0 + 500.0 - 3694.0 - 200.0) / 857.0,
        "baseline_reported_per_share_zar": 35.00,
        "discrepancy_zar": 35.00 - ((15995.0 + 600.0 + 500.0 - 3694.0 - 200.0) / 857.0),
        "target_plug_equity_zar_m": 35.00 * 857.0 - (15995.0 + 600.0 + 500.0 - 3694.0 - 200.0)
    },
    "cash_flow": {
        "cash_from_trading_zar_k": 3124134,
        "working_capital_zar_k": 125820,
        "cash_from_operations_zar_k": 3124134 + 125820,
        "finance_income_zar_k": 28492,
        "finance_costs_zar_k": -559644,
        "tax_paid_zar_k": -401870,
        "dividends_paid_zar_k": -524221,
        "statutory_ocf_zar_k": 3124134 + 125820 + 28492 - 559644 - 401870 - 524221,
        "capex_maintain_zar_k": -373968,
        "capex_expand_zar_k": -729620,
        "total_capex_zar_k": -1103588,
        "lease_principal_zar_k": -691992,
        "baseline_subtraction_residual_zar_k": 1792711 - 1103588 - 691992,
        "baseline_reported_pre_div_fcfe_zar_k": 521000,
        "addback_dividends_residual_zar_k": (1792711 - 1103588 - 691992) + 524221
    },
    "debt_and_cash": {
        "bank_balances_zar_k": 104996,
        "call_accounts_zar_k": 10669,
        "cash_on_hand_zar_k": 18730,
        "gross_cash_zar_k": 134395,
        "bank_overdraft_zar_k": -1301359,
        "net_cash_and_equivalents_zar_k": -1166964,
        "non_current_loans_zar_k": 1509942,
        "current_loans_zar_k": 517636,
        "total_loans_ex_leases_zar_k": 2027578,
        "net_debt_ex_leases_calc_zar_k": 2027578 - (-1166964),
        "current_lease_liability_zar_k": 695209,
        "non_current_lease_liability_zar_k": 2248024,
        "total_lease_liability_zar_k": 2943233,
        "scf_in_trade_payables_zar_k": 965000,
        "total_indebtedness_with_scf_and_leases_zar_k": 3194542 + 2943233 + 965000
    },
    "earnings_and_shares": {
        "attributable_pat_zar_k": 978894,
        "disposal_ppe_zar_k": -294,
        "jv_impairment_zar_k": 18,
        "third_party_compensation_zar_k": -5283,
        "tax_on_adjustments_zar_k": 1486,
        "headline_earnings_calc_zar_k": 978894 - 294 + 18 - 5283 + 1486,
        "wanos_basic": 857006527,
        "wanos_diluted": 857817750,
        "basic_heps_calc_cents": (974821 * 1000 / 857006527) * 100,
        "diluted_heps_calc_cents": (974821 * 1000 / 857817750) * 100,
        "basic_eps_calc_cents": (978894 * 1000 / 857006527) * 100,
        "diluted_eps_calc_cents": (978894 * 1000 / 857817750) * 100
    }
}

print(json.dumps(reconciliations, indent=2))
