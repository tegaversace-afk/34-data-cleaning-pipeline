"""
database.py — Role 4: Reports + Storage (SQLite)
Stores one row per cleaning run ("job") so the UI can show history and
re-download a cleaned file. Uses sqlite3 from the standard library.
NOTE: On Render's free tier the disk is ephemeral — history resets on
redeploy. That is an honest, documented MVP limitation.
"""
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent / "jobs.db"


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id          TEXT PRIMARY KEY,
                filename    TEXT NOT NULL,
                created_at  TEXT NOT NULL,
                report_json TEXT NOT NULL,
                issues_json TEXT NOT NULL,
                cleaned_csv TEXT NOT NULL
            )
            """
        )


def save_job(filename, report, issues, cleaned_csv):
    job_id = uuid.uuid4().hex[:10]
    with _connect() as conn:
        conn.execute(
            "INSERT INTO jobs VALUES (?,?,?,?,?,?)",
            (job_id, filename, datetime.now(timezone.utc).isoformat(),
             json.dumps(report), json.dumps(issues), cleaned_csv),
        )
    return job_id


def list_jobs(limit=10):
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, filename, created_at, report_json FROM jobs "
            "ORDER BY created_at DESC LIMIT ?", (limit,),
        ).fetchall()
    return [{"id": r["id"], "filename": r["filename"],
             "created_at": r["created_at"], "report": json.loads(r["report_json"])}
            for r in rows]


def get_job(job_id):
    with _connect() as conn:
        row = conn.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    if row is None:
        return None
    return {"id": row["id"], "filename": row["filename"],
            "created_at": row["created_at"],
            "report": json.loads(row["report_json"]),
            "issues": json.loads(row["issues_json"]),
            "cleaned_csv": row["cleaned_csv"]}
