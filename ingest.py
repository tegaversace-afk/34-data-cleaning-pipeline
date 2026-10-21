"""
ingest.py — Role 1: Ingestion
Owner (intended): Ingestion teammate. This is a WORKING fallback so the
demo never breaks. If Role 1 delivers their own version, keep the same
function signature:  read_csv_bytes(content, filename) -> (headers, rows)

Reads raw uploaded bytes and turns them into headers + list of dict rows.
Uses only the Python standard library (csv) — no pandas needed.
"""
import csv
import io

MAX_FILE_BYTES = 5 * 1024 * 1024  # 5 MB safety limit for the MVP


def read_csv_bytes(content: bytes, filename: str = "upload.csv"):
    """Parse CSV bytes. Returns (headers, rows). Raises ValueError with a
    user-friendly message for every bad input we expect judges to try."""
    if not content:
        raise ValueError("The uploaded file is empty.")
    if len(content) > MAX_FILE_BYTES:
        raise ValueError("File is too large. The MVP limit is 5 MB.")
    if filename and not filename.lower().endswith(".csv"):
        raise ValueError("Only .csv files are accepted.")

    # utf-8-sig strips the BOM Excel sometimes adds; errors='strict' so
    # binary/non-CSV files fail loudly instead of producing garbage.
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise ValueError("Could not read this file as text. Please upload a UTF-8 CSV file.")

    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None or all(not (h or "").strip() for h in reader.fieldnames):
        raise ValueError("No header row found. The first row must contain column names.")

    headers = [h.strip() for h in reader.fieldnames]
    rows = []
    for raw in reader:
        # Normalise every row to exactly our headers (missing cell -> "")
        row = {h: (raw.get(h) or "") for h in reader.fieldnames}
        row = {h.strip(): v for h, v in row.items()}
        # Skip completely blank lines in the file
        if all(not (v or "").strip() for v in row.values()):
            continue
        rows.append(row)

    if not rows:
        raise ValueError("The CSV has a header but no data rows.")
    return headers, rows
