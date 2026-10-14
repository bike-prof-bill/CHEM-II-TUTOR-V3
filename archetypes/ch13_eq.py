"""Chapter 13, combined (the instructor, 13 Oct 2026 evening: ICE and Q versus K are one archetype; four scenarios; each begins
with the direction, Q against K, then its ICE work where the problem has any, then TWO separate perturbations, then the meaning
and the last metacognitive question). Fixed problems. Replaces ch13_ice and the ch13_q_vs_k skeleton once the rebuilt scenarios
are approved; until then ch13_ice stays as shipped and this archetype ships nothing (its openers file has no row).

Step map (items present depend on the problem's `mode`):
  account_given -> relation_chosen (pick: the K or the Q expression) -> [conc_found] -> [Q_found] -> shift_predicted (direction)
  -> mode "setup":  table -> expression_set -> method                                          (Haber: stops before x, quartic)
     mode "solve":  table -> expression_set -> method -> x_found -> other_root_checked -> value_found -> leftover_found -> K_confirmed
     mode "none":   nothing between the direction and the perturbations                      (the tracer: no number to solve)
  -> perturb_1 (direction) -> perturb_1_why (text) -> perturb_2 (direction) -> perturb_2_why (text) -> meaning_given -> reflection.

Every number is declared from the problem data; the perturbation answers are computed from the reaction record (dH sign, gas
moles, which species is a solid) by archetypes/_equilibrium.py and re-derived in test_ch13_eq.py. The perturbation words (what the
researcher does) live in the scenario's moves rows (perturb_1, perturb_2, opener column); the archetype holds only the type and
the species, from SCENARIO_CLAUDE's problems sheet. Problems and perturbations marked DRAFT are placeholders.
"""
import json, os
from engine import round_sig
from _equilibrium import (quotient, multipliers_quotient, direction, x_max, solve_x, quadratic_roots, polynomial_degree, perturb_direction, PERTURBATION_TYPES)

ID = "ch13_eq"
TITLE = "Equilibrium: which way, how far, and what a change does"
RELATION_TEXT = "K = [products]^coefficients / [reactants]^coefficients at equilibrium; Q is the same fraction at any moment"
NOTEBOOK_URL = "https://notebook.google.com/notebook/6458f208-db32-496a-8088-fe0c1c6cd539"   # INSTRUCTOR: the course notebook
KINDS = ["haber_setup", "wgs_equilibrium", "agcl_tracer"]

_RX = json.load(open(os.path.join(os.path.dirname(__file__), "data", "reactions.json"), encoding="utf-8"))["reactions"]
def _rxn(rid, species, coef, side, active, gas, names, sim_keys):
    r = _RX[rid]
    return {"id": rid, "species": species, "coef": coef, "side": side, "active": active, "gas": gas, "K": r["Kc"],
            "dH_sign": r.get("dH_sign", 0), "names": names, "sim_keys": sim_keys, "equation": r["equation"]}
HABER = _rxn("haber_ammonia", ["N2", "H2", "NH3"], [1, 3, 2], [-1, -1, 1], [True] * 3, [True] * 3, ["nitrogen", "hydrogen", "ammonia"], ["nN2", "nH2", "nNH3"])
WGS   = _rxn("wgs", ["CO", "H2O", "CO2", "H2"], [1, 1, 1, 1], [-1, -1, 1, 1], [True] * 4, [True] * 4, ["carbon monoxide", "steam", "carbon dioxide", "hydrogen"], ["nCO", "nH2O", "nCO2", "nH2"])
AGCL  = _rxn("agcl_dissolution", ["AgCl", "Ag+", "Cl-"], [1, 1, 1], [-1, 1, 1], [False, True, True], [False] * 3, ["silver chloride", "silver ion", "chloride ion"], ["cAg", "cCl"])

# ---- perturbations per scenario (type, species) as (perturb_1, perturb_2). DRAFT: SCENARIO_CLAUDE and the instructor choose them.
PERTURB = {
  "haber_setup":    [("remove_product", "NH3"), ("heat", None)],          # DRAFT placeholders: ammonia drawn off; the reactor heated (exothermic: reverse)
  "wgs_equilibrium": [("add_reactant", "H2O"), ("compress", None)],       # DRAFT placeholders: more steam; the chamber squeezed (same gas moles each side: no shift)
  "agcl_tracer":    [("add_common_ion", "Cl-"), ("heat", None)],          # from the dynamic-solubility sketch: NaCl added; warmed (endothermic: forward)
}

