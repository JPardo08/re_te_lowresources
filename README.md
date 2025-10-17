# Relation Extraction (RE) and Triplet Extraction (TE) in Low-resource scenarios. 

## Abstracts

### From Relation Extraction to Triplet Extraction: A Survey on Low-Resource Scenarios
Recent advances in generative frameworks have shifted Relation Extraction (RE) toward Triplet Extraction (TE), framing Information Extraction (IE) as an open-schema generation of *(subject, predicate, object)* triplets. This work provides a structured overview of current solutions, research gaps, and future directions for RE and TE in low-resource scenarios. This survey focuses exclusively on low-resource scenarios, defined by limited availability of annotated data and/or the absence of supporting resources such as external vocabularies or ontologies, which are typically leveraged to identify and extract entities and relations. The goal is stated by four key objectives: (1) illustrate the conceptual foundations of RE and TE, including their similarities and differences; (2) formally defining low-resource scenarios and characterizing their key challenges; (3) analyzing State-of-The-Art (SoTA) methods within their efficacy in low-resource settings for solving RE and TE; and finally, (4) future directions of RE/ TE in such settings.

### Bridging the Data Gap: A Comprehensive Review of Datasets for Low-Resource Relation and Triplet Extraction
Generative frameworks are redefining Information Extraction (IE), recasting it from Relation Extraction (RE) into open-schema Triplet Extraction (TE); the direct generation of *(subject, predicate, object)* triples. This progression, however, presents significant evaluation challenges in low-resource scenarios, where annotated data and supporting resources are scarce. This survey addresses this gap by providing a comprehensive assessment of existing benchmarks for evaluating RE and TE under these constrained conditions. A core contribution is the systematic summary of relevant datasets, ranging from standardized benchmarks to those designed for domain-specific and multilingual challenges. The survey details how these resources are applied and transformed for low-resource settings, including their use in adversarial learning and task-reformulation strategies. By mapping the landscape of available resources and methodologies, this work aims to guide future research toward more robust and reproducible progress in low-resource IE.


## Research strategy 
This semi-systematic literature review follows the methodology outlined by * *, focusing on three key research questions about Relation Extraction (RE) and Triplet Extraction (TE) in low-resource scenarios.

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

- **`datasets/`**
  - Contains the datasets used in the works analyzed from the Scopus and Web of Science results.

### Project Files

- **`research_methodology.xlsx`**: Contains the work planning according to the paper's *keele2007guidelines* strategy, as described in the research methodology section of each paper.
- **`queries.csv`**: Contains all search queries used in the study.
- **`summary.csv`** & **`summary.xlsx`**: Contain the combined results from Web of Science and Scopus for queries ('q31','q32','q33','q34','q46','q47','q48','q49','q61','q62','q63','q64') after removing duplicates between platforms. Provided in both CSV and Excel formats.
- **`summary_reduced.csv`** & **`summary_reduced.xlsx`**: Contain the refined results from the same query set after applying inclusion/exclusion criteria and removing duplicates between platforms. Provided in both CSV and Excel formats.
- **`characteristics.csv`**: Contains the common columns from both datasets that represent characteristics of the analyzed papers.

- **`seleccion.ipynb`**: Jupyter notebook that aggregates results from both platforms, removes duplicates, and applies inclusion/exclusion criteria. This notebook generates: `summary.csv`, `summary_reduced.csv`, `characteristics.csv`, `summary.xlsx`, and `summary_reduced.xlsx`.

> **Development Note:** This code was developed and run in a local environment. The repository contains the code as exported from that environment without subsequent execution here.


## Declaration of competing interest
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.


## Declaration of Generative AI and AI-assisted technologies in the writing process
During the preparation of this work the author(s) used ChatGPT (https://chatgpt.com/) and Deepseek (https://chat.deepseek.com/) for in order to polishing language for clarity, ensuring consistent citation style, structuring data in tables, and assisting in the formatting of scientific visuals. After using this tool/service, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication.


## Funding
This work has received funding from the INESData project (Infrastructure to Inves- tigate Data Spaces in Distributed Environ- ments at UPM), a project funded under the UNICO I+D CLOUD call by the Ministry for Digital Transformation and the Civil Service, within the framework of the recovery plan PRTR financed by the European Union (NextGenerationEU).

In addition, this article is part of the TeresIA research project, funded by the European Union's Next GenerationEU/ PRTR funds through the Spanish Ministry of Economy and Digital Transformation ( now the Ministry for Digital Transformation and Public Service).

