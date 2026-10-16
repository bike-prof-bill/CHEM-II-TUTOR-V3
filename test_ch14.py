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
# 1. pH & pOH
V = build(PH); check(len(V) == 3, "ph: three placeholders")
check(near(ex(V, "S1", "pH_found"), -math.log10(0.0025)) and near(ex(V, "S2", "pH_found"), 12.0) and near(ex(V, "S3", "ion_found"), 0.010) and near(ex(V, "S3", "pH_found"), 12.0), "S1 2.60; S2 12.00; S3: two hydroxides per formula, [OH-] 0.010 M, pH 12.00")
check(right(V, "S1", "perturb_1") == ["p1:rises"] and right(V, "S2", "perturb_1") == ["p1:falls"], "dilution raises an acid's pH, lowers a base's")
check(not any(t["id"] == "IONS_PER_FORMULA_IGNORED" for t in V["S3"]["traps"]) and [e["abs_tol"] for e in V["S1"]["expected"] if e["state"] == "pH_found"] == [0.03], "the dihydroxide's 'formula concentration as [OH-]' equals the given, so the engine drops it as undetectable (a restated given); pH read to two decimals")
# 2. Acids & Bases
V = build(AB); check(len(V) == 5, "acidbase: five placeholders")
x = (-1.8e-5 + math.sqrt(1.8e-5 ** 2 + 4 * 1.8e-5 * 0.10)) / 2
check(near(ex(V, "W1", "x_found"), x) and near(ex(V, "W1", "pH_found"), -math.log10(x)) and near(ex(V, "W1", "percent_found"), 100 * x / 0.10), "W1: x, pH 2.87, 1.3 %")
check(right(V, "W1", "method") == ["method:smallx"] and right(V, "W1", "approx_checked") == ["approx:holds"] and right(V, "W2", "method") == ["method:quadratic"] and right(V, "W2", "approx_checked") == ["approx:fails"], "small-x where the 5 % rule holds, the quadratic where it fails")
x2 = (-4.5e-4 + math.sqrt(4.5e-4 ** 2 + 4 * 4.5e-4 * 0.0050)) / 2
check(near(ex(V, "W2", "x_found"), x2) and ex(V, "W2", "percent_found") > 5 and any(t["id"] == "SMALL_X_WHEN_IT_FAILS" and near(t["value"], math.sqrt(4.5e-4 * 0.0050)) for t in V["W2"]["traps"]), "W2: the quadratic x, the small-x value named")
xb = (-1.8e-5 + math.sqrt(1.8e-5 ** 2 + 4 * 1.8e-5 * 0.25)) / 2
check(near(ex(V, "B1", "pOH_found"), -math.log10(xb)) and near(ex(V, "B1", "pH_found"), 14 + math.log10(xb)) and right(V, "B2", "method") == ["method:quadratic"], "B1 pOH 2.67, pH 11.33; B2 methylamine 0.010 M needs the quadratic")
check(right(V, "W1", "perturb_1") == ["p1:rises"] and right(V, "W1", "perturb_2") == ["p2:rises"] and right(V, "B1", "perturb_2") == ["p2:falls"], "dilution raises percent ionised; conjugate base raises an acid's pH; conjugate acid lowers a base's")
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
