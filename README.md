# A Comprehensive Study of Challenges in LLM based Agentic System Development Frameworks

## data

This directory aggregates all GitHub issue records adopted in this empirical study, which systematically analyzes various development challenges of six mainstream LLM agent frameworks, namely Agno, AutoGen, CrewAI, LangChain, LangGraph and Letta. A total of 1,149 issue reports were collected and filtered for subsequent thematic classification and root cause analysis.

- `issue_part1.json` — Pilot annotation subset: 654 randomly sampled issues (approximately 57% of the full dataset), used to construct the two-dimensional taxonomy covering challenge themes and root causes through open coding.
- `issue_part2_label1.json` — Independent annotation results from the first annotator for the remaining 495 issues.
- `issue_part2_label2.json` — Independent annotation results from the second annotator for the same 495 issues.
- `issue_part2_final.json` — Adjudicated final labels for the 495 part-2 issues: the 456 issues with full agreement were kept unchanged, while the 39 conflicting cases were resolved through adjudication.
- `all_issue_v1.json` — Consolidated dataset of all 1,149 issues, obtained by merging `issue_part1.json` and `issue_part2_final.json`; every issue carries a final theme label and a concrete root cause label.
- `all_issue_v2.json` — The final, complete dataset of all 1,149 issues, obtained after the final reassessment of root-cause uncertainty.

## annotation_reference

**Main reference for annotation**: 7 top-level themes, 20 sub-themes, and 12 root causes.

## analysis

Python scripts for the empirical analyses and label verification.



---

**Root-Cause Uncertainty Labeling**

First, we re-examined the issues in part 2 (Reliability Analysis) on which the two annotators disagreed, and merged the result with part 1 to obtain the complete dataset of 1,149 issues (`data/all_issue_v1.json`). We then conducted an uncertainty analysis on this dataset, assigning a new `Uncertain` label to issues whose evidence was insufficient to determine a specific mechanism, and produced the final dataset (`data/all_issue_v2.json`). 

Before the uncertainty analysis (`data/all_issue_v1.json`), the root-cause distribution was: Model API Compatibility & Adaptation Insufficient 17.8%, State & Session Management Chaos 14.9%, Tool Calling Mechanism Defects 12.9%, Async & Streaming Processing Defects 8.3%, Dependency & Version Management Issues 7.8%, Others 7.7%, Serialization & Data Persistence Issues 7.6%, Error Handling & Retry Logic Incomplete 5.7%, Event Stream & Protocol Implementation Incomplete 5.4%, Documentation & Examples Inaccurate 4.6%, Performance & Observability Missing 3.6%, Security & Authentication Config Missing 2.2%, and Multi-agent Collaboration Logic Defects 1.7%. After the analysis (`data/all_issue_v2.json`), the distribution was: Model API Compatibility & Adaptation Insufficient 16.8%, State & Session Management Chaos 13.1%, Tool Calling Mechanism Defects 11.6%, Others 10.8%, Async & Streaming Processing Defects 7.6%, Dependency & Version Management Issues 7.2%, Serialization & Data Persistence Issues 7.0%, Uncertain 5.6%, Error Handling & Retry Logic Incomplete 5.3%, Event Stream & Protocol Implementation Incomplete 4.7%, Documentation & Examples Inaccurate 3.9%, Performance & Observability Missing 3.4%, Security & Authentication Config Missing 1.7%, and Multi-agent Collaboration Logic Defects 1.5%.
