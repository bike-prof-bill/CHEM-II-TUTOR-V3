"""The universal substance table: every record well-formed, sourced, and physically ordered; the loader refuses silent defaults."""
import sys, os, json
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "archetypes"))
import _substances as S
fails = 0
def check(c, m):
    global fails
    if not c: fails += 1; print("  FAIL:", m)
for name, rec in S.SUBSTANCES.items():
    for f, v in rec.items():
        if f in ("formula", "class", "source"): continue   # text fields
        check(isinstance(v, (int, float)), f"{name}.{f} is numeric")
        check(f in rec.get("source", {}), f"{name}.{f} names its source")
    if "melting_point_C" in rec and "boiling_point_C" in rec: check(rec["melting_point_C"] < rec["boiling_point_C"], f"{name}: melts below it boils")
    if "dHvap_at_Tb_kJ_mol" in rec: check(5 < rec["dHvap_at_Tb_kJ_mol"] < 100, f"{name}: dHvap in a physical range")
try: S.get("unobtainium", "boiling_point_C"); check(False, "unknown substance must raise")
except KeyError: pass
try: S.get("water", "Kf_K_kg_mol"); check(False, "a missing field must raise, not default")
except KeyError: pass
check(len(S.SUBSTANCES) >= 20, "twenty substances present")
print(f"substances: {len(S.SUBSTANCES)} records, {'all pass' if not fails else str(fails) + ' failed'}"); sys.exit(1 if fails else 0)
