"""Lightweight tests for the Scopus reproduction stage."""

from __future__ import annotations

import unittest
from pathlib import Path

from re_te_lowresources.scopus import (
    CORE_QUERY_ORDER,
    EXPECTED_CORE_ROWS,
    EXPECTED_UNIQUE_ROWS,
    OUTPUT_CORE_NAME,
    OUTPUT_UNIQUE_NAME,
    TITLE_COLUMN,
    build_scopus_core,
    build_scopus_unique,
    discover_scopus_exports,
    reproduce_scopus,
)

ROOT = Path(__file__).resolve().parents[1]


class ScopusReproductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sources = ROOT / "sources" / "scopus"

    def test_discover_is_deterministic(self) -> None:
        a = discover_scopus_exports(self.sources)
        b = discover_scopus_exports(self.sources)
        self.assertEqual(a, b)
        queries = [p.parent.parent.name for p in a]
        strategies = [p.parent.name for p in a]
        self.assertEqual(list(dict.fromkeys(queries)), list(CORE_QUERY_ORDER))
        self.assertTrue(all(s in {"A", "B"} for s in strategies))

    def test_core_and_unique_counts(self) -> None:
        core = build_scopus_core(self.sources)
        unique = build_scopus_unique(core)
        self.assertEqual(len(core), EXPECTED_CORE_ROWS)
        self.assertEqual(len(unique), EXPECTED_UNIQUE_ROWS)
        self.assertIn(TITLE_COLUMN, core.columns)
        self.assertIn("query", core.columns)

    def test_terl_duplicate_retained_in_core(self) -> None:
        core = build_scopus_core(self.sources)
        terl = core[
            core[TITLE_COLUMN]
            .astype(str)
            .str.contains("TERL:", case=False, na=False)
        ]
        self.assertGreaterEqual(len(terl), 2)

    def test_reproduce_writes_named_outputs(self) -> None:
        result = reproduce_scopus(ROOT, validate=True, write=True)
        self.assertEqual(result.core_path.name, OUTPUT_CORE_NAME)
        self.assertEqual(result.unique_path.name, OUTPUT_UNIQUE_NAME)
        self.assertTrue(result.core_path.is_file())
        self.assertTrue(result.unique_path.is_file())
        self.assertEqual(result.raw_rows, EXPECTED_CORE_ROWS)
        self.assertEqual(result.dedup_rows, EXPECTED_UNIQUE_ROWS)


if __name__ == "__main__":
    unittest.main()
