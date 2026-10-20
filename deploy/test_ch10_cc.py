"""Independent checks on the factory. Closed forms are written separately from the engine's solver."""
import sys, math, time; sys.path.insert(0, "archetypes"); import engine, ch10_cc as A
R = 8.314; t0 = time.time(); out = engine.build(A, 100, 5000); dt = time.time() - t0; fails = 0
for name, dH, bp, cold, mp in A.SUBSTANCES:
    if not (cold > mp): fails += 1; print(f'  FAIL: {name}: coldest problem temperature {cold} °C is not above its melting point {mp} °C')
for v in out["variants"]:
    ok = "{" not in v["text"] and "true_substance" not in v["text"]
    for kt in [t for t in v["expected"] if t["role"] == "key"]:
        ok &= all(abs(tr["value"] - kt["value"]) > 3 * kt["abs_tol"] for tr in v["traps"] if tr["state"] == kt["state"])
    ok &= not engine.validate(v)                                   # Change 2: every shipped variant passes validation
    ok &= all("dim" in e and "role" in e and "id" in e for e in v["expected"])
    if v["kind"] != "slope":
        k = {n: engine.to_canon(A.VARIABLES[n]["kind"], s["unit"], s["value"]) for n, s in v["givens"].items()}; u = v["kind"]
        if   u == "P2": x = k["P1"] * math.exp(-(k["dH"]/R) * (1/k["T2"] - 1/k["T1"]))
        elif u == "P1": x = k["P2"] / math.exp(-(k["dH"]/R) * (1/k["T2"] - 1/k["T1"]))
        elif u == "T2": x = 1 / (1/k["T1"] - R*math.log(k["P2"]/k["P1"])/k["dH"])
        elif u == "T1": x = 1 / (1/k["T2"] + R*math.log(k["P2"]/k["P1"])/k["dH"])
        else:           x = -R * math.log(k["P2"]/k["P1"]) / (1/k["T2"] - 1/k["T1"])
        kt = [t for t in v["expected"] if t["role"] == "key"][0]
        ok &= abs(engine.from_canon(A.VARIABLES[u]["kind"], kt["unit"], x) - kt["value"]) <= 1e-4 * max(1, abs(kt["value"]))
    fails += (not ok)
n = len(out["variants"]); same = engine.build(A, 2, 7)["content_version"] == engine.build(A, 2, 7)["content_version"]
print(f"{n} variants in {dt:.2f}s | {n-fails}/{n} pass | thrown away: {engine.REJECTS} | same seed same output: {same}")

# The Syringe Boiling Trick (10 Oct): every problem keeps the known point at the normal boiling point and the other temperature
# inside the approved range for its liquid; the step map carries the prediction before the answer.
openers = engine.read_openers("content_ch10_cc_openers.csv"); moves = engine.read_moves("content_ch10_cc_moves.csv")
errors = engine.read_errors("content_ch10_cc_errors.csv"); limits = engine.read_limits("content_ch10_cc_limits.csv"); sentences = engine.read_sentences("content_ch10_cc_sentences.csv")
engine.REJECTS = {k: 0 for k in engine.REJECTS}
out2 = engine.build(A, 6, 7000, openers, moves, errors, limits, sentences)
syr = [v for v in out2["variants"] if openers[v["opener_index"]]["title"] == "The Syringe Boiling Trick"]
lim = limits["The Syringe Boiling Trick"]
for v in syr:
    g = v["givens"]; known = "P1" if v["kind"] == "P2" else "P2"; P = g[known]
    one_atm = (P["unit"] == "atm" and abs(P["value"] - 1) < 1e-9) or (P["unit"] == "torr" and abs(P["value"] - 760) < 0.5)
    if not one_atm: fails += 1; print(f"  FAIL: {v['variant_id']} known pressure is not one atmosphere: {P}")
    Tother = g["T2" if v["kind"] == "P2" else "T1"]; tC = Tother["value"] if Tother["unit"] == "degC" else Tother["value"] - 273.15
    L = lim[v["context"]["substance"]]
    if not (L["lo_C"] - 0.6 <= tC <= L["hi_C"] + 0.6): fails += 1; print(f"  FAIL: {v['variant_id']} other temperature {tC:.1f} °C outside [{L['lo_C']}, {L['hi_C']}] for {v['context']['substance']}")
    ids = [b["id"] for b in v["board"]]
    if ids.index("direction_predicted") > ids.index("value_found") or "reflection" not in ids: fails += 1; print(f"  FAIL: {v['variant_id']} step map order")
