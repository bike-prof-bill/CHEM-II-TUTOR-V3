"""
ch10_cc.py  --  Clausius-Clapeyron.  ARCHETYPE DEFINITION.  All the chemistry-specific parts, one file.
INSTRUCTOR = yours to set.   DRAFT = my placeholder; replace or approve before students see it.
"""
import math
from engine import to_canon, from_canon, solve_for, round_sig
import _substances as _subs

ID    = "ch10_cc"
TITLE = "Clausius-Clapeyron"
RELATION_TEXT = "ln(P2/P1) = -(dHvap/R) * (1/T2 - 1/T1)"
NOTEBOOK_URL  = "https://notebook.google.com/notebook/6458f208-db32-496a-8088-fe0c1c6cd539"
R = 8.314   # J/(mol K)

VARIABLES = {
  "T1": {"kind": "temperature",  "bounds": (150.0, 700.0), "answer_units": ["degC", "K"], "round": {"degC": {"dp": 1}, "K": {"dp": 1}}},
  "T2": {"kind": "temperature",  "bounds": (150.0, 700.0), "answer_units": ["degC", "K"], "round": {"degC": {"dp": 1}, "K": {"dp": 1}}},
  "P1": {"kind": "pressure",     "bounds": (1e-4, 100.0),  "answer_units": ["atm", "torr"], "round": {"atm": {"sig": 3}, "torr": {"sig": 3}}},
  "P2": {"kind": "pressure",     "bounds": (1e-4, 100.0),  "answer_units": ["atm", "torr"], "round": {"atm": {"sig": 3}, "torr": {"sig": 3}}},
  "dH": {"kind": "molar_energy", "bounds": (5e3, 1e5),     "answer_units": ["kJ/mol"], "round": {"kJ/mol": {"sig": 3}, "J/mol": {"sig": 3}}},
}
# Six kinds of problem from one relation. "slope" is the six-measured-points lab form.
KINDS = ["T2", "P2", "T1", "P1", "dH", "slope"]

# ---- INSTRUCTOR: which liquids this archetype's problems may draw, and the coldest temperature a problem may use for each
#      (a teaching choice: how far below the boiling point the questions go; it must sit above the melting point, which the tests check).
#      The physical data (ΔHvap at the normal boiling point, boiling point, melting point) come from the universal table,
#      archetypes/data/substances.json, instructor's NIST values, 9 Oct 2026. Each curve hangs from its normal boiling point (1 atm).
LIQUIDS = [  # name, coldest degC a problem uses
  ("water",                   5.0), ("methanol",             -10.0), ("ethanol",              -10.0), ("1-propanol",      -10.0),
  ("2-propanol",            -10.0), ("1-butanol",            -10.0), ("acetone",              -20.0), ("diethyl ether",   -30.0),
  ("pentane",               -30.0), ("hexane",               -10.0), ("heptane",               10.0), ("cyclohexane",      10.0),
  ("benzene",                10.0), ("toluene",               20.0), ("chloroform",           -10.0), ("carbon tetrachloride", 0.0),
  ("ethyl acetate",           0.0), ("2-butanol",            -10.0), ("isobutyl alcohol",     -10.0),
  ("tert-butyl alcohol",     26.0),   # melts at 25.1 °C: a solid at room temperature
]
# the table this file works from: (name, dHvap kJ/mol at Tb, normal bp degC, coldest degC a problem uses, normal mp degC)
SUBSTANCES = [(n, *_subs.get(n, "dHvap_at_Tb_kJ_mol", "boiling_point_C"), cold, _subs.get(n, "melting_point_C")) for n, cold in LIQUIDS]
P_MIXED_FRACTION = 0.70   # how often the two pressures are shown in different units
T_IN_CELSIUS     = 0.70   # how often a temperature is shown in degC
DH_IN_KJ         = 0.85   # how often dHvap is shown in kJ/mol
ONE_ATM_POINT    = 0.35   # how often one point is the normal boiling point
SPAN_BELOW_BP, SPAN_ABOVE_BP = 60.0, 25.0

