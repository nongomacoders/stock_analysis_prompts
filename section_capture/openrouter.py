"""OpenRouter API client and non-blocking background worker for section capture.

Loads credentials strictly in memory from external secrets or environment,
without logging or exposing the secret key value.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import urllib.request
import urllib.error

from PySide6.QtCore import QThread, Signal

OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "deepseek/deepseek-v4.1-flash-1017"
EXTERNAL_SECRETS_PATH = Path(r"C:\Users\Dion\Desktop\Projects\EXTERNAL_TO_REPOS\credentials\secrets.env")


def get_openrouter_api_key() -> str:
    """Retrieves the OpenRouter API key strictly into memory without logging."""
    # 1. External secrets file (Primary credential store)
    if EXTERNAL_SECRETS_PATH.exists():
        try:
            for line in EXTERNAL_SECRETS_PATH.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("OPENROUTER_API_KEY="):
                    val = line.split("=", 1)[1].strip()
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    if val.strip():
                        return val.strip()
        except Exception:
            pass

    # 2. Environment variable
    env_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if env_key:
        return env_key

    # 3. Local project .env file
    local_env = Path(".env")
    if local_env.exists():
        try:
            for line in local_env.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("OPENROUTER_API_KEY="):
                    val = line.split("=", 1)[1].strip()
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    if val.strip():
                        return val.strip()
        except Exception:
            pass

    return ""


def get_openrouter_model() -> str:
    """Retrieves the preferred OpenRouter model, defaulting to deepseek/deepseek-chat."""
    model = os.environ.get("OPENROUTER_MODEL", "").strip()
    if model:
        return model

    # Check external secrets
    if EXTERNAL_SECRETS_PATH.exists():
        try:
            for line in EXTERNAL_SECRETS_PATH.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("OPENROUTER_MODEL="):
                    val = line.split("=", 1)[1].strip()
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    if val.strip():
                        return val.strip()
        except Exception:
            pass

    return DEFAULT_MODEL


def estimate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Fallback estimation of query cost based on known OpenRouter rates."""
    is_nitro = ":nitro" in (model or "").lower()
    # DeepSeek v4.1 Flash base vs nitro rates
    p_rate = 0.50 / 1_000_000 if is_nitro else 0.14 / 1_000_000
    c_rate = 0.90 / 1_000_000 if is_nitro else 0.28 / 1_000_000
    return round((prompt_tokens * p_rate) + (completion_tokens * c_rate), 6)


def fetch_generation_stats(generation_id: str, key: str | None = None, timeout: int = 10) -> dict:
    """Fetch exact token and billing stats from OpenRouter generation endpoint."""
    api_key = key or get_openrouter_api_key()
    if not api_key or not generation_id:
        return {}
    url = f"https://openrouter.ai/api/v1/generation?id={generation_id}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://github.com/dion/stock_analysis_prompts",
            "X-Title": "Stock Analysis Section Capture",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body.get("data", {})
    except Exception:
        return {}


def query_openrouter(
    prompt: str,
    model: str | None = None,
    timeout: int = 180,
    return_details: bool = False,
) -> str | tuple[str, dict]:
    """Executes a synchronous completion query via OpenRouter API.
    
    If return_details is True, returns (content, stats_dict).
    Raises RuntimeError if key is missing or API call fails.
    """
    key = get_openrouter_api_key()
    if not key:
        raise RuntimeError("OpenRouter API key not found in secrets.env or environment.")

    active_model = model or get_openrouter_model()

    payload = {
        "model": active_model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
    }

    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OPENROUTER_ENDPOINT,
        data=req_data,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/dion/stock_analysis_prompts",
            "X-Title": "Stock Analysis Section Capture",
            "User-Agent": "Antigravity/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            res_body = response.read().decode("utf-8")
            data = json.loads(res_body)
            choices = data.get("choices", [])
            if not choices:
                raise RuntimeError("OpenRouter returned empty choices array.")
            content = choices[0]["message"]["content"]
            if not return_details:
                return content
            usage = data.get("usage") or {}
            stats = {
                "generation_id": data.get("id", ""),
                "model": active_model,
                "prompt_tokens": int(usage.get("prompt_tokens", 0) or 0),
                "completion_tokens": int(usage.get("completion_tokens", 0) or 0),
                "total_tokens": int(usage.get("total_tokens", 0) or 0),
                "cost_usd": None,
            }
            return content, stats
    except urllib.error.HTTPError as err:
        try:
            err_body = err.read().decode("utf-8")
            err_json = json.loads(err_body)
            msg = err_json.get("error", {}).get("message", str(err))
        except Exception:
            msg = f"HTTP Error {err.code}: {err.reason}"
        raise RuntimeError(f"OpenRouter API error ({active_model}): {msg}") from None
    except Exception as exc:
        raise RuntimeError(f"OpenRouter connection error ({active_model}): {exc}") from None


import time


class OpenRouterWorker(QThread):
    """Background worker thread to run OpenRouter completions without freezing the GUI."""
    
    started_query = Signal(str)  # Emits model name
    finished_query = Signal(str, float, object)  # Emits (response_text, elapsed_seconds, stats_dict)
    error_query = Signal(str)  # Emits error message

    def __init__(self, prompt: str, model: str | None = None, parent=None):
        super().__init__(parent)
        self.prompt = prompt
        self.model = model or get_openrouter_model()
        self.last_stats: dict = {}

    def run(self):
        self.started_query.emit(self.model)
        start_t = time.time()
        try:
            res, stats = query_openrouter(self.prompt, self.model, return_details=True)
            elapsed = time.time() - start_t
            stats["elapsed_seconds"] = round(elapsed, 2)
            gen_id = stats.get("generation_id")
            if gen_id:
                # Brief check on generation endpoint for exact total_cost
                time.sleep(0.3)
                gstats = fetch_generation_stats(gen_id)
                if gstats and gstats.get("total_cost") is not None:
                    stats["cost_usd"] = float(gstats["total_cost"])
                    if gstats.get("tokens_prompt"):
                        stats["prompt_tokens"] = int(gstats["tokens_prompt"])
                    if gstats.get("tokens_completion"):
                        stats["completion_tokens"] = int(gstats["tokens_completion"])
                    stats["total_tokens"] = stats["prompt_tokens"] + stats["completion_tokens"]
            if stats.get("cost_usd") is None:
                stats["cost_usd"] = estimate_cost(
                    self.model,
                    stats.get("prompt_tokens", 0),
                    stats.get("completion_tokens", 0),
                )
            self.last_stats = stats
            self.finished_query.emit(res, elapsed, stats)
        except Exception as exc:
            self.error_query.emit(str(exc))

