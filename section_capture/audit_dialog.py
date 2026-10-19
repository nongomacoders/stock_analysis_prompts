"""Forensic Audit & Institutional Valuation Dialog (Stages 1 & 2).

Provides in-GUI compilation and copying of Stage 1 & Stage 2 prompts,
pasting and verification of Gemini 4 Argon responses, and persistence
directly into SQLite (reports table) and disk briefs.
"""

from __future__ import annotations

import os
from pathlib import Path
import sqlite3

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from companies import find_company_dir
from section_capture.db import (
    connect_db,
    get_stage1_report,
    get_stage2_report,
    resolve_db_path,
    save_stage1_report,
    save_stage2_report,
)
from section_capture.map_dialog import fit_dialog_to_screen
from section_capture.packages import PROJECT_ROOT, detect_sector_from_path
from workflow.export_stage1 import build_stage1_prompt_content
from workflow.generate_stage2 import build_stage2_prompt_content


def detect_ticker_and_sector(source_path: str | Path | None) -> tuple[str, str]:
    """Detects company ticker and sector from the PDF file path or directory structure."""
    if not source_path:
        return "COMPANY", "retail"
    p = Path(source_path).resolve()
    if p.parent.name.lower() == "sources":
        ticker = p.parent.parent.name.upper()
        sector = p.parent.parent.parent.name.lower()
        if sector in {"mining", "retail", "finance", "telcos"}:
            return ticker, sector

    detected = detect_sector_from_path(source_path)
    # Check if filename or path matches known tickers
    for cand_sec in ["mining", "retail", "finance", "telcos"]:
        sec_dir = PROJECT_ROOT / "companies" / cand_sec
        if sec_dir.exists():
            for c in sec_dir.iterdir():
                if c.is_dir() and c.name.lower() in str(p).lower():
                    return c.name.upper(), cand_sec
    return "TARGET", detected


