"""Interactive test script to verify OpenRouter API connectivity and model execution.

Safely tests credential loading, authentication, and chat completions without
ever logging or exposing the secret key value.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import time
import urllib.error
import urllib.request

from section_capture.openrouter import (
    DEFAULT_MODEL,
    EXTERNAL_SECRETS_PATH,
    get_openrouter_api_key,
    get_openrouter_model,
    query_openrouter,
)


def mask_key_status(key: str) -> str:
    """Returns a safe descriptive string about key presence without revealing characters."""
    if not key:
        return "[NOT FOUND]"
    prefix = key[:9] if key.startswith("sk-or-v1-") else "custom"
    return f"[PRESENT] (Length: {len(key)} chars, format: {prefix}...)"


def check_auth_key(key: str) -> dict | None:
    """Checks the OpenRouter auth key endpoint for account validity and limits."""
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/auth/key",
        headers={
            "Authorization": f"Bearer {key}",
            "HTTP-Referer": "https://github.com/dion/stock_analysis_prompts",
            "X-Title": "Stock Analysis OpenRouter Test",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("data", {})
    except urllib.error.HTTPError as err:
        try:
            body = json.loads(err.read().decode("utf-8"))
            msg = body.get("error", {}).get("message", str(err))
        except Exception:
            msg = f"HTTP {err.code}: {err.reason}"
        print(f"[-] Auth verification returned error ({err.code}): {msg}")
        return None
    except Exception as exc:
        print(f"[-] Connection error during auth check: {exc}")
        return None


def run_live_test(model: str | None = None, prompt: str | None = None) -> bool:
    print("=" * 65)
    print("           OPENROUTER API LIVE CONNECTIVITY TEST")
    print("=" * 65)

    # 1. Credential Check
    print("\n[1/3] Checking Credentials...")
    key = get_openrouter_api_key()
    if not key:
        print("  [-] ERROR: No OpenRouter API key found.")
        print(f"      Checked:")
        print(f"      - Environment variable: OPENROUTER_API_KEY")
        print(f"      - External secrets file: {EXTERNAL_SECRETS_PATH}")
        print(f"      - Local project file: .env")
        print("\n  [!] Please ensure your key is added as OPENROUTER_API_KEY=<key>.")
        return False

    status_desc = mask_key_status(key)
    source = "Unknown"

    if EXTERNAL_SECRETS_PATH.exists():
        try:
            for l in EXTERNAL_SECRETS_PATH.read_text(encoding="utf-8").splitlines():
                if l.strip().startswith("OPENROUTER_API_KEY="):
                    v = l.strip().split("=", 1)[1].strip().strip("'\"")
                    if v and v == key:
                        source = f"External Secrets File ({EXTERNAL_SECRETS_PATH})"
                        break
        except Exception:
            pass
    if source == "Unknown" and os.environ.get("OPENROUTER_API_KEY", "").strip() == key:
        source = "Environment Variable (OPENROUTER_API_KEY)"
    elif source == "Unknown":
        source = "Local .env file"

    print(f"  [+] Key Detected: {status_desc}")
    print(f"  [+] Key Source:   {source}")


    # 2. Key Auth / Account Endpoint
    print("\n[2/3] Checking OpenRouter Authentication Endpoint...")
    auth_data = check_auth_key(key)
    if auth_data is not None:
        label = auth_data.get("label", "N/A")
        usage = auth_data.get("usage", "N/A")
        limit = auth_data.get("limit", "N/A")
        is_free_tier = auth_data.get("is_free_tier", "N/A")
        print("  [+] Authentication successful!")
        print(f"      - Key Label:    {label}")
        print(f"      - Usage:        ${usage}")
        print(f"      - Credit Limit: ${limit}")
        print(f"      - Free Tier:    {is_free_tier}")
    else:
        print("  [!] Warning: /api/v1/auth/key did not validate this key.")
        print("      If your key was recently generated or has restricted permissions,")
        print("      the chat completion call below will provide the exact error message.")

    # 3. Chat Completion Execution
    active_model = model or get_openrouter_model()
    test_prompt = prompt or "Respond with exactly: 'OpenRouter connection successful!'"

    print(f"\n[3/3] Testing Completion with Model: {active_model}...")
    print(f"  [>] Prompt: \"{test_prompt}\"")
    
    start_time = time.time()
    try:
        response_text = query_openrouter(test_prompt, model=active_model, timeout=60)
        elapsed = time.time() - start_time
        print(f"  [+] Response received in {elapsed:.2f}s:")
        print("  " + "-" * 55)
        for line in response_text.strip().splitlines():
            print(f"    {line}")
        print("  " + "-" * 55)
        print("\n[SUCCESS] OpenRouter API is fully operational and ready for capture!")
        return True
    except RuntimeError as err:
        elapsed = time.time() - start_time
        print(f"  [-] Query failed after {elapsed:.2f}s:")
        print(f"      {err}")
        print("\n[FAILURE] Completion query did not succeed.")
        if "User not found" in str(err) or "401" in str(err):
            print("\n[TROUBLESHOOTING TIP]:")
            print("  The API returned 'User not found' (HTTP 401).")
            print("  This means OpenRouter does not recognize this key.")
            print("  1. Log into your dashboard at https://openrouter.ai/keys")
            print("  2. Create a new API key.")
            print(f"  3. Replace the key in: {EXTERNAL_SECRETS_PATH}")
        return False
    except Exception as exc:
        print(f"  [-] Unexpected error: {exc}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Test OpenRouter API connectivity and model execution.")
    parser.add_argument("--model", "-m", help=f"Model identifier (default: {DEFAULT_MODEL})", default=None)
    parser.add_argument("--prompt", "-p", help="Custom prompt string to test", default=None)

    args = parser.parse_args()
    success = run_live_test(model=args.model, prompt=args.prompt)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
