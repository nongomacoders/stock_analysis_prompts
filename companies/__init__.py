"""Companies package for multi-company stock analysis and financial models."""
from __future__ import annotations

import importlib
from pathlib import Path
import sys

PACKAGE_DIR = Path(__file__).resolve().parent
from companies.sectors import get_all_sector_codes, get_sector_config
SECTORS = get_all_sector_codes()


def find_company_dir(ticker: str, sector: str | None = None) -> tuple[str, Path] | None:
    """Finds the (sector, directory_path) for a given company ticker."""
    ticker_upper = ticker.upper()
    candidates = [ticker_upper]
    if ticker_upper == "IOCO":
        candidates.append("IOC")
    elif ticker_upper == "IOC":
        candidates.append("IOCO")

    if sector:
        for cand_t in candidates:
            target = PACKAGE_DIR / sector / cand_t
            if target.exists():
                return sector, target
    for sec in SECTORS:
        for cand_t in candidates:
            cand = PACKAGE_DIR / sec / cand_t
            if cand.exists():
                return sec, cand
    return None


def _register_legacy_aliases():
    """Exposes companies.<TICKER> as an alias for companies.<SECTOR>.<TICKER> for backward compatibility."""
    for sec in SECTORS:
        sec_dir = PACKAGE_DIR / sec
        if not sec_dir.exists():
            continue
        for comp_dir in sec_dir.iterdir():
            if comp_dir.is_dir() and not comp_dir.name.startswith((".", "_")):
                ticker = comp_dir.name
                alias_name = f"companies.{ticker}"
                target_name = f"companies.{sec}.{ticker}"
                if alias_name not in sys.modules:
                    try:
                        mod = importlib.import_module(target_name)
                        sys.modules[alias_name] = mod
                    except Exception:
                        pass


_register_legacy_aliases()
