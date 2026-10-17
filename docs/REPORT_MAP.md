# Major-section report map

When you open a PDF in the capture app, it scans native titles and running headings to build a coarse outline of the report's major sections. Every saved section prompt includes this map so the LLM knows what material is in the current upload and what sections are still upcoming.

## How to use

1. Open a PDF in **Report Section Capture**. A new report is scanned locally and cached under `documents/maps/<source-sha256>/`.
2. Click **Report map** in the toolbar to inspect the detected sections, **Copy overview** for your chat, or **Rescan**.
3. Save selections as usual. Each exported `prompt.md` embeds the report overview and marks sections overlapping your current crops as `Partial selected evidence: S001...` while marking all other sections as `Not included here; available for possible later reading`.
4. The LLM marks cross-section verification items as `Pending: [section title]` rather than assuming missing disclosures or hallucinating answers from unread pages.

## What the scanner detects

- Checks native large display titles and top running headings on every physical page using `pdfplumber`.
- Recognizes major mining/financial report sections: Highlights, CEO's statement, Financial review, Operating review, Financial statements overview, Primary financial statements (including sightings of financial position, profit or loss, OCI, cash flows, and changes in equity), Financial notes, Other items, Alternative performance measures (APMs), Group production summary, Glossary, Corporate information, and Reporting suite.
- Detects split-page boundaries (`left` / `right`) when different major section headings appear on opposite sides of a two-page spread.
- Keeps printed page labels `null` rather than guessing page offsets, and explicitly lists unclassified pages or scan issues.

## Limits

- The scan is an `automatic_draft` navigation aid based on native PDF text and font sizes (no OCR).
- Overlapping a mapped section marks it as partial selected evidence in that request, not a completed review of the entire section.
