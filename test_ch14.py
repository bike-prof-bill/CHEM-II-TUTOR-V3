"""Independent checks on the four chapter 14 archetypes: every placeholder's numbers re-derived by separate arithmetic (OpenStax
worked examples: 0.10 M acetic acid pH 2.87; the 25.00 mL / 0.100 M titration at 2.87, 4.74, 8.72, 12.30), the method and region
picks, the perturbation answers, named picks never the right answer, traps clear of their steps, constants sourced, nothing shipping."""
import sys, json, math; sys.path.insert(0, "archetypes"); import engine
import ch14_ph as PH, ch14_acidbase as AB, ch14_buffer as BU, ch14_titration as TI
fails = 0
def check(c, m):
    global fails
    if not c: fails += 1; print("  FAIL:", m)
near = lambda a, b, r=0.01: abs(a - b) <= r * max(abs(b), 1e-12)
def build(A):
    m = engine.read_moves(f"content_{A.ID}_moves.csv"); e = engine.read_errors(f"content_{A.ID}_errors.csv")
    check(engine.build(A, 1, 1, engine.read_openers(f"content_{A.ID}_openers.csv"), m, e)["variants"] == [], f"{A.ID}: no scenario row, nothing ships")
    out = engine.build(A, 1, 1, engine.read_openers(f"tests/fixtures/content_{A.ID}_openers_allkinds.csv"), m, e)
    V = {v["fixed_id"]: v for v in out["variants"]}; check(all(v["status"].startswith("DRAFT") for v in V.values()), f"{A.ID}: every placeholder DRAFT")
    for v in V.values():
        for b in v["board"]:
            if b["kind"] in ("direction", "pick") and "options" in b:
                for o in b["options"]:
                    if o.get("names"): check(o["id"] not in b["right"], f"{v['fixed_id']} {b['id']}: named option {o['id']} is wrong")
        for t in v["traps"]:
            if "value" in t:
                for e in v["expected"]:
                    if e["state"] == t["state"]: check(abs(t["value"] - e["value"]) > 2 * max(t["abs_tol"], e["abs_tol"]), f"{v['fixed_id']}: trap {t['id']} clear of {e['label']}")
    return V
ex = lambda V, fid, st: [e for e in V[fid]["expected"] if e["state"] == st][0]["value"]
right = lambda V, fid, st: [b for b in V[fid]["board"] if b["id"] == st][0]["right"]
# 1. pH & pOH and 2. Acids & Bases: every problem against SCENARIO_CLAUDE's sheets (approved 15-16 Oct)
def item(exp, key):
    m = re.search(r"(?:^|\| )" + re.escape(key) + r"[^:|]*: ([^|]+)", exp); return m.group(1).strip() if m else None
def num(s):
    m = re.search(r"-?[0-9.]+(?:e-?\d+)?", s.replace("× 10⁻", "e-").replace("× 10", "e")); return float(m.group(0))
sheets_ph = ["docs/handoff_examples/ch14_ph_problems_off_the_scale.csv", "docs/handoff_examples/ch14_ph_problems_corn_soak_stockroom_concrete.csv"]
sheets_ab = ["docs/handoff_examples/ch14_acidbase_problems_same_label.csv", "docs/handoff_examples/ch14_acidbase_problems_fishy_bowl.csv"]
def shipped(A):
    m = engine.read_moves(f"content_{A.ID}_moves.csv"); e = engine.read_errors(f"content_{A.ID}_errors.csv")
    out = engine.build(A, 1, 1, engine.read_openers(f"content_{A.ID}_openers.csv"), m, e); return out, {v["fixed_id"]: v for v in out["variants"]}
