# DeepSeek workload review

Date: 2026-10-28 (Africa/Johannesburg).
Scope: offline inspection of the current pipeline, sector section prompts, saved section metadata and the preserved NTU max-reasoning comparison. This is a workload/design review, not a new company valuation or independent financial validation. Findings below are proposals; no production prompts, guardrails, ledger entries, database rows or valuations were changed. No network requests or model calls were made.

## Main finding

DeepSeek is asked to do too much bookkeeping and presentation alongside difficult evidence interpretation, with uneven task sizes and weak handoff validation. Improve the evidence flow and allocation of work before increasing reasoning everywhere or adding more instructions. The goal is fewer recurring errors, not merely shorter answers or lower token use.

## What runs today

| Step | Input and task | Current request policy |
| --- | --- | --- |
| Presentation mapping, when enabled | Slide titles/snippets; group into coherent sections | Separate HTTP path; not the section/Stage 1/2 worker |
| Section analysis | Sector template, report map, current capture, entire open ledger; answer questions, inspect footnotes, generate new questions, rewrite ledger, list baseline inputs and choose next section | Worker defaults: reasoning `none`, 16,384 completion tokens, 180-second timeout |
| Stage 1 | Captured text/tables plus section responses, final ledger and applicable guardrails; accounting determinations and unresolved issues | `max`, 65,536 combined reasoning/final-answer ceiling, 900 seconds |
| Stage 2 | Stage 1 response, applicable guardrails, reference price and full extracted PDF/SENS text; forecasts, valuation, sensitivity, publication checks and formatted research note | Same Stage 1 request policy |
| SENS update | Existing note/Stage 1 plus new announcements; revise affected forecasts and valuation | Same Stage 1 request policy |

A fresh full run has optional mapping calls, one call per queued section, then Stage 1 and Stage 2, with retry amplification possible. Already analyzed sections and Stage 1 may be reused. These are source-code policies, not proof of provider behavior for every historical call.

## Measurements

Read-only SQLite inspection found 338 captures across 20 reports: 304 have nonempty saved responses and prompt-token metadata. Historical captures use different workflows; their measurements are not a controlled benchmark of today's prompts.

- Largest saved section input: **151,637 reported prompt tokens**, with 12,273 completion tokens. Three analyzed sections have more than 50,000 reported input tokens. Saved prompt character counts span a factor of 35.8.
- The preserved NTU comparison recorded Stage 1 input **44,677 tokens**, completion **30,050**, including **22,576 reasoning tokens**, elapsed **145.18 seconds**. Stage 2 input **35,974**, completion **43,537**, including **37,211 reasoning tokens**, elapsed **211.44 seconds**. These are historical recorded values, not new runs. They predate the final withholding implementation and do not isolate reasoning as a causal factor.
- All saved section responses total **8,203,536 characters**. Applying the existing Stage 1 compactor yields **4,384,698**: **46.55%** is already removable by its ledger-block cleanup. This supports examining repeated output; it does not mean all those tokens can safely disappear from future section context.
- Example of growth: Calgro AFS has 36 captures, 331,287 evidence characters, 1,831,519 saved prompt characters and 1,555,051 response characters. The final shared ledger is 12,907 characters. These character totals include repeated instructions, context and ledger material; they are not tokenizer-based cost estimates.
- Example of capture coverage: the 132-page Dis-Chem integrated report has one analyzed capture covering physical pages 1-25. NTU has two analyzed captures covering 30 of 38 physical pages. This measures page presence in saved selections, not full-page extraction accuracy, materiality, intentional selection coverage, or what Stage 2 inspected.

## Prioritized findings and proposals

### W01 - Split oversized captures instead of silently clipping them (first priority)

Evidence: `section_capture/section_matcher.py:549` exposes `max_pages=25`; lines 571-573 reduce the end page without scheduling the remainder. The ingestion loop calls this once for each detected section and counts that capture as completed. The saved DCP example is consistent with this risk; historical causation is not independently proven.

Proposal: partition a detected section into consecutive subcaptures based on text/token size, preserving tables and associated footnotes. Keep parent section identity and requested versus actual page spans. Record excluded pages with reasons and flag uncovered required financial statements/notes. A scan or successful analysis of selected captures must not imply whole-report coverage. Preserve intentional manual selection rather than forcing every page into every analysis.

Acceptance example: a detected 40-page section produces complete consecutive coverage (with explicit contextual overlap if needed), never a completed 25-page prefix. An image-only or nearly empty extracted page is flagged as unreadable, not accepted as inspected.

### W02 - Make the app own ledger state; ask DeepSeek for evidence-backed changes