class AuditValuationDialog(QDialog):
    """Two-stage workflow dialog for Cognitive Forensic Audit and Institutional Valuation."""

    def __init__(self, source, parent=None, db_path: str | Path | None = None):
        super().__init__(parent)
        self.source = source
        self.db_path = resolve_db_path(db_path)
        self.ticker, self.sector = detect_ticker_and_sector(self.source.path if self.source else None)
        self.company_title = f"{self.ticker} Group" if self.sector == "retail" else f"{self.ticker} Resources"
        self.period = "FY26"

        comp_info = find_company_dir(self.ticker, sector=self.sector)
        self.company_dir = comp_info[1] if comp_info else PROJECT_ROOT / f"companies/{self.sector}/{self.ticker}"
        self.briefs_dir = self.company_dir / f"briefs/{self.period}"
        self.briefs_dir.mkdir(parents=True, exist_ok=True)

        self.setWindowTitle(f"Forensic Audit & Valuation Pipeline — {self.ticker} ({self.sector.capitalize()})")
        fit_dialog_to_screen(self, target_w=1280, target_h=820, min_w=850, min_h=550)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 12, 14, 12)
        main_layout.setSpacing(8)

        # Header bar
        header = QHBoxLayout()
        title_label = QLabel(f"<b>{self.company_title} ({self.ticker})</b> · Sector: <i>{self.sector.capitalize()}</i>")
        title_label.setStyleSheet("font-size: 14px;")
        header.addWidget(title_label)
        header.addStretch()
        self.report_info_label = QLabel()
        self.report_info_label.setStyleSheet("color: #666; font-size: 12px;")
        header.addWidget(self.report_info_label)
        main_layout.addLayout(header)

        # Tab widget
        self.tabs = QTabWidget()
        self.tab_stage1 = QWidget()
        self.tab_stage2 = QWidget()
        self._build_stage1_tab()
        self._build_stage2_tab()
        self.tabs.addTab(self.tab_stage1, "Stage 1: Cognitive Forensic Audit")
        self.tabs.addTab(self.tab_stage2, "Stage 2: Institutional Valuation Note")
        main_layout.addWidget(self.tabs, 1)

        # Bottom close button
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        btn_box.rejected.connect(self.accept)
        main_layout.addWidget(btn_box)

        # Load existing data
        self._refresh_report_info()
        self._load_initial_data()

    def _refresh_report_info(self):
        if not self.source:
            self.report_info_label.setText("No report loaded")
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
            self.report_info_label.setText(
                f"SQLite Sections: <b>{sec_count}</b>  ·  Questions Ledger: <b>{ql_len:,} chars</b>"
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
        c_desc = QLabel("<b>IMPORTANT:</b> Paste the compiled prompt into Gemini 4 Argon <b>WITHOUT attaching the PDF</b>. "
                        "Argon will audit credit book health, IFRS 9 ECL provisioning, margin bridges, and resolve contradictions.")
        c_desc.setWordWrap(True)
        callout_layout.addWidget(c_title)
        callout_layout.addWidget(c_desc)
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
        self.copy_s1_btn = QPushButton("Copy prompt")
        self.copy_s1_btn.clicked.connect(self.copy_stage1_prompt)
        left_header.addWidget(self.copy_s1_btn)
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
                        "<b>INPUTS:</b> Attach the <b>source PDF report alongside the prompt</b> in Gemini 4 Argon.")
        c_desc.setWordWrap(True)
        callout_layout.addWidget(c_title)
        callout_layout.addWidget(c_desc)
        layout.addWidget(callout)

        # Splitter: Left = Stage 2 Prompt, Right = Final Valuation Report
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel: Stage 2 Prompt
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(6)

        left_header = QHBoxLayout()
        left_title = QLabel("<b>Stage 2 Valuation Prompt</b>")
        left_header.addWidget(left_title)
        left_header.addStretch()
        self.gen_s2_btn = QPushButton("Generate Stage 2 Prompt")
        self.gen_s2_btn.clicked.connect(self.generate_stage2_prompt)
        left_header.addWidget(self.gen_s2_btn)
        self.copy_s2_btn = QPushButton("Copy prompt")
        self.copy_s2_btn.clicked.connect(self.copy_stage2_prompt)
        left_header.addWidget(self.copy_s2_btn)
        self.open_pdf_btn = QPushButton("Open PDF folder")
        self.open_pdf_btn.setToolTip("Open Windows Explorer to the source PDF location for dragging into chat.")
        self.open_pdf_btn.clicked.connect(self.open_pdf_folder)
        left_header.addWidget(self.open_pdf_btn)
        left_layout.addLayout(left_header)

        self.s2_prompt_edit = QPlainTextEdit()
        self.s2_prompt_edit.setReadOnly(True)
        self.s2_prompt_edit.setPlaceholderText("Click 'Generate Stage 2 Prompt' to inject Stage 1 audit determinations into the valuation template.")
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
        if not self.source:
            return

        # 1. Load Stage 1 from DB or disk
        s1_data = get_stage1_report(self.source.sha256, db_path=self.db_path) or {}
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
        s2_data = get_stage2_report(self.source.sha256, db_path=self.db_path) or {}
        s2_prompt = s2_data.get("stage2_prompt") or ""
        s2_response = s2_data.get("stage2_response") or ""

        s2_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage2_valuation_note.md"
        if not s2_response and s2_file.exists():
            try:
                s2_response = s2_file.read_text(encoding="utf-8").strip()
            except Exception:
                pass

        s2_prompt_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage2_valuation_prompt.md"
        if not s2_prompt and s2_prompt_file.exists():
            try:
                s2_prompt = s2_prompt_file.read_text(encoding="utf-8").strip()
            except Exception:
                pass

        if s2_prompt:
            self.s2_prompt_edit.setPlainText(s2_prompt)
            self.s2_prompt_status.setText(f"Stage 2 prompt loaded ({len(s2_prompt):,} chars).")
        if s2_response:
            self.s2_response_edit.setPlainText(s2_response)
            updated_at = s2_data.get("stage2_updated_at") or "disk"
            self.s2_response_status.setText(f"✓ Final valuation report recorded ({len(s2_response):,} chars) [Updated: {updated_at}].")

    # =========================================================================
    # STAGE 1 ACTIONS
    # =========================================================================
    def compile_stage1_prompt(self):
        if not self.source:
            return
        with connect_db(self.db_path) as conn:
            cur = conn.cursor()
            sections = cur.execute(
                """
                SELECT section_number, section_id, heading, subheading, analyst_question,
                       selected_text, stored_questions_snapshot, llm_response
                FROM sections
                WHERE report_sha256 = ?
                ORDER BY section_number ASC, id ASC
                """,
                (self.source.sha256,),
            ).fetchall()

            if not sections:
                QMessageBox.warning(self, "No Sections Captured", "No sections found in SQLite for this report yet.")
                return

            filename = getattr(self.source, "filename", Path(self.source.path).name if self.source.path else "report.pdf")
            prompt_content = build_stage1_prompt_content(
                sections=sections,
                company_title=self.company_title,
                ticker=self.ticker,
                detected_sector=self.sector,
                filename=filename,
            )

        self.s1_prompt_edit.setPlainText(prompt_content)
        self.s1_prompt_status.setText(f"✓ Compiled {len(sections)} sections ({len(prompt_content):,} chars).")

        # Save to DB and disk
        save_stage1_report(self.source.sha256, prompt=prompt_content, db_path=self.db_path)
        out_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage1_forensic_prompt.md"
        out_file.write_text(prompt_content, encoding="utf-8")

    def copy_stage1_prompt(self):
        text = self.s1_prompt_edit.toPlainText().strip()
        if not text:
            self.compile_stage1_prompt()
            text = self.s1_prompt_edit.toPlainText().strip()
        if text:
            QApplication.clipboard().setText(text)
            self.s1_prompt_status.setText(f"✓ Copied Stage 1 Prompt ({len(text):,} chars) to clipboard. Ready for Argon (no PDF).")

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

    def save_stage1_response(self):
        text = self.s1_response_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Empty Response", "Please paste or enter the Stage 1 response before saving.")
            return

        # Save to SQLite
        save_stage1_report(self.source.sha256, response=text, db_path=self.db_path)

        # Save to disk
        out_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage1_audit_response.md"
        out_file.write_text(text, encoding="utf-8")

        self.s1_response_status.setText(
            f"✓ Saved Stage 1 Response ({len(text):,} chars) to SQLite and {out_file.name}."
        )
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
        stage1_content = self.s1_response_edit.toPlainText().strip()
        if not stage1_content:
            # Check DB or disk
            s1_data = get_stage1_report(self.source.sha256, db_path=self.db_path) or {}
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
        )

        self.s2_prompt_edit.setPlainText(prompt_content)
        self.s2_prompt_status.setText(f"✓ Generated Stage 2 prompt ({len(prompt_content):,} chars) incorporating Stage 1 ground truth.")

        # Save to DB and disk
        save_stage2_report(self.source.sha256, prompt=prompt_content, db_path=self.db_path)
        out_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage2_valuation_prompt.md"
        out_file.write_text(prompt_content, encoding="utf-8")

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
            folder = pdf_path.parent
            if folder.exists():
                QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))
                return
        # Fallback to company sources dir
        sources_dir = self.company_dir / "sources"
        if sources_dir.exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(sources_dir)))

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

    def save_stage2_response(self):
        text = self.s2_response_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Empty Report", "Please paste or enter the Stage 2 Valuation Report before saving.")
            return

        # Save to SQLite
        save_stage2_report(self.source.sha256, response=text, db_path=self.db_path)

        # Save to disk
        out_file = self.briefs_dir / f"{self.ticker}_{self.period}_stage2_valuation_note.md"
        out_file.write_text(text, encoding="utf-8")

        self.s2_response_status.setText(
            f"✓ Saved Final Valuation Report ({len(text):,} chars) to SQLite and {out_file.name}."
        )
        QMessageBox.information(
            self,
            "Final Valuation Report Saved",
            f"Stage 2 Institutional Valuation Report successfully saved to SQLite and disk!\n\n"
            f"The complete 3-Tier analysis pipeline for {self.company_title} is now recorded in your database.",
        )
