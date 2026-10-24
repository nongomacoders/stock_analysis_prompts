from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import re

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QAction, QKeyEvent, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFileDialog, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QMainWindow, QMessageBox, QPlainTextEdit,
    QPushButton, QProgressDialog, QScrollArea, QSpinBox, QSplitter, QTextEdit, QToolBar, QVBoxLayout, QWidget,
)

from .audit_dialog import AuditValuationDialog
from .content_types import CONTENT_TYPES
from .db import (
    DOC_TYPES,
    SavedSection,
    _row_to_saved_section,
    auto_link_companion_reports,
    auto_link_parent_report,
    connect_db,
    detect_doc_type_and_date,
    detect_reporting_period,
    get_doc_badge,
    get_doc_code,
    get_linked_sens_reports,
    get_parent_report,
    link_sens_report,
    list_sections,
    load_last_opened_dir,
    resolve_db_path,
    save_last_opened_dir,
    save_section_llm_response,
    set_report_doc_type,
    to_relative_project_path,
    upsert_report,
)
from .map_dialog import QuestionsLedgerDialog, ReportMapDialog, SavedSectionsDialog
from .openrouter import (
    OpenRouterWorker,
    get_model_display_name,
    get_model_short_tag,
    get_openrouter_model,
)
from companies.sectors import get_all_sectors
from .packages import (
    PROJECT_ROOT,
    SUPPORTED_SECTORS,
    build_prompt,
    clean_single_line_text,
    detect_sector_from_path,
    extract_selection_texts,
    has_sector_prompt,
    save_package,
    shorten_section_name,
)
from .pdf_source import Capture, PdfSource
from .pdf_view import PdfCanvas
from .report_map import (
    insert_section_into_report_map,
    load_questions_ledger,
    preview_inserted_section_id,
    save_map,
    scan_report,
    section_requires_subheading,
)


class SanitizedLineEdit(QLineEdit):
    """Single-line text input that automatically strips tabs, line breaks, and collapses whitespace on paste or input."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.textChanged.connect(self._on_text_changed)

    def paste(self):
        text = QApplication.clipboard().text()
        cleaned = clean_single_line_text(text)
        self.insert(cleaned)

    def keyPressEvent(self, event: QKeyEvent):
        if event.matches(QKeySequence.StandardKey.Paste):
            self.paste()
            return
        super().keyPressEvent(event)

    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        for act in menu.actions():
            if "paste" in act.text().lower():
                act.triggered.disconnect()
                act.triggered.connect(self.paste)
                break
        menu.exec(event.globalPos())

    def _on_text_changed(self, text: str):
        if any(c in text for c in "\r\n\t\xa0"):
            cleaned = re.sub(r"[\r\n\t\xa0]+", " ", text)
            cleaned = re.sub(r" {2,}", " ", cleaned)
            pos = self.cursorPosition()
            self.blockSignals(True)
            self.setText(cleaned)
            self.setCursorPosition(min(pos, len(cleaned)))
            self.blockSignals(False)
            self.textChanged.emit(cleaned)


class HeadingComboBox(QComboBox):
    """Editable dropdown for main section headings that stays API-compatible with QLineEdit."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.setLineEdit(SanitizedLineEdit(self))
        self.activated.connect(self._on_item_activated)

    def _on_item_activated(self, index: int):
        raw = self.itemData(index)
        if raw:
            self.setEditText(raw)
        else:
            txt = self.itemText(index)
            if txt.startswith("✓ "):
                self.setEditText(txt[2:].strip())

    @property
    def textChanged(self):
        return self.lineEdit().textChanged

    def text(self) -> str:
        t = self.currentText().strip()
        if t.startswith("✓ "):
            return t[2:].strip()
        return t

    def setText(self, value: str):
        cleaned = clean_single_line_text(value)
        if cleaned.startswith("✓ "):
            cleaned = cleaned[2:].strip()
        self.setEditText(cleaned)

    def clear(self):
        self.lineEdit().clear()

    def setPlaceholderText(self, text: str):
        self.lineEdit().setPlaceholderText(text)

    def set_options(self, options: list[tuple[str, str] | str]):
        current = self.text()
        self.blockSignals(True)
        self.lineEdit().blockSignals(True)
        super().clear()
        for opt in options:
            if isinstance(opt, tuple):
                disp, raw = opt
                self.addItem(clean_single_line_text(disp), clean_single_line_text(raw))
            else:
                raw_val = opt[2:].strip() if opt.startswith("✓ ") else opt
                self.addItem(clean_single_line_text(opt), clean_single_line_text(raw_val))
        self.setEditText(current)
        self.lineEdit().blockSignals(False)
        self.blockSignals(False)


class InsertSectionDialog(QDialog):
    """Dialog to insert a new section at the current page with a '-ins' ID during capture."""

    def __init__(
        self,
        parent,
        report_map: dict | None,
        current_page: int,
        page_count: int,
        initial_title: str = "",
    ):
        super().__init__(parent)
        self.report_map = report_map
        self.page_count = page_count
        self.setWindowTitle("Insert Section into Report Map")
        self.resize(480, 260)
        self.setMinimumWidth(440)
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        info = QLabel(
            "Insert a new section into the report outline while capturing.\n"
            "Existing section IDs will remain stable without shifting."
        )
        info.setObjectName("muted")
        layout.addWidget(info)

        form = QFormLayout()
        form.setSpacing(10)

        self.title_edit = SanitizedLineEdit(self)
        self.title_edit.setPlaceholderText("Section heading (e.g. Our three-pillar strategy)")
        self.title_edit.setText(clean_single_line_text(initial_title))
        form.addRow("Section heading:", self.title_edit)

        self.page_spin = QSpinBox(self)
        self.page_spin.setMinimum(1)
        self.page_spin.setMaximum(max(1, page_count))
        self.page_spin.setValue(max(1, min(current_page, page_count)))
        form.addRow("Start page:", self.page_spin)

        self.id_preview_label = QLabel(self)
        self.id_preview_label.setStyleSheet("font-weight: bold; color: #2e7d32; font-size: 13px;")
        form.addRow("Assigned ID:", self.id_preview_label)

        self.partition_preview_label = QLabel(self)
        self.partition_preview_label.setWordWrap(True)
        form.addRow("Partition:", self.partition_preview_label)

        layout.addLayout(form)

        self.page_spin.valueChanged.connect(self._update_preview)
        self._update_preview()

        btn_box = QHBoxLayout()
        btn_box.addStretch(1)
        self.submit_btn = QPushButton("Insert Section", self)
        self.submit_btn.setObjectName("primary")
        self.submit_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel", self)
        cancel_btn.clicked.connect(self.reject)
        btn_box.addWidget(cancel_btn)
        btn_box.addWidget(self.submit_btn)
        layout.addLayout(btn_box)

        self.title_edit.setFocus()
        if initial_title:
            self.title_edit.selectAll()

    def _update_preview(self):
        page = self.page_spin.value()
        try:
            cand_id, desc = preview_inserted_section_id(self.report_map, page, self.page_count)
            self.id_preview_label.setText(cand_id)
            self.partition_preview_label.setText(desc)
            if hasattr(self, "submit_btn"):
                self.submit_btn.setEnabled(True)
        except Exception as exc:
            self.id_preview_label.setText("Invalid")
            self.partition_preview_label.setText(str(exc))
            if hasattr(self, "submit_btn"):
                self.submit_btn.setEnabled(False)

    @property
    def section_title(self) -> str:
        return self.title_edit.text().strip()

    @property
    def start_page(self) -> int:
        return self.page_spin.value()


