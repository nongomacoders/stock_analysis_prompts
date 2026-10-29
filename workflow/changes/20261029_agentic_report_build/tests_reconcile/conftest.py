"""pytest configuration and fixtures for the P2 reconciliation suite.

Fixtures provide read-only access to the committed `report.sqlite` database
and instantiate the reconciliation engine.
"""
from __future__ import annotations

import pathlib
import sqlite3
import pytest
from reconcile_engine import Engine

DB_REL_PATH = pathlib.Path(__file__).resolve().parent.parent / "build" / "report.sqlite"


@pytest.fixture(scope="session")
def report_db_path():
    assert DB_REL_PATH.is_file(), f"report.sqlite not found at {DB_REL_PATH}"
    return str(DB_REL_PATH)


@pytest.fixture(scope="session")
def report_db(report_db_path):
    con = sqlite3.connect(f"file:{report_db_path}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    try:
        yield con
    finally:
        con.close()


@pytest.fixture(scope="session")
def engine(report_db_path):
    return Engine(report_db_path)
