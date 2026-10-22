"""Dialog for scaffolding a new company hub (ticker, sector, models, sandbox).

Allows the analyst to initialize companies/<SECTOR>/<TICKER>/ directory trees,
optionally copy an initial PDF report into sources/, and immediately open
the report in the PySide6 capture app.
"""

from __future__ import annotations

from pathlib import Path
import shutil

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from companies.sectors import get_all_sectors
from new_company import SUPPORTED_SECTORS, create_company
from section_capture.map_dialog import fit_dialog_to_screen


class NewCompanyDialog(QDialog):
    """Modal dialog to scaffold a new company hub and optionally copy/open a PDF."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Company Hub")
        self.resize(520, 340)

        self.created_ticker: str | None = None
        self.created_sector: str | None = None
        self.created_company_dir: Path | None = None
        self.created_pdf_path: Path | None = None

        self._build_ui()
        fit_dialog_to_screen(self, 520, 360, min_w=460, min_h=300)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        header = QLabel("Scaffold New Company Hub")
        header.setStyleSheet("font-size: 15px; font-weight: bold; color: #1e293b;")
        layout.addWidget(header)

        subtitle = QLabel(
            "Initializes standardized directory structure (sources, models, research, briefs), "
            "baseline valuation config, and interactive Jupyter sandbox under companies/<sector>/<ticker>/."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #64748b; font-size: 12px; margin-bottom: 6px;")
        layout.addWidget(subtitle)

        form = QFormLayout()
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        form.setVerticalSpacing(8)

        # 1. Ticker
        self.ticker_edit = QLineEdit()
        self.ticker_edit.setPlaceholderText("e.g. GRT, RDF, HAR, LEW, SBK, MTN")
        self.ticker_edit.textChanged.connect(self._on_ticker_changed)
        form.addRow("Ticker symbol (required):", self.ticker_edit)

        # 2. Company Name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g. Growthpoint Properties Ltd (optional)")
        form.addRow("Company full name (optional):", self.name_edit)

        # 3. Sector
        self.sector_combo = QComboBox()
        for s in get_all_sectors():
            self.sector_combo.addItem(s.short_label, s.code)
        form.addRow("Sector:", self.sector_combo)

        # 4. Initial PDF picker
        pdf_row = QHBoxLayout()
        pdf_row.setSpacing(6)
        self.pdf_path_edit = QLineEdit()
        self.pdf_path_edit.setPlaceholderText("Optional: select initial PDF report to copy to sources/")
        self.pdf_path_edit.textChanged.connect(self._update_button_text)
        self.browse_pdf_btn = QPushButton("Browse...")
        self.browse_pdf_btn.clicked.connect(self._browse_pdf)
        self.clear_pdf_btn = QPushButton("Clear")
        self.clear_pdf_btn.clicked.connect(lambda: self.pdf_path_edit.clear())

        pdf_row.addWidget(self.pdf_path_edit, 1)
        pdf_row.addWidget(self.browse_pdf_btn)
        pdf_row.addWidget(self.clear_pdf_btn)

        form.addRow("Initial PDF report (optional):", pdf_row)
        layout.addLayout(form)

        # Help / status label
        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("font-size: 11px; color: #475569;")
        layout.addWidget(self.status_label)

        layout.addStretch(1)

        # Buttons
        btn_box = QHBoxLayout()
        btn_box.setSpacing(8)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        self.create_btn = QPushButton("Create Company Hub")
        self.create_btn.setObjectName("primary")
        self.create_btn.setStyleSheet("font-weight: bold; padding: 6px 14px;")
        self.create_btn.clicked.connect(self._on_create)

        btn_box.addStretch(1)
        btn_box.addWidget(self.cancel_btn)
        btn_box.addWidget(self.create_btn)
        layout.addLayout(btn_box)

        self._validate()

    def _on_ticker_changed(self, text: str):
        # Auto-uppercase and filter to clean alphanumeric / hyphen
        clean = "".join(ch for ch in text.upper() if ch.isalnum() or ch in "-_")
        if clean != text:
            pos = self.ticker_edit.cursorPosition()
            self.ticker_edit.setText(clean)
            self.ticker_edit.setCursorPosition(pos)
        self._validate()

    def _update_button_text(self):
        pdf_path = self.pdf_path_edit.text().strip()
        if pdf_path:
            self.create_btn.setText("Create & Open PDF")
            self.status_label.setText(
                "✓ Selected PDF will be copied into the company's sources/ folder and immediately opened in the capture app."
            )
            self.status_label.setStyleSheet("font-size: 11px; color: #166534;")
        else:
            self.create_btn.setText("Create Company Hub")
            self.status_label.setText(
                "Tip: You can select a PDF now or drop it into the sources/ folder later."
            )
            self.status_label.setStyleSheet("font-size: 11px; color: #475569;")

    def _browse_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Company PDF Report",
            "",
            "PDF Files (*.pdf);;All Files (*)",
        )
        if file_path:
            self.pdf_path_edit.setText(file_path)

    def _validate(self) -> bool:
        ticker = self.ticker_edit.text().strip()
        valid = bool(ticker and len(ticker) >= 2)
        self.create_btn.setEnabled(valid)
        if not ticker:
            self.status_label.setText("Please enter a valid ticker symbol (e.g. SBK, LEW, HAR).")
            self.status_label.setStyleSheet("font-size: 11px; color: #b45309;")
        else:
            self._update_button_text()
        return valid

    def _on_create(self):
        if not self._validate():
            return

        ticker = self.ticker_edit.text().strip().upper()
        name = self.name_edit.text().strip() or ticker
        sector = self.sector_combo.currentData() or "mining"

        try:
            company_dir = create_company(ticker=ticker, name=name, sector=sector)
        except Exception as exc:
            QMessageBox.critical(self, "Error Scaffolding Company", str(exc))
            return

        pdf_input = self.pdf_path_edit.text().strip()
        target_pdf_path: Path | None = None

        if pdf_input:
            src_pdf = Path(pdf_input).resolve()
            if not src_pdf.exists() or not src_pdf.is_file():
                QMessageBox.warning(self, "PDF Not Found", f"The specified PDF file could not be found:\n{src_pdf}")
                return
            sources_dir = company_dir / "sources"
            sources_dir.mkdir(parents=True, exist_ok=True)
            dest_pdf = sources_dir / src_pdf.name
            try:
                if src_pdf.resolve() != dest_pdf.resolve():
                    shutil.copy2(src_pdf, dest_pdf)
                target_pdf_path = dest_pdf
            except Exception as exc:
                QMessageBox.warning(
                    self,
                    "PDF Copy Failed",
                    f"Company hub created, but copying PDF failed: {exc}\nYou can copy it manually into {sources_dir}",
                )

        self.created_ticker = ticker
        self.created_sector = sector
        self.created_company_dir = company_dir
        self.created_pdf_path = target_pdf_path

        self.accept()
