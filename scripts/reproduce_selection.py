#!/usr/bin/env python3
"""CLI: dual-view Selection reproducibility (historical + corrected)."""

from __future__ import annotations

import sys
from pathlib import Path

from re_te_lowresources.selection import (
    EXPECTED_FINAL_CORPUS,
    EXPECTED_MANUAL_DOUBT,
    EXPECTED_MANUAL_NO,
    EXPECTED_MANUAL_YES,
    PUBLISHED_FINAL_COUNT_WARNING,
    format_funnel_arrow,
    reproduce_selection,
)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    try:
        result = reproduce_selection(ROOT, validate=True, write=True)
    except (FileNotFoundError, KeyError, ValueError, AssertionError, ImportError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print("Historical:")
    print(format_funnel_arrow(result.historical.counts()))
    print()
    print("Corrected:")
    print(format_funnel_arrow(result.corrected.counts()))
    print()
    print("Manual historical:")
    print(
        f"Yes {EXPECTED_MANUAL_YES} / No {EXPECTED_MANUAL_NO} / "
        f"Doubt {EXPECTED_MANUAL_DOUBT}"
    )
    print(f"Final recoverable corpus: {EXPECTED_FINAL_CORPUS}")
    print()
    print("WARNING:")
    print(PUBLISHED_FINAL_COUNT_WARNING)
    print()

    for mapping in (result.historical_paths, result.corrected_paths):
        for path in mapping.values():
            print(f"Wrote: {path.relative_to(ROOT)}")
    for path in (
        result.study_selection_path,
        result.final_selection_path,
        result.final_corpus_path,
    ):
        if path is not None:
            print(f"Wrote: {path.relative_to(ROOT)}")

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
