"""Dual-view Selection stage: HISTORICAL reproduction vs CORRECTED pipeline.

Public boundary
---------------
Inputs are platform-deduplicated CSVs from the Scopus and WoS stages:

* ``data/automatic/scopus/scopus_unique.csv`` (164)
* ``data/automatic/web_of_science/wos_unique.csv`` (62)

No live database queries. Manual screening evidence is read from
``data/final/summary_reduced.xlsx`` (not modified).

Two views (never silently mixed)
--------------------------------
**HISTORICAL REPRODUCTION** — reconstructs the Paper-1 notebook path that
reindexed Web of Science onto Scopus column names *without* applying the
intended rename map. That defect nulls WoS ``title`` / language / author IDs
and yields the published automatic funnel 226 → 165 → 159 → 135 → 134.

**CORRECTED PIPELINE** — applies the intended Scopus ↔ WoS schema alignment,
then the same title-based scientific filters. Funnel: 226 → 173 → 168 → 140 → 135.

Candidate normalization (135 → 134 historically)
-----------------------------------------------
Collapse bibliographic rows that share a normalized title. The only
within-Scopus pair responsible for the historical −1 is TERL (two EIDs).
``research_methodology.xlsx`` labels that step ``Free``; artifacts do not
support a free-access exclusion — do not model it as Free.

Published final count
--------------------
Preserved analytical artifacts contain **42** studies. The article/README
text reports **43**. This module never invents a 43rd study.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import pandas as pd

TITLE_COLUMN = "title"
LANGUAGE_COLUMN = "language of original document"
AUTHOR_FILTER_COLUMNS: tuple[str, ...] = (
    "authors",
    "author full names",
    "author(s) id",
)
SEARCH_ENGINE_COLUMN = "search_engine"
QUERY_COLUMN = "query"
DOI_COLUMN = "doi"
EID_COLUMN = "eid"

VIEW_HISTORICAL: Literal["historical"] = "historical"
VIEW_CORRECTED: Literal["corrected"] = "corrected"
PIPELINE_VIEW_COLUMN = "pipeline_view"

# Intended WoS → Scopus rename (lowercased names), from seleccion.ipynb.
WOS_TO_SCOPUS_RENAME: dict[str, str] = {
    "article title": "title",
    "start page": "page start",
    "end page": "page end",
    "cited references": "references",
    "publication year": "year",
    "language": "language of original document",
    "journal iso abbreviation": "abbreviated source title",
    "article number": "art. no.",
    "funding name preferred": "funding details",
    "researcher ids": "author(s) id",
    "orcids": "author(s) id",
    "doi link": "link",
    "times cited, all databases": "cited by",
    "conference title": "conference name",
    # Deterministic extras that preserve identifiers without changing filters.
    "ut (unique wos id)": "eid",
}

# Canonical fields preferred first in written CSVs (order stable).
CANONICAL_FIELD_ORDER: tuple[str, ...] = (
    PIPELINE_VIEW_COLUMN,
    "title",
    "year",
    "language of original document",
    "authors",
    "author full names",
    "author(s) id",
    "doi",
    "abstract",
    "source title",
    "document type",
    "affiliations",
    "author keywords",
    "publisher",
    "issn",
    "isbn",
    "volume",
    "issue",
    "pubmed id",
    "conference date",
    "conference location",
    "conference name",
    "abbreviated source title",
    "page start",
    "page end",
    "art. no.",
    "cited by",
    "references",
    "funding details",
    "link",
    "eid",
    "query",
    "search_engine",
)

EXPECTED_SCOPUS_UNIQUE = 164
EXPECTED_WOS_UNIQUE = 62
EXPECTED_MERGED = 226

EXPECTED_HISTORICAL = {
    "merged": 226,
    "unique": 165,
    "english": 159,
    "proceedings_filtered": 135,
    "candidates": 134,
}
EXPECTED_CORRECTED = {
    "merged": 226,
    "unique": 173,
    "english": 168,
    "proceedings_filtered": 140,
    "candidates": 135,
}

EXPECTED_MANUAL_YES = 47
EXPECTED_MANUAL_NO = 69
EXPECTED_MANUAL_DOUBT = 18
EXPECTED_MANUAL_CANDIDATES = 134
EXPECTED_FINAL_CORPUS = 42

TERL_EIDS: frozenset[str] = frozenset(
    {"2-s2.0-85218049221", "2-s2.0-85174436404"}
)
ANCIENT_CHINESE_TITLE = "Few-Shot Relation Extraction on Ancient Chinese Documents"
KBPT_DOI_NORMALIZED = "10.7717/peerj-cs.2014"

STAGE_NAMES: tuple[str, ...] = (
    "merged",
    "unique",
    "english",
    "proceedings_filtered",
    "candidates",
)

PUBLISHED_FINAL_COUNT_WARNING = (
    "Published paper reports 43 final studies; preserved final analytical "
    "artifacts contain 42."
)


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class SelectionPaths:
    root: Path
    scopus_unique: Path
    wos_unique: Path
    summary_xlsx: Path
    historical_dir: Path
    corrected_dir: Path
    manual_dir: Path
    final_dir: Path

    @classmethod
    def from_root(cls, root: Path | None = None) -> "SelectionPaths":
        root = (root or default_repo_root()).resolve()
        auto = root / "data" / "automatic" / "selection"
        return cls(
            root=root,
            scopus_unique=root / "data" / "automatic" / "scopus" / "scopus_unique.csv",
            wos_unique=root
            / "data"
            / "automatic"
            / "web_of_science"
            / "wos_unique.csv",
            summary_xlsx=root / "data" / "final" / "summary_reduced.xlsx",
            historical_dir=auto / VIEW_HISTORICAL,
            corrected_dir=auto / VIEW_CORRECTED,
            manual_dir=root / "data" / "manual",
            final_dir=root / "data" / "final",
        )


def normalize_title(value: object) -> str:
    """Normalize titles for candidate collapse / diagnostics (not cross-platform dedup)."""
    if not isinstance(value, str):
        return ""
    text = value.strip().lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_doi(value: object) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if pd.isna(value):
        return None
    text = str(value).strip().lower()
    text = text.replace("https://doi.org/", "").replace("http://dx.doi.org/", "")
    text = text.strip()
    return text or None


def _lowercase_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip().lower() for c in out.columns]
    return out


def combine_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Coalesce identically named columns (first non-null per row), keep first."""
    out = df.copy()
    for col in list(dict.fromkeys(out.columns)):
        if list(out.columns).count(col) > 1:
            block = out.loc[:, out.columns == col]
            out[col] = block.bfill(axis=1).iloc[:, 0]
            out = out.loc[:, ~out.columns.duplicated(keep="first")]
    return out


