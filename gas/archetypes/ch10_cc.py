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
  ("dichloromethane",       -30.0),   # added 10 Oct 2026 for The Syringe Boiling Trick (instructor approved)
  ("CFC-11",                -30.0),   # added 10 Oct 2026 for The Drinking Bird (instructor approved)
  ("HFE-7000",              -30.0),
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

def draw_state(rng, liquids=None, limits=None, kind=None):
    """limits (per opener, from content_ch10_cc_limits.csv): the known point is the normal boiling point at 1 atm and the
    other temperature lies in [lo_C, hi_C] for that liquid; the unknown pressure is the one at the other temperature."""
    pool = [x for x in SUBSTANCES if not liquids or x[0] in liquids]
    if limits: pool = [x for x in pool if x[0] in limits] or pool
    name, dH_kJ, bp_C, cold_C, mp_C = rng.choice(pool)
    dH, bp = dH_kJ * 1000.0, bp_C + 273.15
    P_at = lambda T: math.exp(-(dH / R) * (1.0 / T - 1.0 / bp))          # atm
    if limits and name in limits:
        L = limits[name]
        depth_m = None
        if L.get("other_by") == "depth":                                               # The Deep-Sea Vent: pressure from depth, temperature from the model
            step = L.get("depth_step_m") or 10.0; n_lo = int(round(L["depth_lo_m"] / step)); n_hi = int(round(L["depth_hi_m"] / step))
            depth_m = step * rng.randint(n_lo, n_hi); P_other = 1.0 + depth_m / 10.0        # atm: the air plus about 1 atm per 10 m of water
            T_known = bp; T_other = 1.0 / (1.0 / bp - (R / dH) * math.log(P_other))        # the model inverted
        elif L["known_point"] == "boiling point":
            T_known = bp; T_other = rng.uniform(L["lo_C"] + 273.15, L["hi_C"] + 273.15)
        else:                                                                          # a drawn known temperature with the model's pressure there
            T_known = rng.uniform(L["known_lo_C"] + 273.15, L["known_hi_C"] + 273.15)
            T_other = T_known + rng.uniform(L["lo_C"], L["hi_C"]) if L["offset"] else rng.uniform(L["lo_C"] + 273.15, L["hi_C"] + 273.15)
        s = {"T1": T_known, "T2": T_other, "P1": P_at(T_known), "P2": P_at(T_other), "dH": dH}       # point 1 = the known point
        if kind in ("P1", "T1"):                                                       # the unknown is point 1: swap
            s = {"T1": T_other, "T2": T_known, "P1": P_at(T_other), "P2": P_at(T_known), "dH": dH}
        ctx = {"substance": name, "one_atm_point": L["known_point"] == "boiling point", "bp_K": bp, "lo_K": min(T_known, T_other), "hi_K": max(T_known, T_other),
               "limited": True, "min_gap": L.get("min_gap", 2.0), "max_P_atm": 250.0 if depth_m is not None else 20.0}
        if depth_m is not None:                                                        # the pressure at depth is not printed; the depth is
            other = "P1" if kind in ("P1", "T1") else "P2"                            # the pressure at the unknown's point
            ctx.update({"depth_m": depth_m, "hidden": [other], "extra_givens": {"depth": {"value": depth_m, "unit": "m"}},
                        "fixed_units": {"T1" if other == "P2" else "T2": "degC", "P1": "atm", "P2": "atm"}})
        return s, ctx
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

def acceptable(full, ctx=None):
    gap = (ctx or {}).get("min_gap", 8.0) if (ctx or {}).get("limited") else 8.0      # a scenario may allow a smaller temperature gap
    pmax = (ctx or {}).get("max_P_atm", 20.0)                                           # the vent reaches 201 atm
    return abs(full["T2"] - full["T1"]) >= gap and 0.003 < full["P1"] < pmax and 0.003 < full["P2"] < pmax

# ---- grading windows (instructor, 19 Sept): +/- 1 K on temperatures, 2 % elsewhere.
def window(kind, value): return 1.0 if kind == "temperature" else 0.02 * abs(value)

