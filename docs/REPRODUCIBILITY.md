# Reproducibility

This document describes how to reproduce the Paper-1 bibliographic pipeline from frozen exports.

## Clean-clone workflow

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
python scripts/reproduce_all.py
python scripts/validate_reproduction.py
```

| Item | Value |
|------|--------|
| Supported Python | ≥ 3.10 |
| Validated environment | Python 3.14.7 |
| API credentials | not required |
| Live Scopus / WoS access | not required |
| Network after install | not required for reproduction |

Dependencies are pinned in `requirements.txt`. The package under `src/re_te_lowresources/` is installed editable via `pyproject.toml`.

## Expected outputs

### Scopus

`sources/scopus/` → `data/automatic/scopus/`

- core: **204**
- unique (`Title`, keep-first): **164**

### Web of Science

`sources/web_of_science/` → `data/automatic/web_of_science/`

- core: **79**
- unique (`Article Title`, keep-first): **62**

### Selection — historical reproduction

Concatenated unique platforms → automatic funnel:

**226 → 165 → 159 → 135 → 134**

Written under `data/automatic/selection/historical/` (`pipeline_view=historical`).

### Selection — corrected pipeline

Same inputs with intended schema alignment:

**226 → 173 → 168 → 140 → 135**

Written under `data/automatic/selection/corrected/` (`pipeline_view=corrected`).

### Manual screening (preserved)

From `data/final/summary_reduced.xlsx` → `data/manual/`:

- candidates: **134**
- Yes **47** / No **69** / Doubt **18**

### Final recoverable corpus

`data/final/final_corpus.csv`: **42** unique studies.

The published article reports **43** final studies; preserved structured artifacts contain **42**. A duplicate-ID explanation of that gap was investigated and is not supported by repository evidence. Validation prints a warning and does **not** fail for the discrepancy.

## Stage scripts

| Command | Effect |
|---------|--------|
| `python scripts/reproduce_all.py` | Scopus → WoS → Selection (both views) → manual/final exports |
| `python scripts/reproduce_scopus.py` | Scopus only |
| `python scripts/reproduce_wos.py` | Web of Science only |
| `python scripts/reproduce_selection.py` | Selection + manual/final |
| `python scripts/validate_reproduction.py` | Count and qualitative checks |

All scripts call shared functions in `src/re_te_lowresources/`; they do not duplicate scientific logic.

## Notebooks

With the editable package installed:

| Notebook | Content |
|----------|---------|
| `notebooks/reproducibility/01_scopus.ipynb` | Frozen Scopus aggregation |
| `notebooks/reproducibility/02_web_of_science.ipynb` | Frozen WoS aggregation |
| `notebooks/reproducibility/03_selection.ipynb` | Historical vs corrected Selection, TERL, manual/final |

Execute non-interactively, for example:

```bash
jupyter nbconvert --to notebook --execute notebooks/reproducibility/01_scopus.ipynb
```

Select the project virtualenv kernel when running interactively.

## Tests

```bash
python -m unittest discover -s tests
```

## Frozen-export boundary

Live database results change over time. This package reproduces processing of the **committed** exports under `sources/scopus/` and `sources/web_of_science/`. It does not query Scopus or Web of Science.

Historical exploratory notebooks and checkpoints may exist locally under ignored `legacy/`; the public runtime does not depend on them.

## Related documents

- [PROVENANCE.md](PROVENANCE.md) — scientific history of each funnel step
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md) — artifact meanings and key columns
