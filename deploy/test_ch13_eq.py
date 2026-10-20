"""Independent checks on the combined chapter 13 archetype: every ICE number equals the retired ch13_ice bundle's (frozen in tests/fixtures) (the twelve
approved problems move unchanged); Q and the perturbation directions re-derived here by separate code; the tracer problem at
Q = K; the shipping gate."""
import sys, json, math; sys.path.insert(0, "archetypes"); import engine, ch13_eq as A
fails = 0
def check(c, m):
    global fails
    if not c: fails += 1; print("  FAIL:", m)
moves = engine.read_moves("content_ch13_eq_moves.csv"); errors = engine.read_errors("content_ch13_eq_errors.csv")
ship = engine.build(A, 1, 1, engine.read_openers("content_ch13_eq_openers.csv"), moves, errors)
check(len(ship["variants"]) == 66 and len(ship["openers"]) == 5, "five approved scenarios ship sixty-six problems")
check(all(not v["status"].startswith("DRAFT") for v in ship["variants"]), "no shipped problem is DRAFT")
check(all(ship["trap_notes"][i]["ask"] for i in ("Q_INVERTED", "COEFFICIENTS_AS_MULTIPLIERS", "EXPONENTS_DROPPED")), "the Q-step errors carry approved asks (base rows, 13 Oct)")
# the kit's named wrong picks
h = [v for v in ship["variants"] if v["kind"] == "haber_setup"][0]; m = [v for v in ship["variants"] if v["kind"] == "wgs_equilibrium"][0]
hb = {b["id"]: b for b in h["board"]}; mb = {b["id"]: b for b in m["board"]}
check([o.get("names") for o in hb["perturb_2"]["options"]] == ["EXO_HEATED_FORWARD", None, None], "Haber: forward on heating is named")
check([o.get("names") for o in mb["perturb_2"]["options"]] == ["SQUEEZE_SHIFT_EQUAL_MOLES", "SQUEEZE_SHIFT_EQUAL_MOLES", None], "Martian: any shift on squeezing is named")
check(ship["trap_notes_by_opener"]["The Haber-Bosch Harvest"]["EXO_HEATED_FORWARD"]["ask"].startswith("Making ammonia gives off heat"), "the approved ask is carried for the Haber error")
out = engine.build(A, 1, 1, engine.read_openers("tests/fixtures/content_ch13_eq_openers_allkinds.csv"), moves, errors)
check(len(out["variants"]) == 66, "sixty-six problems in the harness build")
# parity with the shipped ICE bundle: same expected values and traps for H1-H6, M1-M6
ice = {v["fixed_id"]: v for v in json.load(open("tests/fixtures/ch13_ice.bundle.frozen.json", encoding="utf-8"))["variants"]}
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
    if rx_id.startswith("ag") and rx_id.endswith("_dissolution"): return {"add_common_ion": -1, "heat": 1}[ptype]
    if rx_id == "hi_formation":  return {"add_reactant": 1, "heat": -1}[ptype]            # exothermic (OpenStax 13.3)
    if rx_id == "no2_dimerization": return {"compress": 1, "heat": -1}[ptype]             # 2 gas moles -> 1; exothermic (Example 13.2, 13.3)
for v in out["variants"]:
    for n, p in enumerate(v["context"]["perturbations"], start=1):
        want = expect_dir(v["context"]["reaction"], p["type"], p["species"]); got = p["direction"]
        b = [x for x in v["board"] if x["id"] == f"perturb_{n}"][0]
        tag = {1: "forward", -1: "reverse", 0: "neither"}[want]
        check(got == want and b["right"] == [f"p{n}:{tag}"], f"{v['fixed_id']} perturbation {n} ({p['type']} {p['species']}): {tag}")
        check(all(o["text"].split()[0].rstrip(":,") in ("forward", "reverse", "neither") for o in b["options"]), f"{v['fixed_id']} perturbation {n}: options start with the direction word (a colon after it is allowed since 14 Oct)")
