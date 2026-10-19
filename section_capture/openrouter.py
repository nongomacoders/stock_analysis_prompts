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


def query_openrouter(prompt: str, model: str | None = None, timeout: int = 180) -> str:
    """Executes a synchronous completion query via OpenRouter API.
    
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
            return choices[0]["message"]["content"]
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


class OpenRouterWorker(QThread):
    """Background worker thread to run OpenRouter completions without freezing the GUI."""
    
    started_query = Signal(str)  # Emits model name
    finished_query = Signal(str)  # Emits response text
    error_query = Signal(str)  # Emits error message

    def __init__(self, prompt: str, model: str | None = None, parent=None):
        super().__init__(parent)
        self.prompt = prompt
        self.model = model or get_openrouter_model()

    def run(self):
        self.started_query.emit(self.model)
        try:
            res = query_openrouter(self.prompt, self.model)
            self.finished_query.emit(res)
        except Exception as exc:
            self.error_query.emit(str(exc))
