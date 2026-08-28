"""Reproduce the Web of Science aggregation stage from frozen platform exports.

Public boundary
---------------
Live Web of Science search is **not** reproduced. Inputs are the frozen
per-query Excel exports under ``sources/web_of_science/q*/{A,B}/savedrecs.xls``.

Historical notebook semantics (``legacy/notebooks/wos.ipynb``)
-------------------------------------------------------------
* Core RE/TE queries (methodology funnel 79 → 62) are loaded while excluding
  Information-Extraction / Generation query families
  ``q31–q34, q46–q49, q61–q64``.
* Platform-level deduplication uses ``Article Title`` with ``keep="first"``.
* Concatenation order is frozen to the historical discovery order that produced
  ``legacy/checkpoints/wos_reducido.csv`` (see ``CORE_QUERY_ORDER``).
* Exports are read with pandas ``read_excel(..., engine="xlrd")``.

Public outputs vs legacy filenames
----------------------------------
* ``data/automatic/web_of_science/wos_core.csv`` — concatenated frozen exports for
  the core Paper-1 search (79 rows). Not the exploratory all-query aggregate
  historically saved as ``wos.csv`` (97 unique-title rows after all-query dedup).
* ``data/automatic/web_of_science/wos_unique.csv`` — platform-level title
  deduplication (62 rows), matching the scientific content of
  ``legacy/checkpoints/wos_reducido.csv`` (CSV float formatting may differ).
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

# Families present under sources/web_of_science but excluded from the Paper-1 core.
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

EXPECTED_CORE_ROWS = 79
EXPECTED_UNIQUE_ROWS = 62
# Backwards-compatible aliases used by CLI/tests messaging.
EXPECTED_RAW_ROWS = EXPECTED_CORE_ROWS
EXPECTED_DEDUP_ROWS = EXPECTED_UNIQUE_ROWS

TITLE_COLUMN = "Article Title"
QUERY_COLUMN = "query"
EXPORT_FILENAME = "savedrecs.xls"
OUTPUT_CORE_NAME = "wos_core.csv"
OUTPUT_UNIQUE_NAME = "wos_unique.csv"


@dataclass(frozen=True)
class WoSPaths:
    """Repository-relative paths for the Web of Science stage."""

    root: Path
    sources: Path
    output_dir: Path

    @classmethod
    def from_root(cls, root: Path | None = None) -> "WoSPaths":
        root = (root or default_repo_root()).resolve()
        return cls(
            root=root,
            sources=root / "sources" / "web_of_science",
            output_dir=root / "data" / "automatic" / "web_of_science",
        )


def default_repo_root() -> Path:
    """Return repository root (parent of ``src/``)."""
    return Path(__file__).resolve().parents[2]


def discover_wos_exports(
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
        raise FileNotFoundError(f"Web of Science sources directory not found: {sources}")

    paths: list[Path] = []
    missing: list[str] = []
    for query in query_order:
        qdir = sources / query
        if not qdir.is_dir():
            missing.append(f"{query}/ (directory)")
            continue
        found_for_query = False
        for strategy in strategy_order:
            candidate = qdir / strategy / EXPORT_FILENAME
            if candidate.is_file():
                paths.append(candidate)
                found_for_query = True
        if not found_for_query:
            missing.append(f"{query}/{{A,B}}/{EXPORT_FILENAME}")

    if missing:
        raise FileNotFoundError(
            "Missing required Web of Science core exports:\n  - "
            + "\n  - ".join(missing)
        )
    if not paths:
        raise FileNotFoundError(
            f"No Web of Science .xls exports discovered under {sources}"
        )
    return paths


def load_wos_exports(export_paths: Iterable[Path]) -> pd.DataFrame:
    """Load and concatenate frozen exports, adding a ``query`` column per file."""
    frames: list[pd.DataFrame] = []
    for path in export_paths:
        path = Path(path)
        query = path.parent.parent.name
        if query in EXCLUDED_QUERY_FAMILIES:
            # Defensive: discovery should already omit these.
            continue
        frame = pd.read_excel(path, engine="xlrd")
        frame[QUERY_COLUMN] = query
        frames.append(frame)

    if not frames:
        raise ValueError("No Web of Science export frames loaded")
    return pd.concat(frames, ignore_index=True)


def build_wos_core(
    sources: Path,
    query_order: Sequence[str] = CORE_QUERY_ORDER,
    strategy_order: Sequence[str] = STRATEGY_ORDER,
) -> pd.DataFrame:
    """Concatenate core-query frozen exports (expected 79 rows)."""
    paths = discover_wos_exports(sources, query_order, strategy_order)
    return load_wos_exports(paths)


# Alias kept for readability in call sites that say "full concat".
build_wos_full = build_wos_core


def build_wos_unique(wos_core: pd.DataFrame) -> pd.DataFrame:
    """Platform-level deduplication on ``Article Title`` with keep-first (expected 62)."""
    if TITLE_COLUMN not in wos_core.columns:
        raise KeyError(
            f"Expected title column {TITLE_COLUMN!r} in WoS frame; "
            f"columns={list(wos_core.columns)}"
        )
    return wos_core.drop_duplicates(subset=TITLE_COLUMN, keep="first").reset_index(
        drop=True
    )


def write_wos_outputs(
    wos_core: pd.DataFrame,
    wos_unique: pd.DataFrame,
    output_dir: Path,
) -> tuple[Path, Path]:
    """Write deterministic CSV checkpoints (no pandas index column)."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    core_path = output_dir / OUTPUT_CORE_NAME
    unique_path = output_dir / OUTPUT_UNIQUE_NAME
    wos_core.to_csv(core_path, index=False)
    wos_unique.to_csv(unique_path, index=False)
    return core_path, unique_path


@dataclass(frozen=True)
class WoSReproductionResult:
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


def validate_wos_invariants(core: pd.DataFrame, unique: pd.DataFrame) -> None:
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
    if errors:
        raise AssertionError("WoS invariants failed:\n  - " + "\n  - ".join(errors))


def reproduce_wos(
    root: Path | None = None,
    *,
    validate: bool = True,
    write: bool = True,
) -> WoSReproductionResult:
    """Run the full Web of Science reproduction stage from frozen exports."""
    paths = WoSPaths.from_root(root)
    core = build_wos_core(paths.sources)
    unique = build_wos_unique(core)
    if validate:
        validate_wos_invariants(core, unique)
    if write:
        core_path, unique_path = write_wos_outputs(core, unique, paths.output_dir)
    else:
        core_path = paths.output_dir / OUTPUT_CORE_NAME
        unique_path = paths.output_dir / OUTPUT_UNIQUE_NAME
    return WoSReproductionResult(
        core=core,
        unique=unique,
        core_path=core_path,
        unique_path=unique_path,
    )
