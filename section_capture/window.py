from __future__ import annotations

from pathlib import Path
import re

from PySide6.QtGui import QKeyEvent, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
)

from .db import (
    DOC_TYPES,
    load_last_opened_dir,
    save_last_opened_dir,
)
from .one_shot_view import OneShotView, open_folder_and_select
from .openrouter import (
    get_model_display_name,
    get_openrouter_model,
)
from .packages import clean_single_line_text
from .portfolio_view import PortfolioCoverageDialog


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


class DocumentClassifyDialog(QDialog):
    """Modal dialog prompting the analyst to classify a document role and reporting period."""

    def __init__(self, filename: str, initial_type: str = "annual_report", initial_period: str = "", parent=None):
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
        self.period_combo.addItem("")  # Blank by default to require explicit selection
        common_periods = ["1H26", "2H26", "FY26", "1H27", "2H27", "FY27", "1H25", "2H25", "FY25"]
        if initial_period and initial_period not in common_periods:
            common_periods.insert(0, initial_period)
        for p in common_periods:
            self.period_combo.addItem(p)
        if initial_period:
            idx_p = self.period_combo.findText(initial_period)
            if idx_p >= 0:
                self.period_combo.setCurrentIndex(idx_p)
            else:
                self.period_combo.setEditText(initial_period)
        else:
            self.period_combo.setCurrentIndex(0)
        if self.period_combo.lineEdit():
            self.period_combo.lineEdit().setPlaceholderText("Select / Enter Period")
        form.addRow("Reporting Period:", self.period_combo)

        layout.addLayout(form)

        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(self._on_accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def _on_accept(self):
        self.selected_doc_type = self.type_combo.currentData()
        period = self.period_combo.currentText().strip()
        if not period:
            QMessageBox.critical(
                self,
                "Reporting Period Required",
                "Please select or enter the reporting period (e.g. 1H26, FY26) before continuing.",
            )
            return
        self.selected_period = period
        self.accept()


class CaptureWindow(QMainWindow):
    """Minimalist main window hosting the One-Shot Autonomous Equity Research Pipeline."""

    def __init__(self, output_root: Path | None = None):
        super().__init__()
        self.output_root: Path | None = Path(output_root) if output_root else None
        self.last_opened_dir = load_last_opened_dir(db_path=self.output_root)
        self.setWindowTitle("Equity Research — Autonomous Pipeline")
        self.resize(1400, 900)
        self.setMinimumSize(980, 640)

        self.one_shot_view = OneShotView(parent=self, db_path=self.output_root)
        self.setCentralWidget(self.one_shot_view)

        self.model_status_label = QLabel()
        self.model_status_label.setStyleSheet(
            "padding: 2px 8px; color: #475569; font-size: 11px; font-weight: 500;"
        )
        self._update_model_status_label()
        self.statusBar().addPermanentWidget(self.model_status_label)
        self.statusBar().showMessage(
            "Select or create a company, drop PDFs into sources/ or SENS notices into sources/sens/, and click Start Autonomous Analysis."
        )

    def _active_model_name(self) -> str:
        return get_openrouter_model()

    def _update_model_status_label(self):
        if not hasattr(self, "model_status_label"):
            return
        model_id = self._active_model_name()
        disp = get_model_display_name(model_id)
        self.model_status_label.setText(f"🤖 Active AI: {disp} ({model_id})")

    def show_portfolio_dashboard(self):
        PortfolioCoverageDialog(db_path=self.output_root, parent=self).exec()

    def show_new_company_dialog(self):
        from .new_company_dialog import NewCompanyDialog

        dlg = NewCompanyDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            if hasattr(self, "one_shot_view") and self.one_shot_view:
                self.one_shot_view.refresh_companies(
                    select_ticker=getattr(dlg, "created_ticker", None)
                )
            if dlg.created_company_dir:
                sources_dir = dlg.created_company_dir / "sources"
                if sources_dir.is_dir():
                    self.last_opened_dir = sources_dir
                    save_last_opened_dir(sources_dir, db_path=self.output_root)
                try:
                    open_folder_and_select(sources_dir)
                except Exception:
                    pass
                QMessageBox.information(
                    self,
                    "Company Hub Created",
                    f"Initialized company hub for {dlg.created_ticker} under {dlg.created_sector.upper()}!\n\n"
                    f"Sources folder opened at:\n{sources_dir}\n\n"
                    f"Drop your company PDFs into sources/ or SENS notices into sources/sens/, "
                    f"then click '🔄 Scan Files' to begin.",
                )

    def closeEvent(self, event):
        if hasattr(self, "one_shot_view") and self.one_shot_view:
            self.one_shot_view.stop_pipeline()
        super().closeEvent(event)
