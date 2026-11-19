import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "all_issue_v2.json"
L1 = "Level1_Classification"
L2 = "Level2_Classification"


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


def indent(text):
    return "\n".join("    " + line for line in text.splitlines())


with DATA.open(encoding="utf-8") as handle:
    records = json.load(handle)

total = len(records)
l1_counts = Counter()
l1_to_l2 = defaultdict(Counter)
for record in records:
    level1 = record[L1].strip()
    l1_counts[level1] += 1
    l1_to_l2[level1][record[L2].strip()] += 1

l1_order = sorted(l1_counts, key=lambda name: (-l1_counts[name], name))
l1_rows = [[level1, l1_counts[level1], pct(l1_counts[level1] / total)] for level1 in l1_order]
l1_rows.append(["Total", total, pct(1.0)])

print(f"Code 1 - Level-1 and level-2 distribution, n = {total}")
print()
print("L1 distribution")
print(table(["Level 1 category", "Count", "Share of all issues"], l1_rows, "<>>"))

for index, level1 in enumerate(l1_order, start=1):
    group_total = l1_counts[level1]
    rows = [[level2, count, pct(count / group_total), pct(count / total)]
            for level2, count in sorted(l1_to_l2[level1].items(), key=lambda item: (-item[1], item[0]))]
    rows.append(["Subtotal", group_total, pct(1.0), pct(group_total / total)])
    print()
    print(f"[{index}/{len(l1_order)}] {level1}  -  {group_total} issues  -  {pct(group_total / total)} of all issues")
    print("    L2 distribution")
    print(indent(table(["Level 2 category", "Count", "Share within L1", "Share of all issues"], rows, "<>>>")))
