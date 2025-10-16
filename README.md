# Relation Extraction (RE) and Triplet Extraction (TE) in Low-resource scenarios. 


## From Relation Extraction to Triplet Extraction: A Survey on Low-Resource Scenarios
Recent advances in generative frameworks have shifted Relation Extraction (RE) toward Triplet Extraction (TE), framing Information Extraction (IE) as an open-schema generation of \textit{(subject, predicate, object)} triplets. This work provides a structured overview of current solutions, research gaps, and future directions for RE and TE in low-resource scenarios. This survey focuses exclusively on low-resource scenarios, defined by limited availability of annotated data and/or the absence of supporting resources such as external vocabularies or ontologies, which are typically leveraged to identify and extract entities and relations. The goal is stated by four key objectives: (1) illustrate the conceptual foundations of RE and TE, including their similarities and differences; (2) formally defining low-resource scenarios and characterizing their key challenges; (3) analyzing State-of-The-Art (SoTA) methods within their efficacy in low-resource settings for solving RE and TE; and finally, (4) future directions of RE/ TE in such settings.

## Bridging the Data Gap: A Comprehensive Review of Datasets for Low-Resource Relation and Triplet Extraction
Generative frameworks are redefining Information Extraction (IE), recasting it from Relation Extraction (RE) into open-schema Triplet Extraction (TE); the direct generation of \textit{(subject, predicate, object)} triples. This progression, however, presents significant evaluation challenges in low-resource scenarios, where annotated data and supporting resources are scarce. This survey addresses this gap by providing a comprehensive assessment of existing benchmarks for evaluating RE and TE under these constrained conditions. A core contribution is the systematic summary of relevant datasets, ranging from standardized benchmarks to those designed for domain-specific and multilingual challenges. The survey details how these resources are applied and transformed for low-resource settings, including their use in adversarial learning and task-reformulation strategies. By mapping the landscape of available resources and methodologies, this work aims to guide future research toward more robust and reproducible progress in low-resource IE.

## Repository structure

### Folders
- scopus: this folder cotains the scopus results structurated by each query
    - scopus_reducido.csv: contains the results for specific queries ('q31','q32','q33','q34','q46','q47','q48','q49','q61','q62','q63','q64')
    - scopus.csv: contains the results for all queries
    - scopus.ipynb: extract and aggroup the queries results into one csv. From this notebook emerge scopus.csv and scopus_reducido.csv.
- web_of_science: this folder cotains the web of science results structurated by each query 
    - wos_reducido.csv: contains the results for specific queries ('q31','q32','q33','q34','q46','q47','q48','q49','q61','q62','q63','q64')
    - wos.csv: contains the results for all queries
    - wos_reducido.ipynb: extract and aggroup the queries results into one csv. From this notebook emerge wos.csv and wos_reducido.csv.
- others: papers used in the research extracted from Google Scholar, and Semantic Scholar, along with journals and conferences like Association for Computational Linguistics (ACL) Anthology
- datasets: contains the datasets used in the works analysed from scopus and web of science. 

### Files
- research methodology.xlsx: contains the planification of the work according to the paper's \cite{keele2007guidelines} strategy, described in research methodology section of each paper
- queries.csv: contains all queries
- summary.csv: contains the results of the set of queries ('q31','q32','q33','q34','q46','q47','q48','q49','q61','q62','q63','q64') for web of science and scopus without duplicates between platforms
- summary.xlsx: contains the results of the set of queries ('q31','q32','q33','q34','q46','q47','q48','q49','q61','q62','q63','q64') for web of science and scopus without duplicates between platforms in excel format
- summary_reduced.xlsx: contains the results of the set of queries ('q31','q32','q33','q34','q46','q47','q48','q49','q61','q62','q63','q64') for web of science and scopus without duplicates between platforms and with the inclusion/ exclusion criteria
- summary_reduced.csv: contains the results of the set of queries ('q31','q32','q33','q34','q46','q47','q48','q49','q61','q62','q63','q64') for web of science and scopus without duplicates between platforms and with the inclusion/ exclusion criteria in excel format
- characteristics.csv: common columns in both datasets representing characteristics of papers

- seleccion.ipynb: this notebook aggroup the results from both platforms, remove duplicates and applies inclusion/ exclusion criteria. From this notebook emerge summary.csv, summary_reduced.csv, characteristics.csv, summary.xlsx, and summary_reduced.xlsx 



## Declaration of competing interest
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.


## Declaration of Generative AI and AI-assisted technologies in the writing process
During the preparation of this work the author(s) used ChatGPT (https://chatgpt.com/) and Deepseek (https://chat.deepseek.com/) for in order to polishing language for clarity, ensuring consistent citation style, structuring data in tables, and assisting in the formatting of scientific visuals. After using this tool/service, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication.


## Funding
This work has received funding from the INESData project (Infrastructure to Inves- tigate Data Spaces in Distributed Environ- ments at UPM), a project funded under the UNICO I+D CLOUD call by the Ministry for Digital Transformation and the Civil Service, within the framework of the recovery plan PRTR financed by the European Union (NextGenerationEU).

In addition, this article is part of the TeresIA research project, funded by the European Union's Next GenerationEU/ PRTR funds through the Spanish Ministry of Economy and Digital Transformation ( now the Ministry for Digital Transformation and Public Service).

