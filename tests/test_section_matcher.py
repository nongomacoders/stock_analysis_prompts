import pytest
from pathlib import Path
from PySide6.QtWidgets import QApplication
from section_capture.section_matcher import (
    _normalize_title,
    _token_similarity,
    compare_section_maps,
    extract_all_app_sections,
    SectionMatch,
    SectionComparisonResult,
)
from section_capture.pdf_source import PdfSource
from section_capture.map_dialog import SectionComparisonDialog, ReportMapDialog


def test_normalize_title():
    assert _normalize_title("D002 - Highlights") == "highlights"
    assert _normalize_title("S005: Primary Financial Statements") == "primary financial statements"
    assert _normalize_title("CEO's Statement & Review") == "chief executive statement review"
    assert _normalize_title("Our Portfolio of Assets") == "portfolio assets"
    assert _normalize_title("Note 12: Long-Term Debt") == "long term debt"


def test_token_similarity():
    # Identical
    assert _token_similarity("chief executive officer review", "chief executive officer review") == 1.0
    # Overlapping with synonym expansion
    sim = _token_similarity("chief executive review", "chief executive statement review")
    assert sim >= 0.75
    # Token subset containment
    assert _token_similarity("financial notes", "notes financial statements") >= 0.85


def test_compare_section_maps_exact_and_fuzzy():
    user_sections = [
        {"title": "Highlights", "start_page": 2},
        {"title": "CEO Statement", "start_page": 5},
        {"title": "Financial Statements", "start_page": 17},
        {"title": "Custom Valuation Model Notes", "start_page": 50},  # User only
    ]

    app_sections = [
        {"title": "Unclassified Cover", "start_page": 1, "end_page": 1},
        {"title": "Key Highlights", "start_page": 2, "end_page": 4},
        {"title": "Chief Executive's Review", "start_page": 5, "end_page": 15},
        {"title": "Primary Financial Statements", "start_page": 17, "end_page": 19},
        {"title": "Financial Notes", "start_page": 19, "end_page": 36},  # App only
        {"title": "Alternative Performance Measures", "start_page": 38, "end_page": 47},  # App only
    ]

    res = compare_section_maps(user_sections, app_sections)

    assert len(res.matched) == 3
    # Check that highlights matched
    m_high = next(m for m in res.matched if m.user_section["title"] == "Highlights")
    assert m_high.app_section["title"] == "Key Highlights"
    assert m_high.page_diff == 0

    # Check CEO matched
    m_ceo = next(m for m in res.matched if m.user_section["title"] == "CEO Statement")
    assert m_ceo.app_section["title"] == "Chief Executive's Review"
    assert m_ceo.page_diff == 0

    # Check Statements matched
    m_fs = next(m for m in res.matched if m.user_section["title"] == "Financial Statements")
    assert m_fs.app_section["title"] == "Primary Financial Statements"
    assert m_fs.page_diff == 0

    # User only
    assert len(res.user_only) == 1
    assert res.user_only[0]["title"] == "Custom Valuation Model Notes"

    # App only
    assert len(res.app_only) == 3
    app_titles = [a["title"] for a in res.app_only]
    assert "Financial Notes" in app_titles
    assert "Alternative Performance Measures" in app_titles


def test_extract_all_app_sections_pan(pdf_path):
    source = PdfSource(pdf_path)
    secs = extract_all_app_sections(source)
    assert len(secs) >= 3
    titles = [s["title"].lower() for s in secs]
    assert any("statement" in t or "chief" in t or "financial" in t for t in titles)


def test_section_comparison_dialog_gui(pdf_path, qapp, monkeypatch):
    from PySide6.QtWidgets import QMessageBox
    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(QMessageBox, "question", lambda *args, **kwargs: QMessageBox.StandardButton.Yes)

    source = PdfSource(pdf_path)
    user_sections = [
        {"title": "Highlights", "start_page": 2},
        {"title": "CEO Review", "start_page": 5},
    ]
    dlg = SectionComparisonDialog(source=source, user_sections=user_sections, sector="mining")

    assert dlg.table.rowCount() > 0
    # Verify filter switching
    dlg.filter_combo.setCurrentIndex(1)  # Matched
    assert dlg.table.rowCount() <= len(user_sections)

    # Verify adopt single app section
    initial_count = len(dlg.user_sections)
    if dlg._comparison.app_only:
        first_app_sec = dlg._comparison.app_only[0]
        dlg._adopt_single_app_section(first_app_sec)
        assert len(dlg.user_sections) == initial_count + 1

    dlg.close()
    dlg.deleteLater()


def test_auto_capture_matched_sections(pdf_path, qapp, tmp_path, monkeypatch):
    from PySide6.QtWidgets import QMessageBox
    from section_capture.db import list_sections

    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(QMessageBox, "question", lambda *args, **kwargs: QMessageBox.StandardButton.Yes)

    source = PdfSource(pdf_path)
    user_sections = [
        {"title": "Highlights", "start_page": 2, "end_page": 2},
    ]
    from PySide6.QtWidgets import QWidget
    called = []
    class DummyWindow(QWidget):
        def run_all_pending(self):
            called.append(True)

    dummy_parent = DummyWindow()

    dlg = SectionComparisonDialog(
        source=source,
        user_sections=user_sections,
        sector="mining",
        db_path=tmp_path,
        parent=dummy_parent,
    )

    assert len(dlg._comparison.matched) >= 1
    dlg._on_auto_capture_clicked()

    # Verify that the section was saved to analysis.sqlite in tmp_path
    db_file = tmp_path / "analysis.sqlite"
    assert db_file.exists()

    sections = list_sections(source.sha256, db_path=tmp_path)
    assert len(sections) == 1
    assert "Highlights" in sections[0].heading
    assert len(sections[0].selected_text) > 0

    # Verify run_all_pending was automatically triggered via timer
    qapp.processEvents()
    assert len(called) == 1

    dlg.close()
    dlg.deleteLater()
    dummy_parent.deleteLater()

