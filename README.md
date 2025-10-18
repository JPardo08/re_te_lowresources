# Relation Extraction (RE) and Triplet Extraction (TE) in Low-resource scenarios. 

## Abstracts

### From Relation Extraction to Triplet Extraction: A Survey on Low-Resource Scenarios

Recent advances in generative frameworks have shifted Relation Extraction (RE) toward Triplet Extraction (TE), framing Information Extraction (IE) as an open-schema generation of *(subject, predicate, object)* triplets. This work provides a structured overview of current solutions, research gaps, and future directions for RE and TE in low-resource scenarios. This survey focuses exclusively on low-resource scenarios, defined by limited availability of annotated data and/or the absence of supporting resources such as external vocabularies or ontologies, which are typically leveraged to identify and extract entities and relations. The goal is stated by four key objectives: (1) illustrate the conceptual foundations of RE and TE, including their similarities and differences; (2) formally defining low-resource scenarios and characterizing their key challenges; (3) analyzing State-of-The-Art (SoTA) methods within their efficacy in low-resource settings for solving RE and TE; and finally, (4) future directions of RE/ TE in such settings.

### Bridging the Data Gap: A Comprehensive Review of Datasets for Low-Resource Relation and Triplet Extraction

Generative frameworks are redefining Information Extraction (IE), recasting it from Relation Extraction (RE) into open-schema Triplet Extraction (TE); the direct generation of *(subject, predicate, object)* triples. This progression, however, presents significant evaluation challenges in low-resource scenarios, where annotated data and supporting resources are scarce. This survey addresses this gap by providing a comprehensive assessment of existing benchmarks for evaluating RE and TE under these constrained conditions. A core contribution is the systematic summary of relevant datasets, ranging from standardized benchmarks to those designed for domain-specific and multilingual challenges. The survey details how these resources are applied and transformed for low-resource settings, including their use in adversarial learning and task-reformulation strategies. By mapping the landscape of available resources and methodologies, this work aims to guide future research toward more robust and reproducible progress in low-resource IE.

## Keywords

- Information Extraction 
- Relation Extraction 
- Triplet Extraction
- Low-resources


## Research strategy 

This semi-systematic literature review follows the methodology outlined by *Guidelines for performing systematic literature reviews in software engineering*[^1], focusing on three key research questions about Relation Extraction (RE) and Triplet Extraction (TE) in low-resource scenarios.

### Search Approach

- **Strategy A**: Search with two-term queries only in title
- **Strategy B**: Search terms in title, abstract, and text

### Process Flow

1. **Initial Search**: Conducted on Scopus and Web of Science using 8 predefined queries combining task terms (Relation Extraction, Triplet Extraction) with scenario terms (low-resource, data scarcity, limited data, and sparse data)
2. **Duplicate Removal**: Merged results from both platforms and eliminated duplicates
3. **Filtering**: Applied inclusion/ exclusion criteria through automatic and manual screening
4. **Validation**: Resolved discrepancies through discussion with supervisors and collaborators

### Data Sources

- **Primary**: Scopus and Web of Science for core works
- **Secondary**: Google Scholar, Semantic Scholar, and ACL Anthology for comprehensive coverage

### Selection Criteria

Studies were selected based on relevance to NLP/ RE/ TE, focus on low-resource scenarios, English language availability, peer-reviewed status, and methodological rigor. The process reduced 283 initial results to 43 final papers through systematic filtering.


## Repository structure

### Folders structure

- **`scopus/`**
  - `scopus.csv`: Combined results from all Scopus queries.
  - `scopus_reducido.csv`: A subset of results for specific queries ('q31','q32','q33','q34','q46','q47','q48','q49','q61','q62','q63','q64').
  - `scopus.ipynb`: Jupyter notebook used to generate the `scopus.csv` and `scopus_reducido.csv` files from the individual query results.

- **`web_of_science/`**
  - `wos.csv`: Combined results from all Web of Science queries.
  - `wos_reducido.csv`: A subset of results for specific queries ('q31','q32','q33','q34','q46','q47','q48','q49','q61','q62','q63','q64').
  - `wos_reducido.ipynb`: Jupyter notebook used to generate the `wos.csv` and `wos_reducido.csv` files.

> These two folders contains subfolders for each query with results for both strategies (A and B) presented as .csv files, along with the corresponding papers in .pdf format.

- **`others/`**
  - Contains additional papers sourced from Google Scholar, Semantic Scholar, and venues like the Association for Computational Linguistics (ACL) Anthology.

- **`summary/`**
  - **`summary.csv`** & **`summary.xlsx`**: Contain the combined results from Web of Science and Scopus for queries ('q31','q32','q33','q34','q46','q47','q48','q49','q61','q62','q63','q64') after removing duplicates between platforms. Provided in both CSV and Excel formats.
  - **`summary_reduced.csv`** & **`summary_reduced.xlsx`**: Contain the refined results from the same query set after applying inclusion/ exclusion criteria and removing duplicates between platforms. Provided in both CSV and Excel formats.

- **`datasets/`**
  - Contains the datasets used in the works analyzed from the Scopus and Web of Science results.

### Project Files

- **`research_methodology.xlsx`**: Contains the work planning according to the paper's *Guidelines for performing systematic literature reviews in software engineering*[^1] strategy, as described in the research methodology section of each paper.
- **`queries.csv`**: Contains all search queries used in the study.
- **`characteristics.csv`**: Contains the common columns from both datasets that represent characteristics of the analyzed papers.
- **`seleccion.ipynb`**: Jupyter notebook that aggregates results from both platforms, removes duplicates, and applies inclusion/exclusion criteria. This notebook generates: `summary.csv`, `summary_reduced.csv`, `characteristics.csv`, `summary.xlsx`, and `summary_reduced.xlsx`.

> **Development Note:** This code was developed and run in a local environment. The repository contains the code as exported from that environment without subsequent execution here. The output elements can be in other paths, than the ones specified in the code.

[^1]: Keele, S. (2007). Guidelines for performing systematic literature reviews in software engineering (Vol. 5). Technical report, ver. 2.3 ebse technical report. ebse.


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


## Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.


## Declaration of Generative AI and AI-assisted technologies in the writing process

During the preparation of this work the author(s) used ChatGPT (https://chatgpt.com/) and Deepseek (https://chat.deepseek.com/) in order to polishing language for clarity, ensuring consistent citation style, structuring data in tables, and assisting in the formatting of scientific visuals. After using this tool/ service, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication.


## Funding

This work has received funding from the INESData project (Infrastructure to Investigate Data Spaces in Distributed Environments at UPM), a project funded under the UNICO I+D CLOUD call by the Ministry for Digital Transformation and the Civil Service, within the framework of the recovery plan PRTR financed by the European Union (NextGenerationEU).

In addition, this article is part of the TeresIA research project, funded by the European Union's Next GenerationEU/ PRTR funds through the Spanish Ministry of Economy and Digital Transformation (now the Ministry for Digital Transformation and Public Service).

