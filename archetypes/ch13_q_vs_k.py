"""Chapter 13: Q versus K, which way a mixture must move. Fixed problems (the instructor, 13 Oct 2026: equilibrium problems are
fixed text; fixed is the default for every new archetype from here on). A separate archetype from ch13_ice (instructor, 12 Oct);
its scenarios do not reuse the Haber-Bosch and water-gas shift scenarios (decisions on record, 13 Oct).

Step map, one kind (`q_vs_k`):
  account_given -> relation_chosen (the Q expression, a pick) -> [conc_found, only when amounts are in moles and V is not 1 L]
  -> Q_found (a number, asked for by name after the expression) -> shift_predicted (the `direction` kind: forward | reverse |
  neither, checked against Q and K) -> meaning_given -> reflection.

PLACEHOLDERS. The problems below are V2's Q-versus-K problems (docs/09_CH13_SCENARIOS_AS_THEY_STAND.md), status DRAFT, so the
harness and the tests have something to walk. They are not attached to any scenario (content_ch13_q_vs_k_openers.csv has no row),
so the factory ships no variant for this archetype until SCENARIO_CLAUDE's problems and openers arrive and the instructor
approves them. Every constant lives in archetypes/data/reactions.json with its source; the V2 values are marked "source needed".
Every number is declared from the problem data (`FIXED`) and re-derived separately in test_ch13_q_vs_k.py.
"""
import json, os
from engine import round_sig

ID = "ch13_q_vs_k"
TITLE = "Q versus K: which way the reaction goes"
RELATION_TEXT = "Q = [products]^coefficients / [reactants]^coefficients, at any moment; compare Q with K"
NOTEBOOK_URL = "https://notebook.google.com/notebook/6458f208-db32-496a-8088-fe0c1c6cd539"   # INSTRUCTOR: the course notebook
KINDS = ["q_vs_k"]

_RX = json.load(open(os.path.join(os.path.dirname(__file__), "data", "reactions.json"), encoding="utf-8"))["reactions"]

def _rxn(rid, species, coef, side, names):
    r = _RX[rid]
    return {"id": rid, "species": species, "coef": coef, "side": side, "K": r["Kc"], "names": names, "equation": r["equation"]}

# ---- reactions used by the placeholder problems (replace with SCENARIO_CLAUDE's; keep every constant in reactions.json)
HI   = _rxn("hi_formation",       ["H2", "I2", "HI"],        [1, 1, 2],  [-1, -1, 1],     ["hydrogen", "iodine", "hydrogen iodide"])
N2O4 = _rxn("n2o4_dissociation",  ["N2O4", "NO2"],           [1, 2],     [-1, 1],         ["dinitrogen tetroxide", "nitrogen dioxide"])
SO3  = _rxn("so3_formation",      ["SO2", "O2", "SO3"],      [2, 1, 2],  [-1, -1, 1],     ["sulfur dioxide", "oxygen", "sulfur trioxide"])
MEOH = _rxn("methanol_synthesis", ["CO", "H2", "CH3OH"],     [1, 2, 1],  [-1, -1, 1],     ["carbon monoxide", "hydrogen", "methanol"])

# ---- the problems. conc: concentrations in M in reaction order (V = 1 L means no concentration step); status DRAFT until approved.
#      family: A = all species present, Q < K | B = Q > K | C = a product absent (Q = 0) | D = a reactant absent (no Q) | E = Q = K
def _p(fid, rx, conc, text, family, V=1.0, mol=None, status="DRAFT (V2 placeholder; SCENARIO_CLAUDE replaces)"):
    return {"id": fid, "rxn": rx, "kind": "q_vs_k", "V": V, "conc": conc, "mol": mol, "text": text, "family": family, "version": "", "status": status}
FIXED = [
  _p("Q1", HI,   [0.50, 0.50, 3.0],     "For H2(g) + I2(g) ⇌ 2HI(g), Kc = 54.3 at 430 °C. At a given moment, [H2] = 0.50 M, [I2] = 0.50 M and [HI] = 3.0 M. In which direction will the reaction shift?", "A"),
  _p("Q2", N2O4, [0.12, 0.055],         "For N2O4(g) ⇌ 2NO2(g), Kc = 0.211 at 100 °C. Analysis shows [N2O4] = 0.12 M and [NO2] = 0.055 M. Predict the shift direction.", "A"),
  _p("Q3", SO3,  [0.020, 0.010, 0.050], "For 2SO2(g) + O2(g) ⇌ 2SO3(g), Kc = 280 at this temperature. If [SO2] = 0.020 M, [O2] = 0.010 M and [SO3] = 0.050 M, find Q and the shift direction.", "B"),
  _p("Q4", MEOH, [0.25, 0.40, 0.80],    "The synthesis of methanol, CO(g) + 2H2(g) ⇌ CH3OH(g), has Kc = 50.0 at this temperature. A mixture holds 0.25 M CO, 0.40 M H2 and 0.80 M CH3OH. Find Q and say which way the reaction moves.", "A"),
]

