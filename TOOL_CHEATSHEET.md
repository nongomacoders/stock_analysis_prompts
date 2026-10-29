# Agent Tooling Cheatsheet & Gotchas

Keep interventions fast, lean, and error-free on Windows + PowerShell.

---

### 1. PowerShell & Python One-Liners
* **Quote stripping issue**: Windows PowerShell 5.1 swallows inner double quotes in BOTH `python -c "..."` and single-quoted `python -c 'print("hello world")'` when the inner string contains spaces (turning `"hello world"` into bare tokens `hello world` and raising `SyntaxError: '(' was never closed`).
* **Bracket / type literal parsing**: PowerShell treats unquoted brackets like `print([c[1] for c in ...])` inside command strings as attribute or type literal expressions, throwing `Missing ] at end of attribute or type literal`.
* **Multi-line parser error**: Running multi-line `python -c "..."` causes `ScriptBlock should only be specified as a value of the Command parameter`.
* **Windows Charmap / Unicode error**: PowerShell defaults to `cp1252`. Printing Unicode characters like `⚡`, `✓`, or emojis crashes Python with `UnicodeEncodeError: 'charmap' codec can't encode character...`.
* **PowerShell Ampersand (`&`) error**: An unquoted or double-quote-nested ampersand (`&`) in PowerShell command lines triggers `The ampersand (&) character is not allowed. The & operator is reserved for future use`.
* **PowerShell variable pipe expansion error**: Passing `$var` in double-quoted `powershell -Command "...; $var | ..."` expands `$var` as empty string before sub-execution, leaving bare pipe tokens and triggering `An empty pipe element is not allowed`.
* **Rules**:
  1. Never run SQL strings or nested quotes with `python -c "..."`.
  2. For simple Python one-liners in PowerShell, wrap in single quotes or avoid bracket indexing:
     ```powershell
     python -c 'from section_capture.db import connect_db; print("ok")'
     ```
  3. Set `$env:PYTHONIOENCODING="utf-8"` whenever printing or inspecting text containing Unicode/emojis.
  4. Never run multi-line Python code via `-c`. Put multi-line logic in a scratch `.py` file (e.g. `scratch/run.py`) and execute `python scratch/run.py`.
  5. Path escape sequence gotcha: Windows paths containing `\t` (e.g. `\tmp\...`) in Python string literals evaluate to tab characters (`\x09`). Always use forward slashes (`tmp/...`) or raw string literals (`r'tmp\...'`).

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
* **SQLite Table Schema Gotchas (`analysis.sqlite`)**:
  - `reports` table does NOT contain a `ticker` column. Query/filter by `filename` or `original_path` (e.g. `WHERE original_path LIKE '%NTU%'`).
  - `sections` table uses `section_number` (not `section_index`) for ordering and indexing captures.
  - `sector_guardrails` table uses `enabled` (not `active`) for rule status.

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
* **`section_capture.openrouter`**: `OpenRouterWorker`, `get_openrouter_model()`, and `get_model_display_name()` live in `section_capture.openrouter` (not `section_capture.llm_worker`).


---

### 13. `git add` After `git rm` Gotcha
* **Issue**: Passing a file already deleted via `git rm <path>` into a subsequent `git add <path> <other_files>...` causes `fatal: pathspec '<path>' did not match any files` and aborts staging for all `<other_files>` in that command.
* **Rule**: Do not re-pass `git rm`-deleted paths to `git add`; only pass modified or untracked files to `git add`.


---

### 14. Stock Evaluation Workflow & Output Format Reference
* **Guide**: See [`docs/STOCK_EVALUATION_FORMAT.md`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/docs/STOCK_EVALUATION_FORMAT.md) for the mandatory 5-part user response structure, including the **Valuation Errors Found & Analytical Lessons Learned** section and sector-specific checklist.
* **Evaluation CLI**: Run `.venv\Scripts\python.exe evaluate_stock.py <TICKER> [--period <PERIOD>] [--rerun]`.

---

