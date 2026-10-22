"""Tests for multi-document report suites (IAR & AFS linkage, citations, and export)."""
from __future__ import annotations

import sqlite3
from pathlib import Path
import pytest

from section_capture.db import (
    DOC_TYPES,
    auto_link_companion_reports,
    connect_db,
    detect_doc_type_and_date,
    get_doc_badge,
    get_doc_code,
    get_questions_ledger,
    save_section_llm_response,
    set_report_doc_type,
    upsert_report,
)


def test_doc_types_and_codes():
    assert get_doc_code("iar") == "IAR"
    assert get_doc_code("afs") == "AFS"
    assert get_doc_code("presentation") == "PRES"
    assert get_doc_code("sens") == "SENS"
    assert get_doc_code("annual_report") == "AR"
    assert get_doc_code(None) == "AR"

    assert get_doc_badge("iar") == "[IAR]"
    assert get_doc_badge("afs") == "[AFS]"
    assert get_doc_badge("sens", "2026-09-30") == "[SENS 2026-09-30]"


def test_detect_doc_type_and_date():
    assert detect_doc_type_and_date("ioco_integrated_annual_report_2026.pdf")[0] == "iar"
    assert detect_doc_type_and_date("iOCO_IAR_2026.pdf")[0] == "iar"
    assert detect_doc_type_and_date("ioco_afs_2026.pdf")[0] == "afs"
    assert detect_doc_type_and_date("ioco_annual_financial_statements_2026.pdf")[0] == "afs"
    assert detect_doc_type_and_date("ioco_results_presentation_2026.pdf")[0] == "presentation"
    assert detect_doc_type_and_date("sources/sens/20260930_trading_update.pdf")[0] == "sens"
    assert detect_doc_type_and_date("general_annual_report.pdf")[0] == "annual_report"


def test_companion_linking_and_ledger_sync(tmp_path):
    db_file = tmp_path / "test_analysis.sqlite"
    iar_sha = "a" * 64
    afs_sha = "b" * 64

    iar_path = tmp_path / "companies/it/IOC/sources/iOCO_IAR_2026.pdf"
    afs_path = tmp_path / "companies/it/IOC/sources/iOCO_AFS_2026.pdf"
    iar_path.parent.mkdir(parents=True, exist_ok=True)
    iar_path.write_text("dummy iar", encoding="utf-8")
    afs_path.write_text("dummy afs", encoding="utf-8")

    # 1. Upsert IAR with initial questions ledger
    upsert_report(
        sha256=iar_sha,
        filename=iar_path.name,
        original_path=str(iar_path),
        physical_page_count=100,
        doc_type="iar",
        questions_ledger="Initial IAR questions ledger: verify contract assets.",
        db_path=db_file,
    )

    # 2. Upsert AFS (initially without questions ledger)
    upsert_report(
        sha256=afs_sha,
        filename=afs_path.name,
        original_path=str(afs_path),
        physical_page_count=80,
        doc_type="afs",
        db_path=db_file,
    )

    # 3. Auto-link companion reports
    parent_sha = auto_link_companion_reports(afs_sha, afs_path, doc_type="afs", db_path=db_file)
    assert parent_sha == iar_sha

    # Verify AFS is linked and inherited IAR questions ledger
    with connect_db(db_file) as conn:
        row = conn.execute("SELECT parent_report_sha256, questions_ledger FROM reports WHERE sha256 = ?", (afs_sha,)).fetchone()
        assert row["parent_report_sha256"] == iar_sha
        assert "Initial IAR questions ledger" in row["questions_ledger"]

    # 4. Update questions ledger via set_report_doc_type
    set_report_doc_type(afs_sha, "afs", db_path=db_file)
    with connect_db(db_file) as conn:
        row = conn.execute("SELECT doc_type FROM reports WHERE sha256 = ?", (afs_sha,)).fetchone()
        assert row["doc_type"] == "afs"


def test_export_stage1_multi_document_prompt(tmp_path):
    from workflow.export_stage1 import build_stage1_prompt_content

    iar_sections = [
        {
            "section_number": 1,
            "section_id": "D001",
            "heading": "CEO Strategic Review",
            "subheading": "ARR and Cloud Inflection",
            "analyst_question": "Scrutinize ARR growth vs WIP.",
            "selected_text": "--- Section D001 | [IAR] physical page 12 | text selection | commentary ---\nARR grew 18%.",
            "stored_questions_snapshot": "Pending: [AFS Note 12 - Contract Assets on physical p. 42]",
            "llm_response": "ARR verified at 18%, but unbilled contract assets must be checked in AFS.",
        }
    ]

    afs_sections = [
        {
            "section_number": 2,
            "section_id": "D005",
            "heading": "Note 12: Contract Assets and Liabilities",
            "subheading": "Unbilled Receivables",
            "analyst_question": "Verify unbilled contract assets.",
            "selected_text": "--- Section D005 | [AFS] physical page 42 | table selection | financial_note ---\nContract assets R184m.",
            "stored_questions_snapshot": "",
            "llm_response": "Contract assets decreased from R210m to R184m, confirming cash conversion.",
        }
    ]

    companion_reports = [
        {
            "sha256": "b" * 64,
            "filename": "iOCO_AFS_2026.pdf",
            "doc_type": "afs",
            "sections": afs_sections,
        }
    ]

    prompt = build_stage1_prompt_content(
        sections=iar_sections,
        company_title="iOCO Limited",
        ticker="IOC",
        detected_sector="it",
        filename="iOCO_IAR_2026.pdf",
        companion_reports=companion_reports,
    )

    assert "`iOCO_IAR_2026.pdf` (Integrated Annual Report [IAR]" in prompt
    assert "`iOCO_AFS_2026.pdf` (AFS" in prompt
    assert "PART 1: PRIMARY FINANCIAL DISCLOSURE (`iOCO_IAR_2026.pdf`" in prompt
    assert "PART 2: AFS FINANCIAL STATEMENTS & NOTES (`iOCO_AFS_2026.pdf`" in prompt
    assert "[IAR] physical page 12" in prompt
    assert "[AFS] physical page 42" in prompt
