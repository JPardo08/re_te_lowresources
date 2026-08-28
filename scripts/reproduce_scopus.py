#!/usr/bin/env python3
"""CLI: reproduce Scopus aggregation from frozen exports."""

from __future__ import annotations

import sys
from pathlib import Path

from re_te_lowresources.scopus import (
    EXPECTED_CORE_ROWS,
    EXPECTED_UNIQUE_ROWS,
    reproduce_scopus,
)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    try:
        result = reproduce_scopus(ROOT, validate=True, write=True)
    except (FileNotFoundError, KeyError, ValueError, AssertionError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(f"Scopus core records: {result.raw_rows}")
    print(f"Scopus unique records: {result.dedup_rows}")
    print(f"Wrote: {result.core_path.relative_to(ROOT)}")
    print(f"Wrote: {result.unique_path.relative_to(ROOT)}")

    if result.raw_rows != EXPECTED_CORE_ROWS or result.dedup_rows != EXPECTED_UNIQUE_ROWS:
        print("FAIL", file=sys.stderr)
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
