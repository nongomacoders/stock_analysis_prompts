# Agent Tooling Cheatsheet & Gotchas

Keep interventions fast, lean, and error-free on Windows + PowerShell.

---

### 1. PowerShell & Python One-Liners
* **Quote stripping issue**: PowerShell swallows nested double quotes in `python -c "..."`, causing `SyntaxError: unterminated string literal`.
* **Bracket / type literal parsing**: PowerShell treats unquoted brackets like `print([c[1] for c in ...])` inside command strings as attribute or type literal expressions, throwing `Missing ] at end of attribute or type literal`.
* **Multi-line parser error**: Running multi-line `python -c "..."` causes `ScriptBlock should only be specified as a value of the Command parameter`.
* **Windows Charmap / Unicode error**: PowerShell defaults to `cp1252`. Printing Unicode characters like `⚡`, `✓`, or emojis crashes Python with `UnicodeEncodeError: 'charmap' codec can't encode character...`.
* **PowerShell Ampersand (`&`) error**: An unquoted or double-quote-nested ampersand (`&`) in PowerShell command lines triggers `The ampersand (&) character is not allowed. The & operator is reserved for future use`.
* **Rules**:
  1. Never run SQL strings or nested quotes with `python -c "..."`.
  2. For simple Python one-liners in PowerShell, wrap in single quotes or avoid bracket indexing:
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
* **PyTest `--basetemp` parent directory**: On Windows, passing `--basetemp=tmp/<task>` when `tmp/` does not already exist raises `FileNotFoundError: [WinError 3] The system cannot find the path specified`. Always ensure `tmp/` exists (`New-Item -ItemType Directory -Force -Path tmp`) before passing subdirectories as `--basetemp`.
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

---

### 7. Python 3.12+ Raw String Templates in Scratch Scripts
* **Warning**: `SyntaxWarning: invalid escape sequence '\d'` or `'\-'` when multi-line string templates in scratch replacement scripts contain unescaped regex patterns.
* **Rule**:
  Always use raw triple quotes `r"""..."""` for multi-line replacement blocks containing backslashes or regex patterns (`\d`, `\-`, `\s`).

---

### 8. Tool Absolute Path Requirements
* **Tool path error**: Calling `read_file`, `write_file`, or `edit_file` with a relative path (e.g. `companies/sectors.py`) causes `failed to parse path: ... must be an absolute path: path is not absolute`.
* **Rule**: Always pass absolute paths (e.g. `c:/Users/Dion/Desktop/Projects/stock_analysis_prompts/...`) to file inspection and editing tools.

---

### 9. PyTest Fixtures & Dataclass Return Types in `section_capture`
* **PyTest Fixtures & SQLite `NOT NULL` schema**:
  1. Always use `upsert_report()` instead of raw SQL `INSERT INTO reports` in tests to ensure required columns like `original_path` satisfy NOT NULL constraints.
  2. Use `qapp` (defined in `tests/conftest.py`) instead of `qtbot`.
* **Modal blocking during headless test runs**: Functions that trigger `QMessageBox.information`, `QMessageBox.warning`, or `QMessageBox.question` will hang the test suite if not monkeypatched. In tests invoking dialog actions:
  ```python
  monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
  monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
  monkeypatch.setattr(QMessageBox, "question", lambda *args, **kwargs: QMessageBox.StandardButton.Yes)
  ```
* **Dataclass vs Dictionary returns**: `list_sections()` returns dataclass objects of type `SavedSection`. Access attributes directly (`sec.heading`, `sec.selected_text`), never via dictionary indexing (`sec["heading"]`).
* **Content type enum keys**: `packages.save_package()` validates `capture.content_type in CONTENT_TYPES`. Use lowercase enum keys (`"commentary"`, `"table"`, `"financial_note"`, `"unspecified"`), not display title strings (`"Table"`).

---

### 10. PowerShell `%` Operator Gotcha
* **Issue**: The `%` character in PowerShell command lines is an alias for `ForEach-Object`. In inline Python scripts or shell strings like `Buy (15% to 30%)`, PowerShell parses `%` as an operator, causing `You must provide a value expression following the '%' operator`.
* **Rule**: Always write Python scripts to `.py` scratch files or ensure `%` is not fed through the PowerShell parser unescaped.

---

### 11. Mock Companion PDFs in Tests (Distinct SHA256)
* **Issue**: Copying an existing PDF via `shutil.copy(pdf_path, pdf2)` creates an identical duplicate with identical SHA-256. Code deduping reports by SHA-256 will treat them as the same report.
* **Rule**: Append a trailing comment to create distinct hashes without corrupting PDF format:
  ```python
  pdf2.write_bytes(pdf1.read_bytes() + b"\n%companion_dummy\n")
  ```

---

### 12. Core Function Signatures in `section_capture` & `workflow`
* **`PdfSource(path)`**: Accepts only `path` in `__init__`. Set `source.doc_type` and `source.period` as attributes after instantiation.
* **`load_questions_ledger(sha256, questions_root=...)`**: Uses `questions_root` (not `db_path`) to resolve the database directory.
* **`upsert_report(sha256=..., filename=..., original_path=..., ...)`**: Takes explicit keyword/positional fields (`sha256`, `filename`, `original_path`, `byte_size`, `physical_page_count`, `doc_type`, `period`, `db_path`), not a `PdfSource` object.
* **`build_stage2_prompt_content(...)`**: Takes `(stage1_content, company_title, ticker, detected_sector, sens_announcements=None)` — does not take `filename`.


---

### 13. `git add` After `git rm` Gotcha
* **Issue**: Passing a file already deleted via `git rm <path>` into a subsequent `git add <path> <other_files>...` causes `fatal: pathspec '<path>' did not match any files` and aborts staging for all `<other_files>` in that command.
* **Rule**: Do not re-pass `git rm`-deleted paths to `git add`; only pass modified or untracked files to `git add`.
