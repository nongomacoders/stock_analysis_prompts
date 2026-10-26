"""One-Shot Autonomous Equity Research Pipeline View.

Provides a streamlined interface where the user:
1. Creates or selects a company (Ticker / Sector).
2. Places PDFs into `sources/` or SENS notices into `sources/sens/`.
3. Reviews discovered documents and confirms the Reporting Period.
4. Clicks '🚀 Start Autonomous Analysis' and monitors a detailed live progress screen
   as the pipeline automatically executes:
   - Phase 1: PDF Ingestion & Section Mapping (LLM Slide Clustering / TOC Scan)
   - Phase 2: Sequential Section Audit & Questions Ledger Construction
   - Phase 3: Stage 1 Cognitive Forensic Audit
   - Phase 4: Stage 2 Institutional Valuation & SOTP DCF (or SENS Event Update)
   - Phase 5: Auto-Archiving & Portfolio Coverage Sync
"""

from __future__ import annotations

from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
from typing import Any

from PySide6.QtCore import Qt, QThread, QTimer, Signal
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSplitter,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from companies import SECTORS, find_company_dir
from companies.sectors import get_sector_badge_style, get_sector_short_label
from section_capture.audit_dialog import (
    AuditValuationDialog,
    discover_available_companies,
    open_folder_and_select,
)
from section_capture.db import (
    DOC_TYPES,
    KNOWN_COMPANIES,
    archive_source_pdfs,
    auto_link_companion_reports,
    connect_db,
    detect_doc_type_and_date,
    detect_reporting_period,
    extract_questions_ledger_from_response,
    get_doc_badge,
    get_stage1_report,
    get_stage2_report,
    list_sections,
    parse_valuation_summary,
    resolve_db_path,
    save_section_llm_response,
    save_stage1_report,
    save_stage2_report,
    set_report_doc_type,
    upsert_report,
)
from section_capture.market_data import fetch_jse_quote, save_market_quotes
from section_capture.openrouter import (
    OpenRouterWorker,
    get_model_display_name,
    get_openrouter_api_key,
    get_openrouter_model,
)
from section_capture.packages import (
    PROJECT_ROOT,
    build_prompt,
    extract_selection_texts,
)
from section_capture.pdf_source import PdfSource
from section_capture.report_map import load_questions_ledger
from section_capture.section_matcher import (
    auto_capture_section,
    extract_all_app_sections,
    is_presentation_deck,
)
from workflow.export_stage1 import build_stage1_prompt_content
from workflow.generate_sens_update import (
    build_sens_update_prompt_content,
    move_analyzed_sens_files,
)
from workflow.generate_stage2 import build_stage2_prompt_content


def discover_company_documents(
    company_dir: Path,
    period: str | None = None,
    db_path: Path | str | None = None,
) -> tuple[list[dict[str, Any]], str]:
    """Scans `sources/` and `sources/sens/` (with fallback to `sources/completed/<period>`)
    for all report PDFs and SENS disclosures.

    Returns `(ordered_documents, detected_period)`.
    """
    sources_dir = company_dir / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    sens_dir = sources_dir / "sens"
    sens_dir.mkdir(parents=True, exist_ok=True)

    # Query DB for any already-registered metadata
    db_info: dict[str, dict[str, Any]] = {}
    resolved_db = resolve_db_path(db_path)
    if resolved_db.exists():
        try:
            with connect_db(resolved_db) as conn:
                for row in conn.execute(
                    "SELECT sha256, filename, doc_type, period, physical_page_count FROM reports"
                ):
                    db_info[row["filename"]] = dict(row)
        except Exception:
            pass

    # 1. Discover primary/companion PDFs in sources/ directly (do not re-pull completed/ PDFs)
    active_pdfs = sorted(
        f for f in sources_dir.glob("*.pdf") if f.is_file() and "sens" not in f.name.lower()
    )
    # If no active PDFs in sources/, auto-detect period from completed/ or briefs/
    if not active_pdfs and not period:
        comp_root = sources_dir / "completed"
        if comp_root.exists():
            subdirs = sorted([d.name for d in comp_root.iterdir() if d.is_dir()], reverse=True)
            if subdirs:
                period = subdirs[0]
        if not period:
            b_root = company_dir / "briefs"
            if b_root.exists():
                bsubdirs = sorted([d.name for d in b_root.iterdir() if d.is_dir()], reverse=True)
                if bsubdirs:
                    period = bsubdirs[0]

    # 2. Discover SENS files in sources/sens/
    sens_files = sorted(
        f
        for f in sens_dir.iterdir()
        if f.is_file()
        and f.suffix.lower() in {".pdf", ".txt", ".text", ".md"}
        and f.name.lower() != "readme.md"
    )

    import pypdfium2 as pdfium

    detected_period = period or ""
    docs: list[dict[str, Any]] = []

    for pdf_path in active_pdfs:
        info = db_info.get(pdf_path.name, {})
        dt = info.get("doc_type")
        ann_date = None
        if not dt:
            dt, ann_date = detect_doc_type_and_date(pdf_path)
        if not detected_period:
            detected_period = info.get("period") or detect_reporting_period(pdf_path) or "FY26"

        page_cnt = info.get("physical_page_count") or 0
        sha = info.get("sha256") or ""
        if not sha:
            try:
                sha = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
            except Exception:
                sha = ""

        if not page_cnt:
            try:
                doc = pdfium.PdfDocument(str(pdf_path))
                page_cnt = len(doc)
                # Refine presentation detection via landscape aspect ratio
                if len(doc) > 0:
                    w, h = doc[0].get_size()
                    if h > 0 and (w / h) >= 1.25:
                        dt = "presentation"
                    elif dt == "interim":
                        dt = "afs"
                doc.close()
            except Exception:
                page_cnt = 0

        # Check existing sections in DB
        sec_total = 0
        sec_done = 0
        if sha and resolved_db.exists():
            try:
                secs = list_sections(sha, db_path=resolved_db)
                sec_total = len(secs)
                sec_done = sum(1 for s in secs if (s.llm_response or "").strip())
            except Exception:
                pass

        badge = get_doc_badge(dt)
        # Default ordering priority: Presentation (0) -> IAR/AR (1) -> AFS (2)
        order_prio = 0 if dt == "presentation" else (1 if dt in ("iar", "annual_report") else 2)
        docs.append({
            "path": pdf_path,
            "filename": pdf_path.name,
            "doc_type": dt,
            "badge": badge,
            "period": detected_period or "FY26",
            "page_count": page_cnt,
            "sha256": sha,
            "is_sens": False,
            "is_archived": False,
            "sec_total": sec_total,
            "sec_done": sec_done,
            "order_prio": order_prio,
            "announcement_date": ann_date,
        })

    # Sort report PDFs by default analytical priority (Presentation -> IAR -> AFS)
    docs.sort(key=lambda d: (d["order_prio"], d["filename"].lower()))

    # Append SENS files at the end
    for sf in sens_files:
        page_cnt = 1
        if sf.suffix.lower() == ".pdf":
            try:
                doc = pdfium.PdfDocument(str(sf))
                page_cnt = len(doc)
                doc.close()
            except Exception:
                page_cnt = 1
        try:
            sha = hashlib.sha256(sf.read_bytes()).hexdigest()
        except Exception:
            sha = ""
        _, ann_date = detect_doc_type_and_date(sf)
        docs.append({
            "path": sf,
            "filename": sf.name,
            "doc_type": "sens",
            "badge": "[SENS]",
            "period": detected_period or "FY26",
            "page_count": page_cnt,
            "sha256": sha,
            "is_sens": True,
            "is_archived": False,
            "sec_total": 0,
            "sec_done": 0,
            "order_prio": 9,
            "announcement_date": ann_date,
        })

    if not detected_period:
        detected_period = "FY26"

    return docs, detected_period