# ---- words that mark a particle-level account in this chapter (moved out of the shell, 8 Oct; list unchanged).
MECHANISM_WORDS = ["molecul", "particl", "atom", "ion", "electron", "collid", "collis", "energ", "attract", "escap",
                   "vapor", "vapour", "condens", "surface", "kinetic", "bond", "force", "fraction", "distribut"]

# ---- INSTRUCTOR: the unnamed Equations list the student picks from. `fits` says which kinds it is right for.
EQUATION_PICKS = [
  {"id": "eq_a", "text": "ln(P2/P1) = -(ΔH/R)(1/T2 - 1/T1)", "fits": ["T1", "T2", "P1", "P2", "dH"]},
  {"id": "eq_b", "text": "ln P = -(ΔH/R)(1/T) + C",           "fits": ["slope"]},
  {"id": "eq_c", "text": "ln(k2/k1) = -(Ea/R)(1/T2 - 1/T1)",  "fits": []},
  {"id": "eq_g", "text": "ln(K2/K1) = -(ΔH°/R)(1/T2 - 1/T1)", "fits": []},
  {"id": "eq_d", "text": "PV = nRT",                          "fits": []},
  {"id": "eq_e", "text": "q = m c ΔT",                        "fits": []},
  {"id": "eq_f", "text": "P = X P°",                          "fits": []},
]

def residual(v, flags):
    log  = math.log10 if flags.get("log10") else math.log
    sign = +1.0 if flags.get("sign_flipped") else -1.0
    return log(v["P2"] / v["P1"]) - sign * (v["dH"] / R) * (1.0 / v["T2"] - 1.0 / v["T1"])

def draw_state(rng, liquids=None):
    name, dH_kJ, bp_C, cold_C, mp_C = rng.choice([x for x in SUBSTANCES if not liquids or x[0] in liquids])
    dH, bp = dH_kJ * 1000.0, bp_C + 273.15
    P_at = lambda T: math.exp(-(dH / R) * (1.0 / T - 1.0 / bp))          # atm
    lo, hi = max(cold_C + 273.15, bp - SPAN_BELOW_BP), bp + SPAN_ABOVE_BP
    one_atm = rng.random() < ONE_ATM_POINT
    T1 = bp if one_atm else rng.uniform(lo, hi)
    while True:
        T2 = rng.uniform(lo, hi)
        if abs(T2 - T1) >= 10.0: break
    s = {"T1": T1, "T2": T2, "P1": P_at(T1), "P2": P_at(T2), "dH": dH}
    if rng.random() < 0.5: s["T1"], s["T2"], s["P1"], s["P2"] = s["T2"], s["T1"], s["P2"], s["P1"]
    return s, {"substance": name, "one_atm_point": one_atm, "bp_K": bp, "lo_K": lo, "hi_K": hi}

def pick_unit(rng, name, shown):
    kind = VARIABLES[name]["kind"]
    if kind == "temperature":  return "degC" if rng.random() < T_IN_CELSIUS else "K"
    if kind == "molar_energy": return "kJ/mol" if rng.random() < DH_IN_KJ else "J/mol"
    other = [s["unit"] for n, s in shown.items() if VARIABLES[n]["kind"] == "pressure"]
    if not other: return rng.choice(["atm", "torr"])                       # instructor, 9 Oct: no kPa anywhere in this tutor
    if rng.random() < P_MIXED_FRACTION: return rng.choice([u for u in ("atm", "torr") if u != other[0]])
    return other[0]

def acceptable(full):
    return abs(full["T2"] - full["T1"]) >= 8.0 and 0.003 < full["P1"] < 20 and 0.003 < full["P2"] < 20

# ---- grading windows (instructor, 19 Sept): +/- 1 K on temperatures, 2 % elsewhere.
def window(kind, value): return 1.0 if kind == "temperature" else 0.02 * abs(value)