# ---- words that mark a particle-level account (V2's list for this archetype, kept)
MECHANISM_WORDS = ["molecul", "particl", "collid", "collis", "forward", "reverse", "rate", "recombin", "decompos", "dissociat",
                   "equal", "same pace", "both direction", "fraction", "ratio", "quotient", "more often", "less often"]

# ---- the unnamed Equations list the student picks from. One fits; the others are look-alikes from nearby chapters.
EQUATION_PICKS = [
  {"id": "eq_q",  "text": "Q = [C]₀^c [D]₀^d / ( [A]₀^a [B]₀^b )",      "fits": KINDS},
  {"id": "eq_k",  "text": "K = [C]^c [D]^d / ( [A]^a [B]^b )",         "fits": []},
  {"id": "eq_kp", "text": "Kp = Kc (RT)^Δn",                             "fits": []},
  {"id": "eq_g",  "text": "ΔG = ΔG° + RT ln Q",                           "fits": []},
  {"id": "eq_r",  "text": "rate = k [A]^m [B]^n",                         "fits": []},
  {"id": "eq_ph", "text": "pH = −log[H₃O⁺]",                             "fits": []},
]
CONSTANTS = []        # as in ch13_ice: a bare 1 or 2 here is a quotient, never a harmless restatement

def window(value): return max(0.02 * abs(value), 1e-4)
def E(state, label, value, unit, **kw):
    d = {"state": state, "label": label, "value": round_sig(value, 6), "unit": unit, "abs_tol": round_sig(window(value), 3)}
    d.update(kw); return d

# ---- the chemistry, recomputed from the data (checked independently in test_ch13_q_vs_k.py)
def quotient(rx, conc, exponents=True):
    num = den = 1.0; zero_bottom = False
    for i, s in enumerate(rx["side"]):
        p = rx["coef"][i] if exponents else 1
        if s > 0: num *= conc[i] ** p
        else:
            if conc[i] == 0: zero_bottom = True
            den *= conc[i] ** p
    return None if zero_bottom else num / den
def multipliers_quotient(rx, conc):              # the named error: coefficients multiplied in rather than used as exponents
    num = den = 1.0; zero_bottom = False
    for i, s in enumerate(rx["side"]):
        v = rx["coef"][i] * conc[i]
        if s > 0: num *= v
        else:
            if conc[i] == 0: zero_bottom = True
            den *= v
    return None if zero_bottom else num / den
def direction(rx, conc):                          # +1 forward (toward products), -1 reverse (toward reactants), 0 at equilibrium
    Q = quotient(rx, conc)
    if Q is None: return -1
    return 0 if abs(Q - rx["K"]) <= 1e-9 * max(1.0, rx["K"]) else (1 if Q < rx["K"] else -1)

def _trap(tid, value, state="Q_found"):
    return {"id": tid, "state": state, "value": round_sig(value, 5), "unit": "", "abs_tol": round_sig(window(value), 3)}
def _clear(a, b):                                  # two values the checker can tell apart
    return abs(a - b) > 3 * max(window(a), window(b))