# ---- the problems. mol: starting amounts (V in litres) or conc: concentrations in M; mode: setup | solve | none
def _h(fid, V, mol, text, family): return {"id": fid, "rxn": HABER, "kind": "haber_setup", "mode": "setup", "V": V, "mol": mol, "conc": None, "text": text, "family": family, "version": "", "sf": 2, "status": "approved problem (ch13_ice, 13 Oct); perturbations DRAFT"}
def _m(fid, V, mol, text, family, version): return {"id": fid, "rxn": WGS, "kind": "wgs_equilibrium", "mode": "solve", "V": V, "mol": mol, "conc": None, "text": text, "family": family, "version": version, "sf": 2, "status": "approved problem (ch13_ice, 13 Oct); perturbations DRAFT"}
_HT = "Inside a steel reactor at 500 °C, nitrogen and hydrogen make ammonia: N2(g) + 3H2(g) ⇌ 2NH3(g). At this temperature, Kc = 0.060. A chemist tests a {V} pilot vessel. She puts in {amounts}. Set up the ICE table. Then write Kc in terms of x."
_MT = "On Mars, a rover fills a sealed {V} steel chamber with {amounts} and heats it to 800 K. Inside, CO(g) + H2O(g) ⇌ CO2(g) + H2(g), and Kc = 4.00. What is the concentration of hydrogen at equilibrium? How much carbon monoxide is left?"
FIXED = [
  _h("H1", 1.00, [0.80, 1.20, 0.00], _HT.format(V="1.00 L", amounts="0.80 mol of nitrogen gas and 1.20 mol of hydrogen gas"), "A"),
  _h("H2", 2.00, [1.00, 3.00, 0.00], _HT.format(V="2.00 L", amounts="1.00 mol of nitrogen gas and 3.00 mol of hydrogen gas"), "A"),
  _h("H3", 1.00, [0.00, 0.00, 0.50], _HT.format(V="1.00 L", amounts="0.50 mol of ammonia gas"), "B"),
  _h("H4", 5.00, [0.00, 0.00, 1.00], _HT.format(V="5.00 L", amounts="1.00 mol of ammonia gas"), "B"),
  _h("H5", 1.00, [0.50, 0.50, 0.50], _HT.format(V="1.00 L", amounts="0.50 mol of nitrogen gas, 0.50 mol of hydrogen gas and 0.50 mol of ammonia gas"), "C (Q > K)"),
  _h("H6", 1.00, [0.50, 1.00, 0.10], _HT.format(V="1.00 L", amounts="0.50 mol of nitrogen gas, 1.00 mol of hydrogen gas and 0.10 mol of ammonia gas"), "C (Q < K)"),
  _m("M1", 10.0, [5.00, 5.00, 0.00, 0.00], _MT.format(V="10.0 L", amounts="5.00 mol of carbon monoxide and 5.00 mol of steam"), "A equal", "equal"),
  _m("M2", 2.00, [2.00, 2.00, 0.00, 0.00], _MT.format(V="2.00 L", amounts="2.00 mol of carbon monoxide and 2.00 mol of steam"), "A equal", "equal"),
  _m("M3", 2.00, [1.00, 0.60, 0.00, 0.00], _MT.format(V="2.00 L", amounts="1.00 mol of carbon monoxide and 0.60 mol of steam"), "B unequal", "unequal"),
  _m("M4", 5.00, [2.00, 1.00, 0.00, 0.00], _MT.format(V="5.00 L", amounts="2.00 mol of carbon monoxide and 1.00 mol of steam"), "B unequal", "unequal"),
  _m("M5", 2.00, [0.00, 0.00, 1.00, 1.00], "On Mars, a rover fills a sealed 2.00 L steel chamber with 1.00 mol of carbon dioxide and 1.00 mol of hydrogen and heats it to 800 K. Inside, CO(g) + H2O(g) ⇌ CO2(g) + H2(g), and Kc = 4.00. What is the concentration of hydrogen at equilibrium? How much carbon monoxide is in the chamber at equilibrium?", "C products", "products"),
  _m("M6", 5.00, [1.00, 1.00, 1.00, 1.00], "On Mars, a rover fills a sealed 5.00 L steel chamber with 1.00 mol each of carbon monoxide, steam, carbon dioxide and hydrogen and heats it to 800 K. Inside, CO(g) + H2O(g) ⇌ CO2(g) + H2(g), and Kc = 4.00. What is the concentration of hydrogen at equilibrium? How much carbon monoxide is left?", "D all four", "all"),
  # the dynamic-solubility tracer (the instructor's sketch from the OpenStax text, 13 Oct): at equilibrium. The numbers are the
  # sketch's, to two significant figures: (1.3e-5)^2 = 1.7e-10 equals 1.8e-10 to the figures given, and `direction` judges it so.
  # Q is an intermediate everywhere (asked for by name after the pick): when Q = K it must not be mistaken for the restated given
  {"id": "A1", "rxn": AGCL, "kind": "agcl_tracer", "mode": "none", "V": 1.0, "mol": None, "conc": [None, 1.3e-5, 1.3e-5], "sf": 2,
   "text": "A sealed beaker holds a saturated solution of silver chloride over a bed of solid AgCl at 25 °C: AgCl(s) ⇌ Ag+(aq) + Cl-(aq), Kc = 1.8 × 10^-10. A probe reads [Ag+] = 1.3 × 10^-5 M and [Cl-] = 1.3 × 10^-5 M. A researcher drops a small pellet of AgCl made with radioactive silver-110 onto the solid bed. Nothing else changes. Find Q at that moment and say which way the reaction goes.",
   "family": "E (Q = K)", "version": "", "status": "DRAFT (placeholder from the sketch; new SCENARIO_CLAUDE writes the six problems)"},
]

