"""Shared pieces for the three chapter 15 archetypes (ch15_ksp, ch15_common_ion, ch15_qsp), 16 Oct 2026, prepared for SCENARIO_CLAUDE.
Salts from archetypes/data/salts.json (Appendix J first). A salt M_a X_b dissolves to a M^+ and b X^-; with molar solubility s,
[M] = a s and [X] = b s, so Ksp = (a s)^a (b s)^b = a^a b^b s^(a+b). Every function here is re-derived in test_ch15.py."""
import json, os, math
from engine import round_sig

_D = json.load(open(os.path.join(os.path.dirname(__file__), "data", "salts.json"), encoding="utf-8"))
NOTEBOOK_URL = "https://notebook.google.com/notebook/6458f208-db32-496a-8088-fe0c1c6cd539"   # INSTRUCTOR: the course notebook
DRAFT = "DRAFT (placeholder; SCENARIO_CLAUDE writes the problems)"

def salt(formula):
    s = dict(_D["salts"][formula]); s["formula"] = formula; s["n_ions"] = s["n_cat"] + s["n_an"]
    s["words"] = {"salt": s["name"], "formula": formula, "cation": s["cation"], "anion": s["anion"]}
    return s

def ksp_coefficient(st): return (st["n_cat"] ** st["n_cat"]) * (st["n_an"] ** st["n_an"])         # 1, 4 or 27 for 1:1, 1:2, 2:1
def s_from_ksp(st): return (st["Ksp"] / ksp_coefficient(st)) ** (1.0 / st["n_ions"])             # molar solubility in pure water
def ksp_from_s(st, s): return ksp_coefficient(st) * s ** st["n_ions"]
def ions_at(st, s): return st["n_cat"] * s, st["n_an"] * s
def grams_per_litre(st, s): return s * st["molar_mass"]

def s_with_common_ion(st, which, c_common):
    """Molar solubility when the solution already holds c_common of the cation ('cation') or anion ('anion'): solved exactly by
    bisection on Ksp = [M]^a [X]^b with [common] = c_common + n s, and the small-s estimate used in the text."""
    a, b = st["n_cat"], st["n_an"]
    def f(s):
        cm = (c_common + a * s) if which == "cation" else a * s
        cx = (c_common + b * s) if which == "anion" else b * s
        return cm ** a * cx ** b
    lo, hi = 0.0, s_from_ksp(st)
    for _ in range(300):
        m = 0.5 * (lo + hi)
        if f(m) < st["Ksp"]: lo = m
        else: hi = m
    exact = 0.5 * (lo + hi)
    if which == "cation": small = (st["Ksp"] / (c_common ** a * b ** b)) ** (1.0 / b)
    else: small = (st["Ksp"] / (c_common ** b * a ** a)) ** (1.0 / a)
    return {"exact": exact, "small": small, "small_ok": (max(a, b) * small) / c_common < 0.05}

def qsp(st, c_cat, c_an): return c_cat ** st["n_cat"] * c_an ** st["n_an"]
def mixed(c1, v1, c2, v2):                                      # concentration of each solute after two solutions are mixed
    vt = v1 + v2; return c1 * v1 / vt, c2 * v2 / vt, vt

def window(value):
    if value == 0: return 1e-4
    return max(0.02 * abs(value), 0.5 * 10 ** (math.floor(math.log10(abs(value))) - 1))
def E(state, label, value, unit, **kw):
    d = {"state": state, "label": label, "value": round_sig(value, 6), "unit": unit, "abs_tol": round_sig(window(value), 3)}; d.update(kw); return d
def trap(tid, value, state, unit=""): return {"id": tid, "state": state, "value": round_sig(value, 5), "unit": unit, "abs_tol": round_sig(window(value), 3)}
def clear(a, b): return abs(a - b) > 3 * max(window(a), window(b))
def keep_clear(traps, expected):
    return [t for t in traps if t and ("value" not in t or all(clear(t["value"], e["value"]) for e in expected if e["state"] == t["state"]))]
def g(v): return f"{v:.3g}" if v else "0"
def head():
    return [{"state": "account_given", "kind": "text", "register": "submicro", "requires": []},
            {"state": "relation_chosen", "kind": "pick", "register": "symbolic", "requires": ["account_given"], "options_from": "equation_picks", "pin": True}]