# ---- THE BOARD for one problem: what must be established, and what must come first.
#      Conversions appear only when this problem's numbers call for them.
def board_for(shown, unknown):
    need = []
    if any(s["unit"] == "degC" for n, s in shown.items() if n in ("T1", "T2")): need.append("T_in_K")
    if "dH" in shown and shown["dH"]["unit"] == "kJ/mol":                        need.append("dH_in_J")
    if "P1" in shown and "P2" in shown and shown["P1"]["unit"] != shown["P2"]["unit"]: need.append("P_same_units")
    b = [{"state": "account_given",   "kind": "text",   "register": "submicro",  "requires": []},
         {"state": "relation_chosen", "kind": "pick",   "register": "symbolic",  "requires": ["account_given"], "options_from": "equation_picks", "pin": True},
         # instructor, 20 Sept: the student HAS TO rearrange for the unknown. `explicit` = never implied by a right number.
         {"state": "rearranged",      "kind": "equation", "register": "symbolic", "requires": ["relation_chosen"], "explicit": True, "pin": True}]
    b += [{"state": s, "kind": "number", "register": "symbolic", "requires": ["account_given"], "pin": True,
           "rule": "any" if s == "P_same_units" else "all"} for s in need]
    b += [{"state": "substituted",   "kind": "number", "register": "symbolic",  "requires": ["rearranged"] + need, "rule": "any"},
          {"state": "value_found",   "kind": "number", "register": "macro",     "requires": ["substituted"], "rule": "all", "opens_sim": True},
          {"state": "meaning_given", "kind": "text",   "register": "inference", "requires": ["value_found"], "credit_gate": True}]
    return b

# ---- constants a student may restate without it meaning anything. Declared, never guessed (rebuild spec, Change 2).
#      Any other number that matches nothing is a stray. The 1 is the 1 in 1/T. R in kJ (0.008314) is not here:
#      it is declared as an alternative form of the dH-in-J step, where restating R in kJ does the same job.
CONSTANTS = [
  {"label": "R",              "value": 8.314,    "unit": "J/(mol·K)"},
  {"label": "R_4sf",          "value": 8.3145,   "unit": "J/(mol·K)"},
  {"label": "R_in_L_atm",     "value": 0.08206,  "unit": ""},
  {"label": "zero_C_in_K",    "value": 273.15,   "unit": "K"},
  {"label": "zero_C_in_K_3sf","value": 273.0,    "unit": "K"},
  {"label": "torr_per_atm",   "value": 760.0,    "unit": ""},
  {"label": "J_per_kJ",       "value": 1000.0,   "unit": ""},
  {"label": "one",            "value": 1.0,      "unit": "", "abs_tol": 1e-9},
  # instructor, 8 Oct: small integers a student writes in prose ("step 2", "two points") are not answers here.
  {"label": "zero",           "value": 0.0,      "unit": "", "abs_tol": 1e-9},
  {"label": "two",            "value": 2.0,      "unit": "", "abs_tol": 1e-9},
  {"label": "three",          "value": 3.0,      "unit": "", "abs_tol": 1e-9},
]

# ---- every number a student can legitimately produce, tied to the board state it establishes.
def T(state, label, value, unit, tol, **kw):
    d = {"state": state, "label": label, "value": round_sig(value, 6), "unit": unit, "abs_tol": round_sig(tol, 3)}
    d.update(kw); return d

def targets_for(full, shown, unknown, ans_unit):
    out = []
    for n in ("T1", "T2"):
        if n in shown and shown[n]["unit"] == "degC":
            out.append(T("T_in_K", f"{n} in K", full[n], "K", 0.2))
    if "dH" in shown and shown["dH"]["unit"] == "kJ/mol":
        out.append(T("dH_in_J", "dHvap in J/mol", full["dH"], "J/mol", 0.005 * full["dH"],
                     also=[{"value": 0.008314, "unit": "", "abs_tol": 0.00002, "label": "R restated in kJ"}]))
    if "P1" in shown and "P2" in shown and shown["P1"]["unit"] != shown["P2"]["unit"]:
        u1, u2 = shown["P1"]["unit"], shown["P2"]["unit"]
        a = from_canon("pressure", u2, full["P1"]); b = from_canon("pressure", u1, full["P2"])
        out.append(T("P_same_units", f"P1 in {u2}", a, u2, 0.01 * a))
        out.append(T("P_same_units", f"P2 in {u1}", b, u1, 0.01 * b))
    ratio = full["P2"] / full["P1"]
    out.append(T("substituted", "P2/P1", ratio, "", 0.015 * ratio))
    out.append(T("substituted", "P1/P2", 1 / ratio, "", 0.015 / ratio))
    out.append(T("substituted", "ln(P2/P1)", math.log(ratio), "", 0.015 * abs(math.log(ratio))))
    dinv = 1 / full["T2"] - 1 / full["T1"]
    out.append(T("substituted", "1/T2 - 1/T1", dinv, "1/K", 0.015 * abs(dinv)))
    out.append(T("substituted", "dHvap/R", full["dH"] / R, "K", 0.015 * full["dH"] / R))
    kind = VARIABLES[unknown]["kind"]
    key = from_canon(kind, ans_unit, full[unknown])
    also = []
    for u in {"temperature": ["K", "degC"], "pressure": ["atm", "torr"], "molar_energy": ["kJ/mol", "J/mol"]}[kind]:
        if u != ans_unit:
            v = from_canon(kind, u, full[unknown]); also.append({"value": round_sig(v, 6), "unit": u, "abs_tol": round_sig(window(kind, v), 3)})
    out.append(T("value_found", unknown, key, ans_unit, window(kind, key), role="key", require_unit=True, also=also))
    return out

