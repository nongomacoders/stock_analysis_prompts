from __future__ import annotations

import re
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeyEvent, QKeySequence
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QFileDialog, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QMainWindow, QMessageBox, QPlainTextEdit,
    QPushButton, QProgressDialog, QScrollArea, QSpinBox, QSplitter, QToolBar, QVBoxLayout, QWidget,
)

from .content_types import CONTENT_TYPES
from .db import SavedSection, list_sections, resolve_db_path, save_section_llm_response
from .map_dialog import QuestionsLedgerDialog, ReportMapDialog, SavedSectionsDialog
from .openrouter import OpenRouterWorker, get_openrouter_model
from .packages import (
    DEFAULT_SECTOR,
    PROJECT_ROOT,
    SUPPORTED_SECTORS,
    clean_single_line_text,
    detect_sector_from_path,
    save_package,
    shorten_section_name,
)
from .pdf_source import Capture, PdfSource
from .pdf_view import PdfCanvas
from .report_map import save_map, scan_report, section_requires_subheading


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

    @property
    def textChanged(self):
        return self.lineEdit().textChanged

    def text(self) -> str:
        return self.currentText()

    def setText(self, value: str):
        self.setEditText(clean_single_line_text(value))

    def clear(self):
        self.lineEdit().clear()

    def setPlaceholderText(self, text: str):
        self.lineEdit().setPlaceholderText(text)

    def set_options(self, options: list[str]):
        current = self.lineEdit().text()
        self.blockSignals(True)
        self.lineEdit().blockSignals(True)
        super().clear()
        for opt in options:
            self.addItem(clean_single_line_text(opt))
        self.setEditText(current)
        self.lineEdit().blockSignals(False)
        self.blockSignals(False)


