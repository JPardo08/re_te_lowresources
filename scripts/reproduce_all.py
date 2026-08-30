#!/usr/bin/env python3
"""Orchestrate full Paper-1 public reproducibility (all stages)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from re_te_lowresources.scopus import reproduce_scopus
from re_te_lowresources.selection import (
    EXPECTED_FINAL_CORPUS,
    EXPECTED_MANUAL_DOUBT,
    EXPECTED_MANUAL_NO,
    EXPECTED_MANUAL_YES,
    PUBLISHED_FINAL_COUNT_WARNING,
    format_funnel_arrow,
    reproduce_selection,
)
from re_te_lowresources.web_of_science import reproduce_wos


def main() -> int:
    print("=== 1. Scopus ===")
    try:
        scopus = reproduce_scopus(ROOT, validate=True, write=True)
    except Exception as exc:
        print(f"FAIL Scopus: {exc}", file=sys.stderr)
        return 1
    print(f"Scopus: {scopus.raw_rows} core → {scopus.dedup_rows} unique")

    print("=== 2. Web of Science ===")
    try:
        wos = reproduce_wos(ROOT, validate=True, write=True)
    except Exception as exc:
        print(f"FAIL WoS: {exc}", file=sys.stderr)
        return 1
    print(f"WoS: {wos.raw_rows} core → {wos.dedup_rows} unique")

    print("=== 3–5. Selection (historical + corrected) + manual + final ===")
    try:
        selection = reproduce_selection(ROOT, validate=True, write=True)
    except Exception as exc:
        print(f"FAIL Selection: {exc}", file=sys.stderr)
        return 1
    print(f"Historical: {format_funnel_arrow(selection.historical.counts())}")
    print(f"Corrected:  {format_funnel_arrow(selection.corrected.counts())}")
    print(
        f"Manual: Yes {EXPECTED_MANUAL_YES} / No {EXPECTED_MANUAL_NO} / "
        f"Doubt {EXPECTED_MANUAL_DOUBT}"
    )
    print(f"Final corpus: {EXPECTED_FINAL_CORPUS}")
    if selection.process_statistics_path is not None:
        print(f"Process statistics: {selection.process_statistics_path.relative_to(ROOT)}")
    print(f"WARNING: {PUBLISHED_FINAL_COUNT_WARNING}")
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