# ---- traps: the same relation, bent one way.
def _as_student(known, unknown, ans_unit, swap=None, flags=None):
    lo, hi = VARIABLES[unknown]["bounds"]
    x = solve_for(residual, {**known, **(swap or {})}, unknown, lo / 1000.0, hi * 1000.0, flags)
    return None if x is None else from_canon(VARIABLES[unknown]["kind"], ans_unit, x)
def _celsius(A, shown, known, unknown, ans_unit, key):
    swap = {n: s["value"] for n, s in shown.items() if s["unit"] == "degC"}
    if any(v <= 0 for v in swap.values()): return None
    if unknown in ("T1", "T2"): return solve_for(residual, {**known, **swap}, unknown, 1.0, 5000.0)
    return _as_student(known, unknown, ans_unit, swap=swap)
def _kj(A, shown, known, unknown, ans_unit, key):
    if unknown == "dH": return key * 1000.0
    return _as_student(known, unknown, ans_unit, swap={"dH": shown["dH"]["value"]})
TRAPS = [
  {"id": "CELSIUS_NOT_CONVERTED", "applies": lambda s, u: any(x["unit"] == "degC" for x in s.values()), "value": _celsius},
  {"id": "KJ_WITH_R_IN_J",        "applies": lambda s, u: u == "dH" or s["dH"]["unit"] == "kJ/mol",      "value": _kj},
  {"id": "SIGN_FLIPPED",          "applies": lambda s, u: True, "value": lambda A, s, k, u, au, key: _as_student(k, u, au, flags={"sign_flipped": True})},
  {"id": "LOG10_FOR_LN",          "applies": lambda s, u: True, "value": lambda A, s, k, u, au, key: _as_student(k, u, au, flags={"log10": True})},
  {"id": "PRESSURE_UNITS_MIXED",  "applies": lambda s, u: "P1" in s and "P2" in s and s["P1"]["unit"] != s["P2"]["unit"],
   "value": lambda A, s, k, u, au, key: _as_student(k, u, au, swap={"P1": s["P1"]["value"], "P2": s["P2"]["value"]})},
]

