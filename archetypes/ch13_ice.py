"""Chapter 13: ICE tables and equilibrium concentrations. Twelve fixed problems (the instructor, 13 Oct 2026: "equilibrium
problems are fixed text"), two scenarios, each with its own step map:

  The Haber-Bosch Harvest (kind `haber_setup`, role exam): set up the table and write Kc in terms of x; stops before x
  (the equation is quartic). account -> relation -> approach -> [conc_found] -> [Q_found] -> shift_predicted -> table ->
  expression_set -> method -> meaning -> reflection.
  The Martian Fuel Factory (kind `wgs_equilibrium`, role worked): the water-gas shift, solved. ... -> method -> x_found ->
  other_root_checked -> value_found ([H2]) -> leftover_found ([CO]) -> K_confirmed -> meaning -> reflection.

Every number is declared from the problem data (`FIXED`); nothing is generated. Constants: `archetypes/data/reactions.json`
(each with its source). Named errors and their asks: `content_ch13_ice_errors.csv` (SCENARIO_CLAUDE, instructor-approved);
the values below are SCENARIO_CLAUDE's `ch13_problems.csv`, recomputed here and checked by `test_ch13_ice.py`.
"""
import math, json, os
from engine import round_sig

ID = "ch13_ice"
TITLE = "ICE tables and equilibrium concentrations"
RELATION_TEXT = "K = [products]^coefficients / [reactants]^coefficients, at equilibrium"
NOTEBOOK_URL = "https://notebook.google.com/notebook/6458f208-db32-496a-8088-fe0c1c6cd539"   # INSTRUCTOR: the course notebook
KINDS = ["haber_setup", "wgs_equilibrium"]

_RX = json.load(open(os.path.join(os.path.dirname(__file__), "data", "reactions.json"), encoding="utf-8"))["reactions"]
HABER = {"id": "haber_ammonia", "species": ["N2", "H2", "NH3"], "coef": [1, 3, 2], "side": [-1, -1, 1], "K": _RX["haber_ammonia"]["Kc"],
         "names": ["nitrogen", "hydrogen", "ammonia"], "sim_keys": ["nN2", "nH2", "nNH3"]}
WGS = {"id": "wgs", "species": ["CO", "H2O", "CO2", "H2"], "coef": [1, 1, 1, 1], "side": [-1, -1, 1, 1], "K": _RX["wgs"]["Kc"],
       "names": ["carbon monoxide", "steam", "carbon dioxide", "hydrogen"], "sim_keys": ["nCO", "nH2O", "nCO2", "nH2"]}

# ---- the twelve problems, exactly as approved (SCENARIO_CLAUDE's ch13_problems.csv, instructor 13 Oct 2026).
#      mol: starting amounts in reaction order; V: litres. Haber problems have no x step; Martian ones solve.
def _h(fid, V, mol, text, family): return {"id": fid, "rxn": HABER, "kind": "haber_setup", "V": V, "mol": mol, "text": text, "family": family, "version": ""}
def _m(fid, V, mol, text, family, version): return {"id": fid, "rxn": WGS, "kind": "wgs_equilibrium", "V": V, "mol": mol, "text": text, "family": family, "version": version}
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
]

# ---- words that mark a particle-level account in this chapter (V2's list, kept; the scenario keyword cells carry the chapter's words)
MECHANISM_WORDS = ["molecul", "particl", "atom", "ion", "collid", "collis", "forward", "reverse", "rate", "recombin",
                   "decompos", "dissociat", "associat", "equal", "same pace", "both direction", "energ", "bond", "swap", "break apart"]

# ---- the unnamed Equations list the student picks from. One fits; the others are look-alikes from nearby chapters.
EQUATION_PICKS = [
  {"id": "eq_k",  "text": "K = [C]^c [D]^d / ( [A]^a [B]^b )",         "fits": KINDS},
  {"id": "eq_kp", "text": "Kp = Kc (RT)^Δn",                             "fits": []},
  {"id": "eq_q",  "text": "Q = [C]₀^c [D]₀^d / ( [A]₀^a [B]₀^b )",      "fits": []},
  {"id": "eq_g",  "text": "ΔG° = −RT ln K",                              "fits": []},
  {"id": "eq_r",  "text": "rate = k [A]^m [B]^n",                         "fits": []},
  {"id": "eq_ph", "text": "pH = −log[H₃O⁺]",                             "fits": []},
]
# no declared constants: a bare 1 or 2 here is a root or a quotient, never a harmless restatement (V2's "one" and "two" hid PHANTOM_ROOT = 1.0, 13 Oct)
CONSTANTS = []

