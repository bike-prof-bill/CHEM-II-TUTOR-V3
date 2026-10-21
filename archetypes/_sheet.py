"""Sheet-driven fixed archetypes (chapters 16 and after, 19 Oct 2026). SCENARIO_CLAUDE's approved sheets carry, per problem, every
expected value with its unit, every named mistake's value and step, and every right pick; scripts/sheet_to_problems.py turns a sheet
into archetypes/data/sheets/<id>.json and the archetype reads it. The archetype supplies the step order, the pick options and the
registers; the test re-derives the chemistry from the problem sentence where it can. Nothing here knows the chemistry."""
import json, os, math, re
from engine import round_sig

NOTEBOOK_URL = "https://notebook.google.com/notebook/6458f208-db32-496a-8088-fe0c1c6cd539"   # INSTRUCTOR: the course notebook

def load(arch_id):
    return json.load(open(os.path.join(os.path.dirname(__file__), "data", "sheets", arch_id + ".json"), encoding="utf-8"))["problems"]

PH_LIKE = set()
UNREACHABLE_TRAPS = {}   # archetype -> traps equal to an earlier step's value (never fire under the 11 Oct restatement rule); run.py reports them
UNIT_OF_SHEET = {"°C": "degC", "deg C": "degC", "kJ": "kJ/mol", "J": "J/mol", "years": "y", "days": "d", "MeV/nucleon": "MeV"}   # the sheet's spelling -> the unit key (a reaction's kJ is kJ per mole of reaction)
def window(value, unit=""):
    if unit in ("°C", "degC"): return 0.3                                           # a temperature in Celsius: three tenths of a degree
    if unit == "K": return max(0.5, 0.002 * abs(value))                                # a kelvin temperature: half a kelvin or 0.2 %
    if value == 0: return 1e-4
    return max(0.02 * abs(value), 0.5 * 10 ** (math.floor(math.log10(abs(value))) - 1))   # 2 %, or half a unit in the second significant figure

# option sets, chosen by the right answer's family; every option text begins with the bare word the student may type
OPTION_SETS = [
  (("yes", "no"), [("yes", "yes: spontaneous as written"), ("no", "no: not spontaneous as written")]),
  (("positive", "negative"), [("positive", "positive: the entropy of the system rises"), ("negative", "negative: the entropy of the system falls")]),
  (("always", "never", "low", "high"), [("always", "always: spontaneous at every temperature"), ("never", "never: spontaneous at no temperature"), ("low", "low: spontaneous only at low temperature"), ("high", "high: spontaneous only at high temperature")]),
  (("forward", "reverse", "equilibrium"), [("forward", "forward: ΔG is negative, the reaction runs toward products"), ("reverse", "reverse: ΔG is positive, it runs toward reactants"), ("equilibrium", "equilibrium: ΔG is zero within 0.2 kJ")]),
  (("products", "reactants", "neither"), [("products", "products: K is well above 1"), ("reactants", "reactants: K is well below 1"), ("neither", "neither: K is near 1")]),
  (("doubles", "halves", "unchanged"), [("doubles", "doubles: twice the reaction, twice the value"), ("halves", "halves: half the value"), ("unchanged", "unchanged: the same value")]),
  (("rises", "falls", "unchanged"), [("rises", "rises: the value goes up"), ("falls", "falls: the value goes down"), ("unchanged", "unchanged: the value stays the same")]),
  (("positive", "negative", "zero"), [("positive", "positive"), ("negative", "negative"), ("zero", "zero")]),
  (("zero", "first", "second"), [("zero", "zero: the rate does not depend on the concentration"), ("first", "first: the rate is proportional to the concentration"), ("second", "second: the rate goes with the concentration squared")]),
  (("into", "out", "neither"), [("into", "into: water flows into the cell"), ("out", "out: water flows out of the cell"), ("neither", "neither: no net flow")]),
  (("disappearing", "appearing"), [("disappearing", "disappearing: a reactant, its concentration falls"), ("appearing", "appearing: a product, its concentration rises")]),
]
def options_for(right, named_wrong=None):
    for tags, opts in OPTION_SETS:
        if right in tags:
            out = [{"id": o[0], "text": o[1]} for o in opts]
            for o in out:
                if named_wrong and o["id"] != right: o["names"] = named_wrong
            return out
    raise ValueError(f"no option set holds the pick {right!r}")

