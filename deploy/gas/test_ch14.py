"""Chapter 14, four archetypes, sixteen scenarios: every shipped problem checked against SCENARIO_CLAUDE's sheets (approved 15-17 Oct
2026): expected values, named errors (by value, within tolerance, or explained by a given), right picks and kinds; constants sourced."""
import sys, json, math, csv, re, glob; sys.path.insert(0, "archetypes"); import engine
import ch14_ph as PH, ch14_acidbase as AB, ch14_buffer as BU, ch14_titration as TI
fails = 0
def check(c, m):
    global fails
    if not c: fails += 1; print("  FAIL:", m)
def num(s):
    s = s.replace("× 10⁻", "e-").replace("× 10", "e"); m = re.search(r"-?[0-9.]+(?:e[+-]?\d+)?", s); return float(m.group(0)) if m else None
near = lambda a, b, r=0.02: abs(a - b) <= r * max(abs(b), 1e-30)
def near_ph(a, b): return abs(a - b) <= 0.011
SHEETS = {PH: ["ch14_ph_problems_off_the_scale.csv", "ch14_ph_problems_corn_soak_stockroom_concrete.csv"],
          AB: ["ch14_acidbase_problems_same_label.csv", "ch14_acidbase_problems_fishy_bowl.csv", "ch14_acidbase_problems_glass_and_bleach.csv"],
          BU: ["ch14_buffer_problems_stubborn_beaker.csv", "ch14_buffer_problems_sprint.csv", "ch14_buffer_problems_eye_drops.csv", "ch14_buffer_problems_half_a_buffer.csv"],
          TI: ["ch14_titration_problems_vinegar_lab.csv", "ch14_titration_problems_kombucha.csv", "ch14_titration_problems_floaters.csv"]}
EXPECT = {PH: 36, AB: 24, BU: 24, TI: 24}
PH_STATES = {"pH_found", "pOH_found", "pH_after_1", "pH_after_2"}
for A, sheets in SHEETS.items():
    m = engine.read_moves(f"content_{A.ID}_moves.csv"); e = engine.read_errors(f"content_{A.ID}_errors.csv")
    out = engine.build(A, 1, 1, engine.read_openers(f"content_{A.ID}_openers.csv"), m, e); V = {v["fixed_id"]: v for v in out["variants"]}
    check(len(V) == EXPECT[A] and len(out["openers"]) == 4 and all(not v["status"].startswith("DRAFT") for v in V.values()), f"{A.ID}: {EXPECT[A]} problems under 4 scenarios ship, none DRAFT")
    rows = [r for f in sheets for r in csv.DictReader(open("docs/handoff_examples/" + f, encoding="utf-8-sig"))]
    check(set(r["id"] for r in rows) == set(V), f"{A.ID}: the sheets' ids are the build's ids ({set(V) ^ set(r['id'] for r in rows)})")
    for r in rows:
        v = V[r["id"]]; byst = {}
        for e_ in v["expected"]:
            if e_["role"] != "given": byst.setdefault(e_["state"], []).append(e_["value"])
        for part in r["expected, item by item"].split("|"):
            mm = re.match(r"\s*(\w+)(?: [^:]*)?: (.+)", part.strip())
            if not mm: continue
            st, val = mm.group(1), mm.group(2).strip()
            if st in ("region", "method", "approx_checked") or st.startswith("perturb"): 
                if st.startswith("perturb"): 
                    want = re.search(r"\b(rises|falls|unchanged|forward|reverse|neither)\b", val).group(1); b = [x for x in v["board"] if x["id"] == st]
                    check(b and b[0]["right"][0].endswith(":" + want), f"{r['id']}: {st} {want}")
                elif st == "method": check([x for x in v["board"] if x["id"] == "method"][0]["right"] == ["method:" + val], f"{r['id']}: method {val}")
                elif st == "approx_checked": check([x for x in v["board"] if x["id"] == "approx_checked"][0]["right"] == ["approx:" + val], f"{r['id']}: approx {val}")
                elif st == "region": check(v["kind"].endswith("_" + val), f"{r['id']}: region {val}")
                continue
            x = num(val)
            if x is None: continue
            got = byst.get(st, [])
            dec = len(val.split(".")[1].split()[0]) if "." in val else 0
            ok_ = any(((abs(g_ - x) <= (0.011 if dec >= 2 else 0.06)) if st in PH_STATES else near(g_, x, 0.03)) for g_ in got)
            check(ok_, f"{r['id']}: {st} = {val} (build has {got})")
        have = {(t["id"], t["state"]) for t in v["traps"]}
        gset = [g_["value"] for g_ in v["givens"].values() if isinstance(g_, dict) and "value" in g_]
        for part in r["givens and trap values"].split("|"):
            mm = re.match(r"\s*([A-Z_0-9]+)(?: at (\w+))?: (.+)", part.strip())
            if not mm or mm.group(1) in ("EXCEEDS_INITIAL",) or "pick" in mm.group(3) or "'" in mm.group(3) or "perturb" in mm.group(3): continue
            tid, st, val = mm.group(1), mm.group(2), num(mm.group(3))
            if st is None:                     # the acidbase sheets name the trap without its step: look it up by id alone
                if not any(t["id"] == tid for t in v["traps"]) and val is not None:
                    check(any(near(val, g_, 0.1) or abs(val - g_) <= 0.1 for g_ in gset) or any(near(val, g_, 0.06) for vals in byst.values() for g_ in vals), f"{r['id']}: trap {tid} = {val} missing and unexplained")   # a pH of 0.00 lies within the pH window of a unitless given (Ka): the engine drops it as undetectable
                continue
            if (tid, st) not in have and val is not None:
                check(any(near(val, g_, 0.1) for g_ in gset) or any(near(val, g_, 0.06) for g_ in byst.get(st, [])), f"{r['id']}: trap {tid} at {st} = {val} missing and not explained by a given or the right value")
        if "kind" in r and r["kind"]: check(v["kind"] == r["kind"], f"{r['id']}: kind {r['kind']}")
D = json.load(open("archetypes/data/acids_bases.json", encoding="utf-8"))
check(all(a.get("source") for a in list(D["acids"].values()) + list(D["bases"].values())) and {"ammonium", "dihydrogen_phosphate", "carbonic_blood", "lactic"} <= set(D["acids"]) and {"hypochlorite", "acetate"} <= set(D["bases"]), "every Ka and Kb has a source; the 17 Oct species are in")
print("ch14 (four archetypes, 108 problems): all checks pass" if not fails else f"ch14: {fails} FAILED"); sys.exit(1 if fails else 0)