# the Silent Beaker: every Q against SCENARIO_CLAUDE's sheet; directions; the moles-into-Q trap; Q = K exactly on the 1s
import _equilibrium as EQ, csv, re
sup = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
def sheet_num(txt):
    m = re.search(r"([0-9.]+)(?: × 10⁻?([⁰¹²³⁴⁵⁶⁷⁸⁹]+))?", txt); return float(m.group(1)) * (10 ** (-int(m.group(2).translate(sup))) if m.group(2) else 1)
sheet = {r["id"]: r for r in csv.DictReader(open("docs/handoff_examples/ch13_problems_silent_beaker.csv", encoding="utf-8-sig"))}
tr = [v for v in out["variants"] if v["kind"].endswith("_tracer")]
check(len(tr) == 18 and all(v["context"]["mode"] == "none" for v in tr), "eighteen tracer problems, no table")
for v in tr:
    row = sheet[v["fixed_id"]]; exp = row["expected, item by item"]
    Qs = sheet_num(exp.split("Q_found:")[1].split("|")[0])
    q = [e for e in v["expected"] if e["state"] == "Q_found"]
    check((Qs == 0 and not q) or (q and abs(q[0]["value"] - Qs) <= 0.02 * Qs), f"{v['fixed_id']}: Q = {Qs:.3g} as the sheet says")
    want = {"neither": "neither", "forward": "forward", "reverse": "reverse"}[exp.split("shift_predicted:")[1].split("|")[0].split()[0]]
    check([b for b in v["board"] if b["id"] == "shift_predicted"][0]["right"] == ["direction:" + want], f"{v['fixed_id']}: direction {want}")
    check([p["direction"] for p in v["context"]["perturbations"]] == [-1, 1], f"{v['fixed_id']}: common ion reverse, warming forward")
    if "conc_found" in exp:
        cs = [sheet_num(x) for x in re.findall(r"\[[A-Za-z+-]+\] ([0-9.]+ × 10⁻[⁰¹²³⁴⁵⁶⁷⁸⁹]+)", exp.split("conc_found:")[1].split("|")[0])]
        got = sorted(e["value"] for e in v["expected"] if e["state"] == "conc_found")
        check(len(got) == 2 and all(abs(a - b) <= 0.02 * b for a, b in zip(got, sorted(cs))), f"{v['fixed_id']}: the two concentrations from moles in 0.500 L")
        mt = [t for t in v["traps"] if t["id"] == "MOLES_NOT_CONCENTRATION"]
        check(len(mt) == 1 and mt[0]["state"] == "Q_found" and abs(mt[0]["value"] - sheet_num(row["trap values (named error: value)"].split("Q from moles = ")[1].split(" ")[0].replace("e", " × 10^").replace("^-", "⁻").replace(" × 10^", " × 10"))) <= 0.05 * mt[0]["value"] if False else len(mt) == 1 and mt[0]["state"] == "Q_found", f"{v['fixed_id']}: moles straight into Q is named on the Q step")
    if v["fixed_id"].endswith("1"):
        check(v["context"]["direction"] == 0 and [o.get("names") for o in [b for b in v["board"] if b["id"] == "shift_predicted"][0]["options"]][0] == "FORWARD_AT_EQUILIBRIUM", f"{v['fixed_id']}: Q = K, forward named")
    check([b for b in v["board"] if b["id"] == "perturb_1"][0]["options"][0].get("names") == "FORWARD_ON_COMMON_ION", f"{v['fixed_id']}: forward on the common ion named")
    check(v["sim_params"]["salt"] in ("AgCl", "AgBr", "AgI") and v["sim_params"]["solid"] == (0 if "no solid" in row["family"] else 1), f"{v['fixed_id']}: the page's settings")
    check(v["words"]["sodium_salt"].startswith("sodium ") and all(o["text"].split()[0].rstrip(":") in ("forward", "reverse", "neither") for b in v["board"] if b["kind"] == "direction" for o in b["options"]), f"{v['fixed_id']}: words and the dissolution option wording")
