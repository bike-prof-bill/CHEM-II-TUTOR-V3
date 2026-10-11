"""
ch13_ice.py  --  ICE tables and equilibrium concentrations.  ARCHETYPE DEFINITION, second archetype.
Stand-in built for the rebuild spec (step 3): V2's six problems as FIXED variants, no generator yet.
Shares no code with ch10_cc.py. Everything the shell needs comes through the same contract.

INSTRUCTOR = yours to set.   DRAFT = my placeholder; replace or approve before students see it.
Ported from reference/v2/Code_V2-6.txt: SOLVERS.ice (the numbers), problemPools["ch13_ice"] (the six problems),
TRAPS["ch13_ice"] (the wrong turns), OPENERS/OPENER_KEYWORDS (content_ch13_ice_openers.csv), WORKFLOWS (moves rows).
"""
import math
from engine import round_sig

ID    = "ch13_ice"
TITLE = "ICE tables and equilibrium concentrations"
RELATION_TEXT = "K = [products]^coefficients / [reactants]^coefficients, at equilibrium"
NOTEBOOK_URL  = ""          # INSTRUCTOR: the course notebook for chapter 13. Empty = the notebook card shows no link yet.

KINDS = ["findK", "perfectSquare", "quadratic"]

# ---- the six problems, exactly as V2 shipped them. `text` is V2's wording (instructor's pool). DRAFT only where marked.
#      species: in reaction order; coef: stoichiometric coefficients; side: -1 reactant, +1 product;
#      init_M: initial concentrations; a0 is the reactant whose change is -x (V2's a0).
FIXED = [
  {"id": "hi_findK",   "mode": "findK", "rxn": "H₂ + I₂ ⇌ 2HI", "species": ["H₂", "I₂", "HI"], "coef": [1, 1, 2], "side": [-1, -1, 1],
   "text": "A 1.00 L flask is filled with 1.00 mol of H2 and 1.00 mol of I2. At equilibrium, the concentration of HI is 1.56 M. Calculate Kc for H2 + I2 <=> 2HI.",
   "givens": {"n_H2": (1.00, "mol"), "n_I2": (1.00, "mol"), "V": (1.00, "L"), "HI_eq": (1.56, "M")}, "init_M": [1.00, 1.00, 0.0], "prod_eq": 1.56, "ask": "K"},
  {"id": "cohoh_ps",   "mode": "perfectSquare", "rxn": "CO + H₂O ⇌ CO₂ + H₂", "species": ["CO", "H₂O", "CO₂", "H₂"], "coef": [1, 1, 1, 1], "side": [-1, -1, 1, 1],
   "text": "For CO + H2O <=> CO2 + H2, Kc = 1.00 at 700 K. If initially 1.50 mol of CO and 1.50 mol of H2O are placed in a 2.00 L vessel, find equilibrium concentrations.",
   "givens": {"n_CO": (1.50, "mol"), "n_H2O": (1.50, "mol"), "V": (2.00, "L"), "K": (1.00, "")}, "init_M": [0.750, 0.750, 0.0, 0.0], "K": 1.00, "ask": "product"},
  {"id": "pcl5_quad",  "mode": "quadratic", "rxn": "PCl₅ ⇌ PCl₃ + Cl₂", "species": ["PCl₅", "PCl₃", "Cl₂"], "coef": [1, 1, 1], "side": [-1, 1, 1],
   "text": "For PCl5 <=> PCl3 + Cl2, Kc = 0.042 at 250 °C. Initially 0.80 mol PCl5 is in a 1.0 L container. Find equilibrium [Cl2].",
   "givens": {"n_PCl5": (0.80, "mol"), "V": (1.0, "L"), "K": (0.042, "")}, "init_M": [0.80, 0.0, 0.0], "K": 0.042, "ask": "product"},
  {"id": "n2o4_findK", "mode": "findK", "rxn": "N₂O₄ ⇌ 2NO₂", "species": ["N₂O₄", "NO₂"], "coef": [1, 2], "side": [-1, 1],
   "text": "Initially, 0.500 M of N2O4 is placed in a reaction flask. At equilibrium, the concentration of NO2 is found to be 0.150 M. Calculate the equilibrium constant, Kc, for the reaction N2O4(g) <=> 2NO2(g).",
   "givens": {"N2O4_0": (0.500, "M"), "NO2_eq": (0.150, "M")}, "init_M": [0.500, 0.0], "prod_eq": 0.150, "ask": "K"},
  {"id": "hi_ps",      "mode": "perfectSquare", "rxn": "H₂ + I₂ ⇌ 2HI", "species": ["H₂", "I₂", "HI"], "coef": [1, 1, 2], "side": [-1, -1, 1],
   "text": "A mixture of 0.200 M H2 and 0.200 M I2 is allowed to reach equilibrium at a certain temperature. If the equilibrium constant, Kc, is 49.0 for the reaction H2(g) + I2(g) <=> 2HI(g), what is the equilibrium concentration of HI in M?",
   "givens": {"H2_0": (0.200, "M"), "I2_0": (0.200, "M"), "K": (49.0, "")}, "init_M": [0.200, 0.200, 0.0], "K": 49.0, "ask": "product"},
  {"id": "pcl5_quad2", "mode": "quadratic", "rxn": "PCl₅ ⇌ PCl₃ + Cl₂", "species": ["PCl₅", "PCl₃", "Cl₂"], "coef": [1, 1, 1], "side": [-1, 1, 1],
   "text": "At a certain temperature, the equilibrium constant Kc for the decomposition of phosphorus pentachloride, PCl5(g) <=> PCl3(g) + Cl2(g), is 0.025. If the initial concentration of PCl5 is 0.100 M with no products present, what is the equilibrium concentration of PCl3 in M?",
   "givens": {"PCl5_0": (0.100, "M"), "K": (0.025, "")}, "init_M": [0.100, 0.0, 0.0], "K": 0.025, "ask": "product"},
]

