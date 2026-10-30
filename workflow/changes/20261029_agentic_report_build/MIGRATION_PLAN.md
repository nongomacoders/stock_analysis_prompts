# Migration plan: `agentic-report-build` → standalone GitHub project

Status: **PROPOSED** (2026-10-30). Nothing in this plan has been executed. Branch
`agentic-report-build` at `7bf5614` is the source of truth.

## 1. Why a split rather than a merge

The branch currently lives as a branch of `stock_analysis_prompts` and therefore carries the
entire production project in its tree and history — `section_capture/`, `app.py`,
`evaluate_stock.py`, `companies/**` for eight sectors, `prompts/`, and every production commit
since the merge-base. None of that is needed by the experiment, and some of it belongs to other
agents' work on this checkout.

The split produces a repository whose **tree is the charter and nothing else**: covenants,
extraction, reconciliation suite, evidence, reviews, audit.

## 2. What moves (measured, not estimated)

| Source path | Target path | Size |
|---|---|---|
| `workflow/changes/20261029_agentic_report_build/` | `/` (repo root) | ~1.6 MB incl. `report.sqlite` 1.14 MB, `report_view.xlsx` 186 KB |
| `reviews/p4_review_pack/` | `/reviews/` | ~0.6 MB |
| `companies/mining/PAN/sources/Pan-African-Resources-…-2026.pdf` | `/sources/PAN/` | 1.99 MB |
| `companies/mining/PAN/briefs/FY26/evaluations/20261029T190007Z_codex_p4_source_review/` | `/audit/codex_p4_source_review/` | 1.22 MB (frozen review snapshot) |
| **the full company source corpus** (27 PDFs, all sectors) — *staged separately, see §4a* | `/sources/<SECTOR>/<TICKER>/` | **207.7 MB** |

54 tracked files in the experiment folder; 39 commits touch the three evidence paths.

Two facts about the corpus, measured:

- All 27 PDFs are already git-tracked in the old repo, largest 40.7 MB (`it/IOC/…/iOCO-IAR-2026.pdf`)
  — inside GitHub's 100 MB hard limit and its 50 MB warning threshold.
- `companies/mining/PAN/sources/Pan-African-…-2026.pdf` and
  `companies/mining/PAN/sources/completed/FY26/Pan-African-…-2026.pdf` are **byte-identical**
  (`62b10bcd…`). The new repo carries one copy; the `completed/FY26/` convention does not survive
  the split.

## 3. What stays behind

- All production code and data: `section_capture/`, `app.py`, `evaluate_stock.py`,
  `new_sector.py`, `new_company.py`, `prompts/`, `docs/`, `tests/`, `companies/**` for every
  sector except the PAN source PDF.
- `reviews/20261029T*` — the self-authored role-play reviews. `AUDIT.md` already records that
  they are not independent review; carrying them into a fresh repo would re-import the
  confusion they caused. Leave them, and keep the one paragraph in `AUDIT.md` that says so.
- `.venv/`, `tmp/`, `__pycache__/`, `.pytest_cache/`.

## 4. History: three options

| Option | What you get | Cost |
|---|---|---|
| **A. Fresh single commit** | smallest repo, clean start | loses the P0→P6 commit sequence, which is the charter's evidence that phases ended in receipts |
| **B. `git filter-repo` on the three evidence paths** *(recommended)* | the 39 experiment commits, nothing else; real phase history survives | commit SHAs are rewritten, so every SHA quoted in `AUDIT.md` / `STATE.md` / commit messages becomes stale |
| **C. Push the branch as-is** | SHAs preserved | ships the whole production history into a new repo; defeats the purpose |

**Recommend B**, plus a committed `HISTORY.md` containing the `filter-repo` commit map
(`.git/filter-repo/commit-map`), so any stale SHA can be resolved rather than silently wrong.

This is safe for the database specifically: `cells.extraction_commit` does **not** hold git
SHAs — it holds script labels (`p1_extraction_v3`, `p1_notes_generic_v1`, …). So no cell
lineage dangles when history is rewritten. See §7 — that is also a defect to fix.

### 4a. How the 208 MB corpus enters (decided)

Carrying all 27 PDFs is the right call if this repo is to own the source corpus for every
company it will ever build. But it should not enter through `filter-repo`: that would rewrite
every one of the 39 commits to carry blobs they never touched, and it would make the weight
permanent and interleaved with the phase history.

Instead, two stages:

1. **`filter-repo` carries only the PAN 2026 PDF** — the one document any cell's lineage
   actually resolves against. History stays ~4 MB.
2. **One later commit imports the corpus**: `sources: import company source corpus (27 PDFs,
   207.7 MB)`, laid out as `sources/<SECTOR>/<TICKER>/<file>.pdf`, with `sources/MANIFEST.csv`
   (ticker, sector, filename, sha256, bytes, physical pages).

The second commit is self-contained, revertible, and replaceable by Git LFS later without
touching phase history. That is the difference between a decision you can revisit and one
baked into 39 commits.

## 5. Target layout