### 15. Windows CLI UTF-8 Reconfiguration (`UnicodeEncodeError: 'charmap'`)
* **Issue**: Python scripts printing Unicode symbols (`✓`, `⚠️`, emojis) to default Windows consoles crash on cp1252.
* **Rule**: Always configure standard output encoding at script entrypoints:
  ```python
  if hasattr(sys.stdout, "reconfigure"):
      sys.stdout.reconfigure(encoding="utf-8")
  ```

---

### 16. Disk File Regeneration vs Integration Test Assertions
* **Issue**: Regenerating a valuation note on disk causes tests asserting against that note file in `tests/test_portfolio_valuation.py` to fail if expectations contain legacy numbers.
* **Rule**: Synchronize test assertions with regenerated notes, or use mock/simulated fixtures for invariant parser tests.

---

### 17. OpenRouter Remote Socket Drops (`WinError 10054`) & Backoff Retry
* **Issue**: OpenRouter API connections drop during long 70k+ token completions.
* **Rule**: Wrap API requests in an exponential backoff retry loop (up to 3 attempts with 2s, 4s, 8s delay) in `query_openrouter` (`section_capture/openrouter.py`).


---

### 18. JSE Ticker Examination & Ground-Truth LLM Web Search
* **Issue**: Un-grounded LLM prompts asking about 3-letter stock tickers (e.g. `DCP`) hallucinate non-existent entities (e.g. "DCP (Pty) Ltd Construction") instead of authentic JSE-listed companies (Dis-Chem Pharmacies Limited).
* **Fix**:
  1. Use `fetch_jse_company_profile(ticker)` in `section_capture/market_data.py` via `yfinance` (`<TICKER>.JO`) for instant ground truth.
  2. Pass `web_search=True` (`plugins=[{"id": "web"}]`) in `query_openrouter()` and inject verified listing data into `build_ticker_examination_prompt()`.
  3. Maintain fallback synthesis (`_synthesize_profile_response`) so the UI never crashes or returns empty data if OpenRouter drops out.

---

### 19. File Discovery Without ripgrep & Read Output Limits
* **Issue**: Earlier Windows sessions lacked `rg`; availability can change between sessions (it is available on 2026-10-28). Large combined document reads can exceed tool output limits and hide content.
* **Rule**: Check `Get-Command rg -ErrorAction SilentlyContinue` and prefer `rg` when available. Otherwise fall back to `Get-ChildItem` with explicit file filters, excluding dependency directories. Read Markdown in small batches with `Get-Content -Encoding utf8`, and re-read any truncated portions. When returning different PowerShell object shapes in one invocation, serialize each with `ConvertTo-Json -Compress` or format each group explicitly: automatic table formatting may use the first object's columns and silently render later objects as blank rows.

### 20. PDF Rendering When Pillow's Native Extension Is Unavailable
* **Issue**: `pypdfium2` text extraction works, but `bitmap.to_pil()` fails if the local Pillow installation cannot import `PIL._imaging`.
* **Rule**: For read-only visual checks, render with `page.render(rev_byteorder=True)` and copy the bitmap buffer (`bitmap.buffer`, not `get_buffer()`) into an existing PySide6 `QImage` using its width, height, stride and matching RGB888/RGBA8888 format. Save the PNG with `QImage.save()`. Explicitly close bitmap, page and document handles before cleanup.

### 21. Distinguish Patch-Tool Failures from Filesystem Denials
* **Issue**: In this Windows session, `apply_patch` returned "Failed to write file" for workspace Markdown, while an ordinary authorized PowerShell write to the same file succeeded. A generic patch failure alone does not establish an ACL or sandbox denial.
* **Rule**: Inspect the exact error and verify the normal authorized file-writing path before diagnosing permissions. When no explicit policy denial is reported, use `[System.IO.File]::WriteAllText` with UTF-8 without BOM, exact-match guards, and preserved line endings for routine workspace edits. Never change ACLs or bypass an explicit denial. Check the diff afterward; do not repeatedly ask the user to restart based on an unverified diagnosis.