Evidence: section templates require a full rewritten ledger after every call. `section_capture/db.py:1949` extracts a Markdown block; `save_section_llm_response` replaces the linked reports' ledger when the result is nonempty. Parent/sibling synchronization already exists, so lack of cross-document syncing is not the issue. No check there accounts for every previous question, validates closure evidence or rejects unrelated replacement text. An empty block is indistinguishable from failed extraction. The queue considers any nonempty section response analyzed.

Offline probes of the existing pure extractor confirmed that missing and empty ledgers both return None, while `Everything looks fine.` is accepted as ledger text. A replacement containing only Q2 is extracted without retaining Q1; code inspection shows no conservation check before replacement. These probes do not claim that Q1 actually disappeared in an existing run.

Proposal: retain stable question records in SQLite; model output supplies new questions and updates by stable ID. The app merges them, retains unresolved questions and records closure history. Question identity and target include company, period, source-document identity and section ID, since D003 alone is ambiguous across companion reports. Support an explicitly valid empty-open-ledger state. Reject or visibly flag missing/malformed ledger updates without losing the saved candidate response.

Acceptance: an omitted prior question stays open; closure requires source evidence; partial answers preserve the remainder; a new document's Q1 cannot overwrite another document's Q1; malformed updates do not count as a valid handoff.

### W03 - Improve what the ledger asks and what it retains

Evidence: the templates ask for priority, target section, trigger, verification instruction and forecast significance, which is a useful foundation. But the next section receives open questions rather than a separately validated register of already established facts. Resolved supporting evidence can therefore fall out of subsequent section context. Stage 1 receives earlier responses, so that information is not globally lost.

Proposal: each material question should identify the claim, classification (historical result/management explanation/guidance/assumption), required evidence, period/scope/units, exact reconciliation, target source, impact and closure condition. Permit both benign and adverse explanations. Route questions to current or previously inspected evidence as well as future sections. Keep a compact verified-facts register with citations and rejected interpretations, alongside open questions. Do not treat automatically extracted facts as independently verified merely because they are stored.

Concrete proposed question:

> Q-CASH-001: Starting from the exact statutory cash-flow subtotal for the stated period, what interest, tax and portfolio purchases are already included? Reconcile to the selected cash measure with signed components, capex, leases and borrowing treatment. Cite the physical page, row, units and consolidation scope. Pending: [cash-flow statement and portfolio notes]. Close only when the bridge reproduces the source subtotal and explains the chosen definition; otherwise retain the unexplained residual and its forecast consequence.

This is a proposed ledger design/example, not a newly codified analytical rule.

### W04 - Apply relevant lessons at the earliest stage and establish applicability first

Evidence: `packages.build_prompt` reads the sector's static section template and appends context; it does not call the SQLite guardrail formatter. Stage 1 and Stage 2 do. Thus approved reusable lessons are not dynamically injected into the section-analysis step. The consumer-lending section template leads with general Stage 1/2/3 lending assumptions, while Stage 2 groups finance, telcos and consumer lending under generic segment instructions.

Proposal: map existing approved rules to the section/metric where evidence can test them, and inject a short applicable subset with source requirements. First establish the actual business/asset type and accounting policy, then choose the relevant checks; do not force every credit asset into the same checklist. Route non-applicable items to explained exclusions. Keep global evidence-integrity rules mandatory and preserve every material unresolved dependency. Do not automatically add unapproved amendments or infer that a generic checklist establishes an accounting breach.

Acceptance: the existing approved POCI rule reaches relevant purchased-debt interpretation; a routine lending-staging checklist is not treated as evidence that the applicable policy is wrong. Specific accounting conclusions still require primary-source review.

### W05 - Give Stage 1 a structured evidence handoff, with explicit uncertainty

Evidence: Stage 1 already strips repeated ledger blocks and now carries material FAIL/NOT VERIFIED forward. However, its earlier instructions still call for `definitive determinations`, an `authoritative ledger` and `Final Verified Determination` before the final withholding handoff. Its main input mixes raw evidence and earlier model interpretations.

Proposal: separate source facts, management claims, model interpretations, calculations and unresolved dependencies. Produce a compact handoff table with stable claim IDs, document/page/row, period/scope/units, verdict, signed calculation and dependencies. Contradictory claims remain unresolved until evidence supports a correction. Use the same vocabulary throughout instead of relying on a late instruction to qualify definitive language.

Acceptance: an unresolved footnote-sign or cash subtotal issue remains visible as NOT VERIFIED and is linked to affected forecast cells. Stage 2 can trace a material input to evidence without reconstructing multiple narrative answers.

### W06 - Separate numerical construction/checking from final prose

Evidence: Stage 2 currently receives full extracted report text and performs source interpretation, forecasting, cash/debt reconciliation, valuation, sensitivity, seven readiness declarations, rating logic and publication formatting in one completion. The withholding gate checks declared evidence and numeric pairs but does not independently validate the source or derive the full financial model.

