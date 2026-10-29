"""Persistent question updates. Evidence presence is checked, not financial truth."""
from __future__ import annotations

import hashlib
import json
import re
import uuid

SCHEMA = """
CREATE TABLE IF NOT EXISTS ledger_questions (
    question_id TEXT PRIMARY KEY, suite_sha256 TEXT NOT NULL,
    origin_report_sha256 TEXT NOT NULL, question_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS ledger_events (
    id INTEGER PRIMARY KEY, question_id TEXT NOT NULL, package_id TEXT,
    event_json TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS section_response_attempts (
    id INTEGER PRIMARY KEY, package_id TEXT NOT NULL, response TEXT NOT NULL,
    validation_status TEXT NOT NULL, errors_json TEXT NOT NULL, created_at TEXT NOT NULL
);
"""


def suite_key(conn, sha):
    row = conn.execute("SELECT parent_report_sha256 FROM reports WHERE sha256 = ?", (sha,)).fetchone()
    return (row[0] if row else None) or sha


def records(conn, suite):
    return [json.loads(r[0]) for r in conn.execute(
        "SELECT question_json FROM ledger_questions WHERE suite_sha256 = ? ORDER BY rowid", (suite,)
    )]


def seed_legacy(conn, suite, sha, text, now):
    """Preserve an existing unstructured ledger as one open evidence request."""
    current = records(conn, suite)
    if not (text or '').strip() or (current and text.strip() == render(current).strip()):
        return
    qid = 'Q-' + hashlib.sha256((suite + text).encode()).hexdigest()[:16]
    if any(q['question_id'] == qid for q in current):
        return
    question = dict(question_id=qid, question=text.strip(), priority='high',
                    target_document='See original ledger', target_section='See original ledger',
                    evidence_required='Resolve each original item against source evidence.',
                    closure_condition='All original items must be accounted for with evidence.',
                    status='open', answer='', evidence=[], legacy=True)
    store(conn, suite, sha, question, None, now)


def store(conn, suite, sha, question, package_id, now):
    data = json.dumps(question, ensure_ascii=False)
    conn.execute("INSERT INTO ledger_questions VALUES (?, ?, ?, ?) "
                 "ON CONFLICT(question_id) DO UPDATE SET question_json=excluded.question_json",
                 (question['question_id'], suite, sha, data))
    conn.execute("INSERT INTO ledger_events(question_id, package_id, event_json, created_at) VALUES (?, ?, ?, ?)",
                 (question['question_id'], package_id, data, now))


def render(questions):
    open_items = [q for q in questions if q['status'] != 'resolved']
    if not open_items:
        return 'No open questions. Ledger state validated; source truth still requires review.'
    return '\n\n'.join(
        f"- {q['question_id']} [{q['priority']}] [{q['status']}] "
        f"Target: {q['target_document']} / {q['target_section']}\n"
        f"  Question: {q['question']}\n  Evidence required: {q['evidence_required']}\n"
        f"  Closure condition: {q['closure_condition']}\n"
        f"  Latest answer: {q.get('answer') or 'Pending: ' + q['target_section']}"
        for q in open_items
    )


def render_prompt(questions, context=None, limit=12):
    """Keep evidence requests/closure conditions, omit copied answer narratives."""
    pending = [q for q in questions if q['status'] != 'resolved']
    context = context or {}
    source = context.get('source') or {}
    section_ids = context.get('section_ids') or []
    focus = context.get('heading','') + ' ' + ' '.join(s.get('text','')[:1500] for s in context.get('selections',[]))
    words = set(re.findall(r'[a-z]{4,}',focus.lower()))

    def relevance(q):
        target = q['target_document']
        score = 30 if target in {source.get('filename'),source.get('sha256')} else 0
        score += 20 if any(sid in q['target_section'] for sid in section_ids) else 0
        score += 3 * len(words & set(re.findall(r'[a-z]{4,}',q['question'].lower())))
        return score + {'high':3,'medium':2,'low':1}[q['priority']]

    chosen = sorted(pending,key=relevance,reverse=True)[:limit]
    header = (f'Current-capture questions: {len(chosen)} of {len(pending)} open records. '
              'Unsent questions remain open in the app and in the complete Stage 1 ledger; omission never means resolution.\n')
    return header + '\n'.join(json.dumps({key: q[key] for key in (
        'question_id', 'status', 'priority', 'target_document', 'target_section',
        'question', 'evidence_required', 'closure_condition')}, ensure_ascii=False) for q in chosen)


