"""Small I/O helpers that avoid dirtying tracked files when content is unchanged."""

from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Any

import pandas as pd


def write_bytes_if_changed(path: Path, content: bytes) -> Path:
    """Write ``content`` only when missing or byte-different from the existing file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and path.read_bytes() == content:
        return path
    path.write_bytes(content)
    return path


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Serialize a dataframe to UTF-8 CSV bytes (no index; ``\\n`` terminators)."""
    buf = io.StringIO()
    df.to_csv(buf, index=False, lineterminator="\n")
    return buf.getvalue().encode("utf-8")


def write_dataframe_csv_if_changed(df: pd.DataFrame, path: Path) -> Path:
    return write_bytes_if_changed(Path(path), dataframe_to_csv_bytes(df))


def write_text_if_changed(path: Path, text: str, encoding: str = "utf-8") -> Path:
    return write_bytes_if_changed(Path(path), text.encode(encoding))


def write_csv_rows_if_changed(
    path: Path, rows: list[dict[str, Any]], columns: list[str]
) -> Path:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({c: row.get(c, "") for c in columns})
    return write_bytes_if_changed(Path(path), buf.getvalue().encode("utf-8"))
