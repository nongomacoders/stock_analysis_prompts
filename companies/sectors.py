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
    jse_code: str = ""
    icb_code: str = ""
    jse_sector_name: str = ""


# Per-ticker FTSE/JSE ICB subsector overrides when a sector folder houses multiple JSE subsectors
# Maps TICKER -> (jse_code, icb_code, jse_sector_name)
TICKER_JSE_OVERRIDES: dict[str, tuple[str, str, str]] = {
    "ORN": ("JS5512", "551020", "Industrial Metals and Mining"),
    "AFT": ("JS5512", "551020", "Industrial Metals and Mining"),
}


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
        aliases=("resources", "gold", "minerals", "metals", "js5513", "js5512", "551030", "551020", "precious metals", "industrial metals", "basic materials"),
        jse_code="JS5513",
        icb_code="551030",
        jse_sector_name="Precious Metals and Mining",
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
        aliases=("consumer", "credit_retail", "merchandise", "retailers", "js4041", "404010", "consumer discretionary"),
        jse_code="JS4041",
        icb_code="404010",
        jse_sector_name="Retailers",
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
        aliases=("property", "real_estate", "realestate", "reits", "js3512", "351020", "real estate investment trusts"),
        jse_code="JS3512",
        icb_code="351020",
        jse_sector_name="Real Estate Investment Trusts",
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
        aliases=("tech", "technology", "information_technology", "js1011", "101010", "software and computer services", "software"),
        jse_code="JS1011",
        icb_code="101010",
        jse_sector_name="Software and Computer Services",
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
        aliases=("bank", "banking", "financial_services", "banks", "js3011", "301010", "financials"),
        jse_code="JS3011",
        icb_code="301010",
        jse_sector_name="Banks & Financial Services",
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
        aliases=("telecom", "telecoms", "telecommunications", "js1512", "151020", "telecommunications service providers"),
        jse_code="JS1512",
        icb_code="151020",
        jse_sector_name="Telecommunications Service Providers",
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
        aliases=("materials", "building", "cement", "infrastructure", "engineering", "js5011", "501010", "construction and materials", "js3511", "351010"),
        jse_code="JS5011",
        icb_code="501010",
        jse_sector_name="Construction and Materials",
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


def get_jse_sector_code(code: str | None, ticker: str | None = None) -> str:
    """Returns the official FTSE/JSE index code (e.g. 'JS5513', 'JS4041', 'JS5011')."""
    if ticker:
        t_up = ticker.strip().upper()
        if t_up in TICKER_JSE_OVERRIDES:
            return TICKER_JSE_OVERRIDES[t_up][0]
    cfg = get_sector_config(code)
    return cfg.jse_code or cfg.code.upper()


def get_icb_code(code: str | None, ticker: str | None = None) -> str:
    """Returns the official ICB numeric sector code (e.g. '551030', '404010', '501010')."""
    if ticker:
        t_up = ticker.strip().upper()
        if t_up in TICKER_JSE_OVERRIDES:
            return TICKER_JSE_OVERRIDES[t_up][1]
    cfg = get_sector_config(code)
    return cfg.icb_code


def get_jse_sector_name(code: str | None, ticker: str | None = None) -> str:
    """Returns the official FTSE/JSE ICB sector name (e.g. 'Precious Metals and Mining', 'Retailers')."""
    if ticker:
        t_up = ticker.strip().upper()
        if t_up in TICKER_JSE_OVERRIDES:
            return TICKER_JSE_OVERRIDES[t_up][2]
    cfg = get_sector_config(code)
    return cfg.jse_sector_name or cfg.display_name


def get_jse_sector_label(code: str | None, ticker: str | None = None) -> str:
    """Returns a combined badge/label with short name and JSE code, e.g. 'Mining (JS5513)'."""
    cfg = get_sector_config(code)
    jse_c = get_jse_sector_code(code, ticker=ticker)
    return f"{cfg.short_label} ({jse_c})" if jse_c else cfg.short_label


def get_sector_badge_style(code: str | None) -> str:
    """Returns the CSS stylesheet string for rendering the sector badge."""
    cfg = get_sector_config(code)
    return (
        f"padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; "
        f"background-color: {cfg.badge_bg}; color: {cfg.badge_fg}; border: 1px solid {cfg.badge_border};"
    )


def resolve_sector_alias(candidate: str | None) -> str | None:
    """Resolves a raw sector candidate, JSE code, ICB code, or path slug to canonical sector code."""
    if not candidate:
        return None
    c = candidate.lower().strip()
    if c in SECTOR_REGISTRY:
        return c
    for code, cfg in SECTOR_REGISTRY.items():
        if c == cfg.jse_code.lower() or c == cfg.icb_code.lower() or c == cfg.jse_sector_name.lower():
            return code
        if c in cfg.aliases:
            return code
    return None


def normalize_sector_code(text: str | None) -> str:
    """Extracts and normalizes sector code from raw text, JSE codes, display names, or table cell contents."""
    if not text:
        return ""
    t = text.lower().strip()
    direct = resolve_sector_alias(t)
    if direct:
        return direct
    for code, cfg in SECTOR_REGISTRY.items():
        if (
            code in t
            or cfg.short_label.lower() in t
            or cfg.display_name.lower() in t
            or (cfg.jse_code and cfg.jse_code.lower() in t)
            or (cfg.icb_code and cfg.icb_code.lower() in t)
            or (cfg.jse_sector_name and cfg.jse_sector_name.lower() in t)
        ):
            return code
        for a in cfg.aliases:
            if a in t:
                return code
    return ""
