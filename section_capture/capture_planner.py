"""Local page-level capture planning. Heading evidence is navigation, not financial truth."""
from __future__ import annotations

from collections import Counter
import re

DEFAULT_MAX_PAGES = 6
DEFAULT_MAX_CHARS = 24000
TARGET_PAGES = 3
TARGET_CHARS = 12000


def _key(text):
    text = re.sub(r'\b(?:continued|contd|cont)\b', '', text, flags=re.I)
    return re.sub(r'[^\w]+', ' ', text).strip().casefold()


def heading_profile(words, height):
    """Keep native heading text/positions; ignore small running headers and table dates."""
    sizes = Counter(round(float(w.get('size', 0)), 1) for w in words if re.search('[A-Za-z]', w.get('text', '')))
    body_size = sizes.most_common(1)[0][0] if sizes else 9
    threshold = max(9.5, body_size * 1.12)
    lines = []
    for word in sorted(words, key=lambda w: (round(float(w['top']) / 3), float(w['x0']))):
        if not lines or abs(lines[-1]['top'] - float(word['top'])) > 3:
            lines.append(dict(top=float(word['top']), words=[]))
        lines[-1]['words'].append(word)
    candidates = []
    for line in lines:
        ws = line['words']
        text = ' '.join(w['text'] for w in ws).strip()
        size = max(float(w.get('size', 0)) for w in ws)
        if not 35 <= line['top'] <= height - 45 or size < threshold:
            continue
        if not 4 <= len(text) <= 170 or len(re.findall('[A-Za-z]', text)) < 4:
            continue
        large_letters = sum(len(re.findall('[A-Za-z]', w['text'])) for w in ws if float(w.get('size', 0)) >= threshold)
        title_letters = len(re.findall('[A-Za-z]', re.sub(r'\bcontinued\b', '', text, flags=re.I)))
        if large_letters < title_letters * .6:
            continue  # A large note number beside small table-column labels is not a title.
        if re.search(r'^(?:notes to |condensed consolidated financial statements|for the |as at |at \d|\d{1,2} (?:march|september)|unaudited|audited)', text, re.I):
            continue
        if re.fullmatch(r'[\d\s.,()%/–—-]+|(?:Rm|R000|million|Unaudited|Audited|March|September|\d|\s)+', text, re.I):
            continue
        # Body prose or a row with mixed numeric columns is not a heading.
        if text.endswith(('.', ';')) or len(re.findall(r'\b\d[\d,]*\b', text)) >= 3:
            continue
        item = dict(text=text, top=round(line['top'], 2), size=round(size, 2))
        if candidates and abs(candidates[-1]['size'] - size) < .2 and line['top'] - candidates[-1]['top'] <= size * 1.8:
            candidates[-1]['text'] += ' ' + text
        else:
            candidates.append(item)
    top = [h for h in candidates if h['top'] <= min(280, height * .36)]
    # Specific note/subtable headings follow the broad statement/note heading.
    heading = top[-1]['text'] if top else ''
    numbered = [h['text'] for h in top if re.match(r'^\d+(?:\.\d+)*\s+\D', h['text'])]
    namespace = numbered[-1] if numbered else ''
    key = _key(namespace + ' / ' + heading) if heading else ''
    note_id = re.match(r'^(\d+(?:\.\d+)*)\s', namespace)
    period = ''
    for i, line in enumerate(lines):
        line_text = ' '.join(w['text'] for w in line['words'])
        if 150 <= line['top'] <= 350 and re.match(r'for the (?:half )?year ended', line_text, re.I):
            nearby = ' '.join(w['text'] for row in lines[i:i+3] if row['top']-line['top'] < 60 for w in row['words'])
            match = re.search(r'\b\d{1,2}\s+[A-Za-z]+\s+20\d{2}\b', nearby)
            if match:
                period = match.group().casefold()
                break
    instrument = next((name for name, pattern in [
        ('trade_receivables', r'trade receivables'),
        ('principal_portfolios', r'principal book|purchased book debt'),
        ('leases', r'lease'),
        ('tax', r'\btax'),
    ] if re.search(pattern, heading, re.I)), '')
    return dict(heading=heading, topic_key=key, heading_evidence=candidates,
                note_id=note_id.group(1) if note_id else '', period=period, instrument=instrument,
                mixed_topics_on_page=any(h['top'] > min(280, height * .36) and re.match(r'^\d+(?:\.\d+)*\s+[A-Za-z]', h['text']) for h in candidates))


def inspect_page(source, page):
    try:
        native = source.plumber.pages[page - 1]
        result = heading_profile(native.extract_words(extra_attrs=['size']), float(native.height))
        result['inspection'] = 'native_font_and_position'
        return result
    except (AttributeError, IndexError, KeyError, TypeError, ValueError, RuntimeError) as exc:
        return dict(heading='', topic_key='', heading_evidence=[], mixed_topics_on_page=False,
                    inspection='unavailable', inspection_issue=type(exc).__name__)