# ---- how a typed equation is read and checked (by substitution, as V2 did; never by matching strings).
EQUATION_SYMBOLS = {            # what the student may type  ->  the variable it means
  "T1": ["T1", "T_1", "t1"], "T2": ["T2", "T_2", "t2"], "P1": ["P1", "P_1", "p1"], "P2": ["P2", "P_2", "p2"],
  "dH": ["ΔHvap", "ΔH_vap", "ΔHv", "ΔH", "dHvap", "dH_vap", "dH", "Hvap", "DHvap", "DH"],
  # the straight-line form:  ln P = m (1/T) + b
  "m": ["slope", "m"], "b": ["intercept", "b"], "P": ["P"], "T": ["Tbp", "T_b", "Tb", "T"],
}
EQUATION_CONSTANTS = {"R": R}
# Shown only if the item is parked. Each is verified by the checker in test_core.js.
REARRANGED = {
  "P2": "P2 = P1 · exp( -(ΔHvap/R)(1/T2 - 1/T1) )",
  "P1": "P1 = P2 / exp( -(ΔHvap/R)(1/T2 - 1/T1) )",
  "T2": "T2 = 1 / ( 1/T1 - (R/ΔHvap)·ln(P2/P1) )",
  "T1": "T1 = 1 / ( 1/T2 + (R/ΔHvap)·ln(P2/P1) )",
  "dH": "ΔHvap = -R·ln(P2/P1) / (1/T2 - 1/T1)",
}
def equation_check(rng, unknown):
    """Random states that satisfy the relation, and sets that satisfy it bent one way.
    A typed equation must hold on every true state. Holding on a bent set names the error."""
    def states(flags):
        out = []
        while len(out) < 3:
            k = {"T1": rng.uniform(260, 420), "T2": rng.uniform(260, 420), "P1": rng.uniform(0.05, 3.0), "dH": rng.uniform(2e4, 5e4)}
            if abs(k["T1"] - k["T2"]) < 15: continue
            p2 = solve_for(residual, k, "P2", 1e-6, 1e4, flags)
            if p2: k["P2"] = p2; out.append({n: round_sig(v, 9) for n, v in k.items()})
        return out
    return [{"state": "rearranged", "unknown": unknown, "true": states({}), "alt": [],
             "bent": {"EQ_SIGN_FLIPPED": states({"sign_flipped": True}), "EQ_LOG_BASE": states({"log10": True})},
             "park_text": REARRANGED[unknown]}]

def slope_equation_checks(rng):
    """Two rearrangements for the straight-line kind. P is fixed at 760 torr so that
    'T = m/(ln P - b)' and 'T = m/(ln(760) - b)' both pass. dHvap may be written in J or in kJ."""
    def states(dh_of, base=math.e):
        out = []
        for _ in range(3):
            m, b = rng.uniform(-6000, -2500), rng.uniform(15, 22)
            lnP = math.log(760.0) if base == math.e else math.log10(760.0)
            out.append({"m": round_sig(m, 9), "b": round_sig(b, 9), "P": 760.0, "T": round_sig(m / (lnP - b), 9), "dH": round_sig(dh_of(m), 9)})
        return out
    J, kJ = (lambda m: -m * R), (lambda m: -m * R / 1000.0)
    return [
      {"state": "rearranged_dH", "unknown": "dH", "true": states(J), "alt": [states(kJ)],
       "bent": {"EQ_SIGN_FLIPPED": states(lambda m: m * R)}, "park_text": "ΔHvap = -(slope)·R"},
      {"state": "rearranged_T", "unknown": "T", "true": states(J), "alt": [],
       "bent": {"EQ_LOG_BASE": states(J, base=10)}, "park_text": "T = slope / ( ln(760) - intercept )"},
    ]

# ---- DRAFT. What the tutor is told, and what is asked if the model is unavailable, when a trap value appears.
TRAP_NOTES = {
  "CELSIUS_NOT_CONVERTED": {"note": "Their number is what results when a temperature is left in degC.", "ask": "Look at the temperatures you put into 1/T. What scale are they on, and what scale does the relation need?"},
  "KJ_WITH_R_IN_J":        {"note": "Their number is what results when dHvap in kJ meets R in J.", "ask": "Write out the units of ΔHvap and of R side by side. Do they cancel?"},
  "SIGN_FLIPPED":          {"note": "Their number is what results when the negative sign is lost or the ratio is inverted without it.", "ask": "As the temperature goes up, should the vapor pressure go up or down, and does your number do that?"},
  "LOG10_FOR_LN":          {"note": "Their number is what results from log base 10 in place of the natural log.", "ask": "Which logarithm does this relation use, and which key did you press?"},
  "PRESSURE_UNITS_MIXED":  {"note": "Their number is what results when two pressures in different units are divided as they stand.", "ask": "What are the units of each pressure in your ratio?"},
  "EQ_SIGN_FLIPPED":       {"note": "Their rearranged equation holds only if the negative sign is dropped, or the ratio is inverted without it.", "ask": "Follow the negative sign through each step of your rearrangement. Where does it end up?"},
  "EQ_LOG_BASE":           {"note": "Their equation holds only with log base 10. 'log' is read as base 10; 'ln' as natural.", "ask": "Which logarithm does this relation use, and which one did you write?"},
  "SLOPE_SIGN_KEPT":       {"note": "They kept the slope's negative sign on dHvap.", "ask": "Does it take energy or release energy for a molecule to leave the liquid, and what sign does that give ΔHvap?"},
  "ONE_ATM_IN_TORR_LINE":  {"note": "They set P = 1 in a line fitted with P in torr.", "ask": "In what units was P when this line was fitted, and what is the normal boiling pressure in those units?"},
  "KPA_IN_TORR_LINE":      {"note": "They set P = 101.325 in a line fitted with P in torr.", "ask": "In what units was P when this line was fitted?"},
}