def tail(board, prev):
    board += [{"state": "meaning_given", "kind": "text", "register": "inference", "requires": [prev], "credit_gate": True},
              {"state": "reflection", "kind": "reflection", "register": "inference", "requires": ["meaning_given"]}]
def opts(prefix, texts, named=None):                    # option texts begin with the bare word the student may type
    out = [{"id": f"{prefix}:{k}", "text": t} for k, t in texts]
    for o in out:
        tid = (named or {}).get(o["id"].split(":")[1])
        if tid: o["names"] = tid
    return out

def ice_table(st, c_common=0.0, which=None):
    """The s table over the two ions (the solid is present and not counted, so it has no column). I row: the common ion's
    concentration if any; C: +a s, +b s. The checker reads s as the unknown (EQUATION_SYMBOLS maps s to x)."""
    a, b = st["n_cat"], st["n_an"]
    i_cat = g(c_common) if which == "cation" else "0"; i_an = g(c_common) if which == "anion" else "0"
    e_cat = (f"{g(c_common)} + {a if a > 1 else ''}s" if which == "cation" else f"{a if a > 1 else ''}s")
    e_an = (f"{g(c_common)} + {b if b > 1 else ''}s" if which == "anion" else f"{b if b > 1 else ''}s")
    return {"species": [st["cation"], st["anion"]], "rows": {"I": [i_cat, i_an], "C": [f"+{a if a > 1 else ''}s", f"+{b if b > 1 else ''}s"], "E": [e_cat, e_an]},
            "named": [{"id": "COEFFICIENT_DROPPED_IN_TABLE", "row": "C", "cells": ["+s", "+s"]}] if max(a, b) > 1 else [], "zero_species": [0, 1] if which is None else ([1] if which == "cation" else [0])}

def expression_check(st, c_common=0.0, which=None):
    """Ksp = (a s)^a (b s)^b, or with the common ion added: true states, and the bent forms (coefficient not an exponent; the solid in)."""
    a, b = st["n_cat"], st["n_an"]; K = st["Ksp"]
    sm = s_from_ksp(st) if which is None else s_with_common_ion(st, which, c_common)["exact"]
    def form(exp_ok, mult_ok):
        def f(s):
            cm = (c_common if which == "cation" else 0.0) + (a if mult_ok else 1) * s
            cx = (c_common if which == "anion" else 0.0) + (b if mult_ok else 1) * s
            return cm ** (a if exp_ok else 1) * cx ** (b if exp_ok else 1)
        return f
    def states(f): return [{"x": round_sig(x, 9), "K": round_sig(f(x), 9)} for x in (0.5 * sm, 1.0 * sm, 1.5 * sm)]   # the unknown is x in the checker; s is its alias
    bent = {}
    if max(a, b) > 1: bent["COEFF_NOT_EXPONENT"] = states(form(False, True)); bent["EXPONENT_NOT_IN_TABLE"] = states(form(True, False))
    cat_t = (f"({g(c_common)} + {a if a > 1 else ''}s)" if which == "cation" else (f"({a}s)" if a > 1 else "s")) + (f"^{a}" if a > 1 else "")
    an_t = (f"({g(c_common)} + {b if b > 1 else ''}s)" if which == "anion" else (f"({b}s)" if b > 1 else "s")) + (f"^{b}" if b > 1 else "")
    return {"state": "expression_set", "unknown": "K", "true": states(form(True, True)), "alt": [], "bent": bent, "literal_for": {"K": K}, "park_text": f"{K:.2g} = {cat_t} · {an_t}"}

