#!/usr/bin/env python3
"""Validate generated Paper-1 reproducibility artifacts (counts + invariants)."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

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
    PUBLISHED_FINAL_COUNT_WARNING,
    TERL_EIDS,
    VIEW_CORRECTED,
    VIEW_HISTORICAL,
    normalize_doi,
    normalize_title,
)
from re_te_lowresources.scopus import EXPECTED_CORE_ROWS as SCOPUS_CORE
from re_te_lowresources.scopus import EXPECTED_UNIQUE_ROWS as SCOPUS_UNIQUE
from re_te_lowresources.statistics import (
    PROCESS_STATISTICS_REL,
    compute_process_statistics,
    expected_process_statistics,
    statistics_lookup,
)
from re_te_lowresources.web_of_science import EXPECTED_CORE_ROWS as WOS_CORE
from re_te_lowresources.web_of_science import EXPECTED_UNIQUE_ROWS as WOS_UNIQUE


def _fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)


def _require(path: Path, errors: list[str]) -> Path | None:
    if not path.is_file():
        _fail(f"missing artifact: {path.relative_to(ROOT)}", errors)
        return None
    return path


def main() -> int:
    errors: list[str] = []

    expected_files = [
        ROOT / "data/automatic/scopus/scopus_core.csv",
        ROOT / "data/automatic/scopus/scopus_unique.csv",
        ROOT / "data/automatic/web_of_science/wos_core.csv",
        ROOT / "data/automatic/web_of_science/wos_unique.csv",
        ROOT / "data/automatic/selection/historical/merged.csv",
        ROOT / "data/automatic/selection/historical/unique.csv",
        ROOT / "data/automatic/selection/historical/english.csv",
        ROOT / "data/automatic/selection/historical/proceedings_filtered.csv",
        ROOT / "data/automatic/selection/historical/candidates.csv",
        ROOT / "data/automatic/selection/corrected/merged.csv",
        ROOT / "data/automatic/selection/corrected/unique.csv",
        ROOT / "data/automatic/selection/corrected/english.csv",
        ROOT / "data/automatic/selection/corrected/proceedings_filtered.csv",
        ROOT / "data/automatic/selection/corrected/candidates.csv",
        ROOT / "data/manual/study_selection.csv",
        ROOT / "data/manual/final_selection.csv",
        ROOT / "data/final/final_corpus.csv",
        ROOT / PROCESS_STATISTICS_REL,
    ]
    for path in expected_files:
        _require(path, errors)

    # --- Scopus ---
    scopus_core = ROOT / "data/automatic/scopus/scopus_core.csv"
    scopus_unique = ROOT / "data/automatic/scopus/scopus_unique.csv"
    if scopus_core.is_file() and scopus_unique.is_file():
        n_core = len(pd.read_csv(scopus_core))
        n_unique = len(pd.read_csv(scopus_unique))
        print(f"Scopus: {n_core} core / {n_unique} unique")
        if n_core != SCOPUS_CORE:
            _fail(f"Scopus core: expected {SCOPUS_CORE}, got {n_core}", errors)
        if n_unique != SCOPUS_UNIQUE:
            _fail(f"Scopus unique: expected {SCOPUS_UNIQUE}, got {n_unique}", errors)

    # --- WoS ---
    wos_core = ROOT / "data/automatic/web_of_science/wos_core.csv"
    wos_unique = ROOT / "data/automatic/web_of_science/wos_unique.csv"
    if wos_core.is_file() and wos_unique.is_file():
        n_core = len(pd.read_csv(wos_core))
        n_unique = len(pd.read_csv(wos_unique))
        print(f"WoS: {n_core} core / {n_unique} unique")
        if n_core != WOS_CORE:
            _fail(f"WoS core: expected {WOS_CORE}, got {n_core}", errors)
        if n_unique != WOS_UNIQUE:
            _fail(f"WoS unique: expected {WOS_UNIQUE}, got {n_unique}", errors)

    # --- Selection funnels ---
    def stage_counts(view: str) -> dict[str, int]:
        base = ROOT / "data/automatic/selection" / view
        return {
            name: len(pd.read_csv(base / f"{name}.csv"))
            for name in (
                "merged",
                "unique",
                "english",
                "proceedings_filtered",
                "candidates",
            )
        }

    for view, expected in (
        (VIEW_HISTORICAL, EXPECTED_HISTORICAL),
        (VIEW_CORRECTED, EXPECTED_CORRECTED),
    ):
        base = ROOT / "data/automatic/selection" / view
        if not (base / "merged.csv").is_file():
            continue
        counts = stage_counts(view)
        arrow = (
            f"{counts['merged']} → {counts['unique']} → {counts['english']} → "
            f"{counts['proceedings_filtered']} → {counts['candidates']}"
        )
        print(f"{view.capitalize()} selection: {arrow}")
        for key, exp in expected.items():
            if counts[key] != exp:
                _fail(f"{view}/{key}: expected {exp}, got {counts[key]}", errors)
        for name in expected:
            df = pd.read_csv(base / f"{name}.csv")
            if PIPELINE_VIEW_COLUMN not in df.columns:
                _fail(f"{view}/{name}.csv missing {PIPELINE_VIEW_COLUMN}", errors)
            elif not (df[PIPELINE_VIEW_COLUMN] == view).all():
                _fail(f"{view}/{name}.csv has mixed/wrong pipeline_view", errors)

    # --- Manual ---
    study_path = ROOT / "data/manual/study_selection.csv"
    if study_path.is_file():
        study = pd.read_csv(study_path)
        states = study["choosen_state"].value_counts()
        yes = int(states.get("Yes", 0))
        no = int(states.get("No", 0))
        doubt = int(states.get("Doubt", 0))
        print(f"Manual: Yes {yes} / No {no} / Doubt {doubt} (total {len(study)})")
        if len(study) != EXPECTED_MANUAL_CANDIDATES:
            _fail(
                f"manual total: expected {EXPECTED_MANUAL_CANDIDATES}, got {len(study)}",
                errors,
            )
        if yes != EXPECTED_MANUAL_YES:
            _fail(f"manual Yes: expected {EXPECTED_MANUAL_YES}, got {yes}", errors)
        if no != EXPECTED_MANUAL_NO:
            _fail(f"manual No: expected {EXPECTED_MANUAL_NO}, got {no}", errors)
        if doubt != EXPECTED_MANUAL_DOUBT:
            _fail(f"manual Doubt: expected {EXPECTED_MANUAL_DOUBT}, got {doubt}", errors)
        if (
            study["title"]
            .astype(str)
            .str.contains("Ancient Chinese", case=False, na=False)
            .any()
        ):
            _fail("Ancient Chinese must not appear in historical manual selection", errors)

    # --- Final ---
    corpus_path = ROOT / "data/final/final_corpus.csv"
    if corpus_path.is_file():
        corpus = pd.read_csv(corpus_path)
        print(f"Final corpus: {len(corpus)} unique studies")
        if len(corpus) != EXPECTED_FINAL_CORPUS:
            _fail(f"final corpus: expected {EXPECTED_FINAL_CORPUS}, got {len(corpus)}", errors)
        if corpus["paper_id"].nunique() != len(corpus):
            _fail("final_corpus paper_id values are not unique", errors)

    # --- Process statistics (read-only: compare stored vs recomputed) ---
    stats_path = ROOT / PROCESS_STATISTICS_REL
    if stats_path.is_file():
        stored = pd.read_csv(stats_path)
        computed = compute_process_statistics(ROOT)
        expected = expected_process_statistics()
        for (stage, metric), exp_count in expected.items():
            try:
                got = statistics_lookup(stored, stage, metric)
            except KeyError as exc:
                _fail(str(exc), errors)
                continue
            if got["count"] != exp_count:
                _fail(
                    f"stats {stage}/{metric}: expected {exp_count}, got {got['count']}",
                    errors,
                )
        for row in computed:
            try:
                got = statistics_lookup(stored, row.stage, row.metric)
            except KeyError as exc:
                _fail(str(exc), errors)
                continue
            if got["count"] != row.count:
                _fail(
                    f"stats {row.stage}/{row.metric} stored {got['count']} "
                    f"!= computed {row.count}",
                    errors,
                )
            if row.percentage is not None:
                if got["percentage"] is None or abs(
                    float(got["percentage"]) - float(row.percentage)
                ) > 1e-9:
                    _fail(
                        f"stats {row.stage}/{row.metric} percentage mismatch",
                        errors,
                    )
        print(f"Process statistics: {stats_path.relative_to(ROOT)} OK")

    # --- Qualitative invariants ---
    hist_proc = ROOT / "data/automatic/selection/historical/proceedings_filtered.csv"
    hist_cand = ROOT / "data/automatic/selection/historical/candidates.csv"
    corr_cand = ROOT / "data/automatic/selection/corrected/candidates.csv"
    corr_unique = ROOT / "data/automatic/selection/corrected/unique.csv"

    if hist_proc.is_file() and hist_cand.is_file():
        proc = pd.read_csv(hist_proc)
        cand = pd.read_csv(hist_cand)
        terl_proc = proc[
            proc["title"].astype(str).str.contains("TERL:", case=False, na=False)
        ]
        terl_cand = cand[
            cand["title"].astype(str).str.contains("TERL:", case=False, na=False)
        ]
        if len(terl_proc) < 2:
            _fail(f"TERL before normalization: expected ≥2, got {len(terl_proc)}", errors)
        else:
            eids = set(terl_proc["eid"].dropna().astype(str))
            if not TERL_EIDS.issubset(eids):
                _fail(f"TERL EIDs incomplete: {eids}", errors)
        if len(terl_cand) != 1:
            _fail(f"TERL after normalization: expected 1, got {len(terl_cand)}", errors)

    if corr_cand.is_file():
        cand = pd.read_csv(corr_cand)
        ancient = cand[
            cand["title"].astype(str).str.contains(
                "Ancient Chinese Documents", case=False, na=False
            )
        ]
        if len(ancient) != 1:
            _fail(
                f"Ancient Chinese in corrected candidates: expected 1, got {len(ancient)}",
                errors,
            )
        elif normalize_title(ancient.iloc[0]["title"]) != normalize_title(
            ANCIENT_CHINESE_TITLE
        ):
            _fail("Ancient Chinese title mismatch in corrected candidates", errors)

    if corr_unique.is_file():
        uniq = pd.read_csv(corr_unique)
        dois = uniq["doi"].map(normalize_doi)
        kbpt = uniq[dois == KBPT_DOI_NORMALIZED]
        engines = set(kbpt["search_engine"].dropna().astype(str))
        if "Scopus" not in engines or "Web of Science" not in engines:
            _fail(
                "KBPT DOI collision must include Scopus and Web of Science rows",
                errors,
            )

    print()
    print("WARNING:")
    print(PUBLISHED_FINAL_COUNT_WARNING)
    print()

    if errors:
        print("FAIL:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
