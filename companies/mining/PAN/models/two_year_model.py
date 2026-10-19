"""2-Year Operational & Financial Forecast Engine (FY27 & FY28).

Calculates bottom-up mine production, unit costs, capex cliff, consolidated P&L,
cash flow, and headline earnings per share.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .data_loader import FY26Baseline, AssetBaseline, load_fy26_baseline
from .macro_deck import MacroDeck, Scenario, YearMacro


@dataclass(frozen=True)
class AssetProjection:
    name: str
    fiscal_year: str
    gold_sold_oz: float
    cash_cost_usd_per_oz: float
    aisc_usd_per_oz: float
    sustaining_capex_usdm: float
    expansion_capex_usdm: float
    total_capex_usdm: float
    adjusted_ebitda_usdm: float
    revenue_usdm: float
    cost_of_production_usdm: float


@dataclass(frozen=True)
class ConsolidatedYear:
    fiscal_year: str
    macro: YearMacro
    gold_sold_oz: float

    # Income Statement (USD millions)
    revenue_usdm: float
    cost_of_production_usdm: float
    royalties_usdm: float
    gross_profit_usdm: float
    corporate_overhead_usdm: float
    other_divisions_usdm: float
    adjusted_ebitda_usdm: float
    depreciation_amortisation_usdm: float
    operating_profit_ebit_usdm: float
    net_finance_income_usdm: float
    profit_before_tax_usdm: float
    income_tax_expense_usdm: float
    profit_after_tax_pat_usdm: float
    headline_earnings_usdm: float

    # Per Share Metrics
    diluted_shares_m: float
    heps_usd_cents: float
    heps_zar_cents: float
    heps_gb_pence: float

    # Cash Flow & Capital Allocation (USD millions)
    operating_cash_flow_usdm: float
    working_capital_movement_usdm: float
    sustaining_capex_usdm: float
    expansion_capex_usdm: float
    total_capex_usdm: float
    free_cash_flow_to_equity_usdm: float
    dividend_payment_usdm: float
    dividend_per_share_zar_cents: float
    dividend_per_share_gb_pence: float
    closing_net_cash_usdm: float

    # Asset-by-asset details
    assets: Dict[str, AssetProjection]


@dataclass(frozen=True)
class ConsolidatedForecast:
    scenario: Scenario
    fy26_actual: FY26Baseline
    fy27: ConsolidatedYear
    fy28: ConsolidatedYear


class TwoYearModel:
    """Bottom-up deterministic model projecting FY27 and FY28."""

    def __init__(self, baseline: FY26Baseline | None = None, macro_deck: MacroDeck | None = None):
        self.baseline = baseline or load_fy26_baseline()
        self.macro_deck = macro_deck or MacroDeck.create(Scenario.BASE)

    def project_asset_fy27(self, key: str, macro: YearMacro) -> AssetProjection:
        base = self.baseline.assets[key]
        p = macro.gold_price_usd_per_oz
        inf = macro.cost_inflation_pct

        if key == "barberton_underground":
            oz = 72_000.0
            cash_cost = base.cash_cost_usd_per_oz * (1.0 + inf * 0.7)
            aisc = 2_620.0
            sust_capex = 13.5
            exp_capex = 18.0
        elif key == "btrp":
            oz = 20_000.0  # Ramping up with initial Royal Sheba open-pit feed
            cash_cost = 1_420.0
            aisc = 1_480.0
            sust_capex = 0.5
            exp_capex = 7.0  # Royal Sheba initial development
        elif key == "evander_underground":
            oz = 44_000.0  # Organic Kimberley reef mining
            cash_cost = 1_720.0
            aisc = 1_750.0  # Normalizing from 1,914 down toward organic 1,698
            sust_capex = 2.0
            exp_capex = 28.0  # Deepening 24-26L tapering
        elif key == "elikhulu":
            oz = 56_000.0
            cash_cost = base.cash_cost_usd_per_oz * (1.0 + inf * 0.5)
            aisc = 1_240.0
            sust_capex = 2.0
            exp_capex = 5.0
        elif key == "mtr":
            oz = 63_000.0  # Full year of 12Mtpa throughput
            cash_cost = 1_180.0
            aisc = 1_320.0
            sust_capex = 3.5
            exp_capex = 5.0  # Construction finished
        elif key == "tennant":
            oz = 45_000.0  # Nobles CIL hub optimized
            cash_cost = 1_550.0
            aisc = 2_150.0
            sust_capex = 3.5
            exp_capex = 15.0  # Tapering from 68.4m
        else:
            raise KeyError(f"Unknown asset: {key}")

        tot_capex = sust_capex + exp_capex
        rev = (oz * p) / 1_000_000.0
        prod_cost = (oz * cash_cost) / 1_000_000.0
        ebitda = rev - prod_cost - (oz * 45.0 / 1_000_000.0)  # Minor site overhead

        return AssetProjection(
            name=base.name,
            fiscal_year="FY27E",
            gold_sold_oz=oz,
            cash_cost_usd_per_oz=round(cash_cost, 1),
            aisc_usd_per_oz=round(aisc, 1),
            sustaining_capex_usdm=sust_capex,
            expansion_capex_usdm=exp_capex,
            total_capex_usdm=tot_capex,
            adjusted_ebitda_usdm=round(ebitda, 1),
            revenue_usdm=round(rev, 2),
            cost_of_production_usdm=round(prod_cost, 2),
        )

    def project_asset_fy28(self, key: str, macro: YearMacro) -> AssetProjection:
        base = self.baseline.assets[key]
        p = macro.gold_price_usd_per_oz
        inf = macro.cost_inflation_pct

        if key == "barberton_underground":
            oz = 75_000.0
            cash_cost = base.cash_cost_usd_per_oz * (1.0 + inf * 1.2)
            aisc = 2_650.0
            sust_capex = 14.0
            exp_capex = 10.0
        elif key == "btrp":
            oz = 30_000.0  # Full Royal Sheba contribution
            cash_cost = 1_380.0
            aisc = 1_450.0
            sust_capex = 1.0
            exp_capex = 5.0
        elif key == "evander_underground":
            oz = 46_000.0
            cash_cost = 1_700.0
            aisc = 1_740.0
            sust_capex = 2.5
            exp_capex = 12.0
        elif key == "elikhulu":
            oz = 56_000.0
            cash_cost = 1_120.0
            aisc = 1_250.0
            sust_capex = 2.5
            exp_capex = 0.0
        elif key == "mtr":
            oz = 65_000.0
            cash_cost = 1_160.0
            aisc = 1_300.0
            sust_capex = 4.0
            exp_capex = 0.0
        elif key == "tennant":
            oz = 50_000.0
            cash_cost = 1_500.0
            aisc = 2_100.0
            sust_capex = 4.0
            exp_capex = 3.0
        else:
            raise KeyError(f"Unknown asset: {key}")

        tot_capex = sust_capex + exp_capex
        rev = (oz * p) / 1_000_000.0
        prod_cost = (oz * cash_cost) / 1_000_000.0
        ebitda = rev - prod_cost - (oz * 45.0 / 1_000_000.0)

        return AssetProjection(
            name=base.name,
            fiscal_year="FY28E",
            gold_sold_oz=oz,
            cash_cost_usd_per_oz=round(cash_cost, 1),
            aisc_usd_per_oz=round(aisc, 1),
            sustaining_capex_usdm=sust_capex,
            expansion_capex_usdm=exp_capex,
            total_capex_usdm=tot_capex,
            adjusted_ebitda_usdm=round(ebitda, 1),
            revenue_usdm=round(rev, 2),
            cost_of_production_usdm=round(prod_cost, 2),
        )

    def forecast_year(self, fiscal_year: str, macro: YearMacro, opening_net_cash: float) -> ConsolidatedYear:
        is_fy27 = fiscal_year == "FY27E"
        assets = {}
        for key in self.baseline.assets:
            if is_fy27:
                assets[key] = self.project_asset_fy27(key, macro)
            else:
                assets[key] = self.project_asset_fy28(key, macro)

        total_oz = sum(a.gold_sold_oz for a in assets.values())
        raw_rev = sum(a.revenue_usdm for a in assets.values())
        raw_prod_cost = sum(a.cost_of_production_usdm for a in assets.values()) - macro.solar_savings_usdm

        # Refined gold formula royalty: 0.5% + (EBIT / (Sales * 12.5)), capped at 5.0%
        # At high gold margins, royalty scales toward ~1.6% - 2.0%
        royalty_rate = 0.016 if is_fy27 else 0.017
        royalties = round(raw_rev * royalty_rate, 1)

        gross_profit = round(raw_rev - raw_prod_cost - royalties, 1)
        corp_overhead = 56.0 if is_fy27 else 62.0  # Absorbs SBP and corporate run-rate
        other_divs = 2.0

        ebitda = round(gross_profit - corp_overhead - other_divs, 1)
        da = 72.0 if is_fy27 else 75.0
        ebit = round(ebitda - da, 1)

        # Net finance income on growing net cash buffer (interest ~4.0% on net cash)
        net_fin_income = round(max(5.0, opening_net_cash * 0.04), 1)
        pbt = round(ebit + net_fin_income, 1)

        # Tax calculation applying blended cash tax rate from deep research
        tax_expense = round(pbt * macro.cash_tax_rate, 1)
        pat = round(pbt - tax_expense, 1)
        headline_earnings = pat  # In forward years with no major impairments/disposals, HEPS ~ PAT

        shares_m = self.baseline.shares_in_issue_diluted_m
        heps_usd = round((headline_earnings * 100.0) / shares_m, 2)  # US cents
        heps_zar = round(heps_usd * macro.usd_zar_rate, 1)  # ZAR cents
        heps_gbp = round((heps_zar / macro.usd_zar_rate) * 0.765, 2)  # GB pence

        sust_capex = round(sum(a.sustaining_capex_usdm for a in assets.values()) + 7.0, 1)  # +7m solar/ESG
        exp_capex = round(sum(a.expansion_capex_usdm for a in assets.values()), 1)
        tot_capex = round(sust_capex + exp_capex, 1)

        wc_norm = -20.0 if is_fy27 else 0.0  # Reversing the FY26 payables stretch
        ocf = round(ebitda - royalties - tax_expense + net_fin_income, 1)
        fcfe = round(ocf + wc_norm - tot_capex, 1)

        payout_ratio = 0.40  # 40% payout policy
        dividend_pay = round(fcfe * payout_ratio, 1)
        dps_zar = round((dividend_pay * 1_000_000.0 * macro.usd_zar_rate * 100.0) / (shares_m * 1_000_000.0), 1)
        dps_gbp = round(dps_zar / (macro.usd_zar_rate * 1.30), 2)

        closing_cash = round(opening_net_cash + fcfe - dividend_pay, 1)

        return ConsolidatedYear(
            fiscal_year=fiscal_year,
            macro=macro,
            gold_sold_oz=total_oz,
            revenue_usdm=raw_rev,
            cost_of_production_usdm=raw_prod_cost,
            royalties_usdm=royalties,
            gross_profit_usdm=gross_profit,
            corporate_overhead_usdm=corp_overhead,
            other_divisions_usdm=other_divs,
            adjusted_ebitda_usdm=ebitda,
            depreciation_amortisation_usdm=da,
            operating_profit_ebit_usdm=ebit,
            net_finance_income_usdm=net_fin_income,
            profit_before_tax_usdm=pbt,
            income_tax_expense_usdm=tax_expense,
            profit_after_tax_pat_usdm=pat,
            headline_earnings_usdm=headline_earnings,
            diluted_shares_m=shares_m,
            heps_usd_cents=heps_usd,
            heps_zar_cents=heps_zar,
            heps_gb_pence=heps_gbp,
            operating_cash_flow_usdm=ocf,
            working_capital_movement_usdm=wc_norm,
            sustaining_capex_usdm=sust_capex,
            expansion_capex_usdm=exp_capex,
            total_capex_usdm=tot_capex,
            free_cash_flow_to_equity_usdm=fcfe,
            dividend_payment_usdm=dividend_pay,
            dividend_per_share_zar_cents=dps_zar,
            dividend_per_share_gb_pence=dps_gbp,
            closing_net_cash_usdm=closing_cash,
            assets=assets,
        )

    def run(self) -> ConsolidatedForecast:
        """Executes the full 2-year projection."""
        init_net_cash = -self.baseline.net_debt_usdm  # Starting positive net cash (185.6m)
        fy27 = self.forecast_year("FY27E", self.macro_deck.fy27, init_net_cash)
        fy28 = self.forecast_year("FY28E", self.macro_deck.fy28, fy27.closing_net_cash_usdm)

        return ConsolidatedForecast(
            scenario=self.macro_deck.scenario,
            fy26_actual=self.baseline,
            fy27=fy27,
            fy28=fy28,
        )