# per-scenario optional items (instructor, 10 Oct): a scenario may remove the prediction and the reflection
import random as _r
st, ctx = A.draw_state(_r.Random(5), ["ethanol"]); ctx["items"] = {"add": [], "remove": ["direction_predicted", "reflection"]}
ids = [b["state"] for b in A.board_for({"T1": {"value": 300, "unit": "K"}, "T2": {"value": 350, "unit": "K"}, "P1": {"value": 1, "unit": "atm"}, "dH": {"value": 40, "unit": "kJ/mol"}}, "P2", ctx)]
if "direction_predicted" in ids or "reflection" in ids: fails += 1; print("  FAIL: a scenario could not remove its optional items:", ids)
ids = [b["state"] for b in A.board_for({"T1": {"value": 300, "unit": "K"}, "T2": {"value": 350, "unit": "K"}, "P1": {"value": 1, "unit": "atm"}, "dH": {"value": 40, "unit": "kJ/mol"}}, "P2", {"items": {}})]
if "direction_predicted" not in ids or "reflection" not in ids: fails += 1; print("  FAIL: defaults lost:", ids)
bird = [v for v in out2["variants"] if openers[v["opener_index"]]["title"] == "The Drinking Bird"]
for v in bird:
    g = v["givens"]; kT, uT = ("T1", "T2") if v["kind"] == "P2" else ("T2", "T1"); c = lambda n: n["value"] if n["unit"] == "degC" else n["value"] - 273.15
    if not (19.9 <= c(g[kT]) <= 28.1): fails += 1; print(f"  FAIL: {v['variant_id']} body temperature {c(g[kT]):.1f} outside 20-28")
    if not (1.9 <= c(g[kT]) - c(g[uT]) <= 6.1): fails += 1; print(f"  FAIL: {v['variant_id']} head gap {c(g[kT]) - c(g[uT]):.1f} outside 2-6")
    if not any(e["state"] == "dP_found" and e.get("derive") for e in v["expected"]): fails += 1; print(f"  FAIL: {v['variant_id']} no derived difference")
print(f"bird: {len(bird)} problems keep the body at room temperature with a cooler head | {'ok' if not fails else 'FAIL'}")
vent = [v for v in out2["variants"] if openers[v["opener_index"]]["title"] == "The Deep-Sea Vent"]
for v in vent:
    d = v["givens"]["depth"]["value"]; kT = "T1" if v["kind"] == "T2" else "T2"
    if not (10 <= d <= 2000 and abs(d / 10 - round(d / 10)) < 1e-9): fails += 1; print(f"  FAIL: {v['variant_id']} depth {d} outside 10-2000 m in 10 m steps")
    if v["givens"][kT] != {"value": 100.0, "unit": "degC"}: fails += 1; print(f"  FAIL: {v['variant_id']} known point is not 100.0 °C: {v['givens'][kT]}")
    P = next(e for e in v["expected"] if e["state"] == "P_from_depth")
    if abs(P["value"] - (1 + d / 10)) > 1e-6 or P["unit"] != "atm": fails += 1; print(f"  FAIL: {v['variant_id']} pressure at the vent {P} vs 1 + {d}/10")
    key = next(e for e in v["expected"] if e["role"] == "key"); tC = key["value"] if key["unit"] == "degC" else key["value"] - 273.15
    if not (100 < tC < 374): fails += 1; print(f"  FAIL: {v['variant_id']} boiling temperature {tC:.1f} °C outside (100, 374)")
    if "P1" in v["givens"] and "P2" in v["givens"]: fails += 1; print(f"  FAIL: {v['variant_id']} the vent pressure is printed")
    if not any(t["id"] == "RECIPROCAL_NOT_TAKEN" for t in v["traps"]): fails += 1; print(f"  FAIL: {v['variant_id']} no reciprocal error")
    if next(b for b in v["board"] if b["id"] == "direction_predicted")["right"] != ["direction:higher"]: fails += 1; print(f"  FAIL: {v['variant_id']} prediction should be higher")
print(f"vent: {len(vent)} problems: depth in range, known point 100.0 °C at 1 atm, vent pressure 1 + depth/10 atm, boiling above 100 °C | {'ok' if not fails else 'FAIL'}")
print(f"syringe: {len(syr)} problems keep the known point at the boiling point and the other temperature in range | {'ok' if not fails else 'FAIL'}")
sys.exit(1 if fails else 0)