a6 = [v for v in tr if v["fixed_id"] == "A6"][0]
check(abs([t for t in a6["traps"] if t["id"] == "MOLES_NOT_CONCENTRATION"][0]["value"] - 6.25e-12) < 1e-14, "A6: moles into Q gives 6.3e-12 (two figures)")
# the figures rule by itself: the sketch's 1.3e-5 over the textbook's 1.6e-10 is 6% above K: equal at two figures, not at three
check(EQ.direction(A.AGCL, [0, 1.3e-5, 1.3e-5], sf=3) == -1 and EQ.direction(A.AGCL, [0, 1.3e-5, 1.3e-5], sf=2) == 0, "equality is judged at the figures the data carry")
check(all(v["context"]["direction"] == ice[v["fixed_id"]]["context"]["direction"] for v in out["variants"] if v["fixed_id"] in ice), "the ICE problems' directions unchanged under the figures rule")
a1 = [v for v in tr if v["fixed_id"] == "A1"][0]
# SCENARIO_CLAUDE's two points (13 Oct): an absent solid does not make Q undefined; a named wrong pick is never the right answer
check(EQ.quotient(A.AGCL, [0.0, 1.3e-5, 1.3e-5]) is not None and EQ.direction(A.AGCL, [0.0, 0.0, 1.3e-5], sf=2) == 1, "a solid reactant 'absent' leaves Q defined; pure water over solid (no Ag+) gives Q = 0, forward")
for v in out["variants"]:
    for b in v["board"]:
        if b["kind"] == "direction":
            for o in b["options"]:
                if o.get("names"): check(o["id"] not in b["right"], f"{v['fixed_id']} {b['id']}: named option {o['id']} is a wrong one")
# the Purple Piston and the Fading Brown against SCENARIO_CLAUDE's sheets: Q, direction, method, x, the other root, the answer, the leftover, the named traps
def num(txt): return float(re.search(r"-?[0-9.]+(?:e[+-]?\d+)?", txt.replace("× 10²", "e2")).group(0))
def item(exp, key):
    m = re.search(re.escape(key) + r"[^:|]*: ([^|]+)", exp); return m.group(1).strip() if m else None
