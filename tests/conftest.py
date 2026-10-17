import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtCore import QCoreApplication, QEvent
from PySide6.QtWidgets import QApplication

import section_capture.report_map as report_map_mod
from section_capture.pdf_source import PdfSource
from section_capture.report_map import save_map, scan_report
from section_capture.__main__ import apply_theme


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance() or QApplication([])
    apply_theme(app)
    yield app
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    app.processEvents()


@pytest.fixture(scope="session")
def pdf_path():
    return Path(__file__).resolve().parents[1] / "company_results/PAN/FY-2026/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf"


@pytest.fixture(scope="session", autouse=True)
def isolated_map_cache(qapp, pdf_path, tmp_path_factory):
    cache_dir = tmp_path_factory.mktemp("map-cache")
    questions_dir = tmp_path_factory.mktemp("questions-cache")
    original_cache = report_map_mod.CACHE_ROOT
    original_questions = report_map_mod.QUESTIONS_ROOT
    report_map_mod.CACHE_ROOT = cache_dir
    report_map_mod.QUESTIONS_ROOT = questions_dir
    opened = PdfSource(pdf_path)
    try:
        mapping = scan_report(opened)
        save_map(mapping, cache_dir)
    finally:
        opened.close()
    yield cache_dir
    report_map_mod.CACHE_ROOT = original_cache
    report_map_mod.QUESTIONS_ROOT = original_questions


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
def source(qapp, pdf_path):
    opened = PdfSource(pdf_path)
    opened.questions_ledger = ""
    yield opened
    opened.close()