def plan_capture_groups(captures, profiles, max_pages=DEFAULT_MAX_PAGES, max_chars=DEFAULT_MAX_CHARS):
    """Prefer observed topic starts; retain continuation pages until a hard limit requires a cut."""
    if max_pages < 1 or max_chars < 1:
        raise ValueError('Capture limits must be positive.')
    if len(captures) != len(profiles):
        raise ValueError('Every captured page needs a heading profile.')
    groups = []
    current = []
    current_profiles = []
    chars = 0
    topic = ''
    start_reason = 'requested_range_start'

    def finish():
        if current:
            groups.append(dict(captures=list(current), profiles=list(current_profiles), start_reason=start_reason))

    for cap, profile in zip(captures, profiles, strict=True):
        incoming = profile['topic_key']
        reason = None
        if current:
            divider = len(current) == 1 and len(current[0].text.strip()) < 250 and '|' not in current[0].text
            prior = next((p for p in reversed(current_profiles) if p['topic_key']), {})
            a, b = prior.get('note_id', ''), profile.get('note_id', '')
            related_note = bool(a and b and (a == b or a.startswith(b+'.') or b.startswith(a+'.')))
            prior_instrument = next((p.get('instrument') for p in reversed(current_profiles) if p.get('instrument')), '')
            distinct_instruments = bool(prior_instrument and profile.get('instrument') and prior_instrument != profile['instrument'])
            prior_period = next((p.get('period') for p in reversed(current_profiles) if p.get('period')), '')
            distinct_periods = bool(prior_period and profile.get('period') and prior_period != profile['period'])
            soft_limit = len(current) >= min(TARGET_PAGES, max_pages) or chars + len(cap.text) > min(TARGET_CHARS, max_chars)
            if incoming and (incoming != topic or distinct_periods or distinct_instruments) and not divider:
                if not related_note or distinct_instruments or distinct_periods or profile.get('mixed_topics_on_page') or soft_limit:
                    reason = 'observed_topic_change'
            elif len(current) >= max_pages or chars + len(cap.text) > max_chars:
                reason = 'hard_size_limit'
            elif not incoming and not topic and (len(current) >= min(TARGET_PAGES, max_pages) or chars + len(cap.text) > min(TARGET_CHARS, max_chars)):
                reason = 'fallback_size_limit'
            # Related headings cannot bypass the hard resource ceiling.
            if reason is None and (len(current) >= max_pages or chars + len(cap.text) > max_chars):
                reason = 'hard_size_limit'
        if reason:
            finish()
            current, current_profiles, chars, topic, start_reason = [], [], 0, '', reason
        current.append(cap)
        current_profiles.append(profile)
        chars += len(cap.text)
        if incoming:
            topic = incoming
    finish()
    for i, group in enumerate(groups):
        group['heading'] = next((p['heading'] for p in group['profiles'] if p['heading']), '')
        group['pages'] = [group['captures'][0].page, group['captures'][-1].page]
        group['continuation_cut'] = i + 1 < len(groups) and groups[i+1]['start_reason'] in {'hard_size_limit', 'fallback_size_limit'}
        group['continuation_reason'] = 'size_limit' if group['continuation_cut'] else None
        if i + 1 < len(groups):
            upcoming = next((p['heading'] for p in groups[i+1]['profiles'] if p['heading']), '')
            trailing = group['profiles'][-1]
            if upcoming and trailing.get('mixed_topics_on_page') and any(
                _key(h['text']) == _key(upcoming) for h in trailing.get('heading_evidence', [])
            ):
                group['continuation_cut'] = True
                group['continuation_reason'] = 'note_starts_on_shared_page'
    return groups


def partition_detected_ranges(sections, total_pages):
    """One automatic owner per physical page; retain gaps and overlapping source titles."""
    if total_pages < 1:
        return []
    candidates = []
    for sec in sections:
        start = max(1, min(int(sec.get('start_page', 1)), total_pages))
        end = max(start, min(int(sec.get('end_page', start)), total_pages))
        candidates.append(dict(sec, start_page=start, end_page=end))
    result = []
    previous_owner = None
    for page in range(1, total_pages + 1):
        owners = [i for i,s in enumerate(candidates) if s['start_page'] <= page <= s['end_page']]
        owner = min(owners, key=lambda i: (candidates[i]['end_page']-candidates[i]['start_page'], -int(candidates[i].get('level') or 0), i)) if owners else -1
        if result and owner == previous_owner:
            result[-1]['end_page'] = page
        else:
            base = dict(candidates[owner]) if owner != -1 else dict(title='Unclassified report pages', source='coverage_remainder')
            result.append(dict(base, start_page=page, end_page=page, overlapping_titles=[]))
        titles = result[-1]['overlapping_titles']
        for i in owners:
            title = candidates[i].get('title', '')
            if title and title not in titles:
                titles.append(title)
        previous_owner = owner
    return result
