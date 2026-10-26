"""Read-only draft overview, stored-questions ledger, and saved-sections / LLM-response dialogs."""
import copy
import json

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFrame, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMessageBox, QPlainTextEdit, QProgressBar, QPushButton, QSpinBox, QSplitter, QTableWidget, QTableWidgetItem, QTextBrowser, QVBoxLayout, QWidget,
)

from .db import (
    clear_section_llm_response,
    connect_db,
    extract_questions_ledger_from_response,
    list_sections,
    save_section_llm_response,
)
from .openrouter import (
    OpenRouterWorker,
    get_model_display_name,
    get_model_short_tag,
    get_openrouter_model,
)
from .packages import build_prompt, clean_single_line_text, detect_sector_from_path, extract_selection_texts
from .report_map import assign_section_ids, build_manual_section_map, load_questions_ledger, report_overview, save_map, save_questions_ledger
from .section_matcher import auto_capture_section, compare_section_maps, extract_all_app_sections


def fit_dialog_to_screen(dialog: QDialog, target_w: int, target_h: int, min_w: int = 540, min_h: int = 380):
    screen = QApplication.primaryScreen()
    if screen:
        avail = screen.availableGeometry()
        w = min(target_w, max(min_w, avail.width() - 60))
        h = min(target_h, max(min_h, avail.height() - 80))
        dialog.resize(w, h)
    else:
        dialog.resize(min(target_w, 860), min(target_h, 560))