def make_fixed_from_sheet(ID, problems, fid, step_order, pick_named=None, sim_params=None, registers=None, key_state=None, no_key=False, pick_options=None, tolerance=None, relation=True, sim_student=None, drop_restated=False):
    """step_order: the states in order; a state present in the problem's expected or picks is put on the board, the rest are skipped.
    pick_named: {pick state: error id named on a wrong option}. sim_params(problem) -> dict for the page's address.
    Brief 32 (21 Oct): a `sim_predict` state is the prediction pick that opens the page (its options and right answer from the sheet's
    `sim predict` cell; a trap with a pick value names a wrong option); `sim_instrument` is the reading the student takes on the page,
    checked like any number in the sheet's window; `sim_gap` is the gap question. sim_student maps page placeholders to the student's
    own values ({"T_student": "T_found", "pred": "sim_predict"}), filled by the shell at the reveal."""
    P = [p for p in problems if p["id"] == fid][0]; pick_named = dict(pick_named or {}); registers = registers or {}
    for t in P["traps"]:                                                      # a named wrong pick from the sheet ("PERTURB_I_IGNORED at perturb_1: unchanged")
        if "pick" in t: pick_named.setdefault(t["state"], {})
        if "pick" in t and isinstance(pick_named[t["state"]], dict): pick_named[t["state"]][t["pick"]] = t["id"]
    if isinstance(step_order, dict): step_order = step_order[P["kind"]]
    exp_by = {}
    for e in P["expected"]:
        if e["state"] == "coeffs_found": continue                                      # a coefficient row, not a number
        exp_by.setdefault(e["state"], []).append(e)
    board = [{"state": "account_given", "kind": "text", "register": "submicro", "requires": []}]
    if relation: board.append({"state": "relation_chosen", "kind": "pick", "register": "symbolic", "requires": ["account_given"], "options_from": "equation_picks", "pin": True})
    expected, traps = [], []; prev = "relation_chosen" if relation else "account_given"
    numbers = [s for s in step_order if s in exp_by]
    last_number = numbers[-1] if numbers else None
    for st in step_order:
        if st in exp_by:
            for e in exp_by[st]:
                role = "intermediate" if no_key else ("key" if st == (key_state or last_number) else "intermediate")
                unit = UNIT_OF_SHEET.get(e["unit"], e["unit"])   # a reaction's kJ is kJ per mole of reaction, the unit the student types as kJ
                tol = sheet_tolerance(P, e["value"])
                if tol is None and tolerance: tol = tolerance(P, st, e["value"], unit)
                if tol is None: tol = max(0.02 * abs(e["value"]), e.get("half_ulp", 0), 0.3 if unit == "degC" else 0, 0.5 if unit == "K" else 0)
                label = e["label"] or st
                if any(x["label"] == label for x in expected): label = f"{label} ({e['unit'] or st})"     # two items with one label (binding energy in J and in MeV) stay distinct
                expected.append({"state": st, "label": label, "value": round_sig(e["value"], 6), "unit": unit, "abs_tol": round_sig(tol, 3),
                                 "role": role, "require_unit": bool(e["unit"]), "after": prev})
            board.append({"state": st, "kind": "number", "register": registers.get(st, "symbolic"), "requires": [prev], "explicit": True, "pin": True, **({"rule": "all"} if len(exp_by[st]) > 1 else {})})
            prev = st
        elif st == "coeffs_found" and P.get("coeffs"):
            cf = P["coeffs"]
            board.append({"state": st, "kind": "coefficients", "register": "symbolic", "requires": [prev], "species": cf["species"], "right": cf["right"], "arrow_after": cf["arrow_after"], "explicit": True, "pin": True}); prev = st
        elif st in P["picks"] or (st == "sim_predict" and P.get("sim_predict")):
            right = P["picks"].get(st) or P["sim_predict"]["right"]
            pn = pick_named.get(st)
            opts = (pick_options(P, st, right) if pick_options else None) or options_for(right, pn if isinstance(pn, str) else None)
            if isinstance(pn, dict):                                              # {wrong option: error id}
                for o in opts:
                    if o["id"] in pn: o["names"] = pn[o["id"]]
            elif pick_options and pn:
                for o in opts:
                    if o["id"] != right: o["names"] = pn
            item = {"state": st, "kind": "direction", "register": registers.get(st, "macro"), "requires": [prev], "options": opts, "right": [f"{st}:{right}"], "explicit": True, "pin": True}
            if st == "sim_predict":
                item["opens_sim"] = True; item["register"] = "macro"
                if sim_student: item["sim_student"] = dict(sim_student)
            board.append(item)
            for o in board[-1]["options"]: o["id"] = f"{st}:{o['id']}"
            prev = st
            if st.startswith("perturb_"): board.append({"state": st + "_why", "kind": "text", "register": "submicro", "requires": [st]}); prev = st + "_why"
        elif st == "sim_instrument" and (P.get("sim_instrument") or {}).get("value") is not None:
            ins = P["sim_instrument"]; u = ins.get("unit", "")
            expected.append({"state": st, "label": "reading from the page" + (f" ({ins.get('control')})" if ins.get("control") else ""), "value": round_sig(ins["value"], 6), "unit": u,
                             "abs_tol": round_sig(ins.get("abs_tol") or max(0.02 * abs(ins["value"]), 0.5), 3), "role": "intermediate", "require_unit": bool(u), "after": prev})
            board.append({"state": st, "kind": "number", "register": "macro", "requires": [prev], "explicit": True, "pin": True,
                          "instrument": {k: ins.get(k) for k in ("control", "reading", "target", "target_unit") if ins.get(k) is not None}})
            prev = st
        elif st == "sim_gap" and P.get("sim_gap"):
            board.append({"state": st, "kind": "text", "register": "inference", "requires": [prev]}); prev = st
    board += [{"state": "meaning_given", "kind": "text", "register": "inference", "requires": [prev], "credit_gate": True},
              {"state": "reflection", "kind": "reflection", "register": "inference", "requires": ["meaning_given"]}]
    unit_of = {e["state"]: UNIT_OF_SHEET.get(e["unit"], e["unit"]) for e in P["expected"]}
    dropped_restate = []
    for t in P["traps"]:
        if "value" not in t or t["state"] not in exp_by: continue
        ttol = tolerance(P, t["state"], t["value"], unit_of.get(t["state"], "")) if tolerance else None
        tol = round_sig(ttol if ttol is not None else max(0.02 * abs(t["value"]), 0.3 if unit_of.get(t["state"], "") in ("°C", "degC") else 0, 0.5 if unit_of.get(t["state"], "") == "K" else 0), 3)
        def _clear(a, e):
            if e["value"] and a and e["abs_tol"] >= 0.5 * abs(e["value"]) and abs(math.log10(abs(e["value"]))) >= 15:                 # an item accepted as a power of ten: clear means a factor of 3 apart, or the other sign
                return (a > 0) != (e["value"] > 0) or max(abs(a), abs(e["value"])) / min(abs(a), abs(e["value"])) > 3
            return abs(a - e["value"]) > 3 * max(tol, e["abs_tol"])
        earlier = [e["state"] for e in expected]; earlier = earlier[:earlier.index(t["state"])] if t["state"] in earlier else []   # states established before this one
        same_as_other = [e for e in expected if e["state"] in earlier and e.get("value") is not None and abs(t["value"] - e["value"]) <= max(tol, e["abs_tol"]) and unit_of.get(t["state"], "") == e.get("unit", "")]
        if same_as_other:                                                     # the shell reads a restated established value as a restatement, never a wrong try (instructor, 11 Oct): the trap can never fire
            dropped_restate.append(f"{t['id']} at {t['state']} = {same_as_other[0]['state']}'s value")
            if drop_restated: continue                                        # brief-32 archetypes drop it; older bundles keep it (and their content version) until the instructor rules
        if all(_clear(t["value"], e) for e in expected if e["state"] == t["state"]):
            traps.append({"id": t["id"], "state": t["state"], "value": round_sig(t["value"], 5), "unit": unit_of.get(t["state"], ""), "abs_tol": tol, **({"registry": t["registry"]} if t.get("registry") else {})})
    out = {"kind": P["kind"], "fixed_id": fid, "version": "", "status": P["status"], "context": {"scenario": P["scenario"], "picks": P["picks"]}, "text": P["text"],
            "givens": {}, "board": board, "targets": expected, "traps": traps, "table": None, "words": {}, "eq_checks": [], "reveal_with_problem": None, "sim": None,
            "sim_params": dict(sim_params(P) if sim_params else {}, **(P.get("sim") or {}))}   # the sheet's own values, when it has them, win (20 Oct)
    for k in ("difficulty", "nearest_eoc", "companion", "exam_item", "sim_reveal", "sim_opens_at"):   # brief 32 fields, carried for the shell, the log and the tests
        if P.get(k): out[k] = P[k]
    if dropped_restate and drop_restated: out["traps_dropped"] = [f"RESTATEMENT:{x}" for x in dropped_restate]
    elif dropped_restate: UNREACHABLE_TRAPS.setdefault(ID, set()).update(dropped_restate)   # reported by run.py, not changed
    ins = P.get("sim_instrument") or {}
    words = dict(P.get("sim") or {})                                              # the sheet's own slots fill {water_kg}-style placeholders in a moves row
    if ins.get("target") is not None: words["target"] = f"{ins['target']:.1f}".replace("-", "−"); words["target_unit"] = ins.get("target_unit", "")
    if P.get("sim_gap"): words["gap_question"] = P["sim_gap"]
    out["words"] = words
    return out

