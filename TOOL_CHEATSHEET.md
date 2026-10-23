# Agent Tooling Cheatsheet & Gotchas

Keep interventions fast, lean, and error-free on Windows + PowerShell.

---

### 1. PowerShell & Python One-Liners
* **Quote stripping issue**: PowerShell swallows nested double quotes in `python -c "..."`, causing `SyntaxError: unterminated string literal`.
* **Multi-line parser error**: Running multi-line `python -c "..."` causes `ScriptBlock should only be specified as a value of the Command parameter`.
* **Windows Charmap / Unicode error**: PowerShell defaults to `cp1252`. Printing Unicode characters like `⚡`, `✓`, or emojis crashes Python with `UnicodeEncodeError: 'charmap' codec can't encode character...`.
* **Rules**:
  1. Never run SQL strings or nested quotes with `python -c "..."`.
  2. For simple Python one-liners in PowerShell, wrap in single quotes:
     ```powershell
     python -c 'from section_capture.db import connect_db; print("ok")'
     ```
  3. Set `$env:PYTHONIOENCODING="utf-8"` whenever printing or inspecting text containing Unicode/emojis.
  4. Never run multi-line Python code via `-c`. Put multi-line logic in a scratch `.py` file (e.g. `scratch/run.py`) and execute `python scratch/run.py`.

---

### 2. `edit_file` & Windows CRLF Newlines
* **Target not found issue**: Windows files often use CRLF (`\r\n`). Mismatches in line endings or indentation cause `edit_file` to fail.
* **Rules**:
  1. Keep `Target` small and unique (3–6 lines) instead of huge blocks.
  2. Include exact leading indentation.
  3. If `edit_file` fails once due to line endings, don't write complex multi-file patch scripts—use a simple 3-line Python replacement:
     ```python
     p.write_text(p.read_text("utf-8").replace(old, new, 1), "utf-8")
     ```

---

### 3. Workflow Speed & Focus
* **Fix the direct issue first**: Make the 1–3 line code fix immediately.
* **Targeted tests before full suite**: Run `pytest tests/test_specific.py` (~5s) to verify logic before running full suite (~25s).
* **Avoid unnecessary audits**: Don't query or inspect unrelated historical records unless explicitly asked.
