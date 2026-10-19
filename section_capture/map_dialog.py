"""Read-only draft overview, stored-questions ledger, and saved-sections / LLM-response dialogs."""
import copy
import json

from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDialog, QDialogButtonBox, QHBoxLayout, QLabel,
    QPlainTextEdit, QPushButton, QTextBrowser, QVBoxLayout,
)

from .db import (
    clear_section_llm_response,
    connect_db,
    extract_questions_ledger_from_response,
    list_sections,
    save_section_llm_response,
)
from .openrouter import OpenRouterWorker, get_openrouter_model
from .packages import build_prompt, detect_sector_from_path
from .report_map import load_questions_ledger, report_overview, save_questions_ledger


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
    def __init__(self, source, rescan, parent=None):
        super().__init__(parent)
        self.source, self.rescan = source, rescan
        self.setWindowTitle('Report sections — draft scan')
        fit_dialog_to_screen(self, target_w=920, target_h=620)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)
        hint = QLabel('Copy this overview into your model chat first. New reading prompts also include it. '
                      'Check draft boundaries; the scan does not read or verify the section contents.')
        hint.setWordWrap(True)
        layout.addWidget(hint)
        self.preview = QTextBrowser()
        layout.addWidget(self.preview)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        self.copy_button = buttons.addButton('Copy overview', QDialogButtonBox.ButtonRole.ActionRole)
        self.copy_button.clicked.connect(self.copy_overview)
        rescan_button = buttons.addButton('Rescan', QDialogButtonBox.ButtonRole.ActionRole)
        rescan_button.clicked.connect(self.scan_again)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.refresh()

    def refresh(self):
        mapping = self.source.report_map
        self.preview.setMarkdown(report_overview(mapping) if mapping else 'No section map is available. Rescan to look for major native-text headings.')
        self.copy_button.setEnabled(mapping is not None)

    def copy_overview(self):
        if self.source.report_map:
            QApplication.clipboard().setText(report_overview(self.source.report_map))

    def scan_again(self):
        self.rescan()
        self.refresh()


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

        worker.finished_query.connect(on_finished)
        worker.error_query.connect(on_error)
        worker.start()