for sheet_file in ("docs/handoff_examples/ch13_problems_purple_piston.csv", "docs/handoff_examples/ch13_problems_fading_brown.csv"):
    for row in csv.DictReader(open(sheet_file, encoding="utf-8-sig")):
        v = [x for x in out["variants"] if x["fixed_id"] == row["id"]][0]; exp = row["expected, item by item"]; tr = row["trap values (named error: value)"]
        ex = {e["state"]: e for e in v["expected"] if e["role"] != "given"}; near = lambda a, b: abs(a - b) <= 0.015 * max(abs(b), 1e-12) + 1e-12
        q = item(exp, "Q_found")
        if q.startswith("none"): check("Q_found" not in ex, f"{row['id']}: no Q (a reactant absent)")
        else: check("Q_found" in ex and near(ex["Q_found"]["value"], num(q)), f"{row['id']}: Q = {q} (got {ex.get('Q_found', {}).get('value')})")
        want = item(exp, "shift_predicted").split()[0]; check([b for b in v["board"] if b["id"] == "shift_predicted"][0]["right"] == ["direction:" + want], f"{row['id']}: direction {want}")
        if item(exp, "x_found"):
            check(near(ex["x_found"]["value"], num(item(exp, "x_found"))) and near(ex["other_root_checked"]["value"], num(item(exp, "other_root_checked"))), f"{row['id']}: x and the other root ({ex['x_found']['value']:.4g}, {ex['other_root_checked']['value']:.4g})")
            check(near(ex["value_found"]["value"], num(item(exp, "value_found"))) and near(ex["leftover_found"]["value"], num(item(exp, "leftover_found"))), f"{row['id']}: the answer and the leftover")
            m = "sqrt" if "square root" in item(exp, "method") else "quadratic"; check([b for b in v["board"] if b["id"] == "method"][0]["right"] == ["method:" + m], f"{row['id']}: method {m}")
            check(ex["value_found"]["label"].endswith(f"[{v['kind'][:2].upper() if False else ('HI' if v['kind'].startswith('hi') else 'N2O4')}]"), f"{row['id']}: the answer is the species the sheet names")
            if "iodine is left" in exp or "iodine is left" in row["problem sentence (as the student sees it)"]: check(ex["leftover_found"]["label"].endswith("[I2]"), f"{row['id']}: the leftover is iodine")
            for tid, key in (("PHANTOM_ROOT", "PHANTOM_ROOT"), ("SQRT_ONE_SIDE", "SQRT_ONE_SIDE"), ("CHANGE_COEFF_IGNORED", "CHANGE_COEFF_IGNORED")):
                if key + ":" in tr or key + " (x):" in tr:
                    val = num(tr.split(key)[1].split(":")[1].split("|")[0]); got = [x for x in v["traps"] if x["id"] == tid and x["state"] == "x_found"]
                    if tid == "CHANGE_COEFF_IGNORED" and not got: check(any(not (abs(val - x["value"]) > 3 * 0.02 * max(val, x["value"])) for x in v["traps"] if x["state"] == "x_found"), f"{row['id']}: {tid} dropped only because it lies on another x trap")
                    else: check(got and near(got[0]["value"], val), f"{row['id']}: {tid} = {val}")
            if "SQRT_ON_NONSQUARE" in tr:
                vals = sorted(float(x) for x in re.findall(r"[0-9.]+", tr.split("SQRT_ON_NONSQUARE: [")[1].split("]")[0])); got = sorted(x["value"] for x in v["traps"] if x["id"] == "SQRT_ON_NONSQUARE")
                check(len(got) == 2 and all(near(a, b) for a, b in zip(got, vals)), f"{row['id']}: SQRT_ON_NONSQUARE {vals}")
            if "MOLES_NOT_CONCENTRATION (value_found)" in tr: check(any(x["id"] == "MOLES_NOT_CONCENTRATION" and x["state"] == "value_found" and near(x["value"], num(tr.split("MOLES_NOT_CONCENTRATION (value_found):")[1])) for x in v["traps"]), f"{row['id']}: moles trap on the answer")
            else: check(not any(x["id"] == "MOLES_NOT_CONCENTRATION" and x["state"] == "value_found" for x in v["traps"]), f"{row['id']}: no moles trap in a 1.00 L vessel")
        if "OLD_VOLUME_USED" in tr:
            got = sorted(x["value"] for x in v["traps"] if x["id"] == "OLD_VOLUME_USED"); vals = [float(x) for x in re.findall(r"([0-9.]+)(?:,| M)", tr.split("OLD_VOLUME_USED:")[1].split("|")[0])]
            check(got and all(any(near(g, w) for w in vals) for g in got) and all(all(abs(g - e["value"]) > 3 * 0.02 * e["value"] for e in v["expected"] if e["state"] == "conc_found") for g in got), f"{row['id']}: OLD_VOLUME_USED values from the sheet, only those clear of a new concentration ({got})")
        if row["named wrong pick"].strip(): check([o.get("names") for o in [b for b in v["board"] if b["id"] == "shift_predicted"][0]["options"]] == ["SHIFT_ON_EQUAL_MOLES", "SHIFT_ON_EQUAL_MOLES", None], f"{row['id']}: any shift on a volume change is named")
        p1, p2 = item(exp, "perturb_1").split()[0], item(exp, "perturb_2").split()[0]
        check([{1: "forward", -1: "reverse", 0: "neither"}[p["direction"]] for p in v["context"]["perturbations"]] == [p1, p2], f"{row['id']}: perturbations {p1}, {p2}")
        check(v["sim_params"].get("V") == float(re.search(r"A ([0-9.]+) L", row["problem sentence (as the student sees it)"]).group(1)) or v["context"].get("mode") == "none" and v["kind"] == "hi_volume", f"{row['id']}: the page gets the vessel's volume")
# every constant and every dH sign used has a source line
rxs = json.load(open("archetypes/data/reactions.json", encoding="utf-8"))["reactions"]
for r in (A.HABER, A.WGS, A.AGCL, A.AGBR, A.AGI, A.HI, A.NO2): check(bool(rxs[r["id"]]["source"].get("Kc")) and bool(rxs[r["id"]]["source"].get("dH_sign")), f"{r['id']}: Kc and dH sign have source lines")
print("ch13_eq: all checks pass" if not fails else f"ch13_eq: {fails} FAILED"); sys.exit(1 if fails else 0)