TRAP_NOTES_CH19_21 = {
  "D_COUNT_FROM_GROUP": {"note": "Their d count is the metal's group number, ignoring the oxidation state.", "ask": "How many electrons did the metal lose to reach this oxidation state?"},
  "SPIN_STATE_WRONG": {"note": "Their unpaired count belongs to the other spin state.", "ask": "Does this ligand split the orbitals enough to make pairing cheaper?"},
  "NM_NOT_CONVERTED": {"note": "Their energy uses the wavelength in nanometres.", "ask": "What unit does λ need in E = hc/λ?"},
  "NA_OMITTED": {"note": "Their per-mole value is the per-ion value.", "ask": "How many ions are in a mole?"},
  "LAMBDA_INVERTED": {"note": "Their decay constant is t½/0.693.", "ask": "Does a longer half-life mean a larger or smaller decay constant?"},
  "FRACTION_DECAYED": {"note": "They gave the fraction decayed where the fraction remaining was asked.", "ask": "Which fraction is still there?"},
  "LINEAR_HALVING": {"note": "Their fraction treats decay as a straight line.", "ask": "Does the same amount decay in each half-life, or the same fraction?"},
  "LOG10_FOR_LN": {"note": "Their value uses the base-10 logarithm where ln was needed.", "ask": "Which logarithm goes with 0.693?"},
  "DAUGHTER_AS_N0": {"note": "Their ratio uses the daughter as the starting amount.", "ask": "What was the starting amount of the parent?"},
  "MASS_RATIO_USED": {"note": "Their age uses masses where moles were needed.", "ask": "Do equal masses of parent and daughter hold equal numbers of atoms?"},
  "ELECTRONS_OMITTED": {"note": "Their mass defect leaves out the electrons.", "ask": "Does the atomic mass include the electrons?"},
  "AMU_NOT_CONVERTED": {"note": "Their energy uses the mass in amu where kilograms were needed.", "ask": "What unit of mass does E = mc² need?"},
  "DIVIDED_BY_Z": {"note": "Their per-nucleon value divides by the protons only.", "ask": "How many nucleons are in the nucleus?"},
  "EV_FOR_MEV": {"note": "Their value is in electronvolts where MeV was asked.", "ask": "How many electronvolts are in an MeV?"},
}
TRAP_NOTES_CH17 = {
  "N_ADDED": {"note": "Their electron count adds the two half-reactions' electrons instead of finding the common multiple.", "ask": "How many electrons does each half-reaction have to give or take so that the counts match?"},
  "NOT_LOWEST_WHOLE_NUMBERS": {"note": "Their coefficients balance but are not the lowest whole numbers.", "ask": "Is there a number every coefficient can be divided by?"},
  "ANODE_CATHODE_SWAPPED": {"note": "Their cell potential has the anode and cathode the wrong way round.", "ask": "Which electrode is oxidised, and which potential is subtracted from which?"},
  "POTENTIALS_ADDED": {"note": "Their value adds the two standard potentials.", "ask": "Does the relation add the potentials or take their difference?"},
  "N_WRONG": {"note": "Their value uses the wrong number of electrons.", "ask": "How many electrons pass for the equation as written?"},
  "J_FOR_KJ": {"note": "Their value mixes joules and kilojoules.", "ask": "What unit does nFE carry before you convert?"},
  "LN_FOR_LOG": {"note": "Their value uses the natural logarithm where the base-10 form with 0.0592 V was needed, or the reverse.", "ask": "Which logarithm goes with 0.0592 V?"},
  "Q_INVERTED": {"note": "Their Q is upside down.", "ask": "Which concentrations go on top of Q?"},
  "N_DROPPED": {"note": "Their Nernst value leaves out n.", "ask": "What divides 0.0592 V in the relation?"},
  "NERNST_SIGN": {"note": "Their Nernst value adds the correction instead of subtracting it.", "ask": "What sign sits between E° and the logarithm term?"},
  "TIME_NOT_CONVERTED": {"note": "Their charge uses the time in hours or minutes where seconds were needed.", "ask": "What unit of time does a coulomb per second need?"},
  "ELECTRONS_PER_ION_WRONG": {"note": "Their moles of metal use the wrong electrons per ion.", "ask": "How many electrons does each of these ions take to become the metal?"},
  "FARADAY_INVERTED": {"note": "Their moles of electrons multiply by F instead of dividing.", "ask": "Does the charge divided by F give moles, or the other way round?"},
}
TRAP_NOTES_CH16 = {   # fallbacks only; the approved asks are in each archetype's errors file
  "PRODUCTS_REACTANTS_SWAPPED": {"note": "Their value is products and reactants the wrong way round.", "ask": "Which side's values are subtracted from which?"},
  "COEFFICIENTS_DROPPED": {"note": "Their value ignores a coefficient.", "ask": "How many moles of each species does the equation show?"},
  "J_FOR_KJ": {"note": "Their value mixes joules and kilojoules.", "ask": "What unit does each term carry before you combine them?"},
  "KJ_NOT_CONVERTED": {"note": "Their value keeps ΔH in kilojoules where joules were needed.", "ask": "What unit does ΔS carry, and does ΔH match it?"},
  "J_KJ_MISMATCH": {"note": "Their value divides kilojoules by joules per kelvin without converting.", "ask": "Are the two quantities in the same energy unit?"},
  "CELSIUS_FOR_KELVIN": {"note": "Their value uses a temperature in degrees Celsius.", "ask": "Which temperature scale do these relations use?"},
  "KELVIN_AS_CELSIUS": {"note": "They gave the kelvin temperature where degrees Celsius were asked.", "ask": "How do kelvins and degrees Celsius differ?"},
  "SURROUNDINGS_SIGN": {"note": "Their entropy change of the surroundings has the wrong sign.", "ask": "If the system takes in heat, what happens to the surroundings' entropy?"},
  "TDS_SIGN": {"note": "Their ΔG adds TΔS instead of subtracting it.", "ask": "What sign sits between ΔH and TΔS?"},
  "COUPLED_SUBTRACTED": {"note": "Their coupled ΔG subtracts the second reaction instead of adding it.", "ask": "When two reactions are added, what happens to their ΔG values?"},
  "Q_INVERTED": {"note": "Their Q is upside down.", "ask": "Which concentrations or pressures go on top?"},
  "LOG_FOR_LN": {"note": "Their value uses the base-10 logarithm where the natural logarithm was needed.", "ask": "Which logarithm does this relation use?"},
  "STANDARD_FOR_NONSTANDARD": {"note": "They gave ΔG° where ΔG under the stated conditions was asked.", "ask": "Are the conditions here standard?"},
  "SIGN_DROPPED": {"note": "Their value has the sign dropped.", "ask": "What sign does the relation carry in front?"},
  "SIGN_PICK_WRONG": {"note": "They picked the wrong sign for ΔS of the system.", "ask": "Count the gas molecules on each side. Which side has more ways to be arranged?"},
  "SPONTANEITY_FROM_SYSTEM": {"note": "They judged spontaneity from the system's entropy alone.", "ask": "Which entropy change decides spontaneity: the system's, or the universe's?"},
  "EXTENSIVE_IGNORED": {"note": "They predicted no change in ΔG when the equation was doubled.", "ask": "If twice as much reacts, what happens to the energy change?"},
  "CASE_WRONG": {"note": "They picked the wrong sign case.", "ask": "What are the signs of ΔH and ΔS here, and which term wins at high temperature?"},
}