### 22. Replaying Audit Calculation Scripts Can Modify Original Evidence
* **Issue**: An evaluator's saved reconciliation script may contain hard-coded writes to its original audit output and even to its own source file. Running a copied script can therefore overwrite the original evaluation despite executing from another directory.
* **Rule**: Inspect saved scripts for write paths and side effects before replaying them. Preserve originals and independently reproduce relevant calculations into a new evaluation run. Do not run an untrusted audit script merely to verify its printed calculations.

### 23. Keep Completion Writes Separate from Cleanup Commands
* **Issue**: A combined command containing documentation writes and recursive temporary-directory cleanup was rejected before execution because sandbox approval was disabled. Earlier non-destructive writes succeeded.
* **Rule**: After a pre-execution rejection, do not assume any preceding statements ran. Save authorized non-destructive completion records separately, report blocked cleanup accurately, and do not route denied deletion through another tool or shell to bypass the approval boundary.

### 24. Stage Reasoning Requires Explicit API Settings and Answer Headroom
* **Issue**: The OpenRouter client hard-coded `reasoning.effort=none`, so changing a provider UI preference would not enable reasoning in Stage 1/2. Raising effort while retaining a small completion limit can also exhaust the shared reasoning/final-answer budget; raw reasoning or a partial final answer must not be saved as a completed report.
* **Rule**: Pass reasoning effort explicitly per analysis stage, retain it through retries/provider fallback, allocate completion headroom and record requested effort versus reported reasoning tokens separately. Reject `finish_reason=length` even when partial content exists and never substitute a reasoning field for missing final content. Check current official API documentation rather than assuming a provider's effort vocabulary. Preflight exact-match edit counts before writing: similar GUI stage log strings may occur a different number of times than expected.


### 25. Process Polling Can Encounter Approval Review After Initial Dispatch
* **Issue**: A long-running tool invocation returned a session and created local evidence, but a later `write_stdin` output poll was rejected by automatic approval review for an external-data upload. The status file still said running after the session disappeared. Never infer that no transmission occurred just because the poll was rejected, or that stale status proves an active run.
* **Rule**: Do not retry or route the upload through another mechanism. Preserve local evidence, attempt safe cancellation, record transmission/completion/exit-code uncertainty, and obtain the explicit payload/destination approval required by the reviewer before resuming. Separate public endpoint reachability from authenticated payload authorization.
* **Process inspection**: `Get-CimInstance Win32_Process` may report unavailable CIM access even when its enclosing command exits 0. Inspect errors and do not interpret an empty filtered result as proof no process exists; use an allowed read-only process listing where possible.


### 26. Managed HTTPS Proxy and Host-Level Telemetry Review
* **Issue**: A process-local network guard that allowed only remote OpenRouter IPs blocked the environment-owned loopback HTTPS proxy. Its port changes between tool invocations, so hard-coding a port caused a separate assertion failure before execution.
* **Rule**: Retain the managed proxy, read its exact loopback address/port in the executing process, and constrain the external request URL independently. Never disable or bypass the managed proxy to work around a denial. Avoid treating arbitrary proxy-scheme environment entries as actual endpoint destinations.
* **Approval review**: Even a guarded Python runner may encounter a reported host Visual Studio telemetry gate. Inspect application request code before assigning causation; distinguish the reviewer's report from an independently observed endpoint/payload. OpenRouter-only user approval does not approve an unrelated destination. If a safer restriction does not resolve the gate, preserve evidence, stop retries and report the specific blocker. Stale running status and missing final process output do not prove no transmission/billing.


### 27. Request Hashes with Embedded PDF CRLF and Unicode Headings
* **Issue**: Stage2 prompt text contains PDF-extracted CRLF; Windows text-mode saving adds another CR, and universal-newline readback does not reconstruct the exact submitted string. A normal read/hash assertion can fail despite an unchanged prompt. Tool-rendered output may also display Unicode em dashes like ASCII hyphens, breaking exact heading parsers.
* **Rule**: Preserve raw file hashes separately from request-string hashes. Verify by reversing exactly the known single Windows write translation (`raw.decode('utf-8').replace('\r\n','\n')`) and checking the recorded request hash; do not broadly strip CR or rewrite originals. Inspect heading codepoints or normalise punctuation in the analysis parser only. Preserve inputs unchanged and record any initial failed assertion/parser run and final exit code.


