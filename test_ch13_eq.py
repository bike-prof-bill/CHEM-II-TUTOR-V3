"""Independent checks on the combined chapter 13 archetype: every ICE number equals the shipped ch13_ice bundle's (the twelve
approved problems move unchanged); Q and the perturbation directions re-derived here by separate code; the tracer problem at
Q = K; the shipping gate."""
import sys, json, math; sys.path.insert(0, "archetypes"); import engine, ch13_eq as A
fails = 0
def check(c, m):
    global fails
    if not c: fails += 1; print("  FAIL:", m)
moves = engine.read_moves("content_ch13_eq_moves.csv"); errors = engine.read_errors("content_ch13_eq_errors.csv")
check(engine.build(A, 1, 1, engine.read_openers("content_ch13_eq_openers.csv"), moves, errors)["variants"] == [], "no scenario row: nothing ships")
out = engine.build(A, 1, 1, engine.read_openers("tests/fixtures/content_ch13_eq_openers_allkinds.csv"), moves, errors)
check(len(out["variants"]) == 13, "thirteen problems in the harness build")
# parity with the shipped ICE bundle: same expected values and traps for H1-H6, M1-M6
ice = {v["fixed_id"]: v for v in json.load(open("output/ch13_ice.bundle.json", encoding="utf-8"))["variants"]}
for v in out["variants"]:
    if v["fixed_id"] not in ice: continue
    old = ice[v["fixed_id"]]
    ev_new = {(e["state"], e["label"]): e["value"] for e in v["expected"] if e["role"] != "given"}
    ev_old = {(e["state"], e["label"]): e["value"] for e in old["expected"] if e["role"] != "given"}
    check(ev_new == ev_old, f"{v['fixed_id']}: declared numbers unchanged from ch13_ice ({set(ev_new.items()) ^ set(ev_old.items())})")
    tr_new = sorted((t["id"], t["state"], t.get("value", t.get("above"))) for t in v["traps"] if t["state"] != "Q_found")
    tr_old = sorted((t["id"], t["state"], t.get("value", t.get("above"))) for t in old["traps"])
    check(tr_new == tr_old, f"{v['fixed_id']}: ICE traps unchanged ({set(tr_new) ^ set(tr_old)})")
    check(v["table"] == old["table"] and v["eq_checks"][0]["true"] == old["eq_checks"][0]["true"], f"{v['fixed_id']}: table and expression check unchanged")
    old_ids = [b["id"] for b in old["board"]]; new_ids = [b["id"] for b in v["board"]]
    kept = [i for i in new_ids if i in old_ids]
    check(kept == [i for i in old_ids if i != "approach"], f"{v['fixed_id']}: the ICE steps kept in order (approach dropped: Q comes first now)")
    check(new_ids[-6:] == ["perturb_1", "perturb_1_why", "perturb_2", "perturb_2_why", "meaning_given", "reflection"], f"{v['fixed_id']}: two perturbations before the meaning and the reflection")
# perturbation directions by separate reasoning
def expect_dir(rx_id, ptype, species):
    if rx_id == "haber_ammonia": return {("remove_product", "NH3"): 1, ("heat", None): -1}[(ptype, species)]
    if rx_id == "wgs":           return {("add_reactant", "H2O"): 1, ("compress", None): 0}[(ptype, species)]
    if rx_id == "agcl_dissolution": return {("add_common_ion", "Cl-"): -1, ("heat", None): 1}[(ptype, species)]
for v in out["variants"]:
    for n, p in enumerate(v["context"]["perturbations"], start=1):
        want = expect_dir(v["context"]["reaction"], p["type"], p["species"]); got = p["direction"]
        b = [x for x in v["board"] if x["id"] == f"perturb_{n}"][0]
        tag = {1: "forward", -1: "reverse", 0: "neither"}[want]
        check(got == want and b["right"] == [f"p{n}:{tag}"], f"{v['fixed_id']} perturbation {n} ({p['type']} {p['species']}): {tag}")
        check(all(o["text"].split()[0] in ("forward", "reverse", "neither") for o in b["options"]), f"{v['fixed_id']} perturbation {n}: options start with a bare word")
# the tracer problem: the sketch's own numbers; Q = K to the figures given (two); no shift; no ICE work; pure solid left out
import _equilibrium as EQ
a1 = [v for v in out["variants"] if v["fixed_id"] == "A1"][0]
Q = 1.3e-5 * 1.3e-5
q = [e for e in a1["expected"] if e["state"] == "Q_found"][0]
check(abs(q["value"] - Q) < 1e-15, "A1: Q = [Ag+][Cl-] = 1.7e-10, the sketch's numbers as written")
check(abs(Q - 1.8e-10) > 0.05 * 1.8e-10 and a1["context"]["direction"] == 0, "A1: Q sits 6% below K yet counts as equal to two figures (half a unit in each last place, propagated)")
check(abs(1.7e-10 - q["value"]) <= q["abs_tol"] and abs(1.8e-10 - q["value"]) > q["abs_tol"], "A1: a student's 1.7e-10 is accepted as Q; K's 1.8e-10 typed as Q is not")
check([b for b in a1["board"] if b["id"] == "shift_predicted"][0]["right"] == ["direction:neither"], "A1: no shift")
check(not any(b["id"] in ("table", "expression_set", "method", "x_found") for b in a1["board"]), "A1: no ICE chain")
check("c_AgCl" not in a1["givens"], "A1: the solid has no concentration")
# the figures rule by itself: three-figure data would not call 1.69e-10 equal to 1.80e-10; two-figure data does
check(EQ.direction(A.AGCL, [0, 1.3e-5, 1.3e-5], sf=3) == 1 and EQ.direction(A.AGCL, [0, 1.3e-5, 1.3e-5], sf=2) == 0, "equality is judged at the figures the data carry")
check(all(v["context"]["direction"] == ice[v["fixed_id"]]["context"]["direction"] for v in out["variants"] if v["fixed_id"] in ice), "the ICE problems' directions unchanged under the figures rule")
# every constant and every dH sign used has a source line
rxs = json.load(open("archetypes/data/reactions.json", encoding="utf-8"))["reactions"]
for r in (A.HABER, A.WGS, A.AGCL): check(bool(rxs[r["id"]]["source"].get("Kc")) and bool(rxs[r["id"]]["source"].get("dH_sign")), f"{r['id']}: Kc and dH sign have source lines")
print("ch13_eq: all checks pass" if not fails else f"ch13_eq: {fails} FAILED"); sys.exit(1 if fails else 0)