```
/
├── README.md                 what this is, how to run it, current state
├── CHARTER.md                from the experiment charter, status PROPOSED → ACTIVE
├── AGENTS.md                 rewritten: covenants + working rules for this repo only
├── RUNBOOK.md                phase order, rewritten for the new paths
├── AUDIT.md                  §1A record, SHA references resolved via HISTORY.md
├── HISTORY.md                commit map + why the SHAs changed
├── SOURCES.md                PDF provenance, SHA-256, licence note
├── WORKPLAN*.md, HYPOTHESES.md, READING_BRIEF*.md
├── build/
│   ├── report.sqlite         4,802 cells · 97 conflicts · 8 open questions
│   ├── report_view.xlsx
│   ├── extraction/           one module per region + words.py
│   └── receipts*.json
├── tests_reconcile/          127 tests
├── ground_truth/             reviewer scoring key (never read by build code)
├── reviews/                  PROMPT.md, PROMPT_CODEX.md, INDEPENDENT_REVIEW.md,
│                             CODEX_REVIEW.md, COVERAGE.md, REMEDIATION_BACKLOG.md, *.csv
├── audit/codex_p4_source_review/
├── sources/
│   ├── MANIFEST.csv            27 PDFs: ticker, sector, filename, sha256, bytes, pages
│   ├── PAN/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf
│   └── <SECTOR>/<TICKER>/…      corpus, imported in its own commit (§4a)
├── docs/EVIDENCE_AUDIT_FORMAT.md   the §1A subset only, extracted from the production doc
├── pyproject.toml            pypdfium2, openpyxl, pytest  (no PySide6)
├── .gitattributes            build/** and audit/** -text (byte-exact evidence)
└── .gitignore                tmp/, __pycache__/, .pytest_cache/, *.png renders
```

## 6. Path defects that break the moment the folder moves

These are real, already present, and would fail silently or loudly on first run in the new repo:

| File | Problem |
|---|---|
| `build/extraction/extract_pan_d009.py:50` | `ROOT = Path(r"C:\Users\diond\Desktop\Projects\stock_prompts_agentic")` — absolute, machine-specific |
| `build/extraction/*.py` (11 files) | PDF located via the literal `companies/mining/PAN/sources/…` path |
| `build/extraction/render_pages.py:12` | `sys.path.insert(…parents[4])` — depth-dependent, and unused |
| `build/extraction/render_pages.py:18` | `EVIDENCE_DIR` hard-coded to `C:\Users\diond\AppData\Local\Temp\opencode\…` |
| `sources` table | `path` column stores the absolute source path |
| `build/remediate_p34_lineage.py` | same PDF literal, plus it is a one-shot remediation script, not a build step |

Fix: one `build/paths.py` resolving `REPO_ROOT = Path(__file__).resolve().parents[2]`, PDF at
`REPO_ROOT/"sources"/…`, and `sources.path` rewritten to a repo-relative string (an `UPDATE` on
`sources` only — no printed cell is touched, so covenant 1 is untouched).

Also: `render_pages.py` imports PySide6 solely to save a `QImage`. `pypdfium2`'s
`PdfBitmap.save()` does it directly. Dropping PySide6 removes the Qt window-disposal rule from
this project entirely — it belongs to the capture app, not here.

## 7. Covenant defect to fix during the move

Covenant 3 says *page + sha256 + **extraction commit***. `cells.extraction_commit` has never
held a commit — it holds extractor versions (`p1_extraction_v3` etc., verified against
`4bea72f` and `16516af`). The Gemini review's claim that D009 cells carry `9d33906` was wrong.

Two columns, not one:

- `extractor_version` — rename of today's value.
- `git_commit` — the real SHA, stamped by the extractor at run time (`git rev-parse HEAD`), NULL
  for rows extracted before this change, with a documented cut-off date.

Do this **in the new repo**, in the same commit that rewrites `CHARTER.md` status, so the charter
stops claiming something the schema does not deliver.

## 8. Commands

### Step 0 — freeze the current branch

```powershell
cd C:\Users\diond\Desktop\Projects\stock_prompts_agentic
git add -A
git commit -m "state: commit Codex audit record + branch state before the standalone split"
git push origin agentic-report-build
git tag pre-split-20261030
git push origin pre-split-20261030
```

The tag is the anchor every rewritten SHA can be traced back to.

### Step 1 — filtered clone

```powershell
cd C:\Users\diond\Desktop\Projects
git clone --no-local --single-branch --branch agentic-report-build `
  stock_prompts_agentic agentic-report-build
cd agentic-report-build

git filter-repo --force `
  --path workflow/changes/20261029_agentic_report_build `
  --path reviews/p4_review_pack `
  --path companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf `
  --path companies/mining/PAN/briefs/FY26/evaluations/20261029T190007Z_codex_p4_source_review `
  --path-rename "workflow/changes/20261029_agentic_report_build/:" `
  --path-rename "reviews/p4_review_pack/:reviews/" `
  --path-rename "companies/mining/PAN/sources/:sources/" `
  --path-rename "companies/mining/PAN/briefs/FY26/evaluations/20261029T190007Z_codex_p4_source_review/:audit/codex_p4_source_review/"

