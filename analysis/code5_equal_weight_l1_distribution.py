import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "all_issue_v2.json"
FW = "Framework"
L1 = "Level1_Classification"


def pct(value):
    return f"{value * 100:.2f}%"


def pp(value):
    points = round(value * 100, 2)
    return "0.00pp" if points == 0 else f"{points:+.2f}pp"


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

framework_counts = Counter()
framework_l1 = defaultdict(Counter)
pooled_l1 = Counter()
for record in records:
    framework = record[FW].strip()
    level1 = record[L1].strip()
    framework_counts[framework] += 1
    framework_l1[framework][level1] += 1
    pooled_l1[level1] += 1

frameworks = sorted(framework_counts)
count_frameworks = len(frameworks)
total = len(records)

equal_weight = {category: sum(framework_l1[fw][category] / framework_counts[fw] for fw in frameworks) / count_frameworks
                for category in pooled_l1}
direct = {category: pooled_l1[category] / total for category in pooled_l1}
order = sorted(pooled_l1, key=lambda name: (-equal_weight[name], name))

print(f"Code 5 - Level-1 distribution: equal-weighted vs direct ({count_frameworks} frameworks)")
print()
rows = [[category, pct(direct[category]), pct(equal_weight[category]), pp(equal_weight[category] - direct[category])]
        for category in order]
rows.append(["Total", pct(1.0), pct(1.0), pp(0.0)])
print(table(["Level 1 category", "Direct", "Equal-weighted", "Diff"], rows, "<>>>"))
