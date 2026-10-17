import copy
import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtCore import QCoreApplication, QEvent
from PySide6.QtWidgets import QApplication

import section_capture.db as db_mod
import section_capture.report_map as report_map_mod
from section_capture.pdf_source import PdfSource
from section_capture.report_map import save_map, save_questions_ledger, scan_report
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
    cache_dir = tmp_path_factory.mktemp("sqlite-cache")
    db_path = cache_dir / "analysis.sqlite"
    original_db = db_mod.DB_PATH
    original_cache = report_map_mod.CACHE_ROOT
    original_questions = report_map_mod.QUESTIONS_ROOT
    db_mod.DB_PATH = db_path
    report_map_mod.CACHE_ROOT = db_path
    report_map_mod.QUESTIONS_ROOT = db_path
    opened = PdfSource(pdf_path)
    try:
        base_map = scan_report(opened)
        save_map(base_map, db_path)
        sha256 = opened.sha256
    finally:
        opened.close()
    yield db_path, sha256, base_map
    db_mod.DB_PATH = original_db
    report_map_mod.CACHE_ROOT = original_cache
    report_map_mod.QUESTIONS_ROOT = original_questions


@pytest.fixture(autouse=True)
def clean_windows(qapp, isolated_map_cache):
    db_path, sha256, base_map = isolated_map_cache
    with db_mod.connect_db(db_path) as conn:
        conn.execute("DELETE FROM sections")
    save_map(copy.deepcopy(base_map), db_path)
    save_questions_ledger(sha256, "", db_path)
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

