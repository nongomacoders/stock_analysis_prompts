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

---

### 4. Cross-Thread Qt Testing in PyTest
* **Issue**: Testing `QThread` workers (e.g. `worker.start()`, `worker.wait()`) can experience race conditions where cross-thread queued signals have posted to the event loop, but a single `qapp.processEvents()` immediately after `wait()` misses delivery under CPU contention across full test suites.
* **Rule**:
  Poll `qapp.processEvents()` in a short loop with brief sleeps until the slot receives the signal:
  ```python
  assert worker.wait(5000)
  for _ in range(20):
      qapp.processEvents()
      if results:
          break
      time.sleep(0.02)
  assert len(results) == 1
  ```

---

### 5. Windows File Locking & SQLite Databases
* **Locking error**: Running `git restore documents/analysis.sqlite` or `shutil.rmtree(tmp_dir)` on Windows fails with `unable to unlink: Invalid argument` or `PermissionError: [WinError 32] The process cannot access the file because it is being used by another process`.
* **Causes**:
  1. The local PySide6 GUI app is actively running on the desktop and holds an open SQLite connection lock on `documents/analysis.sqlite`.
  2. A scratch Python script didn't explicitly close its SQLite connection or `PdfSource` before attempting to delete a temporary folder.
* **Rules**:
  1. Never run `git restore` or `git checkout` on `.sqlite` database files while the desktop application is running. Only stage and commit code/text files (`.py`, `.md`).
  2. Always explicitly close `conn.close()` and `source.close()` in scratch scripts before calling `shutil.rmtree()`.

---

### 6. Scratch Scripts & `sys.path`
* **Import error**: `ModuleNotFoundError: No module named 'section_capture'` when executing `python scratch/my_script.py`.
* **Rule**:
  Always add workspace root to `sys.path` at the very top of scratch scripts:
  ```python
  import sys
  sys.path.insert(0, ".")
  ```
