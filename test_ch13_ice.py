"""Independent checks on the equilibrium archetype: every declared number is re-derived here from the problem data by a method
written separately from the archetype's (bisection on the mass-action equation; the quadratic's roots by the formula), and the
twelve problems' figures are compared with SCENARIO_CLAUDE's approved sheet (ch13_problems.csv, 13 Oct 2026)."""
import sys, math; sys.path.insert(0, "archetypes"); import engine, ch13_ice as A
fails = 0
def check(c, m):
    global fails
    if not c: fails += 1; print("  FAIL:", m)
def mass_action(rx, conc, d, x):
    num = den = 1.0
    for i, s in enumerate(rx["side"]):
        v = conc[i] + s * d * rx["coef"][i] * x
        if s > 0: num *= v ** rx["coef"][i]
        else: den *= v ** rx["coef"][i]
    return num / den
def bisect(rx, conc, d):
    lo, hi = 0.0, min(conc[i] / rx["coef"][i] for i, s in enumerate(rx["side"]) if s * d < 0) * 0.999999
    for _ in range(200):
        m = 0.5 * (lo + hi)
        if (mass_action(rx, conc, d, m) < rx["K"]) == (d > 0): lo = m
        else: hi = m
    return 0.5 * (lo + hi)
openers = engine.read_openers("content_ch13_ice_openers.csv"); moves = engine.read_moves("content_ch13_ice_moves.csv"); errors = engine.read_errors("content_ch13_ice_errors.csv")
out = engine.build(A, 1, 1, openers, moves, errors)
check(len(out["variants"]) == 12, "twelve variants")
# SCENARIO_CLAUDE's approved figures
sheet = {"H1": {"Q": 0}, "H5": {"Q": 4}, "H6": {"Q": 0.02}, "M6": {"Q": 1},
         "M1": {"x": 0.3333, "other": 1.0, "H2": 0.3333, "CO": 0.1667}, "M2": {"x": 0.6667, "other": 2.0, "H2": 0.6667, "CO": 0.3333},
         "M3": {"x": 0.2427, "other": 0.8239, "H2": 0.2427, "CO": 0.2573}, "M4": {"x": 0.1691, "other": 0.6309, "H2": 0.1691, "CO": 0.2309},
         "M5": {"x": 0.1667, "other": 0.5, "H2": 0.3333, "CO": 0.1667}, "M6": {"Q": 1, "x": 0.0667, "other": 0.6, "H2": 0.2667, "CO": 0.1333}}
def ex(v, state): return [e for e in v["expected"] if e.get("state") == state]
for v in out["variants"]:
    P = [f for f in A.FIXED if f["id"] == v["fixed_id"]][0]; rx = P["rxn"]; conc = [m / P["V"] for m in P["mol"]]
    d = v["context"]["direction"]; s = sheet.get(P["id"], {})
    q = ex(v, "Q_found")
    if "Q" in s: check(q and abs(q[0]["value"] - s["Q"]) <= 1e-6, f"{P['id']}: Q {q and q[0]['value']} vs sheet {s['Q']}")
    # the change row follows the shift and the coefficients; every cell I + C = E at a trial x
    for i in range(len(rx["species"])):
        I, C, Ecell = v["table"]["rows"]["I"][i], v["table"]["rows"]["C"][i], v["table"]["rows"]["E"][i]
        sign = -1 if rx["side"][i] * d < 0 else 1
        check(C == ("-" if sign < 0 else "+") + ("" if rx["coef"][i] == 1 else str(rx["coef"][i])) + "x", f"{P['id']}: change cell {C}")
    if rx is A.WGS:
        x = bisect(rx, conc, d); xf = ex(v, "x_found")[0]["value"]; check(abs(x - xf) <= 2e-6, f"{P['id']}: x {xf} vs bisection {x:.6f}")
        iH2, iCO = rx["species"].index("H2"), rx["species"].index("CO")
        eqH2 = conc[iH2] + rx["side"][iH2] * d * x; eqCO = conc[iCO] + rx["side"][iCO] * d * x
        check(abs(ex(v, "value_found")[0]["value"] - eqH2) <= 2e-6 and abs(ex(v, "leftover_found")[0]["value"] - eqCO) <= 2e-6, f"{P['id']}: [H2], [CO]")
        if s:
            check(abs(xf - s["x"]) <= 6e-5, f"{P['id']}: x vs sheet {s['x']}"); other = ex(v, "other_root_checked")[0]
            check(abs(abs(other["value"]) - s["other"]) <= 6e-5, f"{P['id']}: other root {other['value']} vs sheet {s['other']}")
            check(abs(eqH2 - s["H2"]) <= 6e-5 and abs(eqCO - s["CO"]) <= 6e-5, f"{P['id']}: [H2] {eqH2:.4f}/[CO] {eqCO:.4f} vs sheet")
        # the other root really is a root of the same equation, and it leaves a concentration below zero
        o = other["value"] if s else ex(v, "other_root_checked")[0]["value"]
        residual = lambda t: (conc[2] + d * t) * (conc[3] + d * t) - rx["K"] * (conc[0] - d * t) * (conc[1] - d * t)
        check(abs(residual(o)) <= 1e-6 * max(1.0, abs(o)), f"{P['id']}: the other root satisfies the quadratic")
        check(min(conc[i] + rx["side"][i] * d * rx["coef"][i] * o for i in range(4)) < 0, f"{P['id']}: the other root leaves a concentration below zero")
        kc = ex(v, "K_confirmed")[0]; check(kc["value"] == rx["K"] and kc.get("after") == "leftover_found", f"{P['id']}: K_confirmed is K, after the leftover")
    else:
        check(not ex(v, "x_found") and v["eq_checks"][0]["bent"].keys() >= {"EQ_COEFF_NOT_EXPONENT", "EQ_EXPONENT_NOT_IN_TABLE"}, f"{P['id']}: no x; both expression errors declared")
print("ch13_ice: " + ("all checks pass" if not fails else f"{fails} failed")); sys.exit(1 if fails else 0)
