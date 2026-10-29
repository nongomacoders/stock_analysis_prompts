# Fireworks adoption and current section-prompt inspection

Authorized change: user chose Fireworks as the DeepSeek provider. Shared client
restricts DeepSeek requests to Fireworks with provider fallback disabled and
parameter support required. Default model uses base slug. Other model routing and
existing stage reasoning/token controls remain unchanged. No paid requests made.

Offline verification:21 API tests passed in8.97s,exit0; Python DNS/connect/sendto
denied. Test-created process/Qt state disposed at process exit; unique temporary
test directory and temporary result file cleaned with native PowerShell,exit0.
Saved result:test_result.json. Existing worktree changes retained.

Prompt inspection:
- PDF heading/text extraction and capture splitting are local,not a DeepSeek call.
- App section analysis uses packages.build_prompt and the appropriate sector's
  12-analyst-reading-brief/v1.1.0/prompt.md.
- Current consumer-lending template requests:no narrative summary; answer related
  earlier questions; inspect footnotes/qualifications; propose future questions;
  update the ledger; retain factual forecast inputs; suggest the next section.
- New capture contracts replace the copy-all-ledger output with one JSON delta,
  stable IDs and literal current-page evidence; omitted questions remain stored.
- Context appends report map,coverage/continuations,physical pages,source hash,
  relevant ledger questions,analyst focus and selected evidence.
- Consumer-lending checklist includes originator staging/coverage/NIM/regulatory
  caps/ABS prompts. Their applicability is not established merely by sector.
- Compact prompts with run-specific lessons/secondary-heading lists in recent
  NTU experiments are separate from the app's production template.

No extraction/prompt/sector-guardrail changes made. User preference recorded:
effective across companies,simple extraction,and acceptable imperfect first-pass
analysis. A concise common task plus applicable sector hints is a possible next
revision,not an implemented change.

Tool retrospective:oversized combined reads required bounded follow-ups,already
covered by TOOL_CHEATSHEET section19. Git reported its usual LF/CRLF conversion
warning. No shell,encoding or editing failures occurred; no new tooling pattern
required a cheatsheet amendment. Source PDFs,original model outputs and production
SQLite were not written by this work.

Follow-up extraction trace:found optional llm_cluster_presentation_sections uses a
direct OpenRouter request outside the shared client. Added the same Fireworks-only
provider object there. Ordinary report boundary detection uses bookmarks and
native headings;presentations may first ask DeepSeek to group slide titles/snippets.
No extraction logic or prompts changed. Added a mocked check of the separate route;
22 API tests passed in8.76s,exit0,network denied. Actual result saved in
presentation_test_result.json;unique temporary folder/result file cleaned,exit0.
No new shell/encoding/edit errors;no new tooling pattern to add to cheatsheet.
