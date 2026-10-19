"""Export script to compile the complete sequential extraction flow and questions ledger

Generates a single, self-contained markdown audit prompt for Gemini 4 Argon
to test whether it independently arrives at the same 7 forensic conclusions.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DB_PATH = ROOT / "documents" / "analysis.sqlite"
OUTPUT_PATH = ROOT / "companies" / "PAN" / "briefs" / "experiment2_argon_ledger_audit_prompt.md"

PROMPT_HEADER = """# EXPERIMENT 2: INDEPENDENT COGNITIVE AUDIT VIA SEQUENTIAL EXTRACTION & QUESTION LEDGER
**Target Asset:** Pan African Resources PLC (JSE: PAN | LSE: PAF | ASX: PAF)  
**Input Mode:** Sequential Forensic Working Paper & Dynamic Questions Ledger (No PDF Attached)  
**Task Directive:** Forensic Reasoning & Conflict Reconciliation Only (No Full Forward Valuation Model Required)

---

### INSTRUCTIONS FOR GEMINI 4 ARGON:
You are acting as an independent **Managing Director and Senior Forensic Mining Accounting Auditor**. 
You have been provided with the complete, chronological working paper compiled during a section-by-section forensic capture of Pan African Resources PLC's FY26 financial results announcement (19 sections, spanning from `D002` through `D009`).

Notice how this working paper is constructed:
1. At each stage, specific text, accounting notes, APMs, and production tables were extracted directly from the report.
2. Across the sections, an **Open Questions Ledger** evolved dynamically: anomalies and high-level management claims in early sections (`D002` Key Features, `D003` CEO Statement) were flagged with priority levels, specific verification instructions, and carried forward as `Pending` until verified against the primary financial statements (`D005`), detailed accounting notes (`D006`), APM schedules (`D008`), and production summaries (`D009`).

**YOUR MANDATE:**
Review the sequential evidence trail below. Trace how the questions evolved from initial anomalies to audited reconciliation. **Do not produce a forward equity research forecast or valuation report.** Your role is **forensic reasoning only**: you must evaluate the working papers and independently reach your own definitive determinations on the **7 Critical Forensic Junctions** outlined below.

---

## THE 7 CRITICAL FORENSIC JUNCTIONS TO EVALUATE

In your audit report, you must provide a dedicated, in-depth forensic analysis and clear, definitive conclusion on each of the following 7 junctions:

### 1. Junction 1: Diluted Share Count & Emmerson CDI Recognition Date
* *The Investigative Trail:* In `D002` and `D003`, the dividend conversion and narrative cite 2,434,309,216 shares. Note 14.1 cites 2,333,671,529 authorised and issued shares. PAR Gold holds 306,358,058 treasury shares. Note 14.2 and 18.1 cite 102,641,421 Emmerson CDIs in a "Shares to be issued" reserve of US$148.2m.
* *Your Task:* What is the exact diluted share count anchor as at 30 June 2026? When were the Emmerson CDIs formally allotted? Did they rank for the FY26 final dividend? What is the correct pro-forma share count post-1 July 2026 net of the ZAR 500m share buyback?

### 2. Junction 2: Balance Sheet Cash & Debt Position (Net Debt vs. Net Cash)
* *The Investigative Trail:* The CEO Statement claims US$246.2m in cash and liquid investments. Note 16 lists gross borrowings of US$51.5m, lease liabilities of US$7.8m, and financial liabilities of US$1.2m. The APM table reports net cash of US$185.7m, while raw balance sheet lines sum to US$185.597m.
* *Your Task:* Reconcile the exact cash and debt position. Is the company in net debt or net cash? Has the balance sheet de-geared from FY25 ($150.5m net debt), and what specific short-term liquid investments and lease liabilities make up the reconciliation?

### 3. Junction 3: Share-Based Payments (SBP) Treatment in Adjusted EBITDA
* *The Investigative Trail:* In `D003` and `D006.9`, cash-settled SBP is disclosed as US$57.3m in the P&L (leaving a US$64.4m balance sheet liability in Note 17.1). In `D008.4`, Group Adjusted EBITDA is reported as US$609.4m, with corporate overhead reported as US$51.9m / US$52.4m.
* *Your Task:* Was the cash-settled SBP already absorbed into the corporate overhead line inside the US$609.4m Adjusted EBITDA, or should SBP be added back to EBITDA? What is the correct recurring operational EBITDA of the group?

### 4. Junction 4: Third-Party Buy-In Feedstock & AISC Distortions
* *The Investigative Trail:* `D002` and `D009` report total gold production of 272,310 oz and Group AISC of US$1,867/oz. Note 3 and `D009` reveal that 18,667 oz came from third-party buy-in feedstock (Barberton 4,337 oz, BTRP 1,958 oz, Evander 6,609 oz, MTR 5,763 oz).
* *Your Task:* What was Pan African's true *organic* production and *organic* AISC? Quantify the exact unit cost distortion (+US$/oz) that third-party feedstock imposed on Group AISC and Evander Underground AISC. What are the margin implications of this buy-in material?

