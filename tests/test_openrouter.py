"""Unit tests for the OpenRouter API integration."""

from __future__ import annotations

import io
import json
import urllib.error
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QCoreApplication

from section_capture.openrouter import (
    DEFAULT_MODEL,
    OpenRouterWorker,
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
            "choices": [
                {
                    "message": {
                        "content": "### 1. Key Findings\nAnalysis complete."
                    }
                }
            ]
        }).encode("utf-8")
    )
    mock_urlopen = MagicMock()
    mock_urlopen.return_value.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", mock_urlopen):
        result = query_openrouter("Analyze this report section", model="deepseek/deepseek-v4.1-flash-1017")
        assert "Analysis complete." in result


def test_query_openrouter_http_error(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key-xyz")
    mock_err_body = io.BytesIO(json.dumps({"error": {"message": "Invalid model"}}).encode("utf-8"))
    http_err = urllib.error.HTTPError("https://openrouter.ai", 400, "Bad Request", {}, mock_err_body)

    with patch("urllib.request.urlopen", side_effect=http_err):
        with pytest.raises(RuntimeError, match="OpenRouter API error.*Invalid model"):
            query_openrouter("Test prompt")


def test_openrouter_worker_execution(qapp, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key-xyz")
    with patch("section_capture.openrouter.query_openrouter", return_value="### Mocked response"):
        worker = OpenRouterWorker("Test prompt", parent=None)
        results = []
        worker.finished_query.connect(lambda res: results.append(res))
        worker.start()
        worker.wait(3000)
        qapp.processEvents()
        assert results == ["### Mocked response"]

