# From Relation Extraction to Triplet Extraction: A Survey on Low-Resource Scenarios

This repository accompanies the survey:

**From Relation Extraction to Triplet Extraction: A Survey on Low-Resource Scenarios**

It provides a **public reproducibility package** for the Paper-1 bibliographic search, automatic filtering, preserved manual screening evidence, and the recoverable analytical corpus.

## Purpose

Reproduce the survey’s literature-selection pipeline from **frozen** Scopus and Web of Science exports, without live database access.

## Reproducibility scope

| In scope | Out of scope |
|----------|--------------|
| Platform aggregation (Scopus, WoS) | Live Scopus / Web of Science search |
| Dual-view Selection (historical + corrected) | Re-running original API queries |
| Export of preserved manual decisions | Assigning new inclusion decisions |
| Recoverable 42-study final corpus | Guaranteeing identity with today’s live hit lists |

**Frozen-export boundary.** Current live searches are **not** expected to reproduce the historical hit counts. The reproducibility boundary is the committed exports under `sources/`.

See [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md) and [docs/PROVENANCE.md](docs/PROVENANCE.md).

## Repository structure

```
sources/scopus/                  frozen Scopus exports (q*/{A,B}/scopus.csv)
sources/web_of_science/          frozen WoS exports (q*/{A,B}/savedrecs.xls)
sources/others/                  auxiliary PDFs / background material
data/methodology/                research_methodology.xlsx
data/automatic/scopus/           generated Scopus core / unique CSVs
data/automatic/web_of_science/   generated WoS core / unique CSVs
data/automatic/selection/        historical/ and corrected/ Selection stages
data/manual/                     exported Study selection / Yes audit
data/final/                      summary workbook + final_corpus.csv
src/re_te_lowresources/          shared Python implementation
scripts/                         CLI entry points
notebooks/reproducibility/       interactive stage notebooks
docs/                            reproducibility, provenance, data dictionary
tests/                           lightweight validation tests
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
python scripts/reproduce_all.py
python scripts/validate_reproduction.py
```

- Supported Python: **≥ 3.10**
- Validated environment: **Python 3.14.7**

No API credentials or internet access are required after dependencies are installed.

## Expected checkpoints

| Stage | Checkpoint |
|-------|------------|
| Scopus | 204 core → 164 unique |
| Web of Science | 79 core → 62 unique |
| Historical Selection | 226 → 165 → 159 → 135 → 134 |
| Corrected Selection | 226 → 173 → 168 → 140 → 135 |
| Manual | Yes 47 / No 69 / Doubt 18 (134 candidates) |
| Final recoverable corpus | **42** unique studies |

## Scripts

| Script | Role |
|--------|------|
| `scripts/reproduce_all.py` | Run all stages |
| `scripts/validate_reproduction.py` | Validate counts and qualitative invariants |
| `scripts/reproduce_scopus.py` | Scopus only |
| `scripts/reproduce_wos.py` | Web of Science only |
| `scripts/reproduce_selection.py` | Selection (historical + corrected) + manual/final exports |

## Interactive notebooks

| Notebook | Stage |
|----------|-------|
| `notebooks/reproducibility/01_scopus.ipynb` | Scopus aggregation |
| `notebooks/reproducibility/02_web_of_science.ipynb` | WoS aggregation |
| `notebooks/reproducibility/03_selection.ipynb` | Dual-view Selection + manual/final |

## Historical vs corrected Selection

- **Historical reproduction** reconstructs the Paper-1 processing path, including a Web of Science schema-alignment defect that shaped the published automatic funnel (226 → 165 → 159 → 135 → 134).
- **Corrected pipeline** applies the intended Scopus↔WoS field mapping and reports how automatic candidates differ (226 → 173 → 168 → 140 → 135). It does **not** rewrite historical manual screening.

Details: [docs/PROVENANCE.md](docs/PROVENANCE.md).

## Manual review and final corpus

Preserved decisions (`data/manual/study_selection.csv`): **47 Yes / 69 No / 18 Doubt**.

First-pass Yes records are audited in `data/manual/final_selection.csv` (47 rows; 42 marked in the final corpus).

The recoverable analytical corpus is `data/final/final_corpus.csv` (**42** unique `paper_id`s), in agreement with the Summary table and Data extraction rows that have a populated solution name.

### Published 43 vs preserved 42

