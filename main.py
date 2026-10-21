"""
main.py — Role 5: API + UI + Deployment  ★ YOUR FILE ★
Team 7 · 34-data-cleaning-pipeline

What this file does (say this in the demo):
  "main.py is the entry point. It exposes the whole pipeline as a web API
   with FastAPI, serves the dashboard in /static, and is the file Render
   runs. It does no cleaning itself — it calls ingest → validate →
   transform → report in order, stores the run, and returns JSON.
   That separation is why five of us could work in parallel."

Run locally:   uvicorn main:app --reload --port 8000
Run on Render: uvicorn main:app --host 0.0.0.0 --port $PORT
API docs (free from FastAPI):  http://localhost:8000/docs
"""
import csv
import io
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles

import database
import ingest
import report as report_module
import transform
import validate

BASE_DIR = Path(__file__).parent
SAMPLE_PATH = BASE_DIR / "sample_data" / "messy_customers.csv"
PREVIEW_ROWS = 10  # rows returned to the UI for the before/after tables

app = FastAPI(title="Data Cleaning Pipeline — Team 7", version="1.0.0")
database.init_db()

# Serve index.html / style.css / app.js at /static/...
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


# ---------------------------------------------------------------- helpers
def run_pipeline(content: bytes, filename: str) -> dict:
    """The one end-to-end flow: ingest → validate → transform → report → store.
    Raises HTTPException(400) with a friendly message on any bad input."""
    try:
        headers, rows = ingest.read_csv_bytes(content, filename)          # Role 1
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

    issues = validate.validate_rows(rows, headers)                          # Role 2
    cleaned, duplicates, changes = transform.clean_rows(rows, headers)      # Role 3
    summary = report_module.build_report(rows, cleaned, issues, duplicates, changes)  # Role 4

    # Turn cleaned rows back into downloadable CSV text
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=headers)
    writer.writeheader()
    writer.writerows(cleaned)

    job_id = database.save_job(filename, summary, issues, buffer.getvalue())  # Role 4

    return {
        "job_id": job_id,
        "filename": filename,
        "headers": headers,
        "report": summary,
        "issues": issues[:100],               # cap payload; full list stored in DB
        "preview_before": rows[:PREVIEW_ROWS],
        "preview_after": cleaned[:PREVIEW_ROWS],
        "download_url": f"/api/download/{job_id}",
    }


# ----------------------------------------------------------------- routes
@app.get("/")
def home():
    """Serve the dashboard (Role 5 UI)."""
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/health")
def health():
    """Used by Render and judges to check the service is alive."""
    return {"status": "ok", "service": "34-data-cleaning-pipeline"}


@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    """Main user flow: upload a messy CSV, get a quality report + cleaned file."""
    content = await file.read()
    return run_pipeline(content, file.filename or "upload.csv")


@app.post("/api/run-sample")
def run_sample():
    """One-click demo: runs the built-in messy sample so judges need no file."""
    if not SAMPLE_PATH.exists():
        raise HTTPException(status_code=500, detail="Sample data file is missing.")
    return run_pipeline(SAMPLE_PATH.read_bytes(), "messy_customers.csv")


@app.get("/api/sample")
def download_sample():
    return FileResponse(SAMPLE_PATH, media_type="text/csv",
                        filename="messy_customers.csv")


@app.get("/api/jobs")
def jobs():
    """History of previous runs (from SQLite)."""
    return {"jobs": database.list_jobs()}


@app.get("/api/jobs/{job_id}")
def job_detail(job_id: str):
    job = database.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found.")
    job.pop("cleaned_csv")  # don't dump the whole file into this JSON response
    job["download_url"] = f"/api/download/{job_id}"
    return job


@app.get("/api/download/{job_id}")
def download(job_id: str):
    job = database.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found.")
    return Response(
        content=job["cleaned_csv"],
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="cleaned_{job["filename"]}"'},
    )
