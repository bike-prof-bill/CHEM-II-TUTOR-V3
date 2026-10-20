"""Shared pieces for the four chapter 14 archetypes (ch14_ph, ch14_acidbase, ch14_buffer, ch14_titration), 15 Oct 2026, after the
instructor's ruling that chapter 14 keeps its four archetypes so no concept is missed. Constants from archetypes/data/acids_bases.json
(OpenStax first; SCENARIO_CLAUDE holds the appendices). The 5 % rule decides the method, as the text does (the instructor teaches
c > 100·K; "follow the text").
"""
import json, os, math
from engine import round_sig
from _equilibrium import solve_x, quadratic_roots, x_max

_D = json.load(open(os.path.join(os.path.dirname(__file__), "data", "acids_bases.json"), encoding="utf-8"))
KW = _D["Kw"]["value"]
NOTEBOOK_URL = "https://notebook.google.com/notebook/6458f208-db32-496a-8088-fe0c1c6cd539"   # INSTRUCTOR: the course notebook
DRAFT = "DRAFT (placeholder from an OpenStax example; SCENARIO_CLAUDE writes the problems)"

def acid(key):
    a = _D["acids"][key]
    return {"id": key, "species": [a["formula"], "H3O+", a["conjugate"]], "coef": [1, 1, 1], "side": [-1, 1, 1], "active": [True] * 3, "K": a["Ka"], "kind": "acid",
            "names": [a["name"], "hydronium ion", a["conjugate_name"]], "words": {"acid": a["name"], "formula": a["formula"], "conjugate": a["conjugate_name"]}, "ion": "H3O+"}
def base(key):
    b = _D["bases"][key]
    return {"id": key, "species": [b["formula"], b["conjugate"], "OH-"], "coef": [1, 1, 1], "side": [-1, 1, 1], "active": [True] * 3, "K": b["Kb"], "kind": "base",
            "names": [b["name"], b["conjugate_name"], "hydroxide ion"], "words": {"base": b["name"], "formula": b["formula"], "conjugate": b["conjugate_name"]}, "ion": "OH-"}
def strong(formula):
    s = _D["strong"][formula]; return dict(s, formula=formula)

def pH_of(h): return -math.log10(h)
def window(value):                              # 2 %, or half a unit in the second significant figure, whichever is wider (pH 2.88 for 2.875)
    if value == 0: return 1e-4
    return max(0.02 * abs(value), 0.5 * 10 ** (math.floor(math.log10(abs(value))) - 1))
PH_TOL = 0.03                                   # a pH or pOH is read to two decimals: 2.87 or 2.88 for 2.875; a 2 % window would be 0.1 on a log scale, too wide
def is_ph_state(state): return state in ("pH_found", "pOH_found") or state.startswith("pH_after")
def tol_for(state, value): return PH_TOL if is_ph_state(state) else round_sig(window(value), 3)
def E(state, label, value, unit, **kw):
    d = {"state": state, "label": label, "value": round_sig(value, 6), "unit": unit, "abs_tol": tol_for(state, value)}
    d.update(kw); return d
def trap(tid, value, state, unit=""): return {"id": tid, "state": state, "value": round_sig(value, 5), "unit": unit, "abs_tol": tol_for(state, value)}
def clear(a, b, state=None): tol = (lambda v: PH_TOL) if (state and is_ph_state(state)) else window; return abs(a - b) > 3 * max(tol(a), tol(b))
def keep_clear(traps, expected):                # a trap survives only where it is clearly not the right value of its step
    return [t for t in traps if t and ("value" not in t or all(clear(t["value"], e["value"], t["state"]) for e in expected if e["state"] == t["state"]))]
def g(v): return f"{v:.4g}" if v else "0"
def opts(prefix, what, named=None):           # rises | falls | unchanged: the bare first word is what a student may type
    out = [{"id": f"{prefix}:rises", "text": f"rises: the {what} goes up"}, {"id": f"{prefix}:falls", "text": f"falls: the {what} goes down"},
           {"id": f"{prefix}:unchanged", "text": f"unchanged: the {what} stays the same"}]
    for o in out:
        tid = (named or {}).get(o["id"].split(":")[1])
        if tid: o["names"] = tid
    return out
