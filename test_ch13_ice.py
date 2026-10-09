"""Independent checks on the second archetype. Keys are re-derived here by bisection on the mass-action equation,
written separately from the archetype's closed forms; the table is checked for I + C = E at a trial x."""
import sys, math; sys.path.insert(0, "archetypes"); import engine, ch13_ice as A
fails = 0
def check(c, m):
    global fails
    if not c: fails += 1; print("  FAIL:", m)
def mass_action(P, x):
    num = den = 1.0
    for i, s in enumerate(P["side"]):
        v = P["init_M"][i] + s * P["coef"][i] * x
        if s > 0: num *= v ** P["coef"][i]
        else: den *= v ** P["coef"][i]
    return num / den
def x_by_bisection(P):
    lo, hi = 0.0, P["init_M"][0] / P["coef"][0] * 0.999999
    for _ in range(200):
        m = 0.5 * (lo + hi)
        if mass_action(P, m) < P["K"]: lo = m
        else: hi = m
    return 0.5 * (lo + hi)
def ev(expr, x):   # tiny evaluator for the table's cell strings: numbers, x, + - and implied multiply like "2x"
    e = expr.replace("−", "-").replace(" ", "")
    import re
    e = re.sub(r"(\d)x", r"\1*x", e); e = re.sub(r"(^|[+\-])x", r"\g<1>1*x", e)
    return eval(e, {"__builtins__": {}}, {"x": x})

openers = engine.read_openers("content_ch13_ice_openers.csv"); moves = engine.read_moves("content_ch13_ice_moves.csv")
out = engine.build(A, 1, 1, openers, moves)
check(len(out["variants"]) == sum(len(o["fits"]) for o in openers), "one variant per (opener, fitting problem)")
seen = set()
for v in out["variants"]:
    P = [f for f in A.FIXED if f["id"] == v["fixed_id"]][0]; seen.add(P["id"])
    key = [e for e in v["expected"] if e["role"] == "key"][0]
    if P["mode"] == "findK":
        x = P["prod_eq"] / P["coef"][[i for i, s in enumerate(P["side"]) if s > 0][0]]
        K = mass_action(P, x); check(abs(K - key["value"]) <= 1e-4 * K, f"{P['id']}: K {key['value']} vs independent {K:.5g}")
    else:
        x = x_by_bisection(P); asked = [i for i, s in enumerate(P["side"]) if s > 0][0]
        val = P["init_M"][asked] + P["coef"][asked] * x
        check(abs(val - key["value"]) <= 1e-4 * val, f"{P['id']}: [{P['species'][asked]}] {key['value']} vs independent {val:.5g}")
        check(key["unit"] == "M" and key["require_unit"], f"{P['id']}: the concentration key requires its unit")
    check(not engine.validate(dict(v, expected=list(v["expected"]))), f"{P['id']}: validates")
    # the table: E = I + C at a trial x, every column
    T = v["table"]
    for j in range(len(T["species"])):
        check(abs(ev(T["rows"]["E"][j], 0.3) - (ev(T["rows"]["I"][j], 0.3) + ev(T["rows"]["C"][j], 0.3))) < 1e-9, f"{P['id']}: column {T['species'][j]} E = I + C")
    # the schema: branch items exist, options have exactly the right answers declared, stages come from the moves file
    ids = {b["id"] for b in v["board"]}
    for b in v["board"]:
        for opt, items in (b["branch"] or {}).items(): check(set(items) <= ids, f"{P['id']}: branch names unknown items")
        if b["kind"] in ("pick", "direction") and b.get("options"): check(set(b["right"]) <= {o["id"] for o in b["options"]}, f"{P['id']}: {b['id']} right answers are options")
        check(b["stage"] == moves[b["id"]]["stage"], f"{P['id']}: {b['id']} stage from the moves file")
    check(all("dim" in e for e in v["expected"]), f"{P['id']}: every number carries dim")
    check(any(t["id"] == "EXCEEDS_INITIAL" and "above" in t for t in v["traps"]), f"{P['id']}: conservation bound declared")
check(seen == {f["id"] for f in A.FIXED}, "every fixed problem is attached to at least one opener")
same = engine.build(A, 1, 1, openers, moves)["content_version"] == out["content_version"]
print(f"{len(out['variants'])} fixed variants | {'all checks pass' if not fails else str(fails) + ' failed'} | same seed same output: {same}")
sys.exit(1 if fails else 0)
