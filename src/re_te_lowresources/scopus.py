"""Reproduce the Scopus aggregation stage from frozen platform exports.

Public boundary
---------------
Live Scopus / pybliometrics search is **not** reproduced. Inputs are the frozen
per-query CSV exports under ``sources/scopus/q*/{A,B}/scopus.csv``.

Historical notebook semantics (``legacy/notebooks/scopus.ipynb``)
-----------------------------------------------------------------
* Core RE/TE queries (methodology funnel 204 → 164) are loaded while excluding
  Information-Extraction / Generation query families
  ``q31–q34, q46–q49, q61–q64``.
* Platform-level deduplication uses ``Title`` with ``keep="first"``.
* Concatenation order is frozen to the historical discovery order that produced
  ``legacy/checkpoints/scopus_reducido.csv`` (see ``CORE_QUERY_ORDER``).

Public outputs vs legacy filenames
----------------------------------
* ``data/automatic/scopus/scopus_core.csv`` — concatenated frozen exports for the
  core Paper-1 search (204 rows). Not the exploratory all-query aggregate
  historically saved as ``scopus.csv`` (446).
* ``data/automatic/scopus/scopus_unique.csv`` — platform-level title deduplication
  (164 rows), matching the scientific content of
  ``legacy/checkpoints/scopus_reducido.csv`` (CSV float formatting may differ).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import pandas as pd

# Historical load order recovered from legacy checkpoint query first-seen order.
# Within each query, strategy folders are read A then B when both exist.
CORE_QUERY_ORDER: tuple[str, ...] = ("q1", "q17", "q2", "q16", "q4", "q3")
STRATEGY_ORDER: tuple[str, ...] = ("A", "B")

# Families present under sources/scopus but excluded from the Paper-1 core funnel.
EXCLUDED_QUERY_FAMILIES: frozenset[str] = frozenset(
    {
        "q31",
        "q32",
        "q33",
        "q34",
        "q46",
        "q47",
        "q48",
        "q49",
        "q61",
        "q62",
        "q63",
        "q64",
    }
)

EXPECTED_CORE_ROWS = 204
EXPECTED_UNIQUE_ROWS = 164
# Backwards-compatible aliases used by CLI/tests messaging.
EXPECTED_RAW_ROWS = EXPECTED_CORE_ROWS
EXPECTED_DEDUP_ROWS = EXPECTED_UNIQUE_ROWS

TITLE_COLUMN = "Title"
QUERY_COLUMN = "query"
OUTPUT_CORE_NAME = "scopus_core.csv"
OUTPUT_UNIQUE_NAME = "scopus_unique.csv"


@dataclass(frozen=True)
class ScopusPaths:
    """Repository-relative paths for the Scopus stage."""

    root: Path
    sources: Path
    output_dir: Path

    @classmethod
    def from_root(cls, root: Path | None = None) -> "ScopusPaths":
        root = (root or default_repo_root()).resolve()
        return cls(
            root=root,
            sources=root / "sources" / "scopus",
            output_dir=root / "data" / "automatic" / "scopus",
        )


def default_repo_root() -> Path:
    """Return repository root (parent of ``src/``)."""
    return Path(__file__).resolve().parents[2]


def discover_scopus_exports(
    sources: Path,
    query_order: Sequence[str] = CORE_QUERY_ORDER,
    strategy_order: Sequence[str] = STRATEGY_ORDER,
) -> list[Path]:
    """Return frozen export paths in deterministic historical order.

    Raises
    ------
    FileNotFoundError
        If the sources directory is missing or a required core export is absent.
    """
    sources = sources.resolve()
    if not sources.is_dir():
        raise FileNotFoundError(f"Scopus sources directory not found: {sources}")

    paths: list[Path] = []
    missing: list[str] = []
    for query in query_order:
        qdir = sources / query
        if not qdir.is_dir():
            missing.append(f"{query}/ (directory)")
            continue
        found_for_query = False
        for strategy in strategy_order:
            candidate = qdir / strategy / "scopus.csv"
            if candidate.is_file():
                paths.append(candidate)
                found_for_query = True
        if not found_for_query:
            missing.append(f"{query}/{{A,B}}/scopus.csv")

    if missing:
        raise FileNotFoundError(
            "Missing required Scopus core exports:\n  - " + "\n  - ".join(missing)
        )
    if not paths:
        raise FileNotFoundError(f"No Scopus CSV exports discovered under {sources}")
    return paths


def load_scopus_exports(export_paths: Iterable[Path]) -> pd.DataFrame:
    """Load and concatenate frozen exports, adding a ``query`` column per file."""
    frames: list[pd.DataFrame] = []
    for path in export_paths:
        path = Path(path)
        query = path.parent.parent.name
        if query in EXCLUDED_QUERY_FAMILIES:
            # Defensive: discovery should already omit these.
            continue
        frame = pd.read_csv(path)
        frame[QUERY_COLUMN] = query
        frames.append(frame)

    if not frames:
        raise ValueError("No Scopus export frames loaded")
    return pd.concat(frames, ignore_index=True)


def build_scopus_core(
    sources: Path,
    query_order: Sequence[str] = CORE_QUERY_ORDER,
    strategy_order: Sequence[str] = STRATEGY_ORDER,
) -> pd.DataFrame:
    """Concatenate core-query frozen exports (expected 204 rows)."""
    paths = discover_scopus_exports(sources, query_order, strategy_order)
    return load_scopus_exports(paths)


# Alias kept for readability in call sites that say "full concat".
build_scopus_full = build_scopus_core


def build_scopus_unique(scopus_core: pd.DataFrame) -> pd.DataFrame:
    """Platform-level deduplication on ``Title`` with keep-first (expected 164)."""
    if TITLE_COLUMN not in scopus_core.columns:
        raise KeyError(
            f"Expected title column {TITLE_COLUMN!r} in Scopus frame; "
            f"columns={list(scopus_core.columns)}"
        )
    return scopus_core.drop_duplicates(subset=TITLE_COLUMN, keep="first").reset_index(
        drop=True
    )


def write_scopus_outputs(
    scopus_core: pd.DataFrame,
    scopus_unique: pd.DataFrame,
    output_dir: Path,
) -> tuple[Path, Path]:
    """Write deterministic CSV checkpoints (no pandas index column)."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    core_path = output_dir / OUTPUT_CORE_NAME
    unique_path = output_dir / OUTPUT_UNIQUE_NAME
    scopus_core.to_csv(core_path, index=False)
    scopus_unique.to_csv(unique_path, index=False)
    return core_path, unique_path