# ---- words that mark a particle-level account in this chapter. DRAFT.
MECHANISM_WORDS = ["molecul", "particl", "atom", "ion", "collid", "collis", "forward", "reverse", "rate", "recombin",
                   "decompos", "dissociat", "associat", "equal", "same pace", "both direction", "energ", "bond"]

# ---- DRAFT: the unnamed Equations list the student picks from. One fits; the others are look-alikes from nearby chapters.
EQUATION_PICKS = [
  {"id": "eq_k",  "text": "K = [C]^c [D]^d / ( [A]^a [B]^b )",         "fits": KINDS},
  {"id": "eq_kp", "text": "Kp = Kc (RT)^Δn",                             "fits": []},
  {"id": "eq_q",  "text": "Q = [C]₀^c [D]₀^d / ( [A]₀^a [B]₀^b )",      "fits": []},
  {"id": "eq_g",  "text": "ΔG° = −RT ln K",                              "fits": []},
  {"id": "eq_r",  "text": "rate = k [A]^m [B]^n",                         "fits": []},
  {"id": "eq_ph", "text": "pH = −log[H₃O⁺]",                             "fits": []},
]

# ---- constants a student may restate. 1 and 2 are the coefficients; nothing else is harmless here (0 is the INITIAL_IN_K trap).
CONSTANTS = [{"label": "one", "value": 1.0, "unit": "", "abs_tol": 1e-9}, {"label": "two", "value": 2.0, "unit": "", "abs_tol": 1e-9}]

# ---- the chemistry: equilibrium concentrations from the change x.  (V2 SOLVERS.ice, rewritten in one place)
def solve(P):
    a0, coef, side = P["init_M"][0], P["coef"], P["side"]
    rc = coef[0]; pidx = [i for i, s in enumerate(side) if s > 0]; ridx = [i for i, s in enumerate(side) if s < 0]
    if P["mode"] == "findK":
        x = P["prod_eq"] / coef[pidx[0]]
    elif P["mode"] == "perfectSquare":
        r = math.sqrt(P["K"]); pc = coef[pidx[0]]
        x = r * a0 / (pc + r * rc)                      # (pc x)^pc... for the shipped problems the exponents on each side are equal
    else:                                               # quadratic: K = x^2 / (a0 - x)
        K = P["K"]; x = (-K + math.sqrt(K * K + 4 * K * a0)) / 2
    eq = [P["init_M"][i] + side[i] * coef[i] * x for i in range(len(side))]
    num = 1.0
    for i in pidx: num *= eq[i] ** coef[i]
    den = 1.0
    for i in ridx: den *= eq[i] ** coef[i]
    K = num / den if P["mode"] == "findK" else P["K"]
    return {"x": x, "eq": eq, "K": K, "pidx": pidx, "ridx": ridx}