The published article reports **43** final studies. Preserved structured analytical artifacts in this repository consistently contain **42** unique Paper IDs. No recoverable 43-entry final list was found here. A hypothesized duplicate-ID explanation of 43→42 was investigated and **not** supported by Yes / Data extraction / Summary evidence. Public reproducibility therefore treats **42** as the canonical recoverable analytical corpus. See [docs/PROVENANCE.md](docs/PROVENANCE.md).

## Abstract (survey)

Recent advances in generative frameworks have shifted Relation Extraction (RE) toward Triplet Extraction (TE), framing Information Extraction (IE) as an open-schema generation of *(subject, predicate, object)* triplets. This work provides a structured overview of current solutions, research gaps, and future directions for RE and TE in low-resource scenarios. This survey focuses exclusively on low-resource scenarios, defined by limited availability of annotated data and/or the absence of supporting resources such as external vocabularies or ontologies, which are typically leveraged to identify and extract entities and relations. The goal is stated by four key objectives: (1) illustrate the conceptual foundations of RE and TE, including their similarities and differences; (2) formally defining low-resource scenarios and characterizing their key challenges; (3) analyzing State-of-The-Art (SoTA) methods within their efficacy in low-resource settings for solving RE and TE; and finally, (4) future directions of RE/ TE in such settings.

## Keywords

- Information Extraction
- Relation Extraction
- Triplet Extraction
- Low-resources

## Citation

Please cite the associated survey:

Pardo-Ferrera, J., Montiel-Ponsoda, E., & Calleja, P. (2026). From relation extraction to triplet extraction: A survey on low-resource scenarios. *Computer Science Review*, *61*, Article 100954. https://doi.org/10.1016/j.cosrev.2026.100954

Machine-readable citation metadata: [CITATION.cff](CITATION.cff).

## License and third-party material

Original repository code and documentation are released under the [MIT License](LICENSE) (Copyright © 2025 Joel Pardo-Ferrera), unless stated otherwise.

Frozen database exports, PDFs, and other third-party materials remain subject to their own copyright, database, and access terms and are **not** relicensed under MIT. See [NOTICE](NOTICE).

## Further documentation

- [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md) — clean-clone workflow and scripts
- [docs/PROVENANCE.md](docs/PROVENANCE.md) — scientific history of the funnel
- [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) — public data artifacts and key columns

## Works explored for the analysis