@dataclass(frozen=True)
class ScopusReproductionResult:
    core: pd.DataFrame
    unique: pd.DataFrame
    core_path: Path
    unique_path: Path

    @property
    def full(self) -> pd.DataFrame:
        """Alias for ``core``."""
        return self.core

    @property
    def raw_rows(self) -> int:
        return len(self.core)

    @property
    def dedup_rows(self) -> int:
        return len(self.unique)

    @property
    def full_path(self) -> Path:
        """Alias for ``core_path``."""
        return self.core_path


def validate_scopus_invariants(core: pd.DataFrame, unique: pd.DataFrame) -> None:
    """Raise ``AssertionError`` if core funnel counts are not met."""
    errors: list[str] = []
    if len(core) != EXPECTED_CORE_ROWS:
        errors.append(f"core rows: expected {EXPECTED_CORE_ROWS}, got {len(core)}")
    if len(unique) != EXPECTED_UNIQUE_ROWS:
        errors.append(
            f"unique rows: expected {EXPECTED_UNIQUE_ROWS}, got {len(unique)}"
        )
    if TITLE_COLUMN not in core.columns or TITLE_COLUMN not in unique.columns:
        errors.append(f"missing {TITLE_COLUMN!r} column")
    else:
        # Historical TERL double record must still be present at this stage.
        terl_mask = (
            core[TITLE_COLUMN]
            .astype(str)
            .str.contains(
                r"TERL:\s*Transformer Enhanced Reinforcement Learning",
                case=False,
                regex=True,
                na=False,
            )
        )
        terl_count = int(terl_mask.sum())
        if terl_count < 2:
            errors.append(
                f"expected ≥2 TERL bibliographic rows in core concat, found {terl_count}"
            )
    if errors:
        raise AssertionError("Scopus invariants failed:\n  - " + "\n  - ".join(errors))


def reproduce_scopus(
    root: Path | None = None,
    *,
    validate: bool = True,
    write: bool = True,
) -> ScopusReproductionResult:
    """Run the full Scopus reproduction stage from frozen exports."""
    paths = ScopusPaths.from_root(root)
    core = build_scopus_core(paths.sources)
    unique = build_scopus_unique(core)
    if validate:
        validate_scopus_invariants(core, unique)
    if write:
        core_path, unique_path = write_scopus_outputs(core, unique, paths.output_dir)
    else:
        core_path = paths.output_dir / OUTPUT_CORE_NAME
        unique_path = paths.output_dir / OUTPUT_UNIQUE_NAME
    return ScopusReproductionResult(
        core=core,
        unique=unique,
        core_path=core_path,
        unique_path=unique_path,
    )