def direction_item(state, prefix, what, answer, named, requires):
    if answer in (named or {}).values(): raise RuntimeError(f"{state}: names the right answer as an error")
    return {"state": state, "kind": "direction", "register": "macro", "requires": [requires], "options": opts(prefix, what, named), "right": [f"{prefix}:{answer}"], "explicit": True, "pin": True}

METHOD_OPTIONS = [{"id": "method:smallx", "text": "x is small next to the starting concentration: drop it from the denominator, then check."},
                  {"id": "method:quadratic", "text": "Clear the denominator and use the quadratic formula."},
                  {"id": "method:sqrt", "text": "Both sides are perfect squares: take the square root of both."},
                  {"id": "method:solver", "text": "The equation is quartic: a graph or a computer solver."}]

def weak_solution(rx, c):
    """A weak acid or base at formal concentration c: x by the exact quadratic, the small-x estimate, the 5 % verdict, pH and pOH."""
    conc = [c, 0.0, 0.0]; K = rx["K"]
    x = solve_x(rx, conc, 1); x_small = math.sqrt(K * c); approx_ok = x_small / c < 0.05
    h = x if rx["kind"] == "acid" else KW / x; pH = pH_of(h); pOH = 14 - pH; percent = 100 * x / c
    return {"x": x, "x_small": x_small, "approx_ok": approx_ok, "pH": pH, "pOH": pOH, "percent": percent, "conc": conc}

def ice_table(rx, c):
    return {"species": rx["species"], "rows": {"I": [g(c), "0", "0"], "C": ["-x", "+x", "+x"], "E": [f"{g(c)} - x", "x", "x"]},
            "named": [{"id": "CHANGE_SIGNS_REVERSED", "row": "C", "cells": ["+x", "-x", "-x"]}, {"id": "WATER_IN_TABLE", "row": "I", "cells": [g(c), "0", "0", "55.5"]}], "zero_species": [1, 2]}

def expression_check_k(rx, c, K=None, symbol="K"):
    """K = x·x/(c − x), x the one unknown; the bent form writes water in as 55.5 M."""
    K = rx["K"] if K is None else K; conc = [c, 0.0, 0.0]; xm = x_max(rx, conc, 1)
    def states(form): return [{"x": round_sig(x, 9), "K": round_sig(form(x), 9)} for x in (0.15 * xm, 0.35 * xm, 0.55 * xm)]
    return {"state": "expression_set", "unknown": "K", "true": states(lambda x: x * x / (c - x)), "alt": [], "bent": {"WATER_IN_EXPRESSION": states(lambda x: x * x / ((c - x) * 55.5))},
            "literal_for": {"K": K}, "park_text": f"{K:.3g} = x · x / ({g(c)} - x)"}

