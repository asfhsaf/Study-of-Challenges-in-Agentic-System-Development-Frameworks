Dataset Description
This repository contains three Excel files that store raw GitHub issue data and annotation results for an empirical study on LLM-based agentic system development frameworks. Detailed descriptions of each file are provided below:

1. `all_issue.xlsx`
This dataset aggregates all GitHub issue records adopted in this empirical study, which systematically analyzes various development challenges of six mainstream LLM agent frameworks, namely Agno, AutoGen, CrewAI, LangChain, LangGraph and Letta. A total of 1,149 issue reports were collected and filtered for subsequent thematic classification and root cause analysis.

2. `issue_part1.xlsx`
This file corresponds to the pilot annotation subset of the full dataset. We randomly sampled 654 issues (approximately 57% of the entire dataset) to conduct pilot labeling. Through iterative analysis of this pilot sample via open coding, we constructed a two-dimensional taxonomy covering challenge themes and root causes from scratch.

3. `issue_part2_label1.xlsx` and `issue_part2_label2.xlsx`
These two files hold dual independent annotation results for all remaining issues excluding the pilot samples. Specifically, `issue_part2_label1.xlsx` contains the labeling results of the residual dataset completed independently by Author 1, while `issue_part2_label2.xlsx` records the separate annotations produced by Author 2 on the identical set of remaining data. The dual independent labeling design is adopted to evaluate the inter-annotator agreement of the coding scheme developed in the pilot phase.