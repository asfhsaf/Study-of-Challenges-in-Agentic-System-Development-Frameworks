import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LABEL1 = ROOT / "data" / "issue_part2_label1.json"
LABEL2 = ROOT / "data" / "issue_part2_label2.json"
FIELDS = [("Level 2", "Level2_Classification"), ("Root cause", "Root_Cause_Classification")]


def pct(value):
    return f"{value * 100:.2f}%"


def load(path):
    with path.open(encoding="utf-8") as handle:
        return {(rec["Framework"], rec["ID"]): rec for rec in json.load(handle)}


def cohen_kappa(pairs):
    n = len(pairs)
    categories = sorted({a for a, _ in pairs} | {b for _, b in pairs})
    joint = Counter(pairs)
    row_totals = Counter(a for a, _ in pairs)
    col_totals = Counter(b for _, b in pairs)
    observed = sum(joint[(c, c)] for c in categories) / n
    expected = sum((row_totals[c] / n) * (col_totals[c] / n) for c in categories)
    kappa = (observed - expected) / (1.0 - expected) if abs(1.0 - expected) > 1e-12 else float("nan")
    return len(categories), observed, expected, kappa


first = load(LABEL1)
second = load(LABEL2)
keys = sorted(first)

rows = []
for name, field in FIELDS:
    pairs = [(first[key][field].strip(), second[key][field].strip()) for key in keys]
    categories, observed, expected, kappa = cohen_kappa(pairs)
    rows.append((name, categories, pct(observed), pct(expected), kappa))

print(f"Code 0 - Cohen's kappa (label1 vs label2), n = {len(keys)}")
print()
print(f"{'Taxonomy':<12}{'Categories':>12}{'Observed':>11}{'Expected':>11}{'Kappa':>8}")
print("-" * 54)
for name, categories, observed, expected, kappa in rows:
    print(f"{name:<12}{categories:>12}{observed:>11}{expected:>11}{kappa:>8.4f}")
