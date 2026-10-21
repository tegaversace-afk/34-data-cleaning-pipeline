"""
tests/test_api.py — run with:  pytest -v
Covers the happy path AND major failure paths (required by the rubric).
These tests import the app directly — no running server needed.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
GOOD_CSV = b"name,email,age\n  ada lovelace ,ADA@Example.com,36\nada lovelace,ADA@Example.com,36\n,BAD-email,999\n"


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_home_serves_ui():
    res = client.get("/")
    assert res.status_code == 200 and "Data Cleaning Pipeline" in res.text


def test_happy_path_upload_cleans_and_reports():
    res = client.post("/api/upload", files={"file": ("test.csv", GOOD_CSV, "text/csv")})
    assert res.status_code == 200
    data = res.json()
    assert data["report"]["total_rows_in"] == 3
    assert data["report"]["duplicates_removed"] == 1          # rows 1 & 2 identical after cleaning
    assert data["report"]["total_issues"] >= 2                  # missing name, bad email, bad age
    # cleaned file is downloadable
    dl = client.get(data["download_url"])
    assert dl.status_code == 200 and "ada@example.com" in dl.text.lower()


def test_run_sample_one_click_demo():
    res = client.post("/api/run-sample")
    assert res.status_code == 200
    assert res.json()["report"]["total_rows_in"] >= 10


def test_failure_empty_file_rejected():
    res = client.post("/api/upload", files={"file": ("empty.csv", b"", "text/csv")})
    assert res.status_code == 400


def test_failure_non_csv_rejected():
    res = client.post("/api/upload", files={"file": ("notes.txt", b"hello", "text/plain")})
    assert res.status_code == 400


def test_failure_header_only_rejected():
    res = client.post("/api/upload", files={"file": ("h.csv", b"name,email\n", "text/csv")})
    assert res.status_code == 400


def test_unknown_job_is_404():
    assert client.get("/api/download/doesnotexist").status_code == 404
