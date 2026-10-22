import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from ingest import read_csv_bytes


def test_valid_csv():
    content = b"name,age\nTega,25\nJohn,30\n"

    headers, rows = read_csv_bytes(content, "people.csv")

    assert headers == ["name", "age"]
    assert len(rows) == 2
    assert rows[0]["name"] == "Tega"


def test_empty_file():
    with pytest.raises(ValueError, match="empty"):
        read_csv_bytes(b"", "empty.csv")


def test_wrong_file_extension():
    with pytest.raises(ValueError, match="Only .csv"):
        read_csv_bytes(b"name\nTega\n", "people.txt")


def test_header_only_csv():
    with pytest.raises(ValueError, match="no data rows"):
        read_csv_bytes(b"name,age\n", "people.csv")


def test_invalid_encoding():
    with pytest.raises(ValueError, match="UTF-8"):
        read_csv_bytes(b"\xff\xfe\xfa", "people.csv")


def test_file_too_large():
    from ingest import MAX_FILE_BYTES

    content = b"a" * (MAX_FILE_BYTES + 1)

    with pytest.raises(ValueError, match="too large"):
        read_csv_bytes(content, "large.csv")