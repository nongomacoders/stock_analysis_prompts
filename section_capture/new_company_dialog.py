"""Dialog for scaffolding a new company hub (ticker, sector, models, sandbox).

Allows the analyst to initialize companies/<SECTOR>/<TICKER>/ directory trees,
optionally copy an initial PDF report into sources/, and immediately open
the report in the PySide6 capture app.

Includes intelligent AI examination of entered tickers to detect existing hubs,
discover corporate details, and verify Stage 1 and Stage 2 prompt appropriateness.
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
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from companies.sectors import get_all_sectors, resolve_sector_alias
from new_company import SUPPORTED_SECTORS, create_company
from section_capture.map_dialog import fit_dialog_to_screen
from section_capture.openrouter import get_model_display_name, get_openrouter_api_key
from section_capture.ticker_lookup import (
    TickerExamineWorker,
    check_prompt_appropriateness,
    examine_ticker_locally,
)


class NewCompanyDialog(QDialog):
    """Modal dialog to scaffold a new company hub and optionally copy/open a PDF."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Company Hub")
        self.resize(540, 460)

        self.created_ticker: str | None = None
        self.created_sector: str | None = None
        self.created_company_dir: Path | None = None
        self.created_pdf_path: Path | None = None
        self._examine_worker: TickerExamineWorker | None = None

        self._build_ui()
        fit_dialog_to_screen(self, 540, 460, min_w=480, min_h=380)

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
        subtitle.setStyleSheet("color: #64748b; font-size: 12px; margin-bottom: 4px;")
        layout.addWidget(subtitle)

        form = QFormLayout()
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        form.setVerticalSpacing(8)

        # 1. Ticker + Examine Action
        ticker_row = QHBoxLayout()
        ticker_row.setSpacing(6)
        self.ticker_edit = QLineEdit()
        self.ticker_edit.setPlaceholderText("e.g. GRT, RDF, HAR, LEW, SBK, MTN, NTU")
        self.ticker_edit.textChanged.connect(self._on_ticker_changed)
        self.ticker_edit.returnPressed.connect(self._on_examine_ticker)

        self.examine_btn = QPushButton("🔍 Examine Ticker")
        self.examine_btn.setStyleSheet(
            "font-weight: bold; padding: 4px 10px; background-color: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 4px;"
        )
        self.examine_btn.setToolTip("Check if local hub exists, or query OpenRouter to discover company name, sector, and assess Stage 1 & 2 prompt fit.")
        self.examine_btn.clicked.connect(self._on_examine_ticker)

        ticker_row.addWidget(self.ticker_edit, 1)
        ticker_row.addWidget(self.examine_btn)
        form.addRow("Ticker symbol (required):", ticker_row)

        # Assessment / Inspection Frame (expandable card)
        self.assessment_frame = QFrame()
        self.assessment_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.assessment_frame.setStyleSheet(
            "background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 6px;"
        )
        self.assessment_frame.setVisible(False)
        assess_layout = QVBoxLayout(self.assessment_frame)
        assess_layout.setContentsMargins(8, 6, 8, 6)
        assess_layout.setSpacing(4)

        self.assessment_header = QLabel()
        self.assessment_header.setWordWrap(True)
        self.assessment_header.setStyleSheet("font-size: 12px; color: #0f172a;")

        self.assessment_details = QLabel()
        self.assessment_details.setWordWrap(True)
        self.assessment_details.setStyleSheet("font-size: 11px; color: #334155;")

        assess_layout.addWidget(self.assessment_header)
        assess_layout.addWidget(self.assessment_details)
        form.addRow("", self.assessment_frame)

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

    def _on_examine_ticker(self):
        ticker = self.ticker_edit.text().strip().upper()
        if not ticker or len(ticker) < 2:
            self.status_label.setText("Please enter at least 2 characters for the ticker symbol.")
            self.status_label.setStyleSheet("font-size: 11px; color: #b45309;")
            return

        # 1. Local check first (zero latency)
        local_info = examine_ticker_locally(ticker)
        if local_info:
            sec = local_info["sector_code"]
            c_name = local_info["company_name"]
            hub_exists = local_info["hub_exists"]
            pdf_cnt = local_info.get("pdf_count", 0)

            self.name_edit.setText(c_name)
            idx = self.sector_combo.findData(sec)
            if idx >= 0:
                self.sector_combo.setCurrentIndex(idx)

            readiness = check_prompt_appropriateness(sec)
            status_color = "#166534" if hub_exists else "#0369a1"
            hub_msg = f"✓ Company Hub Already Exists ({pdf_cnt} PDF in sources/)" if hub_exists else "✓ Registered in Local System Registry"

            header_html = (
                f"<span style='color: {status_color}; font-size: 12px; font-weight: bold;'>{hub_msg}</span><br/>"
                f"<b>{c_name} ({ticker})</b> — Sector: <b>{readiness.get('display_name', sec.capitalize())}</b>"
            )
            body_html = (
                f"<div style='margin-top: 4px;'>"
                f"<b>🛡️ Stage 1 Forensic Audit:</b> {readiness['summary']}<br/>"
                f"<b>📈 Stage 2 Valuation Note:</b> Dedicated institutional forecast model active.<br/>"
                f"<span style='color: #64748b; font-size: 10px;'>Hub path: companies/{sec}/{ticker}/</span>"
                f"</div>"
            )
            self.assessment_header.setText(header_html)
            self.assessment_details.setText(body_html)
            self.assessment_frame.setVisible(True)
            self._validate()
            return

        # 2. Query OpenRouter
        api_key = get_openrouter_api_key()
        if not api_key:
            self.assessment_header.setText("<span style='color: #b45309;'>⚠️ OpenRouter API Key Not Found</span>")
            self.assessment_details.setText("Configure OPENROUTER_API_KEY in secrets.env or environment to enable online JSE company and prompt evaluation.")
            self.assessment_frame.setVisible(True)
            return

        model_name = get_model_display_name()
        self.examine_btn.setEnabled(False)
        self.examine_btn.setText("⏳ Examining...")
        self.assessment_header.setText(f"⏳ Searching live JSE & querying {model_name} for <b>{ticker}</b> details and evaluating prompt fit...")
        self.assessment_details.setText("")
        self.assessment_frame.setVisible(True)

        self._examine_worker = TickerExamineWorker(ticker, self)
        self._examine_worker.finished_examination.connect(self._on_examination_finished)
        self._examine_worker.failed_examination.connect(self._on_examination_failed)
        self._examine_worker.start()

    def _on_examination_finished(self, data: dict):
        self.examine_btn.setEnabled(True)
        self.examine_btn.setText("🔍 Examine Ticker")

        ticker = data.get("ticker", self.ticker_edit.text().strip().upper())
        c_name = data.get("company_name", ticker)
        jse_sec = data.get("jse_sector", "General")
        icb_code = data.get("icb_code", "")
        sec_code = data.get("matched_sector_code", "")
        biz_summary = data.get("business_summary", "")

        s1_info = data.get("stage1_appropriateness", {})
        s2_info = data.get("stage2_appropriateness", {})

        # Auto-populate name and sector
        if c_name and (not self.name_edit.text().strip() or self.name_edit.text() == ticker):
            self.name_edit.setText(c_name)

        matched_idx = -1
        if sec_code:
            matched_idx = self.sector_combo.findData(sec_code)
            if matched_idx < 0:
                alias = resolve_sector_alias(sec_code)
                if alias:
                    matched_idx = self.sector_combo.findData(alias)
                    sec_code = alias
        if matched_idx >= 0:
            self.sector_combo.setCurrentIndex(matched_idx)

        # Check prompt readiness in our system
        prompt_readiness = check_prompt_appropriateness(sec_code)

        s1_status = s1_info.get("status", "Appropriate")
        s1_focus = s1_info.get("focus_areas", "")
        s1_caveats = s1_info.get("caveats", "")

        s2_status = s2_info.get("status", "Appropriate")
        s2_model = s2_info.get("recommended_valuation_model", "DCF / Multiples")
        s2_drivers = s2_info.get("key_drivers", "")

        badge_color = "#166534" if prompt_readiness.get("is_registered_sector") else "#b45309"
        readiness_badge = "✓ Dedicated Prompts Active" if prompt_readiness.get("is_registered_sector") else f"⚠️ New Sector: {prompt_readiness.get('guidance', '')}"

        icb_str = f" · ICB: {icb_code}" if icb_code else ""
        header_html = (
            f"<span style='color: {badge_color}; font-size: 11px; font-weight: bold;'>{readiness_badge}</span><br/>"
            f"<b>{c_name} ({ticker})</b> — JSE: <b>{jse_sec}</b>{icb_str}"
        )

        body_html = f"<div style='margin-top: 4px; color: #334155; font-size: 11px; line-height: 1.4;'>"
        if biz_summary:
            body_html += f"<i>{biz_summary}</i><br/><hr style='border: none; border-top: 1px solid #e2e8f0; margin: 4px 0;'/>"

        body_html += f"<b>🛡️ Stage 1 Forensic Audit ({s1_status}):</b> {s1_focus}"
        if s1_caveats:
            body_html += f" <i>(Audit Focus: {s1_caveats})</i>"
        body_html += f"<br/><b>📈 Stage 2 Valuation Note ({s2_status}):</b> Model: <b>{s2_model}</b>. Drivers: {s2_drivers}</div>"

        self.assessment_header.setText(header_html)
        self.assessment_details.setText(body_html)
        self.assessment_frame.setVisible(True)
        self._validate()

    def _on_examination_failed(self, err_msg: str):
        self.examine_btn.setEnabled(True)
        self.examine_btn.setText("🔍 Examine Ticker")
        self.assessment_header.setText("<span style='color: #dc2626; font-weight: bold;'>❌ Examination Query Failed</span>")
        self.assessment_details.setText(f"Error: {err_msg}")
        self.assessment_frame.setVisible(True)

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
        sector = self.sector_combo.currentData()
        if not sector:
            QMessageBox.warning(self, "Sector Required", "Please select a valid sector.")
            return

        try:
            company_dir = create_company(ticker=ticker, sector=sector, name=name)
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
