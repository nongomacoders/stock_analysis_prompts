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
DEFAULT_MODEL = "deepseek/deepseek-v4.1-flash-1017:nitro"
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXTERNAL_SECRETS = REPO_ROOT.parent / "EXTERNAL_TO_REPOS" / "credentials" / "secrets.env"
EXTERNAL_SECRETS_PATH = Path(os.environ.get("EXTERNAL_SECRETS_PATH", str(DEFAULT_EXTERNAL_SECRETS))).expanduser()


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


def get_model_display_name(model: str | None = None) -> str:
    """Returns a short, clean, human-readable display name for the configured OpenRouter model."""
    raw = (model if model is not None else get_openrouter_model()).strip()
    if not raw:
        return "AI Model"

    is_nitro = ":nitro" in raw.lower()
    clean = raw.replace(":nitro", "").replace(":free", "").strip()
    _, _, model_id = clean.partition("/")
    if not model_id:
        model_id = clean

    low_id = model_id.lower()
    if "deepseek-v4.1-flash" in low_id or "deepseek-flash" in low_id:
        name = "DeepSeek Flash"
    elif "deepseek-chat" in low_id or "deepseek-v3" in low_id:
        name = "DeepSeek Chat"
    elif "deepseek-r1" in low_id:
        name = "DeepSeek R1"
    elif "claude-3-5-sonnet" in low_id or "claude-3.5-sonnet" in low_id:
        name = "Claude 3.5 Sonnet"
    elif "claude-3-7-sonnet" in low_id or "claude-3.7-sonnet" in low_id:
        name = "Claude 3.7 Sonnet"
    elif "gemini-2.0-flash" in low_id:
        name = "Gemini 2.0 Flash"
    elif "gemini-2.5-pro" in low_id:
        name = "Gemini 2.5 Pro"
    elif "gpt-4o-mini" in low_id:
        name = "GPT-4o Mini"
    elif "gpt-4o" in low_id:
        name = "GPT-4o"
    elif "llama-3.3-70b" in low_id:
        name = "Llama 3.3 70B"
    elif "qwen-2.5-72b" in low_id:
        name = "Qwen 2.5 72B"
    else:
        parts = [p.capitalize() for p in model_id.replace("_", "-").split("-") if p]
        name = " ".join(parts) if parts else model_id

    if is_nitro:
        name += " (nitro)"
    return name


def get_model_short_tag(model: str | None = None) -> str:
    """Returns a short identifier tag suitable for status lines, buttons, or badges (e.g. DeepSeek, DeepSeek:nitro, Claude)."""
    raw = (model if model is not None else get_openrouter_model()).strip()
    is_nitro = ":nitro" in raw.lower()
    disp = get_model_display_name(raw).replace(" (nitro)", "").strip()
    first = disp.split()[0] if disp else "AI"
    return f"{first}:nitro" if is_nitro else first


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
    max_tokens: int = 16384,
    plugins: list[dict[str, Any]] | None = None,
    web_search: bool = False,
) -> str | tuple[str, dict]:
    """Executes a synchronous completion query via OpenRouter API.
    
    If web_search is True and plugins is None, automatically attaches the OpenRouter web search plugin.
    If return_details is True, returns (content, stats_dict).
    Raises RuntimeError if key is missing or API call fails.
    """
    key = get_openrouter_api_key()
    if not key:
        raise RuntimeError("OpenRouter API key not found in secrets.env or environment.")

    active_model = model or get_openrouter_model()

    active_plugins = plugins
    if web_search and not active_plugins:
        active_plugins = [{"id": "web"}]

    attempts = 4
    for attempt in range(1, attempts + 1):
        # Fallback from :nitro to standard model if nitro endpoint drops repeatedly
        current_model = active_model
        if attempt >= 3 and ":nitro" in active_model.lower():
            current_model = active_model.replace(":nitro", "").strip()

        payload: dict[str, Any] = {
            "model": current_model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "max_tokens": max_tokens,
            "reasoning": {"effort": "none"},
        }
        if active_plugins:
            # On final attempt, if earlier attempts failed, try omitting plugins in case of endpoint incompatibility
            if attempt < attempts or not active_plugins:
                payload["plugins"] = active_plugins

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
                "Connection": "close",
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
                msg = choices[0].get("message", {})
                content = (msg.get("content") or "").strip()
                reasoning = (msg.get("reasoning") or "").strip()
                finish_reason = choices[0].get("finish_reason")
                usage = data.get("usage") or {}

                if not content:
                    if finish_reason == "length":
                        comp_tok = usage.get("completion_tokens", 0)
                        raise RuntimeError(
                            f"Model reached completion limit ({comp_tok:,} tokens) before generating response content (finish_reason: length)."
                        )
                    if reasoning:
                        content = reasoning
                    else:
                        raise RuntimeError(f"OpenRouter returned empty response (finish_reason: {finish_reason}).")

                if not return_details:
                    return content
                stats = {
                    "generation_id": data.get("id", ""),
                    "model": current_model,
                    "prompt_tokens": int(usage.get("prompt_tokens", 0) or 0),
                    "completion_tokens": int(usage.get("completion_tokens", 0) or 0),
                    "total_tokens": int(usage.get("total_tokens", 0) or 0),
                    "cost_usd": None,
                }
                return content, stats
        except urllib.error.HTTPError as err:
            if err.code in (429, 500, 502, 503, 504, 520, 524) and attempt < attempts:
                retry_after = err.headers.get("Retry-After") if err.headers else None
                wait_sec = float(retry_after) if retry_after and retry_after.isdigit() else (2 ** attempt)
                time.sleep(wait_sec)
                continue
            try:
                err_body = err.read().decode("utf-8")
                err_json = json.loads(err_body)
                msg = err_json.get("error", {}).get("message", str(err))
            except Exception:
                msg = f"HTTP Error {err.code}: {err.reason}"
            raise RuntimeError(f"OpenRouter API error ({current_model}): {msg}") from None
        except Exception as exc:
            if attempt < attempts:
                time.sleep(2 ** attempt)
                continue
            err_desc = str(exc) or exc.__class__.__name__
            raise RuntimeError(f"OpenRouter connection error ({current_model}): {err_desc}") from None


import time


class OpenRouterWorker(QThread):
    """Background worker thread to run OpenRouter completions without freezing the GUI."""
    
    started_query = Signal(str)  # Emits model name
    finished_query = Signal(str, float, object)  # Emits (response_text, elapsed_seconds, stats_dict)
    error_query = Signal(str)  # Emits error message

    def __init__(self, prompt: str, model: str | None = None, parent=None, timeout: int = 180, max_tokens: int = 16384):
        super().__init__(parent)
        self.prompt = prompt
        self.model = model or get_openrouter_model()
        self.timeout = timeout
        self.max_tokens = max_tokens
        self.last_stats: dict = {}

    def run(self):
        self.started_query.emit(self.model)
        start_t = time.time()
        try:
            res, stats = query_openrouter(self.prompt, self.model, timeout=self.timeout, return_details=True, max_tokens=self.max_tokens)
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