class CaptureWindow(QMainWindow):
    def __init__(self, output_root: Path | None = None):
        super().__init__()
        self.source: PdfSource | None = None
        self.pending: Capture | None = None
        self.captures: list[Capture] = []
        self.output_root: Path | None = Path(output_root) if output_root else None
        self.last_package: SavedSection | None = None
        self.setWindowTitle("Report Section Capture")
        self.resize(1440, 940)
        self.setMinimumSize(1000, 680)
        self.canvas = PdfCanvas()
        self.canvas.selection_changed.connect(self.selection_changed)
        self.canvas.problem.connect(self.show_problem)
        self._build_toolbar()
        self._build_body()
        self.statusBar().showMessage("Open a PDF. Your source stays unchanged; sections are saved to SQLite.")
        self._update_actions()

    def _build_toolbar(self):
        toolbar = QToolBar("PDF controls")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        open_action = QAction("Open PDF", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.choose_pdf)
        toolbar.addAction(open_action)
        toolbar.addSeparator()
        self.previous_button = QPushButton("Previous")
        self.previous_button.clicked.connect(lambda: self.page_spin.setValue(self.page_spin.value() - 1))
        toolbar.addWidget(self.previous_button)
        toolbar.addWidget(QLabel("  Page "))
        self.page_spin = QSpinBox()
        self.page_spin.setMinimum(1)
        self.page_spin.setMaximum(1)
        self.page_spin.setToolTip("Original physical PDF page, counted from 1")
        self.page_spin.valueChanged.connect(self.change_page)
        toolbar.addWidget(self.page_spin)
        self.page_total = QLabel(" of 0  ")
        toolbar.addWidget(self.page_total)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(lambda: self.page_spin.setValue(self.page_spin.value() + 1))
        toolbar.addWidget(self.next_button)
        toolbar.addSeparator()
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("Area selection", "area")
        self.mode_combo.addItem("Text selection", "text")
        self.mode_combo.currentIndexChanged.connect(lambda: self.canvas.set_mode(self.mode_combo.currentData()))
        toolbar.addWidget(self.mode_combo)
        toolbar.addSeparator()
        self.sector_combo = QComboBox()
        for sec in SUPPORTED_SECTORS:
            self.sector_combo.addItem(f"Sector: {sec.capitalize()}", sec)
        self.sector_combo.setToolTip("Active analysis sector (determines prompt template and forensic focus)")
        toolbar.addWidget(self.sector_combo)
        for label, callback in (("Fit page", self.canvas.fit_page), ("−", lambda: self.canvas.zoom(1/1.25)),
                                ("+", lambda: self.canvas.zoom(1.25)), ("Clear selection", self.canvas.clear_selection)):
            action = toolbar.addAction(label)
            action.triggered.connect(callback)
        self.full_page_action = toolbar.addAction("Select page")
        self.full_page_action.triggered.connect(self.canvas.select_full_page)
        self.map_action = toolbar.addAction('Report map')
        self.map_action.triggered.connect(self.show_report_map)
        self.questions_action = toolbar.addAction('Stored questions')
        self.questions_action.triggered.connect(self.show_questions_ledger)
        self.sections_action = toolbar.addAction('Saved sections')
        self.sections_action.triggered.connect(self.show_saved_sections)
        save_action = QAction("Save section", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_section)
        self.addAction(save_action)

    def _build_body(self):
        body = QWidget()
        layout = QVBoxLayout(body)
        layout.setContentsMargins(20, 16, 20, 10)
        self.document_label = QLabel("No report open")
        self.document_label.setObjectName("documentTitle")
        layout.addWidget(self.document_label)
        hint = QLabel("1  Open report     2  Name your section     3  Select evidence     4  Save to SQLite & copy prompt")
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
        self.heading_edit = HeadingComboBox()
        self.heading_edit.setPlaceholderText("Select from dropdown or type section heading")
        self.heading_edit.textChanged.connect(self._update_actions)
        self.heading_edit.currentIndexChanged.connect(lambda _: self._update_actions())
        form.addRow("Section heading", self.heading_edit)
        self.subheading_label = QLabel("Sub-heading (optional)")
        self.subheading_edit = SanitizedLineEdit()
        self.subheading_edit.setPlaceholderText("Optional: e.g. Statement of Financial Position")
        self.subheading_edit.textChanged.connect(self._update_actions)
        form.addRow(self.subheading_label, self.subheading_edit)
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
        new = QPushButton("New section")
        new.clicked.connect(self.new_section)
        row.addWidget(remove)
        row.addWidget(new)
        side.addLayout(row)

        save_row = QHBoxLayout()
        save_row.setSpacing(6)
        self.save_button = QPushButton("Save && copy prompt")
        self.save_button.setToolTip("Save section to SQLite and copy reading prompt to clipboard.")
        self.save_button.clicked.connect(self.save_section)
        self.save_and_run_button = QPushButton("Save && Run DeepSeek")
        self.save_and_run_button.setObjectName("primary")
        self.save_and_run_button.setToolTip("Save section to SQLite and automatically query DeepSeek via OpenRouter API.")
        self.save_and_run_button.clicked.connect(self.save_and_run_model)
        save_row.addWidget(self.save_button)
        save_row.addWidget(self.save_and_run_button)
        side.addLayout(save_row)

        self.nitro_checkbox = QCheckBox("Use Nitro throughput (:nitro)")
        self.nitro_checkbox.setToolTip("Appends :nitro to route via high-throughput priority endpoints when standard response times slow down.")
        self.nitro_checkbox.toggled.connect(self._update_nitro_tooltip)
        side.addWidget(self.nitro_checkbox)

        # Auxiliary navigation and helper buttons in one compact row
        aux_row = QHBoxLayout()
        aux_row.setSpacing(6)
        self.questions_button = QPushButton("Stored questions")
        self.questions_button.setToolTip("Store or update open verification questions from previous sections.")
        self.questions_button.clicked.connect(self.show_questions_ledger)
        self.copy_button = QPushButton("Copy prompt")
        self.copy_button.setToolTip("Re-copy the prompt of the last saved section to clipboard.")
        self.copy_button.clicked.connect(self.copy_prompt)
        self.folder_button = QPushButton("Saved sections")
        self.folder_button.setToolTip("Browse and inspect saved sections in SQLite.")
        self.folder_button.clicked.connect(self.show_saved_sections)
        aux_row.addWidget(self.questions_button)
        aux_row.addWidget(self.copy_button)
        aux_row.addWidget(self.folder_button)
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
        options: list[str] = []
        seen: set[str] = set()

        def _add(val: str):
            cleaned = " ".join((val or "").split()).strip()
            if cleaned and cleaned.lower() not in seen:
                seen.add(cleaned.lower())
                options.append(cleaned)

        if self.source:
            for saved in list_sections(self.source.sha256, db_path=self.output_root):
                if saved.heading:
                    _add(saved.heading)
                if saved.subheading and self.source.report_map and "." in saved.section_id:
                    parent_id = saved.section_id.split(".")[0]
                    for sec in self.source.report_map.get("sections", []):
                        if sec.get("section_id") == parent_id and not sec.get("parent_heading") and saved.heading:
                            sec["parent_heading"] = saved.heading

        if self.source and self.source.report_map:
            for sec in self.source.report_map.get("sections", []):
                if sec.get("kind") == "unclassified":
                    continue
                if sec.get("parent_heading"):
                    _add(sec["parent_heading"])
                _add(sec.get("title", ""))
                for ev in sec.get("heading_evidence", []):
                    _add(ev.get("heading", ""))

        self.heading_edit.set_options(options)

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
        self.questions_button.setEnabled(has_pdf)
        q_text = (getattr(self.source, "questions_ledger", "") or "").strip() if has_pdf else ""
        if q_text:
            q_lines = len([ln for ln in q_text.splitlines() if ln.strip()])
            self.questions_button.setText(f"Stored questions ({q_lines} lines)")
        else:
            self.questions_button.setText("Stored questions (none)")
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
        not_busy = not (hasattr(self, "_active_worker") and self._active_worker and self._active_worker.isRunning())

        self.add_button.setEnabled(self.pending is not None)
        if self.pending is not None:
            self.add_button.setToolTip("Add current uncommitted canvas selection to this section.")
        elif self.captures:
            self.add_button.setToolTip(f"{len(self.captures)} selection(s) already added below. Select another area on the PDF to add more.")
        else:
            self.add_button.setToolTip("Disabled: Drag an area or select text on the PDF canvas first.")

        self.apply_type_button.setEnabled(0 <= self.parts.currentRow() < len(self.captures))
        self.save_button.setEnabled(is_savable and not_busy)
        if hasattr(self, "save_and_run_button"):
            self.save_and_run_button.setEnabled(is_savable and not_busy)

        # Dynamic tooltips explaining why Save is enabled or disabled
        if not not_busy:
            save_tip = "Waiting for model query to finish..."
        elif not has_selection:
            save_tip = "Disabled: Select text or area evidence from the PDF first."
        elif not has_heading:
            save_tip = "Disabled: Choose or enter a Section heading above first."
        elif needs_subheading:
            save_tip = f"Disabled: Section {req} has subsections; enter a sub-heading above."
        else:
            save_tip = "Save section to SQLite and copy reading prompt."

        self.save_button.setToolTip(save_tip)
        if hasattr(self, "save_and_run_button"):
            self.save_and_run_button.setToolTip(
                "Save section to SQLite and automatically query DeepSeek via OpenRouter API."
                if (is_savable and not_busy) else save_tip
            )

        # Visual guidance in warning_label
        if has_selection and not has_heading:
            self.warning_label.setText("⚠ Choose or enter a Section heading above to enable Save")
        elif needs_subheading:
            self.warning_label.setText(f"⚠ Enter a sub-heading: Section {req} already has subsections")
        elif not (self.pending and self.pending.warnings):
            if self.warning_label.text().startswith("⚠"):
                self.warning_label.setText("")

        self.copy_button.setEnabled(self.last_package is not None)
        if self.last_package is not None:
            self.copy_button.setToolTip(f"Re-copy prompt for '{self.last_package.name}' to clipboard.")
        else:
            self.copy_button.setToolTip("Disabled: No section has been saved yet in this session.")
        self.folder_button.setEnabled(has_pdf)

    def show_problem(self, message: str):
        self.warning_label.setText(message)
        self.statusBar().showMessage(message)

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
        filename, _ = QFileDialog.getOpenFileName(self, "Open company report", str(PROJECT_ROOT / "companies"), "PDF documents (*.pdf)")
        if filename:
            self.open_pdf(filename)


    def _can_discard(self):
        if self.captures or self.pending:
            return QMessageBox.question(self, "Unsaved section", "Discard the current unsaved selections?",
                                        QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
                                        QMessageBox.StandardButton.Cancel) == QMessageBox.StandardButton.Discard
        return True

    def open_pdf(self, filename: str | Path):
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
        if hasattr(self, "sector_combo"):
            inferred_sec = detect_sector_from_path(candidate.path)
            idx = self.sector_combo.findData(inferred_sec)
            if idx >= 0:
                self.sector_combo.setCurrentIndex(idx)
        db_file = resolve_db_path(self.output_root)
        self.export_label.setText(f"SQLite DB: {db_file.name}")
        self.export_label.setToolTip(str(db_file))
        self._reset_section()
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
        if old:
            old.close()
        self.statusBar().showMessage("Report opened. Page numbers refer to the original physical PDF pages.")
        self._update_actions()
        if candidate.report_map is None:
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
        if self.source:
            ReportMapDialog(self.source, self.scan_report_map, self).exec()

    def show_questions_ledger(self):
        if self.source:
            QuestionsLedgerDialog(self.source, self, db_path=self.output_root).exec()
            self._update_actions()

    def show_saved_sections(self):
        if self.source:
            SavedSectionsDialog(self.source, self, db_path=self.output_root).exec()
            self._update_actions()

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

    def new_section(self):
        if self._can_discard():
            self._reset_section()

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
        self.run_model_for_package(saved)

    def _active_model_name(self) -> str:
        base = get_openrouter_model()
        if hasattr(self, "nitro_checkbox") and self.nitro_checkbox.isChecked():
            if not base.endswith(":nitro"):
                return f"{base}:nitro"
        return base

    def _update_nitro_tooltip(self):
        model = self._active_model_name()
        tag = "priority throughput" if ":nitro" in model else "standard throughput"
        self.save_and_run_button.setToolTip(f"Save section to SQLite and automatically query {model} ({tag}).")

    def run_model_for_package(self, saved_package):
        if hasattr(self, "_active_worker") and self._active_worker and self._active_worker.isRunning():
            self.show_problem("A model query is already running in the background.")
            return

        active_model = self._active_model_name()
        short_name = shorten_section_name(saved_package.name)
        model_tag = "DeepSeek:nitro" if ":nitro" in active_model else "DeepSeek"
        self.statusBar().showMessage(f"Querying {model_tag} via OpenRouter for {short_name}...")
        worker = OpenRouterWorker(saved_package.prompt, model=active_model, parent=self)
        self._active_worker = worker
        self._update_actions()

        def on_finished(response_text: str, elapsed: float = 0.0, stats: dict | None = None):
            stats = stats or {}
            cleaned = (response_text or "").strip()
            if not cleaned:
                self.show_problem("Model returned an empty response. Not saved.")
                self._active_worker = None
                self._update_actions()
                return
            cost_usd = stats.get("cost_usd")
            tokens = {
                "prompt_tokens": stats.get("prompt_tokens"),
                "completion_tokens": stats.get("completion_tokens"),
                "total_tokens": stats.get("total_tokens"),
            }
            self.statusBar().showMessage(f"Processing LLM response for {short_name}...")
            updated, extracted = save_section_llm_response(
                saved_package.package_id,
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
                f"✓ {model_tag} responded{time_str}{cost_str}{tok_str} and ledger updated for {short_name}!"
            )
            self._active_worker = None
            self._update_actions()

        def on_error(err_msg: str):
            self.show_problem(f"Model query failed: {err_msg}")
            self._active_worker = None
            self._update_actions()

        worker.finished_query.connect(on_finished)
        worker.error_query.connect(on_error)
        worker.start()

    def copy_prompt(self):
        if self.last_package:
            QApplication.clipboard().setText(self.last_package.prompt)
            self.statusBar().showMessage("Prompt copied to clipboard.")

    def closeEvent(self, event):
        if hasattr(self, "_active_worker") and self._active_worker and self._active_worker.isRunning():
            self._active_worker.terminate()
            self._active_worker.wait(1000)
        if self._can_discard():
            self.canvas.source = None
            if self.source:
                self.source.close()
            event.accept()
        else:
            event.ignore()