# ---- grading windows. INSTRUCTOR: 2 % on concentrations and on K (V2 used 2 % relative throughout).
def window(value): return max(0.02 * abs(value), 1e-4)

def E(state, label, value, unit, **kw):
    d = {"state": state, "label": label, "value": round_sig(value, 6), "unit": unit, "abs_tol": round_sig(window(value), 3)}
    d.update(kw); return d

def _fmt_coef(c): return "" if c == 1 else str(c)
def _sym(c, sign, x="x"):
    return ("-" if sign < 0 else "+") + _fmt_coef(c) + x

def make_fixed(rng, fid):
    P = [f for f in FIXED if f["id"] == fid][0]; S = solve(P)
    sp, coef, side, init = P["species"], P["coef"], P["side"], P["init_M"]
    pidx, ridx = S["pidx"], S["ridx"]
    asked = pidx[0] if P["ask"] == "product" else None
    # ---- the ICE table the student must produce. I row numbers; C and E rows are symbolic in x. Checked by substitution.
    table = {"species": sp, "rows": {
        "I": [f"{v:g}" for v in init],
        "C": [_sym(coef[i], side[i]) for i in range(len(sp))],
        "E": [(f"{init[i]:g} {'-' if side[i] < 0 else '+'} {_fmt_coef(coef[i])}x") if init[i] else _fmt_coef(coef[i]) + "x" for i in range(len(sp))]}}
    # ---- every number a student can legitimately produce
    expected = []
    if any(u == "mol" for _, u in P["givens"].values()):      # moles and litres given: the initial concentration is a step
        for i in ridx: expected.append(E("initial_M", f"initial [{sp[i]}]", init[i], "M"))
    key_val = S["K"] if P["ask"] == "K" else S["eq"][asked]
    answer_is_x = P["ask"] == "product" and coef[asked] == 1  # then x IS the answer: one item, not two
    if not answer_is_x: expected.append(E("x_found", "the change x", S["x"], "M"))
    for i in range(len(sp)):                                   # other equilibrium concentrations, when they are distinct numbers
        if P["ask"] == "product" and i == asked: continue
        if P["ask"] == "product" and abs(S["eq"][i] - key_val) <= 3 * window(key_val): continue
        expected.append(E("eq_M", f"equilibrium [{sp[i]}]", S["eq"][i], "M"))
    if P["ask"] == "K":
        expected.append(E("value_found", "Kc", S["K"], "", role="key", require_unit=False))
    else:
        expected.append(E("value_found", f"equilibrium [{sp[asked]}]", key_val, "M", role="key", role_note="", require_unit=True))
    for e in expected: e.setdefault("role", "intermediate"); e.pop("role_note", None)
    # ---- traps (instructor's STUDENT_TRAPS.txt, chapter 13; values as V2 computed them)
    a0 = init[0]; traps = []
    key_state = "value_found"
    if P["mode"] == "quadratic":
        K = P["K"]; x_oo = (a0 + math.sqrt(a0 * a0 + 4 * K * a0)) / 2         # x^2/a0 - x = K, read without brackets
        traps.append({"id": "ORDER_OF_OPERATIONS", "state": key_state, "value": round_sig(x_oo, 5), "unit": "M", "abs_tol": round_sig(window(x_oo), 3)})
    if P["mode"] == "perfectSquare" and coef[pidx[0]] > 1:
        r = math.sqrt(P["K"]); x_ns = r * a0 / (1 + r * coef[0])             # x where (2x) belonged
        traps.append({"id": "COEFFICIENT_NOT_SQUARED", "state": key_state, "value": round_sig(x_ns * coef[pidx[0]], 5), "unit": "M", "abs_tol": round_sig(window(x_ns), 3)})
        traps.append({"id": "COEFFICIENT_NOT_SQUARED", "state": "x_found", "value": round_sig(x_ns, 5), "unit": "M", "abs_tol": round_sig(window(x_ns), 3)})
    if P["mode"] == "findK":
        traps.append({"id": "INITIAL_IN_K", "state": key_state, "value": 0.0, "unit": "", "abs_tol": 1e-9})   # products start at zero
    # conservation: a bound, not a value. x and a leftover reactant cannot exceed a0; a product may, by its coefficient.
    bound = a0 * (coef[asked] if P["ask"] == "product" else 1.0)
    if P["ask"] != "K": traps.append({"id": "EXCEEDS_INITIAL", "state": key_state, "above": round_sig(bound * 1.02, 5), "unit": "M"})
    if not answer_is_x: traps.append({"id": "EXCEEDS_INITIAL", "state": "x_found", "above": round_sig(a0 * 1.02, 5), "unit": "M"})
    if answer_is_x: traps = [t for t in traps if t["state"] != "x_found"]
    # ---- the step map (DRAFT structure; the instructor's moves file supplies every word)
    is_findK = P["mode"] == "findK"
    board = [
      {"state": "account_given",   "kind": "text",      "register": "submicro",  "requires": []},
      {"state": "relation_chosen", "kind": "pick",      "register": "symbolic",  "requires": ["account_given"], "options_from": "equation_picks", "pin": True},
      {"state": "approach",        "kind": "pick",      "register": "symbolic",  "requires": ["relation_chosen"],
       "options": [{"id": "approach:findK", "text": "Equilibrium amounts are measured; find K from them."},
                   {"id": "approach:solveX", "text": "K is known; find the equilibrium amounts from it."}],
       "right": ["approach:findK" if is_findK else "approach:solveX"],
       "branch": {"approach:findK": ["x_found", "value_found"] if not answer_is_x else ["value_found"],
                  "approach:solveX": ["method", "expression_set", "x_found", "value_found"] if not answer_is_x else ["method", "expression_set", "value_found"]}},
      {"state": "table",           "kind": "table",     "register": "symbolic",  "requires": ["approach"], "pin": True, "explicit": True},
      {"state": "method",          "kind": "pick",      "register": "symbolic",  "requires": ["table"],
       "options": [{"id": "method:sqrt", "text": "Both sides are perfect squares: take the square root of both."},
                   {"id": "method:quadratic", "text": "Clear the denominator and use the quadratic formula."},
                   {"id": "method:smallx", "text": "x is small next to the starting amount: drop it from the denominator."}],
       "right": ["method:sqrt", "method:quadratic"] if P["mode"] == "perfectSquare" else ["method:quadratic"]},
      {"state": "expression_set",  "kind": "equation",  "register": "symbolic",  "requires": ["table"], "explicit": True, "pin": True},
      {"state": "x_found",         "kind": "number",    "register": "symbolic",  "requires": ["table"] if is_findK else ["expression_set"], "rule": "all"},
      {"state": "value_found",     "kind": "number",    "register": "macro",     "requires": ["x_found"] if not answer_is_x else (["table"] if is_findK else ["expression_set"]), "rule": "all"},
      # (a "direction" prediction item stood here; the instructor deleted it, 8 Oct. The kind remains available in the shell.)
      {"state": "meaning_given",   "kind": "text",      "register": "inference", "requires": ["value_found"], "credit_gate": True},
      {"state": "reflection",      "kind": "reflection","register": "inference", "requires": ["meaning_given"]},
    ]
    if answer_is_x: board = [b for b in board if b["state"] != "x_found"]
    # ---- the expression check: K = f(x) with this problem's starting amounts written in. (equation engine, by substitution)
    eq_checks = [] if is_findK else [expression_check(P, S)]
    return {"kind": P["mode"], "fixed_id": P["id"], "context": {"reaction": P["rxn"], "ask": P["ask"]}, "text": P["text"],
            "givens": {k: {"value": v, "unit": u} for k, (v, u) in P["givens"].items()},
            "board": board, "targets": expected, "traps": traps, "table": table, "eq_checks": eq_checks,
            "reveal_with_problem": None, "sim": None}