def make_fixed(rng, fid):
    P = [f for f in FIXED if f["id"] == fid][0]; rx = P["rxn"]; sp = rx["species"]
    conc = list(P["conc"]) if P["conc"] is not None else [m / P["V"] for m in P["mol"]]
    d = direction(rx, conc); Q = quotient(rx, conc)
    expected, traps = [], []
    has_conc = P["mol"] is not None and P["V"] != 1.0
    if has_conc:
        for i in range(len(sp)): expected.append(E("conc_found", f"starting [{sp[i]}]", conc[i], "M", role="intermediate", require_unit=True))
    # Q is a pure number asked for by name once the expression is picked (`after`), so a bare number typed earlier is not read as Q,
    # and a Q equal to K (family E) is not thrown away as a restated given
    if Q is not None:
        expected.append(E("Q_found", "Q at this moment", Q, "", role="key", require_unit=False, after="conc_found" if has_conc else "relation_chosen"))
        # named errors as values (errors file: SCENARIO_CLAUDE writes the asks); each kept only when it is clearly not Q or another trap
        cands = []
        if Q > 0: cands.append(("Q_INVERTED", 1.0 / Q))
        qm = multipliers_quotient(rx, conc)
        if qm is not None and any(c > 1 for c in rx["coef"]): cands.append(("COEFFICIENTS_AS_MULTIPLIERS", qm))
        qe = quotient(rx, conc, exponents=False)
        if qe is not None and any(c > 1 for c in rx["coef"]): cands.append(("EXPONENTS_DROPPED", qe))
        for tid, val in cands:
            if _clear(val, Q) and all(_clear(val, t["value"]) for t in traps): traps.append(_trap(tid, val))
    more = rx["names"][next(i for i, s in enumerate(rx["side"]) if s > 0)]      # the first product, named in the options
    # option texts start with a bare word (forward | reverse | neither): the shell reads that word alone when the student types it
    shift_opts = [{"id": "direction:forward", "text": f"forward toward more {more}"},
                  {"id": "direction:reverse", "text": f"reverse toward less {more}"},
                  {"id": "direction:neither", "text": "neither because it is already at equilibrium"}]
    shift_right = "direction:forward" if d > 0 else ("direction:reverse" if d < 0 else "direction:neither")
    board = [
      {"state": "account_given",   "kind": "text",      "register": "submicro", "requires": []},
      {"state": "relation_chosen", "kind": "pick",      "register": "symbolic", "requires": ["account_given"], "options_from": "equation_picks", "pin": True},
    ]
    prev = "relation_chosen"
    if has_conc: board.append({"state": "conc_found", "kind": "number", "register": "symbolic", "requires": [prev], "rule": "all", "pin": True, "explicit": True}); prev = "conc_found"
    if Q is not None: board.append({"state": "Q_found", "kind": "number", "register": "symbolic", "requires": [prev], "explicit": True, "pin": True}); prev = "Q_found"
    board += [
      {"state": "shift_predicted", "kind": "direction",  "register": "macro",     "requires": [prev], "options": shift_opts, "right": [shift_right], "explicit": True, "pin": True},
      {"state": "meaning_given",   "kind": "text",       "register": "inference", "requires": ["shift_predicted"], "credit_gate": True},
      {"state": "reflection",      "kind": "reflection", "register": "inference", "requires": ["meaning_given"]},
    ]
    givens = {f"c_{sp[i]}": {"value": conc[i], "unit": "M"} for i in range(len(sp)) if conc[i]} if not has_conc else \
             {f"n_{sp[i]}": {"value": P["mol"][i], "unit": "mol"} for i in range(len(sp)) if P["mol"][i]}
    if has_conc: givens["V"] = {"value": P["V"], "unit": "L"}
    givens["Kc"] = {"value": rx["K"], "unit": ""}
    sim_params = {f"c{sp[i]}": conc[i] for i in range(len(sp))}; sim_params["Kc"] = rx["K"]
    return {"kind": P["kind"], "fixed_id": P["id"], "version": P["version"], "status": P["status"],
            "context": {"reaction": rx["id"], "family": P["family"], "direction": d, "Q": None if Q is None else round_sig(Q, 6)},
            "text": P["text"], "givens": givens, "board": board, "targets": expected, "traps": traps,
            "eq_checks": [], "reveal_with_problem": None, "sim": None, "sim_params": sim_params}

EQUATION_SYMBOLS = {"Q": ["Qc", "Q_c", "Q"], "K": ["Kc", "K_c", "Keq", "K"]}
EQUATION_CONSTANTS = {}

# Fallbacks only: the approved asks come from content_ch13_q_vs_k_errors.csv (SCENARIO_CLAUDE, instructor-approved).
TRAP_NOTES = {
  "Q_INVERTED":                 {"note": "Their number is 1/Q: reactants over products.",
                                 "ask": "Which concentrations go on top of the fraction, and which go underneath?"},
  "COEFFICIENTS_AS_MULTIPLIERS": {"note": "Their number comes from multiplying each concentration by its coefficient instead of raising it to that power.",
                                 "ask": "Look at the coefficient on the species with the largest one. In the expression, where does that number go?"},
  "EXPONENTS_DROPPED":          {"note": "Their number is the quotient with every exponent read as 1.",
                                 "ask": "Does every species in the expression carry an exponent of 1 here?"},
}

def render_text(*a): raise NotImplementedError("fixed problems carry their own text")
