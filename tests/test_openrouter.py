"""Unit tests for the OpenRouter API integration."""

from __future__ import annotations

import io
import json
import time
import urllib.error
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QCoreApplication

from section_capture.db import SavedSection, insert_section, save_section_llm_response
from section_capture.openrouter import (
    DEFAULT_MODEL,
    IncompleteCompletionError,
    OpenRouterWorker,
    estimate_cost,
    fetch_generation_stats,
    get_model_display_name,
    get_model_short_tag,
    get_openrouter_api_key,
    get_openrouter_model,
    query_openrouter,
)


def test_get_openrouter_model_default(monkeypatch):
    monkeypatch.delenv("OPENROUTER_MODEL", raising=False)
    with patch("section_capture.openrouter.EXTERNAL_SECRETS_PATH") as mock_path:
        mock_path.exists.return_value = False
        assert get_openrouter_model() == "deepseek/deepseek-v4.1-flash-1017"


def test_get_openrouter_model_env_override(monkeypatch):
    monkeypatch.setenv("OPENROUTER_MODEL", "deepseek/deepseek-r1")
    assert get_openrouter_model() == "deepseek/deepseek-r1"


def test_get_model_display_name_and_short_tag(monkeypatch):
    # Default model (normal routing, with provider selected in the request)
    monkeypatch.delenv("OPENROUTER_MODEL", raising=False)
    with patch("section_capture.openrouter.EXTERNAL_SECRETS_PATH") as mock_path:
        mock_path.exists.return_value = False
        assert get_model_display_name() == "DeepSeek Flash"
        assert get_model_short_tag() == "DeepSeek"

    # Base model without :nitro
    assert get_model_display_name("deepseek/deepseek-v4.1-flash-1017") == "DeepSeek Flash"
    assert get_model_short_tag("deepseek/deepseek-v4.1-flash-1017") == "DeepSeek"

    # With :nitro
    assert get_model_display_name("deepseek/deepseek-v4.1-flash-1017:nitro") == "DeepSeek Flash (nitro)"
    assert get_model_short_tag("deepseek/deepseek-v4.1-flash-1017:nitro") == "DeepSeek:nitro"

    # Claude 3.5 Sonnet
    assert get_model_display_name("anthropic/claude-3.5-sonnet") == "Claude 3.5 Sonnet"
    assert get_model_short_tag("anthropic/claude-3.5-sonnet") == "Claude"

    # Claude 3.7 Sonnet :nitro
    assert get_model_display_name("anthropic/claude-3.7-sonnet:nitro") == "Claude 3.7 Sonnet (nitro)"
    assert get_model_short_tag("anthropic/claude-3.7-sonnet:nitro") == "Claude:nitro"

    # OpenAI GPT-4o
    assert get_model_display_name("openai/gpt-4o") == "GPT-4o"
    assert get_model_short_tag("openai/gpt-4o") == "GPT-4o"
    assert get_model_display_name("openai/gpt-4o-mini") == "GPT-4o Mini"

    # Google Gemini
    assert get_model_display_name("google/gemini-2.0-flash") == "Gemini 2.0 Flash"
    assert get_model_short_tag("google/gemini-2.0-flash") == "Gemini"

    # Fallback custom provider
    assert get_model_display_name("mistralai/mixtral-8x7b-instruct") == "Mixtral 8x7b Instruct"
    assert get_model_short_tag("mistralai/mixtral-8x7b-instruct") == "Mixtral"

    # Empty string fallback
    assert get_model_display_name("") == "AI Model"
    assert get_model_short_tag("") == "AI"


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
    with patch("section_capture.openrouter.query_openrouter", return_value=("### Mocked response", mock_stats)) as mocked_query:
        worker = OpenRouterWorker("Test prompt", parent=None, reasoning_effort="max", max_tokens=65536)
        results = []
        worker.finished_query.connect(lambda res, elapsed, stats: results.append((res, elapsed, stats)))
        worker.start()
        assert worker.wait(10000)
        for _ in range(20):
            qapp.processEvents()
            if results:
                break
            time.sleep(0.02)
        assert len(results) == 1
        assert results[0][0] == "### Mocked response"
        assert results[0][1] >= 0.0
        assert results[0][2]["cost_usd"] == 0.00035
        assert results[0][2]["total_tokens"] == 1500
        assert mocked_query.call_args.kwargs["reasoning_effort"] == "max"
        assert mocked_query.call_args.kwargs["max_tokens"] == 65536


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
            '### Section Two Brief\n#### 4. Updated Open Questions Ledger\n```json\n'
            '{"ledger_version":1,"updates":[],"new_questions":[]}\n```',
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


