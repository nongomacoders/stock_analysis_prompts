# Native extraction fix: limited independent audit

Evaluator: Codex. Recorded 2026-10-28T18:29:39.165999+00:00; local timezone Africa/Johannesburg (UTC+02:00).
Decision: **extraction improvement supported within selected coverage; model corrections still required**. Section-only engineering pilot; no valuation requested or validated.

## Implemented change
Numeric body anchors and native vertical rules separate nearby cells, wrapped headings map by overlap, broad prose is excluded from column inference, and paragraphs are emitted as prose. No company-specific extraction rules. The ledger prompt asks for short literal cell/sentence anchors; apply_delta and its atomic validation are byte-for-byte unchanged from the preserved function baseline. No dependency additions.

## Evidence and measurements
Original NTU and PAN PDF SHA-256 verified before export and after generation. Full-page before/after corpus: NTU9,13,18,22,24,25,30,31; PAN4,38,39,48,49,50. Offline extraction coverage is not full financial verification. Independently viewed original physical NTU22,24,25 and PAN48,49 this turn; retained renders in workflow/changes/20261028_table_extraction/renders. Read new answers and validation states for all five samples. NTU13/21/23/31 and PAN50 checked as extracted text, not newly visually audited. Unread remainder and external disclosures are NOT VERIFIED. Prior review/source images remain preserved.

All five selected calls complete, all five deltas syntactically/evidentially valid. Fireworks only, DeepSeek deepseek/deepseek-v4.1-flash-1017, reasoning none/excluded, max16384, temperature0.1. No fallback, paid repair or Stage1/2. Incoming NTU ledger states and capture bounds reused from saved baseline; independent cases do not feed each other. PAN baseline predates additional prompt refinements. Both extraction and anchor instruction changed, so benefits cannot be attributed to either in isolation.

Cost USD 0.0199752336; input 41078; completion 14468; reasoning 0; cached input 3908. Summed request time 69.952s; first dispatch through last accounting 98.782372s. Five unique IDs and all generation metadata available. Cost is API-reported, not invoice verification. See metrics.json, calls.csv, exact requests and receipts.

## Confirmed benefits and remaining analytical errors
NTU22 now keeps5/390 separate:5+390+3845+644=4884. NTU25 comparative FX dates are correct in new answer. NTU13 prose delta now validates, signed roll-forwards correct. NTU24 wrapped headers are improved, but answer still mislabels impairment loss as release; do not promote its earnings interpretation. PAN nearby tailings cells are separate, but grouped headers remain imperfect and model still double-counts1081oz in FY25. Correct disjoint sum92643+2654+98636+1081+1513=196527. No issuer fault established. Some literal-valid answers overstate ledger closure or invent likely explanations; findings.json records these separately from generation/validation success.

## Verification and preservation
Targeted tests: initial53passed(exit0); expanded run58passed/1failed(exit1), exposed genuine paragraph-ending/header leakage; corrected extraction; rerun59passed(exit0). Full offline suite232passed(exit0), DNS/connect/sendto denied. Six real-PDF regressions cover columns, wrapped headers, comparative dates, prose anchors, parentheses and dense PAN numeric cells. See saved result JSONs. New corpus exported after final code change. No new code changes after passing suite.

Production SQLite tables, source PDFs and baseline files unchanged (preservation.json). Original responses, incoming states and code snapshots retained. No guardrail SQL writes. Existing valuations preserved. No full report rerun, financial forecasts, current quote, Stage1, Stage2, or valuation readiness verified.

## Handoff
Use gemini/review_prompt.md in Antigravity. Review every new output, the same original sources, before/after text and ledger closure conditions. Prioritize remaining sign/overlap errors before requesting another paid trial. No additional analytical guardrails implemented; the sign and scope lessons overlap existing guidance. No embedding matcher, partial acceptance or fuzzy quote validation added.
