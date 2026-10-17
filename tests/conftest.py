import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtCore import QCoreApplication, QEvent
from PySide6.QtWidgets import QApplication

from section_capture.pdf_source import PdfSource
from section_capture.__main__ import apply_theme


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance() or QApplication([])
    apply_theme(app)
    yield app
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    app.processEvents()


@pytest.fixture(autouse=True)
def clean_windows(qapp):
    yield
    for window in QApplication.topLevelWidgets():
        window.hide()
        # Tests explicitly save/reset drafts before closing to avoid a modal.
        window.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    qapp.processEvents()


@pytest.fixture
def pdf_path():
    return Path(__file__).resolve().parents[1] / "company_results/PAN/FY-2026/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf"


@pytest.fixture
def source(qapp, pdf_path):
    opened = PdfSource(pdf_path)
    yield opened
    opened.close()
