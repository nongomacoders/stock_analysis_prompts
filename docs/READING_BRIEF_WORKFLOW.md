# Analyst reading and verification workflow

Instead of feeding an entire company PDF to an LLM at once, this workflow scans the PDF's major sections first, then feeds captured sections one by one. For each section, the LLM summarizes key points, questions consequential claims, and advises what to verify in upcoming sections.

## Intended LLM response

1. **What this section is saying**: Concise summary of the important message, key figures, and qualifications, citing selection IDs and physical PDF pages (e.g., `[S003, physical PDF p. 7]`).
2. **What to check**: Prioritized list (high/medium/low) of consequential claims or questions, why each matters, what specific evidence or reconciliation to inspect, and whether it is supported here, shows a visible discrepancy, or is `Pending: [section]` for a later section.
3. **Where to read next**: Which upcoming report sections, notes, APM reconciliations, or operating tables to capture next and what question each will resolve.

The prompt adapts guidance based on each selection's analyst-tagged data type (`Commentary`, `Table`, `Financial note`, or `Mixed / unspecified`).

## Step-by-step usage

1. Open the PDF in the capture app (`Run Capture.cmd`). The app automatically scans native headings to build a coarse major-section map.
2. Optionally click **Report map → Copy overview** and paste it into a fresh LLM chat to orient the model before uploading the first section.
3. Select the relevant text or area regions for a section, tag their data types, and click **Save section + upload ZIP**.
4. Click **Open saved folder**, attach the PNG images from `evidence/` to your LLM chat, and paste **Copy reading prompt** (`prompt.md`).
5. Review the model's summary and pending verification questions, then capture the next recommended section (e.g., CEO commentary, primary financial statements, financial notes, APMs, or operating tables) to resolve those pending checks.
