"""Lightweight global orchestrator/validator smoke tests."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class GlobalReproductionInterfaceTests(unittest.TestCase):
    def test_validate_reproduction_script(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_reproduction.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr + proc.stdout)
        self.assertIn("PASS", proc.stdout)
        self.assertIn("Published paper reports 43", proc.stdout)

    def test_package_importable(self) -> None:
        import re_te_lowresources
        from re_te_lowresources import scopus, selection, web_of_science

        self.assertTrue(hasattr(scopus, "reproduce_scopus"))
        self.assertTrue(hasattr(web_of_science, "reproduce_wos"))
        self.assertTrue(hasattr(selection, "reproduce_selection"))
        self.assertEqual(re_te_lowresources.__version__, "0.1.0")


if __name__ == "__main__":
    unittest.main()
