"""Chapter 11 (the pilot, The Salted Road): every expected value, trap value and instrument reading re-derived from the problem sentence
and OpenStax Appendix A, independently of the sheet. Also: the brief-32 fields are present (difficulty, companion of the same rank,
prediction, instrument window, gap question), the textbook anchors resolve, and the sample answers never reach the bundle."""
import json, re, sys, os, glob
sys.path.insert(0, "archetypes")
ATOMIC = {"Na": 22.99, "K": 39.10, "Mg": 24.31, "Ca": 40.08, "Cl": 35.45}   # OpenStax 2e, Appendix A (the sheet's constants cell)
KF = 1.86
def molar_mass(formula):
    f = formula.translate(str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")); tot = 0.0; ions = 0
    for el, n in re.findall(r"([A-Z][a-z]?)(\d*)", f): n = int(n or 1); tot += ATOMIC[el] * n; ions += n
    return tot, ions
def close(a, b, tol): return abs(a - b) <= tol
fails = []
def check(cond, msg):
    if not cond: fails.append(msg)
B = json.load(open("output/ch11_colligative.bundle.json"))
check("samples" not in B or not B.get("samples"), "sample answers are in the shipped bundle")
check("sample answers" not in open("gas/Archetype_ch11_colligative.gs", encoding="utf-8").read().lower(), "sample answers are in the .gs")
n_checks = 0
for V in B["variants"]:
    t = V["text"]; fid = V["fixed_id"]
    g = float(re.search(r"spreads ([0-9.]+) g", t).group(1)); kg = float(re.search(r"in ([0-9.]+) kg of meltwater", t).group(1))
    formula = re.search(r"\(([A-Z][A-Za-z₀-₉0-9]*)\)", t).group(1)
    M, i = molar_mass(formula)
    mol = g / M; m = mol / kg; dT = i * KF * m; Tf = -dT
    exp = {e["state"]: e for e in V["expected"] if e["state"]}
    for st, val in (("mol_found", mol), ("m_found", m), ("i_found", i), ("dT_found", dT), ("T_found", Tf)):
        e = exp[st]; n_checks += 1
        check(close(e["value"], val, max(e["abs_tol"], 0.006 * abs(val))), f"{fid} {st}: sheet {e['value']} vs derived {val:.4g}")
    check(exp["T_found"]["role"] == "key" and exp["dT_found"]["role"] == "intermediate", f"{fid}: the freezing point is the key")
    # the instrument: grams of this salt in this water for Tf = -10.0 °C
    ins = exp.get("sim_instrument"); n_checks += 1
    grams = (10.0 / (i * KF)) * kg * M
    check(ins is not None and close(ins["value"], grams, ins["abs_tol"] + 0.5) and ins["unit"] == "g", f"{fid} instrument: sheet {ins and ins['value']} vs derived {grams:.1f} g")
    board = {b["id"]: b for b in V["board"]}
    check(board["sim_predict"].get("opens_sim") and board["sim_predict"].get("sim_student") == {"T_student": "T_found", "pred": "sim_predict"}, f"{fid}: the prediction opens the page with the student's values")
    check(board["sim_instrument"]["requires"] == ["sim_predict"] and board["sim_gap"]["requires"] == ["sim_instrument"] and board["perturb_1"]["requires"] == ["sim_gap"], f"{fid}: step order around the page")
    check(all(b.get("stage") == b["id"] for b in V["board"]), f"{fid}: the ladder counts per step (stage = step)")
    check(V.get("precision_rule") is True, f"{fid}: the precision rule is declared")
    # traps re-derived
    tv = {(x["id"], x["state"]): x for x in V["traps"]}
    expected_traps = {("I_OMITTED", "i_found"): 1.0, ("I_OMITTED", "dT_found"): KF * m, ("SOLUTION_MASS", "m_found"): mol / (kg + g / 1000), ("GRAMS_FOR_MOLES", "m_found"): g / kg,
                      ("DT_SIGNED", "dT_found"): -dT}
    check(("FP_SIGN", "T_found") not in tv and any(x.startswith("RESTATEMENT:FP_SIGN") for x in V.get("traps_dropped", [])), f"{fid}: FP_SIGN (+ΔT at the freezing point) equals the lowering already on the board and is dropped as unreachable (11 Oct restatement rule); SCENARIO_CLAUDE to know")
    for k, val in expected_traps.items():
        n_checks += 1
        check(k in tv and close(tv[k]["value"], val, max(tv[k]["abs_tol"], 0.006 * abs(val))), f"{fid} trap {k}: {tv.get(k, {}).get('value')} vs derived {val:.4g}")
    for x in V["traps"]:   # every trap clear of the right value by three windows
        e = exp[x["state"]]; n_checks += 1
        check(abs(x["value"] - e["value"]) > 3 * max(x["abs_tol"], e["abs_tol"]), f"{fid} trap {x['id']} at {x['state']} too near the right value")
    named = {o["id"]: o.get("names") for b in V["board"] if b["kind"] == "direction" for o in b["options"]}
    check(named.get("sim_predict:rises") == "SIM_PREDICT_SALT" and named.get("perturb_1:unchanged") == "PERTURB_I_IGNORED", f"{fid}: named wrong picks")
    right = {b["id"]: b["right"] for b in V["board"] if b["kind"] == "direction"}
    other = "CaCl₂" if formula in ("NaCl", "KCl") else "NaCl"   # the sheet's change of salt: to a 3-ion salt from a 2-ion one, and back
    check(right["sim_predict"] == ["sim_predict:falls"], f"{fid}: twice the salt lowers the freezing point further")
    check(right["perturb_1"] == ["perturb_1:" + ("falls" if i == 2 else "rises")], f"{fid}: same moles of a {3 if i == 2 else 2}-ion salt -> {'falls' if i == 2 else 'rises'}")
    # brief 32 fields
    check(str(V.get("difficulty", "")).startswith("3"), f"{fid}: difficulty rank 3 (steps 4, conv 1)")
    comp = [c for c in B["variants"] if c["fixed_id"] == V.get("companion")]
    check(len(comp) == 1 and comp[0].get("difficulty") == V.get("difficulty") and comp[0]["fixed_id"] != fid, f"{fid}: companion {V.get('companion')} exists, same rank, not itself")
    check(V["sim_params"].get("salt") in ("NaCl", "KCl", "CaCl2", "MgCl2") and float(V["sim_params"]["salt_g"]) == g and float(V["sim_params"]["water_kg"]) == kg, f"{fid}: page parameters match the sentence")
    check(V["words"].get("gap_question", "").endswith("?") and V["words"].get("target") == "−10.0", f"{fid}: gap question and target carried in words")
    check(not re.search(r"\^", t), f"{fid}: a caret in student text")
# anchors and passages
moves = B["moves"]; anchored = [k for k, r in moves.items() if isinstance(r, dict) and r.get("openstax")]
check(len(anchored) == 10 and len(B["passages"]) == 10 and not B.get("passages_unresolved"), f"textbook anchors: {len(anchored)} anchored, {len(B['passages'])} resolved, unresolved {B.get('passages_unresolved')}")
for k, p in B["passages"].items():
    check(p["text"] and "grst" not in p["text"] and len(p["text"]) <= 2700, f"passage {k}: empty, ligature error or too long")
# the reader's wrong accounts and the two-list gate
op = B["openers"][0]
check(len(op["wrong_accounts"]) == 4 and all(a["repair"].endswith("?") for a in op["wrong_accounts"]), "four wrong accounts with repair questions")
check(len(op["keywords"]) >= 8 and len(op["mechanism"]) >= 10 and "freezing" not in op["keywords"] + op["mechanism"] and "lowers" not in op["keywords"] + op["mechanism"], "two keyword lists without 'freezing' or 'lowers'")
check(os.path.exists("output/ch11_colligative.samples.json"), "sample answers written beside the bundle for the simulated students")
print(f"ch11 (one archetype, {len(B['variants'])} problems; {n_checks} values re-derived): " + ("all checks pass" if not fails else f"{len(fails)} FAILED"))
for f in fails: print("  FAIL:", f)
sys.exit(1 if fails else 0)
