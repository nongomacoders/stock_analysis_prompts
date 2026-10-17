from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QAction, QDesktopServices, QKeySequence
from PySide6.QtWidgets import (
    QApplication, QComboBox, QFileDialog, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QMainWindow, QMessageBox, QPlainTextEdit,
    QPushButton, QProgressDialog, QScrollArea, QSpinBox, QSplitter, QToolBar, QVBoxLayout, QWidget,
)

from .packages import PROJECT_ROOT, save_package
from .pdf_source import Capture, PdfSource
from .pdf_view import PdfCanvas
from .content_types import CONTENT_TYPES
from .map_dialog import ReportMapDialog
from .report_map import save_map, scan_report


class CaptureWindow(QMainWindow):
    def __init__(self, output_root: Path | None = None):
        super().__init__()
        self.source: PdfSource | None = None
        self.pending: Capture | None = None
        self.captures: list[Capture] = []
        self.output_root = Path(output_root) if output_root else PROJECT_ROOT / "captures"
        self.last_package: Path | None = None
        self.setWindowTitle("Report Section Capture")
        self.resize(1440, 940)
        self.setMinimumSize(1000, 680)
        self.canvas = PdfCanvas()
        self.canvas.selection_changed.connect(self.selection_changed)
        self.canvas.problem.connect(self.show_problem)
        self._build_toolbar()
        self._build_body()
        self.statusBar().showMessage("Open a PDF. Your source stays unchanged; saved packs remain on this computer.")
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
        for label, callback in (("Fit page", self.canvas.fit_page), ("−", lambda: self.canvas.zoom(1/1.25)),
                                ("+", lambda: self.canvas.zoom(1.25)), ("Clear selection", self.canvas.clear_selection)):
            action = toolbar.addAction(label)
            action.triggered.connect(callback)
        self.full_page_action = toolbar.addAction("Select page")
        self.full_page_action.triggered.connect(self.canvas.select_full_page)
        self.map_action = toolbar.addAction('Report map')
        self.map_action.triggered.connect(self.show_report_map)
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
        hint = QLabel("1  Open report     2  Name your section     3  Select evidence     4  Save for your model")
        hint.setObjectName("muted")
        layout.addWidget(hint)
        splitter = QSplitter()
        splitter.addWidget(self.canvas)
        panel = QWidget()
        panel.setMinimumWidth(345)
        panel.setMaximumWidth(485)
        side = QVBoxLayout(panel)
        side.setSpacing(5)
        side.setContentsMargins(20, 0, 0, 0)
        title = QLabel("Capture a section")
        title.setObjectName("sectionTitle")
        side.addWidget(title)
        form = QFormLayout()
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        self.heading_edit = QLineEdit()
        self.heading_edit.setPlaceholderText("e.g. Production and operating costs")
        self.heading_edit.textChanged.connect(self._update_actions)
        form.addRow("Section heading", self.heading_edit)
        self.question_edit = QPlainTextEdit()
        self.question_edit.setPlaceholderText("Optional: which claim or concern should the model examine?")
        self.question_edit.setFixedHeight(56)
        form.addRow("Analyst question (optional)", self.question_edit)
        self.content_type_combo = QComboBox()
        for key, label in CONTENT_TYPES.items():
            self.content_type_combo.addItem(label, key)
        self.content_type_combo.setToolTip("Applies when you add or save a selection. Stays selected for the next region; each added item keeps its own type.")
        form.addRow("Data type for next selection", self.content_type_combo)
        self.label_edit = QLineEdit()
        self.label_edit.setPlaceholderText("Only if visibly printed; otherwise leave empty")
        form.addRow("Printed page label for next selection (optional)", self.label_edit)
        side.addLayout(form)
        self.selection_label = QLabel("Drag on the PDF to select an area. Use Text selection for prose.")
        self.selection_label.setWordWrap(True)
        side.addWidget(self.selection_label)
        self.preview = QPlainTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setPlaceholderText("Selected native text will appear here. Images are also saved.")
        self.preview.setFixedHeight(90)
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
        self.parts.setFixedHeight(52)
        self.parts.currentRowChanged.connect(self.preview_part)
        side.addWidget(self.parts, 1)
        row = QHBoxLayout()
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
        self.save_button = QPushButton("Save section + upload ZIP")
        self.save_button.setObjectName("primary")
        self.save_button.clicked.connect(self.save_section)
        side.addWidget(self.save_button)
        self.export_label = QLabel("Choose where your saved sections go.")
        self.export_label.setWordWrap(True)
        self.export_label.setObjectName("muted")
        side.addWidget(self.export_label)
        choose_output = QPushButton("Choose save folder…")
        choose_output.clicked.connect(self.choose_output)
        side.addWidget(choose_output)
        actions = QHBoxLayout()
        self.copy_button = QPushButton("Copy reading prompt")
        self.copy_button.clicked.connect(self.copy_prompt)
        self.folder_button = QPushButton("Open saved folder")
        self.folder_button.clicked.connect(self.open_saved_folder)
        actions.addWidget(self.copy_button)
        actions.addWidget(self.folder_button)
        side.addLayout(actions)
        side.addStretch(1)
        panel_scroll = QScrollArea()
        panel_scroll.setWidgetResizable(True)
        panel_scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        panel_scroll.setMinimumWidth(365)
        panel_scroll.setMaximumWidth(510)
        panel_scroll.setWidget(panel)
        splitter.addWidget(panel_scroll)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)
        splitter.setSizes([980, 400])
        layout.addWidget(splitter, 1)
        self.setCentralWidget(body)

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
        self.add_button.setEnabled(self.pending is not None)
        self.apply_type_button.setEnabled(0 <= self.parts.currentRow() < len(self.captures))
        self.save_button.setEnabled(bool(self.heading_edit.text().strip()) and bool(self.captures or self.pending))
        self.copy_button.setEnabled(self.last_package is not None)
        self.folder_button.setEnabled(self.last_package is not None)

    def show_problem(self, message: str):
        self.warning_label.setText(message)
        self.statusBar().showMessage(message)

    def selection_changed(self, capture):
        self.pending = capture
        if not hasattr(self, "preview"):
            return
        self.preview.setPlainText(capture.text if capture else "")
        self.warning_label.setText("\n".join(capture.warnings) if capture else "")
        if capture:
            self.selection_label.setText(f"Page {capture.page} · {capture.mode} selection · {len(capture.text):,} text characters")
        else:
            self.selection_label.setText("Drag to select evidence. Added selections stay in the list when you change pages.")
        self._update_actions()

    def choose_pdf(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open company report", str(PROJECT_ROOT / "company_results"), "PDF documents (*.pdf)")
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
        self._reset_section()
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
            save_map(mapping)
            self.source.report_map = mapping
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
            self.pending.printed_label = self.label_edit.text().strip() or None
            self.pending.content_type = self.content_type_combo.currentData()
            self.captures.append(self.pending)
            self.parts.addItem(self.part_label(len(self.captures) - 1))
            self.canvas.clear_selection()
            self.label_edit.clear()
            self.parts_label.setText(f"Section selections · {len(self.captures)}")
            self._update_actions()

    def preview_part(self, row):
        if 0 <= row < len(self.captures):
            cap = self.captures[row]
            self.preview.setPlainText(cap.text)
            self.warning_label.setText("\n".join(cap.warnings))
            self.selection_label.setText(f"Added selection {row + 1} · original page {cap.page} · {cap.mode} · {CONTENT_TYPES[cap.content_type]}")
        self._update_actions()

    def part_label(self, row):
        cap = self.captures[row]
        return f"{row + 1:02d}  ·  Page {cap.page}  ·  {CONTENT_TYPES[cap.content_type]}  ·  {cap.mode}"

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
        self.question_edit.clear()
        self.content_type_combo.setCurrentIndex(0)
        self.label_edit.clear()
        self.parts_label.setText("Section selections · 0")
        self._update_actions()

    def new_section(self):
        if self._can_discard():
            self._reset_section()

    def choose_output(self):
        chosen = QFileDialog.getExistingDirectory(self, "Save sections in", str(self.output_root))
        if chosen:
            self.output_root = Path(chosen)
            self.export_label.setText(str(self.output_root))

    def save_section(self):
        if not self.source or not self.heading_edit.text().strip():
            self.show_problem("Open a PDF and enter a section heading first.")
            return None
        if self.pending:
            self.add_selection()
        try:
            folder = save_package(self.source, self.heading_edit.text(), self.question_edit.toPlainText(), self.captures, self.output_root)
        except Exception as exc:
            QMessageBox.warning(self, "Could not save section", str(exc))
            return None
        self.last_package = folder
        self._reset_section()
        self.export_label.setText(f"Saved: {folder.name}")
        self.export_label.setToolTip(str(folder))
        self.statusBar().showMessage("Saved. Upload the PNGs and paste the reading prompt for a summary and suggested checks.")
        self._update_actions()
        return folder

    def copy_prompt(self):
        if self.last_package:
            try:
                QApplication.clipboard().setText((self.last_package / "prompt.md").read_text(encoding="utf-8"))
                self.statusBar().showMessage("Prompt copied. Attach the saved evidence PNGs in your model chat.")
            except OSError as exc:
                self.show_problem(str(exc))

    def open_saved_folder(self):
        if self.last_package:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.last_package)))

    def closeEvent(self, event):
        if self._can_discard():
            self.canvas.source = None
            if self.source:
                self.source.close()
            event.accept()
        else:
            event.ignore()
