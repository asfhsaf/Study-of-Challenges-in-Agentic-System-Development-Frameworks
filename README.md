# A Comprehensive Study of Challenges in LLM based Agentic System Development Frameworks

## data

This directory aggregates all GitHub issue records adopted in this empirical study, which systematically analyzes various development challenges of six mainstream LLM agent frameworks, namely Agno, AutoGen, CrewAI, LangChain, LangGraph and Letta. A total of 1,149 issue reports were collected and filtered for subsequent thematic classification and root cause analysis.

- `issue_part1.json` — Pilot annotation subset: 654 randomly sampled issues (approximately 57% of the full dataset), used to construct the two-dimensional taxonomy covering challenge themes and root causes through open coding.
- `issue_part2_label1.json` — Independent annotation results from the first annotator for the remaining 495 issues.
- `issue_part2_label2.json` — Independent annotation results from the second annotator for the same 495 issues.
- `issue_part2_final.json` — Adjudicated final labels for the 495 part-2 issues: the 456 issues with full agreement were kept unchanged, while the 39 conflicting cases were resolved through adjudication.
- `all_issue_v1.json` — Consolidated dataset of all 1,149 issues, obtained by merging `issue_part1.json` and `issue_part2_final.json`; every issue carries a final theme label and a concrete root cause label.
- `all_issue_v2.json` — The final, complete dataset of all 1,149 issues, obtained after the final reassessment of root-cause uncertainty.

## annotation_reference/

 Basis for reference labeling

## analysis/

Python scripts for the empirical analyses and label verification.