class ReportMapDialog(QDialog):
    def __init__(self, source, rescan, parent=None, db_path=None):
        super().__init__(parent)
        self.setModal(False)
        self.source, self.rescan = source, rescan
        self.db_path = db_path if db_path is not None else getattr(parent, 'output_root', None)
        self.setWindowTitle('Report Sections & Outline Map')
        fit_dialog_to_screen(self, target_w=980, target_h=640)

        self._sections_data: list[dict] = []
        sec_combo = getattr(parent, "sector_combo", None)
        parent_sec = sec_combo.currentData() if sec_combo else None
        self.sector = parent_sec or detect_sector_from_path(getattr(source, "path", None))
        self._init_sections_from_source()

        if parent and hasattr(parent, "page_spin"):
            parent.page_spin.valueChanged.connect(self._on_parent_page_changed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        hint = QLabel(
            'Map the major sections of this report manually or from the Table of Contents. '
            'Mapped sections populate the Section Heading dropdown and guide the Questions Ledger.'
        )
        hint.setWordWrap(True)
        hint.setStyleSheet('color: #475569; font-size: 12px;')
        layout.addWidget(hint)

        splitter = QSplitter(self)

        # ---------------- Left Panel: Manual Section Map Builder ----------------
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 8, 0)
        left_layout.setSpacing(6)

        left_title = QLabel('Mapped Major Sections')
        left_title.setStyleSheet('font-weight: bold; font-size: 13px; color: #1e293b;')
        left_layout.addWidget(left_title)

        # Quick Add Row
        add_box = QHBoxLayout()
        add_box.setSpacing(4)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText('Major section heading (e.g. Mineral Resources)')
        self.page_input = QSpinBox()
        self.page_input.setMinimum(1)
        self.page_input.setMaximum(self.source.page_count if self.source else 9999)
        current_page = getattr(getattr(parent, 'page_spin', None), 'value', lambda: 1)()
        self.page_input.setValue(current_page)
        self.page_input.setToolTip('Physical PDF page where this section starts')

        self.add_btn = QPushButton('+ Add')
        self.add_btn.setToolTip('Add section starting at the specified page')
        self.add_btn.clicked.connect(self._on_add_clicked)

        add_box.addWidget(self.title_input, 1)
        add_box.addWidget(QLabel('Page:'))
        add_box.addWidget(self.page_input)
        add_box.addWidget(self.add_btn)
        left_layout.addLayout(add_box)

        # Grab from current canvas selection button
        self.add_from_canvas_btn = QPushButton('Add from selected text on PDF')
        self.add_from_canvas_btn.setToolTip('Uses highlighted canvas text as title and current PDF page as start page.')
        self.add_from_canvas_btn.clicked.connect(self._on_add_from_canvas)
        left_layout.addWidget(self.add_from_canvas_btn)

        # Table of mapped sections
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Section Title', 'Start', 'End'])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        left_layout.addWidget(self.table, 1)

        # Action buttons for left panel
        table_btn_row = QHBoxLayout()
        table_btn_row.setSpacing(6)
        self.remove_btn = QPushButton('Remove selected')
        self.remove_btn.clicked.connect(self._on_remove_clicked)
        self.compare_btn = QPushButton('🔍 Compare with App Scan')
        self.compare_btn.setToolTip('Compare your captured major sections against all app-detected sections in the PDF.')
        self.compare_btn.clicked.connect(self.open_comparison_dialog)
        self.save_map_btn = QPushButton('Save Map & Update Dropdown')
        self.save_map_btn.setObjectName('primary')
        self.save_map_btn.setStyleSheet('font-weight: bold;')
        self.save_map_btn.clicked.connect(self.save_manual_map)

        table_btn_row.addWidget(self.remove_btn)
        table_btn_row.addWidget(self.compare_btn)
        table_btn_row.addStretch(1)
        table_btn_row.addWidget(self.save_map_btn)
        left_layout.addLayout(table_btn_row)

        splitter.addWidget(left_widget)

        # ---------------- Right Panel: Markdown Overview Preview ----------------
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(8, 0, 0, 0)
        right_layout.setSpacing(6)

        right_title = QLabel('Overview Markdown (Included in Prompts)')
        right_title.setStyleSheet('font-weight: bold; font-size: 13px; color: #1e293b;')
        right_layout.addWidget(right_title)

        self.preview = QTextBrowser()
        right_layout.addWidget(self.preview, 1)

        bottom_buttons = QHBoxLayout()
        bottom_buttons.setSpacing(6)
        self.copy_button = QPushButton('Copy overview')
        self.copy_button.clicked.connect(self.copy_overview)
        rescan_button = QPushButton('Rescan (Heuristic)')
        rescan_button.setToolTip('Run automated pattern search (optional fallback).')
        rescan_button.clicked.connect(self.scan_again)
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(self.accept)

        bottom_buttons.addWidget(self.copy_button)
        bottom_buttons.addWidget(rescan_button)
        bottom_buttons.addStretch(1)
        bottom_buttons.addWidget(close_btn)
        right_layout.addLayout(bottom_buttons)

        splitter.addWidget(right_widget)
        splitter.setSizes([480, 500])
        layout.addWidget(splitter, 1)

        self.refresh()

    def _init_sections_from_source(self):
        self._sections_data = []
        if self.source and self.source.report_map:
            for s in self.source.report_map.get('sections', []):
                title = s.get('title', '')
                start_p = s.get('start', {}).get('physical_page', 1)
                sec_id = s.get('section_id')
                if title:
                    self._sections_data.append({'title': title, 'start_page': start_p, 'section_id': sec_id})

    def _update_table(self):
        self._sections_data.sort(key=lambda s: s['start_page'])
        self.table.setRowCount(len(self._sections_data))
        page_count = self.source.page_count if self.source else 9999
        seq_counter = 1
        for row, item in enumerate(self._sections_data):
            existing_id = item.get("section_id")
            if existing_id and "-ins" in existing_id:
                sec_id = existing_id
            else:
                sec_id = f"D{seq_counter:03d}"
                seq_counter += 1
            item['section_id'] = sec_id
            start_p = item['start_page']
            next_start = None
            for next_item in self._sections_data[row + 1:]:
                if next_item['start_page'] > start_p:
                    next_start = next_item['start_page']
                    break
            end_p = (next_start - 1) if next_start is not None else page_count
            end_p = max(start_p, end_p)

            self.table.setItem(row, 0, QTableWidgetItem(sec_id))
            self.table.setItem(row, 1, QTableWidgetItem(item['title']))
            self.table.setItem(row, 2, QTableWidgetItem(f"p. {start_p}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"p. {end_p}"))

    def _on_add_clicked(self):
        title = self.title_input.text().strip()
        p = self.page_input.value()
        if not title:
            QMessageBox.warning(self, "Title Required", "Please enter a major section heading.")
            return
        self._sections_data.append({'title': title, 'start_page': p, 'section_id': None})
        self.title_input.clear()
        self._update_table()

    def _on_parent_page_changed(self, page: int):
        if hasattr(self, "page_input"):
            self.page_input.setValue(page)

    def _on_add_from_canvas(self):
        selected_text = ""
        parent = self.parent()
        if parent and hasattr(parent, "_get_current_selected_text"):
            selected_text = parent._get_current_selected_text()
        current_page = getattr(getattr(parent, "page_spin", None), "value", lambda: 1)()

        if selected_text:
            cleaned = clean_single_line_text(selected_text)
            self._sections_data.append({"title": cleaned, "start_page": current_page, "section_id": None})
            self._update_table()
            if parent and hasattr(parent, "canvas") and hasattr(parent.canvas, "clear_selection"):
                parent.canvas.clear_selection()
            if parent and hasattr(parent, "statusBar"):
                parent.statusBar().showMessage(f"Added section '{cleaned[:40]}' (page {current_page}) to map.")
        else:
            QMessageBox.information(
                self,
                "No Text Selected",
                "Highlight a section heading on the PDF canvas first (press Alt+T for text selection),\n"
                "then click this button to add it to the section map.",
            )

    def closeEvent(self, event):
        parent = self.parent()
        if parent and hasattr(parent, "page_spin"):
            try:
                parent.page_spin.valueChanged.disconnect(self._on_parent_page_changed)
            except (RuntimeError, TypeError):
                pass
        super().closeEvent(event)

    def _on_remove_clicked(self):
        row = self.table.currentRow()
        if 0 <= row < len(self._sections_data):
            self._sections_data.pop(row)
            self._update_table()

    def save_manual_map(self):
        if not self.source:
            return
        if not self._sections_data:
            QMessageBox.warning(self, "No Sections", "Please add at least one section before saving the map.")
            return

        try:
            mapping = build_manual_section_map(self.source, self._sections_data)
            save_map(mapping, cache_root=self.db_path)
            self.source.report_map = mapping
            self.refresh()
            if self.parent() and hasattr(self.parent(), "_refresh_heading_options"):
                self.parent()._refresh_heading_options()
            QMessageBox.information(
                self,
                "Section Map Saved",
                f"Successfully saved {len(mapping['sections'])} major sections to SQLite!\n\n"
                "The Section Heading dropdown in the capture panel has been updated with your sections.",
            )
        except Exception as exc:
            QMessageBox.critical(self, "Error Saving Map", str(exc))

    def refresh(self):
        self._update_table()
        mapping = self.source.report_map if self.source else None
        if mapping and self.sector:
            self.preview.setMarkdown(report_overview(mapping, sector=self.sector))
        elif mapping and not self.sector:
            self.preview.setMarkdown(
                "⚠️ No active sector selected. Please select a Sector in the main window toolbar to preview orientation map."
            )
        else:
            self.preview.setMarkdown("No section map is saved yet. Add major sections on the left and click 'Save Map'.")
        self.copy_button.setEnabled(mapping is not None and bool(self.sector))

    def copy_overview(self):
        if self.source and self.source.report_map and self.sector:
            QApplication.clipboard().setText(report_overview(self.source.report_map, sector=self.sector))

    def scan_again(self):
        self.rescan()
        self._init_sections_from_source()
        self.refresh()
        if self.parent() and hasattr(self.parent(), "_refresh_heading_options"):
            self.parent()._refresh_heading_options()

    def open_comparison_dialog(self):
        if not self.source:
            QMessageBox.warning(self, "No PDF", "Please open a PDF report first.")
            return
        dlg = SectionComparisonDialog(
            source=self.source,
            user_sections=self._sections_data,
            parent=self,
            db_path=self.db_path,
            sector=self.sector,
        )
        if dlg.exec():
            self._update_table()
            self.refresh()
            if getattr(dlg, "auto_captured", False):
                self.close()


class SectionComparisonDialog(QDialog):
    def __init__(self, source, user_sections: list[dict], parent=None, db_path=None, sector=None):
        super().__init__(parent)
        self.source = source
        self.user_sections = user_sections
        self.db_path = db_path
        self.sector = sector
        self.setWindowTitle('Report Sections Alignment & Matching')
        fit_dialog_to_screen(self, target_w=1080, target_h=680)

        self._app_sections = extract_all_app_sections(self.source)
        self._comparison = compare_section_maps(self.user_sections, self._app_sections)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        matched_cnt = len(self._comparison.matched)
        user_only_cnt = len(self._comparison.user_only)
        app_only_cnt = len(self._comparison.app_only)

        self.summary_label = QLabel(
            f"<b>Report Map Comparison:</b> {matched_cnt} matching sections identified | "
            f"{user_only_cnt} analyst custom sections | {app_only_cnt} additional app-discovered sections."
        )
        self.summary_label.setStyleSheet("font-size: 13px; color: #1e293b;")
        layout.addWidget(self.summary_label)

        hint = QLabel(
            "Review how your captured report map aligns with all sections detected by the app. "
            "You can synchronize page boundaries, adopt discovered sections, or auto-capture matching sections."
        )
        hint.setWordWrap(True)
        hint.setStyleSheet("color: #64748b; font-size: 11px;")
        layout.addWidget(hint)

        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(6)
        filter_layout.addWidget(QLabel("Filter View:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            f"All Sections ({matched_cnt + user_only_cnt + app_only_cnt})",
            f"🟢 Matched ({matched_cnt})",
            f"🟡 User-Only ({user_only_cnt})",
            f"🔵 App-Discovered ({app_only_cnt})",
        ])
        self.filter_combo.currentIndexChanged.connect(self._populate_table)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addStretch(1)
        layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Status", "User Section Title", "User Start", "App Detected Title", "App Pages", "Match Note", "Action"
        ])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        for col in (0, 2, 4, 5, 6):
            self.table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table, 1)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-size: 11px; color: #0284c7;")
        layout.addWidget(self.status_label)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.auto_capture_btn = QPushButton("⚡ Auto-Capture Matched Sections")
        self.auto_capture_btn.setObjectName("primary")
        self.auto_capture_btn.setStyleSheet("font-weight: bold; background-color: #0284c7; color: white; padding: 6px 12px;")
        self.auto_capture_btn.setToolTip("Extract and save all matched sections into SQLite without manual bounding box drawing.")
        self.auto_capture_btn.clicked.connect(self._on_auto_capture_clicked)

        self.sync_bounds_btn = QPushButton("Sync Matched Boundaries")
        self.sync_bounds_btn.setToolTip("Update your captured sections with the app's detected end page bounds.")
        self.sync_bounds_btn.clicked.connect(self._on_sync_all_bounds)

        self.add_all_app_btn = QPushButton("Adopt All App Sections")
        self.add_all_app_btn.setToolTip("Add all discovered app sections into your report map.")
        self.add_all_app_btn.clicked.connect(self._on_adopt_all_app_sections)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)

        btn_layout.addWidget(self.auto_capture_btn)
        btn_layout.addWidget(self.sync_bounds_btn)
        btn_layout.addWidget(self.add_all_app_btn)
        btn_layout.addStretch(1)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        self._populate_table()

    def _populate_table(self):
        filter_idx = self.filter_combo.currentIndex()
        rows_data = []

        # 0: All, 1: Matched, 2: User Only, 3: App Only
        if filter_idx in (0, 1):
            for m in self._comparison.matched:
                rows_data.append(('matched', m))
        if filter_idx in (0, 2):
            for u in self._comparison.user_only:
                rows_data.append(('user_only', u))
        if filter_idx in (0, 3):
            for a in self._comparison.app_only:
                rows_data.append(('app_only', a))

        self.table.setRowCount(len(rows_data))
        for row, (kind, item) in enumerate(rows_data):
            if kind == 'matched':
                m = item
                status_item = QTableWidgetItem("🟢 Matched")
                status_item.setToolTip("Matches an app-detected section.")
                u_title = m.user_section.get("title", "")
                u_page = f"p. {m.user_section.get('start_page', '?')}"
                a_title = m.app_section.get("title", "") if m.app_section else ""
                a_st = m.app_section.get("start_page", "?") if m.app_section else "?"
                a_en = m.app_section.get("end_page", "?") if m.app_section else "?"
                a_pages = f"p. {a_st} - p. {a_en}"
                note = f"{m.match_type} ({m.notes})"

                self.table.setItem(row, 0, status_item)
                self.table.setItem(row, 1, QTableWidgetItem(u_title))
                self.table.setItem(row, 2, QTableWidgetItem(u_page))
                self.table.setItem(row, 3, QTableWidgetItem(a_title))
                self.table.setItem(row, 4, QTableWidgetItem(a_pages))
                self.table.setItem(row, 5, QTableWidgetItem(note))

                sync_btn = QPushButton("Sync Bounds")
                sync_btn.setStyleSheet("font-size: 11px; padding: 2px 6px;")
                sync_btn.clicked.connect(lambda _, m=m: self._sync_single_match(m))
                self.table.setCellWidget(row, 6, sync_btn)

            elif kind == 'user_only':
                u = item
                status_item = QTableWidgetItem("🟡 User Only")
                status_item.setToolTip("Section defined by user without corresponding automated scan hit.")
                u_title = u.get("title", "")
                u_page = f"p. {u.get('start_page', '?')}"

                self.table.setItem(row, 0, status_item)
                self.table.setItem(row, 1, QTableWidgetItem(u_title))
                self.table.setItem(row, 2, QTableWidgetItem(u_page))
                self.table.setItem(row, 3, QTableWidgetItem("-"))
                self.table.setItem(row, 4, QTableWidgetItem("-"))
                self.table.setItem(row, 5, QTableWidgetItem("Analyst custom section"))
                self.table.setItem(row, 6, QTableWidgetItem("-"))

            elif kind == 'app_only':
                a = item
                status_item = QTableWidgetItem("🔵 App Discovered")
                status_item.setToolTip("Discovered by the app scanner but not in user's captured map.")
                a_title = a.get("title", "")
                a_st = a.get("start_page", "?")
                a_en = a.get("end_page", "?")
                a_pages = f"p. {a_st} - p. {a_en}"
                note = f"Source: {a.get('source', 'scan')}"

                self.table.setItem(row, 0, status_item)
                self.table.setItem(row, 1, QTableWidgetItem("-"))
                self.table.setItem(row, 2, QTableWidgetItem("-"))
                self.table.setItem(row, 3, QTableWidgetItem(a_title))
                self.table.setItem(row, 4, QTableWidgetItem(a_pages))
                self.table.setItem(row, 5, QTableWidgetItem(note))

                add_btn = QPushButton("+ Add to Map")
                add_btn.setStyleSheet("font-size: 11px; padding: 2px 6px; color: #0369a1;")
                add_btn.clicked.connect(lambda _, a=a: self._adopt_single_app_section(a))
                self.table.setCellWidget(row, 6, add_btn)

    def _sync_single_match(self, match):
        if not match.app_section:
            return
        end_p = match.app_section.get("end_page")
        if end_p is not None:
            match.user_section["end_page"] = end_p
            QMessageBox.information(
                self,
                "Boundaries Synchronized",
                f"Updated '{match.user_section.get('title')}' end page to p. {end_p}."
            )
            self._populate_table()

    def _adopt_single_app_section(self, app_sec: dict):
        title = app_sec.get("title", "")
        start_p = app_sec.get("start_page", 1)
        if not title:
            return
        is_already_present = any(
            u.get("title") == title and abs(int(u.get("start_page", 1)) - int(start_p)) <= 1
            for u in self.user_sections
        )
        if not is_already_present:
            # If same title already exists at a different page, qualify with page number
            display_title = title
            if any(u.get("title") == title for u in self.user_sections):
                display_title = f"{title} (p.{start_p})"
            self.user_sections.append({"title": display_title, "start_page": start_p, "section_id": None})
            self._comparison = compare_section_maps(self.user_sections, self._app_sections)
            self._populate_table()
            QMessageBox.information(self, "Section Added", f"Added '{display_title}' (p. {start_p}) to your section map.")
        else:
            QMessageBox.information(self, "Section Exists", f"'{title}' at page {start_p} is already in your section map.")

    def _on_sync_all_bounds(self):
        count = 0
        for m in self._comparison.matched:
            if m.app_section and m.app_section.get("end_page") is not None:
                m.user_section["end_page"] = m.app_section["end_page"]
                count += 1
        self._populate_table()
        QMessageBox.information(
            self,
            "Boundaries Synchronized",
            f"Synchronized page boundaries for {count} matched sections."
        )

    def _on_adopt_all_app_sections(self):
        added = 0
        for a in self._comparison.app_only:
            title = a.get("title", "")
            start_p = a.get("start_page", 1)
            is_already_present = any(
                u.get("title") == title and abs(int(u.get("start_page", 1)) - int(start_p)) <= 1
                for u in self.user_sections
            )
            if title and not is_already_present:
                display_title = title
                if any(u.get("title") == title for u in self.user_sections):
                    display_title = f"{title} (p.{start_p})"
                self.user_sections.append({"title": display_title, "start_page": start_p, "section_id": None})
                added += 1
        if added > 0:
            self._comparison = compare_section_maps(self.user_sections, self._app_sections)
            self._populate_table()
            QMessageBox.information(self, "Sections Adopted", f"Added {added} app-discovered sections to your map.")
        else:
            QMessageBox.information(self, "No New Sections", "All app sections are already in your map.")

    def _on_auto_capture_clicked(self):
        matched = self._comparison.matched
        if not matched:
            QMessageBox.warning(self, "No Matched Sections", "No matched sections available to auto-capture.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Auto-Capture",
            f"Auto-capture all {len(matched)} matched sections into SQLite?\n\n"
            "This will extract page text and tables for each section automatically without manual cropping.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        self.auto_capture_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, len(matched))
        self.progress_bar.setValue(0)

        success = 0
        errors = []

        for i, m in enumerate(matched):
            u_sec = m.user_section
            a_sec = m.app_section or {}
            title = u_sec.get("title", "")
            start_p = u_sec.get("start_page") or a_sec.get("start_page", 1)
            end_p = u_sec.get("end_page") or a_sec.get("end_page", start_p)

            self.status_label.setText(f"Capturing ({i+1}/{len(matched)}): {title} (p.{start_p}-p.{end_p})...")
            QApplication.processEvents()

            try:
                auto_capture_section(
                    source=self.source,
                    title=title,
                    start_page=start_p,
                    end_page=end_p,
                    sector=self.sector,
                    output_root=self.db_path,
                )
                success += 1
            except Exception as exc:
                errors.append(f"{title}: {exc}")

            self.progress_bar.setValue(i + 1)
            QApplication.processEvents()

        self.auto_capture_btn.setEnabled(True)
        self.status_label.setText(f"Auto-capture complete: {success} sections captured.")

        self.auto_captured = (success > 0)
        if errors:
            QMessageBox.warning(
                self,
                "Auto-Capture Completed with Warnings",
                f"Successfully captured {success} sections.\n\nErrors encountered:\n" + "\n".join(errors[:5]),
            )
        else:
            QMessageBox.information(
                self,
                "Auto-Capture Complete",
                f"Successfully auto-captured {success} major sections directly into SQLite!\n\n"
                f"Auto-queued all {success} sections for sequential DeepSeek processing and questions ledger construction in the background.",
            )

        if success > 0:
            target = self.parent()
            while target and not hasattr(target, "run_all_pending"):
                target = target.parent() if hasattr(target, "parent") else None
            if target and hasattr(target, "run_all_pending"):
                target.run_all_pending()

        self.accept()



class QuestionsLedgerDialog(QDialog):
    def __init__(self, source, parent=None, db_path=None):
        super().__init__(parent)
        self.source = source
        self.db_path = db_path if db_path is not None else getattr(parent, 'output_root', None)
        self.setWindowTitle('Stored verification questions for upcoming sections (SQLite)')
        fit_dialog_to_screen(self, target_w=900, target_h=600)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)
        hint = QLabel(
            'Store open verification questions from the LLM here (saved in SQLite). When you save the next section, '
            'these stored questions are automatically embedded in the prompt so the LLM answers ONLY '
            'the questions relevant to that section and carries the rest forward.'
        )
        hint.setWordWrap(True)
        layout.addWidget(hint)

        top_row = QHBoxLayout()
        self.replace_clip_button = QPushButton('Replace from clipboard && Save')
        self.replace_clip_button.clicked.connect(self.replace_from_clipboard)
        self.append_clip_button = QPushButton('Append from clipboard && Save')
        self.append_clip_button.clicked.connect(self.append_from_clipboard)
        self.clear_button = QPushButton('Clear ledger')
        self.clear_button.clicked.connect(lambda: self.editor.clear())
        top_row.addWidget(self.replace_clip_button)
        top_row.addWidget(self.append_clip_button)
        top_row.addWidget(self.clear_button)
        top_row.addStretch(1)
        layout.addLayout(top_row)

        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText(
            'Paste the "Updated Open Questions Ledger" (or full LLM response) here.\n'
            'Leave empty when capturing the very first section of a report.'
        )
        disk_questions = load_questions_ledger(self.source.sha256, questions_root=self.db_path)
        if disk_questions:
            self.source.questions_ledger = disk_questions
        self.editor.setPlainText(self.source.questions_ledger or '')
        layout.addWidget(self.editor, 1)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.save_and_close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def replace_from_clipboard(self):
        clip = QApplication.clipboard().text().strip()
        if clip:
            extracted = extract_questions_ledger_from_response(clip)
            self.editor.setPlainText(extracted or clip)
            self._persist()

    def append_from_clipboard(self):
        clip = QApplication.clipboard().text().strip()
        if clip:
            current = self.editor.toPlainText().strip()
            combined = (current + '\n\n' + clip).strip() if current else clip
            self.editor.setPlainText(combined)
            self._persist()

    def _persist(self):
        text = self.editor.toPlainText().strip()
        save_questions_ledger(self.source.sha256, text, questions_root=self.db_path)
        self.source.questions_ledger = text

    def save_and_close(self):
        self._persist()
        self.accept()


