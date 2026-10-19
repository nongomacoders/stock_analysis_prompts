"""2-Year Valuation and Forecasting Package for Pan African Resources PLC.

Strictly bounded to an institutional 2-year analyst horizon (FY27 & FY28),
anchoring baseline numbers in documents/analysis.sqlite and macro parameters
in deep_research/01_two_year_gold_price_forecast.pdf and
deep_research/02_sa_mining_tax_eskom_solar_tennant_creek.txt.
"""

from .data_loader import load_fy26_baseline
from .macro_deck import MacroDeck, Scenario
from .two_year_model import TwoYearModel, AssetProjection, ConsolidatedForecast
from .multiples_valuation import ValuationEngine, ValuationMultiples

__all__ = [
    "load_fy26_baseline",
    "MacroDeck",
    "Scenario",
    "TwoYearModel",
    "AssetProjection",
    "ConsolidatedForecast",
    "ValuationEngine",
    "ValuationMultiples",
]
