"""Tests for centralized sector registry and sector onboarding architecture."""
from __future__ import annotations

import pytest
from companies.sectors import (
    DEFAULT_SECTOR,
    SECTOR_REGISTRY,
    get_all_sector_codes,
    get_all_sectors,
    get_sector_badge_style,
    get_sector_config,
    get_sector_display,
    get_sector_short_label,
    resolve_sector_alias,
)


def test_sector_registry_defaults():
    codes = get_all_sector_codes()
    for expected in ["mining", "retail", "reit", "it", "finance", "telcos"]:
        assert expected in codes

    it_cfg = get_sector_config("it")
    assert it_cfg.short_label == "IT"
    assert "Technology" in it_cfg.display_name
    assert "Forensic Technology" in it_cfg.stage1_persona
    assert "Head of Technology" in it_cfg.stage2_persona
    assert "Head of Technology" in it_cfg.sens_persona

    reit_cfg = get_sector_config("reit")
    assert reit_cfg.short_label == "REIT"
    assert "Real Estate" in reit_cfg.display_name

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
    assert "Retail" in get_sector_display("retail")