def expression_check(P, S):
    """States for the equation engine: K and x that satisfy K = prod(eq)^c / prod(react)^c with THIS problem's
    starting concentrations as literals. The student types e.g. `K = x^2 / (0.80 - x)`. Bent sets name the error."""
    a0, coef, side, init = P["init_M"][0], P["coef"], P["side"], P["init_M"]
    def states(form):
        out = []
        for x in (0.3 * a0, 0.5 * a0, 0.7 * a0):
            out.append({"x": round_sig(x, 9), "K": round_sig(form(x), 9)})
        return out
    def true_form(x):
        num = 1.0; den = 1.0
        for i, s in enumerate(side):
            v = init[i] + s * coef[i] * x
            if s > 0: num *= v ** coef[i]
            else: den *= v ** coef[i]
        return num / den
    pidx = [i for i, s in enumerate(side) if s > 0]; pc = coef[pidx[0]]
    bent = {}
    if pc > 1:
        def not_squared(x):                                    # 2x^2 in place of (2x)^2
            num = 1.0; den = 1.0
            for i, s in enumerate(side):
                v = init[i] + s * coef[i] * x
                if s > 0: num *= coef[i] * x ** coef[i]
                else: den *= v ** coef[i]
            return num / den
        bent["EQ_COEFFICIENT_NOT_SQUARED"] = states(not_squared)
    if len(pidx) == 2 and all(coef[i] == 1 for i in range(len(coef))) and len(side) == 3:
        pass
    if P["mode"] == "quadratic":
        bent["EQ_ORDER_OF_OPERATIONS"] = states(lambda x: x * x / a0 - x)   # x^2/a0 - x
    return {"state": "expression_set", "unknown": "K", "true": states(true_form), "alt": [], "bent": bent,
            "literal_for": {"K": P["K"]},                      # "49 = (2x)^2/(0.2-x)^2" is read as "K = ..."
            "park_text": "K = " + " · ".join(f"({init[i]:g} + {coef[i]}x)^{coef[i]}" if init[i] else f"({coef[i]}x)^{coef[i]}" for i, s in enumerate(side) if s > 0)
                       + " / ( " + " · ".join(f"({init[i]:g} - {coef[i]}x)^{coef[i]}" for i, s in enumerate(side) if s < 0) + " )"}

