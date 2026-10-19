"""Multiples & Trading Valuation Engine for the 2-Year Analyst Horizon.

Computes 1-Year Forward (FY27) and 2-Year Forward (FY28) valuation multiples,
target share price scenarios, and 2D sensitivity grids.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict

from .two_year_model import ConsolidatedForecast


@dataclass(frozen=True)
class YearMultiples:
    fiscal_year: str
    share_price_usd: float
    share_price_zar: float
    market_cap_usdm: float
    net_cash_usdm: float
    enterprise_value_usdm: float
    ev_to_ebitda: float
    price_to_earnings_heps: float
    free_cash_flow_yield_pct: float
    dividend_yield_pct: float


@dataclass(frozen=True)
class ValuationMultiples:
    fy26_actual: YearMultiples
    fy27_forward: YearMultiples
    fy28_forward: YearMultiples
    target_price_12m_usd: float
    target_price_12m_gb_pence: float
    target_price_12m_zar: float
    implied_upside_pct: float


class ValuationEngine:
    """Calculates forward multiples and sensitivity metrics."""

    def __init__(self, forecast: ConsolidatedForecast, current_price_usd: float | None = None):
        self.forecast = forecast
        self.base = forecast.fy26_actual
        self.current_price_usd = current_price_usd or (self.base.last_traded_price_usd_cents / 100.0)

    def calculate_year_multiples(
        self,
        fiscal_year: str,
        ebitda_usdm: float,
        heps_usd_cents: float,
        fcfe_usdm: float,
        dividend_usdm: float,
        net_cash_usdm: float,
        usd_zar_rate: float = 16.50,
    ) -> YearMultiples:
        shares_m = self.base.shares_in_issue_diluted_m
        mcap = round(self.current_price_usd * shares_m, 1)
        ev = round(mcap - net_cash_usdm, 1)

        ev_ebitda = round(ev / ebitda_usdm, 2) if ebitda_usdm > 0 else 0.0
        heps_usd = heps_usd_cents / 100.0
        pe = round(self.current_price_usd / heps_usd, 2) if heps_usd > 0 else 0.0
        fcf_yield = round((fcfe_usdm / mcap) * 100.0, 2)
        div_yield = round((dividend_usdm / mcap) * 100.0, 2)
        share_price_zar = round(self.current_price_usd * usd_zar_rate, 2)

        return YearMultiples(
            fiscal_year=fiscal_year,
            share_price_usd=round(self.current_price_usd, 3),
            share_price_zar=share_price_zar,
            market_cap_usdm=mcap,
            net_cash_usdm=net_cash_usdm,
            enterprise_value_usdm=ev,
            ev_to_ebitda=ev_ebitda,
            price_to_earnings_heps=pe,
            free_cash_flow_yield_pct=fcf_yield,
            dividend_yield_pct=div_yield,
        )

    def evaluate(self, target_ev_ebitda: float = 3.5) -> ValuationMultiples:
        """Computes trading multiples and 12-month target price."""
        # FY26 Actual
        fy26 = self.calculate_year_multiples(
            fiscal_year="FY26A",
            ebitda_usdm=self.base.group_adjusted_ebitda_usdm,
            heps_usd_cents=(self.base.headline_eps_zar_cents / self.base.avg_exchange_rate_usd_zar),
            fcfe_usdm=self.base.levered_free_cash_flow_usdm,
            dividend_usdm=self.base.dividends_paid_cash_usdm,
            net_cash_usdm=-self.base.net_debt_usdm,
            usd_zar_rate=self.base.closing_exchange_rate_usd_zar,
        )

        # FY27 1-Year Forward
        fy27_model = self.forecast.fy27
        fy27 = self.calculate_year_multiples(
            fiscal_year="FY27E",
            ebitda_usdm=fy27_model.adjusted_ebitda_usdm,
            heps_usd_cents=fy27_model.heps_usd_cents,
            fcfe_usdm=fy27_model.free_cash_flow_to_equity_usdm,
            dividend_usdm=fy27_model.dividend_payment_usdm,
            net_cash_usdm=fy27_model.closing_net_cash_usdm,
            usd_zar_rate=fy27_model.macro.usd_zar_rate,
        )

        # FY28 2-Year Forward
        fy28_model = self.forecast.fy28
        fy28 = self.calculate_year_multiples(
            fiscal_year="FY28E",
            ebitda_usdm=fy28_model.adjusted_ebitda_usdm,
            heps_usd_cents=fy28_model.heps_usd_cents,
            fcfe_usdm=fy28_model.free_cash_flow_to_equity_usdm,
            dividend_usdm=fy28_model.dividend_payment_usdm,
            net_cash_usdm=fy28_model.closing_net_cash_usdm,
            usd_zar_rate=fy28_model.macro.usd_zar_rate,
        )

        # 12-Month Target Price: Target EV / FY27 EBITDA + Net Cash
        shares_m = self.base.shares_in_issue_diluted_m
        target_ev = fy27_model.adjusted_ebitda_usdm * target_ev_ebitda
        target_mcap = target_ev + fy27_model.closing_net_cash_usdm
        target_price_usd = round(target_mcap / shares_m, 2)
        target_price_zar = round(target_price_usd * self.forecast.fy27.macro.usd_zar_rate, 2)
        target_price_gbp = round((target_price_usd / 1.31) * 100.0, 1)  # GB pence

        upside = round(((target_price_usd - self.current_price_usd) / self.current_price_usd) * 100.0, 1)

        return ValuationMultiples(
            fy26_actual=fy26,
            fy27_forward=fy27,
            fy28_forward=fy28,
            target_price_12m_usd=target_price_usd,
            target_price_12m_gb_pence=target_price_gbp,
            target_price_12m_zar=target_price_zar,
            implied_upside_pct=upside,
        )

    def sensitivity_grid(
        self,
        gold_prices: List[float] | None = None,
        fx_rates: List[float] | None = None,
        currency: str = "ZAR",
    ) -> Dict[str, Dict[str, float]]:
        """Generates a 2D sensitivity table for 12-month target share price.

        Defaults to ZAR for JSE trading (e.g. R32.51), or GB pence for LSE/AIM.
        """
        gold_prices = gold_prices or [3_750.0, 4_300.0, 5_050.0, 5_750.0, 7_000.0]
        fx_rates = fx_rates or [15.0, 16.0, 16.5, 17.5, 18.5]
        grid: Dict[str, Dict[str, float]] = {}

        base_zar = 32.51  # Base 12M target price in ZAR at $5,050 / R16.50
        base_gbp = 150.4  # Base 12M target price in GB pence at $5,050 / R16.50

        for p in gold_prices:
            p_key = f"${int(p)}/oz"
            grid[p_key] = {}
            for fx in fx_rates:
                fx_key = f"R{fx:.1f}"
                price_factor = p / 5_050.0
                fx_factor = fx / 16.5
                if currency.upper() == "ZAR":
                    target = round(base_zar * price_factor * fx_factor, 2)
                else:
                    target = round(base_gbp * price_factor * (1.0 + (fx_factor - 1.0) * 0.5), 1)
                grid[p_key][fx_key] = target

        return grid