### 28. Resuming Interrupted Edits and Offline Regression Tests
* **Issue**: The execution host disconnected before a combined edit/test command began. On reconnection, old failures remained. Exact-match preflights also exposed rendered emoji mismatches and incorrect variable names; an AST fixture edit decoded raw CRLF before Windows text writes, creating doubled line breaks and a misplaced future import.
* **Rule**: Verify actual files after a pre-execution transport failure; never assume edits ran. Match real source text/codepoints, keep changes bounded, normalize source newlines before text writes, and place imports after `from __future__`. Inspect each terminal result rather than treating a shell exit as proof every earlier operation succeeded.
* **Offline test alternative**: If approval review reports unexplained telemetry, do not retry the same network-capable test process. Inspect relevant project/profile code first. A materially safer local test session can opt out of runtime telemetry and load a pytest plugin before collection that denies Python DNS/connect/sendto events. Preserve the actual result/exit code; host telemetry and source financial truth are not established by a passing suite. `workflow/changes/20261028_valuation_withholding/offline_pytest_plugin.py` preserves the plugin used for178 passing regressions.

### 29. SQLite Read Helpers, Literal Quotes and Live Runner Revisions
* **SQLite inspection side effects**: Application read helpers may call schema migrations. Repeated `INSERT OR IGNORE` into an AUTOINCREMENT table can advance `sqlite_sequence` even when business rows are unchanged. Integration tests must use a SQLite backup in their temporary workspace, not an explicit production database path. If a file hash changes, compare logical tables read-only before concluding valuations changed; preserve the observed difference rather than restoring the file wholesale.
* **Evidence quotations**: PDF line wrapping can make a literal quotation differ only in whitespace. Normalize whitespace for presence checks, preserving words, numbers and signs. Paraphrases and invented quotations still fail; retain questions and original rejected outputs. A locally retained open question is not a successful model answer.
* **Long-running script revisions**: Editing a script while an earlier version is running can make displayed traceback source lines differ from the executing code. Preserve dispatch-time runner revisions and exact requests/receipts; do not infer which revision ran from the current file alone. Resume from saved outputs instead of repeating completed paid calls.

### 30. Pilot Live Protocols Before Broad Reruns; Telemetry Startup Scope
* **Trial scope**: Validate captured failures offline, then run a one/two-section live pilot before dispatching full company comparisons. Report the expected section/call count. One repair is sufficient to expose a recurring contract problem; stop the broad trial for diagnosis instead of maintaining live repair/budget-escalation loops. Use targeted tests during small fixes and the full suite at a coherent milestone.
* **Telemetry opt-out timing**: `DOTNET_CLI_TELEMETRY_OPTOUT=1` and `POWERSHELL_TELEMETRY_OPTOUT=1` request opt-out. PowerShell requires its variable before the shell process starts; setting it inside an exec command does not establish disabled startup telemetry. Python socket-denial hooks cover Python, not the host shell. Attribute a delay to telemetry only with observed timing/approval/network evidence, not because the variable name appears in a command. Do not change machine-wide settings or bypass the managed proxy on suspicion.
* **Evidence**: `workflow/changes/20261028_workload_reliability/delay_retrospective.md` records 141 successful responses (44 repairs), DCP's approximately 54-minute trial and timing limitations. Earlier telemetry interruptions are separate incidents.

### 31. Bound Windows Audit Inspection Commands
* **Issue**: An inline PowerShell/Python SQL inspection broke nested quotes; a scratch read without UTF-8 failed on preserved Unicode. Passing `section_capture/*ledger*` directly as an rg path produced a Windows filename error even though the enclosing command later exited 0.
* **Rule**: Put nontrivial Python/SQL in a saved script, explicitly use UTF-8 for JSON/text evidence, and pass exact rg paths or a directory with `-g` filters. Inspect inner errors, not just the final shell exit. Reopen truncated evidence in small batches; record only pages and files actually examined.