# ---- how a typed expression is read. Students write x and K; coefficients and starting amounts are numbers.
EQUATION_SYMBOLS = {"x": ["x"], "K": ["Kc", "K_c", "Keq", "K"]}
EQUATION_CONSTANTS = {}

# ---- DRAFT. What the tutor is told, and what is asked if the model is unavailable, when a trap appears.
#      Wording follows V2's TRAPS["ch13_ice"].say and the instructor's STUDENT_TRAPS.txt.
TRAP_NOTES = {
  "EXCEEDS_INITIAL":            {"note": "Their answer is larger than the amount they started with, so more reactant was consumed than existed. Impossible whatever the algebra did.",
                                 "ask": "Compare your number with the amount you started with. Can more react away than was there?"},
  "ORDER_OF_OPERATIONS":        {"note": "Their number is what x^2/a0 - x gives when the denominator is not bracketed: (x^2/a0) - x, a different equation.",
                                 "ask": "Say out loud what is on the bottom of your fraction. How would you have to write it so a calculator reads the same thing?"},
  "COEFFICIENT_NOT_SQUARED":    {"note": "They used x where the expression needs the coefficient: (2x) squared, not x squared.",
                                 "ask": "How many product molecules does one reaction event make, and where does that number go in the expression?"},
  "INITIAL_IN_K":               {"note": "They put the initial concentrations into the equilibrium expression. The products start at zero, so K came out zero.",
                                 "ask": "Which row of your table belongs in the equilibrium expression, and why that one?"},
  "EQ_COEFFICIENT_NOT_SQUARED": {"note": "Their expression holds only with 2x squared read as 2·x², not (2x)².",
                                 "ask": "What is being squared in the numerator: x, or the whole concentration of the product?"},
  "EQ_ORDER_OF_OPERATIONS":     {"note": "Their expression holds only when read as (x²/a0) − x: the denominator was not bracketed.",
                                 "ask": "Which terms are in the denominator of your expression, and does your line say so?"},
}

# the instructor's problem sentences are V2's pool, verbatim; nothing is rendered.
def render_text(*a): raise NotImplementedError("fixed problems carry their own text")
