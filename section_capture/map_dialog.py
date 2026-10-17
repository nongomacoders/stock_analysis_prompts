"""Read-only draft overview and editable stored-questions ledger dialog."""
from PySide6.QtWidgets import (
    QApplication, QDialog, QDialogButtonBox, QHBoxLayout, QLabel,
    QPlainTextEdit, QPushButton, QTextBrowser, QVBoxLayout,
)

from .report_map import report_overview, save_questions_ledger


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
    def __init__(self, source, parent=None):
        super().__init__(parent)
        self.source = source
        self.setWindowTitle('Stored verification questions for upcoming sections')
        self.resize(980, 680)
        layout = QVBoxLayout(self)
        hint = QLabel(
            'Store open verification questions from the LLM here. When you save the next section, '
            'these stored questions are automatically embedded in prompt.md so the LLM answers ONLY '
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
            'Paste the "Updated Open Questions Ledger" from your LLM response here.\n'
            'Leave empty when capturing the very first section of a report.'
        )
        self.editor.setPlainText(self.source.questions_ledger or '')
        layout.addWidget(self.editor, 1)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.save_and_close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def replace_from_clipboard(self):
        clip = QApplication.clipboard().text().strip()
        if clip:
            self.editor.setPlainText(clip)
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
        save_questions_ledger(self.source.sha256, text)
        self.source.questions_ledger = text

    def save_and_close(self):
        self._persist()
        self.accept()
