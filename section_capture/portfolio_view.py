"""Portfolio Coverage & Valuation Dashboard.

Displays all analyzed stocks across the coverage universe, their current reference prices,
12-month JSE target prices, implied returns, recommendation ratings, and actionable
monitoring triggers ('What to watch for that will move the stock').
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from companies.sectors import get_all_sectors, get_jse_sector_code, get_jse_sector_label, get_jse_sector_name, get_sector_short_label

from section_capture.db import (
    get_analyzed_stocks,
    get_stage1_report,
    get_stage2_report,
    resolve_db_path,
)
from section_capture.map_dialog import fit_dialog_to_screen


def normalize_markdown_for_qt(md: str | None) -> str:
    """Normalize LLM markdown output for clean rendering in PySide6 QTextBrowser.

    1. Fixes unclosed HTML tags (like '<br>' inside table cells or paragraphs) by converting them
       to '<br/>' so Qt's CommonMark/HTML parser does not enter a corrupted state that strips paragraphs.
    2. Re-stitches Markdown table rows broken across multiple lines or blank lines (\\n\\n) so they
       render as complete, aligned tables rather than leaking raw pipe syntax.
    """
    if not md:
        return ""

    # Replace unclosed <br> or <br > with valid self-closing <br/>
    cleaned = re.sub(r'<br\s*>', '<br/>', md, flags=re.IGNORECASE)

    lines = cleaned.splitlines()
    out: list[str] = []
    in_table = False
    cur_row = ""

    for line in lines:
        s = line.strip()
        if s.startswith("|") and s.endswith("|") and s.count("|") >= 2:
            # Full table row
            if cur_row:
                out.append(cur_row)
                cur_row = ""
            in_table = True
            out.append(s)
        elif s.startswith("|"):
            # Start or continuation of a table row
            if cur_row:
                if cur_row.endswith("|") and cur_row.count("|") >= 3:
                    out.append(cur_row)
                    cur_row = s
                else:
                    cur_row += " " + s
            else:
                cur_row = s
            in_table = True
        elif in_table and cur_row:
            if not s:
                # Blank line within an unclosed table row
                continue
            cur_row += " " + s
            if cur_row.endswith("|") and cur_row.count("|") >= 3:
                out.append(cur_row)
                cur_row = ""
        else:
            if cur_row:
                out.append(cur_row)
                cur_row = ""
            in_table = False
            out.append(line)

    if cur_row:
        out.append(cur_row)

    return "\n".join(out)


class MarkdownViewerDialog(QDialog):
    """Reusable dialog to display full Markdown reports (Stage 1 Audit or Stage 2 Valuation)."""

    def __init__(self, title: str, markdown_text: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        fit_dialog_to_screen(self, target_w=1100, target_h=750, min_w=700, min_h=450)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        browser = QTextBrowser()
        cleaned = normalize_markdown_for_qt(markdown_text)
        browser.setMarkdown(cleaned or "*(No content available)*")
        layout.addWidget(browser, 1)

        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        copy_btn = btn_box.addButton("Copy to Clipboard", QDialogButtonBox.ButtonRole.ActionRole)
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(markdown_text))
        btn_box.rejected.connect(self.accept)
        layout.addWidget(btn_box)


class PortfolioView(QWidget):
    """Interactive portfolio coverage dashboard and monitoring triggers panel."""

    def __init__(self, db_path: str | Path | None = None, parent=None):
        super().__init__(parent)
        self.db_path = resolve_db_path(db_path)
        self.stocks_data: list[dict[str, Any]] = []
        self.filtered_data: list[dict[str, Any]] = []
        self.current_stock: dict[str, Any] | None = None

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # ---------------------------------------------------------------------
        # Top Filter & Summary Bar
        # ---------------------------------------------------------------------
        filter_bar = QHBoxLayout()
        filter_bar.setSpacing(8)

        self.summary_label = QLabel()
        self.summary_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #1a237e;")
        filter_bar.addWidget(self.summary_label)

        filter_bar.addSpacing(12)
        filter_bar.addWidget(QLabel("Filter:"))

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search ticker or name...")
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.setMaximumWidth(200)
        self.search_edit.textChanged.connect(self._apply_filters)
        filter_bar.addWidget(self.search_edit)

        self.sector_combo = QComboBox()
        self.sector_combo.addItems(["All Sectors"] + [s.short_label for s in get_all_sectors()])
        self.sector_combo.currentIndexChanged.connect(self._apply_filters)
        filter_bar.addWidget(self.sector_combo)

        self.rec_combo = QComboBox()
        self.rec_combo.addItems(["All Ratings", "BUY", "HOLD", "SELL", "IN PROGRESS"])
        self.rec_combo.currentIndexChanged.connect(self._apply_filters)
        filter_bar.addWidget(self.rec_combo)

        filter_bar.addStretch()

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setToolTip("Reload coverage universe from SQLite")
        self.refresh_btn.clicked.connect(self.refresh)
        filter_bar.addWidget(self.refresh_btn)

        self.copy_table_btn = QPushButton("Copy Universe Table")
        self.copy_table_btn.setToolTip("Copy portfolio summary markdown table to clipboard")
        self.copy_table_btn.clicked.connect(self._copy_universe_table)
        filter_bar.addWidget(self.copy_table_btn)

        layout.addLayout(filter_bar)

        # ---------------------------------------------------------------------
        # Main Splitter (Table on top, What to Watch For on bottom)
        # ---------------------------------------------------------------------
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setChildrenCollapsible(False)

        # Table Container
        table_container = QWidget()
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(4)

        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "Ticker",
            "Company Name",
            "Sector",
            "Current Price",
            "12M Target",
            "Implied Upside",
            "Div Yield",
            "12M TSR",
            "Rating",
            "Stage 1 / S2 Status",
            "Analysis Date",
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.itemSelectionChanged.connect(self._on_row_selected)
        self.table.itemDoubleClicked.connect(self._on_table_double_clicked)
        table_layout.addWidget(self.table)
        splitter.addWidget(table_container)

        # Details Panel ("What to Watch For That Will Move the Stock")
        details_container = QWidget()
        details_layout = QVBoxLayout(details_container)
        details_layout.setContentsMargins(4, 6, 4, 4)
        details_layout.setSpacing(6)

        # Stock header banner + KPI cards
        self.kpi_banner = QFrame()
        self.kpi_banner.setFrameShape(QFrame.Shape.StyledPanel)
        self.kpi_banner.setStyleSheet(
            "background-color: #f8fafc; border: 1px solid #cfd8dc; border-radius: 6px; padding: 6px;"
        )
        banner_layout = QHBoxLayout(self.kpi_banner)
        banner_layout.setContentsMargins(8, 6, 8, 6)

        self.stock_title_label = QLabel("<b>Select a stock from the table above</b>")
        self.stock_title_label.setStyleSheet("font-size: 14px; color: #0d47a1;")
        banner_layout.addWidget(self.stock_title_label)

        banner_layout.addStretch()

        self.kpi_metrics_label = QLabel()
        self.kpi_metrics_label.setStyleSheet("font-size: 12px; color: #37474f;")
        banner_layout.addWidget(self.kpi_metrics_label)
        details_layout.addWidget(self.kpi_banner)

        # Section Title
        watch_header = QHBoxLayout()
        watch_title = QLabel("<b>What to Watch For That Will Move the Stock (Monitoring Triggers & Catalysts)</b>")
        watch_title.setStyleSheet("font-size: 13px; color: #263238;")
        watch_header.addWidget(watch_title)
        watch_header.addStretch()

        self.copy_triggers_btn = QPushButton("Copy Triggers")
        self.copy_triggers_btn.setToolTip("Copy actionable monitoring triggers to clipboard")
        self.copy_triggers_btn.clicked.connect(self._copy_triggers)
        watch_header.addWidget(self.copy_triggers_btn)

        self.view_s2_btn = QPushButton("View Full Valuation Note")
        self.view_s2_btn.clicked.connect(self._view_stage2_note)
        watch_header.addWidget(self.view_s2_btn)

        self.view_s1_btn = QPushButton("View Stage 1 Audit")
        self.view_s1_btn.clicked.connect(self._view_stage1_audit)
        watch_header.addWidget(self.view_s1_btn)

        self.go_to_s2_btn = QPushButton("⚡ Go to Stage 2 Valuation")
        self.go_to_s2_btn.setStyleSheet("font-weight: bold; color: #0d47a1;")
        self.go_to_s2_btn.setToolTip("Switch active company in Valuation dialog and jump to Stage 2 Valuation Note tab.")
        self.go_to_s2_btn.clicked.connect(self._go_to_stage2_tab)
        watch_header.addWidget(self.go_to_s2_btn)

        details_layout.addLayout(watch_header)

        # Text browser for Markdown rendering of triggers
        self.triggers_browser = QTextBrowser()
        self.triggers_browser.setOpenExternalLinks(True)
        details_layout.addWidget(self.triggers_browser, 1)

        splitter.addWidget(details_container)
        splitter.setSizes([340, 400])
        layout.addWidget(splitter, 1)

    def refresh(self):
        """Reload all analyzed stocks from SQLite and refresh table."""
        self.stocks_data = get_analyzed_stocks(self.db_path)
        self._apply_filters()

    def _apply_filters(self):
        query = self.search_edit.text().strip().lower()
        selected_sector = self.sector_combo.currentText().lower()
        selected_rec = self.rec_combo.currentText().upper()

        filtered = []
        for s in self.stocks_data:
            ticker = s["ticker"].lower()
            name = s["company_name"].lower()
            sector = s["sector"].lower()
            rec = (s["recommendation"] or "").upper()

            if query and (query not in ticker and query not in name):
                continue
            if selected_sector != "all sectors" and sector != selected_sector:
                continue
            if selected_rec != "ALL RATINGS":
                if selected_rec not in rec:
                    continue
            filtered.append(s)

        self.filtered_data = filtered
        self._populate_table()

    def _populate_table(self):
        self.table.setRowCount(len(self.filtered_data))
        valued_count = sum(1 for s in self.stocks_data if s["has_stage2"])
        total_count = len(self.stocks_data)
        self.summary_label.setText(
            f"Coverage Universe: <b>{valued_count} Active Valuation{'s' if valued_count != 1 else ''}</b> · "
            f"<b>{total_count} Total Asset{'s' if total_count != 1 else ''} Tracked</b>"
        )

        for row_idx, s in enumerate(self.filtered_data):
            # Ticker
            t_item = QTableWidgetItem(s["ticker"])
            t_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            t_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 0, t_item)

            # Company Name
            name_item = QTableWidgetItem(s["company_name"])
            self.table.setItem(row_idx, 1, name_item)

            # Sector
            sec_display = get_jse_sector_label(s["sector"], ticker=s["ticker"])
            sec_item = QTableWidgetItem(sec_display)
            sec_item.setToolTip(f"{get_jse_sector_name(s['sector'], ticker=s['ticker'])} ({get_jse_sector_code(s['sector'], ticker=s['ticker'])})")
            sec_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 2, sec_item)

            # Current Reference Price
            ref_val = s["reference_price_zar"]
            ref_str = f"R{ref_val:,.2f}" if ref_val is not None else "—"
            ref_item = QTableWidgetItem(ref_str)
            ref_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_idx, 3, ref_item)

            # 12M Target Price
            tp_val = s["target_price_zar"]
            tp_str = f"R{tp_val:,.2f}" if tp_val is not None else "—"
            tp_item = QTableWidgetItem(tp_str)
            tp_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            tp_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_idx, 4, tp_item)

            # Implied Upside
            up_val = s["upside_pct"]
            up_str = f"{up_val:+.1f}%" if up_val is not None else "—"
            up_item = QTableWidgetItem(up_str)
            up_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            if up_val is not None:
                if up_val > 10.0:
                    up_item.setForeground(QColor("#2e7d32"))
                elif up_val < 0:
                    up_item.setForeground(QColor("#c62828"))
            self.table.setItem(row_idx, 5, up_item)

            # Dividend Yield
            dy_val = s["dividend_yield_pct"]
            dy_str = f"{dy_val:.1f}%" if dy_val is not None else "—"
            dy_item = QTableWidgetItem(dy_str)
            dy_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_idx, 6, dy_item)

            # 12M TSR
            tsr_val = s["tsr_pct"]
            tsr_str = f"{tsr_val:+.1f}%" if tsr_val is not None else "—"
            tsr_item = QTableWidgetItem(tsr_str)
            tsr_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            tsr_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            if tsr_val is not None:
                if tsr_val >= 20.0:
                    tsr_item.setForeground(QColor("#1b5e20"))
                elif tsr_val >= 10.0:
                    tsr_item.setForeground(QColor("#2e7d32"))
                elif tsr_val < 0:
                    tsr_item.setForeground(QColor("#c62828"))
            self.table.setItem(row_idx, 7, tsr_item)

            # Recommendation Badge
            rec_str = s["recommendation"] or "—"
            rec_item = QTableWidgetItem(rec_str)
            rec_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            rec_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            if "BUY" in rec_str:
                rec_item.setBackground(QColor("#e8f5e9"))
                rec_item.setForeground(QColor("#1b5e20"))
            elif "HOLD" in rec_str:
                rec_item.setBackground(QColor("#fff3e0"))
                rec_item.setForeground(QColor("#e65100"))
            elif "SELL" in rec_str:
                rec_item.setBackground(QColor("#ffebee"))
                rec_item.setForeground(QColor("#b71c1c"))
            else:
                rec_item.setForeground(QColor("#546e7a"))
            self.table.setItem(row_idx, 8, rec_item)

            # Stage 1 / S2 Status
            if s["has_stage2"]:
                status_str = f"Valued ({s['section_count']} sec)"
            elif s["has_stage1"]:
                status_str = f"Audited ({s['section_count']} sec)"
            else:
                status_str = f"Captured ({s['section_count']} sec)"
            status_item = QTableWidgetItem(status_str)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 9, status_item)

            # Analysis Date
            date_val = s["stage2_updated_at"] or s["updated_at"] or ""
            date_str = date_val.split("T")[0] if date_val else "—"
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 10, date_item)

        # Select first row if available
        if self.filtered_data:
            self.table.selectRow(0)
            self.current_stock = self.filtered_data[0]
            self._render_details(self.current_stock)
        else:
            self._clear_details()

    def _on_row_selected(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            self._clear_details()
            return
        row = selected_rows[0].row()
        if 0 <= row < len(self.filtered_data):
            self.current_stock = self.filtered_data[row]
            self._render_details(self.current_stock)

    def _clear_details(self):
        self.current_stock = None
        self.stock_title_label.setText("<b>No stock selected</b>")
        self.kpi_metrics_label.setText("")
        self.triggers_browser.setMarkdown("*(Select a stock from the table to view monitoring triggers)*")
        self.view_s1_btn.setEnabled(False)
        self.view_s2_btn.setEnabled(False)
        self.copy_triggers_btn.setEnabled(False)
        if hasattr(self, "go_to_s2_btn"):
            self.go_to_s2_btn.setEnabled(False)

    def _render_details(self, s: dict[str, Any]):
        ticker = s["ticker"]
        name = s["company_name"]
        jse_sec_name = get_jse_sector_name(s["sector"], ticker=ticker)
        jse_sec_code = get_jse_sector_code(s["sector"], ticker=ticker)
        sector_str = f"{jse_sec_name} ({jse_sec_code})" if jse_sec_code else get_sector_short_label(s["sector"])
        tp = f"R{s['target_price_zar']:,.2f}" if s["target_price_zar"] is not None else "N/A"
        ref = f"R{s['reference_price_zar']:,.2f}" if s["reference_price_zar"] is not None else "N/A"
        tsr = f"{s['tsr_pct']:+.1f}%" if s["tsr_pct"] is not None else "N/A"
        rec = s["recommendation"] or "IN PROGRESS"

        self.stock_title_label.setText(f"<b>{name} ({ticker})</b> · Sector: <i>{sector_str}</i>")
        self.kpi_metrics_label.setText(
            f"<b>Target:</b> {tp}  |  <b>Current:</b> {ref}  |  <b>12M TSR:</b> {tsr}  |  <b>Rating:</b> <b>{rec}</b>"
        )

        triggers = s.get("monitoring_triggers", "").strip()
        if triggers:
            self.triggers_browser.setMarkdown(normalize_markdown_for_qt(triggers))
        else:
            if s["has_stage2"]:
                self.triggers_browser.setMarkdown(
                    f"### {name} ({ticker}) — Institutional Valuation Note Available\n\n"
                    "No explicit monitoring triggers section was extracted from the response. "
                    "Click **View Full Valuation Note** below to inspect the complete 2-year forecast and sensitivity matrices."
                )
            elif s["has_stage1"]:
                self.triggers_browser.setMarkdown(
                    f"### {name} ({ticker}) — Stage 1 Forensic Audit Completed\n\n"
                    "Stage 1 cognitive audit determinations have been compiled. "
                    "Generate and execute the **Stage 2 Institutional Valuation Prompt** to produce the 2-year model, "
                    "target price, and actionable portfolio monitoring triggers."
                )
            else:
                self.triggers_browser.setMarkdown(
                    f"### {name} ({ticker}) — Evidence Captured ({s['section_count']} sections)\n\n"
                    "Working papers are captured in SQLite. Proceed to the **Audit & Valuation** dialog "
                    "to compile Stage 1 Cognitive Forensic Audit Determinations."
                )

        self.view_s1_btn.setEnabled(s["has_stage1"])
        self.view_s2_btn.setEnabled(s["has_stage2"])
        self.copy_triggers_btn.setEnabled(bool(triggers))
        if hasattr(self, "go_to_s2_btn"):
            self.go_to_s2_btn.setEnabled(True)

    def _on_table_double_clicked(self, item):
        row = item.row()
        if 0 <= row < len(self.filtered_data):
            self.current_stock = self.filtered_data[row]
            self._go_to_stage2_tab()

    def _go_to_stage2_tab(self):
        if not self.current_stock:
            return
        ticker = self.current_stock["ticker"]
        parent_dlg = self.window()
        if hasattr(parent_dlg, "select_company_by_ticker"):
            parent_dlg.select_company_by_ticker(ticker)
            if hasattr(parent_dlg, "tabs"):
                parent_dlg.tabs.setCurrentIndex(1)

    def _copy_triggers(self):
        if not self.current_stock:
            return
        text = self.current_stock.get("monitoring_triggers", "").strip()
        if text:
            QApplication.clipboard().setText(text)
            QMessageBox.information(self, "Copied", "Monitoring triggers copied to clipboard.")

    def _copy_universe_table(self):
        if not self.stocks_data:
            QMessageBox.information(self, "No Data", "No analyzed stocks to export.")
            return

        lines = [
            "| Ticker | Company Name | Sector | Ref Price (ZAR) | 12M Target (ZAR) | Upside % | Div Yield % | 12M TSR % | Rating | Status |",
            "| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |",
        ]
        for s in self.stocks_data:
            ref = f"R{s['reference_price_zar']:,.2f}" if s["reference_price_zar"] is not None else "—"
            tp = f"R{s['target_price_zar']:,.2f}" if s["target_price_zar"] is not None else "—"
            up = f"{s['upside_pct']:+.1f}%" if s["upside_pct"] is not None else "—"
            dy = f"{s['dividend_yield_pct']:.1f}%" if s["dividend_yield_pct"] is not None else "—"
            tsr = f"{s['tsr_pct']:+.1f}%" if s["tsr_pct"] is not None else "—"
            rec = s["recommendation"] or "IN PROGRESS"
            status = "Valued" if s["has_stage2"] else ("Audited" if s["has_stage1"] else "Captured")
            sec_display = get_jse_sector_label(s["sector"], ticker=s["ticker"])
            lines.append(
                f"| **{s['ticker']}** | {s['company_name']} | {sec_display} | {ref} | {tp} | {up} | {dy} | {tsr} | **{rec}** | {status} |"
            )

        md = "\n".join(lines)
        QApplication.clipboard().setText(md)
        QMessageBox.information(self, "Copied", "Portfolio coverage table copied to clipboard in Markdown format.")

    def _view_stage1_audit(self):
        if not self.current_stock:
            return
        rep = get_stage1_report(self.current_stock["sha256"], self.db_path)
        if not rep or not rep.get("stage1_response"):
            QMessageBox.warning(self, "Not Found", "No Stage 1 Forensic Audit response found for this company.")
            return
        dlg = MarkdownViewerDialog(
            f"Stage 1 Forensic Audit — {self.current_stock['company_name']} ({self.current_stock['ticker']})",
            rep["stage1_response"],
            parent=self,
        )
        dlg.exec()

    def _view_stage2_note(self):
        if not self.current_stock:
            return
        rep = get_stage2_report(self.current_stock["sha256"], self.db_path)
        if not rep or not rep.get("stage2_response"):
            QMessageBox.warning(self, "Not Found", "No Stage 2 Institutional Valuation note found for this company.")
            return
        dlg = MarkdownViewerDialog(
            f"Stage 2 Institutional Valuation Note — {self.current_stock['company_name']} ({self.current_stock['ticker']})",
            rep["stage2_response"],
            parent=self,
        )
        dlg.exec()


class PortfolioCoverageDialog(QDialog):
    """Standalone top-level dialog displaying the full Portfolio Coverage Universe."""

    def __init__(self, db_path: str | Path | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Institutional Portfolio Coverage & Monitoring Triggers Dashboard")
        fit_dialog_to_screen(self, target_w=1280, target_h=800, min_w=850, min_h=550)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        self.portfolio_view = PortfolioView(db_path=db_path, parent=self)
        layout.addWidget(self.portfolio_view, 1)

        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        btn_box.rejected.connect(self.accept)
        layout.addWidget(btn_box)