# ---------- simulation parameters from a problem's own sentence (19-20 Oct 2026: "simulations need to be active") ----------
SIM_IDS = json.load(open(os.path.join(os.path.dirname(__file__), "data", "sim_ids.json"), encoding="utf-8"))
_SUBD = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
_F = r"[A-Za-z0-9₀-₉()⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+?"
_PH = r"\((s|l|g|aq)(?:,\s*([a-z]+))?\)"
def _tok(formula, phase, tag):
    f = re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]", "", formula).translate(_SUBD).replace("(", "").replace(")", "")
    return f + phase + ((tag or "")[:4])
def _side_tokens(side):
    return [_tok(m.group(2), m.group(3), m.group(4)) for m in re.finditer(r"(?:^|\+)\s*(\d*)\s*(" + _F + ")" + _PH, side)]
def reaction_of(text):
    """'... CaCO₃(s) → CaO(s) + CO₂(g) ...' -> (['CaCO3s'], ['CaOs', 'CO2g']); ions lose their charges (Ag⁺(aq) -> Agaq); a tag is kept (C(s, graphite) -> Csgrap)."""
    unit = r"\d*\s*" + _F + r"\((?:s|l|g|aq)(?:,\s*[a-z]+)?\)"
    m = re.search(r"((?:" + unit + r"\s*\+\s*)*" + unit + r")\s*(?:→|⇌|->)\s*((?:" + unit + r"(?:\s*\+\s*)?)+)", text)
    if not m: return None
    return _side_tokens(m.group(1)), _side_tokens(m.group(2))
