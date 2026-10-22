#!/usr/bin/env python3
"""Daily Analyst Workbench Scaffolding Tool.

Initializes a new company hub under companies/<SECTOR>/<TICKER>/ with standardized
directories for sources, valuation models, deep research, and analyst briefs.

Usage:
    python new_company.py HAR --sector mining --name "Harmony Gold Mining Company Ltd"
    python new_company.py LEW --sector retail --name "Lewis Group Ltd"
    python new_company.py SBK --sector finance --name "Standard Bank Group Ltd"
    python new_company.py MTN --sector telcos --name "MTN Group Ltd"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from companies.sectors import get_all_sector_codes

ROOT = Path(__file__).resolve().parent
COMPANIES_DIR = ROOT / "companies"
SUPPORTED_SECTORS = get_all_sector_codes()


def create_company(ticker: str, name: str | None = None, sector: str = "mining") -> Path:
    ticker = ticker.upper().strip()
    company_name = name or ticker
    sector = (sector or "mining").lower().strip()

    if sector not in SUPPORTED_SECTORS:
        raise ValueError(f"Invalid sector {sector!r}. Choose from: {SUPPORTED_SECTORS}")

    sector_dir = COMPANIES_DIR / sector
    sector_dir.mkdir(parents=True, exist_ok=True)
    if not (sector_dir / "__init__.py").exists():
        (sector_dir / "__init__.py").write_text(f'"""{sector.capitalize()} sector companies."""\n', encoding="utf-8")

    company_dir = sector_dir / ticker

    if company_dir.exists():
        print(f"[*] Company directory already exists: {company_dir}")
        return company_dir

    # Create directory tree
    sources_dir = company_dir / "sources"
    models_dir = company_dir / "models"
    research_dir = company_dir / "research"
    briefs_dir = company_dir / "briefs"

    for d in [sources_dir, models_dir, research_dir, briefs_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # 1. companies/<SECTOR>/<TICKER>/__init__.py
    (company_dir / "__init__.py").write_text(
        f'"""{company_name} (Ticker: {ticker}, Sector: {sector})."""\n',
        encoding="utf-8",
    )

    # 2. companies/<SECTOR>/<TICKER>/sources/README.md
    (sources_dir / "README.md").write_text(
        f"# Source Documents: {company_name} ({ticker})\n\n"
        f"Drop original company PDF reports, presentations, and SENS announcements here.\n"
        f"Then open the PDF in the capture app (`Run Capture.cmd` or `python app.py`) to scan sections.\n",
        encoding="utf-8",
    )

    # 3. companies/<SECTOR>/<TICKER>/research/README.md
    (research_dir / "README.md").write_text(
        f"# Deep Research: {company_name} ({ticker})\n\n"
        f"Save targeted Gemini Argon deep research outputs (PDFs, text reports) here.\n"
        f"Recommended naming: `01_topic_description.pdf`, `02_topic_description.txt`.\n",
        encoding="utf-8",
    )

    # 4. companies/<SECTOR>/<TICKER>/briefs/README.md
    (briefs_dir / "README.md").write_text(
        f"# Analyst Briefs: {company_name} ({ticker})\n\n"
        f"Generated 2-year forecast reports, reading briefs, and investment memos are saved here.\n",
        encoding="utf-8",
    )

    # 5. companies/<SECTOR>/<TICKER>/models/config.py
    reporting_currency = "ZAR" if sector in ["retail", "reit", "it", "construction", "finance", "telcos"] else "USD"
    (models_dir / "config.py").write_text(
        f'"""Configuration & baseline parameters for {company_name} ({ticker})."""\n\n'
        f"TICKER = {ticker!r}\n"
        f"COMPANY_NAME = {company_name!r}\n"
        f"SECTOR = {sector!r}\n"
        f"REPORTING_CURRENCY = {reporting_currency!r}\n"
        f"LOCAL_CURRENCY = 'ZAR'\n"
        f"SHARES_IN_ISSUE_M = 100.0\n",
        encoding="utf-8",
    )

    # 6. companies/<SECTOR>/<TICKER>/models/__init__.py
    (models_dir / "__init__.py").write_text(
        f'"""Valuation & forecast models for {company_name} ({ticker})."""\n',
        encoding="utf-8",
    )

    # 7. companies/<SECTOR>/<TICKER>/models/run.py
    (models_dir / "run.py").write_text(
        f'"""CLI Runner for {company_name} ({ticker}) 2-Year Forecast."""\n\n'
        f"from .config import TICKER, COMPANY_NAME, SECTOR\n\n"
        f"def main():\n"
        f"    print(f'=== 2-Year Analyst Forecast Model: {{COMPANY_NAME}} ({{TICKER}}) [{{SECTOR.upper()}}] ===')\n"
        f"    print('To run full valuation, populate baseline metrics from documents/analysis.sqlite.')\n\n"
        f"if __name__ == '__main__':\n"
        f"    main()\n",
        encoding="utf-8",
    )

    # 8. companies/<SECTOR>/<TICKER>/models/<ticker>_sandbox.ipynb
    sandbox_nb = models_dir / f"{ticker.lower()}_sandbox.ipynb"
    generate_company_notebook(ticker, company_name, sector, sandbox_nb)

    print(f"[+] Initialized company hub for {company_name} ({ticker}) under [{sector.upper()}] at:")
    print(f"    {company_dir}")
    print(f"\nNext Steps:")
    print(f"  1. Copy company PDF to: companies/{sector}/{ticker}/sources/")
    print(f"  2. Open PDF in capture app: Run Capture.cmd")
    print(f"  3. Open sandbox notebook: companies/{sector}/{ticker}/models/{ticker.lower()}_sandbox.ipynb")
    print(f"  4. Run valuation model: python -m companies.{sector}.{ticker}.models.run")

    return company_dir


def generate_company_notebook(ticker: str, company_name: str, sector: str, output_path: Path) -> Path:
    """Generates an interactive Jupyter notebook sandbox for the company."""
    ticker_upper = ticker.upper()

    if sector == "retail":
        macro_text = (
            "1. **Tweak Operating Assumptions**: Merchandise sales growth, gross profit margin %, debtor costs %.\n"
            "2. **Credit Book Health**: Impairment allowance coverage, collection rate %, satisfactory-paid customer %.\n"
            "3. **Store Footprint Dynamics**: Store count expansion, trading density (revenue/m²).\n"
            "4. **Evaluate Multiples**: P/E, EV/EBITDA, dividend yield, and JSE target price upside.\n"
        )
        macro_code = (
            "# ==============================================================================\n"
            "# [CONTROLS] INTERACTIVE ANALYST RETAIL & CREDIT ASSUMPTIONS\n"
            "# ==============================================================================\n\n"
            "MERCHANDISE_GROWTH_PCT = 0.075    # Projected merchandise sales growth\n"
            "GROSS_PROFIT_MARGIN_PCT = 0.437   # Gross profit margin\n"
            "DEBTOR_COSTS_PCT_DEBTORS = 0.143  # Debtor costs as % of gross carrying debtors\n"
            "STORE_EXPANSION_NET = 40          # Net store openings per year\n"
            "TARGET_PE_MULTIPLE = 10.0         # Target forward P/E multiple\n\n"
            "print('[+] Retail analyst assumptions set:')\n"
            "print(f'    * Merch Sales Growth: {MERCHANDISE_GROWTH_PCT*100:.1f}% | Gross Margin: {GROSS_PROFIT_MARGIN_PCT*100:.1f}%')\n"
            "print(f'    * Debtor Costs / Debtors: {DEBTOR_COSTS_PCT_DEBTORS*100:.1f}% | Net Stores Planned: {STORE_EXPANSION_NET}')\n"
        )
    elif sector == "reit":
        macro_text = (
            "1. **Tweak Property Assumptions**: Contractual rental escalations, like-for-like NPI growth, vacancy rates.\n"
            "2. **Balance Sheet & Cost of Debt**: Loan-to-Value (LTV) ratio, hedging percentage, weighted average cost of debt.\n"
            "3. **Distributable Income & Payout**: Distributable earnings per share (DIPS), payout ratio on distributable income.\n"
            "4. **Valuation Multiples**: Exit capitalization rate (cap rate), SOTP NAV per share, forward dividend yield.\n"
        )
        macro_code = (
            "# ==============================================================================\n"
            "# [CONTROLS] INTERACTIVE ANALYST REIT & PROPERTY ASSUMPTIONS\n"
            "# ==============================================================================\n\n"
            "CONTRACTUAL_ESCALATION_PCT = 0.065   # Average contractual lease escalation (%)\n"
            "PORTFOLIO_VACANCY_PCT = 0.055        # Portfolio-wide vacancy rate (%)\n"
            "EXIT_CAP_RATE_PCT = 0.0875          # Weighted exit capitalization rate\n"
            "TARGET_LTV_PCT = 0.380              # Target Look-through Loan-to-Value (LTV)\n"
            "DISTRIBUTION_PAYOUT_PCT = 0.900     # Payout ratio on Distributable Income\n"
            "TARGET_DIVIDEND_YIELD_PCT = 0.095   # Target forward distribution yield\n\n"
            "print('[+] REIT analyst assumptions set:')\n"
            "print(f'    * Escalation: {CONTRACTUAL_ESCALATION_PCT*100:.1f}% | Vacancy: {PORTFOLIO_VACANCY_PCT*100:.1f}%')\n"
            "print(f'    * Exit Cap Rate: {EXIT_CAP_RATE_PCT*100:.2f}% | Target LTV: {TARGET_LTV_PCT*100:.1f}% | Payout: {DISTRIBUTION_PAYOUT_PCT*100:.1f}%')\n"
        )
    elif sector == "construction":
        macro_text = (
            "1. **Tweak Operating & Backlog Assumptions**: Order book replenishment, book-to-bill ratio, revenue burn rate.\n"
            "2. **Contract Margin & Cost Escalation**: Operating EBIT margin, materials cost pass-through (CPAP formula), diesel/steel inflation.\n"
            "3. **Working Capital & Cash Flow**: Contract assets / WIP days, retention receivables release, operating cash conversion %.\n"
            "4. **Valuation Multiples**: EV/EBITDA, P/E multiple, dividend yield, and JSE equity target price upside.\n"
        )
        macro_code = (
            "# ==============================================================================\n"
            "# [CONTROLS] INTERACTIVE ANALYST CONSTRUCTION & MATERIALS ASSUMPTIONS\n"
            "# ==============================================================================\n\n"
            "BOOK_TO_BILL_RATIO = 1.15         # Target book-to-bill ratio (>1.0x indicates backlog growth)\n"
            "OPERATING_MARGIN_PCT = 0.055      # Target consolidated operating margin (%)\n"
            "MATERIALS_INFLATION_PCT = 0.060   # Annual building materials input inflation (%)\n"
            "CASH_CONVERSION_PCT = 0.85        # Operating cash conversion (% of EBITDA)\n"
            "TARGET_PE_MULTIPLE = 9.0          # Target forward P/E multiple\n\n"
            "print('[+] Construction & Materials analyst assumptions set:')\n"
            "print(f'    * Book-to-Bill: {BOOK_TO_BILL_RATIO:.2f}x | EBIT Margin: {OPERATING_MARGIN_PCT*100:.1f}%')\n"
            "print(f'    * Materials Inflation: {MATERIALS_INFLATION_PCT*100:.1f}% | Cash Conversion: {CASH_CONVERSION_PCT*100:.1f}% | Target P/E: {TARGET_PE_MULTIPLE:.1f}x')\n"
        )
    else:
        macro_text = (
            "1. **Tweak Macro Assumptions**: Realized commodity prices, FX rates, and inflation.\n"
            "2. **Inspect Real-Time Financials**: Revenue, EBITDA margins, Capex schedules, and FCF.\n"
            "3. **Evaluate Trading Multiples**: EV/EBITDA, P/E, FCF yield, and target price upside.\n"
            "4. **Run Sensitivity Grids**: 2D heatmaps across commodity price x FX rates.\n"
        )
        macro_code = (
            "# ==============================================================================\n"
            "# [CONTROLS] INTERACTIVE ANALYST MACRO ASSUMPTIONS\n"
            "# ==============================================================================\n\n"
            "FY27_PRICE = 5050.0  # FY27 commodity price target\n"
            "FY28_PRICE = 5750.0  # FY28 commodity price target\n"
            "USD_ZAR = 16.50      # Spot exchange rate\n"
            "TARGET_EV_EBITDA = 3.5\n\n"
            "print('[+] Macro inputs set:')\n"
            "print(f'    * FY27 Price: ${FY27_PRICE:,.0f} | FY28 Price: ${FY28_PRICE:,.0f}')\n"
            "print(f'    * USD/ZAR: {USD_ZAR} | Target Multiple: {TARGET_EV_EBITDA}x')\n"
        )

    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"# {company_name} ({ticker_upper}) -- 2-Year Analyst Forecast Sandbox\n",
                f"**Sector**: {sector.capitalize()} | **Ticker**: {ticker_upper}\n\n",
                "Welcome to your interactive valuation sandbox! Use this notebook to:\n",
                macro_text,
                f"> **Thin Notebook Architecture**: Business logic lives under `companies.{sector}.{ticker_upper}.models`.\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Enable inline plotting for VS Code\n",
                "%matplotlib inline\n\n",
                "import sys\n",
                "from pathlib import Path\n\n",
                "NOTEBOOK_DIR = Path.cwd()\n",
                "PROJECT_ROOT = next((p for p in NOTEBOOK_DIR.parents if (p / 'section_capture').exists()), NOTEBOOK_DIR)\n",
                "if str(PROJECT_ROOT) not in sys.path:\n",
                "    sys.path.insert(0, str(PROJECT_ROOT))\n\n",
                "try:\n",
                "    from IPython.display import display\n",
                "except ImportError:\n",
                "    display = print\n\n",
                "import pandas as pd\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n\n",
                f"from companies.{sector}.{ticker_upper}.models.config import TICKER, COMPANY_NAME, SECTOR\n\n",
                "print(f'[+] Initialized sandbox environment for {COMPANY_NAME} ({TICKER}) [{SECTOR.upper()}]')\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                macro_code,
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# ==============================================================================\n",
                "# FINANCIAL SUMMARY & MULTIPLES PLACEHOLDER\n",
                "# Populated once baseline numbers are extracted into models/data_loader.py\n",
                "# ==============================================================================\n\n",
                "print('[+] Ready for baseline data loading and 2-year model execution.')\n",
            ],
        },
    ]

    notebook_data = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (.venv)",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.12.14",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 4,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notebook_data, f, indent=1)

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Create a new company hub in the Analyst Workbench.")
    parser.add_argument("ticker", help="Company ticker symbol (e.g. HAR, LEW, SBK, MTN)")
    parser.add_argument("--sector", choices=SUPPORTED_SECTORS, default="mining", help="Company sector (mining, retail, reit, it, finance, telcos)")
    parser.add_argument("--name", help="Full company name", default=None)

    args = parser.parse_args()
    create_company(args.ticker, args.name, sector=args.sector)


if __name__ == "__main__":
    main()
