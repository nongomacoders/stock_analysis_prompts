# Use this section in an online model

1. Start a fresh model chat.
2. Upload all PNG files from evidence/.
3. Paste the entire contents of prompt.md. It already includes the selected text and source IDs.
4. Ask for the readable summary and prioritized verification advice described in the prompt. No JSON response is requested.
5. Save the raw response unchanged, recording the model name and settings.

The reading prompt includes the report outline when a draft scan is available. You may paste report-overview.md first to orient the chat; it is also included in prompt.md. Unprovided sections remain possible follow-ups, not evidence already inspected.

The ZIP is a convenient copy of this folder. If the chat cannot read ZIP files, unzip it and attach the PNGs directly. The original PDF is not included. With the selections alone, the model suggests checks for you to do in the report. If you want it to inspect the report for those checks, also attach the original PDF; a local path is not access.

manifest.json preserves original physical pages, source identity and selection coordinates. Each selection's data type is an analyst hint; the prompt includes reading guidance for commentary, tables and financial notes. The manifest is local JSON metadata; the requested model response is a Markdown reading brief. A summary or suggested check does not establish source verification or analyst approval.
