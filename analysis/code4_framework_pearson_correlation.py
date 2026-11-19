import json
import math
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "all_issue_v2.json"
FW = "Framework"
TAXONOMIES = [("L1", "Level1_Classification"), ("L2", "Level2_Classification"), ("Root cause", "Root_Cause_Classification")]


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


def pearson(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    dx = [value - mean_x for value in x]
    dy = [value - mean_y for value in y]
    sxx = sum(component * component for component in dx)
    syy = sum(component * component for component in dy)
    if sxx <= 1e-15 or syy <= 1e-15:
        return float("nan")
    return sum(a * b for a, b in zip(dx, dy)) / math.sqrt(sxx * syy)


with DATA.open(encoding="utf-8") as handle:
    records = json.load(handle)

total = len(records)

print("=" * 96)
print(" CODE 4 - PEARSON CORRELATION BETWEEN FRAMEWORKS ON L1 / L2 / ROOT CAUSE")
print(f" dataset : {DATA}")
print(f" issues  : {total}")
print(" profiles are category-share vectors; r is computed across categories")
print("=" * 96)

for name, field in TAXONOMIES:
    framework_counts = Counter()
    cross_table = defaultdict(Counter)
    for record in records:
        framework = record[FW].strip()
        category = record[field].strip()
        framework_counts[framework] += 1
        cross_table[framework][category] += 1

    frameworks = sorted(framework_counts, key=lambda item: (-framework_counts[item], item))
    categories = sorted({category for group in cross_table.values() for category in group})
    profiles = {framework: [cross_table[framework][category] / framework_counts[framework] for category in categories]
                for framework in frameworks}

    matrix = [[1.0 if a == b else pearson(profiles[a], profiles[b]) for b in frameworks] for a in frameworks]
    matrix_rows = [[frameworks[i]] + [f"{value:.4f}" for value in matrix[i]] for i in range(len(frameworks))]

    print()
    print("=" * 96)
    print(f" {name} - Pearson correlation matrix ({len(frameworks)} frameworks x {len(categories)} categories)")
    print("=" * 96)
    print(table(["Framework"] + frameworks, matrix_rows, "<" + ">" * len(frameworks)))
    print()
