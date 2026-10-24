"""Intelligent matcher and comparator between user-captured report map sections and full app-detected sections."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

# Standard executive and financial reporting synonym expansions
ACRONYMS = {
    r'\bceo\b': 'chief executive',
    r'\bcfo\b': 'chief financial',
    r'\bcoo\b': 'chief operating',
    r'\bmd\b': 'managing director',
    r'\bfs\b': 'financial statements',
    r'\bafs\b': 'annual financial statements',
    r'\biar\b': 'integrated annual report',
    r'\bapm\b': 'alternative performance measure',
    r'\bapms\b': 'alternative performance measures',
}

STOP_WORDS = {
    'the', 'and', 'to', 'of', 'for', 'in', 'our', 'a', 'an', 'at', 'by', 'on', 'with',
    's', 'overview', 'item', 'items'
}


def _normalize_title(title: str | None) -> str:
    """Normalize a section title for fuzzy comparison by expanding acronyms and stripping noise."""
    if not title:
        return ""
    text = str(title)
    # Remove section ID prefix like D001, S001, Note 1, etc.
    text = re.sub(r'^(?:[DS]\d{3}[a-zA-Z0-9_\-\.]*|NOTE\s+\d+)\s*[-:\.]\s*', '', text, flags=re.IGNORECASE)
    # Handle possessives like CEO's -> CEO
    text = re.sub(r"['’]s\b", '', text, flags=re.IGNORECASE)
    # Strip remaining non-alphanumeric
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text).lower()
    
    # Expand acronyms
    for pattern, replacement in ACRONYMS.items():
        text = re.sub(pattern, replacement, text)
        
    # Remove stop words and collapse whitespace
    words = [w for w in text.split() if w not in STOP_WORDS]
    return ' '.join(words)


def _token_similarity(t1: str, t2: str) -> float:
    """Calculates token overlap similarity between two normalized strings, rewarding subsets."""
    tokens1 = set(t1.split())
    tokens2 = set(t2.split())
    if not tokens1 and not tokens2:
        return 1.0
    if not tokens1 or not tokens2:
        return 0.0
    intersection = tokens1 & tokens2
    union = tokens1 | tokens2
    jaccard = len(intersection) / len(union)

    # If all tokens of the shorter string are present in the longer string
    shorter, longer = (tokens1, tokens2) if len(tokens1) <= len(tokens2) else (tokens2, tokens1)
    if shorter.issubset(longer):
        return max(0.85, len(shorter) / len(longer))

    # Check direct substring containment
    if t1 in t2 or t2 in t1:
        return max(jaccard, 0.85)

    # Dice coefficient
    dice = 2.0 * len(intersection) / (len(tokens1) + len(tokens2))
    return max(jaccard, dice)


@dataclass
class SectionMatch:
    user_section: dict[str, Any]
    app_section: dict[str, Any] | None
    match_type: str  # 'exact', 'high_confidence', 'page_aligned', 'user_only'
    similarity_score: float
    page_diff: int
    notes: str = ""

    @property
    def is_matched(self) -> bool:
        return self.app_section is not None


@dataclass
class SectionComparisonResult:
    matched: list[SectionMatch] = field(default_factory=list)
    user_only: list[dict[str, Any]] = field(default_factory=list)
    app_only: list[dict[str, Any]] = field(default_factory=list)

    @property
    def total_user_sections(self) -> int:
        return len(self.matched) + len(self.user_only)

    @property
    def total_app_sections(self) -> int:
        matched_app_count = sum(1 for m in self.matched if m.app_section is not None)
        return matched_app_count + len(self.app_only)


def compare_section_maps(
    user_sections: list[dict[str, Any]],
    app_sections: list[dict[str, Any]],
    page_tolerance: int = 5,
) -> SectionComparisonResult:
    """
    Compares the user's captured major sections against the full app-scanned sections.
    
    Matches are resolved by evaluating both title token similarity and physical page proximity.
    """
    result = SectionComparisonResult()
    unmatched_app_indices = set(range(len(app_sections)))

    for u_sec in user_sections:
        u_title = u_sec.get('title', '')
        u_norm = _normalize_title(u_title)
        u_page = u_sec.get('start_page') or u_sec.get('start', {}).get('physical_page') or 1

        best_idx = None
        best_score = -1.0
        best_page_diff = 9999
        best_match_type = 'user_only'

        for a_idx in unmatched_app_indices:
            a_sec = app_sections[a_idx]
            a_title = a_sec.get('title', '')
            a_norm = _normalize_title(a_title)
            a_page = a_sec.get('start_page') or a_sec.get('start', {}).get('physical_page') or 1

            title_sim = _token_similarity(u_norm, a_norm)
            page_diff = abs(int(u_page) - int(a_page))

            # Page proximity penalty: 0 penalty if 0-1 pages away
            prox_penalty = max(0.0, (page_diff / 10.0))
            combined_score = title_sim - (prox_penalty if page_diff > 1 else 0.0)

            # Check criteria
            if u_norm == a_norm and page_diff <= 2:
                best_idx = a_idx
                best_score = 1.0
                best_page_diff = page_diff
                best_match_type = 'exact'
                break

            if title_sim >= 0.6 and page_diff <= page_tolerance:
                if combined_score > best_score:
                    best_score = combined_score
                    best_idx = a_idx
                    best_page_diff = page_diff
                    best_match_type = 'high_confidence'
            elif title_sim >= 0.4 and page_diff <= 2:
                if combined_score > best_score:
                    best_score = combined_score
                    best_idx = a_idx
                    best_page_diff = page_diff
                    best_match_type = 'high_confidence'
            elif page_diff == 0 and title_sim >= 0.2:
                # Same exact start page
                if combined_score > best_score:
                    best_score = combined_score
                    best_idx = a_idx
                    best_page_diff = page_diff
                    best_match_type = 'page_aligned'

        if best_idx is not None and best_score > 0.2:
            matched_app_sec = app_sections[best_idx]
            unmatched_app_indices.remove(best_idx)
            note = f"Score: {best_score:.2f}, page diff: {best_page_diff}"
            result.matched.append(
                SectionMatch(
                    user_section=u_sec,
                    app_section=matched_app_sec,
                    match_type=best_match_type,
                    similarity_score=best_score,
                    page_diff=best_page_diff,
                    notes=note,
                )
            )
        else:
            result.user_only.append(u_sec)

    # Remaining app sections are app_only
    for a_idx in sorted(unmatched_app_indices):
        result.app_only.append(app_sections[a_idx])

    return result


def extract_all_app_sections(source: Any) -> list[dict[str, Any]]:
    """
    Extracts all sections present in the PDF report using:
    1. PDF Bookmarks / Outline (TOC) via pypdfium2 (if present)
    2. Heading heuristics via report_map.scan_report()
    Returns a unified list of detected sections sorted by start_page.
    """
    if not source or not getattr(source, "path", None):
        return []

    sections: list[dict[str, Any]] = []
    seen_keys: set[tuple[str, int]] = set()
    total_pages = getattr(source, "page_count", 9999)

    # 1. Try PDF Bookmarks
    try:
        import pypdfium2 as pdfium
        doc = pdfium.PdfDocument(str(source.path))
        toc = list(doc.get_toc())
        if toc:
            for b in toc:
                title = b.get_title().strip()
                dest = b.get_dest()
                if not title or not dest:
                    continue
                p_idx = dest.get_index()
                start_p = p_idx + 1 if p_idx is not None else 1
                key = (title.lower(), start_p)
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                sections.append({
                    "title": title,
                    "start_page": start_p,
                    "source": "bookmark",
                    "level": b.level,
                })
    except Exception:
        pass

    # 2. Heading Scan via report_map
    try:
        from .report_map import scan_report
        heuristics_map = getattr(source, "report_map", None) or scan_report(source)
        for s in heuristics_map.get("sections", []):
            title = s.get("title", "").strip()
            if not title or title.startswith("Unclassified"):
                continue
            start_p = s.get("start", {}).get("physical_page", 1)
            end_p = s.get("end", {}).get("physical_page", total_pages)
            key = (title.lower(), start_p)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            sections.append({
                "title": title,
                "start_page": start_p,
                "end_page": end_p,
                "kind": s.get("kind", ""),
                "source": "heading_scan",
            })
    except Exception:
        pass

    # Sort by start page
    sections.sort(key=lambda s: s["start_page"])

    # Compute end pages if missing
    for i, s in enumerate(sections):
        if "end_page" not in s or s["end_page"] is None:
            if i + 1 < len(sections):
                next_start = sections[i + 1]["start_page"]
                s["end_page"] = max(s["start_page"], next_start - 1)
            else:
                s["end_page"] = total_pages

    return sections


def auto_capture_section(
    source: Any,
    title: str,
    start_page: int,
    end_page: int,
    sector: str | None = None,
    output_root: Any = None,
    max_pages: int = 25,
) -> Any:
    """
    Extracts text for pages in [start_page, end_page] and saves as a SavedSection package in SQLite.
    """
    from PySide6.QtCore import QRectF
    from .packages import save_package

    if not source:
        raise ValueError("Valid PdfSource is required.")

    total_pages = getattr(source, "page_count", 9999)
    start_p = max(1, min(start_page, total_pages))
    end_p = max(start_p, min(end_page, total_pages))

    # Cap maximum pages per section to prevent accidental massive extractions
    if end_p - start_p + 1 > max_pages:
        end_p = start_p + max_pages - 1

    captures = []
    for page in range(start_p, end_p + 1):
        w, h = source.size(page)
        cap = source.capture_area(page, QRectF(0, 0, w, h))

        lower_title = title.lower()
        if "|" in cap.text and cap.text.count("|") >= 4:
            cap.content_type = "table"
        elif "note" in lower_title or "statement" in lower_title:
            cap.content_type = "financial_note"
        else:
            cap.content_type = "commentary"
        captures.append(cap)

    saved = save_package(
        source=source,
        heading=title,
        question="Scrutinize key accounting policies, unusual movements, and forward guidance.",
        captures=captures,
        output_root=output_root,
        sector=sector,
    )
    return saved

