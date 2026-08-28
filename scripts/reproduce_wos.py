#!/usr/bin/env python3
"""CLI: reproduce Web of Science aggregation from frozen exports."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from re_te_lowresources.web_of_science import (  # noqa: E402
    EXPECTED_CORE_ROWS,
    EXPECTED_UNIQUE_ROWS,
    reproduce_wos,
)


def main() -> int:
    try:
        result = reproduce_wos(ROOT, validate=True, write=True)
    except (FileNotFoundError, KeyError, ValueError, AssertionError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(f"WoS core records: {result.raw_rows}")
    print(f"WoS deduplicated records: {result.dedup_rows}")
    print(f"Wrote: {result.core_path.relative_to(ROOT)}")
    print(f"Wrote: {result.unique_path.relative_to(ROOT)}")

    if result.raw_rows != EXPECTED_CORE_ROWS or result.dedup_rows != EXPECTED_UNIQUE_ROWS:
        print("FAIL", file=sys.stderr)
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
