import argparse
import sys
from pathlib import Path

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

from .window import CaptureWindow


STYLE = """
QMainWindow, QWidget { background: #f7f9fc; color: #182c40; }
QToolBar { padding: 6px; spacing: 6px; background: white; border-bottom: 1px solid #dce3eb; }
QPushButton { padding: 6px 10px; background: white; border: 1px solid #c8d4df; border-radius: 5px; }
QPushButton:hover { border-color: #087e8b; background: #eef8f9; }
QPushButton:disabled { color: #8b99a8; background: #edf1f5; border-color: #dce3eb; }
QPushButton#primary { background: #087e8b; color: white; border: none; padding: 9px 12px; font-weight: 600; }
QPushButton#primary:disabled { background: #b9d1d4; }
QLineEdit, QPlainTextEdit, QListWidget, QSpinBox, QComboBox { background: white; border: 1px solid #cbd6e2; border-radius: 4px; padding: 5px; }
QLabel#documentTitle { font-size: 16px; font-weight: 600; padding-bottom: 2px; }
QLabel#sectionTitle { font-size: 18px; font-weight: 600; padding: 2px 0 4px 0; }
QLabel#muted { color: #64768a; font-size: 11px; padding-bottom: 4px; }
QLabel#warning { color: #89520a; font-size: 12px; font-weight: 500; }
QStatusBar { background: #eaf0f6; padding: 4px; }
"""


def apply_theme(app):
    if not QFontDatabase.families():
        for name in ("segoeui.ttf", "seguisb.ttf"):
            path = Path("C:/Windows/Fonts") / name
            if path.exists():
                QFontDatabase.addApplicationFont(str(path))
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(STYLE)


def main():
    parser = argparse.ArgumentParser(description="Autonomous Equity Research Pipeline.")
    parser.add_argument("--output", type=Path, help="Folder for SQLite database")
    args = parser.parse_args()
    app = QApplication(sys.argv[:1])
    app.setApplicationName("Equity Research — Autonomous Pipeline")
    apply_theme(app)
    window = CaptureWindow(args.output)
    screen = app.primaryScreen()
    if screen:
        available = screen.availableGeometry()
        window.resize(min(1440, available.width() - 50), min(940, available.height() - 60))
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
