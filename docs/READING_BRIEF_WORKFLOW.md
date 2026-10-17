# Progressive Section Question-Ledger & Footnote Workflow

Instead of feeding an entire company PDF to an LLM at once—or letting the LLM write generic narrative commentary on each section—this workflow uses the LLM as a **sequential verification and question engine**:

1. **Capture Section 1**:
   - The LLM does **not** write general summary commentary.
   - It scrutinizes every footnote (`[^1]`, `*`, etc.) and qualification that contains operational, accounting, or forecast commentary.
   - It draws up specific verification questions to check in future sections (tagged by Report Map section ID, e.g., `D003`, `D005`, `D006`, `D008`, `D009`) and outputs an **Open Questions Ledger** block plus compact baseline numbers for forecasting.
   - You copy that open-questions block and click **Stored questions → Replace from clipboard & Save** in the app.
2. **Capture Section 2 (and subsequent sections)**:
   - When you save the next section, the app **automatically embeds your Stored Questions Ledger** into `prompt.md`.
   - The LLM:
     1. **Answers ONLY the stored questions that relate to the current section** (`Resolved`, `Partially resolved`, or `Contradicted`, citing `[S00X, physical PDF p. Y]`).
     2. **Unpacks footnotes with commentary** in the current section.
     3. **Draws up new verification questions** from the current section for remaining upcoming sections.
     4. **Outputs an Updated Open Questions Ledger** (carrying forward unanswered questions for other sections + new questions from this section), ready to copy into **Stored questions → Replace from clipboard & Save** for Section 3.
     5. **Lists compact hard forecast inputs** captured or verified in this section.
3. **Sync across computers via Git**:
   - Saved captures, cached report maps (`documents/maps/`), and stored question ledgers (`documents/questions/`) are tracked in Git so you can commit, push, and continue on another computer seamlessly.