| **Paper ID** | **Title** | **Authors** | **Year** | **Venue** |
|:--------------|:-----------|:-------------|:----------:|:-----------|
| bai | *Clear Up Confusion: Advancing Cross-Domain Few-Shot Relation Extraction through Relation-Aware Prompt Learning* | Bai G.; Lu C.; Guo D.; Li S.; Liu Y.; Zhang Z.; Dong G.; Liu R.; Sun Y. | 2024 | NAACL 2024 – Conference of the North American Chapter of the Association for Computational Linguistics |
| chen2 | *KnowPrompt: Knowledge-aware Prompt-tuning with Synergistic Optimization for Relation Extraction* | Chen X.; Zhang N.; Xie X.; Deng S.; Yao Y.; Tan C.; Huang F.; Si L.; Chen H. | 2022 | WWW 2022 – ACM Web Conference |
| chen | *DiffFSRE: Diffusion-Enhanced Prototypical Network for Few-Shot Relation Extraction* | Chen Y.; Shi B. | 2024 | *Entropy* |
| chen3 | *PTCAS: Prompt tuning with continuous answer search for relation extraction* | Chen Y.; Shi B.; Xu K. | 2024 | *Information Sciences* |
| chia | *RelationPrompt: Leveraging Prompts to Generate Synthetic Data for Zero-Shot Relation Triplet Extraction* | Chia Y.K.; Bing L.; Poria S.; Si L. | 2022 | ACL Annual Meeting |
| gao | *Fine-Grained Relation Extraction for Drug Instructions Using Contrastive Entity Enhancement* | Gao F.; Song X.; Gu J.; Zhang L.; Liu Y.; Zhang X.; Liu Y.; Jing S. | 2023 | *IEEE Access* |
| guo | *KBPT: knowledge-based prompt tuning for zero-shot relation triplet extraction* | Guo Q.; Guo Y.; Zhao J. | 2024 | *PeerJ Computer Science* |
| halike | *Zero-Shot Relation Triple Extraction with Prompts for Low-Resource Languages* | Halike A.; Wumaier A.; Yibulayin T. | 2023 | *Applied Sciences (Switzerland)* |
| han | *A Zero-Shot Framework for Low-Resource Relation Extraction via Distant Supervision and Large Language Models* | Han P.; Liang G.; Wang Y. | 2025 | *Electronics (Switzerland)* |
| haoran | *Improved Chinese Few-Shot Relation Extraction using Large Language Model for Data Augmentation and Prototypical Network* | Haoran X.; Lou K.; Chan S. | 2024 | IEEE International Conference on Systems, Man and Cybernetics |
| hsu | *Prompt-Learning for Cross-Lingual Relation Extraction* | Hsu C.; Zan C.; Ding L.; Wang L.; Wang X.; Liu W.; Lin F.; Hu W. | 2023 | IJCNN 2023 |
| hu2 | *SelfLRE: Self-refining Representation Learning for Low-resource Relation Extraction* | Hu X.; Chen J.; Meng S.; Wen L.; Yu P.S. | 2023 | SIGIR 2023 |
| hu | *GDA: Generative Data Augmentation Techniques for Relation Extraction Tasks* | Hu X.; Liu A.; Tan Z.; Zhang X.; Zhang C.; King I.; Yu P.S. | 2023 | ACL Annual Meeting |
| hu3 | *Gradient Imitation Reinforcement Learning for Low Resource Relation Extraction* | Hu X.; Zhang C.; Yang Y.; Li X.; Lin L.; Wen L.; Yu P.S. | 2021 | EMNLP 2021 |
| li2 | *CoPrompt: A Contrast-prompt Tuning Method for Multiparty Dialogue Character Relationship Extraction* | Li Y.; Jiang Y.; Chen J.; Wang L.; Tao Y.; Zhang Y. | 2023 | ACM Proceedings |
| liu2 | *RexUIE: A Recursive Method with Explicit Schema Instructor for Universal Information Extraction* | Liu C.; Zhao F.; Kang Y.; Zhang J.; Zhou X.; Sun C.; Kuang K.; Wu F. | 2023 | *Findings of EMNLP 2023* |
| liu | *Aspect sentiment triplet extraction based on data augmentation and task feedback* | Liu S.; Lu T.; Li K.; Liu W. | 2024 | *Journal of Intelligent Information Systems* |
| liu_2 | *Domain-aware and Co-adaptive Feature Transformation for Domain Adaptation Few-shot Relation Extraction* | Liu Y.; Dai F.; Gu X.; Zhai M.; Li B.; Zhang M. | 2024 | LREC-COLING 2024 |
| lu | *Summarization as Indirect Supervision for Relation Extraction* | Lu K.; Hsu I.-H.; Zhou W.; Ma M.D.; Chen M. | 2022 | *Findings of EMNLP 2022* |
| lu2 | *Reasoning Makes Good Annotators: An Automatic Task-specific Rules Distilling Framework for Low-resource Relation Extraction* | Lu Y.; Shi H.; Li J.; Chen T.; Wang X.; Tang S. | 2023 | *Findings of EMNLP 2023* |
| ly | *DSP: Discriminative Soft Prompts for Zero-Shot Entity and Relation Extraction* | Lv B.; Liu X.; Dai S.; Liu N.; Yang F.; Luo P.; Yu Y. | 2023 | ACL Annual Meeting |
| ma | *Making Pre-trained Language Models Better Continual Few-Shot Relation Extractors* | Ma S.; Han J.; Liang Y.; Cheng B. | 2024 | LREC-COLING 2024 |
| miao | *Generating Commonsense Counterfactuals for Stable Relation Extraction* | Miao X.; Li Y.; Qian T. | 2023 | EMNLP 2023 |
| moscato | *Multi-task learning for few-shot biomedical relation extraction* | Moscato V.; Napolano G.; Postiglione M.; Sperlë G. | 2023 | *Artificial Intelligence Review* |
| plum | *Guided Distant Supervision for Multilingual Relation Extraction Data: Adapting to a New Language* | Plum A.; Ranasinghe T.; Purschke C. | 2024 | LREC-COLING 2024 |
| qin | *ERICA: Improving Entity and Relation Understanding for Pre-trained Language Models via Contrastive Learning* | Qin Y.; Lin Y.; Takanobu R.; Liu Z.; Li P.; Ji H.; Huang M.; Sun M.; Zhou J. | 2021 | ACL-IJCNLP 2021 |
| rocktaschel | *Injecting logical background knowledge into embeddings for relation extraction* | Rocktäschel T.; Singh S.; Riedel S. | 2015 | NAACL HLT 2015 |
| shi | *AgentRE: An Agent-Based Framework for Navigating Complex Information Landscapes in Relation Extraction* | Shi Y.; Jiang G.; Qiu T.; Yang D. | 2024 | CIKM 2024 |
| wang4 | *fmLRE: A Low-Resource Relation Extraction Model Based on Feature Mapping Similarity Calculation* | Wang P.; Shao T.; Ji K.; Li G.; Ke W. | 2023 | AAAI 2023 |
| xu5 | *S2ynRE: Two-stage Self-training with Synthetic Data for Low-resource Relation Extraction* | Xu B.; Wang Q.; Lyu Y.; Dai D.; Zhang Y.; Mao Z. | 2023 | ACL Annual Meeting |
| xu2 | *Can NLI Provide Proper Indirect Supervision for Low-resource Biomedical Relation Extraction?* | Xu J.; Ma M.D.; Chen M. | 2023 | ACL Annual Meeting |
| xu | *Question Answering on Freebase via Relation Extraction and Textual Evidence* | Xu K.; Reddy S.; Feng Y.; Huang S.; Zhao D. | 2016 | ACL 2016 |
| xu_1 | *Towards Realistic Low-resource Relation Extraction: A Benchmark with Empirical Baseline Study* | Xu X.; Chen X.; Zhang N.; Xie X.; Chen X.; Chen H. | 2022 | *Findings of EMNLP 2022* |
| yu | *Reliable Data Generation and Selection for Low-Resource Relation Extraction* | Yu J.; Wang X.; Chen W. | 2024 | AAAI 2024 |
| yuan | *Biomedical Relation Extraction via Domain Knowledge and Prompt Learning* | Yuan J.; Du W.; Liu X.; Zhang Y. | 2024 | *CEUR Workshop Proceedings* |
| zhang | *Relation Adversarial Network for Low Resource Knowledge Graph Completion* | Zhang N.; Deng S.; Sun Z.; Chen J.; Zhang W.; Chen H. | 2020 | WWW 2020 |
| zhang3 | *Co-Training with Validation: A Generic Framework for Semi-Supervised Relation Extraction* | Zhang S.; Lu X.; Wu J. | 2022 | CIKM 2022 |
| zhang2 | *A Prompt Tuning Method Based on Relation Graphs for Few-Shot Relation Extraction* | Zhang Z.; Yang Y.; Chen B. | 2025 | *Neural Networks* |
| zhang4 | *Prompt Tuning for Few-shot Relation Extraction via Modeling Global and Local Graphs* | Zhang Z.; Yang Y.; Chen B. | 2024 | LREC-COLING 2024 |
| zhao2 | *An Exploration of Prompt-Based Zero-Shot Relation Extraction Method* | Zhao J.; Hu Y.; Xu N.; Gui T.; Zhang Q.; Chen Y.; Gao X. | 2022 | CCL 2022 |
| zheng | *Making LLMs as Fine-Grained Relation Extraction Data Augmentor* | Zheng Y.; Ke W.; Liu Q.; Yang Y.; Zhao R.; Feng D.; Zhang J.; Fang Z. | 2024 | IJCAI 2024 |
| zhou2 | *Continual Contrastive Finetuning Improves Low-Resource Relation Extraction* | Zhou W.; Zhang S.; Naumann T.; Chen M.; Poon H. | 2023 | ACL Annual Meeting |

The table above enumerates the **42** recoverable analytical studies matching `data/final/final_corpus.csv` (Paper IDs agree exactly). The published article reports **43**; see [Published 43 vs preserved 42](#published-43-vs-preserved-42).


## Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.


## Declaration of Generative AI and AI-assisted technologies in the writing process

During the preparation of this work the author(s) used ChatGPT (https://chatgpt.com/) and Deepseek (https://chat.deepseek.com/) in order to polish language for clarity, ensuring consistent citation style, structuring data in tables, and assisting in the formatting of scientific visuals. After using this tool/ service, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication.

## Funding

This work has received funding from the INESData project (Infrastructure to Investigate Data Spaces in Distributed Environments at UPM), a project funded under the UNICO I+D CLOUD call by the Ministry for Digital Transformation and the Civil Service, within the framework of the recovery plan PRTR financed by the European Union (NextGenerationEU).

In addition, this article is part of the TeresIA research project, funded by the European Union's Next GenerationEU/ PRTR funds through the Spanish Ministry of Economy and Digital Transformation (now the Ministry for Digital Transformation and Public Service).