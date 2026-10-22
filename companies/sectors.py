"""Central registry of supported sectors, display labels, styling, and forensic personas."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class SectorConfig:
    """Configuration and metadata for an equity research sector."""
    code: str
    display_name: str
    short_label: str
    badge_bg: str
    badge_fg: str
    badge_border: str
    stage1_persona: str
    stage2_persona: str
    sens_persona: str
    aliases: tuple[str, ...] = ()


SECTOR_REGISTRY: dict[str, SectorConfig] = {
    "mining": SectorConfig(
        code="mining",
        display_name="Mining & Natural Resources",
        short_label="Mining",
        badge_bg="#fef3c7",
        badge_fg="#92400e",
        badge_border="#fde68a",
        stage1_persona="Managing Director and Senior Forensic Mining Accounting Auditor",
        stage2_persona="Managing Director & Head of Mining Equity Research",
        sens_persona="Managing Director & Head of Mining Equity Research",
        aliases=("resources", "gold", "minerals", "metals"),
    ),
    "retail": SectorConfig(
        code="retail",
        display_name="Retail & Consumer Goods",
        short_label="Retail",
        badge_bg="#e0f2fe",
        badge_fg="#0369a1",
        badge_border="#bae6fd",
        stage1_persona="Managing Director and Senior Forensic Retail & Consumer Credit Accounting Auditor",
        stage2_persona="Managing Director & Head of Retail & Consumer Equity Research",
        sens_persona="Managing Director & Head of Retail & Consumer Equity Research",
        aliases=("consumer", "credit_retail", "merchandise"),
    ),
    "reit": SectorConfig(
        code="reit",
        display_name="Real Estate & Listed Property (REITs)",
        short_label="REIT",
        badge_bg="#ecfdf5",
        badge_fg="#065f46",
        badge_border="#a7f3d0",
        stage1_persona="Managing Director and Senior Forensic Listed Property & REIT Financial Auditor",
        stage2_persona="Managing Director & Head of Listed Property & REIT Equity Research",
        sens_persona="Managing Director & Head of Listed Property & REIT Equity Research",
        aliases=("property", "real_estate", "realestate", "reits"),
    ),
    "it": SectorConfig(
        code="it",
        display_name="Technology / IT Services",
        short_label="IT",
        badge_bg="#e0e7ff",
        badge_fg="#3730a3",
        badge_border="#c7d2fe",
        stage1_persona="Managing Director and Senior Forensic Technology & IT Services Financial Auditor",
        stage2_persona="Managing Director & Head of Technology & IT Services Equity Research",
        sens_persona="Managing Director & Head of Technology & IT Services Equity Research",
        aliases=("tech", "technology", "information_technology"),
    ),
    "finance": SectorConfig(
        code="finance",
        display_name="Banking & Financial Services",
        short_label="Finance",
        badge_bg="#f3e8ff",
        badge_fg="#6b21a8",
        badge_border="#e9d5ff",
        stage1_persona="Managing Director and Senior Forensic Banking & Financial Institutions Auditor",
        stage2_persona="Managing Director & Head of Banking & Financial Institutions Equity Research",
        sens_persona="Managing Director & Head of Banking & Financial Institutions Equity Research",
        aliases=("bank", "banking", "financial_services"),
    ),
    "telcos": SectorConfig(
        code="telcos",
        display_name="Telecommunications & Media",
        short_label="Telcos",
        badge_bg="#ffedd5",
        badge_fg="#9a3412",
        badge_border="#fed7aa",
        stage1_persona="Managing Director and Senior Forensic Telecommunications Financial Auditor",
        stage2_persona="Managing Director & Head of Telecommunications Equity Research",
        sens_persona="Managing Director & Head of Telecommunications Equity Research",
        aliases=("telecom", "telecoms", "telecommunications"),
    ),
    "construction": SectorConfig(
        code="construction",
        display_name="Construction & Materials",
        short_label="Construction",
        badge_bg="#ecfeff",
        badge_fg="#155e75",
        badge_border="#a5f3fc",
        stage1_persona="Managing Director and Senior Forensic Construction & Infrastructure Financial Auditor",
        stage2_persona="Managing Director & Head of Construction & Materials Equity Research",
        sens_persona="Managing Director & Head of Construction & Materials Equity Research",
        aliases=('materials', 'building', 'cement', 'infrastructure', 'engineering'),
    ),
}

DEFAULT_SECTOR = "mining"


def get_sector_config(code: str | None) -> SectorConfig:
    """Returns the SectorConfig for the given sector code, or default if not found."""
    if not code:
        return SECTOR_REGISTRY[DEFAULT_SECTOR]
    normalized = code.lower().strip()
    if normalized in SECTOR_REGISTRY:
        return SECTOR_REGISTRY[normalized]
    alias_match = resolve_sector_alias(normalized)
    return SECTOR_REGISTRY.get(alias_match or DEFAULT_SECTOR, SECTOR_REGISTRY[DEFAULT_SECTOR])


def get_all_sector_codes() -> list[str]:
    """Returns a list of all canonical sector codes in registry order."""
    return list(SECTOR_REGISTRY.keys())


def get_all_sectors() -> list[SectorConfig]:
    """Returns a list of all SectorConfig items in registry order."""
    return list(SECTOR_REGISTRY.values())


def get_sector_display(code: str | None) -> str:
    """Returns the full human-readable display name for the sector."""
    return get_sector_config(code).display_name


def get_sector_short_label(code: str | None) -> str:
    """Returns the short uppercase/title label for the sector (e.g. 'REIT', 'IT', 'Mining')."""
    return get_sector_config(code).short_label


def get_sector_badge_style(code: str | None) -> str:
    """Returns the CSS stylesheet string for rendering the sector badge."""
    cfg = get_sector_config(code)
    return (
        f"padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; "
        f"background-color: {cfg.badge_bg}; color: {cfg.badge_fg}; border: 1px solid {cfg.badge_border};"
    )


def resolve_sector_alias(candidate: str | None) -> str | None:
    """Resolves a raw sector candidate or path slug to canonical sector code."""
    if not candidate:
        return None
    c = candidate.lower().strip()
    if c in SECTOR_REGISTRY:
        return c
    for code, cfg in SECTOR_REGISTRY.items():
        if c in cfg.aliases:
            return code
    return None