def window(value): return max(0.02 * abs(value), 1e-4)
def E(state, label, value, unit, **kw):
    d = {"state": state, "label": label, "value": round_sig(value, 6), "unit": unit, "abs_tol": round_sig(window(value), 3)}
    d.update(kw); return d
def _fmt_coef(c): return "" if c == 1 else str(c)
def _g(v): return f"{v:.3f}"

# ---- the chemistry, recomputed from the data (checked independently in test_ch13_ice.py)
def quotient(rx, conc):
    num = den = 1.0; zero_bottom = False
    for i, s in enumerate(rx["side"]):
        if s > 0: num *= conc[i] ** rx["coef"][i]
        else:
            if conc[i] == 0: zero_bottom = True
            den *= conc[i] ** rx["coef"][i]
    return None if zero_bottom else num / den
def direction(rx, conc):                          # +1 toward products, -1 toward reactants, 0 at equilibrium
    Q = quotient(rx, conc)
    if Q is None: return -1                       # a reactant is missing entirely: the reverse reaction is the only one that can run
    return 0 if abs(Q - rx["K"]) <= 1e-9 else (1 if Q < rx["K"] else -1)
def mass_action(rx, conc, d, x):
    num = den = 1.0
    for i, s in enumerate(rx["side"]):
        v = conc[i] + s * d * rx["coef"][i] * x
        if s > 0: num *= v ** rx["coef"][i]
        else: den *= v ** rx["coef"][i]
    return num / den
def x_max(rx, conc, d):                           # the largest x before a consumed species runs out
    return min(conc[i] / rx["coef"][i] for i, s in enumerate(rx["side"]) if s * d < 0)
def solve_x(rx, conc, d):                         # bisection on the mass-action equation, the only solver here
    lo, hi = 0.0, x_max(rx, conc, d) * 0.999999
    for _ in range(300):
        m = 0.5 * (lo + hi)
        if (mass_action(rx, conc, d, m) < rx["K"]) == (d > 0): lo = m
        else: hi = m
    return 0.5 * (lo + hi)
def wgs_roots(conc, d, K):                        # the water-gas shift's quadratic, both roots, x measured in the direction of the shift
    a, b, c, e = [conc[i] for i in range(4)]      # CO, H2O, CO2, H2
    if d > 0:  A, B, C = K - 1.0, -(K * (a + b) + (c + e)), K * a * b - c * e          # K(a-x)(b-x) = (c+x)(e+x)
    else:      A, B, C = 1.0 - K, -((c + e) + K * (a + b)), c * e - K * a * b          # (c-x)(e-x) = K(a+x)(b+x)
    if abs(A) < 1e-12: return [-C / B]
    disc = math.sqrt(B * B - 4 * A * C); return sorted([(-B - disc) / (2 * A), (-B + disc) / (2 * A)])

