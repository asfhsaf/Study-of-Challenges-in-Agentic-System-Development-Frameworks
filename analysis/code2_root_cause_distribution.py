import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "all_issue_v2.json"
RC = "Root_Cause_Classification"


def pct(value):
    return f"{value * 100:.2f}%"


def table(headers, rows, aligns=None):
    head = [str(h) for h in headers]
    body = [[str(c) for c in row] for row in rows]
    widths = [max([len(head[c])] + [len(row[c]) for row in body]) for c in range(len(head))]
    pattern = aligns or ("<" + ">" * (len(head) - 1))
    lines = [" | ".join(f"{head[c]:{pattern[c]}{widths[c]}}" for c in range(len(head))),
             "-+-".join("-" * w for w in widths)]
    for row in body:
        lines.append(" | ".join(f"{row[c]:{pattern[c]}{widths[c]}}" for c in range(len(head))))
    return "\n".join(lines)


with DATA.open(encoding="utf-8") as handle:
    records = json.load(handle)

total = len(records)
counts = Counter(record[RC].strip() for record in records)
ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))

print("=" * 86)
print(" CODE 2 - ROOT-CAUSE DISTRIBUTION")
print(f" dataset : {DATA}")
print(f" issues  : {total}")
print(f" root-cause categories : {len(counts)}")
print("=" * 86)
print()

rows = []
cumulative = 0
for rank, (cause, count) in enumerate(ordered, start=1):
    cumulative += count
    rows.append([rank, cause, count, pct(count / total), pct(cumulative / total)])
rows.append(["", "Total", total, pct(1.0), pct(1.0)])

print(table(["Rank", "Root-cause category", "Count", "Share of all issues", "Cumulative share"], rows, "><>>>"))
