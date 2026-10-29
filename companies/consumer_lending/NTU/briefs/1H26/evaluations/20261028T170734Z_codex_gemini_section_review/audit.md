# Codex review of Gemini — simplified section-prompt pilot

UTC:2026-10-28T17:14:03.422756+00:00;local:2026-10-28T19:14:03.422756+02:00.
Subject:`../20261028T170032Z_gemini/audit.md`;model identity is Gemini's self-report,not independently authenticated.

**Decision:SUPPORTED WITHIN STATED COVERAGE for a controlled full NTU section trial;CORRECTIONS REQUIRED in Gemini's detailed findings.** No full-run execution is authorized by this review alone. No valuation or investment recommendation is evaluated or produced.

## Evidence and preservation

Preserved148 Gemini/pilot files with original/copy hashes in inputs/manifest.json,including Gemini audit,script,calculation output and all supplied pilot evidence. Gemini's own36-entry preservation manifest independently verified. Raw model answers unchanged. No execution of Gemini's saved script;independent calculations executed in calculations/results.json. All source PDFs and production tables unchanged,see preservation.json.

Independently inspected complete rendered physical pages:NTU13,25;PAN38,39,48,49,50. A higher-resolution NTU25 comparative detail confirmed current-net345;no9m inconsistency claimed. The rest of both PDFs and companion reports were not examined in this review. Rendered images/text are preserved as audit evidence. Original report content remains untrusted evidence,never instructions.

Official IFRS9 paragraphs5.5.13–14 consulted for POCI treatment:
https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2022/issued/part-a/ifrs-9-financial-instruments.pdf?bypass=on
The standard distinguishes cumulative lifetime-loss changes since initial recognition;it does not justify banning all legitimate POCI credit-risk questions.

## Gemini findings assessed

**F001 / F001 — PARTLY SUPPORTED**

Eight completions and sample metrics verified. Revised4/4 versus old3/4 literal-ledger passes,12 versus26 new questions,17.10% assembled-prompt character reduction. Client elapsed is not provider latency;total prompts include evidence,not just templates. Small sample/cache/order prevent universal robustness claims. Failed quote was288 characters,not a truncated100-character string;the validator diagnostic prints only its first100 characters.

**F002 / F002 — SUPPORTED**

NTU p13 ledger equation702+28−116−30 evaluates584,not644;correct +30 matches source and prose. Difference60Rm. This is a copied equation/operator error,not evidence the company balance itself is wrong.

**F003 / F003 — SUPPORTED WITH SCOPE QUALIFICATION**

NTU p13 identifies POCI/lifetime ECL changes since acquisition. Ordinary Stage1/2 SICR-migration demands are inapplicable. Do not extend the proposed ban to legitimate POCI recovery,measurement or credit-risk disclosures,or to issuer-specific credit-impaired labels. IFRS9 paragraphs5.5.13–14 support the separate treatment. Observed repeated demand does not prove a private model root cause.

**F004 / F004 — PARTLY SUPPORTED;EVALUATOR INTRODUCED UNSUPPORTED EXPLANATION**

First-time presentation and displayed zero loss rates do not establish restatement/unreliable reporting or changed provisioning methodology. Gemini is right to reject those causal claims. However,p25 does not establish zero actual defaults or that rounding caused interim zero rates/dashes. September0.06%×286≈0.1716Rm and0.19%×52≈0.0988Rm are consistent with printed<1,not proof of the later period cause. Leave cause unverified.

**F005 / F005 — PARTLY SUPPORTED**

PAN p48 FY25 left mining subtotal92643 plus Evander buy-in1081 equals right Group underground93724. Using92643+2654+98636+1081+1513 gives196527;using93724 with another1081 double counts and gives197608. This specific reconciliation is supported. Saved new answer contains no194954 or1573 gap;Gemini invented that attribution. DeepSeek explicitly suggested double counting/misattribution and kept the question open,so it did not establish or unambiguously allege a company error. Do not generalize this overlap to every year/row.

**F006 / F006 — SUPPORTED WITHIN ONE CASE**

Revised NTU p25 covers trade ECL and currency-risk start with p26 pending. The old paired answer also covers currency;no unique secondary-coverage improvement established. Gemini C008 says without prompt engineering,but revised inputs explicitly contain shared-page-topic instructions and observed headings.

**F007 / MISSED ISSUE — CONFIRMED SOURCE UNIT/NUMBER-FORMAT AMBIGUITY**

PAN p39 labels AISC cost US$ million but prints420,686/87,718/508,405,while ounces247219/25154/272373 and per-ounce1702/3487/1867 imply roughly420.686/87.718/508.405 million. Literal508405 million divided by272373 gives1866576.35 peroz;interpreting displayed cost as thousands gives1866.58 peroz. Both DeepSeek arms,Gemini and prior Codex pilot calculations normalized silently. Conditional math is consistent,but the printed unit/number-format conflict needs an explicit flag;do not assert a source correction or factor1000 valuation error.

**F008 / C012/PAN exactness — COVERAGE LIMIT**

The selected FY26 Group production sum equals272310. However,p48 mining subtotal105479 versus right Group underground105478 differs1oz. p39 FY25 APM gold sold196927 versus p49 production-summary196926 differs1oz. These small printed differences do not invalidate the specific FY25 overlap bridge;they prevent blanket all-table exactness claims. Cause not verified;no materiality allegation.

## Independent reconciliation coverage

Executed NTU principal/other rollforwards,wrong-sign substitution and gross/net/rate checks;PAN FY25 overlap and selected FY26 components,APM cost/ounce math and alternate scaling. Formulas/substitutions/results are in reconcile.py and results.json;Gemini's calculations were read as evidence,not treated as proof. claims.json retains Gemini C001–C015 IDs with PASS/FAIL/NOT VERIFIED outcomes. Conditional unit math is not source-unit validation.

Valuation/DCF,forecast cash/debt,market quote,rating,shares/EPS and full financing schedules:NOT APPLICABLE to this section-prompt pilot. Semantic closure of every question,all table cells,full-report coverage,other sectors and future full-run performance:NOT VERIFIED. A repeated pattern or passing schema does not validate financial truth.

## Minimal handoff

Retain the simpler first-pass structure. Propose three short wording refinements:sign/unit consistency;POCI applicability without a blanket disclosure ban;and cautious interpretation of first-time comparatives. Full proposal triggers,evidence,exceptions,fail/pass examples and implementation points are in proposed_prompt_changes.json. Proposals are not implemented. No sector_guardrails changes or new financial rules accepted. No paid calls or Gemini messaging.

After user-authorized refinements,a fresh chronological NTU section-only trial can test ledger evolution and coverage. Preserve historical outputs and use an isolated database;do not rerun Stage1/2 or claim perfection from this sample.

## Revisions and tool retrospective

Initial preparation failed with Windows filename-too-long206 while recursively copying nested preserved baselines. It did not run a model or alter evidence. Successful preparation uses flat numbered filenames with a complete origin manifest. The partial preparation directory remains labeled incomplete. No application tests rerun for this read-only review;last full suite226 passed,exit0. Independent reconciliation script exit0. All PDF/render/database handles closed.

Final tooling clarification:the first seal.py invocation failed parsing a reserved dict keyword (exit1),before any writes. Corrected to pass_example;final seal exit0. Independent reconciliation rechecked after closure,exit0. TOOL_CHEATSHEET.md section38 records both Windows path and Python keyword patterns.