# ---- the six "measured" points and their straight-line fit. Made here, seeded, so server and picture agree.
def measured(rng, dH, T_ref, P_ref_atm, lo, hi):
    P_at = lambda T: P_ref_atm * math.exp(-(dH / R) * (1.0 / T - 1.0 / T_ref))
    pts = []
    for i in range(6):
        Tk = lo + (hi - lo) * i / 5.0
        lnP = math.log(P_at(Tk) * 760.0) + (rng.random() - 0.5) * 0.02
        pts.append([round(Tk - 273.15, 1), float(f"{math.exp(lnP):.4g}")])                 # degC, torr
    xs = [1.0 / (t + 273.15) for t, p in pts]; ys = [math.log(p) for t, p in pts]
    sx, sy = sum(xs), sum(ys)
    m = (6 * sum(x * y for x, y in zip(xs, ys)) - sx * sy) / (6 * sum(x * x for x in xs) - sx * sx)
    return pts, m, (sy - m * sx) / 6

def sim_payload(full, unknown, rng):
    lo, hi = min(full["T1"], full["T2"]) - 8.0, max(full["T1"], full["T2"]) + 8.0
    pts, m, b = measured(rng, full["dH"], full["T1"], full["P1"], lo, hi)
    return {"measured_degC_torr": pts, "fit_slope_K": round(m, 1), "fit_intercept": round(b, 2),
            "problem_points": [[round(full["T1"] - 273.15, 2), float(f"{full['P1'] * 760.0:.4g}")], [round(full["T2"] - 273.15, 2), float(f"{full['P2'] * 760.0:.4g}")]],   # in the plot's own units
            "asked_point": 1 if unknown in ("T1", "P1") else (2 if unknown in ("T2", "P2") else 0)}

