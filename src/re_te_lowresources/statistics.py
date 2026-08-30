"""Derive Paper-1 process statistics from public canonical artifacts.

Statistics are computed from platform CSVs, Selection funnel CSVs, manual
exports, and ``final_corpus.csv``. They are not an independent authoritative
source. Free / Peer-review stages are intentionally omitted (no reproducible
count transformation).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

from re_te_lowresources.io_util import write_csv_rows_if_changed
from re_te_lowresources.scopus import EXPECTED_CORE_ROWS as SCOPUS_CORE
from re_te_lowresources.scopus import EXPECTED_UNIQUE_ROWS as SCOPUS_UNIQUE
from re_te_lowresources.selection import (
    EXPECTED_CORRECTED,
    EXPECTED_FINAL_CORPUS,
    EXPECTED_HISTORICAL,
    EXPECTED_MANUAL_CANDIDATES,
    EXPECTED_MANUAL_DOUBT,
    EXPECTED_MANUAL_NO,
    EXPECTED_MANUAL_YES,
)
from re_te_lowresources.web_of_science import EXPECTED_CORE_ROWS as WOS_CORE
from re_te_lowresources.web_of_science import EXPECTED_UNIQUE_ROWS as WOS_UNIQUE

PROCESS_STATISTICS_REL = Path("data/final/process_statistics.csv")
PROCESS_STATISTICS_COLUMNS = [
    "stage",
    "metric",
    "count",
    "denominator",
    "percentage",
    "notes",
]

# Display rounding only; stored percentages keep full float precision.
DISPLAY_PERCENT_DECIMALS = 1


@dataclass(frozen=True)
class StatRow:
    stage: str
    metric: str
    count: int
    denominator: int | None = None
    percentage: float | None = None
    notes: str = ""


def _pct(count: int, denominator: int) -> float:
    if denominator == 0:
        raise ValueError("percentage denominator must be non-zero")
    return (count / denominator) * 100.0


def format_percentage(
    percentage: float | None, decimals: int = DISPLAY_PERCENT_DECIMALS
) -> str:
    if percentage is None:
        return ""
    return f"{percentage:.{decimals}f}"


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def compute_process_statistics(root: Path | None = None) -> list[StatRow]:
    """Compute long-format process statistics from public artifacts."""
    root = Path(root).resolve() if root is not None else default_repo_root()

    n_scopus_core = len(pd.read_csv(root / "data/automatic/scopus/scopus_core.csv"))
    n_scopus_unique = len(pd.read_csv(root / "data/automatic/scopus/scopus_unique.csv"))
    n_wos_core = len(pd.read_csv(root / "data/automatic/web_of_science/wos_core.csv"))
    n_wos_unique = len(pd.read_csv(root / "data/automatic/web_of_science/wos_unique.csv"))

    def funnel_counts(view: str) -> dict[str, int]:
        base = root / "data/automatic/selection" / view
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

    hist = funnel_counts("historical")
    corr = funnel_counts("corrected")

    study = pd.read_csv(root / "data/manual/study_selection.csv")
    states = study["choosen_state"].value_counts()
    n_yes = int(states.get("Yes", 0))
    n_no = int(states.get("No", 0))
    n_doubt = int(states.get("Doubt", 0))
    n_candidates = int(len(study))

    corpus = pd.read_csv(root / "data/final/final_corpus.csv")
    n_final = int(len(corpus))

    rows: list[StatRow] = [
        StatRow("platform_scopus", "core", n_scopus_core),
        StatRow("platform_scopus", "unique", n_scopus_unique),
        StatRow("platform_wos", "core", n_wos_core),
        StatRow("platform_wos", "unique", n_wos_unique),
        StatRow("selection_historical", "merged", hist["merged"]),
        StatRow("selection_historical", "unique", hist["unique"]),
        StatRow("selection_historical", "english", hist["english"]),
        StatRow(
            "selection_historical",
            "author_metadata_filtered",
            hist["proceedings_filtered"],
            notes="required author metadata present (proceedings-like shell filter)",
        ),
        StatRow(
            "selection_historical",
            "normalized_candidates",
            hist["candidates"],
            notes="normalized-title collapse (TERL dual bibliographic rows)",
        ),
        StatRow("selection_corrected", "merged", corr["merged"]),
        StatRow("selection_corrected", "unique", corr["unique"]),
        StatRow("selection_corrected", "english", corr["english"]),
        StatRow(
            "selection_corrected",
            "author_metadata_filtered",
            corr["proceedings_filtered"],
            notes="required author metadata present",
        ),
        StatRow(
            "selection_corrected",
            "normalized_candidates",
            corr["candidates"],
            notes="normalized-title collapse",
        ),
        StatRow("manual", "candidates", n_candidates),
        StatRow(
            "manual",
            "yes",
            n_yes,
            n_candidates,
            _pct(n_yes, n_candidates),
            notes="among historical manual candidates",
        ),
        StatRow(
            "manual",
            "no",
            n_no,
            n_candidates,
            _pct(n_no, n_candidates),
            notes="among historical manual candidates",
        ),
        StatRow(
            "manual",
            "doubt",
            n_doubt,
            n_candidates,
            _pct(n_doubt, n_candidates),
            notes="among historical manual candidates",
        ),
        StatRow(
            "final",
            "recoverable_corpus",
            n_final,
            notes="canonical recoverable analytical corpus (published narrative reports 43)",
        ),
    ]
    return rows


def expected_process_statistics() -> dict[tuple[str, str], int]:
    """Expected (stage, metric) → count for validation."""
    return {
        ("platform_scopus", "core"): SCOPUS_CORE,
        ("platform_scopus", "unique"): SCOPUS_UNIQUE,
        ("platform_wos", "core"): WOS_CORE,
        ("platform_wos", "unique"): WOS_UNIQUE,
        ("selection_historical", "merged"): EXPECTED_HISTORICAL["merged"],
        ("selection_historical", "unique"): EXPECTED_HISTORICAL["unique"],
        ("selection_historical", "english"): EXPECTED_HISTORICAL["english"],
        ("selection_historical", "author_metadata_filtered"): EXPECTED_HISTORICAL[
            "proceedings_filtered"
        ],
        ("selection_historical", "normalized_candidates"): EXPECTED_HISTORICAL[
            "candidates"
        ],
        ("selection_corrected", "merged"): EXPECTED_CORRECTED["merged"],
        ("selection_corrected", "unique"): EXPECTED_CORRECTED["unique"],
        ("selection_corrected", "english"): EXPECTED_CORRECTED["english"],
        ("selection_corrected", "author_metadata_filtered"): EXPECTED_CORRECTED[
            "proceedings_filtered"
        ],
        ("selection_corrected", "normalized_candidates"): EXPECTED_CORRECTED[
            "candidates"
        ],
        ("manual", "candidates"): EXPECTED_MANUAL_CANDIDATES,
        ("manual", "yes"): EXPECTED_MANUAL_YES,
        ("manual", "no"): EXPECTED_MANUAL_NO,
        ("manual", "doubt"): EXPECTED_MANUAL_DOUBT,
        ("final", "recoverable_corpus"): EXPECTED_FINAL_CORPUS,
    }


def statistics_to_records(rows: Iterable[StatRow]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for row in rows:
        records.append(
            {
                "stage": row.stage,
                "metric": row.metric,
                "count": row.count,
                "denominator": "" if row.denominator is None else row.denominator,
                "percentage": "" if row.percentage is None else row.percentage,
                "notes": row.notes,
            }
        )
    return records


def write_process_statistics(root: Path | None = None, path: Path | None = None) -> Path:
    """Derive and write ``data/final/process_statistics.csv`` if content changed."""
    root = Path(root).resolve() if root is not None else default_repo_root()
    out = Path(path) if path is not None else root / PROCESS_STATISTICS_REL
    rows = compute_process_statistics(root)
    records = statistics_to_records(rows)
    # Normalize percentage serialization for stable bytes.
    serialized: list[dict[str, Any]] = []
    for rec in records:
        pct = rec["percentage"]
        if pct == "":
            pct_out = ""
        else:
            pct_out = f"{float(pct):.12f}".rstrip("0").rstrip(".")
        serialized.append(
            {
                "stage": rec["stage"],
                "metric": rec["metric"],
                "count": int(rec["count"]),
                "denominator": ""
                if rec["denominator"] == ""
                else int(rec["denominator"]),
                "percentage": pct_out,
                "notes": rec["notes"],
            }
        )
    return write_csv_rows_if_changed(out, serialized, PROCESS_STATISTICS_COLUMNS)


def load_process_statistics(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def statistics_lookup(df: pd.DataFrame, stage: str, metric: str) -> dict[str, Any]:
    hit = df[(df["stage"] == stage) & (df["metric"] == metric)]
    if len(hit) != 1:
        raise KeyError(f"expected one row for {stage}/{metric}, got {len(hit)}")
    row = hit.iloc[0]
    return {
        "count": int(row["count"]),
        "denominator": None
        if pd.isna(row["denominator"]) or row["denominator"] == ""
        else int(row["denominator"]),
        "percentage": None
        if pd.isna(row["percentage"]) or row["percentage"] == ""
        else float(row["percentage"]),
    }