ALIASES = {("H2Os",): {("H2Ol",): "ice_melting"}}
def match_reaction(text, ids):
    rx = reaction_of(text)
    if not rx: return ""
    L, R = rx
    al = ALIASES.get(tuple(L), {}).get(tuple(R))
    if al and al in ids: return al
    def fits(page_side, ours):
        toks = page_side.split("_")
        if len(toks) != len(ours): return False
        ok = lambda a, b: a == b or a.startswith(b) or b.startswith(a)
        return all(any(ok(t, o) for t in toks) for o in ours) and all(any(ok(t, o) for o in ours) for t in toks)
    for i in ids:
        if "_to_" not in i: continue
        a, b = i.split("_to_", 1)
        if fits(a, L) and fits(b, R): return i
    return ""
def first_number(text, pattern):
    m = re.search(pattern, text)
    return float(m.group(1)) if m else None
def all_reactions(text):
    unit = r"\d*\s*" + _F + r"\((?:s|l|g|aq)(?:,\s*[a-z]+)?\)"
    out = []
    for m in re.finditer(r"((?:" + unit + r"\s*\+\s*)*" + unit + r")\s*(?:→|⇌|->)\s*((?:" + unit + r"(?:\s*\+\s*)?)+)", text):
        out.append((_side_tokens(m.group(1)), _side_tokens(m.group(2))))
    return out
