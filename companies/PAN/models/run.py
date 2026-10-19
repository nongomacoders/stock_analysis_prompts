"""Report generator module for the 2-Year Analyst Forecast & Valuation.

Produces a formatted institutional summary report comparing FY26A vs FY27E vs FY28E,
with primary focus on Johannesburg Stock Exchange (JSE: PAN) trading in ZAR.
"""

from __future__ import annotations

import sys
from .macro_deck import MacroDeck, Scenario
from .two_year_model import TwoYearModel
from .multiples_valuation import ValuationEngine


def generate_analyst_report(scenario: Scenario = Scenario.BASE) -> str:
    macro_deck = MacroDeck.create(scenario)
    model = TwoYearModel(macro_deck=macro_deck)
    forecast = model.run()
    val_engine = ValuationEngine(forecast)
    multiples = val_engine.evaluate(target_ev_ebitda=3.5)
    grid = val_engine.sensitivity_grid(currency="ZAR")

    fy26 = forecast.fy26_actual
    fy27 = forecast.fy27
    fy28 = forecast.fy28

    lines = [
        f"# Institutional 2-Year Analyst Forecast Report: Pan African Resources PLC (JSE: PAN)",
        f"**Scenario**: {scenario.value.upper()} | **Primary Exchange**: JSE (ZAR) | **Date**: October 2026",
        "",
        "## 1. Executive Summary & 2-Year Trading Multiples",
        "",
        "| Valuation Metric | FY26 Actual | FY27E (1-Yr Fwd) | FY28E (2-Yr Fwd) |",
        "|---|---|---|---|",
        f"| **JSE Share Price (ZAR)** | R{multiples.fy26_actual.share_price_zar:.2f} | R{multiples.fy27_forward.share_price_zar:.2f} | R{multiples.fy28_forward.share_price_zar:.2f} |",
        f"| **Gold Sold (oz)** | {fy26.gold_sold_total_oz:,.0f} | {fy27.gold_sold_oz:,.0f} | {fy28.gold_sold_oz:,.0f} |",
        f"| **Realized Gold Price (US$/oz)** | ${fy26.realized_gold_price_usd_per_oz:,.0f} | ${fy27.macro.gold_price_usd_per_oz:,.0f} | ${fy28.macro.gold_price_usd_per_oz:,.0f} |",
        f"| **Revenue (US$m)** | ${fy26.revenue_usdm:,.1f} | ${fy27.revenue_usdm:,.1f} | ${fy28.revenue_usdm:,.1f} |",
        f"| **Group Adjusted EBITDA (US$m)** | ${fy26.group_adjusted_ebitda_usdm:,.1f} | ${fy27.adjusted_ebitda_usdm:,.1f} | ${fy28.adjusted_ebitda_usdm:,.1f} |",
        f"| **Attributable Net Profit / HEPS (US$m)** | ${fy26.profit_after_tax_pat_usdm:,.1f} | ${fy27.profit_after_tax_pat_usdm:,.1f} | ${fy28.profit_after_tax_pat_usdm:,.1f} |",
        f"| **Headline EPS (ZAR cents)** | {fy26.headline_eps_zar_cents:.1f}c | {fy27.heps_zar_cents:.1f}c | {fy28.heps_zar_cents:.1f}c |",
        f"| **Headline EPS (GB pence)** | {fy26.headline_eps_gb_pence:.2f}p | {fy27.heps_gb_pence:.2f}p | {fy28.heps_gb_pence:.2f}p |",
        f"| **Free Cash Flow to Equity (US$m)** | ${fy26.levered_free_cash_flow_usdm:,.1f} | ${fy27.free_cash_flow_to_equity_usdm:,.1f} | ${fy28.free_cash_flow_to_equity_usdm:,.1f} |",
        f"| **Total Capex (US$m)** | ${fy26.total_capex_accrual_usdm:,.1f} | ${fy27.total_capex_usdm:,.1f} | ${fy28.total_capex_usdm:,.1f} |",
        f"| **Closing Net Cash (US$m)** | ${-fy26.net_debt_usdm:,.1f} | ${fy27.closing_net_cash_usdm:,.1f} | ${fy28.closing_net_cash_usdm:,.1f} |",
        f"| **EV / Adjusted EBITDA** | {multiples.fy26_actual.ev_to_ebitda:.2f}x | {multiples.fy27_forward.ev_to_ebitda:.2f}x | {multiples.fy28_forward.ev_to_ebitda:.2f}x |",
        f"| **Price / Earnings (P/E on HEPS)** | {multiples.fy26_actual.price_to_earnings_heps:.2f}x | {multiples.fy27_forward.price_to_earnings_heps:.2f}x | {multiples.fy28_forward.price_to_earnings_heps:.2f}x |",
        f"| **Free Cash Flow Yield (%)** | {multiples.fy26_actual.free_cash_flow_yield_pct:.2f}% | {multiples.fy27_forward.free_cash_flow_yield_pct:.2f}% | {multiples.fy28_forward.free_cash_flow_yield_pct:.2f}% |",
        f"| **Dividend Yield (%)** | {multiples.fy26_actual.dividend_yield_pct:.2f}% | {multiples.fy27_forward.dividend_yield_pct:.2f}% | {multiples.fy28_forward.dividend_yield_pct:.2f}% |",
        "",
        f"### 12-Month JSE Price Target & Return:",
        f"- **12-Month JSE Target Price**: **ZAR {multiples.target_price_12m_zar:.2f}** (R{multiples.target_price_12m_zar:.2f} / share) [US${multiples.target_price_12m_usd:.2f} / {multiples.target_price_12m_gb_pence:.1f}p]",
        f"- **Current JSE Share Price**: **ZAR {multiples.fy26_actual.share_price_zar:.2f}** (R{multiples.fy26_actual.share_price_zar:.2f} / share)",
        f"- **Implied JSE Capital Upside**: **+{multiples.implied_upside_pct:.1f}%**",
        "",
        "## 2. Asset-by-Asset Operational Forecast (FY27 & FY28)",
        "",
        "| Operation / Mine | FY27E Gold Sold (oz) | FY27E AISC ($/oz) | FY27E Capex ($m) | FY28E Gold Sold (oz) | FY28E AISC ($/oz) | FY28E Capex ($m) |",
        "|---|---|---|---|---|---|---|",
    ]

    for key, a27 in fy27.assets.items():
        a28 = fy28.assets[key]
        lines.append(
            f"| **{a27.name}** | {a27.gold_sold_oz:,.0f} | ${a27.aisc_usd_per_oz:,.0f} | ${a27.total_capex_usdm:.1f} | {a28.gold_sold_oz:,.0f} | ${a28.aisc_usd_per_oz:,.0f} | ${a28.total_capex_usdm:.1f} |"
        )

    lines.extend([
        "",
        "## 3. 2D Sensitivity Grid: 12-Month JSE Target Share Price (ZAR)",
        "",
        "| Gold Price \\ USD/ZAR | " + " | ".join(grid[list(grid.keys())[0]].keys()) + " |",
        "|---|---" + "|---" * len(grid[list(grid.keys())[0]]) + "|",
    ])

    for p_key, row in grid.items():
        row_str = " | ".join(f"R{v:.2f}" for v in row.values())
        lines.append(f"| **{p_key}** | {row_str} |")

    return "\n".join(lines)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    report = generate_analyst_report(Scenario.BASE)
    print(report)