Proposal: define forecast and valuation schedules before writing the research note. Use deterministic local calculations for agreed formulas: cash/debt roll-forwards, share/unit conversions, bridge totals, sensitivity cells and returns. Feed discrepancies back as specific unresolved questions. The model remains responsible for explaining and supporting assumptions; software arithmetic does not validate those assumptions. Generate the final summary only from checked schedules, with withholding retained.

Acceptance: a deliberately inconsistent cash roll-forward or sensitivity centre is detected independently of a model's PASS declaration. A balanced model with unsupported inputs still cannot publish. This may be implemented as bounded stages within the current workflow; it need not introduce more paid calls automatically.

### W07 - Allocate context and reasoning to actual difficulty

Evidence: technical accounting section calls use the same default worker policy as simple sections, while later stages request max. Section sizes vary substantially, and `len(prompt)//4` is a display estimate rather than an enforced token budget. The existing Stage 1 compactor already removes many repeated ledger blocks; keep that improvement.

Proposal: combine coherent capture splitting, relevant open questions, concise cited facts and applicable approved rules. Retain an index to original evidence, and include all material dependent tables/footnotes rather than pruning purely by length. Estimate request size conservatively and record actual usage. Evaluate stronger reasoning on difficult sections (cash flow, portfolio accounting, shares and financing), while keeping mapping/simple extraction inexpensive. Do not raise every call to max or promise quality gains from the setting alone.

Acceptance: compare workload profiles on a fixed preserved case set, measuring evidence coverage, lost questions, incorrect closures, recurring errors, unexplained numerical residuals, withholding correctness, tokens and elapsed time. A later paid comparison requires authorization and must hold other changes constant where feasible.

### W08 - Make handoffs reproducible and failures visible

Evidence: `_process_next_section` catches every prompt-rebuild exception and silently sends the stored prompt instead; this can omit the latest ledger. Stage 1 reuse is based on saved output/no pending sections, without checking hashes of every input and active prompt/rule version. In the GUI Stage 2 route, the saved prompt is the base prompt, but the submitted request adds the full PDF/SENS dossier later. The preserved comparison runner has more complete request artifacts; that does not establish equivalent production capture.

Proposal: surface rebuild/ledger failures, save the exact submitted dossier and request hash plus context versions, and key reuse to input/prompt/guardrail/ledger hashes. Changes should mark affected stages stale and show the reason without automatically rerunning paid models. Derive forecast years and historical-versus-forecast columns from the report period and company year end, replacing the current FY26/FY27/FY28 literals.

Acceptance: changed prompt/guardrail/evidence marks dependent artifacts stale; a request can be reconstructed exactly; a 1H report does not silently reuse a full-year period basis; failed prompt rebuilding is visible before submission.

## Suggested implementation order

1. Coverage-preserving capture splitting and explicit coverage status (W01).
2. Persistent question IDs, validated updates and evidence-backed closure; compact cited facts (W02/W03).
3. Relevant approved guardrails at section level and consistent Stage 1 handoff (W04/W05).
4. Deterministic schedules, request reproducibility, reuse invalidation and dynamic periods (W06/W08).
5. Controlled reasoning/context comparison after the preceding offline checks (W07).

No proposed item has been implemented in production by this review. Prefer one bounded change at a time, with failure cases and preserved-case comparisons, rather than adding a large checklist to every prompt.

## Evidence, validation and limitations

Artifacts: `workload_metrics.json` includes source-code/template hashes, per-capture sizes, saved token metadata, capture page sets, enabled-rule scope counts and historical NTU run metadata. `offline_probe_results.json` records four assertions and compaction measurements. `inspect_workload.py` and `probe_workload.py` are reproducible local review scripts; both exited 0. They use SQLite URI read-only mode and avoid importing application modules. The probe script extracts existing pure functions through the AST to avoid database initialization or Qt side effects.

The production database SHA-256 was unchanged during both inspections. No original reports or model outputs were rewritten. No new extraction of PDFs or financial re-audit was performed. Captured-page presence does not prove content completeness. Saved provider token counts are reported metadata, not independently tokenized requests. Historical metadata is not proof of current provider routing. Suggested quality/cost improvements remain hypotheses until tested.

The full pytest suite was not rerun because production code was unchanged. The previous full offline result remains 178 passed, exit code 0. Terminal retrospective: initial combined reads and verbose metrics output exceeded display limits; bounded reads and the saved JSON supplied the needed detail (existing TOOL_CHEATSHEET.md section 19). The installed rg executable is available in this session despite earlier notes about its absence. No new shell, encoding or editing failure pattern was found.