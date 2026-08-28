"""Lightweight tests for the Web of Science reproduction stage."""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from re_te_lowresources.web_of_science import (
    CORE_QUERY_ORDER,
    EXPECTED_CORE_ROWS,
    EXPECTED_UNIQUE_ROWS,
    OUTPUT_CORE_NAME,
    OUTPUT_UNIQUE_NAME,
    TITLE_COLUMN,
    build_wos_core,
    build_wos_unique,
    discover_wos_exports,
    reproduce_wos,
)

ROOT = Path(__file__).resolve().parents[1]


class WoSReproductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sources = ROOT / "sources" / "web_of_science"

    def test_discover_is_deterministic(self) -> None:
        a = discover_wos_exports(self.sources)
        b = discover_wos_exports(self.sources)
        self.assertEqual(a, b)
        queries = [p.parent.parent.name for p in a]
        strategies = [p.parent.name for p in a]
        self.assertEqual(list(dict.fromkeys(queries)), list(CORE_QUERY_ORDER))
        self.assertTrue(all(s in {"A", "B"} for s in strategies))
        self.assertTrue(all(p.name == "savedrecs.xls" for p in a))

    def test_core_and_unique_counts(self) -> None:
        core = build_wos_core(self.sources)
        unique = build_wos_unique(core)
        self.assertEqual(len(core), EXPECTED_CORE_ROWS)
        self.assertEqual(len(unique), EXPECTED_UNIQUE_ROWS)
        self.assertIn(TITLE_COLUMN, core.columns)
        self.assertIn("query", core.columns)

    def test_title_column_and_keep_first_dedup(self) -> None:
        core = build_wos_core(self.sources)
        unique = build_wos_unique(core)
        self.assertEqual(TITLE_COLUMN, "Article Title")
        # keep="first": first occurrence of each title in concat order is retained.
        first_titles = core.drop_duplicates(subset=TITLE_COLUMN, keep="first")[
            TITLE_COLUMN
        ].tolist()
        self.assertEqual(unique[TITLE_COLUMN].tolist(), first_titles)

    def test_reproduce_writes_named_outputs(self) -> None:
        result = reproduce_wos(ROOT, validate=True, write=True)
        self.assertEqual(result.core_path.name, OUTPUT_CORE_NAME)
        self.assertEqual(result.unique_path.name, OUTPUT_UNIQUE_NAME)
        self.assertTrue(result.core_path.is_file())
        self.assertTrue(result.unique_path.is_file())
        self.assertEqual(result.raw_rows, EXPECTED_CORE_ROWS)
        self.assertEqual(result.dedup_rows, EXPECTED_UNIQUE_ROWS)

    def test_cli_independent_of_cwd(self) -> None:
        script = ROOT / "scripts" / "reproduce_wos.py"
        env = os.environ.copy()
        # Prefer repo venv python if present.
        python = ROOT / ".venv" / "bin" / "python"
        exe = str(python) if python.is_file() else sys.executable
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [exe, str(script)],
                cwd=tmp,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr + proc.stdout)
        self.assertIn("PASS", proc.stdout)
        out_core = ROOT / "data" / "automatic" / "web_of_science" / OUTPUT_CORE_NAME
        out_unique = ROOT / "data" / "automatic" / "web_of_science" / OUTPUT_UNIQUE_NAME
        self.assertTrue(out_core.is_file())
        self.assertTrue(out_unique.is_file())
        # Smoke: files are non-empty and stable under a second run from another cwd.
        h1 = hashlib.sha256(out_unique.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as tmp:
            proc2 = subprocess.run(
                [exe, str(script)],
                cwd=tmp,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(proc2.returncode, 0)
        h2 = hashlib.sha256(out_unique.read_bytes()).hexdigest()
        self.assertEqual(h1, h2)


if __name__ == "__main__":
    unittest.main()