def match_coupled(text, ids):
    """Two reactions added (a coupled reaction): species on both sides cancel; the overall is matched against the page's ids."""
    rs = all_reactions(text)
    if len(rs) < 2: return ""
    L, R = [], []
    for a, b in rs[:2]: L += a; R += b
    for t in list(L):
        if t in R: L.remove(t); R.remove(t)
    fake = " + ".join(L) + " → " + " + ".join(R)
    def fits(page_side, ours):
        toks = page_side.split("_")
        ok = lambda a, b: a == b or a.startswith(b) or b.startswith(a)
        return len(toks) == len(ours) and all(any(ok(t, o) for t in toks) for o in ours) and all(any(ok(t, o) for o in ours) for t in toks)
    for i in ids:
        if "_to_" in i:
            a, b = i.split("_to_", 1)
            if fits(a, sorted(set(L))) and fits(b, sorted(set(R))): return i
    return ""
def temperature_K(text, default=298):
    m = re.search(r"(?:at|of|to)\s+([0-9]+(?:\.[0-9]+)?)\s*K\b", text)
    if m: return float(m.group(1))
    m = re.search(r"(?:at|of)\s+(-?[0-9]+(?:\.[0-9]+)?)\s*°C", text)
    return round(float(m.group(1)) + 273.15, 2) if m else default
