"""Chapter 13, combined (the instructor, 13 Oct 2026 evening: ICE and Q versus K are one archetype; four scenarios; each begins
with the direction, Q against K, then its ICE work where the problem has any, then TWO separate perturbations, then the meaning
and the last metacognitive question). Fixed problems. Replaced ch13_ice (retired 15 Oct 2026; its files are under docs/retired/ch13_ice) and the ch13_q_vs_k skeleton.

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
RELATION_TEXT = "K = products over reactants, each raised to its coefficient, at equilibrium; Q is the same fraction at any moment"
NOTEBOOK_URL = "https://notebook.google.com/notebook/6458f208-db32-496a-8088-fe0c1c6cd539"   # INSTRUCTOR: the course notebook
KINDS = ["haber_setup", "wgs_equilibrium", "agcl_tracer", "agbr_tracer", "agi_tracer", "hi_volume", "hi_equilibrium", "no2_equilibrium"]

_RX = json.load(open(os.path.join(os.path.dirname(__file__), "data", "reactions.json"), encoding="utf-8"))["reactions"]
def _rxn(rid, species, coef, side, active, gas, names, sim_keys, words=None):
    r = _RX[rid]
    return {"id": rid, "species": species, "coef": coef, "side": side, "active": active, "gas": gas, "K": r["Kc"],
            "dH_sign": r.get("dH_sign", 0), "names": names, "sim_keys": sim_keys, "equation": r["equation"], "words": words or {}}
HABER = _rxn("haber_ammonia", ["N2", "H2", "NH3"], [1, 3, 2], [-1, -1, 1], [True] * 3, [True] * 3, ["nitrogen", "hydrogen", "ammonia"], ["nN2", "nH2", "nNH3"])
WGS   = _rxn("wgs", ["CO", "H2O", "CO2", "H2"], [1, 1, 1, 1], [-1, -1, 1, 1], [True] * 4, [True] * 4, ["carbon monoxide", "steam", "carbon dioxide", "hydrogen"], ["nCO", "nH2O", "nCO2", "nH2"])
# the three silver halides of the Silent Beaker (SCENARIO_CLAUDE's kit, approved 13 Oct). `words` fill {salt}, {anion}, {sodium_salt} in the
# scenario's moves rows; sim_keys are the approved page's link settings (salt, Ag, X, solid; concentrations, and solid 0 when none is present at the start)
def _halide(rid, X, salt, anion):
    return _rxn(rid, ["Ag" + X.rstrip("-"), "Ag+", X], [1, 1, 1], [-1, 1, 1], [False, True, True], [False] * 3,
                [salt, "silver ion", anion + " ion"], ["Ag", "X"], {"salt": salt, "anion": anion, "sodium_salt": "sodium " + anion})
AGCL = _halide("agcl_dissolution", "Cl-", "silver chloride", "chloride")
AGBR = _halide("agbr_dissolution", "Br-", "silver bromide", "bromide")
AGI  = _halide("agi_dissolution",  "I-",  "silver iodide",   "iodide")
TRACER_RX = {"A": AGCL, "B": AGBR, "C": AGI}
# the Purple Piston (hydrogen iodide, OpenStax 13.3) and the Fading Brown (NO2 dimerisation, OpenStax Example 13.2), approved 14 Oct
HI  = _rxn("hi_formation",     ["H2", "I2", "HI"],  [1, 1, 2], [-1, -1, 1], [True] * 3, [True] * 3, ["hydrogen", "iodine", "hydrogen iodide"], ["nH2", "nI2", "nHI"])
NO2 = _rxn("no2_dimerization", ["NO2", "N2O4"],     [2, 1],    [-1, 1],     [True] * 2, [True] * 2, ["nitrogen dioxide", "dinitrogen tetroxide"], ["nNO2", "nN2O4"])
TRACER_KIND = {"A": "agcl_tracer", "B": "agbr_tracer", "C": "agi_tracer"}

# ---- perturbations per scenario (type, species) as (perturb_1, perturb_2). DRAFT: SCENARIO_CLAUDE and the instructor choose them.
PERTURB = {
  "haber_setup":    [("remove_product", "NH3"), ("heat", None, {"forward": "EXO_HEATED_FORWARD"})],                                    # approved 13-14 Oct: ammonia drawn off; the reactor heated (exothermic: reverse)
  "wgs_equilibrium": [("add_reactant", "H2O"), ("compress", None, {"forward": "SQUEEZE_SHIFT_EQUAL_MOLES", "reverse": "SQUEEZE_SHIFT_EQUAL_MOLES"})],   # approved: more steam; squeezed to half (equal gas moles: no shift)
  "agcl_tracer":    [("add_common_ion", "Cl-", {"forward": "FORWARD_ON_COMMON_ION"}), ("heat", None)],   # approved 13 Oct: the sodium salt stirred in; the beaker warmed (dissolving takes in heat: forward)
  "agbr_tracer":    [("add_common_ion", "Br-", {"forward": "FORWARD_ON_COMMON_ION"}), ("heat", None)],
  "agi_tracer":     [("add_common_ion", "I-",  {"forward": "FORWARD_ON_COMMON_ION"}), ("heat", None)],
  "hi_volume":      [("add_reactant", "H2"), ("heat", None)],            # approved 14 Oct: more hydrogen; warmed (exothermic: reverse)
  "hi_equilibrium": [("add_reactant", "H2"), ("heat", None)],
  "no2_equilibrium": [("compress", None), ("heat", None)],               # approved 14 Oct: squeezed to half (fewer gas moles on the right: forward); warmed (exothermic: reverse)
}
# A third member on a perturbation, or `named_shift` on a problem, names a wrong pick ({option tag: error id}) so the errors file's
# ask is used instead of the generic one (SCENARIO_CLAUDE, 13 Oct; the shell reads `names` on an option)

# ---- the problems. mol: starting amounts (V in litres) or conc: concentrations in M; mode: setup | solve | none
def _h(fid, V, mol, text, family): return {"id": fid, "rxn": HABER, "kind": "haber_setup", "mode": "setup", "V": V, "mol": mol, "conc": None, "text": text, "family": family, "version": "", "sf": 2, "status": "approved (ch13_eq kit, 14 Oct 2026)"}
def _m(fid, V, mol, text, family, version): return {"id": fid, "rxn": WGS, "kind": "wgs_equilibrium", "mode": "solve", "V": V, "mol": mol, "conc": None, "text": text, "family": family, "version": version, "sf": 2, "status": "approved (ch13_eq kit, 14 Oct 2026)"}
_HT = "Inside a steel reactor at 500 °C, nitrogen and hydrogen make ammonia: N2(g) + 3H2(g) ⇌ 2NH3(g). At this temperature, Kc = 0.060. A chemist tests a {V} pilot vessel. She puts in {amounts}. Set up the ICE table. Then write Kc in terms of x."
_MT = "On Mars, a rover fills a sealed {V} steel chamber with {amounts} and heats it to 800 K. Inside, CO(g) + H2O(g) ⇌ CO2(g) + H2(g), and Kc = 4.00. What is the concentration of hydrogen at equilibrium? How much carbon monoxide is left?"
def _t(fid, salt, family, conc, mol, V, solid, named_eq, text):
    return {"id": fid, "rxn": TRACER_RX[salt], "kind": TRACER_KIND[salt], "mode": "none", "V": V, "mol": mol, "conc": conc, "solid": solid, "text": text,
            "family": family, "version": "", "sf": 2, "named_shift": ({"forward": "FORWARD_AT_EQUILIBRIUM"} if named_eq else None),
            "status": "approved (Silent Beaker kit, 13 Oct 2026)"}
def _g2(fid, rx, kind, family, mol, V, V_old, mode, method, value_sp, left_sp, named, text):
    return {"id": fid, "rxn": rx, "kind": kind, "mode": mode, "V": V, "V_old": V_old, "mol": mol, "conc": None, "text": text, "family": family,
            "version": ("equal" if fid.startswith("P2") else ("unequal" if fid.startswith("P3") else "")), "sf": 3, "method": method, "value_sp": value_sp, "left_sp": left_sp,
            "named_shift": ({"forward": "SHIFT_ON_EQUAL_MOLES", "reverse": "SHIFT_ON_EQUAL_MOLES"} if named else None),
            "status": "approved (three-floaters kit, 14 Oct 2026)"}
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
  # The Silent Beaker: eighteen problems (SCENARIO_CLAUDE's ch13_problems_silent_beaker.csv, approved by the instructor 13 Oct 2026), six per
  # salt, mode none (no table). The solid is marked None in conc/mol: present, not counted. `solid` 0 when no solid is there at the start (the page's setting).
  # Every number re-derived in test_ch13_eq.py against the sheet's expected column.
  _t('A1', 'A', 'E (Q = K)', [None, 2e-05, 8e-06], None, 1.0, 1, True, r"""Silver chloride dissolves in water: \( \mathrm{AgCl}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{Cl^{-}}(aq) \). At 25 °C, \( K_c = 1.6 \times 10^{-10} \). A chemist made solid silver chloride by mixing silver nitrate solution with a little less sodium chloride solution, so the water holds a little extra silver. The solid has sat in a sealed beaker for days. The ion probes read \( [\mathrm{Ag^{+}}] = 2.0 \times 10^{-5} \) M and \( [\mathrm{Cl^{-}}] = 8.0 \times 10^{-6} \) M. A pellet of silver chloride made with radioactive silver is dropped onto the solid. Write Q, find its value, and say which way the reaction goes."""),
  _t('A2', 'A', 'Q < K, solid present', [None, 1e-06, 0.0001], None, 1.0, 1, False, r"""Silver chloride dissolves in water: \( \mathrm{AgCl}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{Cl^{-}}(aq) \). At 25 °C, \( K_c = 1.6 \times 10^{-10} \). Water over solid silver chloride has \( [\mathrm{Ag^{+}}] = 1.0 \times 10^{-6} \) M and \( [\mathrm{Cl^{-}}] = 1.0 \times 10^{-4} \) M. Write Q, find its value, and say which way the reaction goes."""),
  _t('A3', 'A', 'Q > K, no solid at the start', [None, 5e-05, 5e-05], None, 1.0, 0, False, r"""Silver chloride dissolves in water: \( \mathrm{AgCl}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{Cl^{-}}(aq) \). At 25 °C, \( K_c = 1.6 \times 10^{-10} \). Two clear solutions are mixed. Right after mixing, before anything settles, \( [\mathrm{Ag^{+}}] = 5.0 \times 10^{-5} \) M and \( [\mathrm{Cl^{-}}] = 5.0 \times 10^{-5} \) M. Write Q, find its value, and say which way the reaction goes."""),
  _t('A4', 'A', 'product absent (Q = 0)', [None, 0.0, 0.0], None, 1.0, 1, False, r"""Silver chloride dissolves in water: \( \mathrm{AgCl}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{Cl^{-}}(aq) \). At 25 °C, \( K_c = 1.6 \times 10^{-10} \). Pure water is poured over solid silver chloride. Write Q, find its value, and say which way the reaction goes."""),
  _t('A5', 'A', 'Q > K, silver ion added', [None, 0.001, 8e-06], None, 1.0, 1, False, r"""Silver chloride dissolves in water: \( \mathrm{AgCl}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{Cl^{-}}(aq) \). At 25 °C, \( K_c = 1.6 \times 10^{-10} \). A sealed beaker holds water over solid silver chloride. A chemist stirs in some silver nitrate. Right after it dissolves, \( [\mathrm{Ag^{+}}] = 1.0 \times 10^{-3} \) M and \( [\mathrm{Cl^{-}}] = 8.0 \times 10^{-6} \) M. Write Q, find its value, and say which way the reaction goes."""),
  _t('A6', 'A', 'Q < K, moles in 0.500 L', None, [None, 2.4999999999999998e-06, 2.4999999999999998e-06], 0.5, 1, False, r"""Silver chloride dissolves in water: \( \mathrm{AgCl}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{Cl^{-}}(aq) \). At 25 °C, \( K_c = 1.6 \times 10^{-10} \). A flask holds 0.500 L of water over solid silver chloride. The water contains \( 2.5 \times 10^{-6} \) mol of silver ions and \( 2.5 \times 10^{-6} \) mol of chloride ions. Write Q, find its value, and say which way the reaction goes."""),
  _t('B1', 'B', 'E (Q = K)', [None, 1e-06, 5e-07], None, 1.0, 1, True, r"""Silver bromide dissolves in water: \( \mathrm{AgBr}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{Br^{-}}(aq) \). At 25 °C, \( K_c = 5.0 \times 10^{-13} \). A chemist made solid silver bromide by mixing silver nitrate solution with a little less sodium bromide solution, so the water holds a little extra silver. The solid has sat in a sealed beaker for days. The ion probes read \( [\mathrm{Ag^{+}}] = 1.0 \times 10^{-6} \) M and \( [\mathrm{Br^{-}}] = 5.0 \times 10^{-7} \) M. A pellet of silver bromide made with radioactive silver is dropped onto the solid. Write Q, find its value, and say which way the reaction goes."""),
  _t('B2', 'B', 'Q < K, solid present', [None, 1e-07, 2e-06], None, 1.0, 1, False, r"""Silver bromide dissolves in water: \( \mathrm{AgBr}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{Br^{-}}(aq) \). At 25 °C, \( K_c = 5.0 \times 10^{-13} \). Water over solid silver bromide has \( [\mathrm{Ag^{+}}] = 1.0 \times 10^{-7} \) M and \( [\mathrm{Br^{-}}] = 2.0 \times 10^{-6} \) M. Write Q, find its value, and say which way the reaction goes."""),
  _t('B3', 'B', 'Q > K, no solid at the start', [None, 3e-06, 3e-06], None, 1.0, 0, False, r"""Silver bromide dissolves in water: \( \mathrm{AgBr}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{Br^{-}}(aq) \). At 25 °C, \( K_c = 5.0 \times 10^{-13} \). Two clear solutions are mixed. Right after mixing, before anything settles, \( [\mathrm{Ag^{+}}] = 3.0 \times 10^{-6} \) M and \( [\mathrm{Br^{-}}] = 3.0 \times 10^{-6} \) M. Write Q, find its value, and say which way the reaction goes."""),
  _t('B4', 'B', 'product absent (Q = 0)', [None, 0.0, 0.0], None, 1.0, 1, False, r"""Silver bromide dissolves in water: \( \mathrm{AgBr}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{Br^{-}}(aq) \). At 25 °C, \( K_c = 5.0 \times 10^{-13} \). Pure water is poured over solid silver bromide. Write Q, find its value, and say which way the reaction goes."""),
  _t('B5', 'B', 'Q > K, silver ion added', [None, 0.001, 5e-07], None, 1.0, 1, False, r"""Silver bromide dissolves in water: \( \mathrm{AgBr}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{Br^{-}}(aq) \). At 25 °C, \( K_c = 5.0 \times 10^{-13} \). A sealed beaker holds water over solid silver bromide. A chemist stirs in some silver nitrate. Right after it dissolves, \( [\mathrm{Ag^{+}}] = 1.0 \times 10^{-3} \) M and \( [\mathrm{Br^{-}}] = 5.0 \times 10^{-7} \) M. Write Q, find its value, and say which way the reaction goes."""),
  _t('B6', 'B', 'Q < K, moles in 0.500 L', None, [None, 1e-07, 1e-07], 0.5, 1, False, r"""Silver bromide dissolves in water: \( \mathrm{AgBr}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{Br^{-}}(aq) \). At 25 °C, \( K_c = 5.0 \times 10^{-13} \). A flask holds 0.500 L of water over solid silver bromide. The water contains \( 1.0 \times 10^{-7} \) mol of silver ions and \( 1.0 \times 10^{-7} \) mol of bromide ions. Write Q, find its value, and say which way the reaction goes."""),
  _t('C1', 'C', 'E (Q = K)', [None, 3.0000000000000004e-08, 5e-09], None, 1.0, 1, True, r"""Silver iodide dissolves in water: \( \mathrm{AgI}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{I^{-}}(aq) \). At 25 °C, \( K_c = 1.5 \times 10^{-16} \). A chemist made solid silver iodide by mixing silver nitrate solution with a little less sodium iodide solution, so the water holds a little extra silver. The solid has sat in a sealed beaker for days. The ion probes read \( [\mathrm{Ag^{+}}] = 3.0 \times 10^{-8} \) M and \( [\mathrm{I^{-}}] = 5.0 \times 10^{-9} \) M. A pellet of silver iodide made with radioactive silver is dropped onto the solid. Write Q, find its value, and say which way the reaction goes."""),
  _t('C2', 'C', 'Q < K, solid present', [None, 1e-09, 5e-08], None, 1.0, 1, False, r"""Silver iodide dissolves in water: \( \mathrm{AgI}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{I^{-}}(aq) \). At 25 °C, \( K_c = 1.5 \times 10^{-16} \). Water over solid silver iodide has \( [\mathrm{Ag^{+}}] = 1.0 \times 10^{-9} \) M and \( [\mathrm{I^{-}}] = 5.0 \times 10^{-8} \) M. Write Q, find its value, and say which way the reaction goes."""),
  _t('C3', 'C', 'Q > K, no solid at the start', [None, 5e-08, 5e-08], None, 1.0, 0, False, r"""Silver iodide dissolves in water: \( \mathrm{AgI}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{I^{-}}(aq) \). At 25 °C, \( K_c = 1.5 \times 10^{-16} \). Two clear solutions are mixed. Right after mixing, before anything settles, \( [\mathrm{Ag^{+}}] = 5.0 \times 10^{-8} \) M and \( [\mathrm{I^{-}}] = 5.0 \times 10^{-8} \) M. Write Q, find its value, and say which way the reaction goes."""),
  _t('C4', 'C', 'product absent (Q = 0)', [None, 0.0, 0.0], None, 1.0, 1, False, r"""Silver iodide dissolves in water: \( \mathrm{AgI}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{I^{-}}(aq) \). At 25 °C, \( K_c = 1.5 \times 10^{-16} \). Pure water is poured over solid silver iodide. Write Q, find its value, and say which way the reaction goes."""),
  _t('C5', 'C', 'Q > K, silver ion added', [None, 0.001, 5e-09], None, 1.0, 1, False, r"""Silver iodide dissolves in water: \( \mathrm{AgI}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{I^{-}}(aq) \). At 25 °C, \( K_c = 1.5 \times 10^{-16} \). A sealed beaker holds water over solid silver iodide. A chemist stirs in some silver nitrate. Right after it dissolves, \( [\mathrm{Ag^{+}}] = 1.0 \times 10^{-3} \) M and \( [\mathrm{I^{-}}] = 5.0 \times 10^{-9} \) M. Write Q, find its value, and say which way the reaction goes."""),
  _t('C6', 'C', 'Q < K, moles in 0.500 L', None, [None, 2.5e-09, 2.5e-09], 0.5, 1, False, r"""Silver iodide dissolves in water: \( \mathrm{AgI}(s) \rightleftharpoons \mathrm{Ag^{+}}(aq) + \mathrm{I^{-}}(aq) \). At 25 °C, \( K_c = 1.5 \times 10^{-16} \). A flask holds 0.500 L of water over solid silver iodide. The water contains \( 2.5 \times 10^{-9} \) mol of silver ions and \( 2.5 \times 10^{-9} \) mol of iodide ions. Write Q, find its value, and say which way the reaction goes."""),
  # The Purple Piston (P, hydrogen iodide) and the Fading Brown (F, NO2 dimerisation): SCENARIO_CLAUDE's sheets, approved 14 Oct 2026. P1: a volume
  # change at equilibrium (conc_found from the new volume; the old volume's values are the named error OLD_VOLUME_USED); F6: the amounts after the valve.
  _g2('P1a', HI, 'hi_volume', 'Q = K after a volume change', [0.04, 0.08, 0.4], 1.0, 2.0, 'none', None, 'HI', 'H2', True, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 2.00 L cylinder at equilibrium holds 0.04 mol of hydrogen, 0.08 mol of iodine and 0.4 mol of hydrogen iodide. The piston squeezes it to 1.00 L. Find each new concentration, then Q, and say which way the reaction goes."""),
  _g2('P1b', HI, 'hi_volume', 'Q = K after a volume change', [0.06, 0.12, 0.6], 1.0, 3.0, 'none', None, 'HI', 'H2', True, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 3.00 L cylinder at equilibrium holds 0.06 mol of hydrogen, 0.12 mol of iodine and 0.6 mol of hydrogen iodide. The piston squeezes it to 1.00 L. Find each new concentration, then Q, and say which way the reaction goes."""),
  _g2('P1c', HI, 'hi_volume', 'Q = K after a volume change', [0.02, 0.04, 0.2], 2.0, 1.0, 'none', None, 'HI', 'H2', True, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 1.00 L cylinder at equilibrium holds 0.02 mol of hydrogen, 0.04 mol of iodine and 0.2 mol of hydrogen iodide. The piston is pulled out until the gas fills 2.00 L. Find each new concentration, then Q, and say which way the reaction goes."""),
  _g2('P2a', HI, 'hi_equilibrium', 'reactants only, equal', [0.5, 0.5, 0.0], 1.0, None, 'solve', 'sqrt', 'HI', 'H2', False, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 1.00 L flask is filled with 0.500 mol of hydrogen and 0.500 mol of iodine. Find the concentration of hydrogen iodide at equilibrium. How much hydrogen is left?"""),
  _g2('P2b', HI, 'hi_equilibrium', 'reactants only, equal', [0.4, 0.4, 0.0], 2.0, None, 'solve', 'sqrt', 'HI', 'H2', False, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 2.00 L flask is filled with 0.400 mol of hydrogen and 0.400 mol of iodine. Find the concentration of hydrogen iodide at equilibrium. How much hydrogen is left?"""),
  _g2('P2c', HI, 'hi_equilibrium', 'reactants only, equal', [1.5, 1.5, 0.0], 5.0, None, 'solve', 'sqrt', 'HI', 'H2', False, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 5.00 L flask is filled with 1.50 mol of hydrogen and 1.50 mol of iodine. Find the concentration of hydrogen iodide at equilibrium. How much hydrogen is left?"""),
  _g2('P3a', HI, 'hi_equilibrium', 'reactants only, unequal', [0.2, 0.4, 0.0], 2.0, None, 'solve', 'quadratic', 'HI', 'I2', False, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 2.00 L flask is filled with 0.200 mol of hydrogen and 0.400 mol of iodine. Find the concentration of hydrogen iodide at equilibrium. How much iodine is left?"""),
  _g2('P3b', HI, 'hi_equilibrium', 'reactants only, unequal', [0.3, 0.2, 0.0], 1.0, None, 'solve', 'quadratic', 'HI', 'H2', False, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 1.00 L flask is filled with 0.300 mol of hydrogen and 0.200 mol of iodine. Find the concentration of hydrogen iodide at equilibrium. How much hydrogen is left?"""),
  _g2('P3c', HI, 'hi_equilibrium', 'reactants only, unequal', [0.1, 0.3, 0.0], 1.0, None, 'solve', 'quadratic', 'HI', 'I2', False, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 1.00 L flask is filled with 0.100 mol of hydrogen and 0.300 mol of iodine. Find the concentration of hydrogen iodide at equilibrium. How much iodine is left?"""),
  _g2('P4a', HI, 'hi_equilibrium', 'product only', [0.0, 0.0, 1.0], 1.0, None, 'solve', 'sqrt', 'HI', 'H2', False, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 1.00 L flask is filled with 1.00 mol of hydrogen iodide. Find the concentration of hydrogen iodide at equilibrium. How much hydrogen forms?"""),
  _g2('P4b', HI, 'hi_equilibrium', 'product only', [0.0, 0.0, 0.8], 2.0, None, 'solve', 'sqrt', 'HI', 'H2', False, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 2.00 L flask is filled with 0.800 mol of hydrogen iodide. Find the concentration of hydrogen iodide at equilibrium. How much hydrogen forms?"""),
  _g2('P4c', HI, 'hi_equilibrium', 'product only', [0.0, 0.0, 1.5], 5.0, None, 'solve', 'sqrt', 'HI', 'H2', False, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 5.00 L flask is filled with 1.50 mol of hydrogen iodide. Find the concentration of hydrogen iodide at equilibrium. How much hydrogen forms?"""),
  _g2('P5a', HI, 'hi_equilibrium', 'all three, Q < K', [0.1, 0.1, 0.1], 1.0, None, 'solve', 'sqrt', 'HI', 'H2', False, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 1.00 L flask holds 0.100 mol each of hydrogen, iodine and hydrogen iodide. Find the concentration of hydrogen iodide at equilibrium. How much hydrogen is left?"""),
  _g2('P5b', HI, 'hi_equilibrium', 'all three, Q < K', [0.2, 0.2, 0.4], 2.0, None, 'solve', 'sqrt', 'HI', 'H2', False, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 2.00 L flask holds 0.200 mol of hydrogen, 0.200 mol of iodine and 0.400 mol of hydrogen iodide. Find the concentration of hydrogen iodide at equilibrium. How much hydrogen is left?"""),
  _g2('P5c', HI, 'hi_equilibrium', 'all three, Q < K', [0.1, 0.2, 0.1], 1.0, None, 'solve', 'quadratic', 'HI', 'I2', False, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 1.00 L flask holds 0.100 mol of hydrogen, 0.200 mol of iodine and 0.100 mol of hydrogen iodide. Find the concentration of hydrogen iodide at equilibrium. How much iodine is left?"""),
  _g2('P6a', HI, 'hi_equilibrium', 'all three, Q > K', [0.02, 0.02, 0.4], 1.0, None, 'solve', 'sqrt', 'HI', 'H2', False, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 1.00 L flask holds 0.0200 mol of hydrogen, 0.0200 mol of iodine and 0.400 mol of hydrogen iodide. Find the concentration of hydrogen iodide at equilibrium. How much hydrogen is left?"""),
  _g2('P6b', HI, 'hi_equilibrium', 'all three, Q > K', [0.06, 0.06, 1.0], 2.0, None, 'solve', 'sqrt', 'HI', 'H2', False, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 2.00 L flask holds 0.0600 mol of hydrogen, 0.0600 mol of iodine and 1.00 mol of hydrogen iodide. Find the concentration of hydrogen iodide at equilibrium. How much hydrogen is left?"""),
  _g2('P6c', HI, 'hi_equilibrium', 'all three, Q > K', [0.04, 0.04, 0.5], 1.0, None, 'solve', 'sqrt', 'HI', 'H2', False, r"""Hydrogen and iodine make hydrogen iodide: \( \mathrm{H_2}(g) + \mathrm{I_2}(g) \rightleftharpoons 2\mathrm{HI}(g) \). At 400 °C, \( K_c = 50.0 \). A 1.00 L flask holds 0.0400 mol of hydrogen, 0.0400 mol of iodine and 0.500 mol of hydrogen iodide. Find the concentration of hydrogen iodide at equilibrium. How much hydrogen is left?"""),
  _g2('F1a', NO2, 'no2_equilibrium', 'NO2 only', [0.1, 0.0], 1.0, None, 'solve', 'quadratic', 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 1.00 L cell is filled with 0.1 mol of nitrogen dioxide. Find the concentration of dinitrogen tetroxide at equilibrium. How much nitrogen dioxide is left?"""),
  _g2('F1b', NO2, 'no2_equilibrium', 'NO2 only', [0.05, 0.0], 1.0, None, 'solve', 'quadratic', 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 1.00 L cell is filled with 0.05 mol of nitrogen dioxide. Find the concentration of dinitrogen tetroxide at equilibrium. How much nitrogen dioxide is left?"""),
  _g2('F1c', NO2, 'no2_equilibrium', 'NO2 only', [0.3, 0.0], 2.0, None, 'solve', 'quadratic', 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 2.00 L cell is filled with 0.3 mol of nitrogen dioxide. Find the concentration of dinitrogen tetroxide at equilibrium. How much nitrogen dioxide is left?"""),
  _g2('F2a', NO2, 'no2_equilibrium', 'N2O4 only', [0.0, 0.05], 1.0, None, 'solve', 'quadratic', 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 1.00 L cell is filled with 0.05 mol of dinitrogen tetroxide. Find the concentration of dinitrogen tetroxide at equilibrium. How much nitrogen dioxide forms?"""),
  _g2('F2b', NO2, 'no2_equilibrium', 'N2O4 only', [0.0, 0.02], 1.0, None, 'solve', 'quadratic', 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 1.00 L cell is filled with 0.02 mol of dinitrogen tetroxide. Find the concentration of dinitrogen tetroxide at equilibrium. How much nitrogen dioxide forms?"""),
  _g2('F2c', NO2, 'no2_equilibrium', 'N2O4 only', [0.0, 0.15], 2.0, None, 'solve', 'quadratic', 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 2.00 L cell is filled with 0.15 mol of dinitrogen tetroxide. Find the concentration of dinitrogen tetroxide at equilibrium. How much nitrogen dioxide forms?"""),
  _g2('F3a', NO2, 'no2_equilibrium', 'both, Q < K', [0.1, 0.02], 1.0, None, 'solve', 'quadratic', 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 1.00 L cell holds 0.1 mol of nitrogen dioxide and 0.02 mol of dinitrogen tetroxide. Find the concentration of dinitrogen tetroxide at equilibrium. How much nitrogen dioxide is left?"""),
  _g2('F3b', NO2, 'no2_equilibrium', 'both, Q < K', [0.12, 0.04], 2.0, None, 'solve', 'quadratic', 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 2.00 L cell holds 0.12 mol of nitrogen dioxide and 0.04 mol of dinitrogen tetroxide. Find the concentration of dinitrogen tetroxide at equilibrium. How much nitrogen dioxide is left?"""),
  _g2('F3c', NO2, 'no2_equilibrium', 'both, Q < K', [0.08, 0.5], 1.0, None, 'solve', 'quadratic', 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 1.00 L cell holds 0.08 mol of nitrogen dioxide and 0.5 mol of dinitrogen tetroxide. Find the concentration of dinitrogen tetroxide at equilibrium. How much nitrogen dioxide is left?"""),
  _g2('F4a', NO2, 'no2_equilibrium', 'both, Q > K', [0.01, 0.05], 1.0, None, 'solve', 'quadratic', 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 1.00 L cell holds 0.01 mol of nitrogen dioxide and 0.05 mol of dinitrogen tetroxide. Find the concentration of dinitrogen tetroxide at equilibrium. How much nitrogen dioxide is left?"""),
  _g2('F4b', NO2, 'no2_equilibrium', 'both, Q > K', [0.03, 0.2], 2.0, None, 'solve', 'quadratic', 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 2.00 L cell holds 0.03 mol of nitrogen dioxide and 0.2 mol of dinitrogen tetroxide. Find the concentration of dinitrogen tetroxide at equilibrium. How much nitrogen dioxide is left?"""),
  _g2('F4c', NO2, 'no2_equilibrium', 'both, Q > K', [0.02, 0.1], 1.0, None, 'solve', 'quadratic', 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 1.00 L cell holds 0.02 mol of nitrogen dioxide and 0.1 mol of dinitrogen tetroxide. Find the concentration of dinitrogen tetroxide at equilibrium. How much nitrogen dioxide is left?"""),
  _g2('F5a', NO2, 'no2_equilibrium', 'Q = K', [0.025, 0.1], 1.0, None, 'none', None, 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 1.00 L cell holds 0.025 mol of nitrogen dioxide and 0.1 mol of dinitrogen tetroxide. Find Q and say which way the reaction goes."""),
  _g2('F5b', NO2, 'no2_equilibrium', 'Q = K', [0.04, 0.128], 2.0, None, 'none', None, 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 2.00 L cell holds 0.04 mol of nitrogen dioxide and 0.128 mol of dinitrogen tetroxide. Find Q and say which way the reaction goes."""),
  _g2('F5c', NO2, 'no2_equilibrium', 'Q = K', [0.05, 0.4], 1.0, None, 'none', None, 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 1.00 L cell holds 0.05 mol of nitrogen dioxide and 0.4 mol of dinitrogen tetroxide. Find Q and say which way the reaction goes."""),
  _g2('F6a', NO2, 'no2_equilibrium', 'NO2 added to an equilibrium mixture', [0.05, 0.1], 1.0, None, 'solve', 'quadratic', 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 1.00 L cell at equilibrium holds 0.025 mol of nitrogen dioxide and 0.1 mol of dinitrogen tetroxide. A valve adds 0.025 mol more nitrogen dioxide. Find the concentration of dinitrogen tetroxide at the new equilibrium. How much nitrogen dioxide is left?"""),
  _g2('F6b', NO2, 'no2_equilibrium', 'NO2 added to an equilibrium mixture', [0.1, 0.128], 2.0, None, 'solve', 'quadratic', 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 2.00 L cell at equilibrium holds 0.04 mol of nitrogen dioxide and 0.128 mol of dinitrogen tetroxide. A valve adds 0.06 mol more nitrogen dioxide. Find the concentration of dinitrogen tetroxide at the new equilibrium. How much nitrogen dioxide is left?"""),
  _g2('F6c', NO2, 'no2_equilibrium', 'NO2 added to an equilibrium mixture', [0.15000000000000002, 0.4], 1.0, None, 'solve', 'quadratic', 'N2O4', 'NO2', False, r"""Nitrogen dioxide joins to form dinitrogen tetroxide: \( 2\mathrm{NO_2}(g) \rightleftharpoons \mathrm{N_2O_4}(g) \). At 25 °C, \( K_c = 1.6 \times 10^{2} \). A 1.00 L cell at equilibrium holds 0.05 mol of nitrogen dioxide and 0.4 mol of dinitrogen tetroxide. A valve adds 0.1 mol more nitrogen dioxide. Find the concentration of dinitrogen tetroxide at the new equilibrium. How much nitrogen dioxide is left?"""),
]

MECHANISM_WORDS = ["molecul", "particl", "atom", "ion", "collid", "collis", "forward", "reverse", "rate", "recombin", "decompos", "dissociat",
                   "associat", "equal", "same pace", "both direction", "energ", "bond", "swap", "break apart", "dissolv", "precipitat", "settle", "trade", "exchange"]

# ---- the unnamed Equations list. The K form and the Q form both fit (the student meets Q first; instructor to confirm).
EQUATION_PICKS = [   # written in \( \) so the page renders them; the instructor's rule: no caret in anything a student reads (15 Oct)
  {"id": "eq_k",  "text": r"\( K = \dfrac{[\mathrm{C}]^{c}[\mathrm{D}]^{d}}{[\mathrm{A}]^{a}[\mathrm{B}]^{b}} \)",            "fits": KINDS},
  {"id": "eq_q",  "text": r"\( Q = \dfrac{[\mathrm{C}]_0^{\,c}[\mathrm{D}]_0^{\,d}}{[\mathrm{A}]_0^{\,a}[\mathrm{B}]_0^{\,b}} \)",  "fits": KINDS},
  {"id": "eq_kp", "text": r"\( K_p = K_c (RT)^{\Delta n} \)",                                                          "fits": []},
  {"id": "eq_g",  "text": r"\( \Delta G^\circ = -RT \ln K \)",                                                      "fits": []},
  {"id": "eq_r",  "text": r"\( \text{rate} = k[\mathrm{A}]^{m}[\mathrm{B}]^{n} \)",                                   "fits": []},
  {"id": "eq_ph", "text": r"\( \mathrm{pH} = -\log[\mathrm{H_3O^+}] \)",                                             "fits": []},
]
CONSTANTS = []
# The Q-step named errors (1/Q, coefficients as multipliers, exponents dropped): their base errors rows (every scenario) were approved
# with the Silent Beaker kit, 13 Oct, so they attach to every kind; each is kept only where its value is clearly apart from Q.
Q_TRAPS_FOR = set(KINDS)

def window(value): return max(0.02 * abs(value), 1e-4 if abs(value) >= 1e-2 else 0.02 * abs(value))
def E(state, label, value, unit, **kw):
    d = {"state": state, "label": label, "value": round_sig(value, 6), "unit": unit, "abs_tol": round_sig(window(value), 3)}
    d.update(kw); return d
def _fmt_coef(c): return "" if c == 1 else str(c)
def _g(v): return f"{v:.3f}"
def _trap(tid, value, state): return {"id": tid, "state": state, "value": round_sig(value, 5), "unit": "", "abs_tol": round_sig(window(value), 3)}
def _clear(a, b): return abs(a - b) > 3 * max(window(a), window(b))
def _dir_opts(prefix, more, named=None, dissolution=False):   # option texts start with the bare word the shell reads when it is typed
    if dissolution:                                 # approved wording for a solid dissolving (instructor, 13 Oct)
        opts = [{"id": f"{prefix}:forward", "text": "forward: more of the solid dissolves"},
                {"id": f"{prefix}:reverse", "text": "reverse: more solid forms"},
                {"id": f"{prefix}:neither", "text": "neither: no change overall"}]
    else:
        opts = [{"id": f"{prefix}:forward", "text": f"forward toward more {more}"},
                {"id": f"{prefix}:reverse", "text": f"reverse toward less {more}"},
                {"id": f"{prefix}:neither", "text": "neither because it stays at equilibrium"}]
    for o in opts:
        tid = (named or {}).get(o["id"].split(":")[1])
        if tid: o["names"] = tid
    return opts
def _dir_id(prefix, d): return f"{prefix}:forward" if d > 0 else (f"{prefix}:reverse" if d < 0 else f"{prefix}:neither")

def make_fixed(rng, fid):
    P = [f for f in FIXED if f["id"] == fid][0]; rx = P["rxn"]; sp, coef, side, act = rx["species"], rx["coef"], rx["side"], rx["active"]
    conc = [0.0 if m is None else m / P["V"] for m in P["mol"]] if P["mol"] is not None else [0.0 if c is None else c for c in P["conc"]]
    d = direction(rx, conc, sf=P["sf"]); Q = quotient(rx, conc)
    has_conc = P["mol"] is not None and (P["V"] != 1.0 or P.get("V_old") is not None)
    expected, traps = [], []
    if has_conc:
        for i in range(len(sp)):
            if act[i]: expected.append(E("conc_found", f"starting [{sp[i]}]", conc[i], "M", role="intermediate", require_unit=True))
        if P.get("V_old"):                             # the volume changed: a concentration from the old volume is a named error, where it is clearly not a new one
            for i in range(len(sp)):
                old = P["mol"][i] / P["V_old"]
                if act[i] and P["mol"][i] and all(_clear(old, c) for c in conc if c) and all(_clear(old, t["value"]) for t in traps if t["state"] == "conc_found"):
                    traps.append({"id": "OLD_VOLUME_USED", "state": "conc_found", "value": round_sig(old, 5), "unit": "M", "abs_tol": round_sig(window(old), 3)})
    if Q is not None:
        expected.append(E("Q_found", "Q at the start", Q, "", role="intermediate", require_unit=False, after="conc_found" if has_conc else "relation_chosen"))
        cands = (((("Q_INVERTED", 1.0 / Q),) if Q > 0 else ()) + ((("COEFFICIENTS_AS_MULTIPLIERS", multipliers_quotient(rx, conc)),) if any(c > 1 for c, a in zip(coef, act) if a) else ()) + ((("EXPONENTS_DROPPED", quotient(rx, conc, exponents=False)),) if any(c > 1 for c, a in zip(coef, act) if a) else ())) if P["kind"] in Q_TRAPS_FOR else ()
        if P["mode"] == "none" and P["mol"] is not None and P["V"] != 1.0:   # moles straight into Q (the Silent Beaker's 6s): named on Q itself, since there is no table
            cands = cands + (("MOLES_NOT_CONCENTRATION", quotient(rx, [0.0 if m is None else m for m in P["mol"]])),)
        for tid, val in cands:
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
        iV, iL = sp.index(P.get("value_sp", "H2")), sp.index(P.get("left_sp", "CO"))
        vl, ll = f"equilibrium [{sp[iV]}]", f"equilibrium [{sp[iL]}]"
        expected += [E("x_found", "x", x, "", role="intermediate", require_unit=False),
                     E("other_root_checked", "the other root", other, "", role="intermediate", require_unit=False, after="x_found",
                       also=([{"value": round_sig(-other, 6), "unit": "", "abs_tol": round_sig(window(other), 3)}] if other < 0 else [])),
                     E("value_found", vl, eq[iV], "M", role="key", require_unit=True),
                     E("leftover_found", ll, eq[iL], "M", role="intermediate", require_unit=True),
                     E("K_confirmed", "Kc from the equilibrium row", rx["K"], "", role="intermediate", require_unit=False, after="leftover_found", abs_tol=round_sig(0.03 * rx["K"], 3))]
        traps.append({"id": "PHANTOM_ROOT", "state": "x_found", "value": round_sig(abs(other), 5), "unit": "", "abs_tol": round_sig(window(other), 3)})
        if abs(eq[iL] - eq[iV]) > 3 * max(window(eq[iL]), window(eq[iV])):
            traps.append({"id": "LEFTOVER_FOR_PRODUCT", "state": "value_found", "value": round_sig(eq[iL], 5), "unit": "M", "abs_tol": round_sig(window(eq[iL]), 3)})
            traps.append({"id": "LEFTOVER_FOR_PRODUCT", "state": "leftover_found", "value": round_sig(eq[iV], 5), "unit": "M", "abs_tol": round_sig(window(eq[iV]), 3)})
        if P["V"] != 1.0: traps.append({"id": "MOLES_NOT_CONCENTRATION", "state": "value_found", "value": round_sig(eq[iV] * P["V"], 5), "unit": "M", "abs_tol": round_sig(window(eq[iV] * P["V"]), 3)})
        # the square-root errors, for a forward run from reactants only: c_p the product's coefficient, c_r each reactant's (1 here)
        a, b = conc[0], conc[1]; c_p = coef[next(i for i, sd in enumerate(side) if sd > 0)]
        if P["version"] == "equal":
            x_one = rx["K"] * a / (c_p + rx["K"]); traps.append({"id": "SQRT_ONE_SIDE", "state": "x_found", "value": round_sig(x_one, 5), "unit": "", "abs_tol": round_sig(window(x_one), 3)})
        if P["version"] == "unequal":
            r = rx["K"] ** 0.5
            for s0 in (a, b): xs = r * s0 / (c_p + r); traps.append({"id": "SQRT_ON_NONSQUARE", "state": "x_found", "value": round_sig(xs, 5), "unit": "", "abs_tol": round_sig(window(xs), 3)})
        if P["kind"] == "no2_equilibrium":            # the sheet's CHANGE_COEFF_IGNORED on x: the change row written -x for NO2, the exponent kept (approved 14 Oct)
            x1 = solve_x_change_ignored(rx, conc, d)
            if _clear(x1, x) and all(_clear(x1, t["value"]) for t in traps if t["state"] == "x_found" and "value" in t):
                traps.append({"id": "CHANGE_COEFF_IGNORED", "state": "x_found", "value": round_sig(x1, 5), "unit": "", "abs_tol": round_sig(window(x1), 3)})
        traps.append({"id": "EXCEEDS_INITIAL", "state": "x_found", "above": round_sig(x_max(rx, conc, d) * 1.02, 5), "unit": ""})
    # ---- the perturbations: the right answer from the reaction record
    perts = [(p[0], p[1], p[2] if len(p) > 2 else {}) for p in PERTURB[P["kind"]]]
    if len(perts) != 2: raise RuntimeError(f"{ID}: {P['kind']} must declare exactly two perturbations")
    pdirs = [perturb_direction(rx, t, s) for t, s, _ in perts]
    for (t, s, named), pd in zip(perts, pdirs):            # a named wrong pick must be wrong
        if any(tag == {1: "forward", -1: "reverse", 0: "neither"}[pd] for tag in named): raise RuntimeError(f"{ID}: {P['id']} names the right answer as an error")
    # ---- the step map
    more = rx["names"][next(i for i, s in enumerate(side) if s > 0)]; dissol = not act[0]
    board = [
      {"state": "account_given",   "kind": "text", "register": "submicro", "requires": []},
      {"state": "relation_chosen", "kind": "pick", "register": "symbolic", "requires": ["account_given"], "options_from": "equation_picks", "pin": True},
    ]
    prev = "relation_chosen"
    if has_conc: board.append({"state": "conc_found", "kind": "number", "register": "symbolic", "requires": [prev], "rule": "all", "pin": True, "explicit": True}); prev = "conc_found"
    if Q is not None: board.append({"state": "Q_found", "kind": "number", "register": "symbolic", "requires": [prev], "explicit": True, "pin": True}); prev = "Q_found"
    board.append({"state": "shift_predicted", "kind": "direction", "register": "macro", "requires": [prev], "options": _dir_opts("direction", more, P.get("named_shift"), dissol), "right": [_dir_id("direction", d)], "explicit": True, "pin": True}); prev = "shift_predicted"
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
           "right": ["method:solver"] if deg > 2 else (["method:" + P["method"]] if P.get("method") else (["method:sqrt"] if P["version"] in ("equal", "products", "all") else ["method:quadratic"]))},
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
    for n, (pd, (_t, _s, named)) in enumerate(zip(pdirs, perts), start=1):
        board += [
          {"state": f"perturb_{n}",     "kind": "direction", "register": "macro",    "requires": [prev], "options": _dir_opts(f"p{n}", more, named, dissol), "right": [_dir_id(f"p{n}", pd)], "explicit": True, "pin": True},
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
        if P.get("V_old"): givens["V_old"] = {"value": P["V_old"], "unit": "L"}
    else:
        givens = {f"c_{sp[i]}": {"value": conc[i], "unit": "M"} for i in range(len(sp)) if act[i] and conc[i]}
    givens["Kc"] = {"value": rx["K"], "unit": ""}
    if dissol: sim_params = {"salt": sp[0], "Ag": conc[1], "X": conc[2], "solid": P.get("solid", 1)}     # the Silent Beaker page's settings (concentrations, also on the 6s)
    else: sim_params = {k: P["mol"][i] for i, k in enumerate(rx["sim_keys"])}; sim_params["V"] = P["V"]
    return {"kind": P["kind"], "fixed_id": P["id"], "version": P["version"], "status": P["status"],
            "context": {"reaction": rx["id"], "family": P["family"], "direction": d, "mode": P["mode"], "sf": P["sf"], "solid": P.get("solid"),
                        "perturbations": [{"type": t, "species": s, "direction": pd, "named": named} for (t, s, named), pd in zip(perts, pdirs)]},
            "text": P["text"], "givens": givens, "board": board, "targets": expected, "traps": traps, "table": table, "words": dict(rx["words"]),
            "eq_checks": eq_checks, "reveal_with_problem": None, "sim": None, "sim_params": sim_params}

def solve_x_change_ignored(rx, conc, d):          # bisection on K = Π(c ± x)^coef with every change written as one x
    lo, hi = 0.0, min(conc[i] for i, s in enumerate(rx["side"]) if s * d < 0 and rx["active"][i]) * 0.999999
    def f(x):
        num = den = 1.0
        for i, s in enumerate(rx["side"]):
            if not rx["active"][i]: continue
            v = conc[i] + s * d * x
            if s > 0: num *= v ** rx["coef"][i]
            else: den *= v ** rx["coef"][i]
        return num / den
    for _ in range(300):
        m = 0.5 * (lo + hi)
        if (f(m) < rx["K"]) == (d > 0): lo = m
        else: hi = m
    return 0.5 * (lo + hi)

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
        bent["COEFF_NOT_EXPONENT"] = states(form(False, True)); bent["EXPONENT_NOT_IN_TABLE"] = states(form(True, False))
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
  "COEFF_NOT_EXPONENT":         {"note": "Their expression holds only with every exponent read as 1: the coefficients are in the table but not used as exponents.", "ask": "The coefficients do double duty. What is the exponent for each species?"},
  "EXPONENT_NOT_IN_TABLE":      {"note": "Their expression holds only with the change row read as ±x for every species: the exponents are there, the table's multiples are not.", "ask": "A coefficient is an exponent here. Is it also in the change row?"},
  "Q_INVERTED":                 {"note": "Their number is 1/Q: reactants over products.", "ask": "Which concentrations go on top of the fraction, and which go underneath?"},
  "COEFFICIENTS_AS_MULTIPLIERS": {"note": "Their number comes from multiplying each concentration by its coefficient instead of raising it to that power.", "ask": "Look at the largest coefficient. In the expression, where does that number go?"},
  "EXPONENTS_DROPPED":          {"note": "Their number is the quotient with every exponent read as 1.", "ask": "Does every species in the expression carry an exponent of 1 here?"},
  "FORWARD_AT_EQUILIBRIUM":     {"note": "They predicted a forward shift although Q equals K to the figures given: they compared the digits, not the figures.", "ask": "How many figures does K carry? To that many, is your Q different from it?"},
  "OLD_VOLUME_USED":            {"note": "Their concentration uses the old volume, before the piston moved.", "ask": "Which volume does the gas fill now?"},
  "SHIFT_ON_EQUAL_MOLES":       {"note": "They predicted a shift after a volume change although both sides have the same number of gas moles.", "ask": "Count the gas molecules on each side of the arrow. Did Q change when the volume did?"},
  "FORWARD_ON_COMMON_ION":      {"note": "They predicted more dissolving after a product ion was added.", "ask": "The added ion is on which side of the equation? What happens to collisions between ions in the water?"},
}

def render_text(*a): raise NotImplementedError("fixed problems carry their own text")