### 32. Persist OpenRouter Accounting Before Rejecting a Completion
* **Issue**: Completion-limit errors previously discarded generation IDs/usage, leaving failed-call costs unknown. In the NTU default-thinking pilot, all32,768 completion tokens were reported as reasoning with no final answer; the failed call still costUSD0.016893918. Immediate generation-metadata lookups also returned404 before the same records became available later.
* **Rule**: Persist generation ID, finish reason, usage/cost and client timing before completeness or ledger validation. Streaming usage arrives at the end; never save raw reasoning as an answer. Reasoning tokens are included in completion tokens, not added again. Retain failed/repair calls in totals; unavailable costs remain unknown. Retry delayed metadata reads separately, without resubmitting a paid completion. Preserve the managed proxy and never log credentials.
* **Default settings**: Query and save the model catalog. For DeepSeek's current snapshot, omitted reasoning controls leave default thinking enabled/high; “default” must not be assumed to mean medium or disabled. Removing `:nitro` is distinct from choosing a reasoning effort. Record provider/account routing effects and any prompt revisions before comparing performance.

### 33. Logical Capture Boundaries and Multi-Package Fixtures
* **Mixed fonts**: A note number/title can use a larger font than its “continued” suffix, while a large number can also sit beside small table-column labels. Inspect word-level font/position evidence; do not let either pattern silently create/drop a heading. A numbered subnote can start halfway down a page and continue on the next page; keep the shared page whole and record the dependency.
* **One-to-many API**: `auto_capture_section` returns the first saved package while saving every part. Fixtures representing completed cached work must mark every saved package complete, not just the return value. Tests isolating stage orchestration can mock the capture plan, while dedicated tests verify full-page coverage/overlap handling against real PDFs.
* **Layout fixtures**: Keep synthetic heading coordinates outside synthetic body-text rows. Geometrically overlapping text can merge into one mixed-font line and invalidate a test of heading detection; compare with the real PDF before weakening detection rules.
* **Patch verification**: A multi-file patch failed verification in this turn and wrote none of its proposed changes. Re-read the affected files before retrying bounded hunks; do not assume earlier hunks applied or diagnose a permission problem from a context mismatch.

### 34. Pilot Scope, Resolved Questions and Uncapped Upstream Limits
* **Whole-page scope**: A model can ignore a secondary note even when the entire page is captured and ledger quotations validate. Keep a compact list of native note starts,including those lower on shared pages,in the brief prompt. Test actual secondary-content coverage; page presence alone is insufficient. NTU p.25 initially lost currency risk; a focused scope recheck fixed it.
* **Question reuse**: An open-only prompt omits resolved questions,so the model may recreate them under new wording. A short resolved-ID/question index can discourage this without repeating long answers. Preserve old duplicates and reopen original IDs only against contradictory evidence; exact-text deduplication is not semantic deduplication.
* **Chronological trials**: Use a separate pilot database. Do not import later-section pilot resolutions into a supposedly fresh source-order full run. Intentional repeated pilot/full calls need separate cost accounting.
* **No caller cap is not unlimited**: The reviewed NTU Stage2 request omitted token-limit fields but still stopped at131,072 completion tokens,all reasoning. Record the observed upstream limit;do not claim which provider/router/account setting imposed it without evidence. A successful previous uncapped call does not guarantee completion. Preserve the failed cost/ID and avoid automatic paid escalation.
* **Final progress state**: A focused recheck can leave a transport status marked running after its last response. Finalize phase status separately from raw receipts;do not infer an active process from stale status.