def test_adopt_app_sections_with_identical_titles(pdf_path, qapp, monkeypatch):
    from PySide6.QtWidgets import QMessageBox
    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)

    source = PdfSource(pdf_path)
    user_sections = [
        {"title": "Financial statements overview", "start_page": 1},
    ]
    dlg = SectionComparisonDialog(source=source, user_sections=user_sections, sector="retail")
    dlg._comparison.app_only = [
        {"title": "Financial statements overview", "start_page": 4, "end_page": 28},
        {"title": "Financial statements overview", "start_page": 33, "end_page": 83},
    ]
    dlg._on_adopt_all_app_sections()
    assert len(dlg.user_sections) == 3
    assert any("p.4" in u["title"] for u in dlg.user_sections)
    assert any("p.33" in u["title"] for u in dlg.user_sections)
    dlg.close()
    dlg.deleteLater()



def test_document_order_dialog(qapp):
    from section_capture.map_dialog import DocumentOrderDialog
    from PySide6.QtCore import Qt

    docs = [
        {
            "path": Path("doc_a.pdf"),
            "filename": "doc_a.pdf",
            "doc_type": "presentation",
            "badge": "[PRES]",
            "period": "1H26",
            "page_count": 25,
            "sha256": "sha_a",
            "is_active": True,
        },
        {
            "path": Path("doc_b.pdf"),
            "filename": "doc_b.pdf",
            "doc_type": "afs",
            "badge": "[AFS]",
            "period": "1H26",
            "page_count": 60,
            "sha256": "sha_b",
            "is_active": False,
        },
    ]

    dlg = DocumentOrderDialog(docs)
    assert dlg.table.rowCount() == 2

    ordered = dlg.get_ordered_documents()
    assert len(ordered) == 2
    assert ordered[0]["sha256"] == "sha_a"
    assert ordered[1]["sha256"] == "sha_b"

    # Select row 0 and move down
    dlg.table.selectRow(0)
    dlg._on_move_down()

    ordered = dlg.get_ordered_documents()
    assert ordered[0]["sha256"] == "sha_b"
    assert ordered[1]["sha256"] == "sha_a"

    # Move back up
    dlg.table.selectRow(1)
    dlg._on_move_up()
    ordered = dlg.get_ordered_documents()
    assert ordered[0]["sha256"] == "sha_a"
    assert ordered[1]["sha256"] == "sha_b"

    # Uncheck doc_a
    item = dlg.table.item(0, 0)
    item.setCheckState(Qt.CheckState.Unchecked)
    ordered = dlg.get_ordered_documents()
    assert len(ordered) == 1
    assert ordered[0]["sha256"] == "sha_b"

    dlg.close()
    dlg.deleteLater()


def test_auto_capture_multi_document_ordering(pdf_path, qapp, tmp_path, monkeypatch):
    import shutil
    from PySide6.QtWidgets import QMessageBox, QDialog, QWidget
    from section_capture.map_dialog import DocumentOrderDialog

    sources_dir = tmp_path / "companies" / "mining" / "TEST" / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    pdf1 = sources_dir / "report1_pres.pdf"
    pdf2 = sources_dir / "report2_afs.pdf"
    shutil.copy(pdf_path, pdf1)
    pdf2.write_bytes(pdf_path.read_bytes() + b"\n%companion_dummy\n")

    source1 = PdfSource(pdf1)

    captured_order = []
    class MockWindow(QWidget):
        def run_all_pending(self, ordered_shas=None):
            captured_order.extend(ordered_shas or [])

    mock_parent = MockWindow()

    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: QMessageBox.StandardButton.Ok)
    monkeypatch.setattr(QMessageBox, "question", lambda *args, **kwargs: QMessageBox.StandardButton.Yes)

    def mock_order_exec(dlg_self):
        dlg_self.table.selectRow(0)
        dlg_self._on_move_down()
        return QDialog.DialogCode.Accepted

    monkeypatch.setattr(DocumentOrderDialog, "exec", mock_order_exec)

    user_sections = [{"title": "Highlights", "start_page": 2, "end_page": 2}]
    dlg = SectionComparisonDialog(
        source=source1,
        user_sections=user_sections,
        sector="mining",
        db_path=tmp_path,
        parent=mock_parent,
    )

    dlg._on_auto_capture_clicked()

    assert len(captured_order) == 2
    import hashlib
    sha1 = hashlib.sha256(pdf1.read_bytes()).hexdigest()
    sha2 = hashlib.sha256(pdf2.read_bytes()).hexdigest()
    assert captured_order[0] == sha2
    assert captured_order[1] == sha1

    source1.close()
    dlg.close()
    dlg.deleteLater()
    mock_parent.deleteLater()