MECHANISM_WORDS = ["molecul", "particl", "atom", "ion", "collid", "collis", "forward", "reverse", "rate", "recombin", "decompos", "dissociat",
                   "associat", "equal", "same pace", "both direction", "energ", "bond", "swap", "break apart", "dissolv", "precipitat", "settle", "trade", "exchange"]

# ---- the unnamed Equations list. The K form and the Q form both fit (the student meets Q first; instructor to confirm).
EQUATION_PICKS = [
  {"id": "eq_k",  "text": "K = [C]^c [D]^d / ( [A]^a [B]^b )",         "fits": KINDS},
  {"id": "eq_q",  "text": "Q = [C]₀^c [D]₀^d / ( [A]₀^a [B]₀^b )",      "fits": KINDS},
  {"id": "eq_kp", "text": "Kp = Kc (RT)^Δn",                             "fits": []},
  {"id": "eq_g",  "text": "ΔG° = −RT ln K",                              "fits": []},
  {"id": "eq_r",  "text": "rate = k [A]^m [B]^n",                         "fits": []},
  {"id": "eq_ph", "text": "pH = −log[H₃O⁺]",                             "fits": []},
]
CONSTANTS = []

def window(value): return max(0.02 * abs(value), 1e-4 if abs(value) >= 1e-2 else 0.02 * abs(value))
def E(state, label, value, unit, **kw):
    d = {"state": state, "label": label, "value": round_sig(value, 6), "unit": unit, "abs_tol": round_sig(window(value), 3)}
    d.update(kw); return d
def _fmt_coef(c): return "" if c == 1 else str(c)
def _g(v): return f"{v:.3f}"
def _trap(tid, value, state): return {"id": tid, "state": state, "value": round_sig(value, 5), "unit": "", "abs_tol": round_sig(window(value), 3)}
def _clear(a, b): return abs(a - b) > 3 * max(window(a), window(b))
def _dir_opts(prefix, more):                       # option texts start with a bare word: the shell reads that word alone when typed
    return [{"id": f"{prefix}:forward", "text": f"forward toward more {more}"},
            {"id": f"{prefix}:reverse", "text": f"reverse toward less {more}"},
            {"id": f"{prefix}:neither", "text": "neither because it stays at equilibrium"}]
def _dir_id(prefix, d): return f"{prefix}:forward" if d > 0 else (f"{prefix}:reverse" if d < 0 else f"{prefix}:neither")

