"""Coarse native-heading scan for navigation, never evidence of section contents."""
from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .db import get_questions_ledger, get_report_map, upsert_report

ROOT = Path(__file__).resolve().parents[1]
CACHE_ROOT = ROOT / 'documents/maps'
QUESTIONS_ROOT = ROOT / 'documents/questions'
ORIENTATION_STAGE = "00-report-orientation"
ORIENTATION_VERSION = "v1.0.0"
ORIENTATION_PATH = ROOT / f"prompts/mining/{ORIENTATION_STAGE}/{ORIENTATION_VERSION}/prompt.md"


def get_orientation_path(sector: str = "mining") -> Path:
    sec = sector.lower().strip() if sector else "mining"
    custom = ROOT / f"prompts/{sec}/{ORIENTATION_STAGE}/{ORIENTATION_VERSION}/prompt.md"
    if custom.exists():
        return custom
    return ORIENTATION_PATH

KINDS = [
    ('financial_notes', 'Financial notes', r'NOTES TO (?:THE )?(?:SUMMARISED )?CONSOLIDATED (?:ANNUAL )?FINANCIAL STATEMENTS'),
    ('financial_statements', 'Primary financial statements', r'(?:CONSOLIDATED )?STATEMENT OF (?:FINANCIAL POSITION|PROFIT|CASH FLOWS|CHANGES IN EQUITY|COMPREHENSIVE INCOME)'),
    ('statements_overview', 'Financial statements overview / contents', r'ANNUAL FINANCIAL STATEMENTS'),
    ('highlights', 'Highlights', r'KEY (?:F[Y]?\d+ )?FEATURES|FINANCIAL HIGHLIGHTS|KEY HIGHLIGHTS'),
    ('ceo_commentary', "CEO's statement", r'CHIEF EXECUTIVE OFFICER S STATEMENT|CHIEF EXECUTIVE S (?:STATEMENT|REVIEW)|CEO (?:STATEMENT|REVIEW|REPORT)'),
    ('financial_review', 'Financial review', r'FINANCIAL REVIEW|CHIEF FINANCIAL OFFICER S (?:REVIEW|REPORT)'),
    ('operating_review', 'Operating review', r'OPERATING REVIEW|OPERATIONAL REVIEW'),
    ('apms', 'Alternative performance measures', r'ALTERNATIVE PERFORMANCE MEASURES'),
    ('production_summary', 'Group production summary', r'GROUP PRODUCTION SUMMARY'),
    ('glossary', 'Glossary', r'GLOSSARY'),
    ('corporate_information', 'Corporate information', r'CORPORATE INFORMATION'),
    ('reporting_suite', 'Reporting suite', r'OUR REPORTING SUITE'),
    ('other_items_overview', 'Other items overview / contents', r'OTHER ITEMS'),
]
STATEMENTS = {
    'financial_position': r'STATEMENT OF FINANCIAL POSITION',
    'profit_or_loss': r'PROFIT OR LOSS',
    'other_comprehensive_income': r'OTHER COMPREHENSIVE INCOME',
    'cash_flows': r'STATEMENT OF CASH FLOWS',
    'changes_in_equity': r'STATEMENT OF CHANGES IN EQUITY',
}


def clean_single_line_text(text: str | None) -> str:
    """Strips tabs, line breaks, non-breaking spaces, and collapses whitespace."""
    if not text:
        return ""
    cleaned = re.sub(r"[\r\n\t\xa0]+", " ", str(text))
    cleaned = re.sub(r" {2,}", " ", cleaned)
    return cleaned.strip()


def normalized(words):
    text = ' '.join(w['text'] for w in words).upper()
    return re.sub(r'[^A-Z0-9]+', ' ', text).strip()


def heading_hits(words):
    # Large display titles anywhere, and smaller running headings near the top.
    # Ordinary body text/contents entries do not establish section starts.
    candidates = [w for w in words if w['size'] >= 12 or (w['size'] >= 9.5 and w['top'] < 115)]
    text = normalized(candidates)
    hits = []
    for kind, title, pattern in KINDS:
        match = re.search(r'\b(?:' + pattern + r')\b', text)
        if match:
            # The notes header includes 'annual financial statements'.
            if kind == 'statements_overview' and any(h['kind'] == 'financial_notes' for h in hits):
                continue
            hits.append({'kind': kind, 'title': title, 'matched_heading': match.group()})
    return hits, text


