"""Forensic Audit & Institutional Valuation Dialog (Stages 1 & 2).

Provides in-GUI compilation and copying of Stage 1 & Stage 2 prompts,
pasting and verification of Gemini 4 Argon responses, and persistence
directly into SQLite (reports table) and disk briefs.
"""

from __future__ import annotations

import os
from pathlib import Path
import sqlite3
import subprocess

from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from companies import SECTORS, find_company_dir
from companies.sectors import get_jse_sector_code, get_jse_sector_label, get_jse_sector_name, get_sector_badge_style, get_sector_short_label
from section_capture.db import (
    KNOWN_COMPANIES,
    connect_db,
    get_analyzed_stocks,
    get_stage1_report,
    get_stage2_report,
    resolve_db_path,
    resolve_project_path,
    save_stage1_report,
    save_stage2_report,
)
from section_capture.map_dialog import fit_dialog_to_screen
from section_capture.packages import PROJECT_ROOT, detect_sector_from_path
from section_capture.portfolio_view import PortfolioView
from workflow.export_stage1 import build_stage1_prompt_content
from workflow.generate_stage2 import build_stage2_prompt_content
from section_capture.openrouter import OpenRouterWorker, get_openrouter_api_key, get_openrouter_model


def open_folder_and_select(file_or_dir: Path | str):
    """Opens Windows Explorer with the target file highlighted, or opens the directory."""
    path = Path(file_or_dir).resolve()
    if path.is_file():
        try:
            if os.name == "nt":
                subprocess.Popen(["explorer", f"/select,{str(path)}"])
                return
        except Exception:
            pass
        folder = path.parent
    else:
        folder = path

    if folder.exists():
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))


class ReportSourceRef:
    """Lightweight source reference representing a selected report in the valuation dialog."""

    def __init__(self, sha256: str = "", path: str | Path | None = None, filename: str | None = None):
        self.sha256 = sha256 or ""
        self.path = Path(path).resolve() if path else None
        self.filename = filename or (self.path.name if self.path else "report.pdf")


def detect_ticker_and_sector(source_path: str | Path | None) -> tuple[str, str]:
    """Detects company ticker and sector from the PDF file path or directory structure."""
    if not source_path:
        return "COMPANY", "retail"
    p = Path(source_path).resolve()

    # Check path parts for /companies/<sector>/<ticker>/...
    parts = list(p.parts)
    for i, part in enumerate(parts):
        if part.lower() == "companies" and i + 2 < len(parts):
            cand_sec = parts[i + 1].lower()
            cand_ticker = parts[i + 2].upper()
            if cand_sec in SECTORS and not cand_ticker.startswith((".", "_")):
                return cand_ticker, cand_sec

    # Check if inside sources/
    for i, part in enumerate(parts):
        if part.lower() == "sources" and i >= 2:
            cand_ticker = parts[i - 1].upper()
            cand_sec = parts[i - 2].lower()
            if cand_sec in SECTORS:
                return cand_ticker, cand_sec

    # Check known companies in filename or path
    s = str(p).lower()
    for ticker, (name, sec) in KNOWN_COMPANIES.items():
        if ticker.lower() in s or name.lower() in s:
            return ticker, sec

    detected = detect_sector_from_path(source_path)
    # Check if filename matches known tickers
    for cand_sec in SECTORS:
        sec_dir = PROJECT_ROOT / "companies" / cand_sec
        if sec_dir.exists():
            for c in sec_dir.iterdir():
                if c.is_dir() and c.name.lower() in str(p).lower():
                    return c.name.upper(), cand_sec
    return "TARGET", detected


def discover_available_companies(db_path: Path | str | None = None) -> list[dict]:
    """Discovers all available companies from SQLite reports table and companies/ filesystem."""
    resolved_db = resolve_db_path(db_path)
    stocks = get_analyzed_stocks(resolved_db)
    items: list[dict] = []
    seen_tickers: set[str] = set()

    # 1. Primary reports from SQLite (ordered by Valued -> Audited -> Captured)
    for s in stocks:
        ticker = s["ticker"].upper()
        if ticker in {"COMPANY", "TARGET"}:
            continue
        seen_tickers.add(ticker)
        name = s["company_name"]
        sector = s["sector"].lower()
        sha = s["sha256"]

        # Resolve PDF path
        pdf_path = None
        if s.get("original_path"):
            cand = resolve_project_path(s["original_path"])
            if cand and cand.exists():
                pdf_path = cand
        if not pdf_path:
            comp_dir_info = find_company_dir(ticker, sector=sector)
            c_dir = comp_dir_info[1] if comp_dir_info else PROJECT_ROOT / f"companies/{sector}/{ticker}"
            if s.get("filename"):
                cand = c_dir / "sources" / s["filename"]
                if cand.exists():
                    pdf_path = cand
            if not pdf_path and (c_dir / "sources").exists():
                pdfs = [p for p in (c_dir / "sources").glob("*.pdf") if "sens" not in p.name.lower()]
                if pdfs:
                    pdf_path = pdfs[0]

        # Status string
        sens_count = s.get("sens_count", 0)
        sens_str = f" · {sens_count} SENS" if sens_count else ""
        if s.get("target_price_zar") is not None:
            rec = f" ({s['recommendation']})" if s.get("recommendation") else ""
            status = f"Valued · Target: R{s['target_price_zar']:,.2f}{rec}{sens_str}"
        elif s.get("has_stage1"):
            status = f"Audited ({s.get('section_count', 0)} sec){sens_str}"
        elif s.get("section_count", 0) > 0:
            status = f"Captured ({s['section_count']} sec){sens_str}"
        else:
            status = f"Registered{sens_str}"

        sec_display = "REIT" if sector == "reit" else sector.capitalize()
        display_text = f"{ticker} — {name} ({sec_display}) [{status}]"
        items.append({
            "ticker": ticker,
            "company_title": name,
            "sector": sector,
            "sha256": sha,
            "filename": s.get("filename") or (pdf_path.name if pdf_path else "report.pdf"),
            "pdf_path": pdf_path,
            "status": status,
            "display_text": display_text,
        })

    # 2. Additional scaffolded companies under companies/<sector>/<ticker>
    for sec in SECTORS:
        sec_dir = PROJECT_ROOT / "companies" / sec
        if sec_dir.exists():
            for comp_dir in sorted(sec_dir.iterdir()):
                if not comp_dir.is_dir() or comp_dir.name.startswith((".", "_")):
                    continue
                ticker = comp_dir.name.upper()
                if ticker in seen_tickers or ticker in {"COMPANY", "TARGET"}:
                    continue
                seen_tickers.add(ticker)
                default_title = f"{ticker} Properties" if sec == "reit" else (f"{ticker} Technologies" if sec == "it" else (f"{ticker} Group" if sec == "retail" else f"{ticker} Resources"))
                c_name = KNOWN_COMPANIES.get(ticker, (default_title, sec))[0]
                sources_dir = comp_dir / "sources"
                pdf_path = None
                if sources_dir.exists():
                    pdfs = [p for p in sources_dir.glob("*.pdf") if "sens" not in p.name.lower()]
                    if pdfs:
                        pdf_path = pdfs[0]
                status = "Scaffolded"
                sha = ""
                if pdf_path and resolved_db.exists():
                    with connect_db(resolved_db) as conn:
                        row = conn.execute(
                            "SELECT sha256 FROM reports WHERE original_path = ? OR filename = ? LIMIT 1",
                            (str(pdf_path), pdf_path.name),
                        ).fetchone()
                        if row:
                            sha = row["sha256"]
                            sec_cnt = conn.execute("SELECT COUNT(*) FROM sections WHERE report_sha256 = ?", (sha,)).fetchone()[0]
                            status = f"Captured ({sec_cnt} sec)" if sec_cnt > 0 else "Registered"
                sec_lbl = "REIT" if sec == "reit" else ("IT" if sec == "it" else sec.capitalize())
                display_text = f"{ticker} — {c_name} ({sec_lbl}) [{status}]"
                items.append({
                    "ticker": ticker,
                    "company_title": c_name,
                    "sector": sec,
                    "sha256": sha,
                    "filename": pdf_path.name if pdf_path else "report.pdf",
                    "pdf_path": pdf_path,
                    "status": status,
                    "display_text": display_text,
                })

    return items