# ---- THE BOARD for one problem: what must be established, and what must come first.
#      Conversions appear only when this problem's numbers call for them.
def board_for(shown, unknown, ctx=None):
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
    b += [{"state": "substituted",   "kind": "number", "register": "symbolic",  "requires": ["rearranged"] + need, "rule": "any"}]
    # Optional items. Defaults (instructor, 10 Oct): the prediction on every pressure problem, the reflection on every problem.
    # A scenario's openers row may add or remove them: "+direction_predicted", "-reflection".
    items = (ctx or {}).get("items") or {}
    want = lambda name, default: (name not in items.get("remove", [])) and (default or name in items.get("add", []))
    with_direction = want("direction_predicted", unknown in ("P1", "P2", "T1", "T2")) and unknown in ("P1", "P2", "T1", "T2")
    with_reflection = want("reflection", True)
    if with_direction:                                        # SCENARIO_CLAUDE, approved 10 Oct: predict before computing (pressure kinds; temperature kinds from the vent)
        q = "pressure" if unknown in ("P1", "P2") else "temperature"
        b.insert(1, {"state": "direction_predicted", "kind": "direction", "register": "macro", "requires": ["account_given"], "explicit": True, "pin": True,
                     "options": [{"id": "direction:higher", "text": f"higher than the {q} I was given"}, {"id": "direction:lower", "text": f"lower than the {q} I was given"},
                                 {"id": "direction:same", "text": f"the same as the {q} I was given"}],
                     "right": ["direction:" + _direction(shown, unknown, (ctx or {}).get("_full"))]})
    if (ctx or {}).get("depth_m") is not None:                   # The Deep-Sea Vent: the pressure at the vent from its depth, before substitution
        b.insert(len([x for x in b if x["kind"] != "number"]) if False else next(i for i, x in enumerate(b) if x["state"] == "substituted"),
                 {"state": "P_from_depth", "kind": "number", "register": "symbolic", "requires": ["account_given"], "rule": "all", "pin": True})
        next(x for x in b if x["state"] == "substituted")["requires"].append("P_from_depth")
    b += [{"state": "value_found",   "kind": "number", "register": "macro",     "requires": ["substituted"] + (["direction_predicted"] if with_direction else []), "rule": "all", "opens_sim": True},
          {"state": "meaning_given", "kind": "text",   "register": "inference", "requires": ["value_found"], "credit_gate": True}]
    if "dP_found" in items.get("add", []) and unknown in ("P1", "P2"):     # The Drinking Bird: how much higher is the pressure in the body
        mg = next(x for x in b if x["state"] == "meaning_given"); mg["requires"] = ["dP_found"]
        b.insert(b.index(mg), {"state": "dP_found", "kind": "number", "register": "macro", "requires": ["value_found"], "rule": "all", "pin": True})
    if with_reflection: b.append({"state": "reflection", "kind": "reflection", "register": "inference", "requires": ["meaning_given"]})   # never graded (approved 10 Oct)
    return b

def extra_targets(full, shown, unknown, ans_unit, ctx):
    """Declared numbers a scenario adds. The Drinking Bird: body pressure minus head pressure, in the answer unit, either sign.
    `derive` tells the verifier to grade it against the student's OWN accepted head pressure (so the 2 % allowance on the head
    pressure is not counted twice): expected = base - value typed for the entry named."""
    items = (ctx or {}).get("items") or {}; out = []
    if (ctx or {}).get("depth_m") is not None:                   # The Deep-Sea Vent: 1 atm + depth/10 atm, within 2 %, unit required
        hid = (ctx.get("hidden") or ["P2"])[0]; P = full[hid]
        out.append(T("P_from_depth", "pressure at the vent", P, "atm", 0.02 * P, role="intermediate", require_unit=True))
    if "dP_found" not in items.get("add", []) or unknown not in ("P1", "P2"): return out
    known = "P1" if unknown == "P2" else "P2"
    P_known = from_canon("pressure", ans_unit, full[known]); P_unknown = from_canon("pressure", ans_unit, full[unknown])
    dP = P_known - P_unknown
    return [T("dP_found", "body minus head pressure", dP, ans_unit, 0.02 * abs(dP), role="intermediate", require_unit=True,
              derive={"from": "key_value_found", "base": round_sig(P_known, 6)},                  # expected = base - student's head pressure
              also=[{"value": round_sig(-dP, 6), "unit": ans_unit, "abs_tol": round_sig(0.02 * abs(dP), 3)}])]