def weak_chain(rx, c, expected, traps, board, requires, pH_key=True, K=None):
    """The ICE work for a weak acid or base: table -> expression -> method -> x -> (pOH) -> pH -> percent -> the 5 % check. Appends to
    expected, traps, board; returns (last state, the solution dict, table, eq_check)."""
    w = weak_solution(dict(rx, K=K) if K else rx, c); K = K or rx["K"]; ion = rx["ion"]; is_acid = rx["kind"] == "acid"
    expected.append(E("x_found", f"x = [{ion}]", w["x"], "M", role="intermediate", require_unit=True))
    if not is_acid: expected.append(E("pOH_found", "pOH", w["pOH"], "", role="intermediate", require_unit=False, after="x_found"))
    expected.append(E("pH_found", "pH", w["pH"], "", role="key" if pH_key else "intermediate", require_unit=False, after="pOH_found" if not is_acid else "x_found"))
    expected.append(E("percent_found", "percent ionised (out of 100)", w["percent"], "", role="intermediate", require_unit=False, after="pH_found"))
    traps += [trap("SQRT_FORGOTTEN", K * c, "x_found", "M"), trap("PH_FROM_FORMAL_CONCENTRATION", pH_of(c) if is_acid else 14 - pH_of(c), "pH_found"),
              trap("PKA_TYPED_AS_PH", -math.log10(K), "pH_found"), trap("PERCENT_AS_FRACTION", w["x"] / c, "percent_found")]
    if not w["approx_ok"]: traps.append(trap("SMALL_X_WHEN_IT_FAILS", w["x_small"], "x_found", "M"))
    traps.append({"id": "EXCEEDS_INITIAL", "state": "x_found", "above": round_sig(c * 1.02, 5), "unit": "M"})
    board += [{"state": "table", "kind": "table", "register": "symbolic", "requires": [requires], "pin": True, "explicit": True},
              {"state": "expression_set", "kind": "equation", "register": "symbolic", "requires": ["table"], "explicit": True, "pin": True},
              {"state": "method", "kind": "pick", "register": "symbolic", "requires": ["expression_set"], "options": METHOD_OPTIONS, "right": ["method:smallx"] if w["approx_ok"] else ["method:quadratic"]},
              {"state": "x_found", "kind": "number", "register": "symbolic", "requires": ["method"], "explicit": True}]
    prev = "x_found"
    if not is_acid: board.append({"state": "pOH_found", "kind": "number", "register": "symbolic", "requires": [prev], "explicit": True}); prev = "pOH_found"
    board += [{"state": "pH_found", "kind": "number", "register": "macro", "requires": [prev], "explicit": True, "pin": True},
              {"state": "percent_found", "kind": "number", "register": "macro", "requires": ["pH_found"], "explicit": True},
              {"state": "approx_checked", "kind": "pick", "register": "symbolic", "requires": ["percent_found"],
               "options": [{"id": "approx:holds", "text": "holds: less than 5 % ionised, so dropping x was fine"}, {"id": "approx:fails", "text": "fails: more than 5 % ionised, so the quadratic was needed"}],
               "right": ["approx:holds" if w["approx_ok"] else "approx:fails"], "explicit": True}]
    return "approx_checked", w, ice_table(rx, c), expression_check_k(rx, c, K)

def hh_pH(K, ratio): return -math.log10(K) + math.log10(ratio)

def tail(board, prev):
    board += [{"state": "meaning_given", "kind": "text", "register": "inference", "requires": [prev], "credit_gate": True},
              {"state": "reflection", "kind": "reflection", "register": "inference", "requires": ["meaning_given"]}]

def head():
    return [{"state": "account_given", "kind": "text", "register": "submicro", "requires": []},
            {"state": "relation_chosen", "kind": "pick", "register": "symbolic", "requires": ["account_given"], "options_from": "equation_picks", "pin": True}]

EQ = {
  "ph":  {"id": "eq_ph",  "text": r"\( \mathrm{pH} = -\log[\mathrm{H_3O^+}] \)"},
  "ka":  {"id": "eq_ka",  "text": r"\( K_a = \dfrac{[\mathrm{H_3O^+}][\mathrm{A^-}]}{[\mathrm{HA}]} \)"},
  "kb":  {"id": "eq_kb",  "text": r"\( K_b = \dfrac{[\mathrm{BH^+}][\mathrm{OH^-}]}{[\mathrm{B}]} \)"},
  "hh":  {"id": "eq_hh",  "text": r"\( \mathrm{pH} = \mathrm{p}K_a + \log\dfrac{[\mathrm{A^-}]}{[\mathrm{HA}]} \)"},
  "kw":  {"id": "eq_kw",  "text": r"\( K_w = [\mathrm{H_3O^+}][\mathrm{OH^-}] \)"},
  "kakb": {"id": "eq_kakb", "text": r"\( K_a K_b = K_w \)"},
  "k":   {"id": "eq_k",   "text": r"\( K = \dfrac{[\mathrm{C}]^{c}[\mathrm{D}]^{d}}{[\mathrm{A}]^{a}[\mathrm{B}]^{b}} \)"},
  "g":   {"id": "eq_g",   "text": r"\( \Delta G^\circ = -RT \ln K \)"},
  "exc": {"id": "eq_excess", "text": r"\( [\mathrm{H_3O^+}] \text{ or } [\mathrm{OH^-}] = \dfrac{\text{moles in excess}}{\text{total volume}} \)"},
}
def picks(fits_by_id):
    return [dict(EQ[k], fits=fits_by_id.get(EQ[k]["id"], [])) for k in EQ]