def scan_report(source, progress=None):
    """Scan each physical page. Missing running headers may imply continuation."""
    sections, sightings, unclassified, scan_issues = [], [], [], []
    previous = None
    for page_number, page in enumerate(source.plumber.pages, 1):
        if progress and progress(page_number - 1, source.page_count) is False:
            raise InterruptedError('Section scan cancelled; no complete map was saved.')
        try:
            words = page.extract_words(extra_attrs=['size'])
        except Exception as exc:
            words = []
            scan_issues.append({'physical_page': page_number, 'description': f'Native heading scan failed: {exc}'})
        sides = {}
        for side in ('left', 'right'):
            group = [w for w in words if ((w['x0'] + w['x1'])/2 < page.width/2) == (side == 'left')]
            sides[side] = heading_hits(group)
        all_hits, _ = heading_hits(words)
        left, right = sides['left'][0], sides['right'][0]
        left_kinds, right_kinds = {h['kind'] for h in left}, {h['kind'] for h in right}
        if left and right and left_kinds != right_kinds:
            # Different actual headings establish relative regions, not inferred printed pages.
            units = [('left', left, sides['left'][1]), ('right', right, sides['right'][1])]
        elif all_hits:
            units = [('full', all_hits, heading_hits(words)[1])]
        else:
            units = [('full', [], '')]
        for location, hits, text in units:
            hit = hits[0] if hits else None
            inferred = False
            if not hit and len(words) >= 30 and previous and previous['kind'] != 'unclassified':
                hit = {key: previous[key] for key in ('kind', 'title')}
                inferred = True
            if not hit:
                hit = {'kind': 'unclassified', 'title': 'Unclassified / cover or other material'}
                unclassified.append(page_number)
            position = {'physical_page': page_number, 'location': location, 'printed_label': None}
            if sections and sections[-1]['kind'] == hit['kind']:
                section = sections[-1]
                section['end'] = dict(position)
            else:
                section = {'section_id': f'D{len(sections)+1:03}', 'kind': hit['kind'], 'title': hit['title'],
                           'start': dict(position), 'end': dict(position), 'heading_evidence': [],
                           'inferred_continuation_pages': []}
                sections.append(section)
            if inferred:
                section['inferred_continuation_pages'].append(page_number)
            elif hit.get('matched_heading'):
                # Store only boundary evidence to keep this a major-section map.
                if not section['heading_evidence']:
                    section['heading_evidence'].append({**position, 'heading': hit['matched_heading']})
            if hit['kind'] == 'financial_statements':
                # Use each relative region even when both belong to the same section.
                for side, (side_hits, side_text) in sides.items():
                    if any(h['kind'] == 'financial_statements' for h in side_hits):
                        for statement_kind, pattern in STATEMENTS.items():
                            if re.search(pattern, side_text):
                                sighting = {'kind': statement_kind, 'physical_page': page_number, 'location': side}
                                if sighting not in sightings:
                                    sightings.append(sighting)
            previous = section
    if progress:
        progress(source.page_count, source.page_count)
    result = {
        'schema_version': 'coarse_report_map_v1', 'map_id': 'map-' + uuid.uuid4().hex,
        'created_at': datetime.now(timezone.utc).isoformat(), 'source_sha256': source.sha256,
        'source_filename': source.path.name, 'physical_page_count': source.page_count,
        'status': 'automatic_draft', 'method': 'native_large_titles_and_running_headings_v1',
        'scanned_physical_pages': list(range(1, source.page_count + 1)),
        'sections': sections, 'primary_statement_sightings': sightings,
        'unclassified_physical_pages': sorted(set(unclassified)), 'issues': scan_issues,
        'limitations': ['Navigation only; section contents have not been analysed or supplied to the model by this scan.',
                       'Ranges between heading observations are inferred and need checking; native-text scans may miss headings.',
                       'Relative left/right locations do not establish printed-page labels. No OCR or full financial verification.'],
    }
    validate_map(result, source.sha256, source.page_count)
    return result


def _position(endpoint, end=False):
    location = endpoint['location']
    fraction = {'left': (0, .5), 'right': (.5, 1), 'full': (0, 1)}[location][int(end)]
    return endpoint['physical_page'] - 1 + fraction


def validate_map(mapping, source_sha256, page_count):
    if not re.fullmatch(r'[0-9a-f]{64}', source_sha256) or not isinstance(page_count, int) or page_count < 1:
        raise ValueError('Invalid source identity/page count for report map.')
    if mapping['schema_version'] != 'coarse_report_map_v1' or mapping['source_sha256'] != source_sha256 or mapping['physical_page_count'] != page_count:
        raise ValueError('Report map does not match this PDF identity/page count.')
    if mapping['status'] != 'automatic_draft':
        raise ValueError('Unsupported report-map status; a scan cannot establish review or confirmation.')
    if mapping['scanned_physical_pages'] != list(range(1, page_count + 1)):
        raise ValueError('Report map scan is incomplete.')
    cursor, ids = 0, set()
    for section in mapping['sections']:
        start, end = _position(section['start']), _position(section['end'], True)
        if section['section_id'] in ids or start != cursor or end <= start or end > page_count:
            raise ValueError('Report map has duplicate IDs, gaps, overlaps or invalid boundaries.')
        ids.add(section['section_id'])
        cursor = end
    if cursor != page_count:
        raise ValueError('Report map does not account for all physical pages.')