def test_query_openrouter_retry_on_winerror_10054(monkeypatch):
    """Verifies that query_openrouter transparently retries on connection reset (10054)."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key-xyz")
    monkeypatch.setattr("time.sleep", lambda s: None)  # fast tests

    attempts = []

    def mock_urlopen(req, timeout=180):
        attempts.append(req)
        if len(attempts) < 3:
            raise ConnectionResetError(10054, "An existing connection was forcibly closed by the remote host")
        mock_resp = io.BytesIO(
            json.dumps({
                "id": "gen-retry-ok",
                "choices": [{"message": {"content": "Retry successful after drops!"}}],
                "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
            }).encode("utf-8")
        )
        return mock_resp

    with patch("urllib.request.urlopen", side_effect=mock_urlopen):
        result = query_openrouter("Test prompt", model="deepseek/deepseek-v4.1-flash-1017:nitro")
        assert result == "Retry successful after drops!"
        assert len(attempts) == 3


def test_query_openrouter_nitro_fallback_to_standard(monkeypatch):
    """Verifies that on repeated drops, query_openrouter gracefully falls back from :nitro to standard endpoint."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key-xyz")
    monkeypatch.setattr("time.sleep", lambda s: None)

    models_seen = []

    def mock_urlopen(req, timeout=180):
        body = json.loads(req.data.decode("utf-8"))
        models_seen.append(body["model"])
        if len(models_seen) < 3:
            import http.client
            raise http.client.RemoteDisconnected("Remote end closed connection without response")
        mock_resp = io.BytesIO(
            json.dumps({
                "id": "gen-fallback-ok",
                "choices": [{"message": {"content": "Fallback successful!"}}],
                "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
            }).encode("utf-8")
        )
        return mock_resp

    with patch("urllib.request.urlopen", side_effect=mock_urlopen):
        result = query_openrouter("Test prompt", model="deepseek/deepseek-v4.1-flash-1017:nitro")
        assert result == "Fallback successful!"
        assert len(models_seen) == 3
        # First 2 attempts used :nitro
        assert models_seen[0] == "deepseek/deepseek-v4.1-flash-1017:nitro"
        assert models_seen[1] == "deepseek/deepseek-v4.1-flash-1017:nitro"
        # 3rd attempt stepped down to standard endpoint
        assert models_seen[2] == "deepseek/deepseek-v4.1-flash-1017"


@pytest.mark.parametrize("effort", ["none", "max"])
def test_reasoning_policy_reaches_http_payload_and_usage(monkeypatch, effort):
    monkeypatch.setattr("section_capture.openrouter.get_openrouter_api_key", lambda: "fake-key")
    payloads = []

    def respond(req, timeout):
        payloads.append(json.loads(req.data))
        return io.BytesIO(json.dumps({
            "id": "gen-reasoning-test",
            "provider": "mock-provider",
            "choices": [{"message": {"content": "Completed financial analysis"}, "finish_reason": "stop"}],
            "usage": {"completion_tokens": 1000, "completion_tokens_details": {"reasoning_tokens": 600}},
        }).encode())

    with patch("urllib.request.urlopen", side_effect=respond):
        content, stats = query_openrouter("Report", reasoning_effort=effort, max_tokens=65536, return_details=True)
    assert content == "Completed financial analysis"
    assert payloads[0]["reasoning"] == {"effort": effort, "exclude": True}
    assert payloads[0]["max_tokens"] == 65536
    assert payloads[0]["provider"] == {"only": ["fireworks"], "allow_fallbacks": False, "require_parameters": True}
    assert stats["reasoning_effort_requested"] == effort
    assert stats["reasoning_tokens"] == 600
    assert stats["max_tokens_requested"] == 65536
    assert stats["finish_reason"] == "stop"


