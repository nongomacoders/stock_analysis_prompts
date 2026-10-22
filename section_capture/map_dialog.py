"""Read-only draft overview, stored-questions ledger, and saved-sections / LLM-response dialogs."""
import copy
import json

from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFrame, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMessageBox, QPlainTextEdit, QPushButton, QSpinBox, QSplitter, QTableWidget, QTableWidgetItem, QTextBrowser, QVBoxLayout, QWidget,
)

from .db import (
    clear_section_llm_response,
    connect_db,
    extract_questions_ledger_from_response,
    list_sections,
    save_section_llm_response,
)
from .openrouter import OpenRouterWorker, get_openrouter_model
from .packages import build_prompt, clean_single_line_text, detect_sector_from_path
from .report_map import assign_section_ids, build_manual_section_map, load_questions_ledger, report_overview, save_map, save_questions_ledger


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
        self.save_map_btn = QPushButton('Save Map & Update Dropdown')
        self.save_map_btn.setObjectName('primary')
        self.save_map_btn.setStyleSheet('font-weight: bold;')
        self.save_map_btn.clicked.connect(self.save_manual_map)

        table_btn_row.addWidget(self.remove_btn)
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
        self.preview.setMarkdown(
            report_overview(mapping) if mapping else "No section map is saved yet. Add major sections on the left and click 'Save Map'."
        )
        self.copy_button.setEnabled(mapping is not None)

    def copy_overview(self):
        if self.source and self.source.report_map:
            QApplication.clipboard().setText(report_overview(self.source.report_map))

    def scan_again(self):
        self.rescan()
        self._init_sections_from_source()
        self.refresh()
        if self.parent() and hasattr(self.parent(), "_refresh_heading_options"):
            self.parent()._refresh_heading_options()


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
        self.run_api_btn = QPushButton('Query Model (OpenRouter)')
        self.run_api_btn.setObjectName("primary")
        self.run_api_btn.setToolTip('Send reading prompt directly to DeepSeek via OpenRouter API and save response.')
        self.run_api_btn.clicked.connect(self.run_openrouter_for_current)
        self.run_all_btn = QPushButton('Run All Pending')
        self.run_all_btn.setToolTip('Sequentially query DeepSeek for all sections that do not yet have an LLM response.')
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
        actions_row.addWidget(self.copy_prompt_btn)
        actions_row.addWidget(self.paste_resp_btn)
        actions_row.addWidget(self.clear_resp_btn)
        actions_row.addStretch(1)
        actions_row.addWidget(self.audit_btn)
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
        texts = [s.get("text", "") for s in sec.selections]
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
        model_tag = "DeepSeek:nitro" if ":nitro" in model else "DeepSeek"
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
        model_tag = "DeepSeek:nitro" if ":nitro" in model else "DeepSeek"
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
