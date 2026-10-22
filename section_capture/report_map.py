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
    if mapping['status'] not in ('automatic_draft', 'manual_outline'):
        raise ValueError('Unsupported report-map status; expected automatic_draft or manual_outline.')
    if mapping['scanned_physical_pages'] != list(range(1, page_count + 1)):
        raise ValueError('Report map scan is incomplete.')

    if mapping['status'] == 'automatic_draft':
        cursor, ids = 0, set()
        for section in mapping['sections']:
            start, end = _position(section['start']), _position(section['end'], True)
            if section['section_id'] in ids or start != cursor or end <= start or end > page_count:
                raise ValueError('Report map has duplicate IDs, gaps, overlaps or invalid boundaries.')
            ids.add(section['section_id'])
            cursor = end
        if cursor != page_count:
            raise ValueError('Report map does not account for all physical pages.')
    else:
        # manual_outline: allows multiple sections sharing physical pages (e.g. 2-up spreads)
        ids = set()
        for section in mapping['sections']:
            if section['section_id'] in ids:
                raise ValueError(f"Report map has duplicate ID: {section['section_id']}")
            ids.add(section['section_id'])
            start_p = section['start']['physical_page']
            end_p = section['end']['physical_page']
            if start_p < 1 or end_p > page_count or end_p < start_p:
                raise ValueError(f"Section {section['section_id']} has invalid page boundaries ({start_p}–{end_p}).")


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


def assign_section_ids(items: list[dict]) -> list[str]:
    """Assign stable IDs to items, generating <prev_id>-ins for newly inserted items."""
    has_any_existing = any(bool(item.get("section_id")) for item in items)
    if not has_any_existing:
        return [f"D{i+1:03d}" for i in range(len(items))]

    assigned: list[str] = []
    used_ids: set[str] = {item["section_id"] for item in items if item.get("section_id")}

    for i, item in enumerate(items):
        sid = item.get("section_id")
        if sid:
            assigned.append(sid)
            continue
        # Newly inserted section
        if i > 0 and assigned:
            prev_id = assigned[i - 1]
        elif i + 1 < len(items) and items[i + 1].get("section_id"):
            prev_id = items[i + 1]["section_id"]
        else:
            prev_id = "D001"

        base_prefix = re.sub(r"-ins\d*$", "", prev_id)
        candidate = f"{base_prefix}-ins"
        counter = 2
        while candidate in used_ids:
            candidate = f"{base_prefix}-ins{counter}"
            counter += 1
        used_ids.add(candidate)
        assigned.append(candidate)

    return assigned


def build_manual_section_map(source, sections_data: list[dict]) -> dict:
    """Build a valid contiguous coarse_report_map_v1 from manually captured sections.

    Each item in sections_data must have 'title' and 'start_page' (1-based physical page),
    and optionally 'section_id' to preserve stable IDs across in-flight edits.
    Newly inserted sections receive a '-ins' suffix based on their predecessor.
    """
    page_count = source.page_count
    cleaned = []
    for item in sections_data:
        title = clean_single_line_text(item.get("title", ""))
        try:
            p = int(item.get("start_page", 1))
        except (ValueError, TypeError):
            p = 1
        sid = item.get("section_id")
        if title and 1 <= p <= page_count:
            cleaned.append({"title": title, "start_page": p, "section_id": sid})

    cleaned.sort(key=lambda s: s["start_page"])
    if not cleaned:
        cleaned = [{"title": "General Material", "start_page": 1, "section_id": None}]

    sections = []
    seq_counter = 1
    for i, item in enumerate(cleaned):
        existing_sid = item.get("section_id")
        if existing_sid and "-ins" in existing_sid:
            sec_id = existing_sid
        else:
            sec_id = f"D{seq_counter:03d}"
            seq_counter += 1
        start_p = item["start_page"]
        # Find next section with a strictly greater start page
        next_start = None
        for next_item in cleaned[i + 1:]:
            if next_item["start_page"] > start_p:
                next_start = next_item["start_page"]
                break
        end_p = (next_start - 1) if next_start is not None else page_count
        end_p = max(start_p, end_p)
        sections.append({
            "section_id": sec_id,
            "kind": "unclassified",
            "title": item["title"],
            "start": {"physical_page": start_p, "location": "full", "printed_label": None},
            "end": {"physical_page": end_p, "location": "full", "printed_label": None},
            "subsections": [],
            "heading_evidence": [],
            "inferred_continuation_pages": list(range(start_p, end_p + 1)),
        })

    mapping = {
        "schema_version": "coarse_report_map_v1",
        "source_sha256": source.sha256,
        "source_filename": getattr(source, "filename", Path(source.path).name if getattr(source, "path", None) else "report.pdf"),
        "physical_page_count": page_count,
        "status": "manual_outline",
        "scanned_physical_pages": list(range(1, page_count + 1)),
        "sections": sections,
        "primary_statement_sightings": [],
        "unclassified_physical_pages": [],
        "issues": [],
        "limitations": [
            "Manually recorded outline of major report sections.",
            "Sections account contiguously for physical PDF pages.",
        ],
    }
    validate_map(mapping, source.sha256, page_count)
    return mapping


