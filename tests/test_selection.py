"""Lightweight tests for the dual-view Selection stage."""

from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

from re_te_lowresources.selection import (
    ANCIENT_CHINESE_TITLE,
    EXPECTED_CORRECTED,
    EXPECTED_FINAL_CORPUS,
    EXPECTED_HISTORICAL,
    EXPECTED_MANUAL_CANDIDATES,
    EXPECTED_MANUAL_DOUBT,
    EXPECTED_MANUAL_NO,
    EXPECTED_MANUAL_YES,
    KBPT_DOI_NORMALIZED,
    PIPELINE_VIEW_COLUMN,
    TERL_EIDS,
    TITLE_COLUMN,
    VIEW_CORRECTED,
    VIEW_HISTORICAL,
    build_corrected_funnel,
    build_historical_funnel,
    load_platform_uniques,
    normalize_doi,
    normalize_title,
    reproduce_selection,
)

ROOT = Path(__file__).resolve().parents[1]


class SelectionReproductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scopus, cls.wos = load_platform_uniques()
        cls.historical = build_historical_funnel(cls.scopus, cls.wos)
        cls.corrected = build_corrected_funnel(cls.scopus, cls.wos)

    def test_historical_funnel_counts(self) -> None:
        self.assertEqual(self.historical.counts(), EXPECTED_HISTORICAL)
        self.assertEqual(self.historical.view, VIEW_HISTORICAL)

    def test_corrected_funnel_counts(self) -> None:
        self.assertEqual(self.corrected.counts(), EXPECTED_CORRECTED)
        self.assertEqual(self.corrected.view, VIEW_CORRECTED)

    def test_views_not_mixed_in_outputs(self) -> None:
        for frame in self.historical.as_dict().values():
            self.assertTrue((frame[PIPELINE_VIEW_COLUMN] == VIEW_HISTORICAL).all())
        for frame in self.corrected.as_dict().values():
            self.assertTrue((frame[PIPELINE_VIEW_COLUMN] == VIEW_CORRECTED).all())

    def test_terl_collapses_at_candidates(self) -> None:
        proc = self.historical.proceedings_filtered
        terl_proc = proc[
            proc[TITLE_COLUMN].astype(str).str.contains("TERL:", case=False, na=False)
        ]
        self.assertEqual(len(terl_proc), 2)
        eids = set(terl_proc["eid"].dropna().astype(str))
        self.assertTrue(TERL_EIDS.issubset(eids))
        terl_cand = self.historical.candidates[
            self.historical.candidates[TITLE_COLUMN]
            .astype(str)
            .str.contains("TERL:", case=False, na=False)
        ]
        self.assertEqual(len(terl_cand), 1)

    def test_ancient_chinese_corrected_only(self) -> None:
        corr = self.corrected.candidates[
            self.corrected.candidates[TITLE_COLUMN]
            .astype(str)
            .str.contains("Ancient Chinese Documents", case=False, na=False)
        ]
        self.assertEqual(len(corr), 1)
        self.assertEqual(
            normalize_title(corr.iloc[0][TITLE_COLUMN]),
            normalize_title(ANCIENT_CHINESE_TITLE),
        )
        hist = self.historical.candidates[
            self.historical.candidates[TITLE_COLUMN]
            .astype(str)
            .str.contains("Ancient Chinese", case=False, na=False)
        ]
        self.assertEqual(len(hist), 0)

    def test_kbpt_doi_collision_diagnostic(self) -> None:
        uniq = self.corrected.unique.copy()
        uniq["_doi"] = uniq["doi"].map(normalize_doi)
        kbpt = uniq[uniq["_doi"] == KBPT_DOI_NORMALIZED]
        self.assertGreaterEqual(len(kbpt), 2)
        engines = set(kbpt["search_engine"].astype(str))
        self.assertIn("Scopus", engines)
        self.assertIn("Web of Science", engines)

    def test_source_order_scopus_then_wos(self) -> None:
        merged = self.corrected.merged
        engines = merged["search_engine"].tolist()
        first_wos = engines.index("Web of Science")
        self.assertTrue(all(e == "Scopus" for e in engines[:first_wos]))
        self.assertEqual(engines[first_wos:].count("Web of Science"), 62)
        self.assertEqual(first_wos, 164)

    def test_reproduce_writes_and_manual_final(self) -> None:
        result = reproduce_selection(ROOT, validate=True, write=True)
        self.assertEqual(result.historical.counts(), EXPECTED_HISTORICAL)
        self.assertEqual(result.corrected.counts(), EXPECTED_CORRECTED)

        study = Path(result.study_selection_path)
        final_sel = Path(result.final_selection_path)
        corpus = Path(result.final_corpus_path)
        self.assertTrue(study.is_file())
        self.assertTrue(final_sel.is_file())
        self.assertTrue(corpus.is_file())

        import pandas as pd

        study_df = pd.read_csv(study)
        self.assertEqual(len(study_df), EXPECTED_MANUAL_CANDIDATES)
        states = study_df["choosen_state"].value_counts()
        self.assertEqual(int(states["Yes"]), EXPECTED_MANUAL_YES)
        self.assertEqual(int(states["No"]), EXPECTED_MANUAL_NO)
        self.assertEqual(int(states["Doubt"]), EXPECTED_MANUAL_DOUBT)
        # Ancient Chinese never manually screened historically.
        self.assertFalse(
            study_df["title"]
            .astype(str)
            .str.contains("Ancient Chinese", case=False, na=False)
            .any()
        )

        final_df = pd.read_csv(final_sel)
        self.assertEqual(len(final_df), EXPECTED_MANUAL_YES)
        self.assertEqual(int(final_df["in_final_corpus"].sum()), EXPECTED_FINAL_CORPUS)
        non_final = sorted(
            final_df.loc[~final_df["in_final_corpus"].astype(bool), "paper_id"]
            .astype(str)
            .tolist()
        )
        self.assertEqual(
            non_final, ["jian", "liu5_349", "souza_508", "wang_109", "zhao"]
        )

        corpus_df = pd.read_csv(corpus)
        self.assertEqual(len(corpus_df), EXPECTED_FINAL_CORPUS)
        self.assertEqual(corpus_df["paper_id"].nunique(), EXPECTED_FINAL_CORPUS)

        # Directory separation prevents accidental confusion.
        for path in result.historical_paths.values():
            self.assertIn(f"/{VIEW_HISTORICAL}/", path.as_posix())
        for path in result.corrected_paths.values():
            self.assertIn(f"/{VIEW_CORRECTED}/", path.as_posix())

    def test_deterministic_outputs(self) -> None:
        reproduce_selection(ROOT, validate=True, write=True)
        paths = [
            ROOT / "data/automatic/selection/historical/candidates.csv",
            ROOT / "data/automatic/selection/corrected/candidates.csv",
            ROOT / "data/manual/study_selection.csv",
            ROOT / "data/manual/final_selection.csv",
            ROOT / "data/final/final_corpus.csv",
        ]
        hashes = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        reproduce_selection(ROOT, validate=True, write=True)
        for p, h in hashes.items():
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), h, msg=str(p))


if __name__ == "__main__":
    unittest.main()
