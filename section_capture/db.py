"""Central SQLite persistence for report maps, captured sections, prompts, LLM responses, and question ledgers."""
from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "documents/analysis.sqlite"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS reports (
    sha256 TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    original_path TEXT NOT NULL,
    byte_size INTEGER NOT NULL DEFAULT 0,
    physical_page_count INTEGER NOT NULL,
    report_map_json TEXT,
    questions_ledger TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id TEXT UNIQUE NOT NULL,
    report_sha256 TEXT NOT NULL,
    section_number INTEGER NOT NULL,
    section_id TEXT NOT NULL,
    heading TEXT NOT NULL,
    subheading TEXT,
    analyst_question TEXT,
    selected_text TEXT NOT NULL,
    selections_json TEXT NOT NULL,
    stored_questions_snapshot TEXT,
    prompt TEXT NOT NULL,
    llm_response TEXT,
    manifest_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (report_sha256) REFERENCES reports(sha256)
);
"""


@dataclass
class SavedSection:
    package_id: str
    report_sha256: str
    section_number: int
    section_id: str
    name: str
    heading: str
    subheading: str | None
    analyst_question: str | None
    selected_text: str
    selections: list[dict]
    stored_questions: str | None
    prompt: str
    llm_response: str | None
    manifest: dict
    created_at: str
    db_path: Path

    @property
    def response_time_seconds(self) -> float | None:
        return self.manifest.get("review", {}).get("response_time_seconds")

    @property
    def cost_usd(self) -> float | None:
        return self.manifest.get("review", {}).get("cost_usd")

    @property
    def model_used(self) -> str | None:
        return self.manifest.get("review", {}).get("model")

    @property
    def total_tokens(self) -> int | None:
        t = self.manifest.get("review", {}).get("tokens")
        if isinstance(t, dict):
            return t.get("total_tokens")
        return None


def resolve_db_path(db_path: str | Path | None = None) -> Path:
    if db_path is None:
        target = Path(DB_PATH)
    else:
        candidate = Path(db_path)
        if candidate.suffix.lower() in {".sqlite", ".sqlite3", ".db"}:
            target = candidate
        else:
            target = candidate / "analysis.sqlite"
    target.parent.mkdir(parents=True, exist_ok=True)
    return target.resolve()


def connect_db(db_path: str | Path | None = None) -> sqlite3.Connection:
    path = resolve_db_path(db_path)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA_SQL)
    return conn


def upsert_report(
    sha256: str,
    filename: str = "",
    original_path: str = "",
    byte_size: int = 0,
    physical_page_count: int = 1,
    report_map: dict | None = None,
    questions_ledger: str | None = None,
    db_path: str | Path | None = None,
) -> Path:
    now = datetime.now(timezone.utc).isoformat()
    map_json = json.dumps(report_map, ensure_ascii=False) if report_map is not None else None
    with connect_db(db_path) as conn:
        existing = conn.execute("SELECT * FROM reports WHERE sha256 = ?", (sha256,)).fetchone()
        if existing is None:
            conn.execute(
                """
                INSERT INTO reports (
                    sha256, filename, original_path, byte_size, physical_page_count,
                    report_map_json, questions_ledger, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    sha256,
                    filename or (report_map or {}).get("source_filename", "") or "report.pdf",
                    original_path or "",
                    byte_size,
                    physical_page_count or (report_map or {}).get("physical_page_count", 1),
                    map_json,
                    (questions_ledger or "").strip(),
                    now,
                    now,
                ),
            )
        else:
            new_filename = filename or existing["filename"]
            new_orig = original_path or existing["original_path"]
            new_size = byte_size if byte_size > 0 else existing["byte_size"]
            new_pages = physical_page_count if physical_page_count > 1 else existing["physical_page_count"]
            new_map = map_json if map_json is not None else existing["report_map_json"]
            new_q = questions_ledger.strip() if questions_ledger is not None else existing["questions_ledger"]
            conn.execute(
                """
                UPDATE reports
                   SET filename = ?,
                       original_path = ?,
                       byte_size = ?,
                       physical_page_count = ?,
                       report_map_json = ?,
                       questions_ledger = ?,
                       updated_at = ?
                 WHERE sha256 = ?
                """,
                (new_filename, new_orig, new_size, new_pages, new_map, new_q, now, sha256),
            )
    return resolve_db_path(db_path)