def load_cached_map(source_sha256, page_count, cache_root=None):
    if not re.fullmatch(r'[0-9a-f]{64}', source_sha256):
        return None
    mapping = get_report_map(source_sha256, db_path=cache_root)
    if mapping is not None:
        try:
            validate_map(mapping, source_sha256, page_count)
            return mapping
        except (ValueError, KeyError, TypeError):
            return None
    return None


def save_map(mapping, cache_root=None):
    validate_map(mapping, mapping['source_sha256'], mapping['physical_page_count'])
    return upsert_report(
        sha256=mapping['source_sha256'],
        filename=mapping.get('source_filename', ''),
        physical_page_count=mapping['physical_page_count'],
        report_map=mapping,
        db_path=cache_root,
    )


def _range(section):
    def label(endpoint):
        return f"{endpoint['physical_page']} {endpoint['location']}"
    return label(section['start']) + ' – ' + label(section['end'])


def _part_location(part) -> str:
    width = part['page_size_points'][0]
    x0, x1 = part['bbox'][0], part['bbox'][2]
    if x1 <= width * 0.55:
        return 'left'
    if x0 >= width * 0.45:
        return 'right'
    return 'full'


def register_subsection(mapping, subheading: str, selections=(), heading: str = "") -> list[str]:
    """Add or update a subsection under the matched major section in mapping and return its subsection ID(s)."""
    subheading = clean_single_line_text(subheading)
    heading = clean_single_line_text(heading)
    if not mapping or not subheading or not selections:
        return []
    matched_sections = []
    for section in mapping.get('sections', []):
        for part in selections:
            width = part['page_size_points'][0]
            start = part['physical_page'] - 1 + part['bbox'][0] / width
            end = part['physical_page'] - 1 + part['bbox'][2] / width
            if start < _position(section['end'], True) and end > _position(section['start']):
                matched_sections.append(section)
                break
    if not matched_sections:
        return []
    parent = matched_sections[0]
    if heading:
        parent['parent_heading'] = heading
    subs = parent.setdefault('subsections', [])
    sorted_parts = sorted(selections, key=lambda p: (p['physical_page'], p['bbox'][0], p['bbox'][1]))
    first_part, last_part = sorted_parts[0], sorted_parts[-1]
    start_loc = _part_location(first_part)
    end_loc = _part_location(last_part)
    if first_part['physical_page'] == last_part['physical_page'] and start_loc != end_loc:
        start_loc = end_loc = 'full'
    start_ep = {'physical_page': first_part['physical_page'], 'location': start_loc, 'printed_label': None}
    end_ep = {'physical_page': last_part['physical_page'], 'location': end_loc, 'printed_label': None}
    for existing in subs:
        if existing.get('title', '').strip().lower() == subheading.lower():
            existing['title'] = subheading
            existing['start'] = start_ep
            existing['end'] = end_ep
            return [existing['subsection_id']]
    sub_id = f"{parent['section_id']}.{len(subs) + 1}"
    subs.append({
        'subsection_id': sub_id,
        'parent_id': parent['section_id'],
        'title': subheading,
        'start': start_ep,
        'end': end_ep,
    })
    return [sub_id]