class SavedSectionsDialog(QDialog):
    def __init__(self, source, parent=None, db_path=None):
        super().__init__(parent)
        self.source = source
        self.db_path = db_path if db_path is not None else getattr(parent, 'output_root', None)
        self.setWindowTitle('Saved sections & LLM responses (SQLite)')
        fit_dialog_to_screen(self, target_w=920, target_h=620)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        section_row = QHBoxLayout()
        section_row.setSpacing(6)
        section_row.addWidget(QLabel('Section:'))
        self.section_combo = QComboBox()
        self.section_combo.currentIndexChanged.connect(self._load_selected_section)
        section_row.addWidget(self.section_combo, 1)
        layout.addLayout(section_row)

        actions_row = QHBoxLayout()
        actions_row.setSpacing(6)
        model_name = get_model_display_name()
        self.run_api_btn = QPushButton('Query Model (OpenRouter)')
        self.run_api_btn.setObjectName("primary")
        self.run_api_btn.setToolTip(f'Send reading prompt directly to {model_name} via OpenRouter API and save response.')
        self.run_api_btn.clicked.connect(self.run_openrouter_for_current)
        self.run_all_btn = QPushButton('Run All Pending')
        self.run_all_btn.setToolTip(f'Sequentially query {model_name} for all sections that do not yet have an LLM response.')
        self.run_all_btn.clicked.connect(self.run_openrouter_for_all_pending)
        self.nitro_checkbox = QCheckBox(":nitro")
        self.nitro_checkbox.setToolTip("Route query via OpenRouter :nitro priority throughput.")
        self.copy_prompt_btn = QPushButton('Copy prompt')
        self.copy_prompt_btn.setToolTip('Copy the formatted reading prompt for this section to clipboard.')
        self.copy_prompt_btn.clicked.connect(self.copy_selected_prompt)
        self.paste_resp_btn = QPushButton('Paste response')
        self.paste_resp_btn.setToolTip('Paste LLM response from clipboard and update the Stored Questions ledger.')
        self.paste_resp_btn.clicked.connect(self.paste_llm_response_from_clipboard)
        self.clear_resp_btn = QPushButton('Clear response')
        self.clear_resp_btn.setToolTip('Clear the stored LLM response for this section so it can be re-run.')
        self.clear_resp_btn.clicked.connect(self.clear_current_response)
        self.audit_btn = QPushButton('Audit & Valuation →')
        self.audit_btn.setToolTip('Proceed to Stage 1 Forensic Audit and Stage 2 Valuation.')
        self.audit_btn.clicked.connect(self.open_audit_valuation)

        actions_row.addWidget(self.run_api_btn)
        actions_row.addWidget(self.run_all_btn)
        actions_row.addWidget(self.nitro_checkbox)
        actions_row.addWidget(self.clear_resp_btn)
        actions_row.addStretch(1)
        actions_row.addWidget(self.audit_btn)
        self.copy_prompt_btn.setVisible(False)
        self.paste_resp_btn.setVisible(False)
        layout.addLayout(actions_row)

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        self.response_edit = QPlainTextEdit()
        self.response_edit.setPlaceholderText(
            'Paste the LLM Markdown reading brief for this section here and click Save.\n'
            'Section 4 (Updated Open Questions Ledger) will automatically update the report\'s Stored Questions ledger.'
        )
        layout.addWidget(self.response_edit, 1)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Close)
        buttons.accepted.connect(self.save_current_response)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.sections = list_sections(self.source.sha256, db_path=self.db_path)
        for sec in self.sections:
            self.section_combo.addItem(self._combo_label(sec), sec.package_id)
        if self.sections:
            self.section_combo.setCurrentIndex(len(self.sections) - 1)
            self._load_selected_section()

    @staticmethod
    def _combo_label(sec) -> str:
        title = f"{sec.heading} — {sec.subheading}" if sec.subheading else sec.heading
        status = "✓ LLM response saved" if sec.llm_response else "pending LLM response"
        return f"{sec.section_number:02d}-{sec.section_id} · {title} ({status})"

    def _current_section(self):
        idx = self.section_combo.currentIndex()
        if 0 <= idx < len(self.sections):
            return self.sections[idx]
        return None

    def _load_selected_section(self):
        sec = self._current_section()
        if not sec:
            self.response_edit.clear()
            self.status_label.setText('No sections saved in SQLite for this report yet.')
            return
        self.response_edit.setPlainText(sec.llm_response or '')
        if sec.llm_response:
            meta = sec.manifest.get("review", {})
            time_s = meta.get("response_time_seconds")
            cost_usd = meta.get("cost_usd")
            tokens = meta.get("tokens", {})
            model = meta.get("model", "")
            model_tag = f" · {model}" if model else ""
            time_info = f" · {time_s:.1f}s" if time_s else ""
            cost_info = f" · ${cost_usd:.4f}" if cost_usd is not None else ""
            tok_info = f" · {tokens.get('total_tokens', 0):,} tok" if tokens and tokens.get("total_tokens") else ""
            self.status_label.setText(
                f"Status: ✓ Response saved{model_tag}{time_info}{cost_info}{tok_info}  ·  Package: {sec.package_id}"
            )
        else:
            self.status_label.setText(
                f"Status: pending LLM response  ·  Package: {sec.package_id}  ·  Section ID: {sec.section_id}  ·  "
                f"Prompt: {len(sec.prompt):,} chars  ·  Selected text: {len(sec.selected_text):,} chars"
            )

    def _refresh_section_prompt_with_current_ledger(self, sec):
        if not self.source:
            return
        current_ledger = (getattr(self.source, "questions_ledger", "") or "").strip() or None
        manifest = copy.deepcopy(sec.manifest)
        manifest["stored_questions"] = current_ledger
        resolved_sector = manifest.get("sector") or detect_sector_from_path(self.source.path)
        manifest["sector"] = resolved_sector
        texts = extract_selection_texts(manifest, selected_text=sec.selected_text, prompt=sec.prompt)
        new_prompt = build_prompt(manifest, texts, sector=resolved_sector)
        if new_prompt != sec.prompt or manifest != sec.manifest:
            with connect_db(self.db_path) as conn:
                conn.execute(
                    "UPDATE sections SET prompt = ?, manifest_json = ? WHERE package_id = ?",
                    (new_prompt, json.dumps(manifest, ensure_ascii=False), sec.package_id),
                )
            sec.prompt = new_prompt
            sec.manifest = manifest

    def copy_selected_prompt(self):
        sec = self._current_section()
        if sec:
            self._refresh_section_prompt_with_current_ledger(sec)
            QApplication.clipboard().setText(sec.prompt)
            self.status_label.setText(f"Copied prompt for {sec.section_number:02d}-{sec.section_id} to clipboard.")

    def clear_current_response(self):
        sec = self._current_section()
        if not sec:
            return
        updated = clear_section_llm_response(sec.package_id, db_path=self.db_path)
        if updated:
            idx = self.section_combo.currentIndex()
            self.sections[idx] = updated
            self.section_combo.setItemText(idx, self._combo_label(updated))
            self.response_edit.clear()
            self.status_label.setText(
                f"✓ Cleared LLM response for {updated.section_number:02d}-{updated.section_id}. Ready to resubmit."
            )
            if self.parent() is not None and hasattr(self.parent(), "_update_actions"):
                self.parent()._update_actions()

    def open_audit_valuation(self):
        from .audit_dialog import AuditValuationDialog
        self.accept()
        AuditValuationDialog(self.source, parent=self.parent(), db_path=self.db_path).exec()

    def paste_llm_response_from_clipboard(self):
        clip = QApplication.clipboard().text().strip()
        if clip:
            self.response_edit.setPlainText(clip)
            self.save_current_response()

    def save_current_response(
        self,
        response_time_seconds: float | None = None,
        cost_usd: float | None = None,
        tokens: dict | None = None,
        model: str | None = None,
    ):
        sec = self._current_section()
        if not sec:
            return
        cleaned = self.response_edit.toPlainText().strip()
        if not cleaned:
            self.status_label.setText("Response text is empty; not saving.")
            return
        updated, extracted = save_section_llm_response(
            sec.package_id,
            cleaned,
            update_ledger=True,
            response_time_seconds=response_time_seconds,
            cost_usd=cost_usd,
            tokens=tokens,
            model=model,
            db_path=self.db_path,
        )
        if updated:
            idx = self.section_combo.currentIndex()
            self.sections[idx] = updated
            self.section_combo.setItemText(idx, self._combo_label(updated))
            time_str = f" in {response_time_seconds:.1f}s" if response_time_seconds else ""
            cost_str = f" (${cost_usd:.4f})" if cost_usd is not None else ""
            chars_str = f" ({len(self.response_edit.toPlainText()):,} chars)"
            if extracted:
                self.source.questions_ledger = extracted
                self.status_label.setText(
                    f"✓ Saved LLM response{time_str}{cost_str}{chars_str} for {updated.section_number:02d}-{updated.section_id} and updated Stored Questions ledger in SQLite."
                )
            else:
                self.status_label.setText(f"✓ Saved LLM response{time_str}{cost_str}{chars_str} for {updated.section_number:02d}-{updated.section_id} in SQLite.")
            if self.parent() is not None and hasattr(self.parent(), "_update_actions"):
                self.parent()._update_actions()

    def run_openrouter_for_current(self):
        sec = self._current_section()
        if not sec:
            return
        self._refresh_section_prompt_with_current_ledger(sec)
        if not sec.prompt:
            self.status_label.setText("No prompt available for the selected section.")
            return
        if hasattr(self, "_active_worker") and self._active_worker and self._active_worker.isRunning():
            self.status_label.setText("A query is already in progress...")
            return

        base_model = get_openrouter_model()
        model = f"{base_model}:nitro" if self.nitro_checkbox.isChecked() else base_model
        model_tag = get_model_short_tag(model)
        self.status_label.setText(f"Querying {model_tag} via OpenRouter for {sec.section_number:02d}-{sec.section_id}...")
        self.run_api_btn.setEnabled(False)

        worker = OpenRouterWorker(sec.prompt, model=model, parent=self)
        self._active_worker = worker

        def on_finished(response_text: str, elapsed: float = 0.0, stats: dict | None = None):
            stats = stats or {}
            cleaned = (response_text or "").strip()
            if not cleaned:
                self.status_label.setText("Model returned an empty response. Not saved.")
                self.run_api_btn.setEnabled(True)
                self._active_worker = None
                return
            cost_usd = stats.get("cost_usd")
            tokens = {
                "prompt_tokens": stats.get("prompt_tokens"),
                "completion_tokens": stats.get("completion_tokens"),
                "total_tokens": stats.get("total_tokens"),
            }
            self.response_edit.setPlainText(cleaned)
            self.save_current_response(
                response_time_seconds=elapsed,
                cost_usd=cost_usd,
                tokens=tokens,
                model=model,
            )
            self.run_api_btn.setEnabled(True)
            self._active_worker = None

        def on_error(err_msg: str):
            self.status_label.setText(f"Query failed: {err_msg}")
            self.run_api_btn.setEnabled(True)
            self._active_worker = None
            QMessageBox.critical(
                self,
                "OpenRouter Query Failed",
                f"The model query failed:\n{err_msg}\n\nCheck your OpenRouter key and connectivity, then retry.",
            )

        worker.finished_query.connect(on_finished)
        worker.error_query.connect(on_error)
        worker.start()

    def run_openrouter_for_all_pending(self):
        if hasattr(self, "_active_worker") and self._active_worker and self._active_worker.isRunning():
            self.status_label.setText("A query is already in progress...")
            return

        pending_indices = [
            i for i, s in enumerate(self.sections)
            if not s.llm_response or not s.llm_response.strip()
        ]
        if not pending_indices:
            self.status_label.setText("✓ All sections already have saved LLM responses.")
            return

        self._pending_queue = pending_indices
        self._total_pending_count = len(pending_indices)
        self.run_api_btn.setEnabled(False)
        self.run_all_btn.setEnabled(False)
        self._process_next_pending()

    def _process_next_pending(self):
        if not hasattr(self, "_pending_queue") or not self._pending_queue:
            self.run_api_btn.setEnabled(True)
            self.run_all_btn.setEnabled(True)
            self._active_worker = None
            self.status_label.setText("✓ Finished processing all pending sections!")
            return

        target_idx = self._pending_queue.pop(0)
        self.section_combo.setCurrentIndex(target_idx)
        sec = self.sections[target_idx]
        self._refresh_section_prompt_with_current_ledger(sec)
        if not sec.prompt:
            self._process_next_pending()
            return

        base_model = get_openrouter_model()
        model = f"{base_model}:nitro" if self.nitro_checkbox.isChecked() else base_model
        model_tag = get_model_short_tag(model)
        completed = self._total_pending_count - len(self._pending_queue)
        self.status_label.setText(
            f"[{completed}/{self._total_pending_count}] Querying {model_tag} for Section {sec.section_number:02d}: {sec.heading}..."
        )

        worker = OpenRouterWorker(sec.prompt, model=model, parent=self)
        self._active_worker = worker

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
                self.response_edit.setPlainText(cleaned)
                self.save_current_response(
                    response_time_seconds=elapsed,
                    cost_usd=cost_usd,
                    tokens=tokens,
                    model=model,
                )
            self._process_next_pending()

        def on_error(err_msg: str):
            self.run_api_btn.setEnabled(True)
            self.run_all_btn.setEnabled(True)
            self._active_worker = None
            self.status_label.setText(f"Batch query stopped: {err_msg}")
            QMessageBox.critical(
                self,
                "OpenRouter Query Failed",
                f"Model query failed on Section {sec.section_number:02d} ({sec.heading}):\n{err_msg}\n\nCheck your OpenRouter key and connectivity, then retry.",
            )

        worker.finished_query.connect(on_finished)
        worker.error_query.connect(on_error)
        worker.start()

    def reject(self):
        if hasattr(self, "_pending_queue"):
            self._pending_queue.clear()
        if hasattr(self, "_active_worker") and self._active_worker:
            try:
                self._active_worker.finished_query.disconnect()
                self._active_worker.error_query.disconnect()
            except Exception:
                pass
            self._active_worker.quit()
        super().reject()

    def closeEvent(self, event):
        if hasattr(self, "_pending_queue"):
            self._pending_queue.clear()
        if hasattr(self, "_active_worker") and self._active_worker:
            try:
                self._active_worker.finished_query.disconnect()
                self._active_worker.error_query.disconnect()
            except Exception:
                pass
            self._active_worker.quit()
        super().closeEvent(event)