class AuditValuationDialog(QDialog):
    """Two-stage workflow dialog for Cognitive Forensic Audit and Institutional Valuation."""

    def __init__(self, source=None, parent=None, db_path: str | Path | None = None, initial_tab: int = 0):
        super().__init__(parent)
        self.source = source
        self.db_path = resolve_db_path(db_path)
        self.period = "FY26"
        self._is_populating_combo = False

        # Discover available companies
        self.available_companies = discover_available_companies(self.db_path)

        # Determine initial selection
        initial_data = None
        if self.source:
            s_sha = getattr(self.source, "sha256", "")
            s_path = getattr(self.source, "path", None)
            init_ticker, init_sector = detect_ticker_and_sector(s_path)
            for comp in self.available_companies:
                if (s_sha and comp.get("sha256") == s_sha) or (comp.get("ticker") == init_ticker):
                    initial_data = comp
                    break
            if not initial_data:
                c_title = KNOWN_COMPANIES.get(init_ticker, (f"{init_ticker} Group" if init_sector == "retail" else f"{init_ticker} Resources", init_sector))[0]
                initial_data = {
                    "ticker": init_ticker,
                    "company_title": c_title,
                    "sector": init_sector,
                    "sha256": s_sha,
                    "filename": getattr(self.source, "filename", Path(s_path).name if s_path else "report.pdf"),
                    "pdf_path": Path(s_path) if s_path else None,
                    "status": "Loaded",
                    "display_text": f"{init_ticker} — {c_title} ({init_sector.capitalize()}) [Loaded]",
                }
                self.available_companies.insert(0, initial_data)
        elif self.available_companies:
            initial_data = self.available_companies[0]
        else:
            initial_data = {
                "ticker": "NONE",
                "company_title": "No Companies Available",
                "sector": "",
                "sha256": "",
                "filename": "",
                "pdf_path": None,
                "status": "No reports",
                "display_text": "No analyzed reports found in database",
            }
            self.available_companies.append(initial_data)

        self._apply_company_data(initial_data, reload_ui=False)

        fit_dialog_to_screen(self, target_w=1280, target_h=820, min_w=850, min_h=550)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 12, 14, 12)
        main_layout.setSpacing(8)

        # Header bar with Company / Ticker dropdown
        header = QHBoxLayout()
        header.setSpacing(8)

        combo_label = QLabel("<b>Company / Ticker:</b>")
        combo_label.setStyleSheet("font-size: 13px;")
        header.addWidget(combo_label)

        self.company_combo = QComboBox()
        self.company_combo.setMinimumWidth(340)
        self.company_combo.setStyleSheet("font-size: 12px; font-weight: bold; padding: 3px 6px;")
        self._populate_company_combo(initial_data)
        self.company_combo.currentIndexChanged.connect(self._on_company_combo_changed)
        header.addWidget(self.company_combo)

        self.sector_badge = QLabel()
        self._update_sector_badge()
        header.addWidget(self.sector_badge)

        self.load_canvas_btn = QPushButton("Open in Canvas")
        self.load_canvas_btn.setToolTip("Open this company's PDF report directly in the main viewer canvas.")
        self.load_canvas_btn.clicked.connect(self._load_selected_into_canvas)
        self.load_canvas_btn.setEnabled(bool(initial_data.get("pdf_path") and Path(initial_data["pdf_path"]).exists()))
        header.addWidget(self.load_canvas_btn)

        header.addStretch()

        self.report_info_label = QLabel()
        self.report_info_label.setStyleSheet("color: #666; font-size: 12px;")
        header.addWidget(self.report_info_label)
        main_layout.addLayout(header)

        # Tab widget
        self.tabs = QTabWidget()
        self.tab_stage1 = QWidget()
        self.tab_stage2 = QWidget()
        self.tab_portfolio = PortfolioView(db_path=self.db_path, parent=self)
        self._build_stage1_tab()
        self._build_stage2_tab()
        self.tabs.addTab(self.tab_stage1, "Stage 1: Cognitive Forensic Audit")
        self.tabs.addTab(self.tab_stage2, "Stage 2: Institutional Valuation Note")
        self.tabs.addTab(self.tab_portfolio, "Analyzed Stocks & Portfolio Coverage")
        self.tabs.currentChanged.connect(self._on_tab_changed)
        if initial_tab > 0:
            self.tabs.setCurrentIndex(initial_tab)
        main_layout.addWidget(self.tabs, 1)

        # Bottom close button
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        btn_box.rejected.connect(self.accept)
        main_layout.addWidget(btn_box)

        # Load existing data
        self._refresh_report_info()
        self._load_initial_data()

    def _populate_company_combo(self, selected_data: dict | None = None):
        self._is_populating_combo = True
        self.company_combo.clear()
        target_idx = 0
        for idx, comp in enumerate(self.available_companies):
            self.company_combo.addItem(comp["display_text"], comp)
            if selected_data and comp.get("ticker") == selected_data.get("ticker"):
                target_idx = idx
        self.company_combo.setCurrentIndex(target_idx)
        self._is_populating_combo = False

    def _on_company_combo_changed(self, index: int):
        if self._is_populating_combo or index < 0:
            return
        data = self.company_combo.itemData(index)
        if not data:
            return
        self._apply_company_data(data, reload_ui=True)

    def select_company_by_ticker(self, ticker: str) -> bool:
        """Programmatically switch to a company by ticker symbol."""
        t_up = ticker.strip().upper()
        for idx in range(self.company_combo.count()):
            data = self.company_combo.itemData(idx)
            if data and data.get("ticker", "").upper() == t_up:
                self.company_combo.setCurrentIndex(idx)
                return True
        return False

    def _apply_company_data(self, data: dict, reload_ui: bool = True):
        self.current_company_data = data
        self.ticker = data["ticker"]
        self.sector = data["sector"]
        self.company_title = data["company_title"]

        comp_info = find_company_dir(self.ticker, sector=self.sector)
        self.company_dir = comp_info[1] if comp_info else PROJECT_ROOT / f"companies/{self.sector}/{self.ticker}"
        prod_db = (PROJECT_ROOT / "documents/analysis.sqlite").resolve()
        is_isolated_test_db = self.db_path.resolve() != prod_db and self.db_path.resolve() != resolve_db_path(None)
        if is_isolated_test_db:
            self.briefs_dir = self.db_path.parent / "briefs" / self.period
        else:
            self.briefs_dir = self.company_dir / f"briefs/{self.period}"
        self.briefs_dir.mkdir(parents=True, exist_ok=True)

        self.setWindowTitle(f"Forensic Audit & Valuation Pipeline — {self.ticker} ({self.sector.capitalize()})")

        # Update source reference
        sha = data.get("sha256")
        pdf_path = data.get("pdf_path")
        if not sha and pdf_path and self.db_path.exists():
            with connect_db(self.db_path) as conn:
                row = conn.execute(
                    "SELECT sha256 FROM reports WHERE original_path = ? OR filename = ? LIMIT 1",
                    (str(pdf_path), Path(pdf_path).name),
                ).fetchone()
                if row:
                    sha = row["sha256"]
                    data["sha256"] = sha

        if sha:
            self.source = ReportSourceRef(
                sha256=sha,
                path=pdf_path,
                filename=data.get("filename"),
            )
        elif pdf_path:
            self.source = ReportSourceRef(
                sha256="",
                path=pdf_path,
                filename=Path(pdf_path).name,
            )
        else:
            self.source = None

        if hasattr(self, "sector_badge"):
            self._update_sector_badge()
        if hasattr(self, "load_canvas_btn"):
            has_pdf = bool(data.get("pdf_path") and Path(data["pdf_path"]).exists())
            self.load_canvas_btn.setEnabled(has_pdf)

        if reload_ui:
            self._refresh_report_info()
            self._load_initial_data()

    def _update_sector_badge(self):
        t = getattr(self, "ticker", None)
        self.sector_badge.setText(get_jse_sector_label(self.sector, ticker=t))
        self.sector_badge.setToolTip(f"FTSE/JSE ICB Sector: {get_jse_sector_name(self.sector, ticker=t)} ({get_jse_sector_code(self.sector, ticker=t)})")
        self.sector_badge.setStyleSheet(get_sector_badge_style(self.sector))

    def _load_selected_into_canvas(self):
        data = self.company_combo.currentData()
        if not data or not data.get("pdf_path"):
            QMessageBox.information(self, "No PDF Available", f"No PDF file is registered on disk for {self.ticker}.")
            return
        pdf_path = Path(data["pdf_path"])
        if not pdf_path.exists():
            QMessageBox.warning(self, "PDF Missing", f"PDF file not found on disk:\n{pdf_path}")
            return
        parent_win = self.parent()
        if parent_win and hasattr(parent_win, "open_pdf"):
            success = parent_win.open_pdf(pdf_path)
            if success:
                self.report_info_label.setText(f"✓ Active in canvas: <b>{pdf_path.name}</b>")

    def _on_tab_changed(self, index: int):
        if index == 2:
            self.available_companies = discover_available_companies(self.db_path)
            if hasattr(self, "company_combo"):
                self._populate_company_combo(self.current_company_data)
            self.tab_portfolio.refresh()

    def _refresh_report_info(self):
        if not self.source or not getattr(self.source, "sha256", ""):
            if self.source and getattr(self.source, "path", None):
                self.report_info_label.setText(f"File: <b>{self.source.filename}</b> (Not captured in SQLite yet)")
            else:
                self.report_info_label.setText("No report loaded in SQLite")
            return
        with connect_db(self.db_path) as conn:
            cur = conn.cursor()
            sec_count = cur.execute(
                "SELECT COUNT(*) FROM sections WHERE report_sha256 = ?", (self.source.sha256,)
            ).fetchone()[0]
            rep = cur.execute(
                "SELECT length(questions_ledger) FROM reports WHERE sha256 = ?", (self.source.sha256,)
            ).fetchone()
            ql_len = rep[0] if rep and rep[0] else 0
            comp_count = cur.execute(
                "SELECT COUNT(s.id) FROM reports r JOIN sections s ON s.report_sha256 = r.sha256 WHERE r.parent_report_sha256 = ? AND r.doc_type IN ('afs', 'presentation')",
                (self.source.sha256,)
            ).fetchone()[0]
            sens_count = cur.execute(
                "SELECT COUNT(*) FROM reports WHERE parent_report_sha256 = ? AND doc_type = 'sens'",
                (self.source.sha256,)
            ).fetchone()[0]
            total_sec = sec_count + comp_count
            comp_str = f" (+{comp_count} companion)" if comp_count else ""
            sens_str = f"  ·  Linked SENS: <b>{sens_count}</b>" if sens_count else ""
            self.report_info_label.setText(
                f"SQLite Sections: <b>{total_sec}</b>{comp_str}{sens_str}  ·  Questions Ledger: <b>{ql_len:,} chars</b>"
            )

    # =========================================================================
    # STAGE 1 TAB
    # =========================================================================
    def _build_stage1_tab(self):
        layout = QVBoxLayout(self.tab_stage1)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Instruction banner
        callout = QFrame()
        callout.setFrameShape(QFrame.Shape.StyledPanel)
        callout.setStyleSheet("background-color: #f4f6f8; border-radius: 4px; padding: 6px;")
        callout_layout = QVBoxLayout(callout)
        callout_layout.setContentsMargins(8, 6, 8, 6)
        c_title = QLabel("<b>Tier 2 Mandate (Gemini 4 Argon)</b>: Forensic reasoning & conflict reconciliation strictly over working papers.")
        c_desc = QLabel("<b>IMPORTANT:</b> Upload / drag the compiled prompt file into Gemini 4 Argon <b>WITHOUT attaching the PDF</b> "
                        "(working paper prompts are typically 200k–850k chars, which exceed web chat text box limits). "
                        "Click <b>'Open prompt folder'</b> to drag the file directly into chat. "
                        "Argon will audit credit book health, IFRS 9 ECL provisioning, margin bridges, and resolve contradictions.")
        c_desc.setWordWrap(True)
        callout_layout.addWidget(c_title)
        callout_layout.addWidget(c_desc)

        # Chat box instruction row (ready to copy and paste alongside the uploaded prompt file)
        chat_box_layout = QHBoxLayout()
        chat_box_layout.setContentsMargins(0, 4, 0, 0)
        chat_box_layout.setSpacing(6)
        chat_label = QLabel("<b>Chat instruction:</b>")
        chat_label.setStyleSheet("font-size: 11px; color: #334155;")
        self.s1_chat_edit = QLineEdit()
        self.s1_chat_edit.setStyleSheet(
            "background: white; border: 1px solid #cbd5e1; border-radius: 4px; padding: 3px 8px; font-size: 11px; color: #0f172a;"
        )
        self.s1_chat_edit.setText(
            f"Please execute the Stage 1 Forensic Audit for {self.company_title} ({self.ticker}) as detailed in the attached prompt file. Follow all instructions, verification rules, and output structures specified in the document."
        )
        self.s1_chat_edit.setToolTip("Instruction to paste into Gemini 4 Argon chat box when uploading the prompt file.")

        self.copy_s1_chat_btn = QPushButton("📋 Copy chat text")
        self.copy_s1_chat_btn.setStyleSheet(
            "font-size: 11px; font-weight: bold; padding: 3px 10px; background-color: #e2e8f0; border: 1px solid #cbd5e1; border-radius: 4px;"
        )
        self.copy_s1_chat_btn.setToolTip("Copy this instruction to clipboard to paste directly into Gemini chat box.")
        self.copy_s1_chat_btn.clicked.connect(self.copy_s1_chat_instruction)

        chat_box_layout.addWidget(chat_label)
        chat_box_layout.addWidget(self.s1_chat_edit, 1)
        chat_box_layout.addWidget(self.copy_s1_chat_btn)
        callout_layout.addLayout(chat_box_layout)

        layout.addWidget(callout)

        # Splitter: Left = Prompt preview, Right = Response editor
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel: Prompt
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(6)

        left_header = QHBoxLayout()
        left_title = QLabel("<b>Stage 1 Audit Prompt</b>")
        left_header.addWidget(left_title)
        left_header.addStretch()
        self.compile_s1_btn = QPushButton("Compile from SQLite")
        self.compile_s1_btn.clicked.connect(self.compile_stage1_prompt)
        left_header.addWidget(self.compile_s1_btn)
        self.open_s1_folder_btn = QPushButton("Open prompt folder")
        self.open_s1_folder_btn.setToolTip("Open Windows Explorer with the compiled prompt markdown file selected for dragging into Gemini chat.")
        self.open_s1_folder_btn.clicked.connect(self.open_stage1_folder)
        left_header.addWidget(self.open_s1_folder_btn)
        self.copy_s1_btn = QPushButton("Copy text")
        self.copy_s1_btn.setToolTip("Copy prompt text to clipboard (note: files > 100k chars should be uploaded directly into chat).")
        self.copy_s1_btn.clicked.connect(self.copy_stage1_prompt)
        left_header.addWidget(self.copy_s1_btn)
        self.run_s1_deepseek_btn = QPushButton("⚡ Run with DeepSeek")
        self.run_s1_deepseek_btn.setStyleSheet("font-weight: bold; background-color: #0e639c; color: white;")
        self.run_s1_deepseek_btn.setToolTip("Execute the Stage 1 Forensic Audit directly via OpenRouter (DeepSeek Flash) without manual copy-pasting.")
        self.run_s1_deepseek_btn.clicked.connect(self.run_stage1_deepseek)
        left_header.addWidget(self.run_s1_deepseek_btn)
        left_layout.addLayout(left_header)

        self.s1_prompt_edit = QPlainTextEdit()
        self.s1_prompt_edit.setReadOnly(True)
        self.s1_prompt_edit.setPlaceholderText("Click 'Compile from SQLite' to assemble the Stage 1 Forensic Audit Prompt from all captured sections.")
        left_layout.addWidget(self.s1_prompt_edit, 1)

        self.s1_prompt_status = QLabel("Prompt not compiled yet.")
        self.s1_prompt_status.setStyleSheet("color: #666; font-size: 11px;")
        left_layout.addWidget(self.s1_prompt_status)

        splitter.addWidget(left_widget)

        # Right panel: Response
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(6)

        right_header = QHBoxLayout()
        right_title = QLabel("<b>Stage 1 Audit Response (Argon)</b>")
        right_header.addWidget(right_title)
        right_header.addStretch()
        self.paste_s1_btn = QPushButton("Paste from clipboard")
        self.paste_s1_btn.clicked.connect(self.paste_stage1_response)
        right_header.addWidget(self.paste_s1_btn)
        self.load_s1_btn = QPushButton("Load from disk")
        self.load_s1_btn.clicked.connect(self.load_stage1_from_disk)
        right_header.addWidget(self.load_s1_btn)
        self.save_s1_btn = QPushButton("Save Response to DB")
        self.save_s1_btn.setStyleSheet("font-weight: bold;")
        self.save_s1_btn.clicked.connect(self.save_stage1_response)
        right_header.addWidget(self.save_s1_btn)
        right_layout.addLayout(right_header)

        self.s1_response_edit = QPlainTextEdit()
        self.s1_response_edit.setPlaceholderText(
            "Paste the complete Gemini 4 Argon Stage 1 Forensic Audit Report here.\n\n"
            "Once saved, Argon's verified accounting and credit determinations will be persisted in SQLite "
            "and automatically injected as the 99% ground truth prior into Stage 2."
        )
        right_layout.addWidget(self.s1_response_edit, 1)

        self.s1_response_status = QLabel("No Stage 1 response saved in SQLite.")
        self.s1_response_status.setStyleSheet("color: #666; font-size: 11px;")
        right_layout.addWidget(self.s1_response_status)

        splitter.addWidget(right_widget)
        splitter.setSizes([550, 650])
        layout.addWidget(splitter, 1)

    # =========================================================================
    # STAGE 2 TAB
    # =========================================================================
    def _build_stage2_tab(self):
        layout = QVBoxLayout(self.tab_stage2)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Rule banner
        callout = QFrame()
        callout.setFrameShape(QFrame.Shape.StyledPanel)
        callout.setStyleSheet("background-color: #fdf8e2; border-radius: 4px; padding: 6px;")
        callout_layout = QVBoxLayout(callout)
        callout_layout.setContentsMargins(8, 6, 8, 6)
        c_title = QLabel("<b>Tier 3 Mandate (Gemini 4 Argon)</b>: Institutional 2-Year Forecast, SOTP DCF, & JSE Valuation Note.")
        c_desc = QLabel("<b>CORE RULE:</b> Treat Stage 1 Determinations as a <b>99% confidence prior</b>. If Argon finds definitive evidence "
                        "in primary PDF financial notes that disagrees with Stage 1, it must explicitly declare the disagreement, cite the note/page, and explain reasons.\n"
                        "<b>INPUTS:</b> Upload or drag both the <b>source PDF report</b> and the <b>Stage 2 prompt file</b> into Gemini 4 Argon.")
        c_desc.setWordWrap(True)
        callout_layout.addWidget(c_title)
        callout_layout.addWidget(c_desc)

        # Chat box instruction row (ready to copy and paste alongside prompt file & PDF)
        chat_box_layout = QHBoxLayout()
        chat_box_layout.setContentsMargins(0, 4, 0, 0)
        chat_box_layout.setSpacing(6)
        chat_label = QLabel("<b>Chat instruction:</b>")
        chat_label.setStyleSheet("font-size: 11px; color: #713f12;")
        self.s2_chat_edit = QLineEdit()
        self.s2_chat_edit.setStyleSheet(
            "background: white; border: 1px solid #fde047; border-radius: 4px; padding: 3px 8px; font-size: 11px; color: #0f172a;"
        )
        self.s2_chat_edit.setText(
            f"Please execute the Stage 2 Institutional Valuation Note for {self.company_title} ({self.ticker}) as detailed in the attached prompt file and accompanying PDF report. Follow all valuation guidelines, forecast models, and output tables specified in the document."
        )
        self.s2_chat_edit.setToolTip("Instruction to paste into Gemini 4 Argon chat box when uploading prompt and PDF.")

        self.copy_s2_chat_btn = QPushButton("📋 Copy chat text")
        self.copy_s2_chat_btn.setStyleSheet(
            "font-size: 11px; font-weight: bold; padding: 3px 10px; background-color: #fef9c3; border: 1px solid #fde047; border-radius: 4px;"
        )
        self.copy_s2_chat_btn.setToolTip("Copy this instruction to clipboard to paste directly into Gemini chat box.")
        self.copy_s2_chat_btn.clicked.connect(self.copy_s2_chat_instruction)

        chat_box_layout.addWidget(chat_label)
        chat_box_layout.addWidget(self.s2_chat_edit, 1)
        chat_box_layout.addWidget(self.copy_s2_chat_btn)
        callout_layout.addLayout(chat_box_layout)

        layout.addWidget(callout)

        # Splitter: Left = Stage 2 Prompt, Right = Final Valuation Report
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel: Stage 2 Prompt
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(6)

        left_header = QVBoxLayout()
        left_header.setSpacing(4)

        row1 = QHBoxLayout()
        left_title = QLabel("<b>Stage 2 Valuation Prompt</b>")
        row1.addWidget(left_title)
        row1.addStretch()
        self.gen_s2_btn = QPushButton("Generate Stage 2 Prompt")
        self.gen_s2_btn.setToolTip("Full initial valuation prompt (Stage 1 ground truth + PDF report).")
        self.gen_s2_btn.clicked.connect(self.generate_stage2_prompt)
        row1.addWidget(self.gen_s2_btn)

        self.gen_sens_update_btn = QPushButton("⚡ Generate SENS Update Prompt")
        self.gen_sens_update_btn.setStyleSheet("font-weight: bold; color: #0f5132; background-color: #d1e7dd; border: 1px solid #badbcc; padding: 4px 8px;")
        self.gen_sens_update_btn.setToolTip("Fast update: Sends entire SENS PDF/text with baseline valuation note to re-rate target price & triggers (no capturing needed).")
        self.gen_sens_update_btn.clicked.connect(self.generate_sens_update_prompt_gui)
        row1.addWidget(self.gen_sens_update_btn)

        self.move_sens_btn = QPushButton("📦 Move SENS to Completed")
        self.move_sens_btn.setStyleSheet("font-weight: bold; color: #1e293b; background-color: #f1f5f9; border: 1px solid #cbd5e1; padding: 4px 8px;")
        self.move_sens_btn.setToolTip("Move analyzed SENS notice(s) from sources/sens/ into sources/sens/completed/.")
        self.move_sens_btn.clicked.connect(self.move_sens_to_completed_gui)
        row1.addWidget(self.move_sens_btn)
        left_header.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addStretch()
        self.open_s2_folder_btn = QPushButton("Open prompt folder")
        self.open_s2_folder_btn.setToolTip("Open folder with the prompt markdown file selected for dragging into chat.")
        self.open_s2_folder_btn.clicked.connect(self.open_stage2_folder)
        row2.addWidget(self.open_s2_folder_btn)
        self.open_pdf_btn = QPushButton("Open PDF folder")
        self.open_pdf_btn.setToolTip("Open Windows Explorer to the source PDF location for dragging into chat.")
        self.open_pdf_btn.clicked.connect(self.open_pdf_folder)
        row2.addWidget(self.open_pdf_btn)
        self.copy_s2_btn = QPushButton("Copy text")
        self.copy_s2_btn.setToolTip("Copy prompt text to clipboard.")
        self.copy_s2_btn.clicked.connect(self.copy_stage2_prompt)
        row2.addWidget(self.copy_s2_btn)
        self.run_s2_deepseek_btn = QPushButton("⚡ Run Valuation with DeepSeek")
        self.run_s2_deepseek_btn.setStyleSheet("font-weight: bold; background-color: #0e639c; color: white;")
        self.run_s2_deepseek_btn.setToolTip("Execute the Stage 2 Institutional Valuation directly via OpenRouter (DeepSeek Flash) with full PDF ingestion.")
        self.run_s2_deepseek_btn.clicked.connect(self.run_stage2_deepseek)
        row2.addWidget(self.run_s2_deepseek_btn)
        left_header.addLayout(row2)

        left_layout.addLayout(left_header)

        self.s2_prompt_edit = QPlainTextEdit()
        self.s2_prompt_edit.setReadOnly(True)
        self.s2_prompt_edit.setPlaceholderText(
            "Click 'Generate Stage 2 Prompt' for the full model prompt, or click '⚡ Generate SENS Update Prompt' "
            "to automatically combine your baseline valuation report with subsequent SENS notice(s) without capturing."
        )
        left_layout.addWidget(self.s2_prompt_edit, 1)

        self.s2_prompt_status = QLabel("Prompt not generated yet.")
        self.s2_prompt_status.setStyleSheet("color: #666; font-size: 11px;")
        left_layout.addWidget(self.s2_prompt_status)

        splitter.addWidget(left_widget)

        # Right panel: Final Valuation Report
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(6)

        right_header = QHBoxLayout()
        right_title = QLabel("<b>Final Valuation Report (Argon)</b>")
        right_header.addWidget(right_title)
        right_header.addStretch()
        self.paste_s2_btn = QPushButton("Paste from clipboard")
        self.paste_s2_btn.clicked.connect(self.paste_stage2_response)
        right_header.addWidget(self.paste_s2_btn)
        self.load_s2_btn = QPushButton("Load from disk")
        self.load_s2_btn.clicked.connect(self.load_stage2_from_disk)
        right_header.addWidget(self.load_s2_btn)
        self.save_s2_btn = QPushButton("Save Final Report to DB")
        self.save_s2_btn.setStyleSheet("font-weight: bold;")
        self.save_s2_btn.clicked.connect(self.save_stage2_response)
        right_header.addWidget(self.save_s2_btn)
        right_layout.addLayout(right_header)

        self.s2_response_edit = QPlainTextEdit()
        self.s2_response_edit.setPlaceholderText(
            "Paste the complete Gemini 4 Argon Stage 2 Institutional Valuation Report here.\n\n"
            "This contains the 2-year forecast model, consolidated statements, DCF multiples, and definitive ZAR target price."
        )
        right_layout.addWidget(self.s2_response_edit, 1)

        self.s2_response_status = QLabel("No final report saved in SQLite.")
        self.s2_response_status.setStyleSheet("color: #666; font-size: 11px;")
        right_layout.addWidget(self.s2_response_status)

        splitter.addWidget(right_widget)
        splitter.setSizes([550, 650])
        layout.addWidget(splitter, 1)

    # =========================================================================
    # DATA LOADING & INITIALIZATION
    # =========================================================================
    def _load_initial_data(self):
        # Reset text edits and status
        self.s1_prompt_edit.setPlainText("")
        self.s1_response_edit.setPlainText("")
        self.s1_prompt_status.setText("Prompt not compiled yet.")
        self.s1_response_status.setText("No Stage 1 response saved in SQLite.")

        self.s2_prompt_edit.setPlainText("")
        self.s2_response_edit.setPlainText("")
        self.s2_prompt_status.setText("Prompt not generated yet.")
        self.s2_response_status.setText("No final report saved in SQLite.")

        if hasattr(self, "s1_chat_edit"):
            self.s1_chat_edit.setText(
                f"Please execute the Stage 1 Forensic Audit for {self.company_title} ({self.ticker}) as detailed in the attached prompt file. Follow all instructions, verification rules, and output structures specified in the document."
            )
        if hasattr(self, "s2_chat_edit"):
            self.s2_chat_edit.setText(
                f"Please execute the Stage 2 Institutional Valuation Note for {self.company_title} ({self.ticker}) as detailed in the attached prompt file and accompanying PDF report. Follow all valuation guidelines, forecast models, and output tables specified in the document."
            )

        sha = getattr(self.source, "sha256", "") if self.source else ""

        # 1. Load Stage 1 from DB or disk
        s1_data = get_stage1_report(sha, db_path=self.db_path) if sha else {}
        s1_prompt = s1_data.get("stage1_prompt") or ""
        s1_response = s1_data.get("stage1_response") or ""

        # Check disk if not in DB
        s1_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage1_audit_response.md"
        if not s1_response and s1_file.exists():
            try:
                s1_response = s1_file.read_text(encoding="utf-8").strip()
            except Exception:
                pass

        s1_prompt_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage1_forensic_prompt.md"
        if not s1_prompt and s1_prompt_file.exists():
            try:
                s1_prompt = s1_prompt_file.read_text(encoding="utf-8").strip()
            except Exception:
                pass

        if s1_prompt:
            self.s1_prompt_edit.setPlainText(s1_prompt)
            self.s1_prompt_status.setText(f"Stage 1 prompt loaded ({len(s1_prompt):,} chars).")
        if s1_response:
            self.s1_response_edit.setPlainText(s1_response)
            updated_at = s1_data.get("stage1_updated_at") or "disk"
            self.s1_response_status.setText(f"✓ Stage 1 response recorded ({len(s1_response):,} chars) [Updated: {updated_at}].")

        # 2. Load Stage 2 from DB or disk
        s2_data = get_stage2_report(sha, db_path=self.db_path) if sha else {}
        s2_prompt = s2_data.get("stage2_prompt") or ""
        s2_response = s2_data.get("stage2_response") or ""

        s2_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage2_valuation_note.md"
        if not s2_response and s2_file.exists():
            try:
                s2_response = s2_file.read_text(encoding="utf-8").strip()
            except Exception:
                pass

        sens_prompt_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage2_sens_update_prompt.md"
        s2_prompt_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage2_valuation_prompt.md"
        if not s2_prompt:
            if sens_prompt_file.exists():
                try:
                    s2_prompt = sens_prompt_file.read_text(encoding="utf-8").strip()
                except Exception:
                    pass
            elif s2_prompt_file.exists():
                try:
                    s2_prompt = s2_prompt_file.read_text(encoding="utf-8").strip()
                except Exception:
                    pass

        if s2_prompt:
            self.s2_prompt_edit.setPlainText(s2_prompt)
            is_sens = "STAGE 2-U" in s2_prompt
            tag = "SENS Update prompt" if is_sens else "Stage 2 prompt"
            self.s2_prompt_status.setText(f"{tag} loaded ({len(s2_prompt):,} chars).")
        if s2_response:
            self.s2_response_edit.setPlainText(s2_response)
            updated_at = s2_data.get("stage2_updated_at") or "disk"
            self.s2_response_status.setText(f"✓ Final valuation report recorded ({len(s2_response):,} chars) [Updated: {updated_at}].")

    # =========================================================================
    # STAGE 1 ACTIONS
    # =========================================================================
    def compile_stage1_prompt(self):
        if not self.source or not getattr(self.source, "sha256", ""):
            # Attempt to resolve SHA from SQLite reports table using path, filename, or ticker
            if self.db_path.exists():
                with connect_db(self.db_path) as conn:
                    cur = conn.cursor()
                    row = None
                    if self.source and getattr(self.source, "path", None):
                        row = cur.execute(
                            "SELECT sha256, filename FROM reports WHERE original_path = ? OR filename = ? LIMIT 1",
                            (str(self.source.path), Path(self.source.path).name),
                        ).fetchone()
                    if not row and self.ticker:
                        row = cur.execute(
                            "SELECT sha256, filename FROM reports WHERE (original_path LIKE ? OR filename LIKE ?) AND parent_report_sha256 IS NULL ORDER BY updated_at DESC LIMIT 1",
                            (f"%{self.ticker}%", f"%{self.ticker}%"),
                        ).fetchone()
                        if not row:
                            row = cur.execute(
                                "SELECT sha256, filename FROM reports WHERE original_path LIKE ? OR filename LIKE ? ORDER BY updated_at DESC LIMIT 1",
                                (f"%{self.ticker}%", f"%{self.ticker}%"),
                            ).fetchone()
                    if row:
                        self.source = ReportSourceRef(
                            sha256=row["sha256"],
                            path=getattr(self.source, "path", None),
                            filename=row["filename"],
                        )

        if not self.source or not getattr(self.source, "sha256", ""):
            QMessageBox.warning(self, "No Sections Captured", f"No sections found in SQLite for {self.ticker} yet.")
            return

        with connect_db(self.db_path) as conn:
            cur = conn.cursor()
            # Resolve primary report SHA (if source is a SENS notice or companion AFS pointing to a parent Annual Report)
            rep_row = cur.execute("SELECT parent_report_sha256, filename, questions_ledger FROM reports WHERE sha256 = ?", (self.source.sha256,)).fetchone()
            final_questions_ledger = rep_row["questions_ledger"] if rep_row else None
            if rep_row and rep_row["parent_report_sha256"]:
                primary_sha = rep_row["parent_report_sha256"]
                p_row = cur.execute("SELECT filename, questions_ledger FROM reports WHERE sha256 = ?", (primary_sha,)).fetchone()
                filename = p_row["filename"] if p_row else getattr(self.source, "filename", Path(self.source.path).name if self.source.path else "report.pdf")
                if p_row and p_row["questions_ledger"]:
                    final_questions_ledger = p_row["questions_ledger"]
            else:
                primary_sha = self.source.sha256
                filename = getattr(self.source, "filename", Path(self.source.path).name if self.source.path else "report.pdf")

            sections = cur.execute(
                """
                SELECT section_number, section_id, heading, subheading, analyst_question,
                       selected_text, stored_questions_snapshot, llm_response
                FROM sections
                WHERE report_sha256 = ?
                ORDER BY section_number ASC, id ASC
                """,
                (primary_sha,),
            ).fetchall()

            # Query companion reports (AFS, Presentation) linked to primary report
            comp_rows = cur.execute(
                """
                SELECT sha256, filename, doc_type
                FROM reports
                WHERE parent_report_sha256 = ? AND doc_type IN ('afs', 'presentation')
                ORDER BY created_at ASC
                """,
                (primary_sha,),
            ).fetchall()

            companion_reports: list[dict] = []
            for cr in comp_rows:
                c_sections = cur.execute(
                    """
                    SELECT section_number, section_id, heading, subheading, analyst_question,
                           selected_text, stored_questions_snapshot, llm_response
                    FROM sections
                    WHERE report_sha256 = ?
                    ORDER BY section_number ASC, id ASC
                    """,
                    (cr["sha256"],),
                ).fetchall()
                if c_sections:
                    companion_reports.append({
                        "sha256": cr["sha256"],
                        "filename": cr["filename"],
                        "doc_type": cr["doc_type"],
                        "sections": c_sections,
                    })

            # Query linked SENS notices
            sens_rows = cur.execute(
                """
                SELECT sha256, filename, announcement_date
                FROM reports
                WHERE parent_report_sha256 = ? AND doc_type = 'sens'
                ORDER BY COALESCE(announcement_date, '9999-99-99') ASC, created_at ASC
                """,
                (primary_sha,),
            ).fetchall()

            sens_reports: list[dict] = []
            for sr in sens_rows:
                s_sections = cur.execute(
                    """
                    SELECT section_number, section_id, heading, subheading, analyst_question,
                           selected_text, stored_questions_snapshot, llm_response
                    FROM sections
                    WHERE report_sha256 = ?
                    ORDER BY section_number ASC, id ASC
                    """,
                    (sr["sha256"],),
                ).fetchall()
                if s_sections:
                    sens_reports.append({
                        "sha256": sr["sha256"],
                        "filename": sr["filename"],
                        "announcement_date": sr["announcement_date"],
                        "sections": s_sections,
                    })

            total_secs = len(sections) + sum(len(cr["sections"]) for cr in companion_reports) + sum(len(sr["sections"]) for sr in sens_reports)
            if total_secs == 0:
                QMessageBox.warning(self, "No Sections Captured", "No sections found in SQLite for this report yet.")
                return

            prompt_content = build_stage1_prompt_content(
                sections=sections,
                company_title=self.company_title,
                ticker=self.ticker,
                detected_sector=self.sector,
                filename=filename,
                companion_reports=companion_reports if companion_reports else None,
                sens_reports=sens_reports if sens_reports else None,
                final_questions_ledger=final_questions_ledger,
                compact=True,
            )

        self.s1_prompt_edit.setPlainText(prompt_content)
        comp_summary = f" (+ {len(companion_reports)} companion reports)" if companion_reports else ""
        sens_summary = f" (+ {len(sens_reports)} SENS announcements)" if sens_reports else ""
        self.s1_prompt_status.setText(f"✓ Compiled {total_secs} sections{comp_summary}{sens_summary} ({len(prompt_content):,} chars).")

        # Save to DB and disk
        save_stage1_report(primary_sha, prompt=prompt_content, db_path=self.db_path)
        out_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage1_forensic_prompt.md"
        out_file.write_text(prompt_content, encoding="utf-8")

    def open_stage1_folder(self):
        text = self.s1_prompt_edit.toPlainText().strip()
        out_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage1_forensic_prompt.md"
        if not text:
            self.compile_stage1_prompt()
            text = self.s1_prompt_edit.toPlainText().strip()

        if text and not out_file.exists():
            try:
                self.briefs_dir.mkdir(parents=True, exist_ok=True)
                out_file.write_text(text, encoding="utf-8")
            except Exception:
                pass

        if out_file.exists():
            open_folder_and_select(out_file)
            self.s1_prompt_status.setText(
                f"✓ Opened folder with {out_file.name} ({len(text):,} chars). Drag into chat, then paste the Chat instruction."
            )
        else:
            open_folder_and_select(self.briefs_dir)
            self.s1_prompt_status.setText(f"Opened briefs directory: {self.briefs_dir.name}")

    def copy_s1_chat_instruction(self):
        text = self.s1_chat_edit.text().strip()
        if text:
            QApplication.clipboard().setText(text)
            self.s1_prompt_status.setText("✓ Copied chat instruction to clipboard. Ready to paste into Gemini chat box alongside prompt file.")
            self.copy_s1_chat_btn.setText("✓ Copied!")
            QTimer.singleShot(2000, lambda: self.copy_s1_chat_btn.setText("📋 Copy chat text"))

    def copy_stage1_prompt(self):
        text = self.s1_prompt_edit.toPlainText().strip()
        if not text:
            self.compile_stage1_prompt()
            text = self.s1_prompt_edit.toPlainText().strip()
        if text:
            QApplication.clipboard().setText(text)
            if len(text) > 150000:
                self.s1_prompt_status.setText(
                    f"✓ Copied {len(text):,} chars to clipboard. (Notice: >150k chars is too large to paste directly in web chat; click 'Open prompt folder' to upload as a file instead)."
                )
            else:
                self.s1_prompt_status.setText(f"✓ Copied Stage 1 Prompt ({len(text):,} chars) to clipboard. Ready for Argon (no PDF).")

    def run_stage1_deepseek(self):
        """Executes the compiled Stage 1 Forensic Audit prompt directly with DeepSeek via OpenRouter."""
        prompt_text = self.s1_prompt_edit.toPlainText().strip()
        if not prompt_text:
            self.compile_stage1_prompt()
            prompt_text = self.s1_prompt_edit.toPlainText().strip()
        if not prompt_text:
            QMessageBox.warning(self, "No Prompt", "Could not compile Stage 1 prompt. Ensure sections are captured.")
            return

        api_key = get_openrouter_api_key()
        if not api_key:
            QMessageBox.critical(self, "Missing API Key", "OpenRouter API key not configured in secrets.env or environment.")
            return

        model = get_openrouter_model()
        self.run_s1_deepseek_btn.setEnabled(False)
        self.run_s1_deepseek_btn.setText("⏳ Running DeepSeek...")
        token_est = len(prompt_text) // 4
        self.s1_prompt_status.setText(f"⏳ Submitting {len(prompt_text):,} chars (~{token_est:,} tokens) to {model} via OpenRouter...")

        self._s1_worker = OpenRouterWorker(prompt_text, model=model, parent=self, timeout=300, max_tokens=16384)

        def on_finished(response_text, elapsed, stats):
            self.s1_response_edit.setPlainText(response_text)
            self.save_stage1_response(notify=False)
            cost_val = stats.get("cost_usd")
            cost_str = f", ${cost_val:.4f} USD" if cost_val is not None else ""
            tot_tok = stats.get("total_tokens", 0)
            status_msg = f"✓ DeepSeek Stage 1 audit complete in {elapsed:.1f}s ({tot_tok:,} tokens{cost_str}). Saved to DB & disk."
            self.s1_prompt_status.setText(status_msg)
            self.s1_response_status.setText(f"✓ DeepSeek completed in {elapsed:.1f}s ({len(response_text):,} chars). Saved.")
            self.run_s1_deepseek_btn.setEnabled(True)
            self.run_s1_deepseek_btn.setText("⚡ Run with DeepSeek")

        def on_error(err_msg):
            self.s1_prompt_status.setText(f"❌ DeepSeek Stage 1 audit failed: {err_msg}")
            QMessageBox.critical(self, "DeepSeek Query Failed", f"Failed to execute Stage 1 Forensic Audit:\n\n{err_msg}")
            self.run_s1_deepseek_btn.setEnabled(True)
            self.run_s1_deepseek_btn.setText("⚡ Run with DeepSeek")

        self._s1_worker.finished_query.connect(on_finished)
        self._s1_worker.error_query.connect(on_error)
        self._s1_worker.start()

    def paste_stage1_response(self):
        text = QApplication.clipboard().text().strip()
        if text:
            self.s1_response_edit.setPlainText(text)
            self.s1_response_status.setText(f"Pasted response ({len(text):,} chars). Click 'Save Response to DB' to commit.")

    def load_stage1_from_disk(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Stage 1 Audit Response Markdown", str(self.briefs_dir), "Markdown files (*.md *.txt);;All files (*)"
        )
        if path:
            text = Path(path).read_text(encoding="utf-8").strip()
            self.s1_response_edit.setPlainText(text)
            self.s1_response_status.setText(f"Loaded {len(text):,} chars from {Path(path).name}.")

    def save_stage1_response(self, notify: bool = True):
        text = self.s1_response_edit.toPlainText().strip()
        if not text:
            if notify:
                QMessageBox.warning(self, "Empty Response", "Please paste or enter the Stage 1 response before saving.")
            return

        # Save to SQLite if registered
        sha = getattr(self.source, "sha256", "") if self.source else ""
        if not sha and self.ticker:
            from workflow.export_stage1 import get_latest_report_sha
            with connect_db(self.db_path) as conn:
                pair = get_latest_report_sha(conn, self.ticker)
                if pair:
                    sha = pair[0]
        if sha:
            save_stage1_report(sha, response=text, db_path=self.db_path)

        # Save to disk
        out_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage1_audit_response.md"
        out_file.write_text(text, encoding="utf-8")

        self.s1_response_status.setText(
            f"✓ Saved Stage 1 Response ({len(text):,} chars) to SQLite and {out_file.name}."
        )
        if notify:
            QMessageBox.information(
                self,
                "Stage 1 Response Saved",
                f"Stage 1 Audit Response successfully saved to SQLite and disk!\n\n"
                f"Ground truth determinations are now ready for Stage 2 Institutional Valuation.",
            )

    # =========================================================================
    # STAGE 2 ACTIONS
    # =========================================================================
    def generate_stage2_prompt(self):
        primary_sha = self.source.sha256 if self.source else ""
        sens_announcements: list[str] = []
        if primary_sha:
            with connect_db(self.db_path) as conn:
                cur = conn.cursor()
                rep = cur.execute("SELECT parent_report_sha256 FROM reports WHERE sha256 = ?", (primary_sha,)).fetchone()
                if rep and rep["parent_report_sha256"]:
                    primary_sha = rep["parent_report_sha256"]
                for r in cur.execute("SELECT filename, announcement_date FROM reports WHERE parent_report_sha256 = ? ORDER BY COALESCE(announcement_date, '9999-99-99') ASC", (primary_sha,)).fetchall():
                    sens_announcements.append(f"`{r['filename']}` ({r['announcement_date'] or 'SENS'})")

        stage1_content = self.s1_response_edit.toPlainText().strip()
        if not stage1_content and primary_sha:
            # Check DB or disk
            s1_data = get_stage1_report(primary_sha, db_path=self.db_path) or {}
            stage1_content = (s1_data.get("stage1_response") or "").strip()

        if not stage1_content:
            s1_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage1_audit_response.md"
            if s1_file.exists():
                stage1_content = s1_file.read_text(encoding="utf-8").strip()

        if not stage1_content:
            reply = QMessageBox.question(
                self,
                "Stage 1 Response Missing",
                "No Stage 1 Audit Response was found. Would you like to generate the Stage 2 prompt with a placeholder for Stage 1 determinations?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
            stage1_content = "[PASTE STAGE 1 AUDIT DETERMINATIONS HERE]"

        prompt_content = build_stage2_prompt_content(
            stage1_content=stage1_content,
            company_title=self.company_title,
            ticker=self.ticker,
            detected_sector=self.sector,
            sens_announcements=sens_announcements if sens_announcements else None,
        )

        self.s2_prompt_edit.setPlainText(prompt_content)
        self.s2_prompt_status.setText(f"✓ Generated Stage 2 prompt ({len(prompt_content):,} chars) incorporating Stage 1 ground truth.")

        # Save to DB and disk
        if primary_sha:
            save_stage2_report(primary_sha, prompt=prompt_content, db_path=self.db_path)
        out_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage2_valuation_prompt.md"
        out_file.write_text(prompt_content, encoding="utf-8")

        if hasattr(self, "s2_chat_edit"):
            self.s2_chat_edit.setText(
                f"Please execute the Stage 2 Institutional Valuation Note for {self.company_title} ({self.ticker}) as detailed in the attached prompt file and accompanying PDF report. Follow all valuation guidelines, forecast models, and output tables specified in the document."
            )

    def generate_sens_update_prompt_gui(self):
        """Generates the token-efficient SENS Valuation Update prompt directly from baseline valuation note + entire SENS PDF/text."""
        from workflow.generate_sens_update import generate_sens_update_prompt

        try:
            out_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage2_sens_update_prompt.md"
            generate_sens_update_prompt(
                ticker=self.ticker,
                company_name=self.company_title,
                sector=self.sector,
                period=self.period,
                output_path=out_file,
                db_path=self.db_path,
            )
            content = out_file.read_text(encoding="utf-8")
            self.s2_prompt_edit.setPlainText(content)

            has_embedded_txt = "## 2. SUBSEQUENT SENS CONTINUOUS DISCLOSURE EVIDENCE" in content
            if has_embedded_txt:
                self.s2_prompt_status.setText(
                    f"✓ SENS Update Prompt ready ({len(content):,} chars; SENS text notices embedded). Upload prompt to Gemini 4 Argon."
                )
                if hasattr(self, "s2_chat_edit"):
                    self.s2_chat_edit.setText(
                        f"Please execute the Stage 2-U SENS Valuation Update for {self.company_title} ({self.ticker}) as detailed in the attached prompt file. Re-rate target price, recommendations, and monitoring triggers against the baseline report."
                    )
            else:
                self.s2_prompt_status.setText(
                    f"✓ SENS Update Prompt ready ({len(content):,} chars). Upload to Gemini 4 Argon to re-rate target price & triggers."
                )
                if hasattr(self, "s2_chat_edit"):
                    self.s2_chat_edit.setText(
                        f"Please execute the Stage 2-U SENS Valuation Update for {self.company_title} ({self.ticker}) as detailed in the attached prompt file and accompanying SENS PDF. Re-rate target price, recommendations, and monitoring triggers against the baseline report."
                    )
        except Exception as exc:
            QMessageBox.warning(self, "SENS Update Notice", str(exc))

    def move_sens_to_completed_gui(self):
        """Manually moves analyzed SENS notices into completed/ directory."""
        from workflow.generate_sens_update import get_sens_completed_dir, move_analyzed_sens_files

        try:
            moved = move_analyzed_sens_files(self.company_dir)
            if moved:
                comp_dir = get_sens_completed_dir(self.company_dir)
                self.s2_prompt_status.setText(
                    f"✓ Moved {len(moved)} SENS notice(s) to {comp_dir.parent.name}/{comp_dir.name}/."
                )
                QMessageBox.information(
                    self,
                    "SENS Archived",
                    f"Successfully moved {len(moved)} analyzed SENS notice(s) to:\n{comp_dir}\n\n"
                    f"Pending sources/sens folder is now clear for future announcements.",
                )
            else:
                sens_dir = self.company_dir / "sources/sens"
                QMessageBox.information(
                    self,
                    "No Pending SENS",
                    f"No pending SENS notices found in:\n{sens_dir}\n\n(All notices may already be in the completed folder).",
                )
        except Exception as exc:
            QMessageBox.warning(self, "Archive Error", str(exc))

    def open_stage2_folder(self):
        text = self.s2_prompt_edit.toPlainText().strip()
        sens_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage2_sens_update_prompt.md"
        normal_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage2_valuation_prompt.md"

        target_file = sens_file if (sens_file.exists() and "STAGE 2-U" in text) else normal_file
        if not text and not target_file.exists():
            self.generate_stage2_prompt()
            text = self.s2_prompt_edit.toPlainText().strip()

        if text and not target_file.exists():
            try:
                self.briefs_dir.mkdir(parents=True, exist_ok=True)
                target_file.write_text(text, encoding="utf-8")
            except Exception:
                pass

        if target_file.exists():
            open_folder_and_select(target_file)
            self.s2_prompt_status.setText(
                f"✓ Opened folder with {target_file.name} ({len(text):,} chars). Upload into Gemini 4 Argon, then paste the Chat instruction."
            )
        else:
            open_folder_and_select(self.briefs_dir)
            self.s2_prompt_status.setText(f"Opened briefs directory: {self.briefs_dir.name}")

    def copy_s2_chat_instruction(self):
        text = self.s2_chat_edit.text().strip()
        if text:
            QApplication.clipboard().setText(text)
            self.s2_prompt_status.setText("✓ Copied chat instruction to clipboard. Ready to paste into Gemini chat box alongside prompt file & PDF.")
            self.copy_s2_chat_btn.setText("✓ Copied!")
            QTimer.singleShot(2000, lambda: self.copy_s2_chat_btn.setText("📋 Copy chat text"))

    def copy_stage2_prompt(self):
        text = self.s2_prompt_edit.toPlainText().strip()
        if not text:
            self.generate_stage2_prompt()
            text = self.s2_prompt_edit.toPlainText().strip()
        if text:
            QApplication.clipboard().setText(text)
            self.s2_prompt_status.setText(f"✓ Copied Stage 2 Prompt ({len(text):,} chars) to clipboard. Remember to attach the PDF!")

    def open_pdf_folder(self):
        if self.source and self.source.path:
            pdf_path = Path(self.source.path).resolve()
            if pdf_path.exists():
                open_folder_and_select(pdf_path)
                return
        # Fallback to company sources dir
        sources_dir = self.company_dir / "sources"
        if sources_dir.exists():
            open_folder_and_select(sources_dir)

    def paste_stage2_response(self):
        text = QApplication.clipboard().text().strip()
        if text:
            self.s2_response_edit.setPlainText(text)
            self.s2_response_status.setText(f"Pasted final report ({len(text):,} chars). Click 'Save Final Report to DB' to commit.")

    def load_stage2_from_disk(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Final Valuation Report Markdown", str(self.briefs_dir), "Markdown files (*.md *.txt);;All files (*)"
        )
        if path:
            text = Path(path).read_text(encoding="utf-8").strip()
            self.s2_response_edit.setPlainText(text)
            self.s2_response_status.setText(f"Loaded {len(text):,} chars from {Path(path).name}.")

    def run_stage2_deepseek(self):
        """Executes Stage 2 Institutional Valuation directly with DeepSeek Flash, ingesting the full PDF report."""
        base_prompt = self.s2_prompt_edit.toPlainText().strip()
        if not base_prompt:
            self.generate_stage2_prompt()
            base_prompt = self.s2_prompt_edit.toPlainText().strip()
        if not base_prompt:
            QMessageBox.warning(self, "No Prompt", "Could not generate Stage 2 prompt. Ensure Stage 1 determinations are saved.")
            return

        api_key = get_openrouter_api_key()
        if not api_key:
            QMessageBox.critical(self, "Missing API Key", "OpenRouter API key not configured in secrets.env or environment.")
            return

        # Find primary source PDF
        sources_dir = self.company_dir / "sources"
        pdf_files = sorted(sources_dir.glob("*.pdf")) if sources_dir.exists() else []
        if not pdf_files:
            QMessageBox.warning(self, "PDF Not Found", f"No source PDF found in {sources_dir}.")
            return

        # Fast page-by-page text extraction via pypdfium2 across all available source PDFs
        self.run_s2_deepseek_btn.setEnabled(False)
        self.run_s2_deepseek_btn.setText("⏳ Ingesting PDFs...")
        pdf_names = ", ".join(f.name for f in pdf_files)
        self.s2_prompt_status.setText(f"⏳ Ingesting {len(pdf_files)} PDF(s): {pdf_names}...")
        QApplication.processEvents()

        all_pdf_sections = []
        try:
            import pypdfium2 as pdfium
            for pdf_path in pdf_files:
                doc = pdfium.PdfDocument(str(pdf_path))
                pages_text = []
                for i, page in enumerate(doc):
                    t_range = page.get_textpage().get_text_range().strip()
                    pages_text.append(f"--- [{pdf_path.name} | Page {i+1} of {len(doc)}] ---\n{t_range}")
                all_pdf_sections.append(
                    f"## SOURCE DISCLOSURE FILE: {pdf_path.name} ({len(doc)} Pages)\n\n"
                    + "\n\n".join(pages_text)
                )
            pdf_extracted_text = "\n\n---\n\n".join(all_pdf_sections)
        except Exception as exc:
            QMessageBox.critical(self, "PDF Extraction Failed", f"Could not extract text from source PDFs:\n\n{exc}")
            self.run_s2_deepseek_btn.setEnabled(True)
            self.run_s2_deepseek_btn.setText("⚡ Run Valuation with DeepSeek")
            return

        # Load SENS notices if present
        sens_dir = sources_dir / "sens"
        sens_notices = []
        if sens_dir.exists():
            candidate_files = []
            if (sens_dir / "completed").exists():
                candidate_files.extend(sorted((sens_dir / "completed").glob("*.txt")))
            candidate_files.extend(sorted(f for f in sens_dir.glob("*.txt") if f.is_file()))
            for f in candidate_files:
                try:
                    sens_notices.append(f"### SENS ANNOUNCEMENT: {f.name}\n\n{f.read_text(encoding='utf-8').strip()}")
                except Exception:
                    pass

        # Assemble unified prompt package
        prompt_sections = [base_prompt]
        if sens_notices:
            prompt_sections.append(
                "# SUBSEQUENT SENS ANNOUNCEMENTS & POST-BALANCE SHEET EVENTS\n\n"
                + "\n\n---\n\n".join(sens_notices)
            )
        prompt_sections.append(
            f"# COMPLETE PRIMARY SOURCE FINANCIAL REPORT DISCLOSURES & AUDITED NOTES\n"
            f"**Source Documents:** {pdf_names}\n\n"
            + pdf_extracted_text
        )
        full_dossier = "\n\n---\n\n".join(prompt_sections)

        model = get_openrouter_model()
        token_est = len(full_dossier) // 4
        self.run_s2_deepseek_btn.setText("⏳ Running DeepSeek...")
        self.s2_prompt_status.setText(f"⏳ Submitting {len(full_dossier):,} chars (~{token_est:,} tokens) to {model} via OpenRouter...")

        self._s2_worker = OpenRouterWorker(full_dossier, model=model, parent=self, timeout=360, max_tokens=16384)

        def on_finished(response_text, elapsed, stats):
            self.s2_response_edit.setPlainText(response_text)
            self.save_stage2_response(notify=False)
            cost_val = stats.get("cost_usd")
            cost_str = f", ${cost_val:.4f} USD" if cost_val is not None else ""
            tot_tok = stats.get("total_tokens", 0)
            status_msg = f"✓ DeepSeek Stage 2 valuation complete in {elapsed:.1f}s ({tot_tok:,} tokens{cost_str}). Saved to DB & disk."
            self.s2_prompt_status.setText(status_msg)
            self.s2_response_status.setText(f"✓ DeepSeek completed in {elapsed:.1f}s ({len(response_text):,} chars). Metrics saved.")
            self.run_s2_deepseek_btn.setEnabled(True)
            self.run_s2_deepseek_btn.setText("⚡ Run Valuation with DeepSeek")

        def on_error(err_msg):
            self.s2_prompt_status.setText(f"❌ DeepSeek Stage 2 valuation failed: {err_msg}")
            QMessageBox.critical(self, "DeepSeek Query Failed", f"Failed to execute Stage 2 Valuation:\n\n{err_msg}")
            self.run_s2_deepseek_btn.setEnabled(True)
            self.run_s2_deepseek_btn.setText("⚡ Run Valuation with DeepSeek")

        self._s2_worker.finished_query.connect(on_finished)
        self._s2_worker.error_query.connect(on_error)
        self._s2_worker.start()

    def save_stage2_response(self, notify: bool = True):
        text = self.s2_response_edit.toPlainText().strip()
        if not text:
            if notify:
                QMessageBox.warning(self, "Empty Report", "Please paste or enter the Stage 2 Valuation Report before saving.")
            return

        # Resolve primary report SHA (if source is a SENS notice)
        primary_sha = getattr(self.source, "sha256", "") if self.source else ""
        if not primary_sha and self.ticker:
            from workflow.export_stage1 import get_latest_report_sha
            with connect_db(self.db_path) as conn:
                pair = get_latest_report_sha(conn, self.ticker)
                if pair:
                    primary_sha = pair[0]
        if primary_sha:
            with connect_db(self.db_path) as conn:
                rep = conn.execute("SELECT parent_report_sha256 FROM reports WHERE sha256 = ?", (primary_sha,)).fetchone()
                if rep and rep["parent_report_sha256"]:
                    primary_sha = rep["parent_report_sha256"]

        # Check if SENS updates are linked
        sens_dates = []
        if primary_sha:
            with connect_db(self.db_path) as conn:
                rows = conn.execute(
                    "SELECT filename, announcement_date FROM reports WHERE parent_report_sha256 = ? ORDER BY announcement_date ASC",
                    (primary_sha,),
                ).fetchall()
                for r in rows:
                    if r["announcement_date"]:
                        sens_dates.append(r["announcement_date"])

        # Save to SQLite
        if primary_sha:
            save_stage2_report(primary_sha, response=text, db_path=self.db_path)

        # Save to disk: ensure baseline is preserved first
        out_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage2_valuation_note.md"
        baseline_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage2_valuation_note_baseline.md"
        if out_file.exists() and not baseline_file.exists():
            import shutil
            shutil.copy2(out_file, baseline_file)

        out_file.write_text(text, encoding="utf-8")

        # If post-SENS update, also write dated copy and auto-archive analyzed SENS files
        if sens_dates:
            dated_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage2_valuation_note_post_sens_{sens_dates[-1].replace('-', '')}.md"
            dated_file.write_text(text, encoding="utf-8")

        # Auto-archive analyzed SENS notices if this was a SENS update
        s2_prompt_text = self.s2_prompt_edit.toPlainText()
        moved_sens: list[Path] = []
        if "STAGE 2-U" in s2_prompt_text or sens_dates:
            from workflow.generate_sens_update import move_analyzed_sens_files
            try:
                moved_sens = move_analyzed_sens_files(self.company_dir)
            except Exception:
                pass

        moved_msg = f" (Moved {len(moved_sens)} SENS notice(s) to completed/)" if moved_sens else ""
        sens_msg = f" + SENS ({', '.join(sens_dates)})" if sens_dates else ""
        self.s2_response_status.setText(
            f"✓ Saved Final Valuation Report{sens_msg}{moved_msg} ({len(text):,} chars) to SQLite and {out_file.name}."
        )
        self.available_companies = discover_available_companies(self.db_path)
        if hasattr(self, "company_combo"):
            self._populate_company_combo(self.current_company_data)
        self.tab_portfolio.refresh()
        if notify:
            QMessageBox.information(
                self,
                "Valuation Report Saved",
                f"Valuation Report{sens_msg} successfully saved to SQLite and disk!\n\n"
                f"Metrics and Monitoring Triggers are updated in your Portfolio Coverage Dashboard.",
            )
