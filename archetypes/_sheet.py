"""Sheet-driven fixed archetypes (chapters 16 and after, 19 Oct 2026). SCENARIO_CLAUDE's approved sheets carry, per problem, every
expected value with its unit, every named mistake's value and step, and every right pick; scripts/sheet_to_problems.py turns a sheet
into archetypes/data/sheets/<id>.json and the archetype reads it. The archetype supplies the step order, the pick options and the
registers; the test re-derives the chemistry from the problem sentence where it can. Nothing here knows the chemistry."""
import json, os, math
from engine import round_sig

NOTEBOOK_URL = "https://notebook.google.com/notebook/6458f208-db32-496a-8088-fe0c1c6cd539"   # INSTRUCTOR: the course notebook

def load(arch_id):
    return json.load(open(os.path.join(os.path.dirname(__file__), "data", "sheets", arch_id + ".json"), encoding="utf-8"))["problems"]

PH_LIKE = set()
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
]
def options_for(right, named_wrong=None):
    for tags, opts in OPTION_SETS:
        if right in tags:
            out = [{"id": o[0], "text": o[1]} for o in opts]
            for o in out:
                if named_wrong and o["id"] != right: o["names"] = named_wrong
            return out
    raise ValueError(f"no option set holds the pick {right!r}")

def make_fixed_from_sheet(ID, problems, fid, step_order, pick_named=None, sim_params=None, registers=None, key_state=None, no_key=False, pick_options=None, tolerance=None, relation=True):
    """step_order: the states in order; a state present in the problem's expected or picks is put on the board, the rest are skipped.
    pick_named: {pick state: error id named on a wrong option}. sim_params(problem) -> dict for the page's address."""
    P = [p for p in problems if p["id"] == fid][0]; pick_named = pick_named or {}; registers = registers or {}
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
                tol = tolerance(P, st, e["value"], unit) if tolerance else None
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
        elif st in P["picks"]:
            right = P["picks"][st]
            opts = (pick_options(P, st, right) if pick_options else None) or options_for(right, pick_named.get(st))
            if pick_options and pick_named.get(st):
                for o in opts:
                    if o["id"] != right: o["names"] = pick_named[st]
            board.append({"state": st, "kind": "direction", "register": registers.get(st, "macro"), "requires": [prev], "options": opts, "right": [f"{st}:{right}"], "explicit": True, "pin": True})
            for o in board[-1]["options"]: o["id"] = f"{st}:{o['id']}"
            prev = st
            if st.startswith("perturb_"): board.append({"state": st + "_why", "kind": "text", "register": "submicro", "requires": [st]}); prev = st + "_why"
    board += [{"state": "meaning_given", "kind": "text", "register": "inference", "requires": [prev], "credit_gate": True},
              {"state": "reflection", "kind": "reflection", "register": "inference", "requires": ["meaning_given"]}]
    unit_of = {e["state"]: UNIT_OF_SHEET.get(e["unit"], e["unit"]) for e in P["expected"]}
    for t in P["traps"]:
        if t["state"] not in exp_by: continue
        ttol = tolerance(P, t["state"], t["value"], unit_of.get(t["state"], "")) if tolerance else None
        tol = round_sig(ttol if ttol is not None else max(0.02 * abs(t["value"]), 0.3 if unit_of.get(t["state"], "") in ("°C", "degC") else 0, 0.5 if unit_of.get(t["state"], "") == "K" else 0), 3)
        def _clear(a, e):
            if e["value"] and a and e["abs_tol"] >= 0.5 * abs(e["value"]) and abs(math.log10(abs(e["value"]))) >= 15:                 # an item accepted as a power of ten: clear means a factor of 3 apart, or the other sign
                return (a > 0) != (e["value"] > 0) or max(abs(a), abs(e["value"])) / min(abs(a), abs(e["value"])) > 3
            return abs(a - e["value"]) > 3 * max(tol, e["abs_tol"])
        if all(_clear(t["value"], e) for e in expected if e["state"] == t["state"]):
            traps.append({"id": t["id"], "state": t["state"], "value": round_sig(t["value"], 5), "unit": unit_of.get(t["state"], ""), "abs_tol": tol})
    return {"kind": P["kind"], "fixed_id": fid, "version": "", "status": P["status"], "context": {"scenario": P["scenario"], "picks": P["picks"]}, "text": P["text"],
            "givens": {}, "board": board, "targets": expected, "traps": traps, "table": None, "words": {}, "eq_checks": [], "reveal_with_problem": None, "sim": None,
            "sim_params": (sim_params(P) if sim_params else {})}

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
