"""Macroeconomic scenario deck for the 2-Year Forecast Window (FY27 & FY28).

Incorporates institutional gold price targets, USD/ZAR and USD/AUD exchange rates,
cash tax transition rates, and solar power savings from deep research.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Scenario(str, Enum):
    BEAR = "bear"
    BASE = "base"
    BULL = "bull"


@dataclass(frozen=True)
class YearMacro:
    fiscal_year: str
    gold_price_usd_per_oz: float
    usd_zar_rate: float
    usd_aud_rate: float  # AUD per USD (e.g. 1.44 means 1 AUD = 0.694 USD)
    cash_tax_rate: float  # Blended group cash tax percentage
    solar_savings_usdm: float  # Net cash power savings from solar fleet
    cost_inflation_pct: float  # Operating cost inflation


@dataclass(frozen=True)
class MacroDeck:
    scenario: Scenario
    fy27: YearMacro
    fy28: YearMacro

    @classmethod
    def create(cls, scenario: Scenario = Scenario.BASE) -> MacroDeck:
        if scenario == Scenario.BASE:
            return cls(
                scenario=scenario,
                fy27=YearMacro(
                    fiscal_year="FY27E",
                    gold_price_usd_per_oz=5_050.0,
                    usd_zar_rate=16.50,
                    usd_aud_rate=1.44,
                    cash_tax_rate=0.208,  # 20.8% blended cash tax
                    solar_savings_usdm=12.5,
                    cost_inflation_pct=0.055,
                ),
                fy28=YearMacro(
                    fiscal_year="FY28E",
                    gold_price_usd_per_oz=5_750.0,
                    usd_zar_rate=16.50,
                    usd_aud_rate=1.44,
                    cash_tax_rate=0.275,  # 27.5% blended cash tax
                    solar_savings_usdm=18.5,
                    cost_inflation_pct=0.050,
                ),
            )
        elif scenario == Scenario.BEAR:
            return cls(
                scenario=scenario,
                fy27=YearMacro(
                    fiscal_year="FY27E",
                    gold_price_usd_per_oz=3_750.0,
                    usd_zar_rate=18.00,
                    usd_aud_rate=1.45,
                    cash_tax_rate=0.180,
                    solar_savings_usdm=11.5,
                    cost_inflation_pct=0.070,
                ),
                fy28=YearMacro(
                    fiscal_year="FY28E",
                    gold_price_usd_per_oz=4_300.0,
                    usd_zar_rate=18.00,
                    usd_aud_rate=1.45,
                    cash_tax_rate=0.250,
                    solar_savings_usdm=17.0,
                    cost_inflation_pct=0.065,
                ),
            )
        elif scenario == Scenario.BULL:
            return cls(
                scenario=scenario,
                fy27=YearMacro(
                    fiscal_year="FY27E",
                    gold_price_usd_per_oz=5_500.0,
                    usd_zar_rate=15.50,
                    usd_aud_rate=1.40,
                    cash_tax_rate=0.220,
                    solar_savings_usdm=13.5,
                    cost_inflation_pct=0.045,
                ),
                fy28=YearMacro(
                    fiscal_year="FY28E",
                    gold_price_usd_per_oz=7_000.0,
                    usd_zar_rate=15.50,
                    usd_aud_rate=1.40,
                    cash_tax_rate=0.285,
                    solar_savings_usdm=19.5,
                    cost_inflation_pct=0.040,
                ),
            )
        raise ValueError(f"Unknown scenario: {scenario}")
