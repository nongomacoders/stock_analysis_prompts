"""Prepare human-run Antigravity reviews; never call a model or alter evidence."""
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
plan=json.loads((HERE/'comparison_plan.json').read_text(encoding='utf-8'))
preservation=json.loads((HERE/'production_preservation_check.json').read_text(encoding='utf-8'))
summaries=[]
index=['# Antigravity evaluation handoff', '',
       'DeepSeek reruns use isolated databases. Run Gemini in Antigravity; no Gemini API calls were made. '
       'Preserve the complete Gemini review, then ask Codex to evaluate it against original evidence. '
       'These are mixed, iteratively repaired workload trials, not controlled proof of better financial accuracy.', '']

for info in plan['companies']:
    run=Path(info['run'])
    status=json.loads((run/'status.json').read_text(encoding='utf-8'))
    if status['status']!='awaiting_user_antigravity_evaluation':
        index.append(f"- {info['ticker']} {info['period']}: {status['status']} ({status.get('stage')}); pack not yet complete.")
        continue
    for document in info['documents']:
        actual=hashlib.sha256(Path(document['path']).read_bytes()).hexdigest()
        if actual!=document['sha256']:
            raise RuntimeError('Source hash changed before handoff: '+document['filename'])
    before=run/'outputs/execution_status_before_handoff.json'
    if not before.exists():
        shutil.copy2(run/'status.json',before)
    if status.get('error'):
        status['prior_interruption_error']=dict(type=status.pop('error_type',None),message=status.pop('error'))
    status['production_reports_sections_guardrails_unchanged']=all(preservation[k] for k in
        ('reports_unchanged','sections_unchanged','guardrails_unchanged'))
    status['gemini_api_calls']=0
    status['financial_validity']='Awaiting user Gemini review in Antigravity and subsequent Codex review.'
    (run/'status.json').write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')
    conn=sqlite3.connect(Path(info['database']).resolve().as_uri()+'?mode=ro',uri=True)
    try:
        questions=[json.loads(r[0]) for r in conn.execute('SELECT question_json FROM ledger_questions')]
        validations=dict(conn.execute('SELECT validation_status,count(*) FROM section_response_attempts GROUP BY validation_status').fetchall())
    finally:
        conn.close()
    receipts=[json.loads(p.read_text(encoding='utf-8')) for p in (run/'outputs').glob('*.run.json')]
    summary=dict(ticker=info['ticker'],period=info['period'],source_pages=sum(d['page_count'] for d in info['documents']),
                 captures=sum(d['captures'] for d in info['documents']),successful_generation_receipts=len(receipts),
                 reported_prompt_tokens=sum(r.get('prompt_tokens') or 0 for r in receipts),
                 reported_completion_tokens=sum(r.get('completion_tokens') or 0 for r in receipts),
                 reported_reasoning_tokens=sum(r.get('reasoning_tokens') or 0 for r in receipts),
                 token_scope='Successful saved API receipts only; incomplete calls can add unrecorded billed usage. Not a full billing total.',
                 question_records=len(questions),open_question_records=sum(q['status']!='resolved' for q in questions),
                 validation_attempt_counts_including_local_replays=validations,
                 local_open_only_fallbacks=len(status.get('local_open_only_fallbacks',[])),
                 stage2_result_kind=status.get('stage2_result_kind'),gemini_api_calls=0)
    (run/'comparison_metrics.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    prompt_path=run/'gemini/antigravity_evaluation_prompt.md'
    prompt=prompt_path.read_text(encoding='utf-8')
    prompt=prompt.replace('Return audit.md contents; do not claim to have run tools or read PDF images. You receive extracted text only.',
        'Return audit.md contents. The embedded sources are extracted text. When original PDFs are attached, visually verify important tables/signs and record actual physical pages inspected; otherwise state the text-only limitation. Never claim tools or images you did not inspect.')
    prefix='# Execution facts for this review\n\n'+json.dumps(summary,indent=2)+'\n\n'
    if not prompt.startswith('# Execution facts for this review'):
        prompt=prefix+prompt
    scope=('\n\n# Antigravity execution scope\n\nPerform a read-only financial/evidence review. '
           'Save only the versioned audit and supporting calculations under this company\'s evaluations directory '
           'using a fresh current-UTC timestamp followed by _gemini, as required by STOCK_EVALUATION_FORMAT.md. '
           'Do not change production notes, model outputs, source PDFs, prompts or SQLite guardrails; do not run paid models. '
           'Return the absolute saved audit path for the subsequent Codex review.\n')
    if '# Antigravity execution scope' not in prompt:
        prompt+=scope
    if info['ticker']=='NTU':
        prior=run.parent/'20261027T182308Z_codex_review/audit.md'
        if prior.exists():
            copied=run/'inputs/prior_codex_review_reference.md'
            shutil.copy2(prior,copied)
            if '# Prior review reference' not in prompt:
                prompt+='\n\n# Prior review reference\n\nAfter your initial independent source checks, compare against '+copied.as_posix()+'. Treat that prior audit as reviewable claims, not authority; reproduce relevant calculations against the original PDF and report remaining/new errors.\n'
    prompt_path.write_bytes(prompt.encode('utf-8'))
    source_links='\n'.join(f"- [{d['filename']}]({Path(d['path']).as_posix()}) — {d['page_count']} physical pages; SHA-256 `{d['sha256']}`." for d in info['documents'])
    kickoff=(f"# Gemini review request: {info['ticker']} {info['period']}\n\n"
        f"Review the DeepSeek workload trial in `{run.as_posix()}`. This is a read-only evidence evaluation; "
        'save only a new versioned audit and supporting calculations. Do not run models or change production outputs, PDFs, prompts or guardrails.\n\n'
        f"Read `{(ROOT/'docs/STOCK_EVALUATION_FORMAT.md').as_posix()}` section 1A for the mandatory evidence protocol. "
        'Assign claim/finding IDs, verify material calculations against original sources, distinguish historical results, guidance and assumptions, '
        'record physical pages actually inspected and unresolved dependencies. Agreement between models is not verification.\n\n'
        f"Start with `{(run/'comparison_metrics.json').as_posix()}`, `{(run/'inputs/manifest.json').as_posix()}`, "
        f"`{(run/'outputs/stage1.md').as_posix()}` and `{(run/'outputs/publication_assessment.json').as_posix()}`. "
        f"Stage 2 result kind: {summary['stage2_result_kind']}. Read `outputs/stage2.md` when present; "
        'otherwise read `outputs/stage2_withheld_brief.md` and the completion-failure records. '
        'A withheld recovery brief is a narrower task, not a completed full valuation.\n\n'
        'Verify the original PDFs listed below. Consult preserved baseline notes in inputs/, exact requests and section responses '
        'in requests/ and outputs/, source_pages/ text, and the isolated experiment.sqlite ledger as needed. '
        'Load evidence selectively by claim; do not load every repeated ledger/response into one context. '
        'The large antigravity_evaluation_prompt.md is a bundled reference, not a requirement to ingest everything at once.\n\n'
        +source_links+'\n\n'
        'Evaluate errors fixed, repeated and introduced, ledger omissions/unsupported closures, local fallback handling, '
        'cash/portfolio/debt reconciliations, shares, valuation/sensitivity and unsupported missing-disclosure claims. '
        'Separate software integrity improvements from demonstrated financial accuracy. Suggest testable prompt/ledger/guardrail changes '
        'without codifying them. Preserve prior findings and document revisions.\n\n'
        f"Save the full audit in `{run.parent.as_posix()}/<current-UTC-timestamp>_gemini/audit.md` and return the absolute path for Codex's review.\n")
    (run/'gemini/START_HERE.md').write_text(kickoff,encoding='utf-8')
    readme=(f"# {info['ticker']} {info['period']} — Antigravity review\n\n"
        f"Result type: **{summary['stage2_result_kind']}**. Financial validity awaits review.\n\n"
        f"Start with [the concise Antigravity request]({(run/'gemini/START_HERE.md').as_posix()}) and attach/access the original PDFs below. "
        f"The [large bundled reference]({prompt_path.as_posix()}) is available for selective consultation. "
        'It includes the required evidence protocol, preserved baseline note, new Stage 1/Stage 2 outputs, section analyses and full ledger. '
        'Source page presence is not source verification. Historical document-role registrations may be inaccurate; verify actual roles from the PDFs.\n\n'
        +source_links+'\n\n'
        f"[Comparison metrics]({(run/'comparison_metrics.json').as_posix()}) · "
        f"[Stage 1]({(run/'outputs/stage1.md').as_posix()}) · "
        f"[Withholding/publication assessment]({(run/'outputs/publication_assessment.json').as_posix()})\n\n"
        'If full Stage 2 exhausted its budget, the withheld recovery brief is a narrower task; do not treat it as a completed full valuation. '
        'Rejected ledger evidence, local fallbacks and repairs must be assessed separately from valid model answers. '
        'Check source signs/units, cash/debt/portfolio roll-forwards, valuation and sensitivity, unsupported missing-disclosure claims, and whether prior errors were fixed or repeated. '
        'Propose prompt/ledger/guardrail improvements separately; do not change the SQLite registry.\n\n'
        f"Save Gemini's full response under `{run.parent.as_posix()}/<current-UTC-timestamp>_gemini/audit.md`, preserving originals, "
        'and return the absolute path for Codex to review Gemini. No Gemini OpenRouter execution is part of this handoff.\n')
    (run/'gemini/README.md').write_text(readme,encoding='utf-8')
    inputs=[]
    for folder,pattern in [('outputs','*'),('requests','*'),('source_pages','*'),('inputs','*.md')]:
        for path in (run/folder).glob(pattern):
            if path.is_file():
                inputs.append(dict(path=str(path.relative_to(run)),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    handoff=dict(created_utc=datetime.now(timezone.utc).isoformat(),source_pdf_hashes_verified=True,
                 source_documents=info['documents'],preserved_artifacts=inputs,
                 evaluation_prompt_sha256=hashlib.sha256(prompt_path.read_bytes()).hexdigest(),gemini_api_calls=0)
    (run/'gemini/handoff_manifest.json').write_text(json.dumps(handoff,indent=2)+'\n',encoding='utf-8')
    index.append(f"- [{info['ticker']} {info['period']} review pack]({(run/'gemini/README.md').as_posix()}) — {summary['stage2_result_kind']}.")
    summaries.append(summary)

(HERE/'ANTIGRAVITY_HANDOFF.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
(HERE/'completed_comparison_summaries.json').write_text(json.dumps(summaries,indent=2)+'\n',encoding='utf-8')
print(json.dumps([dict(ticker=s['ticker'],stage2_result_kind=s['stage2_result_kind'],successful_receipts=s['successful_generation_receipts']) for s in summaries],indent=2))
