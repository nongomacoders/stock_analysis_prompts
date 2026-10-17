# Active prompts

Prompts are versioned under `prompts/<sector>/<stage>/<version>/prompt.md` and assembled automatically by `section_capture/packages.py` when saving a section pack.

| Prompt | Version | Role |
| --- | --- | --- |
| `mining/00-report-orientation` | `v1.0.0` | Orient the LLM with the coarse major-section map of the PDF so it knows where the current selection fits and which sections follow. |
| `mining/12-analyst-reading-brief` | `v1.1.0` | Instruct the LLM to summarize important points from the captured section, challenge consequential claims, and advise specific verification checks (`Pending: [section]`) for upcoming sections. |
