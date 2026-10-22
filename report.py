"""
report.py + database.py logic is split:
  report.py   — Role 4: builds the quality-report summary statistics
  database.py — Role 4: stores each run in SQLite

build_report(original, cleaned, issues, duplicates, changes) -> dict
"""
from collections import Counter


def build_report(original_rows, cleaned_rows, issues, duplicates_removed, changes_made):
    invalid_rows = len({issue["row"] for issue in issues})
    total = len(original_rows)
    return {
        "total_rows_in": total,
        "rows_out": len(cleaned_rows),
        "duplicates_removed": duplicates_removed,
        "cells_changed": changes_made,
        "total_issues": len(issues),
        "rows_with_issues": invalid_rows,
        "clean_rows": max(total - invalid_rows, 0),
        "issues_by_column": dict(Counter(i["column"] for i in issues)),
        "issues_by_type": dict(Counter(i["error"] for i in issues)),
    }

