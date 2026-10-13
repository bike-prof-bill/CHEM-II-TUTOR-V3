"""Independent checks on the Q versus K archetype: Q re-derived here from the problem data by separate code, the direction compared
with K, the named-error values recomputed, and the shipping gate: an archetype with no scenario row ships nothing."""
import sys, json; sys.path.insert(0, "archetypes"); import engine, ch13_q_vs_k as A
fails = 0
def check(c, m):
    global fails
    if not c: fails += 1; print("  FAIL:", m)
def q_of(rx, conc):
    top = 1.0; bottom = 1.0
    for i, s in enumerate(rx["side"]):
        if s > 0: top *= conc[i] ** rx["coef"][i]
        else: bottom *= conc[i] ** rx["coef"][i]
    return top / bottom
moves = engine.read_moves("content_ch13_q_vs_k_moves.csv"); errors = engine.read_errors("content_ch13_q_vs_k_errors.csv")
# the shipping gate: no opener row, no variant
shipped = engine.build(A, 1, 1, engine.read_openers("content_ch13_q_vs_k_openers.csv"), moves, errors)
check(shipped["variants"] == [], "no scenario row: nothing ships")
# the harness build: every placeholder, every number
fx = engine.read_openers("tests/fixtures/content_ch13_q_vs_k_openers_allkinds.csv")
out = engine.build(A, 1, 1, fx, moves, errors)
check(len(out["variants"]) == len(A.FIXED), f"{len(A.FIXED)} placeholder problems built")
for v in out["variants"]:
    P = [f for f in A.FIXED if f["id"] == v["fixed_id"]][0]; rx = P["rxn"]; conc = P["conc"]
    Q = q_of(rx, conc); right = "direction:forward" if Q < rx["K"] else ("direction:reverse" if Q > rx["K"] else "direction:neither")
    key = [e for e in v["expected"] if e["role"] == "key"]
    check(len(key) == 1 and abs(key[0]["value"] - Q) <= 1e-4 * max(1.0, Q), f"{P['id']}: Q = {Q:.4g} declared")
    sp = [b for b in v["board"] if b["id"] == "shift_predicted"][0]
    check(sp["right"] == [right] and sp["kind"] == "direction", f"{P['id']}: direction {right} checked against Q and K")
    check([b["id"] for b in v["board"]] == ["account_given", "relation_chosen", "Q_found", "shift_predicted", "meaning_given", "reflection"], f"{P['id']}: the six steps in order")
    check(key[0].get("after") == "relation_chosen", f"{P['id']}: Q is asked for by name after the expression")
    for t in v["traps"]:
        if t["id"] == "Q_INVERTED": check(abs(t["value"] - 1 / Q) <= 1e-3 * (1 / Q), f"{P['id']}: 1/Q trap")
        if t["id"] == "EXPONENTS_DROPPED":
            top = bottom = 1.0
            for i, s in enumerate(rx["side"]): (top := top * conc[i]) if s > 0 else (bottom := bottom * conc[i])
            check(abs(t["value"] - top / bottom) <= 1e-3 * (top / bottom), f"{P['id']}: exponents-dropped trap")
        check(abs(t["value"] - Q) > 3 * 0.02 * max(abs(t["value"]), abs(Q)), f"{P['id']}: trap {t['id']} is clearly not Q")
    check(v["status"].startswith("DRAFT"), f"{P['id']}: placeholder is marked DRAFT")
    check(rx["id"] not in ("haber_ammonia", "wgs"), f"{P['id']}: does not reuse the ICE scenarios' reactions")
# every constant has a source line in reactions.json
rxs = json.load(open("archetypes/data/reactions.json", encoding="utf-8"))["reactions"]
for r in (A.HI, A.N2O4, A.SO3, A.MEOH): check(bool(rxs[r["id"]]["source"].get("Kc")), f"{r['id']}: Kc has a source line")
print("ch13_q_vs_k: all checks pass" if not fails else f"ch13_q_vs_k: {fails} FAILED"); sys.exit(1 if fails else 0)