# ---- SPECIAL KIND: six measured points -> dHvap from the slope, then the normal boiling point.
def slope_kind(rng, state, ctx):
    bp, dH = ctx["bp_K"], state["dH"]
    lo, hi = max(ctx["lo_K"], bp - 45.0), bp - 8.0                  # all points below the boiling point
    pts, m, b = measured(rng, dH, bp, 1.0, lo, hi)
    m, b = round(m, 1), round(b, 2)                                 # what the student sees
    dH_key = -m * R / 1000.0                                        # kJ/mol
    Tb_key = m / (math.log(760.0) - b)                              # K
    ans_T = rng.choice(["degC", "K"])
    Tb_shown = Tb_key - 273.15 if ans_T == "degC" else Tb_key
    Tb_other = Tb_key if ans_T == "degC" else Tb_key - 273.15
    targets = [
      T("dH_found", "dHvap from the slope", dH_key, "kJ/mol", 0.02 * dH_key, role="key", require_unit=True,
        also=[{"value": round_sig(dH_key * 1000, 6), "unit": "J/mol", "abs_tol": round_sig(20 * dH_key, 3)}]),
      T("bp_found", "normal boiling point", Tb_shown, ans_T, 1.0, role="key", require_unit=True,
        also=[{"value": round(Tb_other, 2), "unit": "K" if ans_T == "degC" else "degC", "abs_tol": 1.0}]),
    ]
    off = (lambda K: K - 273.15) if ans_T == "degC" else (lambda K: K)
    traps = [
      {"id": "SLOPE_SIGN_KEPT",        "state": "dH_found", "value": round_sig(-dH_key, 5), "unit": "kJ/mol", "abs_tol": round_sig(0.02 * dH_key, 3)},
      {"id": "KJ_WITH_R_IN_J",         "state": "dH_found", "value": round_sig(dH_key * 1000, 5), "unit": "kJ/mol", "abs_tol": round_sig(20 * dH_key, 3)},
      {"id": "ONE_ATM_IN_TORR_LINE",   "state": "bp_found", "value": round_sig(off(-m / b), 5), "unit": ans_T, "abs_tol": 1.0},
      {"id": "KPA_IN_TORR_LINE",       "state": "bp_found", "value": round_sig(off(m / (math.log(101.325) - b)), 5), "unit": ans_T, "abs_tol": 1.0},
    ]
    board = [
      {"state": "account_given",   "kind": "text",   "register": "submicro",  "requires": []},
      {"state": "relation_chosen", "kind": "pick",   "register": "symbolic",  "requires": ["account_given"], "options_from": "equation_picks", "pin": True},
      {"state": "rearranged_dH",   "kind": "equation", "register": "symbolic", "requires": ["relation_chosen"], "explicit": True, "pin": True},
      {"state": "dH_found",        "kind": "number", "register": "symbolic",  "requires": ["rearranged_dH"], "rule": "all"},
      {"state": "rearranged_T",    "kind": "equation", "register": "symbolic", "requires": ["relation_chosen"], "explicit": True, "pin": True},
      {"state": "bp_found",        "kind": "number", "register": "macro",     "requires": ["rearranged_T"], "rule": "all"},
      {"state": "meaning_given",   "kind": "text",   "register": "inference", "requires": ["dH_found", "bp_found"], "credit_gate": True},
    ]
    unit = "°C" if ans_T == "degC" else "K"
    text = (f"Vapor pressure was measured for an unidentified {_hidden(ctx)} at six temperatures (plots at left). "    # DRAFT
            f"The straight-line fit is ln(P) = ({m:g} K)(1/T) + {b:g}, with P in torr and T in K. "
            f"Find the heat of vaporization in kJ/mol and the normal boiling point in {unit}.")
    return {"context": {"substance": "unidentified", "true_substance": ctx["substance"]}, "text": text,
            "givens": {"slope": {"value": m, "unit": "K"}, "intercept": {"value": b, "unit": ""}},
            "board": board, "targets": targets, "traps": traps,
            "eq_checks": slope_equation_checks(rng),
            "reveal_with_problem": {"measured_degC_torr": pts, "fit_slope_K": m, "fit_intercept": b},
            "sim": {"measured_degC_torr": pts, "fit_slope_K": m, "fit_intercept": b, "mark_P_torr": 760.0}}
SPECIAL = {"slope": slope_kind}

# ---- DRAFT problem sentences. Scenarios are the instructor's.
ASK = {"T2": "At what temperature will its vapor pressure be {P2}?", "T1": "At what temperature is its vapor pressure {P1}?",
       "P2": "What is its vapor pressure at {T2}?", "P1": "What is its vapor pressure at {T1}?",
       "dH": "What is the molar heat of vaporization of the {hidden}?"}    # {hidden}: "alcohol" or "liquid", by class (instructor, 9 Oct)
def _hidden(ctx):
    """How a problem names a liquid it must not identify: by class when the class is an alcohol (instructor, 9 Oct), else 'liquid'."""
    return "alcohol" if _subs.get(ctx["substance"], "class") == "alcohol" else "liquid"
def _fmt(s): return f"{s['value']:g} {'°C' if s['unit'] == 'degC' else s['unit']}"
def render_text(shown, unknown, ans_unit, ctx):
    f = {n: _fmt(s) for n, s in shown.items()}
    liquid = f"An unidentified {_hidden(ctx)}" if unknown == "dH" else ctx["substance"].capitalize()
    pts = []
    if "T1" in f and "P1" in f: pts.append(f"a vapor pressure of {f['P1']} at {f['T1']}")
    if "T2" in f and "P2" in f: pts.append(f"a vapor pressure of {f['P2']} at {f['T2']}")
    dh = "" if unknown == "dH" else f" Its heat of vaporization is {f['dH']}."
    return f"{liquid} has " + " and ".join(pts) + f".{dh} {ASK[unknown].format(hidden=_hidden(ctx), **f)} Report the answer in {'°C' if ans_unit == 'degC' else ans_unit}."