def contract_prompt(template):
    replacement = '''### 4. Updated Open Questions Ledger
Return exactly one fenced JSON object for ledger changes, not a replacement ledger:
```json
{"ledger_version": 1, "updates": [], "new_questions": []}
```
The app retains omitted questions. Never renumber existing question IDs. Do not copy
unchanged questions. An empty updates/new_questions pair is valid.
For each update supply question_id, status (open, partial, contradicted, resolved),
answer, and evidence (a list). A resolved/partial/contradicted update requires evidence
objects with source_sha256, physical_page (integer), and quote copied exactly from
the CURRENT supplied capture (whitespace-only differences are allowed). Prefer a
short literal anchor (about 8–50 characters) from one supplied cell or sentence,
preserving numbers and signs. Do not reconstruct a full row across wrapped labels
or quote Markdown separators. The anchor locates evidence; it does not prove the answer.
Explain the answer and satisfy the closure condition before resolving. Keep a partly
answered question partial if essential evidence remains pending or is deferred to a
new question. A citation alone does not establish truth. Legacy imported ledgers
cannot be closed automatically: create separate questions and leave them for review.
For each new question supply question, priority (high/medium/low), target_document
(filename or source hash), target_section, evidence_required and closure_condition.
New questions must request specific source evidence/reconciliation, period, units and
scope where relevant, allow benign explanations and identify forecast consequences.
Do not assign IDs to new questions; the app assigns stable IDs across the report suite.
Section 3 may explain new questions, but the authoritative changes belong in this JSON.

'''
    template = re.sub(r'(?ms)^### 4\. Updated Open Questions Ledger.*?(?=^### 5\.|\Z)',
                      lambda _: replacement, template)
    template = template.replace('Question ID & original question', 'Question ID (do not repeat the original question)')
    return ("STRUCTURED LEDGER CONTRACT TAKES PRIORITY OVER LEGACY COPY-LEDGER WORDING BELOW.\n"
            "The app retains existing questions; output only changed/new records in Section 4. "
            "Keep Sections 1-3 concise: question IDs, short answers, exact figures/citations; no repeated question text "
            "or accounting tutorials. Do not duplicate long answers in prose and JSON. Prefer at most five new "
            "material questions per capture; consolidate related evidence requests. If further material issues "
            "need investigation, retain them explicitly in a backlog question rather than omit them. "
            "Never force resolution to fit an answer budget.\n\n" + template)


def apply_delta(conn, sha, package_id, manifest, response, now):
    suite = suite_key(conn, sha)
    current = records(conn, suite)
    errors = []
    blocks = re.findall(r'```json\s*\n(.*?)```', response, re.S | re.I)
    try:
        payloads = [json.loads(block) for block in blocks]
        payloads = [p for p in payloads if isinstance(p, dict) and 'ledger_version' in p]
        if len(payloads) != 1:
            raise ValueError('Exactly one ledger JSON update is required.')
        payload = payloads[0]
        if payload.get('ledger_version') != 1 or not isinstance(payload.get('updates'), list) or not isinstance(payload.get('new_questions'), list):
            raise ValueError('Invalid ledger version or update arrays.')
        known = {q['question_id']: q for q in current}
        proposed = []
        seen = set()
        for update in payload['updates']:
            if not isinstance(update, dict):
                raise ValueError('Each update must be an object.')
            qid = update.get('question_id')
            if qid not in known or qid in seen:
                raise ValueError('Unknown or duplicate question ID.')
            seen.add(qid)
            status = update.get('status')
            if status not in {'open', 'partial', 'contradicted', 'resolved'}:
                raise ValueError('Unknown question status.')
            answer = update.get('answer')
            evidence = update.get('evidence')
            if not isinstance(answer, str) or not answer.strip() or not isinstance(evidence, list):
                raise ValueError('Update requires an answer and evidence list.')
            if status != 'open' and not evidence:
                raise ValueError('Answer/closure requires evidence from the supplied capture.')
            if status == 'resolved' and known[qid].get('legacy'):
                raise ValueError('Imported legacy ledgers require manual review before closure.')
            for ev in evidence:
                if not isinstance(ev, dict) or ev.get('source_sha256') != sha or type(ev.get('physical_page')) is not int:
                    raise ValueError('Evidence must identify this source and a physical page.')
                quote = ev.get('quote')
                page_texts = [s.get('text', '') for s in manifest.get('selections', [])
                              if s.get('physical_page') == ev['physical_page']]
                normalize = lambda text: re.sub(r'\s+', ' ', text).strip()
                if not isinstance(quote, str) or len(quote.strip()) < 8 or not any(normalize(quote) in normalize(t) for t in page_texts):
                    raise ValueError(f'Evidence quote for {qid}, physical page {ev["physical_page"]} is not literal: '
                                     f'{str(quote)[:100]!r}. Use a short verbatim excerpt or keep this question open without claiming resolution.')
            proposed.append(dict(known[qid], status=status, answer=answer, evidence=evidence))
        signatures = {q['question'].strip().casefold() for q in current}
        for question in payload['new_questions']:
            fields = ('question', 'priority', 'target_document', 'target_section', 'evidence_required', 'closure_condition')
            if not isinstance(question, dict) or any(not isinstance(question.get(f), str) or not question[f].strip() for f in fields):
                raise ValueError('New question is missing required evidence/target/closure fields.')
            if question['priority'] not in {'high', 'medium', 'low'}:
                raise ValueError('Unknown priority.')
            signature = question['question'].strip().casefold()
            if signature in signatures:
                continue
            signatures.add(signature)
            proposed.append(dict({f: question[f].strip() for f in fields},
                                 question_id='Q-' + uuid.uuid4().hex[:16], status='open', answer='', evidence=[]))
    except (ValueError, TypeError, AttributeError, KeyError) as exc:
        errors.append(str(exc))
        proposed = []
    conn.execute("INSERT INTO section_response_attempts(package_id,response,validation_status,errors_json,created_at) VALUES (?,?,?,?,?)",
                 (package_id, response, 'rejected' if errors else 'valid', json.dumps(errors), now))
    if errors:
        return None, errors
    for q in proposed:
        store(conn, suite, sha, q, package_id, now)
    return render(records(conn, suite)), []