class IngestionWorker(QThread):
    """Background worker that ingests selected PDFs, maps/clusters sections, and auto-captures packages into SQLite."""

    log_message = Signal(str)
    doc_status_updated = Signal(str, str, str)  # (filename, sections_text, status_text)
    step_progress = Signal(int, int, str)  # (current, total, banner_message)
    ingestion_finished = Signal(list)  # list of ingested doc dicts
    ingestion_error = Signal(str)

    def __init__(
        self,
        docs: list[dict[str, Any]],
        period: str,
        sector: str,
        db_path: Path | str | None = None,
        force_rerun: bool = False,
        use_llm_clustering: bool = True,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.docs = docs
        self.period = period
        self.sector = sector
        self.db_path = resolve_db_path(db_path)
        self.force_rerun = force_rerun
        self.use_llm_clustering = use_llm_clustering
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        try:
            pdf_docs = [d for d in self.docs if not d.get("is_sens")]
            if not pdf_docs:
                self.ingestion_finished.emit([])
                return

            ingested_results: list[dict[str, Any]] = []
            primary_sha: str | None = None

            for doc_idx, doc_info in enumerate(pdf_docs):
                if self._cancelled:
                    return

                pdf_path = Path(doc_info["path"])
                doc_name = doc_info["filename"]
                dt = doc_info.get("doc_type") or "annual_report"
                badge = doc_info.get("badge") or "[AR]"

                self.doc_status_updated.emit(doc_name, "Scanning...", "📥 Opening PDF...")
                self.step_progress.emit(
                    doc_idx,
                    len(pdf_docs),
                    f"📥 [Phase 1/5] Opening & registering {badge} {doc_name}...",
                )

                source = PdfSource(pdf_path)
                source.doc_type = dt
                source.period = self.period
                sha = source.sha256
                if primary_sha is None:
                    primary_sha = sha

                self.log_message.emit(
                    f"📄 <b>Ingesting Document {doc_idx + 1}/{len(pdf_docs)}:</b> <code>{doc_name}</code> "
                    f"({source.page_count} pages, {badge}, Period: <b>{self.period}</b>, SHA-256: <code>{sha[:12]}…</code>)"
                )

                # Register report in SQLite and link companions
                upsert_report(
                    sha256=sha,
                    filename=doc_name,
                    original_path=str(pdf_path),
                    byte_size=len(source.data),
                    physical_page_count=source.page_count,
                    doc_type=dt,
                    period=self.period,
                    db_path=self.db_path,
                )
                set_report_doc_type(sha, dt, db_path=self.db_path)
                auto_link_companion_reports(sha, pdf_path, doc_type=dt, db_path=self.db_path)

                if self.force_rerun:
                    with connect_db(self.db_path) as conn:
                        conn.execute("DELETE FROM sections WHERE report_sha256 = ?", (sha,))
                        conn.execute("UPDATE reports SET questions_ledger = NULL WHERE sha256 = ?", (sha,))
                        conn.commit()
                    self.log_message.emit(f"🔄 Cleared previous sections for <code>{doc_name}</code> (Force Re-run enabled).")

                existing_secs = list_sections(sha, db_path=self.db_path)
                if existing_secs and not self.force_rerun:
                    done_cnt = sum(1 for s in existing_secs if (s.llm_response or "").strip())
                    pend_cnt = len(existing_secs) - done_cnt
                    self.log_message.emit(
                        f"✓ Found <b>{len(existing_secs)}</b> existing captured sections in SQLite for "
                        f"<code>{doc_name}</code> ({done_cnt} analyzed, {pend_cnt} pending)."
                    )
                    self.doc_status_updated.emit(
                        doc_name,
                        f"{len(existing_secs)} sections ({done_cnt}/{len(existing_secs)} done)",
                        "✓ Ingested (Cached)" if pend_cnt == 0 else f"⏳ {pend_cnt} Pending Audit",
                    )
                    ingested_results.append({
                        **doc_info,
                        "sha256": sha,
                        "page_count": source.page_count,
                        "sec_total": len(existing_secs),
                        "sec_done": done_cnt,
                    })
                    source.close()
                    continue

                # Determine sections (LLM semantic clustering for presentations, TOC/Heading scan for AFS/IAR)
                is_pres = is_presentation_deck(source)
                method_desc = (
                    "LLM Presentation Semantic Clustering"
                    if is_pres
                    else "PDF Outline TOC & Heading Heuristics"
                )
                self.doc_status_updated.emit(doc_name, "Mapping sections...", f"🧠 {method_desc}...")
                self.step_progress.emit(
                    doc_idx,
                    len(pdf_docs),
                    f"🧠 [Phase 1/5] Mapping sections for {doc_name} via {method_desc}...",
                )
                self.log_message.emit(f"🧠 Running <b>{method_desc}</b> on <code>{doc_name}</code>...")

                detected_sections = extract_all_app_sections(source, use_llm=self.use_llm_clustering)
                if not detected_sections:
                    # Fallback: capture whole document in 15-page chunks if no sections detected
                    total_p = max(1, source.page_count)
                    chunk = 15
                    detected_sections = [
                        {
                            "title": f"Report Pages {sp}-{min(sp + chunk - 1, total_p)}",
                            "start_page": sp,
                            "end_page": min(sp + chunk - 1, total_p),
                            "source": "fallback_chunk",
                        }
                        for sp in range(1, total_p + 1, chunk)
                    ]

                self.log_message.emit(
                    f"📋 Discovered <b>{len(detected_sections)} coherent sections</b> in <code>{doc_name}</code>:"
                )
                for s_idx, sec in enumerate(detected_sections, 1):
                    sp = sec.get("start_page", 1)
                    ep = sec.get("end_page", sp)
                    t_str = sec.get("title", f"Section {s_idx}")
                    self.log_message.emit(f"&nbsp;&nbsp;&nbsp;&nbsp;• <b>S{s_idx:02d}</b> [p.{sp}–p.{ep}]: {t_str}")

                # Auto-capture each section into SQLite
                captured_cnt = 0
                for s_idx, sec in enumerate(detected_sections, 1):
                    if self._cancelled:
                        source.close()
                        return
                    sp = int(sec.get("start_page", 1))
                    ep = int(sec.get("end_page", sp))
                    t_str = sec.get("title", f"Section {s_idx}")

                    self.doc_status_updated.emit(
                        doc_name,
                        f"{s_idx}/{len(detected_sections)} captured",
                        f"💾 Capturing S{s_idx:02d}/{len(detected_sections)}...",
                    )
                    self.step_progress.emit(
                        s_idx,
                        len(detected_sections),
                        f"💾 [Phase 1/5] {doc_name}: Capturing S{s_idx:02d}/{len(detected_sections)} — {t_str} (p.{sp}–{ep})...",
                    )
                    try:
                        auto_capture_section(
                            source=source,
                            title=t_str,
                            start_page=sp,
                            end_page=ep,
                            sector=self.sector,
                            output_root=self.db_path,
                        )
                        captured_cnt += 1
                    except Exception as cap_err:
                        self.log_message.emit(
                            f"⚠️ Warning capturing section '{t_str}' in <code>{doc_name}</code>: {cap_err}"
                        )

                self.log_message.emit(
                    f"💾 Auto-captured <b>{captured_cnt}/{len(detected_sections)}</b> section packages for <code>{doc_name}</code> into SQLite."
                )
                self.doc_status_updated.emit(
                    doc_name,
                    f"{captured_cnt} sections (0/{captured_cnt} done)",
                    f"✓ Ingested ({captured_cnt} sections)",
                )
                ingested_results.append({
                    **doc_info,
                    "sha256": sha,
                    "page_count": source.page_count,
                    "sec_total": captured_cnt,
                    "sec_done": 0,
                })
                source.close()

            # Ensure all companion reports are linked to the primary report SHA
            if len(ingested_results) > 1:
                # Choose primary report: prefer IAR/AR, else first document in sequence
                primary_cand = next(
                    (d["sha256"] for d in ingested_results if d.get("doc_type") in ("iar", "annual_report")),
                    ingested_results[0]["sha256"],
                )
                with connect_db(self.db_path) as conn:
                    conn.execute(
                        "UPDATE reports SET parent_report_sha256 = NULL WHERE sha256 = ?",
                        (primary_cand,),
                    )
                    for d in ingested_results:
                        if d["sha256"] != primary_cand:
                            conn.execute(
                                "UPDATE reports SET parent_report_sha256 = ? WHERE sha256 = ?",
                                (primary_cand, d["sha256"]),
                            )
                    conn.commit()

            self.ingestion_finished.emit(ingested_results)
        except Exception as exc:
            self.ingestion_error.emit(str(exc))


class OneShotView(QWidget):
    """Streamlined One-Shot Autonomous Analysis View with detailed real-time progress telemetry."""

    def __init__(self, parent: QWidget | None = None, db_path: Path | str | None = None):
        super().__init__(parent)
        self.main_window = parent
        self.db_path = resolve_db_path(db_path)
        self.available_companies: list[dict[str, Any]] = []
        self.current_company: dict[str, Any] | None = None
        self.discovered_docs: list[dict[str, Any]] = []

        # Workers & pipeline state
        self._is_running = False
        self._ingestion_worker: IngestionWorker | None = None
        self._section_worker: OpenRouterWorker | None = None
        self._s1_worker: OpenRouterWorker | None = None
        self._s2_worker: OpenRouterWorker | None = None
        self._pending_section_queue: list[dict[str, Any]] = []
        self._total_sections_to_run = 0
        self._completed_sections_in_run = 0
        self._ingested_docs: list[dict[str, Any]] = []

        self._build_ui()
        self.refresh_companies()

    # =========================================================================
    # UI CONSTRUCTION
    # =========================================================================
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(10)

        # 1. Onboarding Instruction Strip
        banner = QFrame()
        banner.setStyleSheet(
            "QFrame { background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 6px; }"
        )
        b_layout = QHBoxLayout(banner)
        b_layout.setContentsMargins(12, 8, 12, 8)
        b_title = QLabel(
            "<b>🚀 One-Shot Autonomous Pipeline:</b> &nbsp; "
            "<b>1.</b> Create or Select Company &nbsp;→&nbsp; "
            "<b>2.</b> Drop PDFs into <code>sources/</code> or <code>sources/sens/</code> &nbsp;→&nbsp; "
            "<b>3.</b> Confirm Period & Click <b>Start Autonomous Analysis</b>"
        )
        b_title.setStyleSheet("color: #166534; font-size: 12px; border: none;")
        b_layout.addWidget(b_title, 1)
        root.addWidget(banner)

        # 2. Top Control Card (Company, Folders, Period, Start)
        ctrl_frame = QFrame()
        ctrl_frame.setStyleSheet(
            "QFrame { background-color: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; }"
        )
        ctrl_layout = QVBoxLayout(ctrl_frame)
        ctrl_layout.setContentsMargins(12, 10, 12, 10)
        ctrl_layout.setSpacing(8)

        # Row A: Company selector + New Company + Folder buttons
        row_a = QHBoxLayout()
        row_a.setSpacing(8)

        comp_lbl = QLabel("<b>Company:</b>")
        comp_lbl.setStyleSheet("border: none; color: #1e293b;")
        row_a.addWidget(comp_lbl)

        self.company_combo = QComboBox()
        self.company_combo.setMinimumWidth(340)
        self.company_combo.currentIndexChanged.connect(self._on_company_changed)
        row_a.addWidget(self.company_combo, 1)

        self.sector_badge = QLabel("SECTOR")
        self.sector_badge.setStyleSheet(get_sector_badge_style("retail"))
        row_a.addWidget(self.sector_badge)

        self.new_company_btn = QPushButton("+ Create / Load Company")
        self.new_company_btn.setToolTip("Scaffold or examine a company ticker and create its sources/ and sens/ folders")
        self.new_company_btn.setStyleSheet(
            "QPushButton { background-color: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; "
            "border-radius: 4px; padding: 5px 10px; font-weight: bold; } "
            "QPushButton:hover { background-color: #dbeafe; }"
        )
        self.new_company_btn.clicked.connect(self._on_new_company_clicked)
        row_a.addWidget(self.new_company_btn)

        self.open_sources_btn = QPushButton("📂 Open sources/")
        self.open_sources_btn.setToolTip("Open company sources/ folder to drop Annual Reports, AFS, or Presentations")
        self.open_sources_btn.clicked.connect(self.open_sources_folder)
        row_a.addWidget(self.open_sources_btn)

        self.open_sens_btn = QPushButton("📂 Open sources/sens/")
        self.open_sens_btn.setToolTip("Open company sources/sens/ folder to drop SENS announcements (.pdf or .txt)")
        self.open_sens_btn.clicked.connect(self.open_sens_folder)
        row_a.addWidget(self.open_sens_btn)

        self.refresh_btn = QPushButton("🔄 Scan Files")
        self.refresh_btn.setToolTip("Re-scan sources/ and sources/sens/ for newly added documents")
        self.refresh_btn.clicked.connect(self.scan_current_company_files)
        row_a.addWidget(self.refresh_btn)

        ctrl_layout.addLayout(row_a)

        # Row B: Period selection + Reorder controls + Force Re-run + Start/Stop + Open Dossier
        row_b = QHBoxLayout()
        row_b.setSpacing(10)

        per_lbl = QLabel("<b>Reporting Period:</b>")
        per_lbl.setStyleSheet("border: none; color: #1e293b;")
        row_b.addWidget(per_lbl)

        self.period_combo = QComboBox()
        self.period_combo.setEditable(True)
        self.period_combo.setMinimumWidth(110)
        for p in ["FY26", "1H26", "2H26", "1H27", "FY27", "FY25", "1H25"]:
            self.period_combo.addItem(p)
        self.period_combo.currentTextChanged.connect(self._on_period_changed)
        row_b.addWidget(self.period_combo)

        self.move_up_btn = QPushButton("▲ Move Doc Up")
        self.move_up_btn.setToolTip("Move selected document earlier in the processing queue")
        self.move_up_btn.clicked.connect(self._on_move_doc_up)
        row_b.addWidget(self.move_up_btn)

        self.move_down_btn = QPushButton("▼ Move Doc Down")
        self.move_down_btn.setToolTip("Move selected document later in the processing queue")
        self.move_down_btn.clicked.connect(self._on_move_doc_down)
        row_b.addWidget(self.move_down_btn)

        self.force_rerun_cb = QCheckBox("Force Re-run All")
        self.force_rerun_cb.setToolTip(
            "When unchecked, already-analyzed sections in SQLite are reused. "
            "Check this to wipe and re-extract/re-analyze from scratch."
        )
        self.force_rerun_cb.setStyleSheet("border: none; color: #475569;")
        row_b.addWidget(self.force_rerun_cb)

        row_b.addStretch(1)

        self.open_dossier_btn = QPushButton("🏛️ Open Valuation Dossier & Portfolio")
        self.open_dossier_btn.setToolTip("Open the full Stage 1 & 2 Audit/Valuation Dialog and Portfolio Coverage Table")
        self.open_dossier_btn.clicked.connect(self._on_open_dossier_clicked)
        row_b.addWidget(self.open_dossier_btn)

        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet(
            "QPushButton { background-color: #fee2e2; color: #991b1b; border: 1px solid #fecaca; "
            "border-radius: 5px; padding: 6px 14px; font-weight: bold; } "
            "QPushButton:disabled { background-color: #f1f5f9; color: #94a3b8; border-color: #e2e8f0; }"
        )
        self.stop_btn.clicked.connect(self.stop_pipeline)
        row_b.addWidget(self.stop_btn)

        self.start_btn = QPushButton("🚀 Start Autonomous Analysis")
        self.start_btn.setStyleSheet(
            "QPushButton { background-color: #15803d; color: #ffffff; border: 1px solid #166534; "
            "border-radius: 5px; padding: 7px 18px; font-size: 13px; font-weight: bold; } "
            "QPushButton:hover { background-color: #166534; } "
            "QPushButton:disabled { background-color: #94a3b8; border-color: #cbd5e1; }"
        )
        self.start_btn.clicked.connect(self.start_pipeline)
        row_b.addWidget(self.start_btn)

        ctrl_layout.addLayout(row_b)
        root.addWidget(ctrl_frame)

        # 3. 5-Phase Visual Pipeline Stepper Strip
        stepper_frame = QFrame()
        stepper_frame.setStyleSheet(
            "QFrame { background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; }"
        )
        stepper_layout = QVBoxLayout(stepper_frame)
        stepper_layout.setContentsMargins(12, 8, 12, 8)
        stepper_layout.setSpacing(6)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(8)
        self.phase_cards: list[QLabel] = []
        phase_titles = [
            "1. PDF Ingestion & Mapping",
            "2. Section Audit & Ledger",
            "3. Stage 1 Forensic Audit",
            "4. Stage 2 Valuation / SENS",
            "5. Archive & Portfolio Sync",
        ]
        for pt in phase_titles:
            lbl = QLabel(f"<b>{pt}</b><br><span style='font-size:11px; color:#64748b;'>Waiting</span>")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setWordWrap(True)
            lbl.setMinimumHeight(46)
            lbl.setStyleSheet(
                "QLabel { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 5px; padding: 4px 6px; }"
            )
            cards_row.addWidget(lbl, 1)
            self.phase_cards.append(lbl)
        stepper_layout.addLayout(cards_row)

        prog_row = QHBoxLayout()
        prog_row.setSpacing(10)
        self.live_banner_label = QLabel("Ready — Select a company and confirm the reporting period to begin.")
        self.live_banner_label.setStyleSheet("color: #1e293b; font-size: 12px; font-weight: 600; border: none;")
        prog_row.addWidget(self.live_banner_label, 1)

        self.overall_progress = QProgressBar()
        self.overall_progress.setMinimumWidth(260)
        self.overall_progress.setMaximumHeight(18)
        self.overall_progress.setRange(0, 100)
        self.overall_progress.setValue(0)
        prog_row.addWidget(self.overall_progress)
        stepper_layout.addLayout(prog_row)

        root.addWidget(stepper_frame)

        # 4. Main Workspace Vertical Splitter:
        #    Top: Discovered Documents Table
        #    Bottom: Horizontal Splitter (Left = Live Activity Log, Right = Live Artifact Inspector Tabs)
        main_v_splitter = QSplitter(Qt.Orientation.Vertical)

        # Top: Discovered Documents Table
        docs_widget = QWidget()
        docs_layout = QVBoxLayout(docs_widget)
        docs_layout.setContentsMargins(0, 0, 0, 0)
        docs_layout.setSpacing(4)

        self.docs_header_lbl = QLabel("<b>📄 Discovered Documents in <code>sources/</code> & <code>sources/sens/</code>:</b>")
        self.docs_header_lbl.setStyleSheet("color: #1e293b; font-size: 12px;")
        docs_layout.addWidget(self.docs_header_lbl)

        self.docs_table = QTableWidget(0, 6)
        self.docs_table.setHorizontalHeaderLabels([
            "Order",
            "Role",
            "Document Filename",
            "Pages",
            "Sections",
            "Live Pipeline Status",
        ])
        self.docs_table.verticalHeader().setVisible(False)
        self.docs_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.docs_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.docs_table.setAlternatingRowColors(True)
        hdr = self.docs_table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.docs_table.setMinimumHeight(140)
        docs_layout.addWidget(self.docs_table, 1)
        main_v_splitter.addWidget(docs_widget)

        # Bottom: Horizontal Splitter (Telemetry Log + Live Artifact Tabs)
        bottom_h_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left: Live Activity & Telemetry Log
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)
        log_layout.setContentsMargins(0, 0, 0, 0)
        log_layout.setSpacing(4)
        log_hdr = QHBoxLayout()
        log_hdr.addWidget(QLabel("<b>📡 Detailed Live Progress & Telemetry Log:</b>"))
        log_hdr.addStretch(1)
        clear_log_btn = QPushButton("Clear Log")
        clear_log_btn.setMaximumHeight(22)
        clear_log_btn.clicked.connect(lambda: self.log_view.clear())
        log_hdr.addWidget(clear_log_btn)
        log_layout.addLayout(log_hdr)

        self.log_view = QTextBrowser()
        self.log_view.setOpenExternalLinks(False)
        self.log_view.setStyleSheet(
            "QTextBrowser { background-color: #0f172a; color: #e2e8f0; font-family: Consolas, monospace; "
            "font-size: 12px; border: 1px solid #334155; border-radius: 5px; padding: 8px; }"
        )
        log_layout.addWidget(self.log_view, 1)
        bottom_h_splitter.addWidget(log_widget)

        # Right: Live Artifact Inspector Tabs
        self.output_tabs = QTabWidget()
        self.ledger_preview = QPlainTextEdit()
        self.ledger_preview.setReadOnly(True)
        self.ledger_preview.setPlaceholderText("Live Open Questions Ledger will appear and update here after each section is audited...")
        self.output_tabs.addTab(self.ledger_preview, "📋 Questions Ledger (0)")

        self.stage1_preview = QPlainTextEdit()
        self.stage1_preview.setReadOnly(True)
        self.stage1_preview.setPlaceholderText("Stage 1 Cognitive Forensic Audit response will appear here upon completion...")
        self.output_tabs.addTab(self.stage1_preview, "🔍 Stage 1 Forensic Audit")

        self.stage2_preview = QPlainTextEdit()
        self.stage2_preview.setReadOnly(True)
        self.stage2_preview.setPlaceholderText("Stage 2 Institutional Valuation Note & Rating Bands will appear here upon completion...")
        self.output_tabs.addTab(self.stage2_preview, "💎 Stage 2 Valuation Note")

        bottom_h_splitter.addWidget(self.output_tabs)
        bottom_h_splitter.setStretchFactor(0, 5)
        bottom_h_splitter.setStretchFactor(1, 5)

        main_v_splitter.addWidget(bottom_h_splitter)
        main_v_splitter.setStretchFactor(0, 3)
        main_v_splitter.setStretchFactor(1, 7)

        root.addWidget(main_v_splitter, 1)

    # =========================================================================
    # LOGGING & STEPPER HELPERS
    # =========================================================================
    def append_log(self, html_msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_view.append(f"<span style='color:#64748b;'>[{ts}]</span> {html_msg}")
        sb = self.log_view.verticalScrollBar()
        if sb:
            sb.setValue(sb.maximum())

    def set_phase_state(self, phase_idx: int, status_text: str, state: str = "active"):
        """Updates one of the 5 phase cards (`waiting`, `active`, `done`, `error`)."""
        if not (0 <= phase_idx < len(self.phase_cards)):
            return
        phase_titles = [
            "1. PDF Ingestion & Mapping",
            "2. Section Audit & Ledger",
            "3. Stage 1 Forensic Audit",
            "4. Stage 2 Valuation / SENS",
            "5. Archive & Portfolio Sync",
        ]
        title = phase_titles[phase_idx]
        if state == "active":
            bg, border, fg, sub_fg = "#eff6ff", "#3b82f6", "#1d4ed8", "#1e40af"
            icon = "⏳ "
        elif state == "done":
            bg, border, fg, sub_fg = "#f0fdf4", "#22c55e", "#15803d", "#166534"
            icon = "✓ "
        elif state == "error":
            bg, border, fg, sub_fg = "#fef2f2", "#ef4444", "#b91c1c", "#991b1b"
            icon = "❌ "
        else:
            bg, border, fg, sub_fg = "#ffffff", "#e2e8f0", "#334155", "#64748b"
            icon = ""

        lbl = self.phase_cards[phase_idx]
        lbl.setStyleSheet(
            f"QLabel {{ background-color: {bg}; border: 1.5px solid {border}; border-radius: 5px; padding: 4px 6px; color: {fg}; }}"
        )
        lbl.setText(
            f"<b>{icon}{title}</b><br><span style='font-size:11px; color:{sub_fg};'>{status_text}</span>"
        )

    def reset_phase_cards(self):
        for i in range(5):
            self.set_phase_state(i, "Waiting", "waiting")

    # =========================================================================
    # COMPANY & DOCUMENT DISCOVERY
    # =========================================================================
    def refresh_companies(self, select_ticker: str | None = None):
        self.available_companies = discover_available_companies(self.db_path)
        self.company_combo.blockSignals(True)
        self.company_combo.clear()

        target_idx = 0
        for idx, comp in enumerate(self.available_companies):
            self.company_combo.addItem(comp["display_text"], comp)
            if select_ticker and comp["ticker"].upper() == select_ticker.upper():
                target_idx = idx

        self.company_combo.blockSignals(False)
        if self.available_companies:
            self.company_combo.setCurrentIndex(target_idx)
            self._on_company_changed(target_idx)
        else:
            self.current_company = None
            self.docs_table.setRowCount(0)

    def _on_company_changed(self, index: int):
        if index < 0 or index >= len(self.available_companies):
            return
        comp = self.company_combo.itemData(index)
        if not comp:
            return
        self.current_company = comp
        sector = comp.get("sector", "retail")
        self.sector_badge.setText(get_sector_short_label(sector))
        self.sector_badge.setStyleSheet(get_sector_badge_style(sector))
        self.scan_current_company_files()

    def _get_current_company_dir(self) -> Path | None:
        if not self.current_company:
            return None
        ticker = self.current_company["ticker"]
        sector = self.current_company.get("sector", "retail")
        comp_info = find_company_dir(ticker, sector=sector)
        return comp_info[1] if comp_info else (PROJECT_ROOT / "companies" / sector / ticker)

    def scan_current_company_files(self):
        comp_dir = self._get_current_company_dir()
        if not comp_dir:
            return
        ticker = self.current_company["ticker"]
        hint_period = self.current_company.get("period")
        docs, detected_period = discover_company_documents(
            comp_dir, period=hint_period, db_path=self.db_path
        )
        self.discovered_docs = docs

        # Set period combo
        if detected_period:
            idx = self.period_combo.findText(detected_period)
            if idx >= 0:
                self.period_combo.setCurrentIndex(idx)
            else:
                self.period_combo.setEditText(detected_period)

        self._populate_docs_table()
        self._load_existing_artifacts_preview()

        pdf_cnt = sum(1 for d in docs if not d.get("is_sens"))
        sens_cnt = sum(1 for d in docs if d.get("is_sens"))
        if docs:
            self.docs_header_lbl.setText(
                f"<b>📄 Discovered Documents for {ticker} ({pdf_cnt} Report PDF(s), {sens_cnt} SENS Notice(s)):</b>"
            )
            names = ", ".join(d["filename"] for d in docs)
            self.live_banner_label.setText(
                f"Ready — Found {len(docs)} document(s) for {ticker} ({self.period_combo.currentText()}): {names}"
            )
            self.start_btn.setEnabled(True)
            self.start_btn.setToolTip("Start the 5-phase autonomous pipeline for these documents")
        else:
            active_p = self.period_combo.currentText().strip() or "FY26"
            self.docs_header_lbl.setText(
                f"<b>✓ All source reports for {ticker} ({active_p}) have been analyzed and moved to <code>sources/completed/{active_p}/</code>.</b>"
            )
            self.live_banner_label.setText(
                f"✓ Analysis Complete: All source documents for {ticker} ({active_p}) are archived. "
                f"Review the Questions Ledger, Stage 1 Audit, and Stage 2 Valuation Note below."
            )
            self.start_btn.setEnabled(False)
            self.start_btn.setToolTip("No pending files in sources/ or sources/sens/. Drop new PDFs or SENS files to analyze.")

    def _populate_docs_table(self):
        self.docs_table.setRowCount(len(self.discovered_docs))
        for row_idx, d in enumerate(self.discovered_docs):
            # Col 0: Order + Checkbox
            chk_item = QTableWidgetItem(f"  {row_idx + 1}")
            chk_item.setFlags(
                Qt.ItemFlag.ItemIsEnabled
                | Qt.ItemFlag.ItemIsSelectable
                | Qt.ItemFlag.ItemIsUserCheckable
            )
            chk_item.setCheckState(Qt.CheckState.Checked)
            chk_item.setData(Qt.ItemDataRole.UserRole, d)
            self.docs_table.setItem(row_idx, 0, chk_item)

            # Col 1: Role Badge
            badge_str = d.get("badge", "[AR]")
            if d.get("is_archived"):
                badge_str += " (Archived)"
            role_item = QTableWidgetItem(badge_str)
            role_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.docs_table.setItem(row_idx, 1, role_item)

            # Col 2: Filename
            fn_item = QTableWidgetItem(d["filename"])
            self.docs_table.setItem(row_idx, 2, fn_item)

            # Col 3: Pages
            p_cnt = d.get("page_count", 0)
            p_str = f"{p_cnt} pages" if p_cnt else "Text"
            p_item = QTableWidgetItem(p_str)
            p_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.docs_table.setItem(row_idx, 3, p_item)

            # Col 4: Sections
            if d.get("is_sens"):
                sec_str = "Post-balance sheet"
                status_str = "Queued for Stage 2 / SENS"
            else:
                st = d.get("sec_total", 0)
                sd = d.get("sec_done", 0)
                if st > 0:
                    sec_str = f"{st} sections ({sd}/{st} done)"
                    status_str = "✓ All Sections Audited" if sd == st else f"⏳ {st - sd} Pending Audit"
                else:
                    sec_str = "Auto-map on start"
                    status_str = "Ready to Ingest"

            sec_item = QTableWidgetItem(sec_str)
            sec_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.docs_table.setItem(row_idx, 4, sec_item)

            # Col 5: Status
            st_item = QTableWidgetItem(status_str)
            self.docs_table.setItem(row_idx, 5, st_item)

    def _update_doc_table_row(self, filename: str, sections_text: str, status_text: str):
        for r in range(self.docs_table.rowCount()):
            fn_item = self.docs_table.item(r, 2)
            if fn_item and fn_item.text() == filename:
                if sections_text:
                    self.docs_table.item(r, 4).setText(sections_text)
                if status_text:
                    self.docs_table.item(r, 5).setText(status_text)
                break

    def _on_move_doc_up(self):
        row = self.docs_table.currentRow()
        if row <= 0 or self._is_running:
            return
        self._swap_doc_rows(row, row - 1)
        self.docs_table.selectRow(row - 1)

    def _on_move_doc_down(self):
        row = self.docs_table.currentRow()
        if row < 0 or row >= self.docs_table.rowCount() - 1 or self._is_running:
            return
        self._swap_doc_rows(row, row + 1)
        self.docs_table.selectRow(row + 1)

    def _swap_doc_rows(self, r1: int, r2: int):
        self.discovered_docs[r1], self.discovered_docs[r2] = (
            self.discovered_docs[r2],
            self.discovered_docs[r1],
        )
        self._populate_docs_table()

    def get_selected_ordered_documents(self) -> list[dict[str, Any]]:
        selected: list[dict[str, Any]] = []
        for r in range(self.docs_table.rowCount()):
            item = self.docs_table.item(r, 0)
            if item and item.checkState() == Qt.CheckState.Checked:
                d = item.data(Qt.ItemDataRole.UserRole)
                if d:
                    selected.append(d)
        return selected

    def _on_period_changed(self, text: str):
        if getattr(self, "_is_loading_period", False):
            return
        self._load_existing_artifacts_preview()

    def _load_existing_artifacts_preview(self):
        """Loads any existing Questions Ledger, Stage 1 Audit, and Stage 2 Valuation Note for the active company."""
        self.ledger_preview.clear()
        self.stage1_preview.clear()
        self.stage2_preview.clear()
        self.output_tabs.setTabText(0, "📋 Questions Ledger (0)")

        comp_dir = self._get_current_company_dir()
        if not comp_dir or not self.current_company:
            return
        ticker = self.current_company["ticker"]
        period = self.period_combo.currentText().strip() or "FY26"
        briefs_dir = comp_dir / "briefs" / period

        # If current period has no brief files, find if any other period subfolder has them
        if not (briefs_dir / f"{ticker}_{period}_stage1_audit_response.md").exists() and not (briefs_dir / f"{ticker}_{period}_stage2_valuation_note.md").exists():
            b_root = comp_dir / "briefs"
            if b_root.exists():
                for cand_dir in sorted([d for d in b_root.iterdir() if d.is_dir()], reverse=True):
                    cand_p = cand_dir.name
                    cand_s1 = cand_dir / f"{ticker}_{cand_p}_stage1_audit_response.md"
                    cand_s2 = cand_dir / f"{ticker}_{cand_p}_stage2_valuation_note.md"
                    if cand_s1.exists() or cand_s2.exists():
                        period = cand_p
                        briefs_dir = cand_dir
                        self._is_loading_period = True
                        idx = self.period_combo.findText(period)
                        if idx >= 0:
                            self.period_combo.setCurrentIndex(idx)
                        else:
                            self.period_combo.setEditText(period)
                        self._is_loading_period = False
                        break

        # Check Questions Ledger in DB across discovered PDFs or reports table for this ticker
        ql = ""
        for d in self.discovered_docs:
            sha = d.get("sha256")
            if sha and not d.get("is_sens"):
                ql = load_questions_ledger(sha, questions_root=self.db_path) or ""
                if ql.strip():
                    break
        if not ql:
            try:
                with connect_db(self.db_path) as conn:
                    row = conn.execute(
                        "SELECT questions_ledger FROM reports WHERE (original_path LIKE ? OR filename LIKE ?) AND questions_ledger IS NOT NULL AND length(questions_ledger) > 0 ORDER BY updated_at DESC LIMIT 1",
                        (f"%{ticker}%", f"%{ticker}%"),
                    ).fetchone()
                    if row:
                        ql = row["questions_ledger"] or ""
            except Exception:
                pass

        if ql and ql.strip():
            q_cnt = len(re.findall(r"(?m)^-\s*Q\d+", ql)) or len(ql.splitlines())
            self.ledger_preview.setPlainText(ql)
            self.output_tabs.setTabText(0, f"📋 Questions Ledger ({q_cnt})")

        # Check Stage 1 & Stage 2 files on disk
        s1_file = briefs_dir / f"{ticker}_{period}_stage1_audit_response.md"
        if s1_file.exists():
            try:
                self.stage1_preview.setPlainText(s1_file.read_text(encoding="utf-8"))
            except Exception:
                pass

        s2_file = briefs_dir / f"{ticker}_{period}_stage2_valuation_note.md"
        if s2_file.exists():
            try:
                self.stage2_preview.setPlainText(s2_file.read_text(encoding="utf-8"))
            except Exception:
                pass

    # =========================================================================
    # FOLDER & DIALOG ACTIONS
    # =========================================================================
    def open_sources_folder(self):
        comp_dir = self._get_current_company_dir()
        if not comp_dir:
            return
        sources_dir = comp_dir / "sources"
        sources_dir.mkdir(parents=True, exist_ok=True)
        open_folder_and_select(sources_dir)

    def open_sens_folder(self):
        comp_dir = self._get_current_company_dir()
        if not comp_dir:
            return
        sens_dir = comp_dir / "sources" / "sens"
        sens_dir.mkdir(parents=True, exist_ok=True)
        open_folder_and_select(sens_dir)

    def _on_new_company_clicked(self):
        if self.main_window and hasattr(self.main_window, "show_new_company_dialog"):
            self.main_window.show_new_company_dialog()

    def _on_open_dossier_clicked(self):
        if not self.current_company:
            return
        dlg = AuditValuationDialog(
            source=None,
            parent=self.main_window or self,
            db_path=self.db_path,
        )
        # Select current ticker in dialog
        ticker = self.current_company["ticker"]
        for i in range(dlg.company_combo.count()):
            data = dlg.company_combo.itemData(i)
            if data and data.get("ticker") == ticker:
                dlg.company_combo.setCurrentIndex(i)
                break
        dlg.show()

    # =========================================================================
    # AUTONOMOUS PIPELINE ORCHESTRATION
    # =========================================================================
    def _set_running_ui(self, running: bool):
        self._is_running = running
        self.start_btn.setEnabled(not running)
        self.stop_btn.setEnabled(running)
        self.company_combo.setEnabled(not running)
        self.period_combo.setEnabled(not running)
        self.new_company_btn.setEnabled(not running)
        self.refresh_btn.setEnabled(not running)
        self.move_up_btn.setEnabled(not running)
        self.move_down_btn.setEnabled(not running)
        self.force_rerun_cb.setEnabled(not running)

    def stop_pipeline(self):
        if not self._is_running:
            return
        self.append_log("🛑 <b>Stopping autonomous pipeline at user request...</b>")
        if self._ingestion_worker and self._ingestion_worker.isRunning():
            self._ingestion_worker.cancel()
            self._ingestion_worker.wait(2000)
        if self._section_worker and self._section_worker.isRunning():
            self._section_worker.terminate()
            self._section_worker.wait(1000)
        if self._s1_worker and self._s1_worker.isRunning():
            self._s1_worker.terminate()
            self._s1_worker.wait(1000)
        if self._s2_worker and self._s2_worker.isRunning():
            self._s2_worker.terminate()
            self._s2_worker.wait(1000)
        self._pending_section_queue.clear()
        self._set_running_ui(False)
        self.live_banner_label.setText("⏹ Pipeline stopped by user.")

    def start_pipeline(self, use_llm_clustering: bool = True):
        if self._is_running:
            return
        if not self.current_company:
            QMessageBox.warning(self, "No Company Selected", "Please select or create a company first.")
            return

        selected_docs = self.get_selected_ordered_documents()
        if not selected_docs:
            QMessageBox.warning(
                self,
                "No Documents Found",
                "No PDFs or SENS files are selected.\n\n"
                "Drop company PDFs into 'sources/' or SENS notices into 'sources/sens/' and click '🔄 Scan Files'.",
            )
            return

        api_key = get_openrouter_api_key()
        if not api_key:
            QMessageBox.critical(
                self,
                "Missing OpenRouter API Key",
                "OpenRouter API key not found in secrets.env or environment.",
            )
            return

        ticker = self.current_company["ticker"]
        company_title = self.current_company["company_title"]
        sector = self.current_company.get("sector", "retail")
        period = self.period_combo.currentText().strip() or "FY26"
        force_rerun = self.force_rerun_cb.isChecked()

        self._set_running_ui(True)
        self.reset_phase_cards()
        self.overall_progress.setValue(2)

        doc_names_list = ", ".join(f"{d.get('badge', '[DOC]')} {d['filename']}" for d in selected_docs)
        self.append_log("=" * 72)
        self.append_log(
            f"🚀 <b>STARTING ONE-SHOT AUTONOMOUS PIPELINE: {ticker} ({company_title})</b>"
        )
        self.append_log(
            f"📌 <b>Sector:</b> {sector.upper()} &nbsp;|&nbsp; <b>Period:</b> {period} "
            f"&nbsp;|&nbsp; <b>Documents ({len(selected_docs)}):</b> {doc_names_list}"
        )
        self.append_log("=" * 72)

        # Check if this is a SENS-Only Update on an existing baseline valuation
        comp_dir = self._get_current_company_dir()
        briefs_dir = comp_dir / "briefs" / period
        s2_note_file = briefs_dir / f"{ticker}_{period}_stage2_valuation_note.md"
        sens_docs = [d for d in selected_docs if d.get("is_sens")]
        pdf_docs = [d for d in selected_docs if not d.get("is_sens")]
        all_pdfs_archived = all(d.get("is_archived") for d in pdf_docs) if pdf_docs else True

        if sens_docs and s2_note_file.exists() and all_pdfs_archived and not force_rerun:
            self.append_log(
                f"⚡ <b>Smart SENS Update Mode Detected:</b> Baseline valuation note "
                f"<code>{s2_note_file.name}</code> already exists and {len(sens_docs)} new SENS notice(s) found."
            )
            self.set_phase_state(0, "Skipped (Baseline exists)", "done")
            self.set_phase_state(1, "Skipped (Baseline exists)", "done")
            self.set_phase_state(2, "Skipped (Baseline exists)", "done")
            self.overall_progress.setValue(65)
            self._ingested_docs = pdf_docs
            self._run_phase4_sens_only_update(sens_docs, s2_note_file.read_text(encoding="utf-8"))
            return

        # Phase 1: Launch IngestionWorker
        self.set_phase_state(0, f"Ingesting {len(pdf_docs)} PDF(s)...", "active")
        self._ingestion_worker = IngestionWorker(
            docs=selected_docs,
            period=period,
            sector=sector,
            db_path=self.db_path,
            force_rerun=force_rerun,
            use_llm_clustering=use_llm_clustering,
            parent=self,
        )
        self._ingestion_worker.log_message.connect(self.append_log)
        self._ingestion_worker.doc_status_updated.connect(self._update_doc_table_row)
        self._ingestion_worker.step_progress.connect(self._on_ingestion_progress)
        self._ingestion_worker.ingestion_finished.connect(self._on_phase1_finished)
        self._ingestion_worker.ingestion_error.connect(self._on_pipeline_error)
        self._ingestion_worker.start()

    def _on_ingestion_progress(self, current: int, total: int, banner_msg: str):
        self.live_banner_label.setText(banner_msg)
        pct = min(20, max(2, int((current / max(1, total)) * 20)))
        self.overall_progress.setValue(pct)

    def _on_phase1_finished(self, ingested_docs: list[dict[str, Any]]):
        if not self._is_running:
            return
        self._ingested_docs = ingested_docs
        total_secs = sum(d.get("sec_total", 0) for d in ingested_docs)
        doc_names = ", ".join(d["filename"] for d in ingested_docs)
        self.set_phase_state(0, f"✓ {len(ingested_docs)} PDF(s) ({total_secs} sections)", "done")
        self.append_log(
            f"✅ <b>Phase 1 Complete:</b> Ingested {len(ingested_docs)} document(s) ({doc_names}) "
            f"with {total_secs} total sections."
        )
        self.overall_progress.setValue(20)
        self._run_phase2_section_queue()

    # =========================================================================
    # PHASE 2: SEQUENTIAL SECTION AUDIT & QUESTIONS LEDGER
    # =========================================================================
    def _run_phase2_section_queue(self):
        if not self._is_running:
            return
        self._pending_section_queue.clear()

        for doc_idx, d in enumerate(self._ingested_docs):
            sha = d["sha256"]
            fn = d["filename"]
            badge = d.get("badge", "[DOC]")
            dt = d.get("doc_type", "annual_report")
            path = d["path"]
            secs = list_sections(sha, db_path=self.db_path)
            pend_secs = [s for s in secs if not (s.llm_response or "").strip()]
            for s in pend_secs:
                self._pending_section_queue.append({
                    "section": s,
                    "doc_sha": sha,
                    "doc_filename": fn,
                    "doc_badge": badge,
                    "doc_type": dt,
                    "doc_path": path,
                    "doc_index": doc_idx + 1,
                    "doc_total": len(self._ingested_docs),
                    "doc_sec_total": len(secs),
                })

        self._total_sections_to_run = len(self._pending_section_queue)
        self._completed_sections_in_run = 0

        if self._total_sections_to_run == 0:
            self.append_log("✅ <b>Phase 2 Complete:</b> All captured sections are already audited in SQLite.")
            self.set_phase_state(1, "✓ All sections audited", "done")
            self.overall_progress.setValue(55)
            self._run_phase3_stage1()
            return

        self.append_log(
            f"⚡ <b>Starting Phase 2 (Sequential Section Audit):</b> "
            f"Queuing <b>{self._total_sections_to_run} section(s)</b> across {len(self._ingested_docs)} document(s)..."
        )
        self.set_phase_state(
            1, f"0 / {self._total_sections_to_run} sections audited", "active"
        )
        self._process_next_section()

    def _process_next_section(self):
        if not self._is_running:
            return
        if not self._pending_section_queue:
            self.set_phase_state(
                1, f"✓ {self._total_sections_to_run}/{self._total_sections_to_run} sections audited", "done"
            )
            self.append_log(
                f"✅ <b>Phase 2 Complete:</b> Audited all {self._total_sections_to_run} sections and "
                f"synchronized Questions Ledger."
            )
            self.overall_progress.setValue(55)
            self._run_phase3_stage1()
            return

        item = self._pending_section_queue.pop(0)
        sec = item["section"]
        sha = item["doc_sha"]
        fn = item["doc_filename"]
        badge = item["doc_badge"]
        dt = item["doc_type"]
        doc_path = item["doc_path"]
        doc_sec_total = item["doc_sec_total"]

        curr_idx = self._completed_sections_in_run + 1
        total_q = self._total_sections_to_run
        period = self.period_combo.currentText().strip() or "FY26"
        sector = self.current_company.get("sector", "retail")

        # Rebuild prompt with the latest accumulated Questions Ledger from SQLite
        prompt_to_send = sec.prompt
        try:
            import copy
            latest_ledger = load_questions_ledger(sha, questions_root=self.db_path) or ""
            manifest = copy.deepcopy(sec.manifest) if getattr(sec, "manifest", None) else {}
            if "heading" not in manifest:
                manifest["heading"] = sec.heading
            if "subheading" not in manifest and sec.subheading:
                manifest["subheading"] = sec.subheading
            if "package_id" not in manifest:
                manifest["package_id"] = sec.package_id
            if "source" not in manifest:
                manifest["source"] = {"filename": fn, "sha256": sha}
            elif "sha256" not in manifest["source"]:
                manifest["source"]["sha256"] = sha
            if "selections" not in manifest:
                manifest["selections"] = getattr(sec, "selections", None) or []

            manifest["stored_questions"] = latest_ledger.strip() or None
            manifest["sector"] = sector
            texts = extract_selection_texts(manifest, selected_text=sec.selected_text, prompt=sec.prompt)
            prompt_to_send = build_prompt(manifest, texts, sector=sector)
            with connect_db(self.db_path) as conn:
                conn.execute(
                    "UPDATE sections SET prompt = ?, manifest_json = ? WHERE package_id = ?",
                    (prompt_to_send, json.dumps(manifest, ensure_ascii=False), sec.package_id),
                )
        except Exception:
            pass

        self._update_doc_table_row(
            fn,
            f"{sec.section_number}/{doc_sec_total} auditing",
            f"⚡ Auditing S{sec.section_number:02d}: {sec.heading[:24]}...",
        )
        self.set_phase_state(
            1, f"Sec {curr_idx}/{total_q}: {sec.heading[:28]}...", "active"
        )
        self.live_banner_label.setText(
            f"⚡ [Phase 2/5] ({curr_idx}/{total_q}) {badge} {fn} — Auditing Section #{sec.section_number}: {sec.heading}"
        )
        pct = 20 + int(((curr_idx - 1) / max(1, total_q)) * 35)
        self.overall_progress.setValue(pct)

        self.append_log(
            f"⚡ <b>[Sec {curr_idx}/{total_q}]</b> <code>{fn}</code> — Auditing "
            f"<b>#{sec.section_number} {sec.heading}</b>..."
        )

        model = get_openrouter_model()
        self._section_worker = OpenRouterWorker(prompt_to_send, model=model, parent=self)

        def on_sec_done(resp_text: str, elapsed: float, stats: dict):
            if not self._is_running:
                return
            stats = stats or {}
            tokens = {
                "prompt_tokens": stats.get("prompt_tokens"),
                "completion_tokens": stats.get("completion_tokens"),
                "total_tokens": stats.get("total_tokens"),
            }
            _, extracted = save_section_llm_response(
                sec.package_id,
                resp_text,
                update_ledger=True,
                response_time_seconds=elapsed,
                cost_usd=stats.get("cost_usd"),
                tokens=tokens,
                model=model,
                db_path=self.db_path,
            )
            self._completed_sections_in_run += 1

            # Check updated Questions Ledger
            new_ledger = extracted or load_questions_ledger(sha, questions_root=self.db_path)
            q_cnt = 0
            if new_ledger:
                q_cnt = len(re.findall(r"(?m)^-\s*Q\d+", new_ledger)) or len(new_ledger.splitlines())
                self.ledger_preview.setPlainText(new_ledger)
                self.output_tabs.setTabText(0, f"📋 Questions Ledger ({q_cnt})")

            tok = stats.get("total_tokens", 0)
            self.append_log(
                f"✓ <b>[Sec {self._completed_sections_in_run}/{total_q}]</b> Completed "
                f"<b>{sec.heading}</b> in {elapsed:.1f}s ({tok:,} tokens) — "
                f"Questions Ledger: <b>{q_cnt} open questions</b>."
            )

            # Check if all sections of this document are now done
            all_doc_secs = list_sections(sha, db_path=self.db_path)
            done_doc_secs = sum(1 for s in all_doc_secs if (s.llm_response or "").strip())
            self._update_doc_table_row(
                fn,
                f"{len(all_doc_secs)} sections ({done_doc_secs}/{len(all_doc_secs)} done)",
                "✓ All Sections Audited"
                if done_doc_secs == len(all_doc_secs)
                else f"⏳ {len(all_doc_secs) - done_doc_secs} remaining",
            )
            self._process_next_section()

        def on_sec_err(err_msg: str):
            self._on_pipeline_error(f"Section Audit failed on '{sec.heading}' ({fn}): {err_msg}")

        self._section_worker.finished_query.connect(on_sec_done)
        self._section_worker.error_query.connect(on_sec_err)
        self._section_worker.start()

    # =========================================================================
    # PHASE 3: STAGE 1 COGNITIVE FORENSIC AUDIT
    # =========================================================================
    def _run_phase3_stage1(self):
        if not self._is_running or not self.current_company:
            return

        ticker = self.current_company["ticker"]
        company_title = self.current_company["company_title"]
        sector = self.current_company.get("sector", "retail")
        period = self.period_combo.currentText().strip() or "FY26"
        comp_dir = self._get_current_company_dir()
        briefs_dir = comp_dir / "briefs" / period
        briefs_dir.mkdir(parents=True, exist_ok=True)

        if not self._ingested_docs:
            self._on_pipeline_error("No ingested report documents available for Stage 1.")
            return

        # Identify primary SHA
        primary_doc = next(
            (d for d in self._ingested_docs if d.get("doc_type") in ("iar", "annual_report")),
            self._ingested_docs[0],
        )
        primary_sha = primary_doc["sha256"]
        primary_filename = primary_doc["filename"]

        # Check if Stage 1 already exists and Force Re-run is unchecked
        s1_out_file = briefs_dir / f"{ticker}_{period}_stage1_audit_response.md"
        if not self.force_rerun_cb.isChecked() and s1_out_file.exists():
            existing_s1 = s1_out_file.read_text(encoding="utf-8").strip()
            if existing_s1 and self._total_sections_to_run == 0:
                self.stage1_preview.setPlainText(existing_s1)
                self.set_phase_state(2, f"✓ Reused ({len(existing_s1):,} chars)", "done")
                self.append_log(
                    f"✓ <b>Phase 3 (Stage 1 Audit):</b> Reusing existing Stage 1 response "
                    f"<code>{s1_out_file.name}</code> ({len(existing_s1):,} chars)."
                )
                self.overall_progress.setValue(75)
                self._run_phase4_stage2(existing_s1)
                return

        self.set_phase_state(2, "Compiling Stage 1 dossier...", "active")
        self.live_banner_label.setText(f"🔍 [Phase 3/5] Compiling Stage 1 Forensic Audit Prompt for {ticker}...")

        # Gather primary & companion sections from SQLite
        with connect_db(self.db_path) as conn:
            cur = conn.cursor()
            rep = cur.execute(
                "SELECT questions_ledger FROM reports WHERE sha256 = ?", (primary_sha,)
            ).fetchone()
            final_ledger = rep["questions_ledger"] if rep else None

            primary_sections = cur.execute(
                """
                SELECT section_number, section_id, heading, subheading, analyst_question,
                       selected_text, stored_questions_snapshot, llm_response
                FROM sections
                WHERE report_sha256 = ?
                ORDER BY section_number ASC, id ASC
                """,
                (primary_sha,),
            ).fetchall()

            companion_reports: list[dict[str, Any]] = []
            for d in self._ingested_docs:
                if d["sha256"] == primary_sha:
                    continue
                c_secs = cur.execute(
                    """
                    SELECT section_number, section_id, heading, subheading, analyst_question,
                           selected_text, stored_questions_snapshot, llm_response
                    FROM sections
                    WHERE report_sha256 = ?
                    ORDER BY section_number ASC, id ASC
                    """,
                    (d["sha256"],),
                ).fetchall()
                if c_secs:
                    companion_reports.append({
                        "sha256": d["sha256"],
                        "filename": d["filename"],
                        "doc_type": d.get("doc_type", "afs"),
                        "sections": c_secs,
                    })

        s1_prompt = build_stage1_prompt_content(
            sections=primary_sections,
            company_title=company_title,
            ticker=ticker,
            detected_sector=sector,
            filename=primary_filename,
            companion_reports=companion_reports if companion_reports else None,
            sens_reports=None,
            final_questions_ledger=final_ledger,
            compact=True,
        )

        # Save Stage 1 prompt to DB & disk
        save_stage1_report(primary_sha, prompt=s1_prompt, db_path=self.db_path)
        s1_prompt_file = briefs_dir / f"{ticker}_{period}_stage1_forensic_prompt.md"
        s1_prompt_file.write_text(s1_prompt, encoding="utf-8")

        tok_est = len(s1_prompt) // 4
        model = get_openrouter_model()
        model_name = get_model_display_name(model)
        self.set_phase_state(2, f"Running {model_name} (~{tok_est:,} tok)...", "active")
        self.live_banner_label.setText(
            f"🔍 [Phase 3/5] Running Stage 1 Cognitive Forensic Audit with {model_name} (~{tok_est:,} tokens)..."
        )
        self.append_log(
            f"🔍 <b>Phase 3 (Stage 1 Forensic Audit):</b> Compiled prompt "
            f"<code>{s1_prompt_file.name}</code> ({len(s1_prompt):,} chars, ~{tok_est:,} tokens). "
            f"Submitting to <b>{model_name}</b>..."
        )

        self._s1_worker = OpenRouterWorker(
            s1_prompt, model=model, parent=self, timeout=300, max_tokens=16384
        )

        def on_s1_done(resp_text: str, elapsed: float, stats: dict):
            if not self._is_running:
                return
            save_stage1_report(primary_sha, response=resp_text, db_path=self.db_path)
            s1_out_file.write_text(resp_text, encoding="utf-8")
            self.stage1_preview.setPlainText(resp_text)
            self.output_tabs.setCurrentIndex(1)

            tok = stats.get("total_tokens", 0)
            self.set_phase_state(2, f"✓ Done in {elapsed:.1f}s ({tok:,} tok)", "done")
            self.append_log(
                f"✅ <b>Phase 3 Complete:</b> Stage 1 Forensic Audit finished in {elapsed:.1f}s "
                f"({len(resp_text):,} chars, {tok:,} tokens). Saved to <code>{s1_out_file.name}</code>."
            )
            self.overall_progress.setValue(75)
            self._run_phase4_stage2(resp_text)

        def on_s1_err(err_msg: str):
            self._on_pipeline_error(f"Stage 1 Forensic Audit failed: {err_msg}")

        self._s1_worker.finished_query.connect(on_s1_done)
        self._s1_worker.error_query.connect(on_s1_err)
        self._s1_worker.start()

    # =========================================================================
    # PHASE 4: STAGE 2 INSTITUTIONAL VALUATION (OR SENS UPDATE)
    # =========================================================================
    def _obtain_reference_price(self, ticker: str) -> float | None:
        """Obtains the verified JSE closing price for the company.
        Strict rule: Either live price from yfinance (<TICKER>.JO) or explicit user input via dialog.
        Never uses stale cache values and never guesses.
        """
        self.append_log(
            f"📈 Fetching live JSE closing price for <code>{ticker}.JO</code> via Yahoo Finance (yfinance)..."
        )
        ref_quote = None
        try:
            ref_quote = fetch_jse_quote(ticker)
        except Exception as exc:
            pass

        if ref_quote and ref_quote.get("price_zar") and ref_quote["price_zar"] > 0:
            price = ref_quote["price_zar"]
            save_market_quotes({ticker: ref_quote}, self.db_path)
            self.append_log(
                f"✓ <b>Live Closing Price:</b> <code>{ticker}.JO</code> is <b>R{price:,.2f}</b> via Yahoo Finance."
            )
            return price

        # If yfinance fails: STRICTLY prompt the user (no guessing, no cache)
        self.append_log(
            f"⚠️ Yahoo Finance quote unavailable for <code>{ticker}.JO</code>. "
            f"Prompting user for verified closing price (no guessing)..."
        )
        price, ok = QInputDialog.getDouble(
            self,
            f"JSE Closing Price Required — {ticker}",
            f"Could not retrieve the live closing price from Yahoo Finance for '{ticker}.JO'.\n\n"
            f"Please enter the latest closing share price in ZAR (do not guess):",
            value=0.00,
            minValue=0.01,
            maxValue=1000000.0,
            decimals=2,
        )
        if ok and price > 0:
            price = round(price, 2)
            manual_quote = {
                "ticker": ticker.upper(),
                "symbol": f"{ticker.upper()}.JO",
                "price_zar": price,
                "raw_price": round(price * 100.0, 2),
                "currency": "ZAc",
                "updated_at": datetime.now().isoformat(),
            }
            save_market_quotes({ticker: manual_quote}, self.db_path)
            self.append_log(
                f"✍️ <b>User Input Received:</b> Using confirmed closing price for {ticker}: <b>R{price:,.2f}</b>."
            )
            return price

        self.append_log(
            f"❌ Closing price was not provided for {ticker}. Aborting valuation."
        )
        return None

    def _run_phase4_stage2(self, stage1_response_text: str):
        if not self._is_running or not self.current_company:
            return

        ticker = self.current_company["ticker"]
        company_title = self.current_company["company_title"]
        sector = self.current_company.get("sector", "retail")
        period = self.period_combo.currentText().strip() or "FY26"
        comp_dir = self._get_current_company_dir()
        briefs_dir = comp_dir / "briefs" / period
        briefs_dir.mkdir(parents=True, exist_ok=True)

        primary_doc = next(
            (d for d in self._ingested_docs if d.get("doc_type") in ("iar", "annual_report")),
            self._ingested_docs[0],
        )
        primary_sha = primary_doc["sha256"]
        primary_filename = primary_doc["filename"]

        selected_docs = self.get_selected_ordered_documents()
        sens_docs = [d for d in selected_docs if d.get("is_sens")]
        sens_labels = [
            f"`{d['filename']}` ({d.get('announcement_date') or 'SENS'})" for d in sens_docs
        ]

        ref_price = self._obtain_reference_price(ticker)
        if ref_price is None:
            self._on_pipeline_error(
                f"Valuation aborted: A verified closing price is required for {ticker}. "
                f"Please provide the closing price to proceed."
            )
            return

        self.set_phase_state(3, "Ingesting full PDFs & building dossier...", "active")
        self.live_banner_label.setText(
            f"💎 [Phase 4/5] Building Stage 2 Institutional Valuation Dossier for {ticker} (Ref: R{ref_price:,.2f})..."
        )

        base_s2_prompt = build_stage2_prompt_content(
            stage1_content=stage1_response_text,
            company_title=company_title,
            ticker=ticker,
            detected_sector=sector,
            sens_announcements=sens_labels if sens_labels else None,
            reference_price_zar=ref_price,
        )

        s2_prompt_file = briefs_dir / f"{ticker}_{period}_stage2_valuation_prompt.md"
        s2_prompt_file.write_text(base_s2_prompt, encoding="utf-8")
        save_stage2_report(primary_sha, prompt=base_s2_prompt, db_path=self.db_path)

        # Extract full text across all ingested source PDFs
        import pypdfium2 as pdfium

        all_pdf_blocks: list[str] = []
        for d in self._ingested_docs:
            pdf_p = Path(d["path"])
            if not pdf_p.exists():
                continue
            doc = pdfium.PdfDocument(str(pdf_p))
            pages_txt = [
                f"--- [{pdf_p.name} | Page {i + 1} of {len(doc)}] ---\n"
                + page.get_textpage().get_text_range().strip()
                for i, page in enumerate(doc)
            ]
            all_pdf_blocks.append(
                f"## SOURCE DISCLOSURE FILE: {pdf_p.name} ({len(doc)} Pages)\n\n"
                + "\n\n".join(pages_txt)
            )
            doc.close()

        # Extract SENS notices if any
        sens_blocks: list[str] = []
        for sd in sens_docs:
            sf = Path(sd["path"])
            if not sf.exists():
                continue
            if sf.suffix.lower() in {".txt", ".text", ".md"}:
                sens_blocks.append(
                    f"### SENS ANNOUNCEMENT: {sf.name}\n\n{sf.read_text(encoding='utf-8').strip()}"
                )
            elif sf.suffix.lower() == ".pdf":
                doc_s = pdfium.PdfDocument(str(sf))
                s_pages = [page.get_textpage().get_text_range().strip() for page in doc_s]
                sens_blocks.append(
                    f"### SENS ANNOUNCEMENT (PDF): {sf.name} ({len(doc_s)} Pages)\n\n"
                    + "\n\n".join(s_pages)
                )
                doc_s.close()

        dossier_parts = [base_s2_prompt]
        if sens_blocks:
            dossier_parts.append(
                "# SUBSEQUENT SENS ANNOUNCEMENTS & POST-BALANCE SHEET EVENTS\n\n"
                + "\n\n---\n\n".join(sens_blocks)
            )
        pdf_names_str = ", ".join(d["filename"] for d in self._ingested_docs)
        sens_names_str = (", ".join(d["filename"] for d in sens_docs)) if sens_docs else ""
        sources_summary = pdf_names_str + (f" + SENS: {sens_names_str}" if sens_names_str else "")

        dossier_parts.append(
            f"# COMPLETE PRIMARY SOURCE FINANCIAL REPORT DISCLOSURES & AUDITED NOTES\n"
            f"**Source Documents:** {sources_summary}\n\n"
            + "\n\n---\n\n".join(all_pdf_blocks)
        )
        full_dossier = "\n\n---\n\n".join(dossier_parts)

        tok_est = len(full_dossier) // 4
        model = get_openrouter_model()
        model_name = get_model_display_name(model)
        self.set_phase_state(3, f"Running {model_name} (~{tok_est:,} tok)...", "active")
        self.live_banner_label.setText(
            f"💎 [Phase 4/5] Running Stage 2 Institutional Valuation with {model_name} (~{tok_est:,} tokens)..."
        )
        sens_log = f" + <b>{len(sens_docs)} SENS notice(s)</b> (<code>{sens_names_str}</code>)" if sens_docs else ""
        self.append_log(
            f"💎 <b>Phase 4 (Stage 2 Institutional Valuation):</b> Assembled full PDF + Stage 1 dossier "
            f"{sens_log} ({len(full_dossier):,} chars, ~{tok_est:,} tokens across {sources_summary}). "
            f"Submitting to <b>{model_name}</b>..."
        )

        self._s2_worker = OpenRouterWorker(
            full_dossier, model=model, parent=self, timeout=360, max_tokens=16384
        )

        def on_s2_done(resp_text: str, elapsed: float, stats: dict):
            if not self._is_running:
                return
            save_stage2_report(primary_sha, response=resp_text, db_path=self.db_path)
            s2_out_file = briefs_dir / f"{ticker}_{period}_stage2_valuation_note.md"
            s2_out_file.write_text(resp_text, encoding="utf-8")

            self.stage2_preview.setPlainText(resp_text)
            self.output_tabs.setCurrentIndex(2)

            tok = stats.get("total_tokens", 0)
            self.set_phase_state(3, f"✓ Valued in {elapsed:.1f}s ({tok:,} tok)", "done")
            self.append_log(
                f"✅ <b>Phase 4 Complete:</b> Stage 2 Valuation Note generated in {elapsed:.1f}s "
                f"({len(resp_text):,} chars, {tok:,} tokens). Saved to <code>{s2_out_file.name}</code>."
            )
            self.overall_progress.setValue(92)
            self._run_phase5_finalize(resp_text)

        def on_s2_err(err_msg: str):
            self._on_pipeline_error(f"Stage 2 Institutional Valuation failed: {err_msg}")

        self._s2_worker.finished_query.connect(on_s2_done)
        self._s2_worker.error_query.connect(on_s2_err)
        self._s2_worker.start()

    def _run_phase4_sens_only_update(self, sens_docs: list[dict[str, Any]], baseline_note: str):
        """Runs Stage 2-U SENS Event Update when baseline valuation already exists."""
        if not self._is_running or not self.current_company:
            return

        ticker = self.current_company["ticker"]
        company_title = self.current_company["company_title"]
        sector = self.current_company.get("sector", "retail")
        period = self.period_combo.currentText().strip() or "FY26"
        comp_dir = self._get_current_company_dir()
        briefs_dir = comp_dir / "briefs" / period
        briefs_dir.mkdir(parents=True, exist_ok=True)

        import pypdfium2 as pdfium

        sens_entries: list[dict[str, Any]] = []
        for sd in sens_docs:
            sf = Path(sd["path"])
            if not sf.exists():
                continue
            if sf.suffix.lower() in {".txt", ".text", ".md"}:
                sens_entries.append({
                    "filename": sf.name,
                    "announcement_date": sd.get("announcement_date") or "SENS",
                    "is_text": True,
                    "content": sf.read_text(encoding="utf-8").strip(),
                })
            elif sf.suffix.lower() == ".pdf":
                doc_s = pdfium.PdfDocument(str(sf))
                s_pages = [page.get_textpage().get_text_range().strip() for page in doc_s]
                doc_s.close()
                sens_entries.append({
                    "filename": sf.name,
                    "announcement_date": sd.get("announcement_date") or "SENS",
                    "is_text": True,
                    "content": "\n\n".join(s_pages),
                })

        ref_price = self._obtain_reference_price(ticker)
        if ref_price is None:
            self._on_pipeline_error(
                f"SENS Valuation Update aborted: A verified closing price is required for {ticker}. "
                f"Please provide the closing price to proceed."
            )
            return

        sens_prompt = build_sens_update_prompt_content(
            baseline_valuation_report=baseline_note,
            company_title=company_title,
            ticker=ticker,
            detected_sector=sector,
            sens_entries=sens_entries,
            reference_price_zar=ref_price,
        )
        sens_prompt_file = briefs_dir / f"{ticker}_{period}_stage2_sens_update_prompt.md"
        sens_prompt_file.write_text(sens_prompt, encoding="utf-8")

        tok_est = len(sens_prompt) // 4
        model = get_openrouter_model()
        model_name = get_model_display_name(model)
        self.set_phase_state(3, f"Running SENS Update (~{tok_est:,} tok)...", "active")
        self.live_banner_label.setText(
            f"📡 [Phase 4/5] Running SENS Valuation Update with {model_name} (~{tok_est:,} tokens)..."
        )
        self.append_log(
            f"📡 <b>Phase 4 (SENS Valuation Update):</b> Compiled SENS update dossier "
            f"({len(sens_prompt):,} chars). Submitting to <b>{model_name}</b>..."
        )

        self._s2_worker = OpenRouterWorker(
            sens_prompt, model=model, parent=self, timeout=300, max_tokens=16384
        )

        def on_sens_done(resp_text: str, elapsed: float, stats: dict):
            if not self._is_running:
                return
            # Preserve baseline before overwriting
            s2_out_file = briefs_dir / f"{ticker}_{period}_stage2_valuation_note.md"
            baseline_file = briefs_dir / f"{ticker}_{period}_stage2_valuation_note_baseline.md"
            if s2_out_file.exists() and not baseline_file.exists():
                shutil.copy2(s2_out_file, baseline_file)
            s2_out_file.write_text(resp_text, encoding="utf-8")

            primary_sha = self.current_company.get("sha256")
            if primary_sha:
                save_stage2_report(primary_sha, response=resp_text, db_path=self.db_path)

            self.stage2_preview.setPlainText(resp_text)
            self.output_tabs.setCurrentIndex(2)
            self.set_phase_state(3, f"✓ SENS Updated in {elapsed:.1f}s", "done")
            self.append_log(
                f"✅ <b>Phase 4 Complete:</b> SENS Valuation Update finished in {elapsed:.1f}s "
                f"({len(resp_text):,} chars)."
            )
            self.overall_progress.setValue(92)
            self._run_phase5_finalize(resp_text)

        def on_sens_err(err_msg: str):
            self._on_pipeline_error(f"SENS Valuation Update failed: {err_msg}")

        self._s2_worker.finished_query.connect(on_sens_done)
        self._s2_worker.error_query.connect(on_sens_err)
        self._s2_worker.start()

    # =========================================================================
    # PHASE 5: ARCHIVING & PORTFOLIO SYNC
    # =========================================================================
    def _run_phase5_finalize(self, final_valuation_text: str):
        if not self.current_company:
            return
        ticker = self.current_company["ticker"]
        period = self.period_combo.currentText().strip() or "FY26"
        comp_dir = self._get_current_company_dir()

        self.set_phase_state(4, "Archiving & syncing portfolio...", "active")

        moved_pdfs: list[Path] = []
        moved_sens: list[Path] = []
        try:
            moved_pdfs = archive_source_pdfs(comp_dir, period=period, db_path=self.db_path)
        except Exception:
            pass
        try:
            moved_sens = move_analyzed_sens_files(comp_dir)
        except Exception:
            pass

        if moved_pdfs:
            self.append_log(
                f"📦 Archived {len(moved_pdfs)} source PDF(s) to <code>sources/completed/{period}/</code>."
            )
        if moved_sens:
            self.append_log(
                f"📦 Archived {len(moved_sens)} SENS notice(s) to <code>sources/sens/completed/</code>."
            )

        # Parse executive valuation metrics
        summary = parse_valuation_summary(final_valuation_text) or {}
        rec = summary.get("recommendation") or "RATED"
        target_p = summary.get("target_price") or summary.get("target_price_zar")
        curr_p = summary.get("reference_price") or summary.get("reference_price_zar")
        upside = summary.get("upside_pct") or summary.get("implied_upside_pct")

        target_str = f"R{target_p:,.2f}" if isinstance(target_p, (int, float)) else "N/A"
        curr_str = f"R{curr_p:,.2f}" if isinstance(curr_p, (int, float)) else "N/A"
        upside_str = f"{upside:+.1f}%" if isinstance(upside, (int, float)) else ""

        self.set_phase_state(4, f"✓ {rec} · Target {target_str}", "done")
        self.overall_progress.setValue(100)
        self._set_running_ui(False)

        done_banner = (
            f"🎉 Complete! {ticker} ({period}) — Rating: {rec} | "
            f"Current: {curr_str} | 12m Target: {target_str} ({upside_str})"
        )
        self.live_banner_label.setText(done_banner)
        self.append_log("=" * 72)
        self.append_log(f"🎉 <b>AUTONOMOUS ANALYSIS COMPLETE: {ticker} ({period})</b>")
        self.append_log(
            f"🏆 <b>Rating:</b> {rec} &nbsp;|&nbsp; <b>Current Price:</b> {curr_str} "
            f"&nbsp;|&nbsp; <b>12m Target Price:</b> {target_str} ({upside_str})"
        )
        self.append_log("=" * 72)

        # Refresh company list to reflect updated status
        self.refresh_companies(select_ticker=ticker)

    def _on_pipeline_error(self, err_msg: str):
        self._set_running_ui(False)
        self.live_banner_label.setText(f"❌ Pipeline Error: {err_msg}")
        self.append_log(f"❌ <b>ERROR:</b> <span style='color:#f87171;'>{err_msg}</span>")
        for i, card in enumerate(self.phase_cards):
            if "⏳" in card.text():
                self.set_phase_state(i, "Failed", "error")
