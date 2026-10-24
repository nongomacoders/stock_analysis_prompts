"""Unit and GUI tests for ticker examination and Stage 1 / Stage 2 prompt appropriateness."""
from __future__ import annotations

import json
from pathlib import Path
import pytest
from PySide6.QtWidgets import QApplication

from section_capture.new_company_dialog import NewCompanyDialog
from section_capture.ticker_lookup import (
    build_ticker_examination_prompt,
    check_prompt_appropriateness,
    examine_ticker_locally,
    parse_examination_response,
)


def test_examine_ticker_locally_existing_hub():
    """Verify local hub detection for existing company on disk."""
    res_lew = examine_ticker_locally("LEW")
    assert res_lew is not None
    assert res_lew["ticker"] == "LEW"
    assert res_lew["sector_code"] == "retail"
    assert "Lewis" in res_lew["company_name"]
    assert res_lew["hub_exists"] is True

    res_ntu = examine_ticker_locally("NTU")
    assert res_ntu is not None
    assert res_ntu["ticker"] == "NTU"
    assert res_ntu["sector_code"] == "consumer_lending"
    assert "Nutun" in res_ntu["company_name"]
    assert res_ntu["hub_exists"] is True


def test_examine_ticker_locally_unknown():
    """Verify None returned for non-existent ticker."""
    res = examine_ticker_locally("XYZNONEXISTENT999")
    assert res is None


def test_check_prompt_appropriateness_registered_sectors():
    """Verify prompt readiness and forensic model support across registered sectors."""
    for sec in ["consumer_lending", "retail", "mining", "finance", "telcos", "it", "reit", "construction"]:
        info = check_prompt_appropriateness(sec)
        assert info["is_registered_sector"] is True
        assert info["stage1_supported"] is True
        assert info["stage2_supported"] is True
        assert info["has_orientation_prompt"] is True
        assert info["has_reading_prompt"] is True
        assert info["status"] == "Appropriate & Ready"
        assert len(info["display_name"]) > 0


def test_check_prompt_appropriateness_unregistered_sector():
    """Verify graceful handling and guidance for un-scaffolded sectors."""
    info = check_prompt_appropriateness("healthcare")
    assert info["is_registered_sector"] is False
    assert info["status"] == "New Sector Required"
    assert "new_sector.py" in info["guidance"]


def test_build_and_parse_ticker_examination_prompt():
    """Verify prompt formatting and robust JSON parsing."""
    prompt = build_ticker_examination_prompt("SBK")
    assert "SBK" in prompt
    assert "Stage 1" in prompt
    assert "Stage 2" in prompt
    assert "registered_sectors" not in prompt  # formatted into prompt

    mock_llm_json = """```json
{
  "ticker": "SBK",
  "company_name": "Standard Bank Group Limited",
  "jse_sector": "Banks",
  "icb_code": "301010",
  "matched_sector_code": "finance",
  "business_summary": "Full-service African financial services group.",
  "stage1_appropriateness": {
    "status": "Appropriate",
    "focus_areas": "NIM, credit loss ratio, CET1 capital adequacy, and IFRS 9 Stage 3 coverage.",
    "caveats": "African regional currency exposure."
  },
  "stage2_appropriateness": {
    "status": "Appropriate",
    "recommended_valuation_model": "Dividend Discount Model & P/NAV",
    "key_drivers": "Net interest margin, credit impairment trajectory, and ROE."
  }
}
```"""
    parsed = parse_examination_response(mock_llm_json)
    assert parsed["ticker"] == "SBK"
    assert parsed["company_name"] == "Standard Bank Group Limited"
    assert parsed["matched_sector_code"] == "finance"
    assert parsed["stage1_appropriateness"]["status"] == "Appropriate"
    assert parsed["stage2_appropriateness"]["recommended_valuation_model"] == "Dividend Discount Model & P/NAV"


def test_new_company_dialog_examine_local_ticker(qapp):
    """Test that clicking Examine Ticker on a local company populates details and shows assessment card."""
    dlg = NewCompanyDialog()
    try:
        assert hasattr(dlg, "examine_btn")
        assert hasattr(dlg, "assessment_frame")
        assert dlg.assessment_frame.isHidden()

        dlg.ticker_edit.setText("LEW")
        dlg.examine_btn.click()

        assert not dlg.assessment_frame.isHidden()
        assert "Lewis Group Limited" in dlg.name_edit.text()
        assert dlg.sector_combo.currentData() == "retail"
        assert "Stage 1 Forensic Audit" in dlg.assessment_details.text()
        assert "Stage 2 Valuation Note" in dlg.assessment_details.text()
    finally:
        dlg.deleteLater()


def test_new_company_dialog_examine_callback_simulation(qapp):
    """Test that examination callback updates the UI with Stage 1 & 2 appropriateness findings."""
    dlg = NewCompanyDialog()
    try:
        mock_data = {
            "ticker": "CPI",
            "company_name": "Capitec Bank Holdings Limited",
            "jse_sector": "Consumer Lending",
            "icb_code": "30201020",
            "matched_sector_code": "consumer_lending",
            "business_summary": "South African retail bank and digital consumer credit provider.",
            "stage1_appropriateness": {
                "status": "Appropriate",
                "focus_areas": "IFRS 9 ECL Stage 1/2/3 migration, retail credit loss ratio, and non-interest fee growth.",
                "caveats": "Scrutinize transaction fee vs lending income split.",
            },
            "stage2_appropriateness": {
                "status": "Appropriate",
                "recommended_valuation_model": "P/NAV & 2-Stage DDM",
                "key_drivers": "Active client growth, credit loss ratio, and cost-to-income ratio.",
            },
        }

        dlg.ticker_edit.setText("CPI")
        dlg._on_examination_finished(mock_data)

        assert dlg.name_edit.text() == "Capitec Bank Holdings Limited"
        assert dlg.sector_combo.currentData() == "consumer_lending"
        assert not dlg.assessment_frame.isHidden()
        assert "Consumer Lending" in dlg.assessment_header.text()
        assert "Stage 1 Forensic Audit (Appropriate)" in dlg.assessment_details.text()
        assert "Stage 2 Valuation Note (Appropriate)" in dlg.assessment_details.text()
        assert "P/NAV & 2-Stage DDM" in dlg.assessment_details.text()
    finally:
        dlg.deleteLater()