def _stable_column_order(columns: list[str]) -> list[str]:
    preferred = [c for c in CANONICAL_FIELD_ORDER if c in columns]
    rest = sorted(c for c in columns if c not in preferred)
    return preferred + rest


def _tag_view(df: pd.DataFrame, view: str) -> pd.DataFrame:
    out = df.copy()
    out[PIPELINE_VIEW_COLUMN] = view
    return out.reindex(columns=_stable_column_order(list(out.columns)))


def load_platform_uniques(
    paths: SelectionPaths | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load Scopus/WoS unique CSVs; enforce expected platform counts."""
    paths = paths or SelectionPaths.from_root()
    if not paths.scopus_unique.is_file():
        raise FileNotFoundError(f"Missing Scopus unique CSV: {paths.scopus_unique}")
    if not paths.wos_unique.is_file():
        raise FileNotFoundError(f"Missing WoS unique CSV: {paths.wos_unique}")

    scopus = pd.read_csv(paths.scopus_unique)
    wos = pd.read_csv(paths.wos_unique)
    if len(scopus) != EXPECTED_SCOPUS_UNIQUE:
        raise AssertionError(
            f"Scopus unique rows: expected {EXPECTED_SCOPUS_UNIQUE}, got {len(scopus)}"
        )
    if len(wos) != EXPECTED_WOS_UNIQUE:
        raise AssertionError(
            f"WoS unique rows: expected {EXPECTED_WOS_UNIQUE}, got {len(wos)}"
        )
    return scopus, wos


def prepare_scopus_frame(scopus: pd.DataFrame) -> pd.DataFrame:
    out = _lowercase_columns(scopus)
    out[SEARCH_ENGINE_COLUMN] = "Scopus"
    return out


def prepare_wos_corrected(wos: pd.DataFrame) -> pd.DataFrame:
    """Intended alignment: rename + coalesce Researcher Ids/ORCIDs into author(s) id."""
    out = _lowercase_columns(wos)
    out[SEARCH_ENGINE_COLUMN] = "Web of Science"
    out = out.rename(columns=WOS_TO_SCOPUS_RENAME)
    out = combine_duplicate_columns(out)
    return out


def prepare_wos_historical_defect(
    wos: pd.DataFrame, scopus_columns: list[str]
) -> pd.DataFrame:
    """HISTORICAL DEFECT: lowercase then reindex to Scopus columns without rename.

    This is compatibility reconstruction only — not recommended processing.
    """
    out = _lowercase_columns(wos)
    out[SEARCH_ENGINE_COLUMN] = "Web of Science"
    # Drop WoS-only names that are not in Scopus schema; null out renamed fields.
    return out.reindex(columns=scopus_columns)


def build_corrected_merged(
    scopus: pd.DataFrame, wos: pd.DataFrame
) -> pd.DataFrame:
    sc = prepare_scopus_frame(scopus)
    wo = prepare_wos_corrected(wos)
    # Union of columns: retain unmapped WoS-only fields deterministically.
    merged = pd.concat([sc, wo], ignore_index=True, sort=False)
    drop = [c for c in merged.columns if str(c).startswith("unnamed")]
    if drop:
        merged = merged.drop(columns=drop)
    return _tag_view(merged, VIEW_CORRECTED)


def build_historical_merged(
    scopus: pd.DataFrame, wos: pd.DataFrame
) -> pd.DataFrame:
    sc = prepare_scopus_frame(scopus)
    wo = prepare_wos_historical_defect(wos, list(sc.columns))
    merged = pd.concat([sc, wo], ignore_index=True, sort=False)
    drop = [c for c in merged.columns if str(c).startswith("unnamed")]
    if drop:
        merged = merged.drop(columns=drop)
    return _tag_view(merged, VIEW_HISTORICAL)


def deduplicate_exact_title(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-platform dedup rule: exact ``title``, keep first (Scopus precedes WoS)."""
    if TITLE_COLUMN not in df.columns:
        raise KeyError(f"Missing {TITLE_COLUMN!r}")
    return df.drop_duplicates(subset=TITLE_COLUMN, keep="first").reset_index(drop=True)


def filter_english(df: pd.DataFrame) -> pd.DataFrame:
    if LANGUAGE_COLUMN not in df.columns:
        raise KeyError(f"Missing {LANGUAGE_COLUMN!r}")
    return df[df[LANGUAGE_COLUMN] == "English"].reset_index(drop=True)


def filter_required_author_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """Historical 'remove proceedings' step: dropna on author identity fields."""
    missing = [c for c in AUTHOR_FILTER_COLUMNS if c not in df.columns]
    if missing:
        raise KeyError(f"Missing author filter columns: {missing}")
    return df.dropna(subset=list(AUTHOR_FILTER_COLUMNS)).reset_index(drop=True)


def normalize_candidate_titles(df: pd.DataFrame) -> pd.DataFrame:
    """Collapse equivalent normalized titles (TERL pair → historical 134)."""
    out = df.copy()
    out["_normalized_title"] = out[TITLE_COLUMN].map(normalize_title)
    out = out.drop_duplicates(subset="_normalized_title", keep="first").reset_index(
        drop=True
    )
    return out.drop(columns=["_normalized_title"])


@dataclass
class FunnelFrames:
    view: str
    merged: pd.DataFrame
    unique: pd.DataFrame
    english: pd.DataFrame
    proceedings_filtered: pd.DataFrame
    candidates: pd.DataFrame

    def counts(self) -> dict[str, int]:
        return {
            "merged": len(self.merged),
            "unique": len(self.unique),
            "english": len(self.english),
            "proceedings_filtered": len(self.proceedings_filtered),
            "candidates": len(self.candidates),
        }

    def as_dict(self) -> dict[str, pd.DataFrame]:
        return {
            "merged": self.merged,
            "unique": self.unique,
            "english": self.english,
            "proceedings_filtered": self.proceedings_filtered,
            "candidates": self.candidates,
        }


def run_funnel(merged: pd.DataFrame, view: str) -> FunnelFrames:
    if PIPELINE_VIEW_COLUMN in merged.columns:
        views = set(merged[PIPELINE_VIEW_COLUMN].dropna().unique())
        if views and views != {view}:
            raise ValueError(
                f"Refusing to run funnel: frame tagged {views}, expected {{{view}}}"
            )
    merged = _ensure_view(merged, view)
    unique = _ensure_view(deduplicate_exact_title(merged), view)
    english = _ensure_view(filter_english(unique), view)
    proceedings = _ensure_view(filter_required_author_metadata(english), view)
    candidates = _ensure_view(normalize_candidate_titles(proceedings), view)
    return FunnelFrames(
        view=view,
        merged=merged,
        unique=unique,
        english=english,
        proceedings_filtered=proceedings,
        candidates=candidates,
    )


def _ensure_view(df: pd.DataFrame, view: str) -> pd.DataFrame:
    if PIPELINE_VIEW_COLUMN not in df.columns:
        return _tag_view(df, view)
    out = df.copy()
    out[PIPELINE_VIEW_COLUMN] = view
    return out.reindex(columns=_stable_column_order(list(out.columns)))


def build_historical_funnel(
    scopus: pd.DataFrame | None = None,
    wos: pd.DataFrame | None = None,
    paths: SelectionPaths | None = None,
) -> FunnelFrames:
    if scopus is None or wos is None:
        scopus, wos = load_platform_uniques(paths)
    merged = build_historical_merged(scopus, wos)
    return run_funnel(merged, VIEW_HISTORICAL)


def build_corrected_funnel(
    scopus: pd.DataFrame | None = None,
    wos: pd.DataFrame | None = None,
    paths: SelectionPaths | None = None,
) -> FunnelFrames:
    if scopus is None or wos is None:
        scopus, wos = load_platform_uniques(paths)
    merged = build_corrected_merged(scopus, wos)
    return run_funnel(merged, VIEW_CORRECTED)


def write_funnel_outputs(funnel: FunnelFrames, output_dir: Path) -> dict[str, Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    for name, frame in funnel.as_dict().items():
        path = output_dir / f"{name}.csv"
        frame.to_csv(path, index=False)
        written[name] = path
    return written


def validate_funnel_counts(
    funnel: FunnelFrames, expected: dict[str, int]
) -> None:
    counts = funnel.counts()
    errors: list[str] = []
    for key, exp in expected.items():
        got = counts[key]
        if got != exp:
            errors.append(f"{funnel.view}/{key}: expected {exp}, got {got}")
    if funnel.view == VIEW_HISTORICAL:
        # TERL must still be two rows before candidate normalization.
        proc = funnel.proceedings_filtered
        terl = proc[
            proc[TITLE_COLUMN]
            .astype(str)
            .str.contains(r"TERL:", case=False, na=False, regex=True)
        ]
        if len(terl) < 2:
            errors.append(f"historical proceedings TERL rows: expected ≥2, got {len(terl)}")
        if EID_COLUMN in terl.columns:
            eids = set(terl[EID_COLUMN].dropna().astype(str))
            if not TERL_EIDS.issubset(eids):
                errors.append(f"TERL EIDs incomplete: {eids}")
        cand = funnel.candidates
        terl_c = cand[
            cand[TITLE_COLUMN]
            .astype(str)
            .str.contains(r"TERL:", case=False, na=False, regex=True)
        ]
        if len(terl_c) != 1:
            errors.append(f"historical candidates TERL rows: expected 1, got {len(terl_c)}")
    if funnel.view == VIEW_CORRECTED:
        cand = funnel.candidates
        ancient = cand[
            cand[TITLE_COLUMN].astype(str).str.contains(
                "Ancient Chinese Documents", case=False, na=False
            )
        ]
        if len(ancient) != 1:
            errors.append(
                f"corrected candidates must include Ancient Chinese Documents; found {len(ancient)}"
            )
    if errors:
        raise AssertionError(
            "Selection funnel invariants failed:\n  - " + "\n  - ".join(errors)
        )


def _require_openpyxl() -> None:
    try:
        import openpyxl  # noqa: F401
    except ImportError as exc:
        raise ImportError(
            "openpyxl is required to read summary_reduced.xlsx for manual/final exports"
        ) from exc


def load_study_selection_sheet(summary_xlsx: Path) -> pd.DataFrame:
    _require_openpyxl()
    df = pd.read_excel(summary_xlsx, sheet_name="Study selection")
    # Drop trailing empty rows without titles.
    df = df[df["title"].notna()].copy()
    return df.reset_index(drop=True)


def export_study_selection_csv(
    summary_xlsx: Path, output_path: Path
) -> pd.DataFrame:
    """Deterministic export of the 134 historical manual candidates."""
    df = load_study_selection_sheet(summary_xlsx)
    if len(df) != EXPECTED_MANUAL_CANDIDATES:
        raise AssertionError(
            f"Study selection titled rows: expected {EXPECTED_MANUAL_CANDIDATES}, got {len(df)}"
        )
    states = df["choosen_state"].value_counts()
    for label, exp in (
        ("Yes", EXPECTED_MANUAL_YES),
        ("No", EXPECTED_MANUAL_NO),
        ("Doubt", EXPECTED_MANUAL_DOUBT),
    ):
        got = int(states.get(label, 0))
        if got != exp:
            raise AssertionError(f"choosen_state {label}: expected {exp}, got {got}")

    keep = [
        c
        for c in [
            "title",
            "doi",
            "eid",
            "year",
            "authors",
            "author full names",
            "author(s) id",
            "source title",
            "document type",
            "language of original document",
            "query",
            "search_engine",
            "choosen",
            "choosen_state",
            "downloaded",
            "done",
            "notes",
            "full text",
            "abstract.1",
            "title.1",
        ]
        if c in df.columns
    ]
    out = df[keep].copy()
    # paper_id is not native on this sheet; leave empty placeholder for schema stability.
    out.insert(0, "paper_id", pd.NA)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)
    return out


def export_final_selection_csv(
    summary_xlsx: Path, output_path: Path
) -> pd.DataFrame:
    """47 first-pass Yes records + whether each is in the recoverable final corpus."""
    _require_openpyxl()
    study = load_study_selection_sheet(summary_xlsx)
    yes = study[study["choosen_state"] == "Yes"].copy()
    if len(yes) != EXPECTED_MANUAL_YES:
        raise AssertionError(f"Yes rows: expected {EXPECTED_MANUAL_YES}, got {len(yes)}")

    de = pd.read_excel(summary_xlsx, sheet_name="Data extraction (2)")
    summary = pd.read_excel(summary_xlsx, sheet_name="Summary table ")
    de = de.copy()
    de["_nt"] = de["Title"].map(normalize_title)
    yes["_nt"] = yes["title"].map(normalize_title)
    final_ids = set(summary["Paper ID"].dropna().astype(str))

    merged = yes.merge(
        de[["_nt", "Paper ID", "Solution name", "Title"]],
        on="_nt",
        how="left",
        validate="one_to_one",
    )
    if merged["Paper ID"].isna().any():
        missing = merged.loc[merged["Paper ID"].isna(), "title"].tolist()
        raise AssertionError(f"Yes titles not matched to Data extraction: {missing}")

    merged["in_final_corpus"] = merged["Paper ID"].astype(str).isin(final_ids)
    merged["has_solution_name"] = merged["Solution name"].notna()
    # Validate non-final set from workbook (solution-empty / not in summary).
    non_final = sorted(
        merged.loc[~merged["in_final_corpus"], "Paper ID"].astype(str).tolist()
    )
    if len(merged[merged["in_final_corpus"]]) != EXPECTED_FINAL_CORPUS:
        raise AssertionError(
            "Yes-in-final count: expected "
            f"{EXPECTED_FINAL_CORPUS}, got {int(merged['in_final_corpus'].sum())}"
        )
    if len(non_final) != EXPECTED_MANUAL_YES - EXPECTED_FINAL_CORPUS:
        raise AssertionError(f"Unexpected non-final Yes IDs: {non_final}")

    out = pd.DataFrame(
        {
            "paper_id": merged["Paper ID"].astype(str),
            "title": merged["title"],
            "doi": merged["doi"] if "doi" in merged.columns else pd.NA,
            "year": merged["year"] if "year" in merged.columns else pd.NA,
            "authors": merged["authors"] if "authors" in merged.columns else pd.NA,
            "choosen": merged["choosen"] if "choosen" in merged.columns else pd.NA,
            "choosen_state": merged["choosen_state"],
            "notes": merged["notes"] if "notes" in merged.columns else pd.NA,
            "solution_name": merged["Solution name"],
            "in_final_corpus": merged["in_final_corpus"],
            "has_solution_name": merged["has_solution_name"],
        }
    )
    # Deterministic order by paper_id.
    out = out.sort_values("paper_id").reset_index(drop=True)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)
    return out