def _norm_heading(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', ' ', (text or '').lower()).strip()


def section_requires_subheading(mapping, heading: str = "", selections=()) -> str | None:
    """If the matched section or main heading already has subsections, return a label like 'D006 (D006.1)'."""
    if not mapping:
        return None
    norm_h = _norm_heading(re.sub(r'^D\d{3}\s*[—:\-]\s*', '', clean_single_line_text(heading), flags=re.IGNORECASE))
    for section in mapping.get('sections', []):
        subs = section.get('subsections') or []
        if not subs:
            continue
        overlaps = False
        for part in selections:
            width = part['page_size_points'][0]
            start = part['physical_page'] - 1 + part['bbox'][0] / width
            end = part['physical_page'] - 1 + part['bbox'][2] / width
            if start < _position(section['end'], True) and end > _position(section['start']):
                overlaps = True
                break
        heading_matches = False
        if norm_h:
            candidates = [
                _norm_heading(section.get('title', '')),
                _norm_heading(section.get('parent_heading', '')),
                *[_norm_heading(ev.get('heading', '')) for ev in section.get('heading_evidence', [])],
            ]
            heading_matches = any(c and (norm_h == c or norm_h in c or c in norm_h) for c in candidates)
        if overlaps or heading_matches:
            sub_list = ', '.join(s['subsection_id'] for s in subs)
            return f"{section['section_id']} ({sub_list})"
    return None


def matching_section_ids(mapping, selections=()) -> list[str]:
    if not mapping or not selections:
        return []
    matched = []
    for section in mapping.get('sections', []):
        for part in selections:
            width = part['page_size_points'][0]
            start = part['physical_page'] - 1 + part['bbox'][0] / width
            end = part['physical_page'] - 1 + part['bbox'][2] / width
            if start < _position(section['end'], True) and end > _position(section['start']):
                matched.append(section['section_id'])
                break
    return matched


def report_overview(mapping, selections=(), sector: str = "mining"):
    orient_path = get_orientation_path(sector)
    lines = [orient_path.read_text(encoding='utf-8'), '\n## Report navigation context',
             f"Report: {mapping['source_filename']}", f"Physical PDF pages: {mapping['physical_page_count']}",
             f"Map status: {mapping['status']} — navigation only; not financial analysis or confirmation.",
             'Ranges below use original physical PDF pages, counted from 1; labels left/right describe regions.',
             '\n| ID | Major section | Physical page range | Evidence in this request |',
             '| --- | --- | --- | --- |']
    for section in mapping['sections']:
        overlaps = []
        for part in selections:
            width = part['page_size_points'][0]
            start = part['physical_page']-1 + part['bbox'][0]/width
            end = part['physical_page']-1 + part['bbox'][2]/width
            if start < _position(section['end'], True) and end > _position(section['start']):
                page_ref = f"p. {part['physical_page']}"
                if page_ref not in overlaps:
                    overlaps.append(page_ref)
        status = f"Partial selected evidence: {section['section_id']} ({', '.join(overlaps)})" if overlaps else 'Not included here; available for possible later reading'
        title = section['title'].replace('|', '\\|').replace('\n', ' ')
        lines.append(f"| {section['section_id']} | {title} | {_range(section)} | {status} |")
        has_explicit_sub_ids = any('.' in (p.get('section_id') or '') for p in selections)
        for sub in section.get('subsections', []):
            sub_overlaps = []
            for part in selections:
                part_sids = [s.strip() for s in (part.get('section_id') or '').split(',') if s.strip()]
                if has_explicit_sub_ids:
                    is_match = sub['subsection_id'] in part_sids
                else:
                    width = part['page_size_points'][0]
                    start = part['physical_page'] - 1 + part['bbox'][0] / width
                    end = part['physical_page'] - 1 + part['bbox'][2] / width
                    is_match = start < _position(sub['end'], True) and end > _position(sub['start'])
                if is_match:
                    page_ref = f"p. {part['physical_page']}"
                    if page_ref not in sub_overlaps:
                        sub_overlaps.append(page_ref)
            sub_status = f"Partial selected evidence: {sub['subsection_id']} ({', '.join(sub_overlaps)})" if sub_overlaps else 'Subsection recorded in map; not included in this request'
            sub_title = sub['title'].replace('|', '\\|').replace('\n', ' ')
            lines.append(f"| {sub['subsection_id']} | ↳ {sub_title} | {_range(sub)} | {sub_status} |")
    if mapping['primary_statement_sightings']:
        lines.append('\nPrimary-statement heading sightings (draft navigation, not inspected statement values):')
        for item in mapping['primary_statement_sightings']:
            lines.append(f"- {item['kind'].replace('_', ' ')}: physical PDF p. {item['physical_page']}, {item['location']}.")
    if mapping['unclassified_physical_pages']:
        lines.append('\nUnclassified physical pages: ' + ', '.join(map(str, mapping['unclassified_physical_pages'])) + '. Their purpose has not been established by the scan.')
    if mapping['issues']:
        lines.append(f"\nNative-scan issues: {len(mapping['issues'])}; consult the saved map details. These areas need checking.")
    lines.extend(['\nMap limits:'] + ['- ' + note for note in mapping['limitations']])
    return '\n'.join(lines) + '\n'


def load_questions_ledger(source_sha256: str, questions_root: Path | None = None) -> str:
    if not re.fullmatch(r'[0-9a-f]{64}', source_sha256):
        return ""
    return get_questions_ledger(source_sha256, db_path=questions_root)


def save_questions_ledger(source_sha256: str, text: str, questions_root: Path | None = None) -> Path:
    if not re.fullmatch(r'[0-9a-f]{64}', source_sha256):
        raise ValueError('Invalid source SHA-256 for questions ledger.')
    return upsert_report(
        sha256=source_sha256,
        questions_ledger=text.strip(),
        db_path=questions_root,
    )