@pytest.mark.parametrize("content,finish_reason", [("Partial valuation", "length"), ("", "length"), ("", "stop")])
def test_incomplete_or_reasoning_only_completion_is_never_a_report(monkeypatch, content, finish_reason):
    monkeypatch.setattr("section_capture.openrouter.get_openrouter_api_key", lambda: "fake-key")
    response = io.BytesIO(json.dumps({
        "choices": [{"message": {"content": content, "reasoning": "Internal reasoning is not a final report"},
                     "finish_reason": finish_reason}],
        "usage": {"completion_tokens": 1024},
    }).encode())
    with patch("urllib.request.urlopen", return_value=response) as request:
        with pytest.raises(IncompleteCompletionError):
            query_openrouter("Report", reasoning_effort="max")
    assert request.call_count == 1


def test_max_reasoning_survives_nitro_fallback(monkeypatch):
    monkeypatch.setattr("section_capture.openrouter.get_openrouter_api_key", lambda: "fake-key")
    monkeypatch.setattr("time.sleep", lambda _: None)
    payloads = []

    def respond(req, timeout):
        payloads.append(json.loads(req.data))
        if len(payloads) < 3:
            raise ConnectionResetError("mock disconnection")
        return io.BytesIO(json.dumps({"choices": [{"message": {"content": "Complete report"},
                                                     "finish_reason": "stop"}]}).encode())

    with patch("urllib.request.urlopen", side_effect=respond):
        assert query_openrouter("Report", model=DEFAULT_MODEL+":nitro", reasoning_effort="max", max_tokens=65536) == "Complete report"
    assert payloads[-1]["model"] == DEFAULT_MODEL.replace(":nitro", "")
    assert all(p["reasoning"]["effort"] == "max" and p["max_tokens"] == 65536 for p in payloads)
    assert all(p["provider"] == {"only": ["fireworks"], "allow_fallbacks": False, "require_parameters": True} for p in payloads)


def test_fireworks_selection_does_not_apply_to_other_models(monkeypatch):
    monkeypatch.setattr("section_capture.openrouter.get_openrouter_api_key", lambda: "fake-key")
    response = io.BytesIO(json.dumps({"choices": [{"message": {"content": "Complete"}, "finish_reason": "stop"}]}).encode())
    with patch("urllib.request.urlopen", return_value=response) as request:
        query_openrouter("Report", model="other/model", reasoning_effort="none")
    assert "provider" not in json.loads(request.call_args.args[0].data)


def test_presentation_clustering_uses_fireworks_without_provider_fallback(monkeypatch):
    from section_capture import section_matcher
    monkeypatch.setattr(section_matcher, "get_openrouter_api_key", lambda: "fake-key")
    sections = [{"title": "Overview", "start_page": 1, "end_page": 2},
                {"title": "Financial review", "start_page": 3, "end_page": 4}]
    response = io.BytesIO(json.dumps({"choices": [{"message": {"content": json.dumps(sections)}}]}).encode())
    manifest = [{"slide_num": i, "title": "Slide", "snippet": "Evidence"} for i in range(1, 5)]
    with patch("urllib.request.urlopen", return_value=response) as request:
        result = section_matcher.llm_cluster_presentation_sections(manifest, "example.pdf")
    assert [(s["start_page"], s["end_page"]) for s in result] == [(1, 2), (3, 4)]
    payload = json.loads(request.call_args.args[0].data)
    assert payload["provider"] == {"only": ["fireworks"], "allow_fallbacks": False, "require_parameters": True}