def export_final_corpus_csv(
    summary_xlsx: Path, output_path: Path
) -> pd.DataFrame:
    """42-study recoverable analytical corpus from Summary table (+ solution check)."""
    _require_openpyxl()
    summary = pd.read_excel(summary_xlsx, sheet_name="Summary table ")
    de = pd.read_excel(summary_xlsx, sheet_name="Data extraction (2)")
    with_sol = de[de["Solution name"].notna()].copy()
    sum_ids = set(summary["Paper ID"].dropna().astype(str))
    sol_ids = set(with_sol["Paper ID"].dropna().astype(str))
    if sum_ids != sol_ids:
        raise AssertionError(
            "Summary table Paper IDs must match Data extraction rows with Solution name"
        )
    if len(summary) != EXPECTED_FINAL_CORPUS:
        raise AssertionError(
            f"Final corpus: expected {EXPECTED_FINAL_CORPUS}, got {len(summary)}"
        )

    # Enrich with solution name from DE for auditability.
    out = summary.merge(
        with_sol[["Paper ID", "Solution name", "Query"]],
        on="Paper ID",
        how="left",
        validate="one_to_one",
    )
    out = out.rename(
        columns={
            "Paper ID": "paper_id",
            "Title": "title",
            "Authors": "authors",
            "Year": "year",
            "Venue": "venue",
            "Solution name": "solution_name",
            "Query": "query",
        }
    )
    out = out.sort_values("paper_id").reset_index(drop=True)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)
    return out


