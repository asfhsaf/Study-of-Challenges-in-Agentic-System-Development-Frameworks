import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "all_issue_v2.json"
FW = "Framework"
L1 = "Level1_Classification"
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


def indent(text):
    return "\n".join("    " + line for line in text.splitlines())


with DATA.open(encoding="utf-8") as handle:
    records = json.load(handle)

total = len(records)
framework_counts = Counter()
l1_table = defaultdict(Counter)
rc_table = defaultdict(Counter)
for record in records:
    framework = record[FW].strip()
    framework_counts[framework] += 1
    l1_table[framework][record[L1].strip()] += 1
    rc_table[framework][record[RC].strip()] += 1

frameworks = sorted(framework_counts, key=lambda name: (-framework_counts[name], name))
l1_categories = sorted({category for group in l1_table.values() for category in group})
rc_categories = sorted({category for group in rc_table.values() for category in group})


def pivot(cross_table, categories):
    rows = []
    for category in categories:
        rows.append([category]
                    + [pct(cross_table[framework][category] / framework_counts[framework]) for framework in frameworks]
                    + [pct(sum(cross_table[framework][category] for framework in frameworks) / total)])
    return rows


print("=" * 96)
print(" CODE 3 - LEVEL-1 AND ROOT-CAUSE DISTRIBUTIONS BY FRAMEWORK")
print(f" dataset : {DATA}")
print(f" issues  : {total}")
print(f" frameworks : {len(frameworks)}   level-1 categories : {len(l1_categories)}   root-cause categories : {len(rc_categories)}")
print("=" * 96)
print()
print("TABLE 1 - Framework overview")
print()
print(table(["Framework", "Issues", "Share of all issues"],
            [[framework, framework_counts[framework], pct(framework_counts[framework] / total)] for framework in frameworks]
            + [["Total", total, pct(1.0)]], "<>>"))
print()
print("TABLE 2 - Level-1 distribution by framework (share within each framework)")
print("          Each column sums to 100.00%; the last column is the share of the whole dataset.")
print()
print(table(["Level 1 category"] + frameworks + ["All frameworks"], pivot(l1_table, l1_categories), "<" + ">" * (len(frameworks) + 1)))
print()
print("TABLE 3 - Root-cause distribution by framework (share within each framework)")
print("          Each column sums to 100.00%; the last column is the share of the whole dataset.")
print()
print(table(["Root-cause category"] + frameworks + ["All frameworks"], pivot(rc_table, rc_categories), "<" + ">" * (len(frameworks) + 1)))
print()
print("=" * 96)
print(" PER-FRAMEWORK BREAKDOWN")
print("=" * 96)

for index, framework in enumerate(frameworks, start=1):
    framework_total = framework_counts[framework]
    l1_rows = [[category, count, pct(count / framework_total), pct(count / total)]
               for category, count in sorted(l1_table[framework].items(), key=lambda item: (-item[1], item[0]))]
    l1_rows.append(["Subtotal", framework_total, pct(1.0), pct(framework_total / total)])
    rc_rows = [[category, count, pct(count / framework_total), pct(count / total)]
               for category, count in sorted(rc_table[framework].items(), key=lambda item: (-item[1], item[0]))]
    rc_rows.append(["Subtotal", framework_total, pct(1.0), pct(framework_total / total)])

    print()
    print(f"[{index}/{len(frameworks)}] {framework}  -  {framework_total} issues  -  {pct(framework_total / total)} of all issues")
    print("  level-1 distribution:")
    print(indent(table(["Level 1 category", "Count", "Share within framework", "Share of all issues"], l1_rows, "<>>>")))
    print("  root-cause distribution:")
    print(indent(table(["Root-cause category", "Count", "Share within framework", "Share of all issues"], rc_rows, "<>>>")))