def preview_inserted_section_id(
    mapping: dict | None, start_page: int, page_count: int
) -> tuple[str, str]:
    """Calculate the assigned section ID and partition description for a proposed insertion."""
    if not mapping or not mapping.get("sections"):
        return "D001", f"Initial section spanning pages {start_page} to {page_count}."

    sections = mapping.get("sections", [])
    used_ids = {s["section_id"] for s in sections}

    exact_match = None
    target_idx = -1
    for i, s in enumerate(sections):
        if s["start"]["physical_page"] == start_page:
            exact_match = s
            target_idx = i
            break
        elif s["start"]["physical_page"] < start_page <= s["end"]["physical_page"]:
            target_idx = i

    if target_idx == -1:
        if start_page < sections[0]["start"]["physical_page"]:
            base_prefix = "D001"
            cand = f"{base_prefix}-ins"
            counter = 2
            while cand in used_ids:
                cand = f"{base_prefix}-ins{counter}"
                counter += 1
            first_p = sections[0]["start"]["physical_page"]
            return cand, f"Inserts before first section: {cand} covers p. {start_page}–{first_p - 1}."
        else:
            prev_id = sections[-1]["section_id"]
            base_prefix = re.sub(r"-ins\d*$", "", prev_id)
            cand = f"{base_prefix}-ins"
            counter = 2
            while cand in used_ids:
                cand = f"{base_prefix}-ins{counter}"
                counter += 1
            return cand, f"Extends outline: {cand} starts at p. {start_page} to p. {page_count}."
    else:
        target_sec = sections[target_idx]
        prev_id = target_sec["section_id"]
        base_prefix = re.sub(r"-ins\d*$", "", prev_id)
        cand = f"{base_prefix}-ins"
        counter = 2
        while cand in used_ids:
            cand = f"{base_prefix}-ins{counter}"
            counter += 1
        if exact_match is not None:
            desc = (
                f"Shares start page {start_page} with {prev_id} ('{target_sec['title']}'): "
                f"{cand} will cover p. {start_page}–{target_sec['end']['physical_page']}."
            )
        else:
            desc = (
                f"Splits {prev_id} ('{target_sec['title']}'): {prev_id} will now end at p. {start_page - 1}; "
                f"{cand} will cover p. {start_page}–{target_sec['end']['physical_page']}."
            )
        return cand, desc


