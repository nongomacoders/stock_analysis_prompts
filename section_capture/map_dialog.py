"""Read-only draft overview; map edits/review are not financial confirmations."""
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QLabel, QTextBrowser, QVBoxLayout

from .report_map import report_overview


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