def reaction_for_page(P, key):
    """The page's reaction id for a problem: a coupled problem's overall (stated last, or summed) first, then its first reaction."""
    ids = SIM_IDS[key]
    if P.get("kind") == "coupled":
        rs = all_reactions(P["text"])
        if rs:
            L, R = rs[-1]; fake = " + ".join(f"{x}" for x in L)
        for txt in [P["text"].split("Reaction 2:")[-1]] if "Reaction 2:" in P["text"] else []:
            pass
        last = re.findall(r"[^.]*?(?:→|⇌)[^.]*", P["text"])
        for seg in reversed(last):
            r = match_reaction(seg, ids)
            if r: return r
        r = match_coupled(P["text"], ids)
        if r: return r
    return match_reaction(P["text"], ids)
_SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789"); _SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
ELEMENT_NAMES = {"cobalt": "Co", "strontium": "Sr", "radon": "Rn", "phosphorus": "P", "iodine": "I", "sodium": "Na", "technetium": "Tc", "fluorine": "F", "carbon": "C", "uranium": "U", "rubidium": "Rb"}
def isotope_of(text):
    m = re.search(r"\b(Cobalt|Strontium|Radon|Phosphorus|Iodine|Sodium|Technetium|Fluorine|Carbon|Uranium|Rubidium)-(\d+m?)", text, re.I)
    if m: return f"{ELEMENT_NAMES[m.group(1).lower()]}-{m.group(2)}"
    m = re.search(r"\b([A-Z][a-z]?)-(\d+m?)\b", text)
    return f"{m.group(1)}-{m.group(2)}" if m else ""
def nuclide_of(text):
    m = re.search(r"([⁰¹²³⁴⁵⁶⁷⁸⁹]+)[₀₁₂₃₄₅₆₇₈₉]*([A-Z][a-z]?)", text)
    return f"{m.group(2)}-{m.group(1).translate(_SUP)}" if m else ""
def cell_metals(text):
    """From a cell reaction 'M(s) + N⁺(aq) → ...': the metal oxidised (left, the anode) and the metal deposited (right, the cathode)."""
    rs = all_reactions(text)
    if rs:
        L, R = rs[0]
        anode = next((t[:-1] for t in L if t.endswith("s") and re.fullmatch(r"[A-Z][a-z]?", t[:-1])), "")
        if not anode and "H2g" in L: anode = "H2"
        cath = next((t[:-1] for t in R if t.endswith("s") and re.fullmatch(r"[A-Z][a-z]?", t[:-1])), "")
        if not cath and "H2g" in R: cath = "H2"
        return anode, cath
    return "", ""
