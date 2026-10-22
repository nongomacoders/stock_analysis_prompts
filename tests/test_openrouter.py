"""Unit tests for the OpenRouter API integration."""

from __future__ import annotations

import io
import json
import urllib.error
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QCoreApplication

from section_capture.db import SavedSection, insert_section, save_section_llm_response
from section_capture.openrouter import (
    DEFAULT_MODEL,
    OpenRouterWorker,
    estimate_cost,
    fetch_generation_stats,
    get_openrouter_api_key,
    get_openrouter_model,
    query_openrouter,
)


def test_get_openrouter_model_default(monkeypatch):
    monkeypatch.delenv("OPENROUTER_MODEL", raising=False)
    assert get_openrouter_model() == "deepseek/deepseek-v4.1-flash-1017"


def test_get_openrouter_model_env_override(monkeypatch):
    monkeypatch.setenv("OPENROUTER_MODEL", "deepseek/deepseek-r1")
    assert get_openrouter_model() == "deepseek/deepseek-r1"


def test_get_openrouter_api_key_from_env(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key-12345")
    with patch("section_capture.openrouter.EXTERNAL_SECRETS_PATH") as mock_path:
        mock_path.exists.return_value = False
        assert get_openrouter_api_key() == "test-key-12345"


def test_query_openrouter_missing_key(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with patch("section_capture.openrouter.EXTERNAL_SECRETS_PATH") as mock_path:
        mock_path.exists.return_value = False
        with pytest.raises(RuntimeError, match="OpenRouter API key not found"):
            query_openrouter("Test prompt")


def test_query_openrouter_success(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key-xyz")
    mock_response = io.BytesIO(
        json.dumps({
            "id": "gen-test-1234",
            "choices": [
                {
                    "message": {
                        "content": "### 1. Key Findings\nAnalysis complete."
                    }
                }
            ],
            "usage": {
                "prompt_tokens": 100,
                "completion_tokens": 200,
                "total_tokens": 300,
            }
        }).encode("utf-8")
    )
    mock_urlopen = MagicMock()
    mock_urlopen.return_value.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", mock_urlopen):
        result = query_openrouter("Analyze this report section", model="deepseek/deepseek-v4.1-flash-1017")
        assert "Analysis complete." in result


def test_query_openrouter_return_details(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key-xyz")
    mock_response = io.BytesIO(
        json.dumps({
            "id": "gen-test-9999",
            "choices": [
                {
                    "message": {
                        "content": "Detailed analysis content."
                    }
                }
            ],
            "usage": {
                "prompt_tokens": 1500,
                "completion_tokens": 2500,
                "total_tokens": 4000,
            }
        }).encode("utf-8")
    )
    mock_urlopen = MagicMock()
    mock_urlopen.return_value.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", mock_urlopen):
        content, stats = query_openrouter(
            "Analyze section",
            model="deepseek/deepseek-v4.1-flash-1017:nitro",
            return_details=True,
        )
        assert content == "Detailed analysis content."
        assert stats["generation_id"] == "gen-test-9999"
        assert stats["model"] == "deepseek/deepseek-v4.1-flash-1017:nitro"
        assert stats["prompt_tokens"] == 1500
        assert stats["completion_tokens"] == 2500
        assert stats["total_tokens"] == 4000


def test_estimate_cost():
    # Base model rates
    cost_base = estimate_cost("deepseek/deepseek-v4.1-flash-1017", 1_000_000, 1_000_000)
    assert cost_base == pytest.approx(0.42, rel=1e-3)

    # Nitro model rates
    cost_nitro = estimate_cost("deepseek/deepseek-v4.1-flash-1017:nitro", 1_000_000, 1_000_000)
    assert cost_nitro == pytest.approx(1.40, rel=1e-3)


def test_query_openrouter_http_error(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key-xyz")
    mock_err_body = io.BytesIO(json.dumps({"error": {"message": "Invalid model"}}).encode("utf-8"))
    http_err = urllib.error.HTTPError("https://openrouter.ai", 400, "Bad Request", {}, mock_err_body)

    with patch("urllib.request.urlopen", side_effect=http_err):
        with pytest.raises(RuntimeError, match="OpenRouter API error.*Invalid model"):
            query_openrouter("Test prompt")


def test_openrouter_worker_execution(qapp, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key-xyz")
    mock_stats = {
        "generation_id": "gen-mock-123",
        "model": "deepseek/deepseek-v4.1-flash-1017",
        "prompt_tokens": 500,
        "completion_tokens": 1000,
        "total_tokens": 1500,
        "cost_usd": 0.00035,
    }
    with patch("section_capture.openrouter.query_openrouter", return_value=("### Mocked response", mock_stats)):
        worker = OpenRouterWorker("Test prompt", parent=None)
        results = []
        worker.finished_query.connect(lambda res, elapsed, stats: results.append((res, elapsed, stats)))
        worker.start()
        worker.wait(3000)
        qapp.processEvents()
        assert len(results) == 1
        assert results[0][0] == "### Mocked response"
        assert results[0][1] >= 0.0
        assert results[0][2]["cost_usd"] == 0.00035
        assert results[0][2]["total_tokens"] == 1500


def test_save_section_llm_response_with_cost_and_tokens(isolated_map_cache):
    db_path, sha256, _ = isolated_map_cache
    sec = insert_section(
        package_id="sec-cost-test-1",
        report_sha256=sha256,
        section_number=1,
        section_id="D001",
        name="01-D001-Test",
        heading="Test Heading",
        subheading=None,
        analyst_question=None,
        selected_text="Some text",
        selections=[{"physical_page": 1, "bbox": [0, 0, 100, 100], "page_size_points": [500, 500], "selection_mode": "text", "text": "Text 1"}],
        stored_questions=None,
        prompt="Test Prompt",
        manifest={"source": {"filename": "test.pdf"}},
        db_path=db_path,
    )
    tokens = {"prompt_tokens": 1000, "completion_tokens": 2000, "total_tokens": 3000}
    updated, _ = save_section_llm_response(
        package_id=sec.package_id,
        llm_response="### Mock Response",
        response_time_seconds=15.42,
        cost_usd=0.004567,
        tokens=tokens,
        model="deepseek/deepseek-v4.1-flash-1017:nitro",
        db_path=db_path,
    )
    assert updated is not None
    assert updated.response_time_seconds == 15.42
    assert updated.cost_usd == 0.004567
    assert updated.model_used == "deepseek/deepseek-v4.1-flash-1017:nitro"
    assert updated.total_tokens == 3000
    assert updated.manifest["review"]["model"] == "deepseek/deepseek-v4.1-flash-1017:nitro"




def test_resubmit_sections_missing_only(isolated_map_cache, monkeypatch):
    from workflow.resubmit_sections import resubmit_sections

    db_path, sha256, tmp_path = isolated_map_cache

    # Insert two sections: sec 1 has response, sec 2 is missing
    insert_section(
        package_id="sec-mock-1",
        report_sha256=sha256,
        section_number=1,
        section_id="D001",
        name="01-D001-Sec1",
        heading="Section One",
        subheading=None,
        analyst_question=None,
        selected_text="Text 1",
        selections=[{"physical_page": 1, "bbox": [0, 0, 100, 100], "page_size_points": [500, 500], "selection_mode": "text", "text": "Text 1"}],
        stored_questions=None,
        prompt="Prompt 1",
        manifest={"source": {"filename": "test.pdf"}},
        db_path=db_path,
    )
    save_section_llm_response(
        package_id="sec-mock-1",
        llm_response="### Already complete",
        db_path=db_path,
    )

    insert_section(
        package_id="sec-mock-2",
        report_sha256=sha256,
        section_number=2,
        section_id="D002",
        name="02-D002-Sec2",
        heading="Section Two",
        subheading=None,
        analyst_question=None,
        selected_text="Text 2",
        selections=[{"physical_page": 2, "bbox": [0, 0, 100, 100], "page_size_points": [500, 500], "selection_mode": "text", "text": "Text 2"}],
        stored_questions=None,
        prompt="Prompt 2",
        manifest={"source": {"filename": "test.pdf"}},
        db_path=db_path,
    )

    # Mock query_openrouter
    call_counts = []

    def mock_query(prompt, model=None, timeout=180, return_details=False):
        call_counts.append(prompt)
        return (
            "### Section Two Brief\n#### 4. Updated Open Questions Ledger\n- [ ] Pending: [Section 3]",
            {"prompt_tokens": 500, "completion_tokens": 200, "cost_usd": 0.001, "generation_id": "gen-123"},
        )

    monkeypatch.setattr("workflow.resubmit_sections.query_openrouter", mock_query)
    monkeypatch.setattr("workflow.resubmit_sections.fetch_generation_stats", lambda gid: None)
    monkeypatch.setattr("workflow.resubmit_sections.find_company_dir", lambda t: ("retail", db_path.parent))

    results = resubmit_sections(
        ticker="LEW",
        report=sha256,
        missing_only=True,
        clear=False,
        delay_seconds=0.0,
        db_path=db_path,
    )

    # Only section 2 should be submitted
    assert len(results) == 1
    assert results[0]["section_number"] == 2
    assert len(call_counts) == 1
