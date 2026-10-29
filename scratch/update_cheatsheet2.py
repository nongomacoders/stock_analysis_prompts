from pathlib import Path

p = Path("TOOL_CHEATSHEET.md")
content = p.read_text(encoding="utf-8")

old_text = "  4. Never run multi-line Python code via `-c`. Put multi-line logic in a scratch `.py` file (e.g. `scratch/run.py`) and execute `python scratch/run.py`."
new_text = """  4. Never run multi-line Python code via `-c`. Put multi-line logic in a scratch `.py` file (e.g. `scratch/run.py`) and execute `python scratch/run.py`.
  5. Path escape sequence gotcha: Windows paths containing `\\t` (e.g. `\\tmp\\...`) in Python string literals evaluate to tab characters (`\\x09`). Always use forward slashes (`tmp/...`) or raw string literals (`r'tmp\\...'`)."""

if old_text in content:
    content = content.replace(old_text, new_text, 1)
    p.write_text(content, encoding="utf-8")
    print("TOOL_CHEATSHEET.md updated successfully")
else:
    print("Target text not found in TOOL_CHEATSHEET.md")