def ion_conc(text, metal):
    m = re.search(r"\[" + re.escape(metal) + r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁺]*\]\s*=\s*([0-9.]+(?:e-?\d+)?)", text) or re.search(r"([0-9.]+)\s*M\s+" + re.escape(metal) + r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁺]", text)
    return float(m.group(1)) if m else None
def clean_params(d):
    return {k: (round(v, 6) if isinstance(v, float) else v) for k, v in d.items() if v not in ("", None)}
def cell_notation(text):
    """'Zn(s) | Zn²⁺(aq, 0.1 M) || Zn²⁺(aq, 0.5 M) | Zn(s)' or 'Pt | H₂(g, 1 atm) | H⁺(aq, x M) || ...' -> (left, right, cl, cr)."""
    if "||" not in text: return None
    a, b = text.split("||", 1)
    def metal(seg, first):
        found = re.findall(r"\b([A-Z][a-z]?)(?:₂)?\((?:s|g)", seg)
        if not found: return ""
        m = found[0] if first else found[-1]
        return "H2" if m == "H" else m
    def conc(seg, first):
        cs = re.findall(r"\(aq,\s*([0-9.]+(?:e-?\d+)?)\s*M\)", seg)
        return float(cs[-1] if first else cs[0]) if cs else None
    l, r = metal(a, True), metal(b, False)
    cl, cr = conc(a, True), conc(b, False)
    ph = re.search(r"pH\s+([0-9.]+)", text)
    if cl is None and ph and l == "H2": cl = 10 ** (-float(ph.group(1)))
    return l, r, cl, cr
def nernst_params(P):
    t = P["text"]; cn = cell_notation(t)
    if cn: l, r, cl, cr = cn
    else:
        l, r = cell_metals(t); cl = ion_conc(t, l) if l else None; cr = ion_conc(t, r) if r else None
    return clean_params({"left": l, "right": r, "cl": cl, "cr": cr})
def electrolysis_params(P):
    t = P["text"]; ion = ""
    for pat in (r"from (?:molten )?([A-Z][a-z]?)[⁰¹²³⁴⁵⁶⁷⁸⁹]*[⁺]", r"deposits? (?:[0-9.]+ (?:g|kg) of )?([A-Z][a-z]?)\b", r"produces ([A-Z][a-z]?)\b"):
        mm = re.search(pat, t)
        if mm and mm.group(1) in SIM_IDS["electrolysis_ions"]: ion = mm.group(1); break
    mt = re.search(r"for ([0-9.]+) (h|min|s)\b", t)
    secs = float(mt.group(1)) * {"h": 3600, "min": 60, "s": 1}[mt.group(2)] if mt else next((e["value"] for e in P["expected"] if e["state"] == "time_found"), None)
    return clean_params({"ion": ion, "I": first_number(t, r"current of ([0-9.]+) A"), "t": secs, "mode": P["kind"], "m": first_number(t, r"deposit ([0-9.]+) g")})

def sheet_tolerance(P, value):
    """The sheet's `tolerance` column for this problem: '±1 %' -> 1 % of the value; '±0.01 V' or '0.5 g' -> that amount; 'exact' -> a
    hair; blank -> None (the archetype's rule, then the default 2 % or half a unit in the last written place)."""
    t = (P.get("tolerance") or "").strip().lower().replace("±", "").replace("+/-", "").strip()
    if not t: return None
    if t.startswith("exact"): return 1e-9 + 1e-6 * abs(value)
    m_ = re.match(r"([0-9.]+)\s*%", t)
    if m_: return float(m_.group(1)) / 100 * abs(value)
    m_ = re.match(r"([0-9.]+(?:e-?\d+)?)", t)
    return float(m_.group(1)) if m_ else None
