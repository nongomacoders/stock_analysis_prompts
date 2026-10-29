# Approved NTU ECL guardrail

Codified following the user's explicit approval of the corrected rule in the [Codex audit](../../../companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T093647Z_codex_review/audit.md).

- Rule: `CONSUMER-LENDING-TRADE-RECEIVABLES-SIMPLIFIED-ECL`; enabled, consumer_lending, all stages, origin NTU.
- [Approved wording and authorization](approved_rule.json).
- [Duplicate/conflict review](duplicate_conflict_review.json).
- [Implementation and preservation checks](implementation_record.json).
- `before.sqlite` preserves the pre-change database; `prompt_check.sqlite` is the isolated prompt-verification copy. Do not restore the database wholesale over subsequent work.
- `codify_guardrail.py` preserves the script executed from `scratch/codify_ntu_ecl_guardrail.py`. It deliberately refuses insertion if the rule already exists; do not use it to overwrite a later rule.

Actual script exit: **0**. Six actual prompt-builder checks passed: consumer-lending Stage1, Stage2 and SENS include the full mandate; retail equivalents exclude the rule. Network operations were denied within Python. All other business rows were unchanged. No paid calls, application changes or full pytest suite.

This verifies registry storage and prompt delivery, not future model adherence. Other proposed prompts/questions/guardrails and section-prompt integration were outside the approval and were not changed. Original audit/model evidence and financial outputs remain preserved. Terminal retrospective found no new tooling failures or new patterns requiring another cheatsheet entry.
