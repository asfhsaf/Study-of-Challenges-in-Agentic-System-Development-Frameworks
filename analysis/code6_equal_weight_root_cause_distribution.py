import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "all_issue_v2.json"
FW = "Framework"
RC = "Root_Cause_Classification"


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
framework_rc = defaultdict(Counter)
pooled_rc = Counter()
for record in records:
    framework = record[FW].strip()
    root_cause = record[RC].strip()
    framework_counts[framework] += 1
    framework_rc[framework][root_cause] += 1
    pooled_rc[root_cause] += 1

frameworks = sorted(framework_counts)
count_frameworks = len(frameworks)
total = len(records)

equal_weight = {category: sum(framework_rc[fw][category] / framework_counts[fw] for fw in frameworks) / count_frameworks
                for category in pooled_rc}
direct = {category: pooled_rc[category] / total for category in pooled_rc}
order = sorted(pooled_rc, key=lambda name: (-equal_weight[name], name))

print(f"Code 6 - Root-cause distribution: equal-weighted vs direct ({count_frameworks} frameworks)")
print()
rows = [[category, pct(direct[category]), pct(equal_weight[category]), pp(equal_weight[category] - direct[category])]
        for category in order]
rows.append(["Total", pct(1.0), pct(1.0), pp(0.0)])
print(table(["Root-cause category", "Direct", "Equal-weighted", "Diff"], rows, "<>>>"))
