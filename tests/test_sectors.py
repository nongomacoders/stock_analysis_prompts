"""Tests for centralized sector registry and sector onboarding architecture."""
from __future__ import annotations

import pytest
from companies.sectors import (
    DEFAULT_SECTOR,
    SECTOR_REGISTRY,
    get_all_sector_codes,
    get_all_sectors,
    get_icb_code,
    get_jse_sector_code,
    get_jse_sector_label,
    get_jse_sector_name,
    get_sector_badge_style,
    get_sector_config,
    get_sector_display,
    get_sector_short_label,
    normalize_sector_code,
    resolve_sector_alias,
)


def test_sector_registry_defaults():
    codes = get_all_sector_codes()
    for expected in ["mining", "retail", "reit", "it", "construction", "finance", "telcos"]:
        assert expected in codes

    it_cfg = get_sector_config("it")
    assert it_cfg.short_label == "IT"
    assert "Technology" in it_cfg.display_name
    assert "Forensic Technology" in it_cfg.stage1_persona
    assert "Head of Technology" in it_cfg.stage2_persona
    assert "Head of Technology" in it_cfg.sens_persona
    assert it_cfg.jse_code == "JS1011"
    assert it_cfg.icb_code == "101010"
    assert it_cfg.jse_sector_name == "Software and Computer Services"

    reit_cfg = get_sector_config("reit")
    assert reit_cfg.short_label == "REIT"
    assert "Real Estate" in reit_cfg.display_name
    assert reit_cfg.jse_code == "JS3512"
    assert reit_cfg.icb_code == "351020"

    const_cfg = get_sector_config("construction")
    assert const_cfg.jse_code == "JS5011"
    assert const_cfg.icb_code == "501010"
    assert const_cfg.jse_sector_name == "Construction and Materials"

    unknown = get_sector_config("unknown_sector_xyz")
    assert unknown.code == DEFAULT_SECTOR


def test_sector_alias_resolution():
    assert resolve_sector_alias("tech") == "it"
    assert resolve_sector_alias("technology") == "it"
    assert resolve_sector_alias("property") == "reit"
    assert resolve_sector_alias("real_estate") == "reit"
    assert resolve_sector_alias("gold") == "mining"
    assert resolve_sector_alias("telecom") == "telcos"
    assert resolve_sector_alias("banking") == "finance"
    assert resolve_sector_alias("materials") == "construction"
    assert resolve_sector_alias("building") == "construction"
    assert resolve_sector_alias("cement") == "construction"
    assert resolve_sector_alias("infrastructure") == "construction"
    assert resolve_sector_alias("JS5513") == "mining"
    assert resolve_sector_alias("JS4041") == "retail"
    assert resolve_sector_alias("JS3512") == "reit"
    assert resolve_sector_alias("JS1011") == "it"
    assert resolve_sector_alias("JS5011") == "construction"
    assert resolve_sector_alias("nonexistent") is None


def test_sector_badge_style():
    style = get_sector_badge_style("it")
    assert "background-color: #e0e7ff" in style
    assert "color: #3730a3" in style
    assert "border: 1px solid #c7d2fe" in style


def test_sector_labels():
    assert get_sector_short_label("it") == "IT"
    assert get_sector_short_label("reit") == "REIT"
    assert get_sector_short_label("mining") == "Mining"
    assert get_sector_short_label("construction") == "Construction" 
    assert "Retail" in get_sector_display("retail")


def test_normalize_sector_code():
    assert normalize_sector_code("Mining (Gold)") == "mining"
    assert normalize_sector_code("JSE Retail") == "retail"
    assert normalize_sector_code("REIT / Listed Property") == "reit"
    assert normalize_sector_code("Technology / IT Services") == "it"
    assert normalize_sector_code("Construction & Materials") == "construction"
    assert normalize_sector_code("mining") == "mining"
    assert normalize_sector_code("JS5011") == "construction"
    assert normalize_sector_code("JS4041") == "retail"


def test_jse_sector_helpers_and_ticker_overrides():
    # Construction default
    assert get_jse_sector_code("construction") == "JS5011"
    assert get_icb_code("construction") == "501010"
    assert get_jse_sector_name("construction") == "Construction and Materials"
    assert get_jse_sector_label("construction") == "Construction (JS5011)"

    # Mining default (Precious Metals e.g. PAN, HAR)
    assert get_jse_sector_code("mining") == "JS5513"
    assert get_jse_sector_code("mining", ticker="PAN") == "JS5513"
    assert get_jse_sector_name("mining", ticker="PAN") == "Precious Metals and Mining"
    assert get_jse_sector_label("mining", ticker="PAN") == "Mining (JS5513)"

    # Mining override for Base / Industrial Metals (ORN)
    assert get_jse_sector_code("mining", ticker="ORN") == "JS5512"
    assert get_icb_code("mining", ticker="ORN") == "551020"
    assert get_jse_sector_name("mining", ticker="ORN") == "Industrial Metals and Mining"
    assert get_jse_sector_label("mining", ticker="ORN") == "Mining (JS5512)"

    # Retail default
    assert get_jse_sector_code("retail", ticker="LEW") == "JS4041"
    assert get_jse_sector_name("retail", ticker="LEW") == "Retailers"
    assert get_jse_sector_label("retail", ticker="LEW") == "Retail (JS4041)"
