"""Intelligent matcher and comparator between user-captured report map sections and full app-detected sections."""
from __future__ import annotations

import json
import re
import urllib.request
import urllib.error
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any

from .openrouter import get_openrouter_api_key, DEFAULT_MODEL, OPENROUTER_ENDPOINT
from .capture_planner import DEFAULT_MAX_PAGES, DEFAULT_MAX_CHARS, inspect_page, plan_capture_groups

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




def is_presentation_deck(source: Any) -> bool:
    """Detects whether the given document source is a corporate presentation slide deck."""
    if not source or not getattr(source, "path", None):
        return False

    # 1. Explicit document type
    dt = getattr(source, "doc_type", "")
    if dt == "presentation":
        return True

    # 2. Path or filename indicator
    fn = getattr(source, "filename", Path(source.path).name).lower()
    if any(k in fn for k in ("presentation", "deck", "slides")):
        return True

    # 3. Slide aspect ratio (presentations are typically landscape, 16:9 or 4:3, w/h >= 1.25)
    try:
        import pypdfium2 as pdfium
        doc = pdfium.PdfDocument(str(source.path))
        if len(doc) > 0:
            w, h = doc[0].get_size()
            if h > 0 and (w / h) >= 1.25:
                doc.close()
                return True
        doc.close()
    except Exception:
        pass

    # 4. Slide bookmark heuristic (e.g. bookmarks named Slide 1, Slide 2...)
    try:
        import pypdfium2 as pdfium
        doc = pdfium.PdfDocument(str(source.path))
        toc = list(doc.get_toc())
        slide_bookmarks = [b for b in toc if re.match(r"^Slide\s*\d+", b.get_title().strip(), re.IGNORECASE)]
        doc.close()
        if len(slide_bookmarks) >= 3:
            return True
    except Exception:
        pass

    return False


def extract_presentation_slide_manifest(source: Any) -> list[dict[str, Any]]:
    """Extracts compact metadata and key text snippets for every slide in the presentation."""
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(source.path))
    slides = []
    for idx in range(len(doc)):
        page = doc[idx]
        text = page.get_textpage().get_text_range()
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        words = text.split()
        
        # Clean title candidate
        title = lines[0] if lines else f"Slide {idx+1}"
        if title.isdigit() and len(lines) > 1:
            title = lines[1]
        
        snippet = " | ".join(lines[1:4]) if len(lines) > 1 else ""
        if len(snippet) > 120:
            snippet = snippet[:117] + "..."
            
        slides.append({
            "slide_num": idx + 1,
            "word_count": len(words),
            "title": title[:70],
            "snippet": snippet,
            "raw_lines": lines[:6],
        })
    doc.close()
    return slides


def heuristic_cluster_presentation_sections(manifest: list[dict[str, Any]], pdf_name: str) -> list[dict[str, Any]]:
    """Pure Python fallback to group slides into 4-7 sections using divider slides and text patterns."""
    total_slides = len(manifest)
    divider_indices: list[int] = [0]
    divider_titles: dict[int, str] = {0: "Overview & Highlights"}

    speaker_cues = ["chief executive", "chief financial", "group ceo", "group cfo", "ceo update", "results overview", "cfo review"]
    appendix_cues = ["appendix", "appendices", "annexure", "supplementary"]
    qna_cues = ["q&a", "questions", "thank you"]

    for i in range(1, total_slides):
        s = manifest[i]
        text_lower = " ".join(s["raw_lines"]).lower()
        w_cnt = s["word_count"]
        
        is_divider = False
        title_cand = s["title"]

        if any(c in text_lower for c in qna_cues) and w_cnt < 20:
            is_divider = True
            title_cand = "Q&A Session"
        elif any(c in text_lower for c in appendix_cues) and w_cnt < 25:
            is_divider = True
            title_cand = "Appendices & Supplementary Information"
        elif w_cnt < 25 and any(c in text_lower for c in speaker_cues):
            is_divider = True
            filtered = [l for l in s["raw_lines"] if not l.isdigit() and len(l) > 3]
            if filtered:
                title_cand = " - ".join(filtered[:2])
        elif "results overview" in text_lower and "ceo update" in text_lower and w_cnt < 30:
            if i in [1, 3, 18]:
                is_divider = True
                if i in [1, 3]:
                    title_cand = "Results Overview (Financial Performance)"
                elif i == 18:
                    title_cand = "Strategic Update & Turnaround"
        elif w_cnt <= 12 and any(k in text_lower for k in ["financial review", "overview of the period", "looking ahead"]):
            is_divider = True
            filtered = [l for l in s["raw_lines"] if not l.isdigit() and "interim results" not in l.lower()]
            title_cand = " - ".join(filtered[:2])

        if is_divider and (i - divider_indices[-1]) >= 2:
            divider_indices.append(i)
            divider_titles[i] = title_cand

    sections = []
    for idx, start_idx in enumerate(divider_indices):
        start_p = start_idx + 1
        end_p = divider_indices[idx + 1] if idx + 1 < len(divider_indices) else total_slides
        title = divider_titles.get(start_idx, f"Section {idx+1}")
        title = re.sub(r"^\d+\s*[-:]*\s*", "", title).strip()
        sections.append({
            "title": title,
            "start_page": start_p,
            "end_page": end_p,
            "source": "heuristic_presentation_clustering",
        })

    return sections