class DocumentClassifyDialog(QDialog):
    """Modal dialog prompting the analyst to classify a document role and reporting period upon opening."""

    def __init__(self, filename: str, initial_type: str = "annual_report", initial_period: str = "FY26", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Classify Document Role & Reporting Period")
        self.resize(480, 270)
        self.selected_doc_type = initial_type
        self.selected_period = initial_period

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        header = QLabel("Classify Document for Analysis")
        header.setStyleSheet("font-size: 14px; font-weight: bold; color: #1e293b;")
        layout.addWidget(header)

        fn_lbl = QLabel(f"Document: <b>{filename}</b>")
        fn_lbl.setWordWrap(True)
        fn_lbl.setStyleSheet("color: #475569; font-size: 12px;")
        layout.addWidget(fn_lbl)

        desc_lbl = QLabel(
            "Select this document's role and reporting period to ensure accurate citations ([IAR p. X] vs [AFS p. Y]), "
            "synchronized ledgers, and organized valuation briefs:"
        )
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("color: #64748b; font-size: 11px;")
        layout.addWidget(desc_lbl)

        form = QFormLayout()
        form.setVerticalSpacing(8)
        self.type_combo = QComboBox()
        for dt_key, dt_info in DOC_TYPES.items():
            self.type_combo.addItem(f"{dt_info['badge']} {dt_info['label']}", dt_key)

        idx = self.type_combo.findData(initial_type)
        if idx >= 0:
            self.type_combo.setCurrentIndex(idx)
        form.addRow("Document Role:", self.type_combo)

        self.period_combo = QComboBox()
        self.period_combo.setEditable(True)
        common_periods = ["FY26", "1H27", "FY27", "1H26", "2H26", "FY25", "1H25"]
        if initial_period not in common_periods:
            common_periods.insert(0, initial_period)
        for p in common_periods:
            self.period_combo.addItem(p)
        idx_p = self.period_combo.findText(initial_period)
        if idx_p >= 0:
            self.period_combo.setCurrentIndex(idx_p)
        else:
            self.period_combo.setEditText(initial_period)
        form.addRow("Reporting Period:", self.period_combo)

        layout.addLayout(form)

        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(self._on_accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def _on_accept(self):
        self.selected_doc_type = self.type_combo.currentData()
        self.selected_period = self.period_combo.currentText().strip() or "FY26"
        self.accept()


class CaptureWindow(QMainWindow):
    def __init__(self, output_root: Path | None = None):
        super().__init__()
        self.source: PdfSource | None = None
        self.pending: Capture | None = None
        self.captures: list[Capture] = []
        self.output_root: Path | None = Path(output_root) if output_root else None
        self.last_package: SavedSection | None = None
        self.last_opened_dir = load_last_opened_dir(db_path=self.output_root)
        self.setWindowTitle("Report Section Capture")
        self.resize(1440, 940)
        self.setMinimumSize(1000, 680)
        self.canvas = PdfCanvas()
        self.canvas.selection_changed.connect(self.selection_changed)
        self.canvas.problem.connect(self.show_problem)
        self._build_toolbar()
        self._build_body()
        self.installEventFilter(self)
        self.canvas.installEventFilter(self)
        if self.canvas.viewport():
            self.canvas.viewport().installEventFilter(self)
        app = QApplication.instance()
        if app:
            app.installEventFilter(self)
        self.model_status_label = QLabel()
        self.model_status_label.setStyleSheet("padding: 2px 8px; color: #475569; font-size: 11px; font-weight: 500;")
        self._update_model_status_label()
        self.statusBar().addPermanentWidget(self.model_status_label)
        self.statusBar().showMessage("Open a PDF. Your source stays unchanged; sections are saved to SQLite.")
        self._update_actions()

    def _build_toolbar(self):
        # Row 1: Document opening, PDF page navigation, Selection mode & Sector
        nav_toolbar = QToolBar("PDF navigation")
        nav_toolbar.setMovable(False)
        self.addToolBar(nav_toolbar)

        self.new_action = QAction("New", self)
        self.new_action.setToolTip("Scaffold a new company hub (ticker, sector, models, sandbox)")
        self.new_action.triggered.connect(self.show_new_company_dialog)
        nav_toolbar.addAction(self.new_action)

        open_action = QAction("Open PDF", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.choose_pdf)
        nav_toolbar.addAction(open_action)
        nav_toolbar.addSeparator()

        self.previous_button = QPushButton("Previous")
        self.previous_button.clicked.connect(lambda: self.page_spin.setValue(self.page_spin.value() - 1))
        nav_toolbar.addWidget(self.previous_button)
        nav_toolbar.addWidget(QLabel("  Page "))

        self.page_spin = QSpinBox()
        self.page_spin.setMinimum(1)
        self.page_spin.setMaximum(1)
        self.page_spin.setToolTip("Original physical PDF page, counted from 1")
        self.page_spin.valueChanged.connect(self.change_page)
        nav_toolbar.addWidget(self.page_spin)

        self.page_total = QLabel(" of 0  ")
        nav_toolbar.addWidget(self.page_total)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(lambda: self.page_spin.setValue(self.page_spin.value() + 1))
        nav_toolbar.addWidget(self.next_button)
        nav_toolbar.addSeparator()

        self.mode_combo = QComboBox()
        self.mode_combo.addItem("Area selection (Alt+A)", "area")
        self.mode_combo.addItem("Text selection (Alt+T)", "text")
        self.mode_combo.currentIndexChanged.connect(lambda: self.set_selection_mode(self.mode_combo.currentData()))
        nav_toolbar.addWidget(self.mode_combo)

        self.area_shortcut = QShortcut(QKeySequence("Alt+A"), self)
        self.area_shortcut.activated.connect(lambda: self.set_selection_mode("area"))
        self.text_shortcut = QShortcut(QKeySequence("Alt+T"), self)
        self.text_shortcut.activated.connect(lambda: self.set_selection_mode("text"))
        nav_toolbar.addSeparator()

        self.sector_combo = QComboBox()
        self.sector_combo.addItem("Select Sector...", None)
        for s in get_all_sectors():
            self.sector_combo.addItem(f"Sector: {s.short_label}", s.code)
        self.sector_combo.setToolTip("Active analysis sector (determines prompt template and forensic focus)")
        self.sector_combo.currentIndexChanged.connect(self._on_sector_combo_changed)
        nav_toolbar.addWidget(self.sector_combo)

        # Break to Row 2
        self.addToolBarBreak(Qt.ToolBarArea.TopToolBarArea)

        # Row 2: Zoom/View controls, Canvas selection tools, Report navigation & Dialogs
        tools_toolbar = QToolBar("Tools and analysis")
        tools_toolbar.setMovable(False)
        self.addToolBar(tools_toolbar)

        for label, callback in (("Fit page", self.canvas.fit_page), ("−", lambda: self.canvas.zoom(1/1.25)),
                                ("+", lambda: self.canvas.zoom(1.25)), ("Clear selection", self.canvas.clear_selection)):
            action = tools_toolbar.addAction(label)
            action.triggered.connect(callback)

        self.full_page_action = tools_toolbar.addAction("Select page")
        self.full_page_action.triggered.connect(self.canvas.select_full_page)
        tools_toolbar.addSeparator()

        self.map_action = tools_toolbar.addAction("Report map")
        self.map_action.triggered.connect(self.show_report_map)

        self.questions_action = tools_toolbar.addAction("Stored questions")
        self.questions_action.triggered.connect(self.show_questions_ledger)

        self.sections_action = tools_toolbar.addAction("Saved sections")
        self.sections_action.triggered.connect(self.show_saved_sections)
        tools_toolbar.addSeparator()

        self.audit_action = tools_toolbar.addAction("Audit && Valuation")
        self.audit_action.triggered.connect(self.show_audit_valuation)

        self.portfolio_action = tools_toolbar.addAction("Analyzed Stocks")
        self.portfolio_action.triggered.connect(self.show_portfolio_dashboard)

        save_action = QAction("Save section", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_section)
        self.addAction(save_action)

    def _build_body(self):
        body = QWidget()
        layout = QVBoxLayout(body)
        layout.setContentsMargins(20, 16, 20, 10)

        # Document Switcher, Role Classification & SENS bar
        doc_bar = QHBoxLayout()
        doc_bar.setSpacing(8)
        self.doc_selector = QComboBox()
        self.doc_selector.setMinimumWidth(320)
        self.doc_selector.setToolTip("Active document. Switch between reports and companion announcements.")
        self.doc_selector.currentIndexChanged.connect(self._on_doc_selected)
        doc_bar.addWidget(self.doc_selector, 1)

        doc_bar.addWidget(QLabel("Role:"))
        self.doc_type_combo = QComboBox()
        self.doc_type_combo.setToolTip("Document role / classification (determines [IAR p. X] vs [AFS p. Y] citations and ledger sync).")
        for dt_key, dt_info in DOC_TYPES.items():
            self.doc_type_combo.addItem(f"{dt_info['code']} ({dt_info['label'].split('(')[0].strip()})", dt_key)
        self.doc_type_combo.currentIndexChanged.connect(self._on_doc_type_changed)
        doc_bar.addWidget(self.doc_type_combo)

        self.add_sens_button = QPushButton("+ Add SENS Notice")
        self.add_sens_button.setToolTip("Add a subsequent SENS/ASX announcement issued after the Annual Report.")
        self.add_sens_button.clicked.connect(self.choose_and_add_sens)
        doc_bar.addWidget(self.add_sens_button)
        layout.addLayout(doc_bar)

        self.document_label = QLabel("No report open")
        self.document_label.setObjectName("documentTitle")
        self.document_label.setVisible(False)
        layout.addWidget(self.document_label)
        hint = QLabel("1  Open report     2  Name your section     3  Select evidence     4  Save to SQLite & Run Analysis")
        hint.setObjectName("muted")
        layout.addWidget(hint)
        splitter = QSplitter()
        splitter.addWidget(self.canvas)
        panel = QWidget()
        panel.setMinimumWidth(350)
        panel.setMaximumWidth(520)
        side = QVBoxLayout(panel)
        side.setSpacing(4)
        side.setContentsMargins(14, 10, 14, 10)
        title = QLabel("Capture a section")
        title.setObjectName("sectionTitle")
        side.addWidget(title)
        form = QFormLayout()
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        form.setVerticalSpacing(3)
        # Section heading row with [Use text] and [Insert]
        heading_row = QHBoxLayout()
        heading_row.setSpacing(4)
        self.heading_edit = HeadingComboBox()
        self.heading_edit.setPlaceholderText("Select from dropdown or type section heading")
        self.heading_edit.textChanged.connect(self._update_actions)
        self.heading_edit.currentIndexChanged.connect(lambda _: self._update_actions())
        self.use_text_heading_btn = QPushButton("Use text")
        self.use_text_heading_btn.setToolTip("Fill Section heading with the text currently selected on the PDF canvas.")
        self.use_text_heading_btn.clicked.connect(self.use_selected_text_for_heading)
        self.insert_btn = QPushButton("Insert")
        self.insert_btn.setToolTip("Insert a new section at the current page with a '-ins' ID into the report map.")
        self.insert_btn.clicked.connect(self.insert_section)
        heading_row.addWidget(self.heading_edit, 1)
        heading_row.addWidget(self.use_text_heading_btn)
        heading_row.addWidget(self.insert_btn)
        form.addRow("Section heading", heading_row)

        # Sub-heading row with [Use text] and [New subsection]
        subheading_row = QHBoxLayout()
        subheading_row.setSpacing(4)
        self.subheading_label = QLabel("Sub-heading (optional)")
        self.subheading_edit = SanitizedLineEdit()
        self.subheading_edit.setPlaceholderText("Optional: e.g. Statement of Financial Position")
        self.subheading_edit.textChanged.connect(self._update_actions)
        self.use_text_subheading_btn = QPushButton("Use text")
        self.use_text_subheading_btn.setToolTip("Fill Sub-heading with the text currently selected on the PDF canvas.")
        self.use_text_subheading_btn.clicked.connect(self.use_selected_text_for_subheading)
        self.new_subsection_btn = QPushButton("New subsection")
        self.new_subsection_btn.setToolTip("Keep current Section heading and start a new subsection under it.")
        self.new_subsection_btn.clicked.connect(self.new_subsection)
        subheading_row.addWidget(self.subheading_edit, 1)
        subheading_row.addWidget(self.use_text_subheading_btn)
        subheading_row.addWidget(self.new_subsection_btn)
        form.addRow(self.subheading_label, subheading_row)
        self.question_edit = QPlainTextEdit()
        self.question_edit.setPlaceholderText("Optional: which claim or concern should the model examine?")
        self.question_edit.setFixedHeight(44)
        form.addRow("Analyst question (optional)", self.question_edit)
        side.addLayout(form)

        # Compact combined Data type + Printed page label row
        type_row = QHBoxLayout()
        type_row.setSpacing(8)
        type_box = QVBoxLayout()
        type_box.setSpacing(2)
        type_box.addWidget(QLabel("Data type"))
        self.content_type_combo = QComboBox()
        for key, label in CONTENT_TYPES.items():
            self.content_type_combo.addItem(label, key)
        self.content_type_combo.setToolTip("Applies when you add or save a selection. Stays selected for the next region.")
        type_box.addWidget(self.content_type_combo)

        label_box = QVBoxLayout()
        label_box.setSpacing(2)
        label_box.addWidget(QLabel("Printed page label"))
        self.label_edit = SanitizedLineEdit()
        self.label_edit.setPlaceholderText("Optional (if printed)")
        label_box.addWidget(self.label_edit)

        type_row.addLayout(type_box, 3)
        type_row.addLayout(label_box, 2)
        side.addLayout(type_row)

        self.selection_label = QLabel("Drag on the PDF to select an area. Use Text selection for prose.")
        self.selection_label.setWordWrap(True)
        self.selection_label.setStyleSheet("font-size: 11px; color: #495d72;")
        side.addWidget(self.selection_label)
        self.preview = QPlainTextEdit()
        self.preview.setPlaceholderText("Selected native text will appear here (editable before saving).")
        self.preview.setFixedHeight(68)
        self.preview.textChanged.connect(self._preview_edited)
        side.addWidget(self.preview, 2)
        self.warning_label = QLabel()
        self.warning_label.setObjectName("warning")
        self.warning_label.setWordWrap(True)
        side.addWidget(self.warning_label)
        self.add_button = QPushButton("Add selection to section")
        self.add_button.clicked.connect(self.add_selection)
        side.addWidget(self.add_button)
        self.parts_label = QLabel("Section selections · 0")
        side.addWidget(self.parts_label)
        self.parts = QListWidget()
        self.parts.setFixedHeight(46)
        self.parts.currentRowChanged.connect(self.preview_part)
        side.addWidget(self.parts, 1)

        row = QHBoxLayout()
        row.setSpacing(6)
        self.apply_type_button = QPushButton("Set type")
        self.apply_type_button.setToolTip("Apply the data type above to the selected added item.")
        self.apply_type_button.clicked.connect(self.apply_content_type)
        row.addWidget(self.apply_type_button)
        remove = QPushButton("Remove selected")
        remove.clicked.connect(self.remove_part)
        new = QPushButton("Clear draft")
        new.setToolTip("Clear current uncommitted draft selections and headings.")
        new.clicked.connect(self.new_section)
        row.addWidget(remove)
        row.addWidget(new)
        side.addLayout(row)

        save_row = QHBoxLayout()
        save_row.setSpacing(6)
        self.save_button = QPushButton("Save Section")
        self.save_button.setToolTip("Save section to SQLite (instant, does not wait for AI). Ready for the next section.")
        self.save_button.clicked.connect(self.save_section)
        disp_name = get_model_display_name()
        short_tag = get_model_short_tag()
        self.save_and_run_button = QPushButton(f"Save && Run {short_tag}")
        self.save_and_run_button.setObjectName("primary")
        self.save_and_run_button.setToolTip(f"Save section to SQLite and queue for {disp_name} analysis in the background.")
        self.save_and_run_button.clicked.connect(self.save_and_run_model)
        save_row.addWidget(self.save_button)
        save_row.addWidget(self.save_and_run_button)
        side.addLayout(save_row)

        self.nitro_checkbox = QCheckBox("Use Nitro throughput (:nitro)")
        self.nitro_checkbox.setToolTip("Appends :nitro to route via high-throughput priority endpoints when standard response times slow down.")
        self.nitro_checkbox.toggled.connect(self._update_nitro_tooltip)
        side.addWidget(self.nitro_checkbox)

        # Batch execution and review row (clean, non-duplicated)
        aux_row = QHBoxLayout()
        aux_row.setSpacing(6)
        self.run_pending_button = QPushButton("⚡ Run Pending (0)")
        self.run_pending_button.setToolTip(f"Sequentially process all un-analyzed sections in the background using {disp_name}.")
        self.run_pending_button.clicked.connect(self.run_all_pending)
        self.review_button = QPushButton("Review Sections →")
        self.review_button.setToolTip("Browse and inspect saved sections, prompts, LLM responses, and audit status.")
        self.review_button.clicked.connect(self.show_saved_sections)
        self.folder_button = self.review_button  # alias for backwards compatibility
        self.copy_button = QPushButton("Copy prompt")
        self.copy_button.setToolTip("Re-copy the prompt of the last saved section to clipboard.")
        self.copy_button.clicked.connect(self.copy_prompt)
        self.copy_button.setEnabled(False)

        self.questions_button = QPushButton("Stored questions (none)")
        self.questions_button.setToolTip("Store or update open verification questions from previous sections.")
        self.questions_button.clicked.connect(self.show_questions_ledger)

        aux_row.addWidget(self.run_pending_button, 1)
        aux_row.addWidget(self.review_button, 1)
        aux_row.addWidget(self.questions_button, 1)
        self.copy_button.setVisible(False)
        side.addLayout(aux_row)

        db_file = resolve_db_path(self.output_root)
        self.export_label = QLabel(f"SQLite DB: {db_file.name}")
        self.export_label.setToolTip(str(db_file))
        self.export_label.setWordWrap(True)
        self.export_label.setObjectName("muted")
        side.addWidget(self.export_label)

        side.addStretch(1)
        panel_scroll = QScrollArea()
        panel_scroll.setWidgetResizable(True)
        panel_scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        panel_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        panel_scroll.setMinimumWidth(370)
        panel_scroll.setMaximumWidth(520)
        panel_scroll.setWidget(panel)
        splitter.addWidget(panel_scroll)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)
        splitter.setSizes([880, 440])
        layout.addWidget(splitter, 1)
        self.setCentralWidget(body)

    def _subheading_required_for_current(self) -> str | None:
        if not self.source or not self.source.report_map:
            return None
        active = [*self.captures, *([self.pending] if self.pending else [])]
        previews = [
            {"physical_page": c.page, "bbox": list(c.bbox), "page_size_points": list(c.page_size)}
            for c in active
        ]
        return section_requires_subheading(self.source.report_map, self.heading_edit.text(), previews)

    def _refresh_heading_options(self):
        if not hasattr(self, "heading_edit"):
            return
        options: list[tuple[str, str]] = []
        seen: set[str] = set()

        saved_headings: set[str] = set()
        saved_section_ids: set[str] = set()
        if self.source:
            try:
                for saved in list_sections(self.source.sha256, db_path=self.output_root):
                    if saved.heading:
                        saved_headings.add(saved.heading.strip().lower())
                    if saved.section_id:
                        saved_section_ids.add(saved.section_id.strip().upper())
            except Exception:
                pass

        def _add(val: str, sid: str | None = None):
            cleaned = " ".join((val or "").split()).strip()
            if not cleaned:
                return
            if sid and not re.match(r"^(?:D[a-zA-Z0-9_\-\.]+|SENS(?:-\d+)?)\s*[—:\-]\s*", cleaned, flags=re.IGNORECASE):
                full_val = f"{sid} — {cleaned}"
            else:
                full_val = cleaned

            norm_key = re.sub(r"^(?:D[a-zA-Z0-9_\-\.]+|SENS(?:-\d+)?)\s*[—:\-]\s*", "", cleaned, flags=re.IGNORECASE).strip().lower()

            if norm_key not in seen:
                seen.add(norm_key)
                is_saved = False
                if sid and sid.upper() in saved_section_ids:
                    is_saved = True
                elif cleaned.lower() in saved_headings or full_val.lower() in saved_headings:
                    is_saved = True
                disp = f"✓ {full_val}" if is_saved else full_val
                options.append((disp, full_val))

        if self.source:
            doc_t, _ = detect_doc_type_and_date(self.source.path)
            if doc_t == "sens":
                stem = self.source.path.stem
                clean_title = re.sub(r"^\d{8}[-_]?(?:[A-Za-z0-9]+[-_]?){1,3}", "", stem).replace("-", " ").replace("_", " ").strip()
                if clean_title:
                    _add(f"SENS: {clean_title}")
                _add("SENS-01: Key Terms & Offtake Agreements")
                _add("SENS-02: Operational Milestones & Development Timeline")
                _add("SENS-03: Cash Flow & Financing CPs")

        if self.source and self.source.report_map:
            for sec in self.source.report_map.get("sections", []):
                sid = sec.get("section_id")
                if sec.get("parent_heading"):
                    _add(sec["parent_heading"], sid=sid)
                title = sec.get("title", "")
                if (
                    title
                    and not title.lower().startswith("unclassified")
                    and title.lower() not in ("cover / overview", "cover/overview")
                ):
                    _add(title, sid=sid)
                for ev in sec.get("heading_evidence", []):
                    _add(ev.get("heading", ""), sid=sid)

        if self.source:
            try:
                for saved in list_sections(self.source.sha256, db_path=self.output_root):
                    if saved.subheading and self.source.report_map and "." in saved.section_id:
                        parent_id = saved.section_id.split(".")[0]
                        for sec in self.source.report_map.get("sections", []):
                            if sec.get("section_id") == parent_id and not sec.get("parent_heading") and saved.heading:
                                sec["parent_heading"] = saved.heading
                    elif saved.heading and "." not in (saved.section_id or ""):
                        clean_saved = re.sub(r"^(?:D[a-zA-Z0-9_\-\.]+|SENS(?:-\d+)?)\s*[—:\-]\s*", "", saved.heading, flags=re.IGNORECASE).strip()
                        if clean_saved.lower() not in seen:
                            _add(clean_saved, sid=saved.section_id)
            except Exception:
                pass

        self.heading_edit.set_options(options)

    def _refresh_document_selector(self):
        if not hasattr(self, "doc_selector") or not self.source:
            return
        self.doc_selector.blockSignals(True)
        self.doc_selector.clear()

        current_path = Path(self.source.path).resolve()
        # Determine company sources directory
        sources_dir = None
        if current_path.parent.name.lower() == "sens" and current_path.parent.parent.name.lower() == "sources":
            sources_dir = current_path.parent.parent
        elif current_path.parent.name.lower() == "sources":
            sources_dir = current_path.parent

        items: list[tuple[str, Path, str]] = []  # (label, path, sort_key)
        seen_paths: set[Path] = set()
        db_file = resolve_db_path(self.output_root)

        if sources_dir and sources_dir.exists():
            # 1. Main sources/*.pdf
            for p in sorted(sources_dir.glob("*.pdf"), key=lambda x: x.name.lower()):
                p_res = p.resolve()
                if p_res not in seen_paths:
                    seen_paths.add(p_res)
                    doc_t, date_str = detect_doc_type_and_date(p_res)
                    if db_file.exists():
                        with connect_db(db_file) as conn:
                            row = conn.execute("SELECT doc_type, announcement_date FROM reports WHERE (original_path LIKE ? OR filename = ?)", (f"%{p.name}%", p.name)).fetchone()
                            if row and row["doc_type"]:
                                doc_t = row["doc_type"]
                                date_str = row["announcement_date"] or date_str
                    badge = get_doc_badge(doc_t, date_str)
                    sort_order = "0_iar" if doc_t in ("iar", "annual_report") else ("1_afs" if doc_t == "afs" else ("2_pres" if doc_t == "presentation" else f"3_sens_{date_str or '9999'}"))
                    items.append((f"{badge} {p.name}", p_res, sort_order))

            # 2. SENS subfolder: sources/sens/*.pdf
            sens_sub = sources_dir / "sens"
            if sens_sub.exists():
                for p in sorted(sens_sub.glob("*.pdf"), key=lambda x: x.name.lower()):
                    p_res = p.resolve()
                    if p_res not in seen_paths:
                        seen_paths.add(p_res)
                        doc_t, date_str = detect_doc_type_and_date(p_res)
                        if db_file.exists():
                            with connect_db(db_file) as conn:
                                row = conn.execute("SELECT doc_type, announcement_date FROM reports WHERE (original_path LIKE ? OR filename = ?)", (f"%{p.name}%", p.name)).fetchone()
                                if row and row["doc_type"]:
                                    doc_t = row["doc_type"]
                                    date_str = row["announcement_date"] or date_str
                        badge = get_doc_badge(doc_t, date_str)
                        sort_order = f"3_sens_{date_str or '9999'}_{p_res.name}"
                        items.append((f"{badge} {p.name}", p_res, sort_order))

        # If current document wasn't in sources_dir, include it
        if current_path not in seen_paths:
            doc_t, date_str = detect_doc_type_and_date(current_path)
            if db_file.exists():
                with connect_db(db_file) as conn:
                    row = conn.execute("SELECT doc_type, announcement_date FROM reports WHERE (original_path LIKE ? OR filename = ?)", (f"%{current_path.name}%", current_path.name)).fetchone()
                    if row and row["doc_type"]:
                        doc_t = row["doc_type"]
                        date_str = row["announcement_date"] or date_str
            badge = get_doc_badge(doc_t, date_str)
            items.append((f"{badge} {current_path.name}", current_path, "0"))

        # Sort: IAR first, then AFS, then Presentation, then SENS by date
        items.sort(key=lambda x: x[2])

        selected_idx = 0
        for i, (label, p_path, _) in enumerate(items):
            self.doc_selector.addItem(label, str(p_path))
            if p_path == current_path:
                selected_idx = i

        self.doc_selector.setCurrentIndex(selected_idx)
        self.doc_selector.blockSignals(False)

    def _on_doc_type_changed(self, index: int):
        if not hasattr(self, "doc_type_combo") or index < 0 or not self.source:
            return
        new_type = self.doc_type_combo.itemData(index)
        if new_type:
            set_report_doc_type(self.source.sha256, new_type, self.output_root)
            self._refresh_document_selector()

    def _on_doc_selected(self, index: int):
        if not hasattr(self, "doc_selector") or index < 0:
            return
        target_path = self.doc_selector.itemData(index)
        if target_path and self.source:
            cur = Path(self.source.path).resolve()
            tgt = Path(target_path).resolve()
            if cur != tgt and tgt.exists():
                self.open_pdf(tgt)

    def choose_and_add_sens(self):
        sources_dir = None
        if self.source and hasattr(self.source, "path") and self.source.path:
            p = Path(self.source.path).resolve()
            if p.parent.name.lower() == "sens" and p.parent.parent.name.lower() == "sources":
                sources_dir = p.parent.parent
            elif p.parent.name.lower() == "sources":
                sources_dir = p.parent

        if not sources_dir or not sources_dir.exists():
            folder = getattr(self, "last_opened_dir", None)
            if folder and Path(folder).is_dir():
                sources_dir = Path(folder)
            else:
                sources_dir = PROJECT_ROOT

        sens_dir = sources_dir / "sens" if sources_dir.name.lower() == "sources" else sources_dir
        sens_dir.mkdir(parents=True, exist_ok=True)

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select SENS / ASX Notice PDF",
            str(sens_dir),
            "PDF documents (*.pdf)",
        )
        if not filename:
            return

        picked = Path(filename).resolve()
        target_file = picked
        if not (str(picked).lower().startswith(str(sources_dir).lower())):
            import shutil
            dest = sens_dir / picked.name
            if not dest.exists():
                shutil.copy2(picked, dest)
            target_file = dest

        # Track parent report before opening
        parent_sha = None
        if self.source:
            doc_t, _ = detect_doc_type_and_date(self.source.path)
            if doc_t != "sens":
                parent_sha = self.source.sha256

        self.open_pdf(target_file)
        if self.source and parent_sha and self.source.sha256 != parent_sha:
            link_sens_report(self.source.sha256, parent_sha, db_path=self.output_root)
            self.source.questions_ledger = load_questions_ledger(self.source.sha256, self.output_root)
            self._refresh_document_selector()

    def _update_actions(self):
        if not hasattr(self, "save_button"):
            return
        has_pdf = self.source is not None
        self.page_spin.setEnabled(has_pdf)
        self.previous_button.setEnabled(has_pdf and self.page_spin.value() > 1)
        self.next_button.setEnabled(has_pdf and self.page_spin.value() < self.page_spin.maximum())
        self.mode_combo.setEnabled(has_pdf)
        self.full_page_action.setEnabled(has_pdf)
        self.map_action.setEnabled(has_pdf)
        self.questions_action.setEnabled(has_pdf)
        self.sections_action.setEnabled(has_pdf)
        self.audit_action.setEnabled(True)
        if hasattr(self, "portfolio_action"):
            self.portfolio_action.setEnabled(True)
        if hasattr(self, "insert_btn"):
            self.insert_btn.setEnabled(has_pdf)
        q_text = (getattr(self.source, "questions_ledger", "") or "").strip() if has_pdf else ""
        if q_text:
            q_lines = len([ln for ln in q_text.splitlines() if ln.strip()])
            q_lbl = f"Stored questions ({q_lines} lines)"
        else:
            q_lbl = "Stored questions (none)"
        if hasattr(self, "questions_button"):
            self.questions_button.setEnabled(has_pdf)
            self.questions_button.setText(q_lbl)
        if hasattr(self, "questions_action"):
            self.questions_action.setText(q_lbl)
        if hasattr(self, "copy_button"):
            self.copy_button.setEnabled(self.last_package is not None)
        req = self._subheading_required_for_current()
        if req:
            self.subheading_label.setText(f"Sub-heading (required for {req})")
            self.subheading_edit.setPlaceholderText(f"Required — {req} already has subsections")
        else:
            self.subheading_label.setText("Sub-heading (optional)")
            self.subheading_edit.setPlaceholderText("Optional: e.g. Statement of Financial Position")
        has_any_subheading = bool(self.subheading_edit.text().strip()) or (
            bool(self.captures) and all(bool(getattr(c, "subheading", None)) for c in self.captures) and self.pending is None
        )
        needs_subheading = bool(req and not has_any_subheading)
        has_selection = bool(self.captures or self.pending)
        has_heading = bool(self.heading_edit.text().strip())
        is_savable = has_heading and has_selection and not needs_subheading
        is_worker_running = hasattr(self, "_active_worker") and self._active_worker and self._active_worker.isRunning()

        self.add_button.setEnabled(self.pending is not None)
        if self.pending is not None:
            self.add_button.setToolTip("Add current uncommitted canvas selection to this section.")
        elif self.captures:
            self.add_button.setToolTip(f"{len(self.captures)} selection(s) already added below. Select another area on the PDF to add more.")
        else:
            self.add_button.setToolTip("Disabled: Drag an area or select text on the PDF canvas first.")

        self.apply_type_button.setEnabled(0 <= self.parts.currentRow() < len(self.captures))
        
        # Local saving is completely decoupled from background query latency!
        self.save_button.setEnabled(is_savable)
        if hasattr(self, "save_and_run_button"):
            self.save_and_run_button.setEnabled(is_savable)

        # Dynamic tooltips explaining why Save is enabled or disabled
        if not has_selection:
            save_tip = "Disabled: Select text or area evidence from the PDF first."
        elif not has_heading:
            save_tip = "Disabled: Choose or enter a Section heading above first."
        elif needs_subheading:
            save_tip = f"Disabled: Section {req} has subsections; enter a sub-heading above."
        else:
            save_tip = "Save section draft to SQLite (instant, does not wait for AI)."

        self.save_button.setToolTip(save_tip)
        if hasattr(self, "save_and_run_button"):
            active_disp = get_model_display_name(self._active_model_name())
            self.save_and_run_button.setToolTip(
                f"Save section to SQLite and queue for {active_disp} analysis in the background."
                if is_savable else save_tip
            )

        # Visual guidance in warning_label
        if has_selection and not has_heading:
            self.warning_label.setText("⚠ Choose or enter a Section heading above to enable Save")
        elif needs_subheading:
            self.warning_label.setText(f"⚠ Enter a sub-heading: Section {req} already has subsections")
        elif not (self.pending and self.pending.warnings):
            if self.warning_label.text().startswith("⚠"):
                self.warning_label.setText("")

        # Update batch run button and review button
        if hasattr(self, "run_pending_button"):
            pending_count = 0
            if has_pdf and self.source:
                try:
                    with connect_db(self.output_root) as conn:
                        row = conn.execute(
                            "SELECT COUNT(*) as cnt FROM sections WHERE report_sha256 = ? AND (llm_response IS NULL OR TRIM(llm_response) = '')",
                            (self.source.sha256,),
                        ).fetchone()
                        if row:
                            pending_count = row["cnt"]
                except Exception:
                    pass

            queue_len = len(getattr(self, "_query_queue", []))
            short_tag = get_model_short_tag(self._active_model_name())
            if is_worker_running:
                in_flight = queue_len + 1
                self.run_pending_button.setText(f"⚡ {short_tag} Running ({in_flight} in queue)")
                self.run_pending_button.setEnabled(False)
            elif pending_count > 0:
                self.run_pending_button.setText(f"⚡ Run Pending ({pending_count})")
                self.run_pending_button.setEnabled(True)
            else:
                self.run_pending_button.setText("⚡ Run Pending (0)")
                self.run_pending_button.setEnabled(False)

        if hasattr(self, "review_button"):
            self.review_button.setEnabled(has_pdf)
        if hasattr(self, "folder_button"):
            self.folder_button.setEnabled(has_pdf)

    def show_problem(self, message: str):
        self.warning_label.setText(message)
        self.statusBar().showMessage(message)

    def show_critical_error(self, title: str, message: str):
        self.show_problem(message)
        QMessageBox.critical(self, title, f"{message}\n\nPlease check your OpenRouter key and connectivity, then retry.")

    def selection_changed(self, capture):
        self.pending = capture
        if not hasattr(self, "preview"):
            return
        self.preview.blockSignals(True)
        self.preview.setPlainText(capture.text if capture else "")
        self.preview.blockSignals(False)
        self.warning_label.setText("\n".join(capture.warnings) if capture else "")
        if capture:
            self.selection_label.setText(f"Page {capture.page} · {capture.mode} selection · {len(capture.text):,} text characters")
        elif self.captures:
            self.selection_label.setText(f"{len(self.captures)} selection(s) in list. Drag on PDF to add more, or save section.")
        else:
            self.selection_label.setText("Drag to select evidence. Added selections stay in the list when you change pages.")
        self._update_actions()

    def _preview_edited(self):
        edited = self.preview.toPlainText()
        if self.pending is not None:
            self.pending.text = edited
        elif 0 <= self.parts.currentRow() < len(self.captures):
            self.captures[self.parts.currentRow()].text = edited

    def choose_pdf(self):
        initial_dir = getattr(self, "last_opened_dir", None)
        if self.source and hasattr(self.source, "path") and self.source.path:
            parent_dir = Path(self.source.path).parent
            if parent_dir.is_dir():
                initial_dir = parent_dir
        if not initial_dir or not Path(initial_dir).is_dir():
            initial_dir = load_last_opened_dir(db_path=self.output_root)

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open company report",
            str(initial_dir),
            "PDF documents (*.pdf)",
        )
        if filename:
            self.open_pdf(filename)


    def _can_discard(self):
        if self.captures or self.pending:
            return QMessageBox.question(self, "Unsaved section", "Discard the current unsaved selections?",
                                        QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
                                        QMessageBox.StandardButton.Cancel) == QMessageBox.StandardButton.Discard
        return True

    def open_pdf(self, filename: str | Path, auto_scan: bool = False):
        if not self._can_discard():
            return False
        candidate = None
        try:
            candidate = PdfSource(filename)
            candidate.render(1)
        except Exception as exc:
            if candidate:
                candidate.close()
            QMessageBox.warning(self, "Cannot open report", str(exc))
            return False
        old = self.source
        self.source = candidate
        folder = Path(candidate.path).parent
        if folder.is_dir():
            self.last_opened_dir = folder
            save_last_opened_dir(folder, db_path=self.output_root)
        if hasattr(self, "sector_combo"):
            inferred_sec = detect_sector_from_path(candidate.path)
            if inferred_sec:
                idx = self.sector_combo.findData(inferred_sec)
                if idx >= 0:
                    self.sector_combo.setCurrentIndex(idx)
                if not has_sector_prompt(inferred_sec):
                    self.statusBar().showMessage(f"⚠️ Warning: Sector '{inferred_sec}' has no dedicated prompt template on disk.", 8000)
            else:
                self.sector_combo.setCurrentIndex(0)
                self.statusBar().showMessage(
                    "⚠️ Sector could not be inferred from file path. Please select the active Sector in the toolbar.",
                    10000,
                )
        db_file = resolve_db_path(self.output_root)
        self.export_label.setText(f"SQLite DB: {db_file.name}")
        self.export_label.setToolTip(str(db_file))

        doc_t, date_val = detect_doc_type_and_date(candidate.path)
        sample_txt = ""
        try:
            if candidate.plumber and len(candidate.plumber.pages) > 0:
                sample_txt = candidate.plumber.pages[0].extract_text() or ""
        except Exception:
            pass
        detected_per = detect_reporting_period(candidate.path, text_sample=sample_txt)
        period_val = detected_per

        # Check if already classified in DB or prompt user if interactive
        if db_file.exists():
            with connect_db(db_file) as conn:
                existing_rep = conn.execute("SELECT doc_type, period FROM reports WHERE sha256 = ?", (candidate.sha256,)).fetchone()
                if existing_rep:
                    if existing_rep["doc_type"]:
                        doc_t = existing_rep["doc_type"]
                    if "period" in existing_rep.keys() and existing_rep["period"]:
                        period_val = existing_rep["period"]
                elif self.isVisible() and not os.environ.get("PYTEST_CURRENT_TEST") and not getattr(self, "_suppress_classification_dialog", False):
                    dlg = DocumentClassifyDialog(candidate.path.name, initial_type=doc_t, initial_period=detected_per, parent=self)
                    if dlg.exec() == QDialog.DialogCode.Accepted:
                        doc_t = dlg.selected_doc_type
                        period_val = dlg.selected_period

        upsert_report(
            sha256=candidate.sha256,
            filename=candidate.path.name,
            original_path=to_relative_project_path(candidate.path),
            physical_page_count=candidate.page_count,
            doc_type=doc_t,
            announcement_date=date_val,
            period=period_val,
            db_path=self.output_root,
        )
        auto_link_companion_reports(candidate.sha256, candidate.path, doc_type=doc_t, db_path=self.output_root)
        candidate.period = period_val
        candidate.doc_type = doc_t
        candidate.questions_ledger = load_questions_ledger(candidate.sha256, self.output_root)

        if hasattr(self, "doc_type_combo"):
            self.doc_type_combo.blockSignals(True)
            dt_idx = self.doc_type_combo.findData(doc_t)
            if dt_idx >= 0:
                self.doc_type_combo.setCurrentIndex(dt_idx)
            self.doc_type_combo.blockSignals(False)

        self._reset_section()
        self._refresh_document_selector()
        self._refresh_heading_options()
        self.page_spin.blockSignals(True)
        self.page_spin.setMaximum(candidate.page_count)
        self.page_spin.setValue(1)
        self.page_spin.blockSignals(False)
        self.page_total.setText(f" of {candidate.page_count}  ")
        self.document_label.setText(candidate.path.name)
        self.document_label.setToolTip(str(candidate.path))
        self.canvas.fit_enabled = True
        self.canvas.set_source(candidate)
        self.canvas.setFocus()
        if old:
            old.close()
        self.statusBar().showMessage("Report opened. Page numbers refer to the original physical PDF pages.")
        self._update_actions()
        if auto_scan and candidate.report_map is None:
            self.scan_report_map()
        return True

    def scan_report_map(self):
        if not self.source:
            return False
        progress = QProgressDialog('Looking for major sections…', 'Cancel', 0, self.source.page_count, self)
        progress.setWindowTitle('Scan report sections')
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)
        progress.show()
        def update(done, total):
            progress.setLabelText(f'Checking physical PDF page {min(done + 1, total)} of {total}')
            progress.setValue(done)
            QApplication.processEvents()
            return not progress.wasCanceled()
        try:
            self.source.verify_unchanged()
            mapping = scan_report(self.source, update)
            self.source.verify_unchanged()
            save_map(mapping, self.output_root)
            self.source.report_map = mapping
            self._refresh_heading_options()
            self._update_actions()
            self.statusBar().showMessage('Draft report map ready. Reading prompts will show sections still to come.')
            return True
        except InterruptedError as exc:
            self.statusBar().showMessage(str(exc))
        except Exception as exc:
            self.show_problem(f'Section map unavailable: {exc}')
        finally:
            progress.close()
        return False

    def show_report_map(self):
        if not self.source:
            return
        if not hasattr(self, "_map_dialog") or self._map_dialog is None:
            self._map_dialog = ReportMapDialog(self.source, self.scan_report_map, self, db_path=self.output_root)
            self._map_dialog.finished.connect(self._on_map_dialog_finished)
        else:
            self._map_dialog.source = self.source
            self._map_dialog.db_path = self.output_root
            self._map_dialog._init_sections_from_source()
            self._map_dialog.refresh()
        self._map_dialog.show()
        self._map_dialog.raise_()
        self._map_dialog.activateWindow()

    def _on_map_dialog_finished(self):
        self._refresh_heading_options()
        self._map_dialog = None

    def show_questions_ledger(self):
        if self.source:
            QuestionsLedgerDialog(self.source, self, db_path=self.output_root).exec()
            self._update_actions()

    def show_saved_sections(self):
        if self.source:
            SavedSectionsDialog(self.source, self, db_path=self.output_root).exec()
            self._update_actions()

    def show_audit_valuation(self):
        AuditValuationDialog(self.source, self, db_path=self.output_root, initial_tab=0).exec()
        self._update_actions()

    def show_portfolio_dashboard(self):
        AuditValuationDialog(self.source, self, db_path=self.output_root, initial_tab=2).exec()
        self._update_actions()

    def show_new_company_dialog(self):
        from .new_company_dialog import NewCompanyDialog
        dlg = NewCompanyDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            if dlg.created_pdf_path and dlg.created_pdf_path.exists():
                self.open_pdf(dlg.created_pdf_path)
                if dlg.created_sector and hasattr(self, "sector_combo"):
                    idx = self.sector_combo.findData(dlg.created_sector)
                    if idx >= 0:
                        self.sector_combo.setCurrentIndex(idx)
            elif dlg.created_company_dir:
                if dlg.created_sector and hasattr(self, "sector_combo"):
                    idx = self.sector_combo.findData(dlg.created_sector)
                    if idx >= 0:
                        self.sector_combo.setCurrentIndex(idx)
                sources_dir = dlg.created_company_dir / "sources"
                if sources_dir.is_dir():
                    self.last_opened_dir = sources_dir
                    save_last_opened_dir(sources_dir, db_path=self.output_root)
                try:
                    from .audit_dialog import open_folder_and_select
                    open_folder_and_select(sources_dir)
                except Exception:
                    pass
                QMessageBox.information(
                    self,
                    "Company Hub Created",
                    f"Initialized company hub for {dlg.created_ticker} under {dlg.created_sector.upper()}!\n\n"
                    f"Sources folder opened at:\n{sources_dir}\n\n"
                    f"Drop your company PDF report there and click 'Open PDF' to begin.",
                )

    def change_page(self, page):
        if self.source:
            had_pending = self.pending is not None
            try:
                self.canvas.show_page(page)
                self.label_edit.clear()
                if had_pending:
                    self.statusBar().showMessage("Unadded selection cleared. Use Add selection before changing pages to keep it.")
            except Exception as exc:
                self.show_problem(str(exc))
            self._update_actions()

    def add_selection(self):
        if self.pending:
            self.pending.printed_label = clean_single_line_text(self.label_edit.text()) or None
            self.pending.content_type = self.content_type_combo.currentData()
            self.pending.subheading = clean_single_line_text(self.subheading_edit.text()) or None
            self.captures.append(self.pending)
            self.parts.addItem(self.part_label(len(self.captures) - 1))
            self.canvas.clear_selection()
            self.label_edit.clear()
            self.parts_label.setText(f"Section selections · {len(self.captures)}")
            self.selection_label.setText(f"✓ Added {len(self.captures)} selection(s). Select another area, or choose a Section heading to save.")
            self._update_actions()

    def preview_part(self, row):
        if 0 <= row < len(self.captures):
            cap = self.captures[row]
            self.preview.blockSignals(True)
            self.preview.setPlainText(cap.text)
            self.preview.blockSignals(False)
            self.warning_label.setText("\n".join(cap.warnings))
            self.selection_label.setText(f"Added selection {row + 1} · original page {cap.page} · {cap.mode} · {CONTENT_TYPES[cap.content_type]}")
        self._update_actions()

    def part_label(self, row):
        cap = self.captures[row]
        sub = f"  ·  {cap.subheading}" if getattr(cap, "subheading", None) else ""
        return f"{row + 1:02d}  ·  Page {cap.page}  ·  {CONTENT_TYPES[cap.content_type]}{sub}  ·  {cap.mode}"

    def apply_content_type(self):
        row = self.parts.currentRow()
        if 0 <= row < len(self.captures):
            self.captures[row].content_type = self.content_type_combo.currentData()
            self.parts.item(row).setText(self.part_label(row))
            self.preview_part(row)

    def remove_part(self):
        row = self.parts.currentRow()
        if 0 <= row < len(self.captures):
            self.captures.pop(row)
            self.parts.blockSignals(True)
            self.parts.clear()
            for i in range(len(self.captures)):
                self.parts.addItem(self.part_label(i))
            self.parts.blockSignals(False)
            self.parts_label.setText(f"Section selections · {len(self.captures)}")
            self.selection_changed(self.pending)

    def _reset_section(self):
        self.captures.clear()
        self.parts.clear()
        self.canvas.clear_selection()
        self.heading_edit.clear()
        self.subheading_edit.clear()
        self.question_edit.clear()
        self.content_type_combo.setCurrentIndex(0)
        self.label_edit.clear()
        self.parts_label.setText("Section selections · 0")
        self._update_actions()

    def eventFilter(self, watched, event):
        try:
            if event.type() == QEvent.Type.KeyPress:
                key = event.key()
                active_win = QApplication.activeWindow()
                if QApplication.activeModalWidget() is not None or (active_win is not None and active_win is not self):
                    return False

                is_tab = key in (Qt.Key.Key_Tab, Qt.Key.Key_Backtab)
                is_pagedown = key in (Qt.Key.Key_PageDown, Qt.Key.Key_PageUp)
                focus = QApplication.focusWidget()
                on_canvas = (watched in (self.canvas, self.canvas.viewport())) or (focus in (self.canvas, self.canvas.viewport(), self))
                is_arrow = key in (Qt.Key.Key_Right, Qt.Key.Key_Left) and on_canvas

                if is_tab or is_pagedown or is_arrow:
                    # Do not intercept Tab if delivered to or focused on a text input widget
                    if is_tab:
                        if isinstance(watched, (QLineEdit, QPlainTextEdit, QTextEdit)):
                            return False
                        if isinstance(focus, (QLineEdit, QPlainTextEdit, QTextEdit)) and watched not in (self.canvas, self.canvas.viewport()):
                            return False

                    if self.source and self.source.page_count > 0:
                        is_back = (key in (Qt.Key.Key_Backtab, Qt.Key.Key_PageUp, Qt.Key.Key_Left)) or bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
                        if is_back:
                            if self.page_spin.value() > 1:
                                self.page_spin.setValue(self.page_spin.value() - 1)
                        else:
                            if self.page_spin.value() < self.page_spin.maximum():
                                self.page_spin.setValue(self.page_spin.value() + 1)
                        if hasattr(self, "canvas") and self.canvas:
                            self.canvas.setFocus()
                        return True
        except (RuntimeError, AttributeError):
            return False
        return super().eventFilter(watched, event)



    def set_selection_mode(self, mode: str):
        idx = self.mode_combo.findData(mode)
        if idx >= 0 and self.mode_combo.currentIndex() != idx:
            self.mode_combo.blockSignals(True)
            self.mode_combo.setCurrentIndex(idx)
            self.mode_combo.blockSignals(False)
        self.canvas.set_mode(mode)
        label = "Area selection (Alt+A)" if mode == "area" else "Text selection (Alt+T)"
        self.statusBar().showMessage(f"Mode switched to: {label}")

    def _get_current_selected_text(self) -> str:
        """Returns currently selected text on canvas or in preview."""
        if hasattr(self, "preview") and self.preview.textCursor().hasSelection():
            sel = self.preview.textCursor().selectedText().strip()
            if sel:
                return sel
        if self.pending and getattr(self.pending, "text", None):
            return self.pending.text.strip()
        if hasattr(self, "preview") and self.preview.toPlainText().strip():
            return self.preview.toPlainText().strip()
        return ""

    def use_selected_text_for_heading(self):
        text = self._get_current_selected_text()
        if text:
            cleaned = clean_single_line_text(text)
            self.heading_edit.setText(cleaned)
            self.statusBar().showMessage(f"Set Section heading from selected text: '{cleaned[:45]}'")
        else:
            self.statusBar().showMessage("Select text on the PDF canvas first (press Alt+T for text selection).")

    def use_selected_text_for_subheading(self):
        text = self._get_current_selected_text()
        if text:
            cleaned = clean_single_line_text(text)
            self.subheading_edit.setText(cleaned)
            self.statusBar().showMessage(f"Set Sub-heading from selected text: '{cleaned[:45]}'")
        else:
            self.statusBar().showMessage("Select text on the PDF canvas first (press Alt+T for text selection).")

    def insert_section(self):
        if not self.source:
            QMessageBox.information(self, "No Report Open", "Open a report PDF before inserting a section.")
            return

        initial_title = ""
        if hasattr(self, "_get_current_selected_text"):
            initial_title = clean_single_line_text(self._get_current_selected_text())
        if not initial_title:
            initial_title = clean_single_line_text(self.heading_edit.text())

        current_p = self.page_spin.value()
        dlg = InsertSectionDialog(
            self,
            report_map=self.source.report_map,
            current_page=current_p,
            page_count=self.source.page_count,
            initial_title=initial_title,
        )
        if dlg.exec() == QDialog.DialogCode.Accepted:
            title = dlg.section_title
            start_p = dlg.start_page
            if not title:
                QMessageBox.warning(self, "Title Required", "Please enter a section heading.")
                return

            try:
                map_to_update = self.source.report_map
                if not map_to_update:
                    map_to_update = {
                        "status": "coarse_report_map_v1",
                        "source_filename": getattr(self.source, "filename", Path(self.source.path).name if getattr(self.source, "path", None) else "report.pdf"),
                        "source_sha256": self.source.sha256,
                        "physical_page_count": self.source.page_count,
                        "sections": [],
                    }

                updated_map, new_id = insert_section_into_report_map(
                    map_to_update,
                    title=title,
                    start_page=start_p,
                    page_count=self.source.page_count,
                )
                save_map(updated_map, cache_root=self.output_root)
                self.source.report_map = updated_map
                self._refresh_heading_options()
                self.heading_edit.setText(title)
                self.subheading_edit.clear()
                self.statusBar().showMessage(
                    f"✓ Inserted section '{new_id}: {title}' at page {start_p} into report map."
                )
                if hasattr(self, "_map_dialog") and self._map_dialog and self._map_dialog.isVisible():
                    self._map_dialog.refresh()
            except Exception as exc:
                QMessageBox.critical(self, "Error Inserting Section", str(exc))

    def new_section(self):
        if self._can_discard():
            self._reset_section()
            self.heading_edit.setFocus()
            self.statusBar().showMessage("Ready for new section. Enter section heading and select evidence on the PDF.")

    def new_subsection(self):
        if self._can_discard():
            parent_heading = self.heading_edit.text()
            self.subheading_edit.clear()
            self.question_edit.clear()
            self.captures.clear()
            self.parts.clear()
            self.canvas.clear_selection()
            self.parts_label.setText("Section selections · 0")
            self._update_actions()
            self.subheading_edit.setFocus()
            self.statusBar().showMessage(f"Ready for next subsection under '{parent_heading}'. Enter sub-heading and select evidence.")

    def save_section(self):
        if not self.source or not self.heading_edit.text().strip():
            self.show_problem("Open a PDF and enter a section heading first.")
            return None
        req = self._subheading_required_for_current()
        has_any_subheading = bool(self.subheading_edit.text().strip()) or (
            bool(self.captures) and all(bool(getattr(c, "subheading", None)) for c in self.captures) and self.pending is None
        )
        if req and not has_any_subheading:
            self.show_problem(f"Enter a sub-heading first: section {req} already has subsections.")
            return None
        if self.pending:
            self.add_selection()
        had_subheading = bool(self.subheading_edit.text().strip()) or any(getattr(c, "subheading", None) for c in self.captures)
        saved_heading = clean_single_line_text(self.heading_edit.text())
        current_sector = self.sector_combo.currentData() if hasattr(self, "sector_combo") else None
        try:
            saved = save_package(
                self.source,
                clean_single_line_text(self.heading_edit.text()),
                self.question_edit.toPlainText(),
                self.captures,
                self.output_root,
                subheading=clean_single_line_text(self.subheading_edit.text()),
                sector=current_sector,
            )
        except Exception as exc:
            QMessageBox.warning(self, "Could not save section", str(exc))
            return None
        self.last_package = saved
        QApplication.clipboard().setText(saved.prompt)
        self._reset_section()
        self._refresh_heading_options()
        if had_subheading:
            self.heading_edit.setText(saved_heading)
        short_name = shorten_section_name(saved.name)
        self.export_label.setText(f"Saved in SQLite: {short_name}")
        self.export_label.setToolTip(f"{saved.name}\n\nDatabase: {saved.db_path}")
        self.statusBar().showMessage(f"Saved in SQLite: {short_name} (prompt copied to clipboard).")
        self._update_actions()
        return saved

    def save_and_run_model(self):
        saved = self.save_section()
        if not saved:
            return
        self.queue_or_run_package(saved.package_id, name=saved.name)

    def queue_or_run_package(self, package_id: str, name: str = ""):
        if not hasattr(self, "_query_queue"):
            self._query_queue = []

        if hasattr(self, "_active_worker") and self._active_worker and self._active_worker.isRunning():
            self._query_queue.append(package_id)
            pos = len(self._query_queue)
            short_name = shorten_section_name(name) if name else f"Section {package_id[:8]}"
            short_tag = get_model_short_tag(self._active_model_name())
            self.statusBar().showMessage(
                f"✓ Saved {short_name}! Added to {short_tag} background queue (#{pos} in queue)."
            )
            self._update_actions()
            return

        self._start_query_for_package(package_id, name=name)

    def _start_query_for_package(self, package_id: str, name: str = ""):
        try:
            with connect_db(self.output_root) as conn:
                row = conn.execute("SELECT * FROM sections WHERE package_id = ?", (package_id,)).fetchone()
                if not row:
                    self._process_next_in_queue()
                    return
                sec = _row_to_saved_section(row, self.output_root)
                curr_rep = conn.execute("SELECT questions_ledger FROM reports WHERE sha256 = ?", (sec.report_sha256,)).fetchone()
                current_ledger = (curr_rep["questions_ledger"] if curr_rep else "") or ""

            manifest = copy.deepcopy(sec.manifest)
            if "heading" not in manifest:
                manifest["heading"] = sec.heading
            if "subheading" not in manifest and sec.subheading:
                manifest["subheading"] = sec.subheading
            if "package_id" not in manifest:
                manifest["package_id"] = sec.package_id
            if "source" not in manifest:
                manifest["source"] = {"filename": getattr(self.source, "filename", "report.pdf"), "sha256": sec.report_sha256}
            elif "sha256" not in manifest["source"]:
                manifest["source"]["sha256"] = sec.report_sha256
            if "selections" not in manifest:
                manifest["selections"] = sec.selections or []

            manifest["stored_questions"] = current_ledger.strip() or None
            current_sector = self.sector_combo.currentData() if hasattr(self, "sector_combo") else manifest.get("sector")
            if not current_sector:
                current_sector = detect_sector_from_path(getattr(self.source, "path", None))
            if not current_sector:
                raise ValueError("Sector must be selected before submitting query.")
            manifest["sector"] = current_sector
            texts = extract_selection_texts(manifest, selected_text=sec.selected_text, prompt=sec.prompt)
            refreshed_prompt = build_prompt(manifest, texts, sector=current_sector)

            with connect_db(self.output_root) as conn:
                conn.execute(
                    "UPDATE sections SET prompt = ?, manifest_json = ? WHERE package_id = ?",
                    (refreshed_prompt, json.dumps(manifest, ensure_ascii=False), sec.package_id),
                )

            active_model = self._active_model_name()
            short_name = shorten_section_name(name or sec.heading)
            model_tag = get_model_short_tag(active_model)
            queue_count = len(getattr(self, "_query_queue", []))
            queue_tag = f" [{queue_count} more queued]" if queue_count > 0 else ""
            self.statusBar().showMessage(f"Querying {model_tag} for {short_name}{queue_tag}...")

            worker = OpenRouterWorker(refreshed_prompt, model=active_model, parent=self)
            self._active_worker = worker
            self._update_actions()
        except Exception as exc:
            short_tag = get_model_short_tag(self._active_model_name())
            self.show_critical_error(f"{short_tag} Query Failed", f"Could not prepare section for {short_tag}: {exc}")
            if hasattr(self, "_query_queue"):
                self._query_queue.clear()
            self._active_worker = None
            self._update_actions()
            return

        def on_finished(response_text: str, elapsed: float = 0.0, stats: dict | None = None):
            stats = stats or {}
            cleaned = (response_text or "").strip()
            if cleaned:
                cost_usd = stats.get("cost_usd")
                tokens = {
                    "prompt_tokens": stats.get("prompt_tokens"),
                    "completion_tokens": stats.get("completion_tokens"),
                    "total_tokens": stats.get("total_tokens"),
                }
                updated, extracted = save_section_llm_response(
                    sec.package_id,
                    cleaned,
                    update_ledger=True,
                    response_time_seconds=elapsed,
                    cost_usd=cost_usd,
                    tokens=tokens,
                    model=active_model,
                    db_path=self.output_root,
                )
                if extracted and self.source:
                    self.source.questions_ledger = extracted
                time_str = f" in {elapsed:.1f}s" if elapsed > 0 else ""
                cost_str = f" (${cost_usd:.4f})" if cost_usd is not None else ""
                tok_str = f" [{stats.get('total_tokens', 0):,} tok]" if stats.get("total_tokens") else ""
                self.statusBar().showMessage(
                    f"✓ {model_tag} responded{time_str}{cost_str}{tok_str} for {short_name}!"
                )
            else:
                self.show_problem("Model returned an empty response. Not saved.")

            self._process_next_in_queue()

        def on_error(err_msg: str):
            self.show_critical_error("OpenRouter Query Failed", f"Model query failed for {short_name}:\n{err_msg}")
            if hasattr(self, "_query_queue"):
                self._query_queue.clear()
            self._active_worker = None
            self._update_actions()

        worker.finished_query.connect(on_finished)
        worker.error_query.connect(on_error)
        worker.start()

    def _process_next_in_queue(self):
        if hasattr(self, "_query_queue") and self._query_queue:
            next_id = self._query_queue.pop(0)
            self._start_query_for_package(next_id)
        else:
            self._active_worker = None
            self._update_actions()
            short_tag = get_model_short_tag(self._active_model_name())
            self.statusBar().showMessage(f"✓ {short_tag} completed all queued queries!")

    def run_all_pending(self):
        if not self.source:
            QMessageBox.information(self, "No Report Open", "Please open a report first.")
            return

        with connect_db(self.output_root) as conn:
            rows = conn.execute(
                "SELECT package_id, heading FROM sections WHERE report_sha256 = ? AND (llm_response IS NULL OR TRIM(llm_response) = '') ORDER BY section_number ASC",
                (self.source.sha256,),
            ).fetchall()

        if not rows:
            QMessageBox.information(self, "No Pending Sections", "All sections in this report already have saved LLM responses.")
            return

        if not hasattr(self, "_query_queue"):
            self._query_queue = []

        added = 0
        for r in rows:
            pkg_id = r["package_id"]
            if pkg_id not in self._query_queue:
                self._query_queue.append(pkg_id)
                added += 1

        short_tag = get_model_short_tag(self._active_model_name())
        self.statusBar().showMessage(f"Enqueued {added} pending section(s) for {short_tag} processing.")
        if not (hasattr(self, "_active_worker") and self._active_worker and self._active_worker.isRunning()):
            self._process_next_in_queue()
        else:
            self._update_actions()

    def run_model_for_package(self, saved_package):
        """Backward compatibility wrapper."""
        self.queue_or_run_package(saved_package.package_id, name=saved_package.name)

    def _active_model_name(self) -> str:
        base = get_openrouter_model()
        if hasattr(self, "nitro_checkbox") and self.nitro_checkbox.isChecked():
            if not base.endswith(":nitro"):
                return f"{base}:nitro"
        return base

    def _update_nitro_tooltip(self):
        model = self._active_model_name()
        tag = "priority throughput" if ":nitro" in model else "standard throughput"
        short_tag = get_model_short_tag(model)
        if hasattr(self, "save_and_run_button"):
            self.save_and_run_button.setText(f"Save && Run {short_tag}")
            self.save_and_run_button.setToolTip(f"Save section to SQLite and automatically query {model} ({tag}).")
        self._update_model_status_label()

    def _update_model_status_label(self):
        if not hasattr(self, "model_status_label"):
            return
        active_model = self._active_model_name()
        disp = get_model_display_name(active_model)
        self.model_status_label.setText(f"🤖 Model: {disp}")
        self.model_status_label.setToolTip(
            f"Active OpenRouter model: {active_model}\n"
            f"Configured via OPENROUTER_MODEL in secrets.env or environment."
        )

    def copy_prompt(self):
        if self.last_package:
            QApplication.clipboard().setText(self.last_package.prompt)
            self.statusBar().showMessage("Prompt copied to clipboard.")

    def _on_sector_combo_changed(self, index: int):
        if not hasattr(self, "sector_combo") or index < 0:
            return
        sec = self.sector_combo.itemData(index)
        if not sec:
            return
        if not has_sector_prompt(sec):
            self.statusBar().showMessage(f"⚠️ Warning: Sector '{sec}' has no dedicated reading brief prompt template on disk.", 8000)

    def closeEvent(self, event):
        app = QApplication.instance()
        if app:
            app.removeEventFilter(self)
        if hasattr(self, "_query_queue"):
            self._query_queue.clear()
        if hasattr(self, "_active_worker") and self._active_worker and self._active_worker.isRunning():
            try:
                self._active_worker.finished_query.disconnect()
                self._active_worker.error_query.disconnect()
            except Exception:
                pass
            self._active_worker.terminate()
            self._active_worker.wait(1000)
        if hasattr(self, "_map_dialog") and self._map_dialog:
            try:
                self._map_dialog.close()
            except Exception:
                pass
            self._map_dialog = None
        if self._can_discard():
            self.canvas.source = None
            if self.source:
                self.source.close()
            event.accept()
        else:
            event.ignore()

