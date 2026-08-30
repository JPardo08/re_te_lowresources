"""Tests for Paper-1 derived process statistics."""

from __future__ import annotations

import math
import unittest
from pathlib import Path

import pandas as pd

from re_te_lowresources.statistics import (
    PROCESS_STATISTICS_REL,
    compute_process_statistics,
    expected_process_statistics,
    format_percentage,
    statistics_lookup,
    write_process_statistics,
)

ROOT = Path(__file__).resolve().parents[1]


class ProcessStatisticsTests(unittest.TestCase):
    def test_expected_counts_match_stored_and_computed(self) -> None:
        stored = pd.read_csv(ROOT / PROCESS_STATISTICS_REL)
        computed = compute_process_statistics(ROOT)
        expected = expected_process_statistics()
        for (stage, metric), count in expected.items():
            row = statistics_lookup(stored, stage, metric)
            self.assertEqual(row["count"], count, msg=f"{stage}/{metric}")
        for row in computed:
            got = statistics_lookup(stored, row.stage, row.metric)
            self.assertEqual(got["count"], row.count, msg=f"{row.stage}/{row.metric}")
            if row.percentage is not None:
                self.assertTrue(
                    math.isclose(
                        got["percentage"],
                        row.percentage,
                        rel_tol=0,
                        abs_tol=1e-12,
                    )
                )

    def test_manual_percentages(self) -> None:
        stored = pd.read_csv(ROOT / PROCESS_STATISTICS_REL)
        yes = statistics_lookup(stored, "manual", "yes")
        self.assertTrue(math.isclose(yes["percentage"], 47 / 134 * 100))
        self.assertEqual(format_percentage(47 / 134 * 100), "35.1")

    def test_write_is_noop_when_unchanged(self) -> None:
        path = ROOT / PROCESS_STATISTICS_REL
        before = path.read_bytes()
        write_process_statistics(ROOT)
        self.assertEqual(path.read_bytes(), before)

    def test_no_free_or_peer_review_metrics(self) -> None:
        stored = pd.read_csv(ROOT / PROCESS_STATISTICS_REL)
        metrics = set(stored["metric"].astype(str))
        stages = set(stored["stage"].astype(str))
        self.assertNotIn("free", {m.lower() for m in metrics})
        self.assertNotIn("peer_review", {m.lower() for m in metrics})
        self.assertNotIn("peer review", {m.lower() for m in metrics})
        self.assertNotIn("free", {s.lower() for s in stages})


if __name__ == "__main__":
    unittest.main()