def make_fixed(rng, fid):
    P = [f for f in FIXED if f["id"] == fid][0]; rx = P["rxn"]; sp, coef, side, act = rx["species"], rx["coef"], rx["side"], rx["active"]
    conc = [m / P["V"] for m in P["mol"]] if P["mol"] is not None else [0.0 if c is None else c for c in P["conc"]]
    d = direction(rx, conc, sf=P["sf"]); Q = quotient(rx, conc)
    has_conc = P["mol"] is not None and P["V"] != 1.0
    expected, traps = [], []
    if has_conc:
        for i in range(len(sp)):
            if act[i]: expected.append(E("conc_found", f"starting [{sp[i]}]", conc[i], "M", role="intermediate", require_unit=True))
    if Q is not None:
        expected.append(E("Q_found", "Q at the start", Q, "", role="intermediate", require_unit=False, after="conc_found" if has_conc else "relation_chosen"))
        for tid, val in ((("Q_INVERTED", 1.0 / Q),) if Q > 0 else ()) + ((("COEFFICIENTS_AS_MULTIPLIERS", multipliers_quotient(rx, conc)),) if any(c > 1 for c, a in zip(coef, act) if a) else ()) + ((("EXPONENTS_DROPPED", quotient(rx, conc, exponents=False)),) if any(c > 1 for c, a in zip(coef, act) if a) else ()):
            if val is not None and _clear(val, Q) and all(_clear(val, t["value"]) for t in traps if t["state"] == "Q_found"): traps.append(_trap(tid, val, "Q_found"))
    # ---- the ICE work
    table = None; eq_checks = []
    if P["mode"] in ("setup", "solve"):
        cs = lambda i: ("-" if side[i] * d < 0 else "+") + _fmt_coef(coef[i]) + "x"
        es = lambda i: (f"{_g(conc[i])} {'-' if side[i] * d < 0 else '+'} {_fmt_coef(coef[i])}x") if conc[i] else _fmt_coef(coef[i]) + "x"
        table = {"species": sp, "rows": {"I": [_g(c) for c in conc], "C": [cs(i) for i in range(len(sp))], "E": [es(i) for i in range(len(sp))]},
                 "named": [{"id": "CHANGE_COEFF_IGNORED", "row": "C", "cells": [("-" if side[i] * d < 0 else "+") + "x" for i in range(len(sp))]},
                           {"id": "CHANGE_SIGNS_REVERSED", "row": "C", "cells": [("+" if side[i] * d < 0 else "-") + _fmt_coef(coef[i]) + "x" for i in range(len(sp))]}]
                          + ([{"id": "MOLES_NOT_CONCENTRATION", "row": "I", "cells": [_g(m) for m in P["mol"]]}] if P["V"] != 1.0 else []),
                 "zero_species": [i for i, c in enumerate(conc) if c == 0]}
        eq_checks = [expression_check(rx, conc, d)]
    if P["mode"] == "solve":
        x = solve_x(rx, conc, d); roots = quadratic_roots(rx, conc, d); other = [r for r in roots if abs(r - x) > 1e-6][0]
        eq = [conc[i] + side[i] * d * coef[i] * x for i in range(len(sp))]
        iH2, iCO = sp.index("H2"), sp.index("CO")
        expected += [E("x_found", "x", x, "", role="intermediate", require_unit=False),
                     E("other_root_checked", "the other root", other, "", role="intermediate", require_unit=False, after="x_found",
                       also=([{"value": round_sig(-other, 6), "unit": "", "abs_tol": round_sig(window(other), 3)}] if other < 0 else [])),
                     E("value_found", "equilibrium [H2]", eq[iH2], "M", role="key", require_unit=True),
                     E("leftover_found", "equilibrium [CO]", eq[iCO], "M", role="intermediate", require_unit=True),
                     E("K_confirmed", "Kc from the equilibrium row", rx["K"], "", role="intermediate", require_unit=False, after="leftover_found", abs_tol=round_sig(0.03 * rx["K"], 3))]
        traps.append({"id": "PHANTOM_ROOT", "state": "x_found", "value": round_sig(abs(other), 5), "unit": "", "abs_tol": round_sig(window(other), 3)})
        if abs(eq[iCO] - eq[iH2]) > 3 * max(window(eq[iCO]), window(eq[iH2])):
            traps.append({"id": "LEFTOVER_FOR_PRODUCT", "state": "value_found", "value": round_sig(eq[iCO], 5), "unit": "M", "abs_tol": round_sig(window(eq[iCO]), 3)})
            traps.append({"id": "LEFTOVER_FOR_PRODUCT", "state": "leftover_found", "value": round_sig(eq[iH2], 5), "unit": "M", "abs_tol": round_sig(window(eq[iH2]), 3)})
        traps.append({"id": "MOLES_NOT_CONCENTRATION", "state": "value_found", "value": round_sig(eq[iH2] * P["V"], 5), "unit": "M", "abs_tol": round_sig(window(eq[iH2] * P["V"]), 3)})
        a, b = conc[0], conc[1]
        if P["version"] == "equal":
            x_one = rx["K"] * a / (1 + rx["K"]); traps.append({"id": "SQRT_ONE_SIDE", "state": "x_found", "value": round_sig(x_one, 5), "unit": "", "abs_tol": round_sig(window(x_one), 3)})
        if P["version"] == "unequal":
            r = rx["K"] ** 0.5
            for s0 in (a, b): xs = r * s0 / (1 + r); traps.append({"id": "SQRT_ON_NONSQUARE", "state": "x_found", "value": round_sig(xs, 5), "unit": "", "abs_tol": round_sig(window(xs), 3)})
        traps.append({"id": "EXCEEDS_INITIAL", "state": "x_found", "above": round_sig(x_max(rx, conc, d) * 1.02, 5), "unit": ""})
    # ---- the perturbations: the right answer from the reaction record
    perts = PERTURB[P["kind"]]
    if len(perts) != 2: raise RuntimeError(f"{ID}: {P['kind']} must declare exactly two perturbations")
    pdirs = [perturb_direction(rx, t, s) for t, s in perts]
    # ---- the step map
    more = rx["names"][next(i for i, s in enumerate(side) if s > 0)]
    board = [
      {"state": "account_given",   "kind": "text", "register": "submicro", "requires": []},
      {"state": "relation_chosen", "kind": "pick", "register": "symbolic", "requires": ["account_given"], "options_from": "equation_picks", "pin": True},
    ]
    prev = "relation_chosen"
    if has_conc: board.append({"state": "conc_found", "kind": "number", "register": "symbolic", "requires": [prev], "rule": "all", "pin": True, "explicit": True}); prev = "conc_found"
    if Q is not None: board.append({"state": "Q_found", "kind": "number", "register": "symbolic", "requires": [prev], "explicit": True, "pin": True}); prev = "Q_found"
    board.append({"state": "shift_predicted", "kind": "direction", "register": "macro", "requires": [prev], "options": _dir_opts("direction", more), "right": [_dir_id("direction", d)], "explicit": True, "pin": True}); prev = "shift_predicted"
    if P["mode"] in ("setup", "solve"):
        deg = polynomial_degree(rx)
        board += [
          {"state": "table",          "kind": "table",    "register": "symbolic", "requires": [prev], "pin": True, "explicit": True},
          {"state": "expression_set", "kind": "equation", "register": "symbolic", "requires": ["table"], "explicit": True, "pin": True},
          {"state": "method",         "kind": "pick",     "register": "symbolic", "requires": ["expression_set"],
           "options": [{"id": "method:sqrt", "text": "Both sides are perfect squares: take the square root of both."},
                       {"id": "method:quadratic", "text": "Clear the denominator and use the quadratic formula."},
                       {"id": "method:solver", "text": "The equation is quartic: a graph or a computer solver."},
                       {"id": "method:smallx", "text": "x is small next to the starting amount: drop it from the denominator."}],
           "right": ["method:solver"] if deg > 2 else (["method:sqrt"] if P["version"] in ("equal", "products", "all") else ["method:quadratic"])},
        ]
        prev = "method"
    if P["mode"] == "solve":
        board += [
          {"state": "x_found",            "kind": "number", "register": "symbolic", "requires": ["method"], "explicit": True},
          {"state": "other_root_checked", "kind": "number", "register": "symbolic", "requires": ["x_found"], "explicit": True},
          {"state": "value_found",        "kind": "number", "register": "macro",    "requires": ["other_root_checked"], "explicit": True},
          {"state": "leftover_found",     "kind": "number", "register": "macro",    "requires": ["value_found"], "explicit": True},
          {"state": "K_confirmed",        "kind": "number", "register": "symbolic", "requires": ["leftover_found"], "explicit": True},
        ]
        prev = "K_confirmed"
    for n, pd in enumerate(pdirs, start=1):
        board += [
          {"state": f"perturb_{n}",     "kind": "direction", "register": "macro",    "requires": [prev], "options": _dir_opts(f"p{n}", more), "right": [_dir_id(f"p{n}", pd)], "explicit": True, "pin": True},
          {"state": f"perturb_{n}_why", "kind": "text",      "register": "submicro", "requires": [f"perturb_{n}"]},
        ]
        prev = f"perturb_{n}_why"
    board += [
      {"state": "meaning_given", "kind": "text",       "register": "inference", "requires": [prev], "credit_gate": True},
      {"state": "reflection",    "kind": "reflection", "register": "inference", "requires": ["meaning_given"]},
    ]
    if P["mol"] is not None:
        givens = {f"n_{sp[i]}": {"value": P["mol"][i], "unit": "mol"} for i in range(len(sp)) if P["mol"][i]}
        givens["V"] = {"value": P["V"], "unit": "L"}
    else:
        givens = {f"c_{sp[i]}": {"value": conc[i], "unit": "M"} for i in range(len(sp)) if act[i] and conc[i]}
    givens["Kc"] = {"value": rx["K"], "unit": ""}
    if P["mol"] is not None: sim_params = {k: P["mol"][i] for i, k in enumerate(rx["sim_keys"])}; sim_params["V"] = P["V"]
    else: sim_params = {k: conc[i + 1] for i, k in enumerate(rx["sim_keys"])}
    return {"kind": P["kind"], "fixed_id": P["id"], "version": P["version"], "status": P["status"],
            "context": {"reaction": rx["id"], "family": P["family"], "direction": d, "mode": P["mode"], "sf": P["sf"],
                        "perturbations": [{"type": t, "species": s, "direction": pd} for (t, s), pd in zip(perts, pdirs)]},
            "text": P["text"], "givens": givens, "board": board, "targets": expected, "traps": traps, "table": table,
            "eq_checks": eq_checks, "reveal_with_problem": None, "sim": None, "sim_params": sim_params}