def insert_section_into_report_map(
    mapping: dict, title: str, start_page: int, page_count: int
) -> tuple[dict, str]:
    """Insert a new section into an existing report map while capturing.

    Assigns a stable ID with '-ins' suffix based on predecessor, preserving all existing IDs.
    Returns (mapping, assigned_section_id).
    """
    clean_title = clean_single_line_text(title)
    if not clean_title:
        raise ValueError("Section title cannot be empty.")
    if start_page < 1 or start_page > page_count:
        raise ValueError(f"Start page must be between 1 and {page_count}.")

    sections = mapping.setdefault("sections", [])
    if not sections:
        new_sec_id = "D001"
        mapping["sections"] = [{
            "section_id": new_sec_id,
            "kind": "unclassified",
            "title": clean_title,
            "start": {"physical_page": start_page, "location": "full", "printed_label": None},
            "end": {"physical_page": page_count, "location": "full", "printed_label": None},
            "subsections": [],
            "heading_evidence": [],
            "inferred_continuation_pages": list(range(start_page, page_count + 1)),
        }]
        return mapping, new_sec_id

    used_ids = {s["section_id"] for s in sections}

    exact_match = None
    target_idx = -1
    for i, s in enumerate(sections):
        if s["start"]["physical_page"] == start_page:
            exact_match = s
            target_idx = i
            break
        elif s["start"]["physical_page"] < start_page <= s["end"]["physical_page"]:
            target_idx = i

    if target_idx == -1:
        if start_page < sections[0]["start"]["physical_page"]:
            base_prefix = "D001"
            cand = f"{base_prefix}-ins"
            counter = 2
            while cand in used_ids:
                cand = f"{base_prefix}-ins{counter}"
                counter += 1
            old_end = sections[0]["start"]["physical_page"] - 1
        else:
            prev_id = sections[-1]["section_id"]
            base_prefix = re.sub(r"-ins\d*$", "", prev_id)
            cand = f"{base_prefix}-ins"
            counter = 2
            while cand in used_ids:
                cand = f"{base_prefix}-ins{counter}"
                counter += 1
            old_end = page_count
    else:
        target_sec = sections[target_idx]
        prev_id = target_sec["section_id"]
        base_prefix = re.sub(r"-ins\d*$", "", prev_id)
        cand = f"{base_prefix}-ins"
        counter = 2
        while cand in used_ids:
            cand = f"{base_prefix}-ins{counter}"
            counter += 1
        old_end = target_sec["end"]["physical_page"]
        if exact_match is None:
            target_sec["end"]["physical_page"] = start_page - 1
            target_sec["inferred_continuation_pages"] = list(range(target_sec["start"]["physical_page"], start_page))

    new_sec = {
        "section_id": cand,
        "kind": "unclassified",
        "title": clean_title,
        "start": {"physical_page": start_page, "location": "full", "printed_label": None},
        "end": {"physical_page": old_end, "location": "full", "printed_label": None},
        "subsections": [],
        "heading_evidence": [],
        "inferred_continuation_pages": list(range(start_page, old_end + 1)),
    }
    sections.append(new_sec)
    sections.sort(key=lambda s: s["start"]["physical_page"])
    mapping["sections"] = sections
    return mapping, cand


def section_requires_subheading(mapping, heading: str = "", selections=()) -> str | None:
    """If the matched section or main heading already has subsections, return a label like 'D006 (D006.1)'."""
    if not mapping:
        return None
    norm_h = _norm_heading(re.sub(r'^D[a-zA-Z0-9_\-\.]+\s*[—:\-]\s*', '', clean_single_line_text(heading), flags=re.IGNORECASE))
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
        if heading_matches or (not norm_h and overlaps):
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
    if mapping.get('primary_statement_sightings'):
        lines.append('\nPrimary-statement heading sightings (draft navigation, not inspected statement values):')
        for item in mapping['primary_statement_sightings']:
            lines.append(f"- {item['kind'].replace('_', ' ')}: physical PDF p. {item['physical_page']}, {item['location']}.")
    if mapping.get('unclassified_physical_pages'):
        lines.append('\nUnclassified physical pages: ' + ', '.join(map(str, mapping['unclassified_physical_pages'])) + '. Their purpose has not been established by the scan.')
    if mapping.get('issues'):
        lines.append(f"\nNative-scan issues: {len(mapping['issues'])}; consult the saved map details. These areas need checking.")
    if mapping.get('limitations'):
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