def get_report_map(sha256: str, db_path: str | Path | None = None) -> dict | None:
    path = resolve_db_path(db_path)
    if not path.exists():
        return None
    with connect_db(path) as conn:
        row = conn.execute("SELECT report_map_json FROM reports WHERE sha256 = ?", (sha256,)).fetchone()
        if row and row["report_map_json"]:
            try:
                return json.loads(row["report_map_json"])
            except ValueError:
                return None
    return None


def get_questions_ledger(sha256: str, db_path: str | Path | None = None) -> str:
    path = resolve_db_path(db_path)
    if not path.exists():
        return ""
    with connect_db(path) as conn:
        row = conn.execute("SELECT questions_ledger FROM reports WHERE sha256 = ?", (sha256,)).fetchone()
        if row and row["questions_ledger"]:
            return row["questions_ledger"].strip()
    return ""


def next_section_number(report_sha256: str, db_path: str | Path | None = None) -> int:
    with connect_db(db_path) as conn:
        row = conn.execute(
            "SELECT COALESCE(MAX(section_number), 0) AS max_num FROM sections WHERE report_sha256 = ?",
            (report_sha256,),
        ).fetchone()
        return int(row["max_num"]) + 1


def insert_section(
    *,
    package_id: str,
    report_sha256: str,
    section_number: int,
    section_id: str,
    name: str,
    heading: str,
    subheading: str | None,
    analyst_question: str | None,
    selected_text: str,
    selections: list[dict],
    stored_questions: str | None,
    prompt: str,
    manifest: dict,
    llm_response: str | None = None,
    created_at: str | None = None,
    db_path: str | Path | None = None,
) -> SavedSection:
    now = created_at or datetime.now(timezone.utc).isoformat()
    resolved = resolve_db_path(db_path)
    src = manifest.get("source") or {}
    upsert_report(
        sha256=report_sha256,
        filename=src.get("filename", ""),
        original_path=src.get("original_path", ""),
        byte_size=int(src.get("byte_size", 0) or 0),
        physical_page_count=int(src.get("physical_page_count", 1) or 1),
        report_map=manifest.get("document_map"),
        db_path=resolved,
    )
    with connect_db(resolved) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO sections (
                package_id, report_sha256, section_number, section_id,
                heading, subheading, analyst_question, selected_text,
                selections_json, stored_questions_snapshot, prompt,
                llm_response, manifest_json, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                package_id,
                report_sha256,
                section_number,
                section_id,
                heading,
                subheading,
                analyst_question,
                selected_text,
                json.dumps(selections, ensure_ascii=False),
                stored_questions,
                prompt,
                llm_response,
                json.dumps(manifest, ensure_ascii=False),
                now,
                now,
            ),
        )
    return SavedSection(
        package_id=package_id,
        report_sha256=report_sha256,
        section_number=section_number,
        section_id=section_id,
        name=name,
        heading=heading,
        subheading=subheading,
        analyst_question=analyst_question,
        selected_text=selected_text,
        selections=selections,
        stored_questions=stored_questions,
        prompt=prompt,
        llm_response=llm_response,
        manifest=manifest,
        created_at=now,
        db_path=resolved,
    )


def _row_to_saved_section(row: sqlite3.Row, db_path: Path) -> SavedSection:
    manifest = json.loads(row["manifest_json"])
    selections = json.loads(row["selections_json"])
    name = manifest.get("section_name") or f"{row['section_number']:02d}-{row['section_id']}"
    return SavedSection(
        package_id=row["package_id"],
        report_sha256=row["report_sha256"],
        section_number=row["section_number"],
        section_id=row["section_id"],
        name=name,
        heading=row["heading"],
        subheading=row["subheading"],
        analyst_question=row["analyst_question"],
        selected_text=row["selected_text"],
        selections=selections,
        stored_questions=row["stored_questions_snapshot"],
        prompt=row["prompt"],
        llm_response=row["llm_response"],
        manifest=manifest,
        created_at=row["created_at"],
        db_path=db_path,
    )


def list_sections(report_sha256: str, db_path: str | Path | None = None) -> list[SavedSection]:
    resolved = resolve_db_path(db_path)
    if not resolved.exists():
        return []
    with connect_db(resolved) as conn:
        rows = conn.execute(
            "SELECT * FROM sections WHERE report_sha256 = ? ORDER BY section_number ASC, id ASC",
            (report_sha256,),
        ).fetchall()
        return [_row_to_saved_section(r, resolved) for r in rows]


