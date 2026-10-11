"""Regression (rebuild spec, Change 2): the fortuitous filter guarded only the final key. Now every declared
number is checked: two entries of different state within tolerance, a trap near a same-state entry, or a given
landing on the key after unit conversion all reject the variant."""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "archetypes"))
import engine

def E(id, state, role, value, unit="", tol=0.01, **kw):
    d = {"id": id, "state": state, "role": role, "label": id, "value": value, "unit": unit, "abs_tol": tol, "dim": engine.dim_of(unit)}; d.update(kw); return d
def variant(expected, traps=(), board=()):
    return {"expected": list(expected), "traps": list(traps), "board": list(board) or [{"state": e["state"], "kind": "number"} for e in expected if e["state"]]}

fails = 0
def check(cond, msg):
    global fails
    if not cond: fails += 1; print("  FAIL:", msg)

# 1. two different states, same unitless number -> ambiguous
v = variant([E("ratio", "substituted", "intermediate", 1.36), E("key_value_found", "value_found", "key", 1.36, "", 0.03, require_unit=False)])
check(any(r[0] == "ambiguous" for r in engine.validate(v)), "intermediate equal to the key is rejected")

# 2. same number, but the key requires its unit and the units differ -> the unit settles it, not ambiguous
v = variant([E("ratio", "substituted", "intermediate", 1.36), E("key_value_found", "value_found", "key", 1.36, "atm", 0.03, require_unit=True)])
check(not engine.validate(v), "unitless ratio vs unit-requiring key in atm is settled by the unit")

# 3. trap within three windows of the same-state key -> rejected (the old filter)
v = variant([E("key_value_found", "value_found", "key", 350.0, "K", 1.0, require_unit=True)], traps=[{"id": "X", "state": "value_found", "value": 352.0, "unit": "K", "abs_tol": 1.0}])
check(any(r[0] == "trap_near_expected" for r in engine.validate(v)), "trap near the key is rejected")

# 4. trap within three windows of a same-state INTERMEDIATE -> rejected (new: not only the key)
v = variant([E("T1_in_K", "T_in_K", "intermediate", 300.0, "K", 0.2), E("key_value_found", "value_found", "key", 350.0, "K", 1.0, require_unit=True)],
            traps=[{"id": "X", "state": "T_in_K", "value": 300.4, "unit": "K", "abs_tol": 0.2}])
check(any(r[0] == "trap_near_expected" for r in engine.validate(v)), "trap near an intermediate is rejected")

# 5. a given that lands on the key after unit conversion -> rejected
v = variant([E("key_value_found", "value_found", "key", 760.2, "torr", 15.0, require_unit=True), E("g_P1", None, "given", 1.0, "atm", 1e-6)])
check(any(r[0] == "given_near_key" for r in engine.validate(v)), "1 atm given lands on a 760 torr key after conversion")

# 6. a given that is merely the same number in another unit of a conversion step is NOT a collision
v = variant([E("dH_in_J", "dH_in_J", "intermediate", 39900.0, "J/mol", 200.0), E("g_dH", None, "given", 39.9, "kJ/mol", 4e-5),
             E("key_value_found", "value_found", "key", 350.0, "K", 1.0, require_unit=True)])
check(not engine.validate(v), "39.9 kJ/mol given and 39900 J/mol step do not collide")

# 7. an intermediate equal to a given is removed, not rejected, while another route to its state remains
v = variant([E("ratio", "substituted", "intermediate", 1.36), E("ln_ratio", "substituted", "intermediate", 0.3075, "", 0.005),
             E("g_P2", None, "given", 1.36, "atm", 1e-6), E("key_value_found", "value_found", "key", 350.0, "K", 1.0, require_unit=True)])
check(not engine.validate(v) and v.get("dropped") == ["ratio"] and len(v["expected"]) == 3, "restated-given intermediate dropped, variant ships")

# 8. ... but if it was the only route, the variant is rejected
v = variant([E("ratio", "substituted", "intermediate", 1.36), E("g_P2", None, "given", 1.36, "atm", 1e-6),
             E("key_value_found", "value_found", "key", 350.0, "K", 1.0, require_unit=True)])
check(any(r[0] == "ambiguous" for r in engine.validate(v)), "dropping the only evidence for a state rejects the variant")

# 9. the shipped bundle: every variant passes validation and every number carries a dimension
import ch10_cc as A
out = engine.build(A, 2, 9000)
check(all(not engine.validate(dict(v, expected=list(v["expected"]))) for v in out["variants"]), "every shipped variant validates")
check(all("dim" in e for v in out["variants"] for e in v["expected"]), "every declared number carries dim")

print(f"collision_rejected_by_generator: {9 - fails} of 9 checks pass"); sys.exit(1 if fails else 0)
