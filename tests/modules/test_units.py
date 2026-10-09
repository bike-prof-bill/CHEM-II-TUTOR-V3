"""Units as data: the generator's side of units.json."""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, ROOT)
import engine
fails = 0
def check(c, m):
    global fails
    if not c: fails += 1; print("  FAIL:", m)
check(abs(engine.convert(100, "degC", "K") - 373.15) < 1e-9, "degC -> K")
check(abs(engine.convert(1, "atm", "torr") - 760) < 1e-9, "atm -> torr")
check(engine.convert(1, "atm", "K") is None, "cross-dimension is None")
check(engine.dim_of("kJ/mol") == {"J": 1, "mol": -1} and engine.dim_of("1/K") == {"K": -1} and engine.dim_of("") == {}, "dimension vectors")
check(engine.canonical_unit("pressure") == "atm", "canonical unit")
for u, d in engine.UNITS["units"].items():
    check(d["dimension"] in engine.UNITS["dimensions"], f"unit {u} names a known dimension")
    check(all(isinstance(a, str) and a for a in d["aliases"]), f"unit {u} aliases are strings")
owner = {}
for u, d in engine.UNITS["units"].items():
    for a in d["aliases"]:
        k = a.replace(" ", "").lower()
        check(owner.setdefault(k, u) == u, f"alias {a!r} is claimed by both {owner[k]} and {u}")
print(f"units (python): {'all pass' if not fails else str(fails) + ' failed'}"); sys.exit(1 if fails else 0)
