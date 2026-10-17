import argparse
import sys
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

from .window import CaptureWindow


STYLE = """
QMainWindow, QWidget { background: #f7f9fc; color: #182c40; }
QToolBar { padding: 9px; spacing: 7px; background: white; border-bottom: 1px solid #dce3eb; }
QPushButton { padding: 8px 11px; background: white; border: 1px solid #c8d4df; border-radius: 5px; }
QPushButton:hover { border-color: #087e8b; background: #eef8f9; }
QPushButton:disabled { color: #8b99a8; background: #edf1f5; border-color: #dce3eb; }
QPushButton#primary { background: #087e8b; color: white; border: none; padding: 12px; font-weight: 600; }
QPushButton#primary:disabled { background: #b9d1d4; }
QLineEdit, QPlainTextEdit, QListWidget, QSpinBox, QComboBox { background: white; border: 1px solid #cbd6e2; border-radius: 4px; padding: 6px; }
QLabel#documentTitle { font-size: 17px; font-weight: 600; padding-bottom: 4px; }
QLabel#sectionTitle { font-size: 21px; font-weight: 600; padding: 7px 0; }
QLabel#muted { color: #64768a; font-size: 12px; padding-bottom: 8px; }
QLabel#warning { color: #89520a; font-size: 12px; }
QStatusBar { background: #eaf0f6; padding: 4px; }
"""


def apply_theme(app):
    # Restricted/offscreen Windows sessions sometimes cannot enumerate the
    # registry font catalogue. Load installed system fonts directly as fallback.
    if not QFontDatabase.families():
        for name in ("segoeui.ttf", "seguisb.ttf"):
            path = Path("C:/Windows/Fonts") / name
            if path.exists():
                QFontDatabase.addApplicationFont(str(path))
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(STYLE)


def main():
    parser = argparse.ArgumentParser(description="Select PDF evidence and save an LLM upload pack.")
    parser.add_argument("pdf", nargs="?", help="Optional PDF to open")
    parser.add_argument("--output", type=Path, help="Folder for saved section packs")
    args = parser.parse_args()
    app = QApplication(sys.argv[:1])
    app.setApplicationName("Report Section Capture")
    apply_theme(app)
    window = CaptureWindow(args.output)
    screen = app.primaryScreen()
    if screen:
        available = screen.availableGeometry()
        window.resize(min(1440, available.width() - 50), min(940, available.height() - 60))
    window.show()
    if args.pdf:
        QTimer.singleShot(0, lambda: window.open_pdf(args.pdf))
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