### 35. Explicit Cap Experiments and Midstream Provider Failures
* Preserve identical request messages and all other controls when testing a larger token cap; compare actual providers. An initial HTTP200 can later contain an SSE502 provider_unavailable; null finish reasons are not length. Record no final answer and preserve accounting before interpreting failure. NTU300k passed131072 but failed at183036 reported reasoning tokens. Do not infer which default imposed the old cutoff or why the provider failed.
* Metadata after a failed stream can report zero cost; retain its source and timestamp, refresh metadata separately without another completion, and distinguish reported accounting from invoice verification. Preserve transient404 history after successful metadata retrieval.
* This turn repeated oversized document reads; section19 already covers bounded reads. No shell/encoding/edit failures were observed; the live command exit1 was a provider-stream failure, not a local permission error.

### 36. Preserve Live Results When a Documentation Write Fails
* The Fireworks generation succeeded, but the first offline closure failed with Python OSError22 Invalid argument while opening workflow/STATE.md. The file remained intact; a staged candidate applied successfully through native PowerShell WriteAllText. A closure-write failure does not invalidate a saved generation or justify another paid call. Preserve actual command exit codes and finish independent checks separately; no policy denial was reported.

### 37. Shared Templates, Ticker Filters and Transport Bookkeeping
* A full-manifest LIKE '%PAN%' also matches words such as COMPANY. Use it only to find candidates;verify the source's actual ticker/path component before selecting company evidence. The section-prompt pilot corrected its candidate filter before dispatch.
* When output Section4 becomes the final section,a regex that stops only at Section5 leaves the legacy ledger instruction in place. Accept end-of-template too,and test the assembled common task plus sector notes rather than individual hint files.
* Reused trial transport code may hard-code bookkeeping such as reasoning_controls_sent=false or a model-default label. Verify actual saved HTTP requests after wrapping payload construction. Preserve original receipts before normalizing incorrect derived fields;never change provider usage or raw model answers to match the intended configuration.

### 38. Flatten Nested Audit Copies Before Windows Path Limits
* Recursively copying an evaluation's already-preserved baselines under another long timestamped company path can fail with WinError206. Preserve files under short numbered filenames and record exact original-to-copy paths/SHA in a manifest;do not repeatedly nest the same directory hierarchy. Mark a partial preparation incomplete and link the successful review instead of claiming it finished.
* Python reserved words cannot be used as dict keyword arguments (`dict(pass=...)`). Use a descriptive field such as pass_example or a quoted-key dictionary. Preserve failed/actual final exit codes separately;an audit-generation script failure is not a model/provider failure.

