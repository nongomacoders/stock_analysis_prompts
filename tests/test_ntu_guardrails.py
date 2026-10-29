"""The approved NTU lessons reach the right sector and analysis stages."""

import pytest

from workflow.export_stage1 import build_stage1_prompt_content
from workflow.generate_sens_update import build_sens_update_prompt_content
from workflow.generate_stage2 import build_stage2_prompt_content


@pytest.mark.parametrize("sector,ticker", [("consumer_lending", "NTU"), ("retail", "SPP")])
@pytest.mark.parametrize("stage", ["stage1", "stage2", "sens"])
def test_reviewed_guardrails_reach_prompts_with_correct_sector_scope(tmp_path, sector, ticker, stage):
    common = dict(company_title="Test Company", ticker=ticker, detected_sector=sector, db_path=tmp_path)
    if stage == "stage1":
        prompt = build_stage1_prompt_content(sections=[], filename="interim.pdf", **common)
    elif stage == "stage2":
        prompt = build_stage2_prompt_content(stage1_content="Working paper", reference_price_zar=0.89, **common)
    else:
        prompt = build_sens_update_prompt_content(
            baseline_valuation_report="Baseline valuation",
            reference_price_zar=0.89,
            stage1_audit_report="Working paper",
            **common,
        )

    for code in (
        "ALL-CASH-ROLLFORWARD-CONSISTENCY",
        "ALL-SENSITIVITY-REPRODUCIBILITY",
        "ALL-EQUITY-NAV-VS-CONTRIBUTED-CAPITAL",
    ):
        assert code in prompt
    assert ("CONSUMER-LENDING-POCI-GAIN-VS-ECL-RESERVE" in prompt) == (sector == "consumer_lending")