def make_fixed(rng, fid):
    P = [f for f in FIXED if f["id"] == fid][0]; rx = P["rxn"]; sp, coef, side = rx["species"], rx["coef"], rx["side"]
    conc = [m / P["V"] for m in P["mol"]]; d = direction(rx, conc); Q = quotient(rx, conc)
    cs = lambda i: ("-" if side[i] * d < 0 else "+") + _fmt_coef(coef[i]) + "x"          # the change-row cell
    es = lambda i: (f"{_g(conc[i])} {'-' if side[i] * d < 0 else '+'} {_fmt_coef(coef[i])}x") if conc[i] else _fmt_coef(coef[i]) + "x"
    table = {"species": sp, "rows": {"I": [_g(c) for c in conc], "C": [cs(i) for i in range(len(sp))], "E": [es(i) for i in range(len(sp))]},
             # named wrong tables (instructor-approved errors file): the change row with the coefficients ignored, with the signs reversed,
             # and the initial row in moles when the vessel is not one litre
             "named": [{"id": "CHANGE_COEFF_IGNORED", "row": "C", "cells": [("-" if side[i] * d < 0 else "+") + "x" for i in range(len(sp))]},
                       {"id": "CHANGE_SIGNS_REVERSED", "row": "C", "cells": [("+" if side[i] * d < 0 else "-") + _fmt_coef(coef[i]) + "x" for i in range(len(sp))]}]
                      + ([{"id": "MOLES_NOT_CONCENTRATION", "row": "I", "cells": [_g(m) for m in P["mol"]]}] if P["V"] != 1.0 else []),
             "zero_species": [i for i, c in enumerate(conc) if c == 0]}        # START_ZERO_MISSING: a non-zero or missing initial entry here
    expected, traps = [], []
    has_conc = P["V"] != 1.0
    if has_conc:
        for i in range(len(sp)): expected.append(E("conc_found", f"starting [{sp[i]}]", conc[i], "M", role="intermediate", require_unit=True))
    # Q is a pure number asked for by name after the concentrations (or the approach) are in place; `after` gates it so a bare
    # "1" or "0" earlier is not read as Q (M6: every amount is 1.00 mol and Q = 1)
    if Q is not None: expected.append(E("Q_found", "Q at the start", Q, "", role="intermediate", require_unit=False, after="conc_found" if has_conc else "approach"))
    is_wgs = rx is WGS
    if is_wgs:
        x = solve_x(rx, conc, d); roots = wgs_roots(conc, d, rx["K"]); other = [r for r in roots if abs(r - x) > 1e-6][0]
        eq = [conc[i] + side[i] * d * coef[i] * x for i in range(len(sp))]
        iH2, iCO = sp.index("H2"), sp.index("CO")
        expected += [E("x_found", "x", x, "", role="intermediate", require_unit=False),
                     # the other root, as the formula gives it; its magnitude also counts (M5's is -0.5, which SCENARIO_CLAUDE lists as 0.5)
                     E("other_root_checked", "the other root", other, "", role="intermediate", require_unit=False, after="x_found",
                       also=([{"value": round_sig(-other, 6), "unit": "", "abs_tol": round_sig(window(other), 3)}] if other < 0 else [])),
                     E("value_found", "equilibrium [H2]", eq[iH2], "M", role="key", require_unit=True),
                     E("leftover_found", "equilibrium [CO]", eq[iCO], "M", role="intermediate", require_unit=True),
                     # the check: the equilibrium concentrations put back into Kc. The value equals the given K; it counts only once the
                     # leftover is in (`after`), so a "4.00" typed earlier is the given restated, and typed here is the check (approved show cell: "Type the value")
                     E("K_confirmed", "Kc from the equilibrium row", rx["K"], "", role="intermediate", require_unit=False, after="leftover_found", abs_tol=round_sig(0.03 * rx["K"], 3))]
        # traps as SCENARIO_CLAUDE computed them (instructor-approved 13 Oct); each recomputed here from the same data
        traps.append({"id": "PHANTOM_ROOT", "state": "x_found", "value": round_sig(abs(other), 5), "unit": "", "abs_tol": round_sig(window(other), 3)})
        if abs(eq[iCO] - eq[iH2]) > 3 * max(window(eq[iCO]), window(eq[iH2])):     # the swap is a nameable error only when the two differ clearly (M3, M4: they do not)
            traps.append({"id": "LEFTOVER_FOR_PRODUCT", "state": "value_found", "value": round_sig(eq[iCO], 5), "unit": "M", "abs_tol": round_sig(window(eq[iCO]), 3)})
            traps.append({"id": "LEFTOVER_FOR_PRODUCT", "state": "leftover_found", "value": round_sig(eq[iH2], 5), "unit": "M", "abs_tol": round_sig(window(eq[iH2]), 3)})
        traps.append({"id": "MOLES_NOT_CONCENTRATION", "state": "value_found", "value": round_sig(eq[iH2] * P["V"], 5), "unit": "M", "abs_tol": round_sig(window(eq[iH2] * P["V"]), 3)})
        a, b = conc[0], conc[1]
        if P["version"] == "equal":               # the square root of one side only: sqrt(K) = x/(a-x) read as K = x/(a-x)
            x_one = rx["K"] * a / (1 + rx["K"]); traps.append({"id": "SQRT_ONE_SIDE", "state": "x_found", "value": round_sig(x_one, 5), "unit": "", "abs_tol": round_sig(window(x_one), 3)})
        if P["version"] == "unequal":             # the square root taken although the two starts differ, with either start
            r = math.sqrt(rx["K"])
            for s0 in (a, b): xs = r * s0 / (1 + r); traps.append({"id": "SQRT_ON_NONSQUARE", "state": "x_found", "value": round_sig(xs, 5), "unit": "", "abs_tol": round_sig(window(xs), 3)})
        traps.append({"id": "EXCEEDS_INITIAL", "state": "x_found", "above": round_sig(x_max(rx, conc, d) * 1.02, 5), "unit": ""})
    for e in expected: e.setdefault("role", "intermediate")
    # ---- the step map (SCENARIO_CLAUDE's moves rows supply every word)
    more = rx["names"][sp.index("NH3")] if rx is HABER else rx["names"][sp.index("H2")]
    shift_opts = [{"id": "direction:more", "text": f"toward more {more}"}, {"id": "direction:less", "text": f"toward less {more}"}, {"id": "direction:neither", "text": "neither: it is already at equilibrium"}]
    shift_right = "direction:more" if d > 0 else ("direction:less" if d < 0 else "direction:neither")
    board = [
      {"state": "account_given",   "kind": "text",      "register": "submicro",  "requires": []},
      {"state": "relation_chosen", "kind": "pick",      "register": "symbolic",  "requires": ["account_given"], "options_from": "equation_picks", "pin": True},
      {"state": "approach",        "kind": "pick",      "register": "symbolic",  "requires": ["relation_chosen"],
       "options": [{"id": "approach:findK", "text": "Equilibrium amounts are measured; find K from them."},
                   {"id": "approach:solveX", "text": "K is known; find the equilibrium amounts from it."}], "right": ["approach:solveX"]},
    ]
    prev = "approach"
    if has_conc: board.append({"state": "conc_found", "kind": "number", "register": "symbolic", "requires": [prev], "rule": "all", "pin": True, "explicit": True}); prev = "conc_found"
    if Q is not None: board.append({"state": "Q_found", "kind": "number", "register": "symbolic", "requires": [prev], "explicit": True}); prev = "Q_found"
    board += [
      {"state": "shift_predicted", "kind": "direction", "register": "macro",    "requires": [prev], "options": shift_opts, "right": [shift_right]},
      {"state": "table",           "kind": "table",     "register": "symbolic",  "requires": ["shift_predicted"], "pin": True, "explicit": True},
      {"state": "expression_set",  "kind": "equation",  "register": "symbolic",  "requires": ["table"], "explicit": True, "pin": True},
      {"state": "method",          "kind": "pick",      "register": "symbolic",  "requires": ["expression_set"],
       "options": [{"id": "method:sqrt", "text": "Both sides are perfect squares: take the square root of both."},
                   {"id": "method:quadratic", "text": "Clear the denominator and use the quadratic formula."},
                   {"id": "method:solver", "text": "The equation is quartic: a graph or a computer solver."},
                   {"id": "method:smallx", "text": "x is small next to the starting amount: drop it from the denominator."}],
       "right": ["method:solver"] if not is_wgs else (["method:sqrt"] if P["version"] in ("equal", "products", "all") else ["method:quadratic"])},
    ]
    if is_wgs:
        board += [
          # each number is its own evidence: none is implied by a later one (explicit), since the leftover can be found without the hydrogen
          {"state": "x_found",            "kind": "number", "register": "symbolic", "requires": ["method"], "explicit": True},
          {"state": "other_root_checked", "kind": "number", "register": "symbolic", "requires": ["x_found"], "explicit": True},
          {"state": "value_found",        "kind": "number", "register": "macro",    "requires": ["other_root_checked"], "explicit": True},
          {"state": "leftover_found",     "kind": "number", "register": "macro",    "requires": ["value_found"], "explicit": True},
          {"state": "K_confirmed",        "kind": "number", "register": "symbolic", "requires": ["leftover_found"], "explicit": True},
        ]
    board += [
      {"state": "meaning_given", "kind": "text",       "register": "inference", "requires": ["K_confirmed" if is_wgs else "method"], "credit_gate": True},
      {"state": "reflection",    "kind": "reflection", "register": "inference", "requires": ["meaning_given"]},
    ]
    givens = {f"n_{sp[i]}": {"value": P["mol"][i], "unit": "mol"} for i in range(len(sp)) if P["mol"][i]}
    givens.update({"V": {"value": P["V"], "unit": "L"}, "Kc": {"value": rx["K"], "unit": ""}})
    sim_params = {k: P["mol"][i] for i, k in enumerate(rx["sim_keys"])}; sim_params["V"] = P["V"]
    return {"kind": P["kind"], "fixed_id": P["id"], "version": P["version"], "context": {"reaction": rx["id"], "family": P["family"], "direction": d},
            "text": P["text"], "givens": givens, "board": board, "targets": expected, "traps": traps, "table": table,
            "eq_checks": [expression_check(rx, conc, d)], "reveal_with_problem": None, "sim": None, "sim_params": sim_params}