def _direction(shown, unknown, full=None):
    """Which way the unknown lies from the known one. A pressure: decided by the two temperatures (higher T, higher P).
    A temperature: decided by the two pressures (higher P, higher boiling T)."""
    if unknown in ("P1", "P2"):
        other = "P1" if unknown == "P2" else "P2"
        Tu = shown["T1" if unknown == "P1" else "T2"]; Tk = shown["T1" if other == "P1" else "T2"]
        tu = Tu["value"] + (273.15 if Tu["unit"] == "degC" else 0); tk = Tk["value"] + (273.15 if Tk["unit"] == "degC" else 0)
    else:
        pu = full["P1" if unknown == "T1" else "P2"]; pk = full["P2" if unknown == "T1" else "P1"]; tu, tk = pu, pk
    return "higher" if tu > tk * (1 + 1e-9) else ("lower" if tu < tk * (1 - 1e-9) else "same")

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
    if unknown in ("T1", "T2"):
        inv = 1.0 / full[unknown]; out.append(T("substituted", f"1/{unknown}", inv, "1/K", 0.015 * inv))
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
  # SCENARIO_CLAUDE, approved 10 Oct: the pressure ratio typed as the answer, with a pressure unit. Detectable only when the
  # known pressure is not 1 in the unit typed (then the ratio IS the answer numerically and the unit settles nothing).
  {"id": "RATIO_NOT_SCALED", "applies": lambda s, u: u in ("P1", "P2") and abs(_known_P(s, u) - 1.0) > 0.02,
   "value": lambda A, s, k, u, au, key: _ratio_as_answer(s, k, u, au, key)},
  # The Drinking Bird (SCENARIO_CLAUDE, approved 10 Oct): the head pressure that water's heat of vaporization gives in place of the
  # sealed liquid's. Declared only when the liquid's own value is far enough from water's for the two answers to differ.
  # The Deep-Sea Vent (approved 10 Oct): 1/T typed as the answer, with the answer's unit (bare, it is the declared 1/T step)
  {"id": "RECIPROCAL_NOT_TAKEN", "applies": lambda s, u: u in ("T1", "T2"),
   "value": lambda A, s, k, u, au, key: 1.0 / (key + (273.15 if au == "degC" else 0.0))},
  {"id": "WATER_DH_USED", "openers": ["The Drinking Bird"], "applies": lambda s, u: u in ("P1", "P2") and abs(_dH_kJ(s) - _WATER_DH_KJ) > 0.10 * _WATER_DH_KJ,
   "value": lambda A, s, k, u, au, key: _as_student(k, u, au, swap={"dH": _WATER_DH_KJ * 1000.0})},
]
_WATER_DH_KJ = _subs.get("water", "dHvap_at_Tb_kJ_mol")
def _dH_kJ(shown): v = shown["dH"]; return v["value"] if v["unit"] == "kJ/mol" else v["value"] / 1000.0
def _known_P(shown, unknown):
    other = "P1" if unknown == "P2" else "P2"; return shown[other]["value"]           # in its own unit, as the student sees it
def _ratio_as_answer(shown, known, unknown, ans_unit, key):
    other = "P1" if unknown == "P2" else "P2"
    known_in_ans = from_canon("pressure", ans_unit, known[other])
    return key / known_in_ans                                                           # P_unknown / P_known, which has no unit

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
  "RECIPROCAL_NOT_TAKEN": {"note": "They stopped at 1/T: the number is the reciprocal of the temperature, typed as if it were the temperature.",
                           "ask": "That number is 1/T. What is one more step to get T?"},
  "RATIO_NOT_SCALED":    {"note": "They typed the ratio of the two pressures as if it were the pressure asked for. A ratio has no unit; the unknown pressure is the known one times or divided by it.",
                          "ask": "That number is a ratio of two pressures. It has no unit. How do you use the pressure you know to get the one you are finding?"},
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

