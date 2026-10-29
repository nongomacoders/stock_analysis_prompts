# Charter: Agentic report build ("build software, but the artifact is a report")

Status: **PROPOSED — NOTHING IMPLEMENTED.** This branch (`agentic-report-build`) is the isolated
workspace. Production workflow, `one_shot` branch, prompt templates, app code and SQLite
production tables remain untouched. Created 2026-10-29 from `one_shot@37bfaba`.

## 1. Hypothesis

An OpenCode agent can build an auditable company report the way it builds software:
plan first, scaffold tools (SQLite, extraction scripts, Excel view), iterate against an
executable reconciliation suite, commit receipts, and hold alternative interpretations on
separate branches/worktrees until the suite adjudicates them.

The precondition this tests (from the 2026-10-29 three-pass review):iteration fails when a
deterministic referee is missing. In software that referee is the test suite; in report
reading it must be **executable reconciliation checks** — printed column sums, cross-page
identities, roll-forwards — run as code, never asserted by the model in prose.

## 2. Protocol (phases; each ends in a commit with receipts)

- **P0 Blueprint.** `WORKPLAN.md` in this folder: sections targeted, source PDFs with SHA-256,
  planned schema, known question-ledger imports. No extraction before P0 is committed.
- **P1 Schema + extraction.** SQLite `report.sqlite`: `sources`, `pages`, `extracted_cells`
  (value, unit, physical page, printed label, row/col coordinates, extraction commit), and a
  `conflicts` table. Extraction scripts are committed; every cell carries its page citation
  and the source PDF hash.
- **P2 Reconciliation suite.** A pytest suite (`tests_reconcile/`) that re-adds every printed
  total from leaf rows, checks cross-page identities, and rolls forward balances. CI gate:
  `.venv python -m pytest tests_reconcile -q` must be green, or every failing check is
  **explicitly recorded in `conflicts`** with page citations. Silent insertion of
  "corrected" values is forbidden.
- **P3 Hypothesis branches.** Each competing interpretation of an ambiguity gets its own
  worktree/branch off P2 (examples: which printed value is the operative Barberton total;
  whether a printed total includes a component column). The suite runs on each branch;
  the branch report shows reconciliation delta *with flags*, and **unresolved ambiguity stays
  open as a ledger question** — a branch that requires changing a printed company number
  never merges silently.
- **P4 Narrative + view layer.** The reading brief/report is generated only from the
  reconciled DB. Excel is a *view over commits*: derived tools read `report.sqlite`, never
  the PDF twice, never another tool's spreadsheet output.
- **P5 Review gates.** Treat the P4 commit as a PR: Gemini-role review of the diff, then a
  Codex-role review against the original PDFs — the existing Gemini→Codex loop, unchanged.
- **P6 Audit.** A §1A-shaped record (input manifest, inspected pages, executed checks,
  findings, cost/time) so results meet the same evidentiary bar as every other evaluation.

## 3. Covenants (non-negotiable guardrails)

1. **Never replace a printed source figure.** Conflicts are data (`conflicts` table +
   ledger), not bugs to fix. Conditional agreement (e.g. substituting 84,929 makes a PAN
   opsum tie exactly) is recorded as a *hypothesis with its conditional check*, never as a
   correction — this is the documented 2026-10-29 trap.
2. **All arithmetic executes in code.** The agent writes checkers; it does not compute sums
   in prose. A failed check re-dispatches to the page, not to model memory.
3. **Lineage on every number**: page + sha256 + extraction commit in the DB.
4. **The ledger stays independent of the code verdicts.** The code proves reconciliation;
   it does not decide accounting meaning (sign conventions, APM definitions remain prose
   discipline and open questions).
5. **Extraction layer frozen** before any derived layer is generated.
6. **No production writes, no source-PDF edits, originals preserved**; paid-model run
   accounting preserved like every experiment (cost, tokens, retries — receipts per call).
7. **Scope discipline:** first run is one section only (PAN D009 pp.48-50). Do not scale
   until the section run passes P5/P6 without a silent correction.

## 4. Scoring against the 2026-10-29 baseline

The PAN D009 section already has independently verified ground truth (see
`ground_truth/pan_d009_expected.json`). The build run is scored on:

- **Detection:** does its suite independently surface the known survey items? (1-oz leaf-sum
  71,998 vs 71,997; Δ10,000 Barberton/opsum conflict; Δ5,763 MTR leaf vs total-ops;
  FY25 disjoint 196,527 vs overlap 197,608 resolution opportunity; EBITDA leaf-sum 663.0 vs
  663.1; p.50 revenue/capex ties.)
- **No silent corrections:** zero instances of the covenant-1 violation in the diff audit.
- **Cost/time** vs the three-pass run (known subtotal $0.03107 for both cases; ratios
  2.24x-2.39x cost). Compare apples-to-apples: one section, same model/settings as the agent.
- **Reviewer findings:** Gemini-role then Codex-role findings on the P4 report vs their
  findings on the three-pass outputs. The honest measure is *errors reviewers can no longer
  find, and open questions that stayed open rather than fake-closed*.

## 5. Non-goals

No production `section_analysis`/prompt template changes unless a demonstrated lesson is
ported. No valuation claims from the build run beyond what the reconciled numbers support.
This charter does not modify `AGENTS.md`, the app, or the question-ledger schema; any such
change is a separate, evidence-carrying proposal after P6.

## 6. Open design questions (to answer during the run, not before)

- How should the suite express "source defect confirmed" vs "extraction defect"?
- Can render-and-look (pypdfium2 + vision) become a P1 acceptance test for dense landscape
  tables, and is it worth its token cost?
- Do extracted `conflicts` map cleanly enough onto existing ledger question records to make
  the reconciliation findings reusable in the production workflow later?