def get_section(package_id: str, db_path: str | Path | None = None) -> SavedSection | None:
    resolved = resolve_db_path(db_path)
    if not resolved.exists():
        return None
    with connect_db(resolved) as conn:
        row = conn.execute("SELECT * FROM sections WHERE package_id = ?", (package_id,)).fetchone()
        return _row_to_saved_section(row, resolved) if row else None


def extract_questions_ledger_from_response(response_text: str) -> str | None:
    """Extract Section 4 (Updated Open Questions Ledger) from an LLM Markdown response if present."""
    text = (response_text or "").strip()
    if not text:
        return None
    sec4_match = re.search(
        r"(?:^|\n)#{1,4}\s*(?:4\.?\s*)?Updated Open Questions Ledger[^\n]*\n(.*?)(?=\n#{1,4}\s*(?:5\.?\s*)?(?:Baseline Forecast|Next Section)|\Z)",
        text,
        re.IGNORECASE | re.DOTALL,
    )
    if not sec4_match:
        return None
    block = sec4_match.group(1).strip()
    fence_match = re.search(r"```(?:markdown|md)?\s*\n(.*?)```", block, re.IGNORECASE | re.DOTALL)
    if fence_match:
        extracted = fence_match.group(1).strip()
    else:
        extracted = block
    return extracted or None


def save_section_llm_response(
    package_id: str,
    llm_response: str,
    update_ledger: bool = True,
    response_time_seconds: float | None = None,
    cost_usd: float | None = None,
    tokens: dict | None = None,
    model: str | None = None,
    db_path: str | Path | None = None,
) -> tuple[SavedSection | None, str | None]:
    """Save the LLM response onto a section row and optionally auto-extract & update the report's questions ledger."""
    resolved = resolve_db_path(db_path)
    cleaned_resp = (llm_response or "").strip()
    now = datetime.now(timezone.utc).isoformat()
    extracted_ledger = extract_questions_ledger_from_response(cleaned_resp) if update_ledger else None
    with connect_db(resolved) as conn:
        row = conn.execute("SELECT * FROM sections WHERE package_id = ?", (package_id,)).fetchone()
        if not row:
            return None, None
        manifest = json.loads(row["manifest_json"])
        review = manifest.setdefault("review", {})
        review["model_brief"] = "recorded" if cleaned_resp else "not_run"
        if response_time_seconds is not None:
            review["response_time_seconds"] = round(float(response_time_seconds), 2)
        if cost_usd is not None:
            review["cost_usd"] = round(float(cost_usd), 6)
        if model:
            review["model"] = model
        if tokens:
            review["tokens"] = tokens
        conn.execute(
            "UPDATE sections SET llm_response = ?, manifest_json = ?, updated_at = ? WHERE package_id = ?",
            (cleaned_resp or None, json.dumps(manifest, ensure_ascii=False), now, package_id),
        )

        if extracted_ledger:
            conn.execute(
                "UPDATE reports SET questions_ledger = ?, updated_at = ? WHERE sha256 = ?",
                (extracted_ledger, now, row["report_sha256"]),
            )
        updated_row = conn.execute("SELECT * FROM sections WHERE package_id = ?", (package_id,)).fetchone()
        return _row_to_saved_section(updated_row, resolved), extracted_ledger


def clear_section_llm_response(package_id: str, db_path: str | Path | None = None) -> SavedSection | None:
    """Clear the stored LLM response and review metadata on a section row."""
    resolved = resolve_db_path(db_path)
    now = datetime.now(timezone.utc).isoformat()
    with connect_db(resolved) as conn:
        row = conn.execute("SELECT * FROM sections WHERE package_id = ?", (package_id,)).fetchone()
        if not row:
            return None
        manifest = json.loads(row["manifest_json"])
        manifest["review"] = {"model_brief": "not_run"}
        conn.execute(
            "UPDATE sections SET llm_response = NULL, manifest_json = ?, updated_at = ? WHERE package_id = ?",
            (json.dumps(manifest, ensure_ascii=False), now, package_id),
        )
        updated_row = conn.execute("SELECT * FROM sections WHERE package_id = ?", (package_id,)).fetchone()
        return _row_to_saved_section(updated_row, resolved)


def delete_section(package_id: str, db_path: str | Path | None = None) -> bool:
    """Delete a section row from the database."""
    resolved = resolve_db_path(db_path)
    with connect_db(resolved) as conn:
        cur = conn.execute("DELETE FROM sections WHERE package_id = ?", (package_id,))
        return cur.rowcount > 0