def sim_params(full, shown, unknown, ans_unit, ctx=None):
    """Values a scenario's simulation may take from the problem (placeholders in its address): {T} = the temperature in °C at
    which the unknown pressure is asked (for a pressure problem) or the second point otherwise; {T_known} = the other point's
    temperature in °C (the body temperature for The Drinking Bird, the boiling point for the syringe); {unit} = the answer's unit."""
    t_unknown = full["T2" if unknown in ("P2", "T2", "dH") else "T1"] - 273.15      # the temperature at the unknown's point
    t_known = full["T1" if unknown in ("P2", "T2", "dH") else "T2"] - 273.15
    out = {"T": f"{t_unknown:.1f}", "T_known": f"{t_known:.1f}", "unit": "°C" if ans_unit == "degC" else ans_unit}
    if (ctx or {}).get("depth_m") is not None: out["depth"] = f"{ctx['depth_m']:g}"      # {depth} in m, for The Deep-Sea Vent
    if ans_unit in ("degC", "K"): out["unit"] = "C" if ans_unit == "degC" else "K"           # a temperature unit as a simulation reads it
    return out
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
    items = (ctx or {}).get("items") or {}
    if "reflection" not in items.get("remove", []): board.append({"state": "reflection", "kind": "reflection", "register": "inference", "requires": ["meaning_given"]})
    unit = "°C" if ans_T == "degC" else "K"
    if ctx.get("template"):                                           # the scenario's own sentence (the generator gives the fitted line, P in torr)
        text = ctx["template"].format(liquid="a related " + _class_word(ctx).split(" ", 1)[1] if _class_word(ctx) != "water" else "water", m=f"{m:g} K", b=f"{b:g}", Punit="torr") + f" Give the boiling point in {unit}."
    else:
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
def _class_word(ctx):
    """'an alcohol', 'a ketone', 'an ether', 'an alkane', 'an ester', 'a haloalkane'; water stays 'water'."""
    c = _subs.get(ctx["substance"], "class")
    if c == "water": return "water"
    return ("an " if c[0] in "aeiou" else "a ") + c
def render_text(shown, unknown, ans_unit, ctx):
    f = {n: _fmt(s) for n, s in shown.items()}
    if ctx.get("hidden"): f.update({h: "(not shown)" for h in ctx["hidden"] if h not in f})   # a scenario that hides a variable must supply its own sentence
    if ctx.get("template") and unknown == "dH":                       # the scenario's own sentence for a ΔHvap problem: the liquid stays unnamed
        return ctx["template"].format(liquid="a related " + _class_word(ctx).split(" ", 1)[1] if _class_word(ctx) != "water" else "water",
                                      P1=f.get("P1", ""), T1=f.get("T1", ""), P2=f.get("P2", ""), T2=f.get("T2", ""), unit=ans_unit)
    if ctx.get("template") and unknown in ("P1", "P2", "T1", "T2"):   # the scenario's own sentence (SCENARIO_CLAUDE, 10 Oct)
        known, other = ("P1", "T1") if unknown in ("P2", "T2") else ("P2", "T2")
        t_unknown = "T2" if unknown in ("P2", "T2") else "T1"
        fill = {"liquid": _class_word(ctx), "T_known": f.get(other, ""), "P_known": f.get(known, ""), "T_unknown": f.get(t_unknown, ""), "dHvap": f["dH"], "unit": "°C" if ans_unit == "degC" else ans_unit,
                "depth": (f"{ctx['depth_m']:g} m" if ctx.get("depth_m") is not None else "")}
        fill.update({"T_syringe": fill["T_unknown"], "T_boil": fill["T_known"], "T_body": fill["T_known"], "P_body": fill["P_known"], "T_head": fill["T_unknown"]})
        return ctx["template"].format(**fill)
    liquid = f"An unidentified {_hidden(ctx)}" if unknown == "dH" else ctx["substance"].capitalize()
    pts = []
    if "T1" in f and "P1" in f: pts.append(f"a vapor pressure of {f['P1']} at {f['T1']}")
    if "T2" in f and "P2" in f: pts.append(f"a vapor pressure of {f['P2']} at {f['T2']}")
    dh = "" if unknown == "dH" else f" Its heat of vaporization is {f['dH']}."
    return f"{liquid} has " + " and ".join(pts) + f".{dh} {ASK[unknown].format(hidden=_hidden(ctx), **f)} Report the answer in {'°C' if ans_unit == 'degC' else ans_unit}."