### 38. PowerShell 5.1 Date Formatting, Unicode Character Mapping, and Variable Escaping
* **`Get-Date -AsUTC` parameter error**: In Windows PowerShell 5.1, `Get-Date` does not support `-AsUTC` (which is a PowerShell Core 7+ parameter). It throws `NamedParameterNotFound: A parameter cannot be found that matches parameter name 'AsUTC'`. Use `(Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")` for consistent UTC timestamps.
* **Charmap encoding on Unicode arrows (`→`)**: When inspecting model outputs containing right-arrow indicators (`\u2192` / `→`) or other non-Latin-1 characters, Python scripts in PowerShell default to `cp1252` and crash with `UnicodeEncodeError: 'charmap' codec can't encode character '\u2192'`. Always include `sys.stdout.reconfigure(encoding='utf-8')` at the entry point of inspection scripts or set `$env:PYTHONIOENCODING="utf-8"`.
* **PowerShell string variable escaping**: In double-quoted PowerShell command lines, writing `\$_.FullName` causes PowerShell to treat `\` as a bare token and fail with `CommandNotFoundException: The term '\.FullName.Substring' is not recognized`. Use a dedicated Python scratch script for file iteration rather than complex inline PowerShell scriptblocks.

### 39. Live Section Completion and Atomic Ledger Rejection
* A completed generation is not an accepted ledger update. The app rejects an entire structured delta when one evidence quote fails,including otherwise valid updates and new questions. Preserve raw briefs/unapplied deltas,prove rejected before/after state is unchanged,and report generation and ledger counts separately. Do not silently count raw proposed closures as persisted or infer that the cited financial claim is false from a format mismatch.
* Probe live-run status/receipts before opening output files;an output may not exist until the stream finishes. A premature Get-Content can return shell exit1 even with ErrorAction SilentlyContinue. This is not an API transport failure and does not authorize resubmission.

### 40. Native Extraction Review and Metadata Refresh
* In this local venv, pdfplumber Page.to_image fails because PIL._imaging is unavailable. Render with pypdfium2 bitmap buffers and PySide6 QImage, closing PDF/page/bitmap handles; do not reinstall dependencies or rerun model calls for a rendering failure.
* Pass Windows rg directory paths plus `-g '*.py'`; literal wildcard path arguments can produce OS error123. Avoid broad JSON Select-String when a matching field contains an entire embedded prompt; parse and print only the required record.
* Transport metadata status is `retrieved`, not `available`. A closure-script assertion using the wrong status failed despite successful calls; inspect the saved schema. Three initial metadata lookups were unavailable and later read-only refreshes succeeded. Preserve initial receipts, refresh accounting only, and distinguish generation success, literal ledger validity and semantic correctness.
* Large combined reads still truncated this turn. Recover bounded result JSONs/session outputs; truncation is not evidence that a command failed or completed. This turn's initial source regression failure revealed real prose/header leakage; fix extraction rather than weakening literal evidence tests.

### 41. UTF-8 Input Decoding During Review
* `sys.stdout.reconfigure(encoding='utf-8')` only fixes output encoding. On this Windows Python, `Path.read_text()` without an explicit encoding can decode UTF-8 model files as cp1252 and display mojibake while exiting0. Always use `read_text(encoding='utf-8')` (or `utf-8-sig` for BOM JSON). A diagnostic display error does not justify rewriting original evidence; hash and preserve originals, then decode correctly. The native-extraction review scripts already specify input encodings; one inline inspection omitted it and was corrected.

### 42. Distinguish Short Quotes From Literal Mismatches
* The ledger validator's generic `not literal` error covers both quotes shorter than8characters and failed text matches. In the clarification pilot, `3 414`, `3 845` and `431` were literal but too short; the first error rejected the entire delta. Diagnose length and normalized matching separately without changing the validator or silently accepting the delta. Record all offending quotes for review; do not infer PDF corruption or financial invalidity from this message alone. All pilot commands exited0; no shell/encoding/edit failures or paid retries occurred.

### 43. Preserve Partial Multi-Pass Experiments After HTTP429
* The three-pass experiment's seventh request returned HTTP429Too Many Requests before content, generation ID or usage; six earlier calls succeeded. Stop-on-error left PAN final failed and its fresh single baseline undispatched. Record planned/dispatched/completed counts, failed billing unknown and incomplete arm separately; do not fill gaps from older baselines or treat a missing answer as an accuracy failure. The status code does not identify which router/provider/account quota applied. No automatic paid retry; any later authorized continuation should preserve successful passes and pending request rather than rerun them.
* Complete the independent review/accounting despite generation exit1; metadata refresh needs no inference. Initial derived receipt flags can be wrong even for an HTTP failure: preserve them and normalize from exact saved request fields. Tool review found no local shell/encoding/edit failures; repeated overlarge combined reads still truncated and should be bounded more tightly.

### 44. Escaped Path References Can Corrupt Markdown
* A supplied STATE entry contained BEL in `audit.md` and form feed in `findings.json`,consistent with escaped `\a`/`\f` in a Python string. Preserve the original document before repairing those references; use forward-slash paths,raw strings or Path objects and explicit UTF-8. This review repaired only the two continuity-document references; original Gemini files remain untouched. Preparation/review/repair commands exited0,no local command errors or paid calls; bounded reads are still needed to avoid repeated truncation.

### 45. Git Metadata Permissions During Requested Commit/Push
* This workspace permits project writes but mounts `.git` read-only in the default sandbox. `git fetch origin` failed opening `.git/FETCH_HEAD`; the same user-authorized fetch succeeded with `require_escalated`. Use the escalation mechanism for requested Git metadata mutations rather than changing ACLs or repeatedly retrying the default sandbox. This was a filesystem permission boundary,not an API/model or test failure; automatic approval allowed the escalation.
* Git autocrlf emits thousands of LF/CRLF warnings for newly staged audit files and can change evidence bytes on checkout. `.gitattributes` now marks company evaluation records and workflow change records `-text`; re-stage those records with `--renormalize` and verify staged blob hashes match working files. Do not rewrite raw evidence or disable normalization globally to silence warnings.

### 45. PySide6 QApplication Lives in QtWidgets, Not QtGui
* Rendering snippets copied from older scripts import `QApplication` together with `QImage` from `PySide6.QtGui`. On this venv that raises `ImportError: cannot import name 'QApplication' from 'PySide6.QtGui'` on the very first rendering helper of the turn (observed twice in one review). Split imports: `from PySide6.QtGui import QImage` plus `from PySide6.QtWidgets import QApplication`. Keep the existing pattern `app = QApplication.instance() or QApplication([])` so a test/agent-created instance is reused; dispose any windows created by test helpers after rendering.
* A venv-launched interpreter can still print the base `Python313` install path in tracebacks (`File "C:\...\Python\Python313\Lib\pathlib\..."`) because venv `python.exe` forwards to the base launcher; this is cosmetic. Do not conclude the script ran outside the venv or that site-packages resolution failed because of it — failed scripts still matched the repository's `.venv` PySide6 in the import error above.

### 46. Git Worktrees for Parallel Work Directions
* The OpenCode built-in `worktree_create` tool can fail outright ("Unable to create worktree") with no diagnostic. Fall back to plain git: `git worktree add -b <branch> <short-sibling-path>` then `git worktree list` to confirm. Keep the worktree path short and shallow (a sibling folder, not nested inside the repo) — this is the same WinError206/long-path discipline as evaluation baselines.
* `git worktree add` on this repo emits `warning: unable to access '...Filename too long'` for the deep pre-existing pilot prompt file (`.../inputs/implementation/prompts/consumer_lending/12-analyst-reading-brief/v1.1.0/.gitattributes`). It did not stop the checkout (4838 files, exit 0). Do not treat it as a broken clone; verify the specific file separately only if it is actually needed. `.gitattributes` being absent does not affect text-file usage within a worktree.
* Keep all branch-local documentation edits (worktree's `workflow/STATE.md`, `TOOL_CHEATSHEET.md`) committed to the feature branch, never dangling uncommitted in the main checkout, so `one_shot`/`main` stays pristine while a direction is being drafted.

### 48. Reconciliation Suite & Arithmetic Gate Engineering (PAN D009 P2 build)
* **Never read the scoring fixture**: In an agentic build, the test suite must be derived strictly from the database/schema and company report geometry. An automated test should enforce that the suite source code never mentions the fixture filename (`pan_d009_expected.json`), ensuring the suite is a deterministic referee, not a test answering key.
* **Exact arithmetic vs tolerance**: For printed integers and exact column sums, arithmetic assertions must be exact (`tolerance=Decimal(0)`). Cross-currency checks (e.g. ZAR/kg vs US$/oz via average exchange rate and physical conversion `32.150747` oz/kg) inherently involve rounding in printed rates (16.90 vs 18.17) and should use a bounded relative tolerance (`0.75%`) with documented rationale.
* **PowerShell `-c` escaping traps**: Inside Windows PowerShell 5.1, executing complex python one-liners with double quotes inside `-c "..."` consistently produces `Missing property name after reference operator` or string truncation. Always write probes or inspection utilities to a temporary `.py` script (e.g. `C:\Users\diond\AppData\Local\Temp\opencode\*.py`) with `sys.stdout.reconfigure(encoding="utf-8")` and run the script file.
* **Conflict recording is the gatekeeper**: A reconciliation gate passes when every printed mismatch is explicitly captured in the `conflicts` table with citations, deltas, and links to open ledger questions. Mismatches must never be papered over or silently omitted.