def expression_check(rx, conc, d):
    """The equation engine's states: K and x satisfying K = products^c / reactants^c with THIS problem's starting concentrations as
    literals and the change row folded in. Bent sets name the two expression errors (errors file): the coefficients not used as
    exponents, and the exponents present without the table's multiples of x."""
    xm = x_max(rx, conc, d)
    def states(form): return [{"x": round_sig(x, 9), "K": round_sig(form(x), 9)} for x in (0.15 * xm, 0.35 * xm, 0.55 * xm)]
    def form(exp_ok, mult_ok):
        def f(x):
            num = den = 1.0
            for i, s in enumerate(rx["side"]):
                v = conc[i] + s * d * (rx["coef"][i] if mult_ok else 1) * x
                p = rx["coef"][i] if exp_ok else 1
                if s > 0: num *= v ** p
                else: den *= v ** p
            return num / den
        return f
    bent = {}
    if any(c > 1 for c in rx["coef"]):
        bent["EQ_COEFF_NOT_EXPONENT"] = states(form(False, True)); bent["EQ_EXPONENT_NOT_IN_TABLE"] = states(form(True, False))
    def term(i):
        c, s = rx["coef"][i], rx["side"][i] * d; base = (f"({_g(conc[i])} {'-' if s < 0 else '+'} {_fmt_coef(c)}x)" if conc[i] else (f"({_fmt_coef(c)}x)" if c > 1 else "x"))
        return base + (f"^{c}" if c > 1 else "")
    park = f"{_g(rx['K'])} = " + " · ".join(term(i) for i, s in enumerate(rx["side"]) if s > 0) + " / ( " + " · ".join(term(i) for i, s in enumerate(rx["side"]) if s < 0) + " )"
    return {"state": "expression_set", "unknown": "K", "true": states(form(True, True)), "alt": [], "bent": bent, "literal_for": {"K": rx["K"]}, "park_text": park}

EQUATION_SYMBOLS = {"x": ["x"], "K": ["Kc", "K_c", "Keq", "K"]}
EQUATION_CONSTANTS = {}

# What the tutor is told when a named error appears; the asks come from content_ch13_ice_errors.csv (approved). Fallbacks only.
TRAP_NOTES = {
  "EXCEEDS_INITIAL":            {"note": "Their x is larger than the amount that could react, so a concentration went below zero.",
                                 "ask": "Compare your x with the amount you started with. Can more react away than was there?"},
  "EQ_COEFF_NOT_EXPONENT":      {"note": "Their expression holds only with every exponent read as 1: the coefficients are in the table but not used as exponents.",
                                 "ask": "The coefficients do double duty. What is the exponent for H2? For NH3?"},
  "EQ_EXPONENT_NOT_IN_TABLE":   {"note": "Their expression holds only with the change row read as ±x for every species: the exponents are there, the table's multiples are not.",
                                 "ask": "The 3 in 3H2 is an exponent here. Is it also in the change row?"},
}

def render_text(*a): raise NotImplementedError("fixed problems carry their own text")