def expression_check(rx, conc, d):
    xm = x_max(rx, conc, d)
    def states(form): return [{"x": round_sig(x, 9), "K": round_sig(form(x), 9)} for x in (0.15 * xm, 0.35 * xm, 0.55 * xm)]
    def form(exp_ok, mult_ok):
        def f(x):
            num = den = 1.0
            for i, s in enumerate(rx["side"]):
                if not rx["active"][i]: continue
                v = conc[i] + s * d * (rx["coef"][i] if mult_ok else 1) * x
                p = rx["coef"][i] if exp_ok else 1
                if s > 0: num *= v ** p
                else: den *= v ** p
            return num / den
        return f
    bent = {}
    if any(c > 1 for c, a in zip(rx["coef"], rx["active"]) if a):
        bent["EQ_COEFF_NOT_EXPONENT"] = states(form(False, True)); bent["EQ_EXPONENT_NOT_IN_TABLE"] = states(form(True, False))
    def term(i):
        c, s = rx["coef"][i], rx["side"][i] * d; base = (f"({_g(conc[i])} {'-' if s < 0 else '+'} {_fmt_coef(c)}x)" if conc[i] else (f"({_fmt_coef(c)}x)" if c > 1 else "x"))
        return base + (f"^{c}" if c > 1 else "")
    park = f"{_g(rx['K'])} = " + " · ".join(term(i) for i, s in enumerate(rx["side"]) if s > 0 and rx["active"][i]) + " / ( " + " · ".join(term(i) for i, s in enumerate(rx["side"]) if s < 0 and rx["active"][i]) + " )"
    return {"state": "expression_set", "unknown": "K", "true": states(form(True, True)), "alt": [], "bent": bent, "literal_for": {"K": rx["K"]}, "park_text": park}

