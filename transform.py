"""
transform.py — Role 3: Transformation
Owner (intended): Transformation teammate. Working fallback — keep the
same signature if replaced:
    clean_rows(rows, headers) -> (cleaned_rows, duplicates_removed, changes)

Transformations (each one is easy to explain in the demo):
  1. Trim leading/trailing whitespace from every cell
  2. Lowercase emails        3. Title-case name/city columns
  4. Standardise dates to YYYY-MM-DD (ISO format)
  5. Remove exact duplicate rows (keeps the first copy)
"""
from datetime import datetime

DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%Y/%m/%d")


def _standardise_date(value: str) -> str:
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return value  # leave unparseable dates untouched; validation flags them


def clean_rows(rows, headers):
    cleaned, seen, duplicates, changes = [], set(), 0, 0
    lower = [h.lower() for h in headers]

    for row in rows:
        new_row = {}
        for header, low in zip(headers, lower):
            original = row.get(header) or ""
            value = original.strip()
            if "email" in low:
                value = value.lower()
            elif any(k in low for k in ("name", "city", "country")):
                value = value.title()
            elif "date" in low and value:
                value = _standardise_date(value)
            if value != original:
                changes += 1
            new_row[header] = value

        fingerprint = tuple(new_row[h] for h in headers)
        if fingerprint in seen:
            duplicates += 1
            continue
        seen.add(fingerprint)
        cleaned.append(new_row)

    return cleaned, duplicates, changes