"""Reproduce the page from archived numeric source files, no network required."""
from pathlib import Path
from decimal import Decimal, getcontext
import json, math, statistics

getcontext().prec = 35
ROOT = Path(__file__).parent
D = json.loads((ROOT / 'data.json').read_text())
rows = D['annual']
by = {r['year']: r for r in rows}
results = []
for r in rows:
    # Algorithm 1: monthly-equivalent wage / CNY-per-gram reference.
    grams = r['nonprivate'] / 12 / r['gold']
    # Algorithm 2: convert wage CNY -> USD -> troy ounces -> grams,
    # using high precision Decimal and raw gold/FX source values.
    second = (Decimal(str(r['nonprivate'])) / Decimal(12)
              / Decimal(str(r['fx'])) / Decimal(str(r['gold_usd']))
              * Decimal('31.1034768'))
    assert math.isclose(grams, float(second), rel_tol=1e-12)
    private = None if r['private'] is None else r['private'] / 12 / r['gold']
    results.append({'year': r['year'], 'nonprivate_grams': grams,
                    'private_grams': private, 'decimal_crosscheck': str(second)})
g = {r['year']: r['nonprivate_grams'] for r in results}
key = {
    'gram2005': g[2005], 'gram2015': g[2015], 'gram2018': g[2018], 'gram2025': g[2025],
    'private2025': by[2025]['private'] / 12 / by[2025]['gold'],
    'change2015': g[2025] / g[2015] - 1,
    'change2005': g[2025] / g[2005] - 1,
    'wage_ratio2015': by[2025]['nonprivate'] / by[2015]['nonprivate'],
    'gold_ratio2015': by[2025]['gold'] / by[2015]['gold'],
    'fixed2015price2025wage': by[2025]['nonprivate'] / 12 / by[2015]['gold'],
    'wage_ratio2005': by[2025]['nonprivate'] / by[2005]['nonprivate'],
    'gold_ratio2005': by[2025]['gold'] / by[2005]['gold'],
    'cpi_ratio2005': by[2025]['cpi'] / by[2005]['cpi'],
    'latest_fixed_wage_grams': by[2025]['nonprivate'] / 12 / D['latest']['price'],
}
assert [r['year'] for r in rows] == list(range(2005, 2026))
assert max(results, key=lambda r: r['nonprivate_grams'])['year'] == 2018
assert all(by[y]['private'] is None for y in range(2005, 2009))
assert round(key['gram2005'], 2) == 12.95
assert round(key['gram2015'], 2) == 22.24
assert round(key['gram2025'], 2) == 13.65
assert round(key['private2025'], 2) == 7.55
assert statistics.mean([4000, 5000, 6000, 7000, 28000]) == 10000
assert statistics.median([4000, 5000, 6000, 7000, 28000]) == 6000
for y in [2005, 2011, 2015, 2018, 2021]:
    ratio = (by[2025]['nonprivate'] / by[y]['nonprivate']) / (by[2025]['gold'] / by[y]['gold'])
    assert math.isclose(g[2025] / g[y], ratio)
out = {'annual': results, 'key_metrics': key, 'checks': {'yearly_decimal_crosschecks': len(rows), 'all_passed': True}}
(ROOT / 'calculated.json').write_text(json.dumps(out, ensure_ascii=False, indent=2))
print(json.dumps(key, ensure_ascii=False, indent=2))
