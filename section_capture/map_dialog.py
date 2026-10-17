"""Read-only draft overview, stored-questions ledger, and saved-sections / LLM-response dialogs."""
from PySide6.QtWidgets import (
    QApplication, QComboBox, QDialog, QDialogButtonBox, QHBoxLayout, QLabel,
    QPlainTextEdit, QPushButton, QTextBrowser, QVBoxLayout,
)

from .db import extract_questions_ledger_from_response, list_sections, save_section_llm_response
from .report_map import load_questions_ledger, report_overview, save_questions_ledger


class ReportMapDialog(QDialog):
    def __init__(self, source, rescan, parent=None):
        super().__init__(parent)
        self.source, self.rescan = source, rescan
        self.setWindowTitle('Report sections — draft scan')
        self.resize(1050, 730)
        layout = QVBoxLayout(self)
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
        self.resize(980, 680)
        layout = QVBoxLayout(self)
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
        self.resize(1040, 740)
        layout = QVBoxLayout(self)

        top = QHBoxLayout()
        top.addWidget(QLabel('Section:'))
        self.section_combo = QComboBox()
        self.section_combo.currentIndexChanged.connect(self._load_selected_section)
        top.addWidget(self.section_combo, 1)
        self.copy_prompt_btn = QPushButton('Copy prompt')
        self.copy_prompt_btn.clicked.connect(self.copy_selected_prompt)
        self.paste_resp_btn = QPushButton('Paste LLM response && Update questions')
        self.paste_resp_btn.clicked.connect(self.paste_llm_response_from_clipboard)
        top.addWidget(self.copy_prompt_btn)
        top.addWidget(self.paste_resp_btn)
        layout.addLayout(top)

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
            title = f"{sec.heading} — {sec.subheading}" if sec.subheading else sec.heading
            status = "✓ LLM response saved" if sec.llm_response else "pending LLM response"
            self.section_combo.addItem(f"{sec.section_number:02d}-{sec.section_id} · {title} ({status})", sec.package_id)
        if self.sections:
            self.section_combo.setCurrentIndex(len(self.sections) - 1)
            self._load_selected_section()

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
        self.status_label.setText(
            f"Package: {sec.package_id}  ·  Section ID: {sec.section_id}  ·  "
            f"Prompt: {len(sec.prompt):,} chars  ·  Selected text: {len(sec.selected_text):,} chars"
        )

    def copy_selected_prompt(self):
        sec = self._current_section()
        if sec:
            QApplication.clipboard().setText(sec.prompt)
            self.status_label.setText(f"Copied prompt for {sec.section_number:02d}-{sec.section_id} to clipboard.")

    def paste_llm_response_from_clipboard(self):
        clip = QApplication.clipboard().text().strip()
        if clip:
            self.response_edit.setPlainText(clip)
            self.save_current_response()

    def save_current_response(self):
        sec = self._current_section()
        if not sec:
            return
        updated, extracted = save_section_llm_response(
            sec.package_id,
            self.response_edit.toPlainText(),
            update_ledger=True,
            db_path=self.db_path,
        )
        if updated:
            idx = self.section_combo.currentIndex()
            self.sections[idx] = updated
            if extracted:
                self.source.questions_ledger = extracted
                self.status_label.setText(
                    f"Saved LLM response for {updated.section_number:02d}-{updated.section_id} and updated Stored Questions ledger in SQLite."
                )
            else:
                self.status_label.setText(f"Saved LLM response for {updated.section_number:02d}-{updated.section_id} in SQLite.")

