from pathlib import Path

p = Path("workflow/STATE.md")
content = p.read_text(encoding="utf-8")

new_entry = """- **Gemini independent review of simplified section-reading prompt pilot completed (2026-10-28)**:
  - Saved full independent evidence audit under `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T170032Z_gemini/audit.md`, input manifest in `inputs/manifest.json`, and calculations script in `calculations/reconciliations.py` (all tests passed, exit 0, outputs in `calculations/reconciliation_output.json`). Source PDF hashes verified for NTU (`9a19b3b4...`) and PAN (`62b10bcd...`); production database and all originals preserved untouched.
  - Concluded **SUPPORTED FOR FULL NTU TRIAL — SPECIFIC FIRST-PASS IMPROVEMENTS CONFIRMED; TARGETED REUSABLE PROMPT TWEAKS IDENTIFIED**. Evaluated all 4 paired captures and 8 Fireworks calls against original PDFs (NTU pp.13, 25; PAN pp.38-39, 48-50).
  - Confirmed operational improvements: 4/4 valid ledgers (100%) vs 3/4 (75%), 12 proposed questions vs 26 (-53.8%), prompt chars -17.1%, completion tokens -32.9%, wall-time -29.3%, cost -25.2%. Clean 4-part structure preserved secondary topic starts (NTU p.25 Note 6.2 currency risk) and linked to `Pending: p.26`.
  - Confirmed model defects: NTU p.13 ledger equation string inverted sign (`702 + 28 - 116 - 30 = 644` evaluates to 584, a -60m error; prose is correct), model persisted in requesting POCI ECL staging tables (`Q-b332e6c7ddfc4e8d`) despite sector note warning, and NTU p.25 answers overinterpreted standard interim comparative presentation and zero loss rates.
  - Forensically resolved PAN operations table discrepancy: the apparent 1,573 oz gap in text and 1,081 oz excess in `Q-99e93be7ca7c4594` arise from upstream extraction column collapse and model double-counting of 1,081 oz third-party buy-in feedstock against 2,654 oz Barberton surface production (`2,654 - 1,081 = 1,573 oz`), while company totals (196,527 oz FY25, 272,310 oz FY26) are mathematically exact.
  - Formulated 3 minimal reusable prompt clarifications (strict equation sign consistency, explicit POCI staging prohibition, and interim comparative context) prior to full chronological trial. No paid API calls or production code/guardrails modified. Audit ready for Codex review.

"""

target = "## Completed\n\n"
if target in content and "Gemini independent review of simplified section-reading prompt pilot completed" not in content:
    content = content.replace(target, target + new_entry, 1)
    p.write_text(content, encoding="utf-8")
    print("Updated workflow/STATE.md")
else:
    print("Could not find target or already present")