@dataclass
class SelectionReproductionResult:
    historical: FunnelFrames
    corrected: FunnelFrames
    historical_paths: dict[str, Path] = field(default_factory=dict)
    corrected_paths: dict[str, Path] = field(default_factory=dict)
    study_selection_path: Path | None = None
    final_selection_path: Path | None = None
    final_corpus_path: Path | None = None
    published_final_warning: str = PUBLISHED_FINAL_COUNT_WARNING


def reproduce_selection(
    root: Path | None = None,
    *,
    validate: bool = True,
    write: bool = True,
) -> SelectionReproductionResult:
    """Run HISTORICAL + CORRECTED automatic funnels and manual/final exports."""
    paths = SelectionPaths.from_root(root)
    scopus, wos = load_platform_uniques(paths)
    historical = build_historical_funnel(scopus, wos, paths)
    corrected = build_corrected_funnel(scopus, wos, paths)

    if validate:
        validate_funnel_counts(historical, EXPECTED_HISTORICAL)
        validate_funnel_counts(corrected, EXPECTED_CORRECTED)
        # Guard against silent mixing of views.
        if historical.view == corrected.view:
            raise AssertionError("Historical and corrected views must differ")
        h_titles = set(
            historical.candidates[TITLE_COLUMN].dropna().astype(str).map(normalize_title)
        )
        if normalize_title(ANCIENT_CHINESE_TITLE) in h_titles:
            raise AssertionError(
                "Ancient Chinese must not appear in historical candidates"
            )

    hist_paths: dict[str, Path] = {}
    corr_paths: dict[str, Path] = {}
    study_path = final_sel_path = corpus_path = None

    if write:
        hist_paths = write_funnel_outputs(historical, paths.historical_dir)
        corr_paths = write_funnel_outputs(corrected, paths.corrected_dir)
        study_path = paths.manual_dir / "study_selection.csv"
        final_sel_path = paths.manual_dir / "final_selection.csv"
        corpus_path = paths.final_dir / "final_corpus.csv"
        export_study_selection_csv(paths.summary_xlsx, study_path)
        export_final_selection_csv(paths.summary_xlsx, final_sel_path)
        export_final_corpus_csv(paths.summary_xlsx, corpus_path)

    return SelectionReproductionResult(
        historical=historical,
        corrected=corrected,
        historical_paths=hist_paths,
        corrected_paths=corr_paths,
        study_selection_path=study_path,
        final_selection_path=final_sel_path,
        final_corpus_path=corpus_path,
    )


def format_funnel_arrow(counts: dict[str, int]) -> str:
    return (
        f"{counts['merged']} → {counts['unique']} → {counts['english']} → "
        f"{counts['proceedings_filtered']} → {counts['candidates']}"
    )


def doi_diagnostic_collisions(unique_frame: pd.DataFrame) -> pd.DataFrame:
    """Diagnostic only: DOI collisions remaining after exact-title dedup."""
    frame = unique_frame.copy()
    frame["_doi"] = frame[DOI_COLUMN].map(normalize_doi)
    return (
        frame.dropna(subset=["_doi"])
        .groupby("_doi")
        .filter(lambda g: len(g) > 1)
        .reset_index(drop=True)
    )
