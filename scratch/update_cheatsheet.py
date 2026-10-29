from pathlib import Path

p = Path("TOOL_CHEATSHEET.md")
content = p.read_text(encoding="utf-8")

new_section = """
### 38. PowerShell 5.1 Date Formatting, Unicode Character Mapping, and Variable Escaping
* **`Get-Date -AsUTC` parameter error**: In Windows PowerShell 5.1, `Get-Date` does not support `-AsUTC` (which is a PowerShell Core 7+ parameter). It throws `NamedParameterNotFound: A parameter cannot be found that matches parameter name 'AsUTC'`. Use `(Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")` for consistent UTC timestamps.
* **Charmap encoding on Unicode arrows (`→`)**: When inspecting model outputs containing right-arrow indicators (`\\u2192` / `→`) or other non-Latin-1 characters, Python scripts in PowerShell default to `cp1252` and crash with `UnicodeEncodeError: 'charmap' codec can't encode character '\\u2192'`. Always include `sys.stdout.reconfigure(encoding='utf-8')` at the entry point of inspection scripts or set `$env:PYTHONIOENCODING="utf-8"`.
* **PowerShell string variable escaping**: In double-quoted PowerShell command lines, writing `\\$_.FullName` causes PowerShell to treat `\\` as a bare token and fail with `CommandNotFoundException: The term '\\.FullName.Substring' is not recognized`. Use a dedicated Python scratch script for file iteration rather than complex inline PowerShell scriptblocks.
"""

if "### 38. PowerShell 5.1 Date Formatting" not in content:
    content += new_section
    p.write_text(content, encoding="utf-8")
    print("Appended section 38 to TOOL_CHEATSHEET.md")
else:
    print("Section 38 already present")