EQUATION_SYMBOLS = {"x": ["x"], "K": ["Kc", "K_c", "Keq", "Ksp", "K"]}
EQUATION_CONSTANTS = {}

# Fallbacks only; the approved asks come from content_ch13_eq_errors.csv.
TRAP_NOTES = {
  "EXCEEDS_INITIAL":            {"note": "Their x is larger than the amount that could react, so a concentration went below zero.", "ask": "Compare your x with the amount you started with. Can more react away than was there?"},
  "EQ_COEFF_NOT_EXPONENT":      {"note": "Their expression holds only with every exponent read as 1: the coefficients are in the table but not used as exponents.", "ask": "The coefficients do double duty. What is the exponent for each species?"},
  "EQ_EXPONENT_NOT_IN_TABLE":   {"note": "Their expression holds only with the change row read as ±x for every species: the exponents are there, the table's multiples are not.", "ask": "A coefficient is an exponent here. Is it also in the change row?"},
  "Q_INVERTED":                 {"note": "Their number is 1/Q: reactants over products.", "ask": "Which concentrations go on top of the fraction, and which go underneath?"},
  "COEFFICIENTS_AS_MULTIPLIERS": {"note": "Their number comes from multiplying each concentration by its coefficient instead of raising it to that power.", "ask": "Look at the largest coefficient. In the expression, where does that number go?"},
  "EXPONENTS_DROPPED":          {"note": "Their number is the quotient with every exponent read as 1.", "ask": "Does every species in the expression carry an exponent of 1 here?"},
}

def render_text(*a): raise NotImplementedError("fixed problems carry their own text")