import csv, re
out, V = shipped(PH); check(len(V) == 36 and len(out["openers"]) == 4 and all(not v["status"].startswith("DRAFT") for v in V.values()), "ph: 36 problems under 4 scenarios ship, none DRAFT")
roles = {o["title"]: o.get("role") for o in out["openers"]}; check(roles.get("The Corn Soak") == "worked" and roles.get("Concrete Burn") == "exam", "ph: roles as the README says")
for f in sheets_ph:
    for row in csv.DictReader(open(f, encoding="utf-8-sig")):
        v = V[row["id"]]; exp = row["expected, item by item"]; tr = row["givens and trap values"]
        check(near(ex(V, row["id"], "ion_found"), num(item(exp, "ion_found")), 0.02) and abs(ex(V, row["id"], "pH_found") - num(item(exp, "pH_found"))) <= 0.006 and abs(ex(V, row["id"], "pOH_found") - num(item(exp, "pOH_found"))) <= 0.006, f"{row['id']}: ion, pH, pOH as the sheet")
        want = item(exp, "perturb_1").split()[0]; b = [x for x in v["board"] if x["id"] == "perturb_1"][0]
        check(b["right"] == ["p1:" + want] and any(o.get("names") == "DILUTION_AWAY_FROM_7" for o in b["options"] if o["id"] != b["right"][0]), f"{row['id']}: dilution {want}; the other direction named")
        tids = {t["id"] for t in v["traps"]}
        for tid in ("PH_SIGN_DROPPED", "POH_SIGN_DROPPED", "LN_FOR_LOG", "MOLES_NOT_CONCENTRATION"):
            if tid in tr: check(tid in tids, f"{row['id']}: {tid} named as the sheet lists")
        if "IONS_PER_FORMULA_IGNORED" in tr and "detectable only" not in tr.split("IONS_PER_FORMULA_IGNORED")[1].split("|")[0]: check("IONS_PER_FORMULA_IGNORED" in tids, f"{row['id']}: IONS_PER_FORMULA_IGNORED named")
        if "LN_FOR_LOG" in tr:
            want_ln = num(tr.split("LN_FOR_LOG")[1].split(":")[1].split("|")[0]); got = [t["value"] for t in v["traps"] if t["id"] == "LN_FOR_LOG"]
            check(got and abs(got[0] - want_ln) <= 0.02, f"{row['id']}: LN_FOR_LOG value {want_ln} (got {got})")
check(V["W1"]["version"] == "one_hydroxide" and V["W2"]["version"] == "two_hydroxides", "the Corn Soak's two versions")
out, V = shipped(AB); check(len(V) == 12 and len(out["openers"]) == 2 and all(not v["status"].startswith("DRAFT") for v in V.values()), "acidbase: 12 problems under 2 scenarios ship")
for f in sheets_ab:
    for row in csv.DictReader(open(f, encoding="utf-8-sig")):
        v = V[row["id"]]; exp = row["expected, item by item"]
        check(near(ex(V, row["id"], "x_found"), num(item(exp, "x_found")), 0.02) and abs(ex(V, row["id"], "pH_found") - num(item(exp, "pH_found"))) <= 0.006 and near(ex(V, row["id"], "percent_found"), num(item(exp, "percent_found")), 0.05), f"{row['id']}: x, pH, percent as the sheet")
        if item(exp, "pOH_found"): check(abs(ex(V, row["id"], "pOH_found") - num(item(exp, "pOH_found"))) <= 0.006, f"{row['id']}: pOH as the sheet")
        check(right(V, row["id"], "method") == ["method:" + item(exp, "method")] and right(V, row["id"], "approx_checked") == ["approx:" + item(exp, "approx_checked")], f"{row['id']}: method and the 5 % check as the sheet")
