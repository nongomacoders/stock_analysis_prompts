#!/usr/bin/env python3
"""Daily Analyst Workbench Scaffolding Tool.

Initializes a new company hub under companies/<TICKER>/ with standardized
directories for sources, valuation models, deep research, and analyst briefs.

Usage:
    python new_company.py HAR --name "Harmony Gold Mining Company Ltd"
    python new_company.py GFI --name "Gold Fields Ltd"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
COMPANIES_DIR = ROOT / "companies"


def create_company(ticker: str, name: str | None = None) -> Path:
    ticker = ticker.upper().strip()
    company_name = name or ticker
    company_dir = COMPANIES_DIR / ticker

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

    # 1. companies/<TICKER>/__init__.py
    (company_dir / "__init__.py").write_text(
        f'"""{company_name} (Ticker: {ticker})."""\n',
        encoding="utf-8",
    )

    # 2. companies/<TICKER>/sources/README.md
    (sources_dir / "README.md").write_text(
        f"# Source Documents: {company_name} ({ticker})\n\n"
        f"Drop original company PDF reports, presentations, and SENS/ASX announcements here.\n"
        f"Then open the PDF in the capture app (`Run Capture.cmd` or `python app.py`) to scan sections.\n",
        encoding="utf-8",
    )

    # 3. companies/<TICKER>/research/README.md
    (research_dir / "README.md").write_text(
        f"# Deep Research: {company_name} ({ticker})\n\n"
        f"Save targeted Gemini Argon deep research outputs (PDFs, text reports) here.\n"
        f"Recommended naming: `01_topic_description.pdf`, `02_topic_description.txt`.\n",
        encoding="utf-8",
    )

    # 4. companies/<TICKER>/briefs/README.md
    (briefs_dir / "README.md").write_text(
        f"# Analyst Briefs: {company_name} ({ticker})\n\n"
        f"Generated 2-year forecast reports, reading briefs, and investment memos are saved here.\n",
        encoding="utf-8",
    )

    # 5. companies/<TICKER>/models/config.py
    (models_dir / "config.py").write_text(
        f'"""Configuration & baseline parameters for {company_name} ({ticker})."""\n\n'
        f"TICKER = {ticker!r}\n"
        f"COMPANY_NAME = {company_name!r}\n"
        f"REPORTING_CURRENCY = 'USD'\n"
        f"LOCAL_CURRENCY = 'ZAR'\n"
        f"SHARES_IN_ISSUE_M = 100.0\n",
        encoding="utf-8",
    )

    # 6. companies/<TICKER>/models/__init__.py
    (models_dir / "__init__.py").write_text(
        f'"""Valuation & forecast models for {company_name} ({ticker})."""\n',
        encoding="utf-8",
    )

    # 7. companies/<TICKER>/models/run.py
    (models_dir / "run.py").write_text(
        f'"""CLI Runner for {company_name} ({ticker}) 2-Year Forecast."""\n\n'
        f"from .config import TICKER, COMPANY_NAME\n\n"
        f"def main():\n"
        f"    print(f'=== 2-Year Analyst Forecast Model: {{COMPANY_NAME}} ({{TICKER}}) ===')\n"
        f"    print('To run full valuation, populate baseline metrics from documents/analysis.sqlite.')\n\n"
        f"if __name__ == '__main__':\n"
        f"    main()\n",
        encoding="utf-8",
    )

    # 8. companies/<TICKER>/models/<ticker>_sandbox.ipynb
    sandbox_nb = models_dir / f"{ticker.lower()}_sandbox.ipynb"
    generate_company_notebook(ticker, company_name, sandbox_nb)

    print(f"[+] Initialized company hub for {company_name} ({ticker}) at:")
    print(f"    {company_dir}")
    print(f"\nNext Steps:")
    print(f"  1. Copy company PDF to: companies/{ticker}/sources/")
    print(f"  2. Open PDF in capture app: Run Capture.cmd")
    print(f"  3. Open sandbox notebook: companies/{ticker}/models/{ticker.lower()}_sandbox.ipynb")
    print(f"  4. Run valuation model: python -m companies.{ticker}.models.run")

    return company_dir


def generate_company_notebook(ticker: str, company_name: str, output_path: Path) -> Path:
    """Generates an interactive Jupyter notebook sandbox for the company."""
    ticker_upper = ticker.upper()

    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"# {company_name} ({ticker_upper}) -- 2-Year Analyst Forecast Sandbox\n",
                f"**Forecast Horizon**: FY27E & FY28E | **Ticker**: {ticker_upper}\n\n",
                "Welcome to your interactive valuation sandbox! Use this notebook to:\n",
                "1. **Tweak Macro Assumptions**: Realized commodity prices, FX rates, and inflation.\n",
                "2. **Inspect Real-Time Financials**: Revenue, EBITDA margins, Capex schedules, and FCF.\n",
                "3. **Evaluate Trading Multiples**: EV/EBITDA, P/E, FCF yield, and target price upside.\n",
                "4. **Run Sensitivity Grids**: 2D heatmaps across commodity price x FX rates.\n\n",
                f"> **Thin Notebook Architecture**: Business logic lives under `companies.{ticker_upper}.models`.\n",
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
                "PROJECT_ROOT = NOTEBOOK_DIR.parents[2] if 'companies' in NOTEBOOK_DIR.parts else NOTEBOOK_DIR\n",
                "if str(PROJECT_ROOT) not in sys.path:\n",
                "    sys.path.insert(0, str(PROJECT_ROOT))\n\n",
                "try:\n",
                "    from IPython.display import display\n",
                "except ImportError:\n",
                "    display = print\n\n",
                "import pandas as pd\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n\n",
                f"from companies.{ticker_upper}.models.config import TICKER, COMPANY_NAME\n\n",
                "print(f'[+] Initialized sandbox environment for {COMPANY_NAME} ({TICKER})')\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# ==============================================================================\n",
                "# [CONTROLS] INTERACTIVE ANALYST MACRO ASSUMPTIONS\n",
                "# ==============================================================================\n\n",
                "FY27_PRICE = 5050.0  # FY27 commodity price target\n",
                "FY28_PRICE = 5750.0  # FY28 commodity price target\n",
                "USD_ZAR = 16.50      # Spot exchange rate\n",
                "TARGET_EV_EBITDA = 3.5\n\n",
                "print('[+] Macro inputs set:')\n",
                "print(f'    * FY27 Price: ${FY27_PRICE:,.0f} | FY28 Price: ${FY28_PRICE:,.0f}')\n",
                "print(f'    * USD/ZAR: {USD_ZAR} | Target Multiple: {TARGET_EV_EBITDA}x')\n",
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
    parser.add_argument("ticker", help="Company ticker symbol (e.g. HAR, GFI, AGL)")
    parser.add_argument("--name", help="Full company name", default=None)

    args = parser.parse_args()
    create_company(args.ticker, args.name)


if __name__ == "__main__":
    main()
