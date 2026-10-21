"""
validate.py — Role 2: Validation
Owner (intended): Validation teammate. Working fallback — keep the same
signature if replaced:  validate_rows(rows, headers) -> list of issues

Each issue: {"row": int (1-based data row), "column": str,
             "value": str, "error": str}
Rules are generic: they activate based on column names, so the pipeline
works on any CSV judges upload, not just our sample.
"""
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[+\d][\d\s\-()]{6,}$")
DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%Y/%m/%d")


def _looks_like_date(value: str) -> bool:
    from datetime import datetime
    for fmt in DATE_FORMATS:
        try:
            datetime.strptime(value.strip(), fmt)
            return True
        except ValueError:
            continue
    return False


def validate_rows(rows, headers):
    issues = []
    lower = [h.lower() for h in headers]

    for i, row in enumerate(rows, start=1):
        for header, low in zip(headers, lower):
            value = (row.get(header) or "").strip()

            if value == "":
                issues.append({"row": i, "column": header, "value": value,
                               "error": "Missing value"})
                continue
            if "email" in low and not EMAIL_RE.match(value):
                issues.append({"row": i, "column": header, "value": value,
                               "error": "Invalid email format"})
            elif low == "age":
                if not value.isdigit() or not (0 <= int(value) <= 120):
                    issues.append({"row": i, "column": header, "value": value,
                                   "error": "Age must be a whole number between 0 and 120"})
            elif "phone" in low and not PHONE_RE.match(value):
                issues.append({"row": i, "column": header, "value": value,
                               "error": "Invalid phone number"})
            elif "date" in low and not _looks_like_date(value):
                issues.append({"row": i, "column": header, "value": value,
                               "error": "Unrecognised date format"})
    return issues