MECHANISM_WORDS = ["molecul", "particl", "ion", "proton", "transfer", "donat", "accept", "collid", "collis", "water", "hydronium", "hydroxide",
                   "forward", "reverse", "rate", "equal", "fraction", "percent", "dissociat", "ioniz", "ionis", "some", "few", "most", "all of", "excess", "left over", "neutral"]

TRAP_NOTES_COMMON = {   # fallbacks only; the approved asks come from each archetype's errors file
  "SQRT_FORGOTTEN":               {"note": "Their x is Ka times c: the square root was not taken.", "ask": "In your expression, what power does x carry on top?"},
  "PH_FROM_FORMAL_CONCENTRATION": {"note": "Their pH comes from the formal concentration, as if every molecule had ionised.", "ask": "What fraction of the molecules have actually given up a proton?"},
  "PKA_TYPED_AS_PH":              {"note": "Their number is -log Ka, the pKa, offered as the pH.", "ask": "Which concentration does pH measure, and is Ka a concentration?"},
  "PERCENT_AS_FRACTION":          {"note": "Their percent is the fraction, not multiplied by 100.", "ask": "Out of a hundred molecules, how many is that?"},
  "SMALL_X_WHEN_IT_FAILS":        {"note": "Their x comes from dropping x in the denominator, but more than 5 % ionised here.", "ask": "Compare your x with the starting concentration. Is it small next to it?"},
  "POH_TYPED_AS_PH":              {"note": "Their number is the pOH offered as the pH.", "ask": "Which ion did you take the logarithm of?"},
  "IONS_PER_FORMULA_IGNORED":     {"note": "Their ion concentration equals the formula concentration though each unit gives more than one ion.", "ask": "How many hydroxide ions does one formula unit release?"},
  "RATIO_INVERTED":               {"note": "Their value uses acid over base.", "ask": "Which concentration goes on top in the relation you picked?"},
  "LOG_FORGOTTEN":                {"note": "Their pH adds the ratio itself to pKa, without the logarithm.", "ask": "What operation sits between pKa and the ratio?"},
  "EXCEEDS_INITIAL":              {"note": "Their x is larger than the starting concentration.", "ask": "Can more ionise than was there?"},
  "WATER_IN_EXPRESSION":          {"note": "Their expression carries water's concentration.", "ask": "Which species in this equilibrium is the solvent, and what happens to its term?"},
  "DILUTION_IONIZATION_FALLS":    {"note": "They predicted a smaller fraction ionised on dilution.", "ask": "With the same Ka and fewer molecules per litre, what must happen to the fraction that ionise?"},
  "CONJUGATE_LOWERS_PH":          {"note": "They predicted the pH falls when the conjugate base is added.", "ask": "The added ion sits on which side of the equation, and which way does that push it?"},
  "CONJUGATE_RAISES_PH":          {"note": "They predicted the pH rises when the conjugate acid is added to the base.", "ask": "The added ion sits on which side of the equation, and which way does that push it?"},
  "BUFFER_PH_FIXED":              {"note": "They predicted no change at all after strong acid or base was added.", "ask": "Something was consumed. Did the ratio of base to acid stay exactly the same?"},
  "ADDED_NOT_CONSUMED":           {"note": "Their new pH treats the added acid or base as if it stayed free in the buffer.", "ask": "What does the added hydroxide meet first in this solution, and what becomes of it?"},
  "PH_7_AT_EQUIVALENCE":          {"note": "They gave pH 7 at the equivalence point of a weak acid.", "ask": "What is in the flask at equivalence, and does that ion leave water alone?"},
  "VOLUME_NOT_TOTALED":           {"note": "Their concentration divides by the original volume, not the total after titrant was added.", "ask": "How much liquid is in the flask now?"},
  "KA_FOR_HYDROLYSIS":            {"note": "Their x at equivalence comes from Ka, but the species there is the conjugate base.", "ask": "Which constant belongs to the conjugate base reacting with water?"},
  "HH_AT_EQUIVALENCE":            {"note": "They used Henderson-Hasselbalch where no acid is left.", "ask": "How much of the acid is left for the ratio?"},
  "MOLES_FROM_ONE_SOLUTION":      {"note": "Their moles ignore one of the two solutions.", "ask": "Which solution supplied the moles you just counted, and which did you leave out?"},
}