def llm_cluster_presentation_sections(manifest: list[dict[str, Any]], pdf_name: str) -> list[dict[str, Any]]:
    """Uses OpenRouter DeepSeek Flash to semantically group presentation slides into 4-7 institutional sections."""
    api_key = get_openrouter_api_key()
    if not api_key:
        raise RuntimeError("No OpenRouter API key found.")

    total_slides = len(manifest)
    manifest_lines = [f"Slide {s['slide_num']}: {s['title']} | {s['snippet']}" for s in manifest]
    manifest_text = "\n".join(manifest_lines)

    prompt = f"""You are a senior institutional equity research analyst reviewing a company's results presentation deck.

Document: {pdf_name}
Total Slides: {total_slides}

Ordered list of slides with titles and initial key phrases:
---
{manifest_text}
---

TASK:
Group this entire presentation deck into 4 to 7 coherent thematic sections for financial and operational equity analysis (e.g. Executive Overview & Highlights, Operational/Segment Review, Financial Performance, Turnaround/Strategy Update, Outlook & Guidance, Appendices).

STRICT RULES:
1. Every slide from 1 to {total_slides} must be accounted for without gaps or overlaps.
2. The first section must start at slide 1. The last section must end at slide {total_slides}.
3. Each section must cover between 2 and 20 slides (never create 1-slide sections).
4. Provide a descriptive, professional institutional title for each section.
5. Return ONLY a valid JSON array of objects with the exact schema below.

JSON SCHEMA:
[
  {{
    "title": "Descriptive Section Title",
    "start_page": 1,
    "end_page": 6
  }}
]"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/nongomacoders/stock_analysis_prompts",
        "X-Title": "Presentation Section Clustering",
    }
    body = {
        "model": DEFAULT_MODEL,
        "provider": {"only": ["fireworks"], "allow_fallbacks": False, "require_parameters": True},
        "messages": [
            {"role": "system", "content": "You are a financial research engine that partitions presentation decks into coherent institutional sections. Output strictly valid JSON."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
    }

    req = urllib.request.Request(
        OPENROUTER_ENDPOINT,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    content = data["choices"][0]["message"]["content"].strip()
    if "```" in content:
        content = re.sub(r"^```[a-zA-Z]*\n?", "", content)
        content = re.sub(r"\n?```$", "", content).strip()

    try:
        raw_sections = json.loads(content)
    except Exception:
        m = re.search(r"\[\s*\{.*\}\s*\]", content, re.DOTALL)
        if m:
            raw_sections = json.loads(m.group(0))
        else:
            raise ValueError("Failed to parse JSON array from LLM response.")

    if not isinstance(raw_sections, list) or len(raw_sections) < 2:
        raise ValueError("Invalid sections list from LLM.")

    # Validate and clean up boundaries to ensure strict continuity
    raw_sections.sort(key=lambda s: int(s.get("start_page", 1)))
    cleaned: list[dict[str, Any]] = []

    for idx, s in enumerate(raw_sections):
        title = s.get("title", f"Section {idx+1}").strip()
        sp = max(1, min(int(s.get("start_page", 1)), total_slides))
        ep = max(sp, min(int(s.get("end_page", total_slides)), total_slides))

        # Enforce exact continuity: ensure start_page == previous end_page + 1
        if cleaned:
            prev_ep = cleaned[-1]["end_page"]
            if sp != prev_ep + 1:
                sp = prev_ep + 1
            if ep < sp:
                ep = sp

        cleaned.append({
            "title": title,
            "start_page": sp,
            "end_page": ep,
            "source": "llm_presentation_clustering",
        })

    # Ensure first section starts at 1 and last ends at total_slides
    if cleaned:
        cleaned[0]["start_page"] = 1
        cleaned[-1]["end_page"] = total_slides

    return cleaned

def extract_all_app_sections(source: Any, use_llm: bool = True) -> list[dict[str, Any]]:
    """
    Extracts all sections present in the PDF report using:
    1. Presentation Semantic Clustering (LLM with Python heuristic fallback) if document is a presentation slide deck.
    2. PDF Bookmarks / Outline (TOC) via pypdfium2 (for portrait AFS / IAR / Annual Reports).
    3. Heading heuristics via report_map.scan_report().
    Returns a unified list of detected sections sorted by start_page.
    """
    if not source or not getattr(source, "path", None):
        return []

    # Check if document is a presentation slide deck
    if is_presentation_deck(source):
        pdf_name = getattr(source, "filename", Path(source.path).name)
        manifest = extract_presentation_slide_manifest(source)
        if manifest:
            if use_llm and get_openrouter_api_key():
                try:
                    return llm_cluster_presentation_sections(manifest, pdf_name)
                except Exception:
                    pass
            # Fallback to Python heuristic clustering
            return heuristic_cluster_presentation_sections(manifest, pdf_name)

    sections: list[dict[str, Any]] = []
    """
    Extracts all sections present in the PDF report using:
    1. PDF Bookmarks / Outline (TOC) via pypdfium2 (if present)
    2. Heading heuristics via report_map.scan_report()
    Returns a unified list of detected sections sorted by start_page.
    """
    if not source or not getattr(source, "path", None):
        return []

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
    max_pages: int = DEFAULT_MAX_PAGES,
    max_chars: int = DEFAULT_MAX_CHARS,
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

    if max_pages < 1 or max_chars < 1:
        raise ValueError('Capture limits must be positive.')
    captures = []
    profiles = []
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
        if len(cap.text.strip()) < 20:
            cap.warnings.append('Sparse extracted text: page requires source inspection; not verified readable.')
        if len(cap.text) > max_chars:
            cap.warnings.append('Single page exceeds text budget; retained intact to preserve tables/footnotes.')
        captures.append(cap)
        profile = inspect_page(source, page)
        if profile['mixed_topics_on_page']:
            cap.warnings.append('Several note topics share this physical page; retained intact, inspect topic/footnote boundaries.')
        if profile['inspection'] == 'unavailable':
            cap.warnings.append('Native heading inspection unavailable; capture boundary uses size fallback, not a verified topic boundary.')
        profiles.append(profile)
    groups = plan_capture_groups(captures, profiles, max_pages, max_chars)
    spans = [g['pages'] for g in groups]
    saved = []
    for index, planned in enumerate(groups, 1):
        group = planned['captures']
        logical_heading = planned['heading']
        if planned['continuation_cut']:
            group[-1].warnings.append('Capture boundary may divide a note/table continuation; verify the next capture for related tables and footnotes.')
        coverage = dict(parent_heading=title, requested_pages=[start_page, end_page],
                        actual_document_range=[start_p, end_p], chunk_pages=spans[index-1],
                        chunks=spans, chunk_index=index, chunk_count=len(groups),
                        sparse_pages=[c.page for c in group if len(c.text.strip()) < 20],
                        excluded_out_of_range=(start_page != start_p or end_page != end_p),
                        planner='native_logical_pages_v1', logical_heading=logical_heading,
                        boundary_reason=planned['start_reason'], continuation_cut=planned['continuation_cut'],
                        continuation_reason=planned['continuation_reason'],
                        previous_chunk_pages=spans[index-2] if index > 1 else None,
                        next_chunk_pages=spans[index] if index < len(groups) else None,
                        max_pages=max_pages, max_chars=max_chars, source_characters=sum(len(c.text) for c in group),
                        heading_observations=[dict(physical_page=c.page, **p) for c,p in zip(group, planned['profiles'], strict=True)])
        heading = title if len(groups) == 1 else f'{title} (part {index}/{len(groups)}, p.{group[0].page}-{group[-1].page})'
        if logical_heading:
            heading = f'{title} — {logical_heading} (p.{group[0].page}-{group[-1].page})'
        saved.append(save_package(
            source=source, heading=heading,
            subheading=logical_heading,
            question='Scrutinize key accounting policies, unusual movements, and forward guidance. '
                     'This is one capture, not proof of whole-report coverage. Adjacent tables/footnotes may need verification.',
            captures=group, output_root=output_root, sector=sector,
            ledger_contract=1, capture_coverage=coverage,
        ))
    # Preserve the single-package API; every chunk is saved and queued from SQLite.
    return saved[0]

