# Provenance

Scientific history of the Paper-1 literature funnel as reconstructed from repository artifacts.

## A. Original search provenance

Primary bibliographic sources were **Scopus** and **Web of Science**, using query families documented in `data/methodology/research_methodology.xlsx` (core RE/TE queries `q1`, `q2`, `q3`, `q4`, `q16`, `q17`; strategies A/B where present).

Frozen per-query exports are committed under:

- `sources/scopus/q*/{A,B}/scopus.csv`
- `sources/web_of_science/q*/{A,B}/savedrecs.xls`

**Live-database limitation.** Re-running the same queries today is not expected to reproduce the historical hit counts. Public reproducibility starts from the frozen exports.

## B. Platform aggregation

| Platform | Core concat | Platform title deduplication |
|----------|------------:|-----------------------------:|
| Scopus | 204 | 164 (`Title`, keep-first) |
| Web of Science | 79 | 62 (`Article Title`, keep-first) |

Information-extraction / generation query families present under `sources/` (`q31–q34`, `q46–q49`, `q61–q64`) are excluded from the Paper-1 core funnel, matching the Scopus/WoS stage implementations.

## C. Historical Selection reconstruction

After concatenating platform-unique rows (164 + 62 = **226**), the published automatic path corresponds to:

**226 → 165 → 159 → 135 → 134**

This path is reproduced explicitly as **historical reproduction** (`data/automatic/selection/historical/`).

### Historical Web of Science alignment defect

The original Selection notebook prepared an intended WoS→Scopus column rename map, but the concatenated frame used a WoS dataframe that was **reindexed onto Scopus column names without applying that rename**. Fields that differ by name (notably title, language, publication year, and author identifiers) were therefore null for Web of Science rows.

Consequence (observed in reconstruction and historical summary artifacts):

- cross-platform “unique” count **165** ≈ 164 Scopus titles + one WoS row with a null title;
- English filtering then retains Scopus English rows only (**159**);
- subsequent automatic stages of the published study are effectively Scopus-dominated.

This defect is documented for transparency. It is **not** recommended data processing. The corrected pipeline is a separate view and was **not** the path that produced the published manual candidate list.

## D. Corrected Selection

With the intended schema alignment applied:

**226 → 173 → 168 → 140 → 135**

(`data/automatic/selection/corrected/`)

This is a **technically corrected reconstruction** of the automatic stages. It does **not** retroactively change historical manual screening.

The corrected normalized candidate set includes:

*Few-Shot Relation Extraction on Ancient Chinese Documents*

That record was never present in the historical manual Study selection sheet. This package does **not** assign it a retrospective Yes/No/Doubt decision.

## E. English → author-metadata filter (159 → 135 historically)

The methodology workbook describes this step as removal of proceedings. The executable condition recovered from the Selection notebook is:

```text
dropna(subset=["authors", "author full names", "author(s) id"])
```

Historically, **24** English rows fail that condition. They are Scopus `Conference review` shell records with empty author fields (proceedings-like bibliographic shells), not peer full-text articles with populated authorship metadata.

## F. Candidate normalization (135 → 134)

Two Scopus bibliographic rows represent the same TERL work under equivalent **normalized** titles, with EIDs:

- `2-s2.0-85218049221`
- `2-s2.0-85174436404`

Candidate normalization keeps the first and yields **134** historical candidates.

`research_methodology.xlsx` labels this −1 step as **Free**. No artifact-level free/full-text exclusion supporting that label was found; the executable evidence is the TERL dual bibliographic representation.

## G. Manual review

Preserved Study selection decisions (134 titled candidates):

| State | Count |
|-------|------:|
| Yes | 47 |
| No | 69 |
| Doubt | 18 |

Of the **47** first-pass Yes records, **42** appear in the recoverable final analytical corpus (`data/final/final_corpus.csv`). Five Yes Paper IDs remain outside that corpus in preserved Data extraction / Summary evidence (`zhao`, `jian`, `liu5_349`, `souza_508`, `wang_109`), typically lacking a populated solution name in Data extraction. This package does not invent additional exclusion narratives beyond those preserved fields.

## H. Published 43 vs preserved 42

Factually, from repository evidence:

- the published article reports **43** final studies;
- preserved structured final analytical artifacts consistently enumerate **42** unique Paper IDs;
- no recoverable 43-entry final study list was located in the repository;
- a duplicate-ID / duplicate-metadata hypothesis for 43→42 was investigated and **not** supported by Yes / Data extraction / Summary evidence.

Therefore public reproducibility uses **42** as the **canonical recoverable analytical corpus**. This documentation records the discrepancy; it does not designate a formal publisher erratum.

## Related outputs

| Artifact | Role |
|----------|------|
| `data/automatic/selection/historical/*` | Historical automatic funnel |
| `data/automatic/selection/corrected/*` | Corrected automatic funnel |
| `data/manual/study_selection.csv` | 134 preserved decisions |
| `data/manual/final_selection.csv` | 47 Yes + final-corpus flag |
| `data/final/final_corpus.csv` | 42-study recoverable corpus |