git branch -m agentic-report-build main
git log --oneline | Measure-Object -Line      # expect ~40
Get-ChildItem -Force                          # expect charter, build/, tests_reconcile/, …
```

### Step 2 — de-nest, re-anchor, rewrite content

One commit per concern, in this order:

1. `paths`: add `build/paths.py`, replace the 13 hard-coded paths, rewrite `sources.path`.
2. `deps`: drop PySide6 from `render_pages.py`, add `pyproject.toml`, `.gitattributes`, `.gitignore`.
3. `docs`: `README.md`, `AGENTS.md`, `SOURCES.md`, `HISTORY.md`, `docs/EVIDENCE_AUDIT_FORMAT.md`;
   `CHARTER.md` PROPOSED → ACTIVE; `RUNBOOK.md` paths; `AUDIT.md` + `READING_BRIEF_CONSOLIDATED.md`
   cell count 4,800 → 4,802.
4. `lineage`: `extraction_commit` → `extractor_version` + `git_commit`, with the cut-off documented.
5. `corpus`: import the 27 PDFs into `sources/<SECTOR>/<TICKER>/`, generate `sources/MANIFEST.csv`,
   drop the byte-identical PAN duplicate. Separate commit, per §4a.

```powershell
# corpus import (run from the old repo, writing into the new one)
$dest = "C:\Users\diond\Desktop\Projects\agentic-report-build\sources"
Get-ChildItem "C:\Users\diond\Desktop\Projects\stock_prompts_agentic\companies" -Recurse -Filter *.pdf |
  Where-Object { $_.FullName -notmatch "completed\\FY26\\Pan-African" } |
  ForEach-Object {
    $rel = $_.FullName -replace '^.*\\companies\\',''
    $sector, $ticker = $rel.Split('\')[0,1]
    $out = Join-Path $dest "$sector\$ticker"
    New-Item -ItemType Directory -Force -Path $out | Out-Null
    Copy-Item $_.FullName -Destination $out
  }
```

### Step 3 — verification gate (must pass before the repo exists on GitHub)

```powershell
python -m pytest tests_reconcile -q -p no:cacheprovider --basetemp=tmp/split
# expect: 127 passed

python -c "import sqlite3;print(sqlite3.connect('build/report.sqlite').execute('SELECT COUNT(*) FROM cells').fetchone())"
# expect: (4802,)

Get-FileHash sources\PAN\*.pdf -Algorithm SHA256
# expect: 62B10BCD8E6216C00BBE005AE85A3C3341E01E82FD24AF0516DE18BF69C9B4DD

git grep -nF "C:\Users" -- . ; git grep -nF "stock_analysis_prompts" -- .
# expect: no hits (-F: literal, so backslashes are not regex escapes)
```

Then a **cold clone** into `tmp/` and repeat the first two checks. A suite that passes only in
its own working directory is not portable.

### Step 4 — create and push

```powershell
gh repo create nongomacoders/agentic-report-build --private --source . --remote origin --push
```

Then: set `main` as default, protect it (require green CI before merge), and add the GitHub
Actions workflow — `.github/workflows/reconcile.yml` running the suite on every push. That is
what turns "the suite is green" from a claim in a markdown file into a gate.

### Step 5 — close the old branch

Leave `agentic-report-build` in `stock_analysis_prompts` intact as the archive (plus the
`pre-split-20261030` tag). Add one line to that repo's `workflow/STATE.md`: the experiment moved
to `nongomacoders/agentic-report-build`, this branch is frozen. Do **not** delete it — the
review trail in `reviews/p4_review_pack/` refers to its SHAs.

## 9. First milestone in the new repo

The move does not fix anything. The new repo opens with `reviews/REMEDIATION_BACKLOG.md`
(F001–F005) as its first milestone, in this order:

1. **Completeness test** — assert that the number of amount positions stored per table equals the
   number printed on the page. This is the deliverable the current suite structurally cannot
   provide: 127 green tests over a dataset missing Note 8's entire table proves arithmetic, never
   coverage.
2. **Per-table schemas** — replace the modal-width-per-page parser that ate Note 8 and mislabelled
   the p.24 geography table.
3. **Restore and reconcile** F004 → F002 → F003 → F001 → F005.
4. **Second document** — only after the completeness gate exists, because a harness that cannot
   detect omission on PAN cannot be trusted on a second report.

## 10. Decisions — resolved 2026-10-30

| Decision | Answer |
|---|---|
| History | **`filter-repo` + committed `HISTORY.md` commit map** (§4) |
| Visibility | **private now**, public once the completeness gate (§9.1) exists |
| PDFs | **the PAN 2026 PDF in filtered history; all 27 company PDFs imported in one later commit** (§4a) |
| Role-play reviews | **left behind**; `AUDIT.md` keeps the correction paragraph |

Still open, and only answerable after the move:

- **Repo name.** `agentic-report-build` is the working assumption. It is accurate today and
  slightly narrow if the corpus makes this the general build project.
- **Does the corpus belong in git at all?** The staged commit makes this reversible. If clone
  time becomes a problem, `git lfs migrate import --include="sources/**/*.pdf"` converts it
  without touching phase history.