EQ = {
  "ksp":  {"id": "eq_ksp",  "text": r"\( K_{sp} = [\mathrm{M^{m+}}]^{a}[\mathrm{X^{x-}}]^{b} \)"},
  "qsp":  {"id": "eq_qsp",  "text": r"\( Q_{sp} = [\mathrm{M^{m+}}]_0^{\,a}[\mathrm{X^{x-}}]_0^{\,b} \)"},
  "k":    {"id": "eq_k",    "text": r"\( K = \dfrac{[\mathrm{C}]^{c}[\mathrm{D}]^{d}}{[\mathrm{A}]^{a}[\mathrm{B}]^{b}} \)"},
  "ka":   {"id": "eq_ka",   "text": r"\( K_a = \dfrac{[\mathrm{H_3O^+}][\mathrm{A^-}]}{[\mathrm{HA}]} \)"},
  "dil":  {"id": "eq_dil",  "text": r"\( M_1 V_1 = M_2 V_2 \)"},
  "g":    {"id": "eq_g",    "text": r"\( \Delta G^\circ = -RT \ln K \)"},
}
def picks(fits_by_id): return [dict(EQ[k], fits=fits_by_id.get(EQ[k]["id"], [])) for k in EQ]

MECHANISM_WORDS = ["ion", "lattice", "crystal", "solid", "dissolv", "precipitat", "settle", "collid", "collis", "water", "surround", "pull", "leave", "return",
                   "forward", "reverse", "rate", "equal", "trade", "exchange", "saturat", "molecul", "particl", "hydrat"]

TRAP_NOTES_COMMON = {
  "COEFF_NOT_EXPONENT":        {"note": "Their expression holds only with every exponent read as 1: the coefficients are in the table but not used as exponents.", "ask": "The coefficients do double duty. What is the exponent for each ion?"},
  "EXPONENT_NOT_IN_TABLE":     {"note": "Their expression has the exponents but the change row reads +s for every ion.", "ask": "A coefficient is an exponent here. Is it also in the change row?"},
  "COEFFICIENT_DROPPED_IN_TABLE": {"note": "Their change row has +s for an ion that forms two per formula unit.", "ask": "How many of that ion does one formula unit release?"},
  "ROOT_FORGOTTEN":            {"note": "Their s is Ksp divided by the coefficient without the root.", "ask": "What power does s carry in your expression?"},
  "COEFFICIENT_FORGOTTEN":     {"note": "Their s is the root of Ksp alone: the 4 or the 27 was left out.", "ask": "What multiplies s to the power in your expression?"},
  "S_FOR_ION":                 {"note": "They gave s where the ion's concentration was asked, though two ions form per formula unit.", "ask": "How many of that ion does each dissolved formula unit put into the water?"},
  "GRAMS_WITHOUT_MOLAR_MASS":  {"note": "Their grams per litre equal the molar solubility: the molar mass was not used.", "ask": "What converts moles per litre into grams per litre?"},
  "COMMON_ION_IGNORED":        {"note": "Their s is the pure-water solubility: the ion already present was not counted.", "ask": "What concentration of that ion was in the water before any solid dissolved?"},
  "SMALL_S_WHEN_IT_FAILS":     {"note": "They dropped s next to the common ion, but s is not small next to it here.", "ask": "Compare your s with the concentration already present. Is it small next to it?"},
  "VOLUME_NOT_TOTALED":        {"note": "Their concentration after mixing divides by one solution's volume, not the total.", "ask": "How much liquid is in the beaker now?"},
  "DILUTION_IGNORED":          {"note": "Their concentration after mixing is the concentration before it.", "ask": "Two solutions were poured together. What happened to each one's concentration?"},
  "Q_INVERTED":                {"note": "Their number is 1/Q.", "ask": "Which concentrations go into Q, and are any divided?"},
  "EXPONENTS_DROPPED":         {"note": "Their Q has every exponent read as 1.", "ask": "Does every ion in the expression carry an exponent of 1 here?"},
  "COEFFICIENTS_AS_MULTIPLIERS": {"note": "Their Q multiplies each concentration by its coefficient instead of raising it to that power.", "ask": "Look at the ion with the coefficient. In the expression, where does that number go?"},
  "PRECIPITATE_WHEN_Q_LESS":   {"note": "They predicted a precipitate although Q is below Ksp.", "ask": "Is the water holding more than it can, or less?"},
  "NO_PRECIPITATE_WHEN_Q_MORE": {"note": "They predicted no precipitate although Q is above Ksp.", "ask": "If Q is larger than Ksp, which way must the ions move?"},
  "SOLUBILITY_RISES_WITH_COMMON_ION": {"note": "They predicted more dissolving when a common ion was added.", "ask": "The added ion sits on which side of the dissolving equation, and which way does that push it?"},
}