### 5. Junction 5: Underground Asset Economics & Higher-Cost Shaft Identification
* *The Investigative Trail:* Barberton Underground is presented as a premier high-grade asset with Fairview MRC and Rossiter platforms (>30g/t). However, `D008.2` and `D009` disclose that Sheba and Consort produced 25,154 oz.
* *Your Task:* Reconcile the cost split within Barberton Mines. What was the AISC of Fairview vs. the AISC of Sheba and Consort? What structural drag do Sheba and Consort represent, and what engineering initiatives (LHOS, PC shaft dewatering) are required to remediate this?

### 6. Junction 6: Forward Capital Expenditure Trajectory (The Capex Fork)
* *The Investigative Trail:* On page 10 of `D003`, narrative text mentions "US$302m total capital spend forecast for FY27", while the formal Board budget table on page 14 guides "US$330m" for FY27E and "US$303m" for FY28E. Note 8 confirms FY26 capex was US$224.0m (accrual) / US$215.8m (cash), of which US$202.2m was expansion capital primarily for MTR.
* *Your Task:* Explain the discrepancy between the $302m narrative and the $330m budget table. Then, critically evaluate the "Capex Fork": If MTR plant construction is finished, what is the technical sustaining/expansion capex requirement vs. management's uncommitted growth budget? Contrast Scenario A ($330m/$303m) with Scenario B ($110m/$65m Capex Cliff) in terms of Free Cash Flow to Equity (FCFE).

### 7. Junction 7: South African Section 36 Mining Tax & Cash Tax Step-Up Dynamics
* *The Investigative Trail:* In `D005.1` and `D006.4`, PBT is US$534.4m, Accounting Tax Expense is US$177.5m (33.2% ETR), but Cash Tax Paid is only US$74.1m (12.3% of EBITDA / 13.9% of PBT). Note 6.2 shows a US$97.2m deferred tax charge.
* *Your Task:* Explain the mechanics of the South African Gold Mining Tax formula ($Y = 33 - 165/X$) and Section 36 upfront capital deductions. Why was cash tax only 12.3% in FY26? What happens to unredeemed capital allowances (UCR) at MTR and Evander as capex drops to $110m? How must cash tax transition in FY27E and FY28E under Scenario B vs Scenario A, and why is applying both $330m capex AND a 32% cash tax rate a fatal accounting contradiction?

---

## REQUIRED STRUCTURE OF YOUR AUDIT REPORT

Please format your response into the following four clear sections:
1. **Executive Forensic Audit Summary:** Concise synthesis of the group's true economic performance, balance sheet health, and key findings.
2. **Detailed Forensic Reasoning & Determinations (Junctions 1 through 7):** Step-by-step walkthrough of each junction, citing specific notes, tables, and calculations.
3. **Audit of Common Surface-Reading Pitfalls:** Contrast your findings against the common errors made by naive readers (e.g. share count doubling, cash tax double deductions, capex budget rigidity, cash draining errors).
4. **Final Forensic Verification Matrix:** A clean markdown summary table listing each Junction, the Raw Initial Claim in D002/D003, the Resolving Note/APM, and your Final Verified Determination.

---

# THE SEQUENTIAL EXTRACTION & WORKING PAPER DOSSIER (19 SECTIONS)

"""


def compile_dossier() -> None:
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT section_number, section_id, heading, subheading, selected_text, stored_questions_snapshot
        FROM sections
        ORDER BY section_number
        """
    )
    rows = cursor.fetchall()
    conn.close()

    print(f"Loaded {len(rows)} sections from {DB_PATH}")

    content_blocks = [PROMPT_HEADER]

    for sec_num, sec_id, heading, subheading, selected_text, snapshot in rows:
        sub_title = f" — {subheading}" if subheading else ""
        header = f"\n\n{'='*80}\n## SECTION {sec_num}: [{sec_id}] {heading}{sub_title}\n{'='*80}\n"
        content_blocks.append(header)

        if snapshot and snapshot.strip():
            content_blocks.append(
                f"\n### [WORKING PAPER: OPEN QUESTIONS LEDGER AT THIS STAGE]\n"
                f"{snapshot.strip()}\n"
            )

        if selected_text and selected_text.strip():
            content_blocks.append(
                f"\n### [FORENSIC EXTRACTION: CAPTURED TEXT & FINANCIAL TABLES]\n"
                f"{selected_text.strip()}\n"
            )

    full_document = "".join(content_blocks)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(full_document)

    print(f"Successfully compiled {len(full_document):,} characters (~{len(full_document)//4:,} tokens)")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    compile_dossier()