check(V["K1"]["version"] == "holds" and V["K2"]["version"] == "fails" and all(V[f"X{i}"]["context"]["approx_ok"] for i in range(1, 7)), "Same Label's two versions; every Fishy Bowl problem holds the rule (instructor's exception)")
D = json.load(open("archetypes/data/acids_bases.json", encoding="utf-8"))
check(D["acids"]["hydrofluoric"]["Ka"] == 6.4e-4 and D["acids"]["nitrous"]["Ka"] == 4.6e-4 and "Ca(OH)2" in D["strong"] and "formic" in D["acids"] and "trimethylamine" in D["bases"], "the appendix corrections and additions are in")
# 3. Buffers (the pH after a small addition, the instructor's floor 0.75 mL)
V = build(BU); check(len(V) == 2, "buffer: two placeholders")
pKa = -math.log10(1.8e-5)
check(near(ex(V, "F1", "pH_found"), pKa) and near(ex(V, "F1", "pH_after_1"), pKa + math.log10(0.11 / 0.09)) and near(ex(V, "F1", "pH_after_2"), pKa + math.log10(0.09 / 0.11)), "F1: pKa 4.74; 0.010 mol base -> 4.83; 0.010 mol acid -> 4.66")
check(near(ex(V, "F2", "pH_found"), pKa + math.log10(2.5)) and near(ex(V, "F2", "pH_after_1"), pKa + math.log10(0.27 / 0.08)) and near(ex(V, "F2", "pH_after_2"), pKa + math.log10(0.23 / 0.12)), "F2: 5.14; 0.020 mol base -> 5.27; acid -> 5.03")
check(right(V, "F1", "perturb_1") == ["p1:rises"] and right(V, "F1", "perturb_2") == ["p2:falls"] and any(t["id"] == "ADDED_NOT_CONSUMED" and near(t["value"], 14 + math.log10(0.010 / 1.010)) for t in V["F1"]["traps"]), "a little base: rises; acid: falls; the added base left free is named")
check(all(a["mL"] > BU.MIN_ADD_ML for v in V.values() for a in v["context"]["additions"]), "every addition is above 0.75 mL")
# 4. Titration (OpenStax Example 14.21 numbers)
V = build(TI); check(len(V) == 7, "titration: seven placeholders")
check([V[f]["kind"] for f in ("T0", "T1", "T2", "T3")] == ["weak_start", "weak_before", "weak_at", "weak_after"] and [right(V, f, "region_chosen")[0] for f in ("U1", "U2", "U3")] == ["region:before", "region:at", "region:after"], "regions from the moles")
check(near(ex(V, "T0", "pH_found"), 2.875, 0.002) and near(ex(V, "T1", "pH_found"), pKa) and near(ex(V, "T2", "pH_found"), 8.72, 0.002) and near(ex(V, "T3", "pH_found"), 12.30, 0.002), "T0 2.87, T1 4.74 (halfway), T2 8.72, T3 12.30")
check(near(ex(V, "T2", "Kb_found"), 1e-14 / 1.8e-5) and near(ex(V, "T2", "conc_found"), 0.0025 / 0.050) and near(ex(V, "T3", "excess_conc"), 0.00125 / 0.0625), "T2: Kb = Kw/Ka, 0.050 M conjugate in 50.00 mL; T3: 0.020 M excess OH- in 62.50 mL")
check(near(ex(V, "U1", "pH_found"), -math.log10(0.00125 / 0.0375)) and ex(V, "U2", "pH_found") == 7.0 and near(ex(V, "U3", "pH_found"), 12.30, 0.002), "U1 1.48, U2 7.00, U3 12.30")
check(any(t["id"] == "PH_7_AT_EQUIVALENCE" for t in V["T2"]["traps"]) and any(t["id"] == "KA_FOR_HYDROLYSIS" for t in V["T2"]["traps"]) and not any(t["id"] == "VOLUME_NOT_TOTALED" for t in V["T2"]["traps"]), "T2: pH 7 and Ka-for-Kb are named; the untotaled volume gives 0.100 M, the given, so it is dropped (SCENARIO_CLAUDE: avoid equal concentrations if that error should be caught)")
rel = {f: [b for b in V[f]["board"] if b["id"] == "relation_chosen"] for f in V}
check(all(rel[f] for f in V) and all(e["role"] == "intermediate" for e in V["T1"]["expected"] if e["state"] == "moles_found"), "every titration problem picks a relation; the moles are both required")
D = json.load(open("archetypes/data/acids_bases.json", encoding="utf-8"))
check(all(a.get("source") for a in list(D["acids"].values()) + list(D["bases"].values())) and D["Kw"].get("source"), "every Ka, Kb and Kw has a source line")
print("ch14 (four archetypes): all checks pass" if not fails else f"ch14: {fails} FAILED"); sys.exit(1 if fails else 0)
