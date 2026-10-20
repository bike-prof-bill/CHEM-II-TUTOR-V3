"""Chapter 19, Crystal field theory: d electrons, spin, magnetism and colour. A sheet-driven archetype (SCENARIO_CLAUDE's design and sheet, approved 18 Oct 2026; archetypes/data/sheets/ch19_cft.json).
Tolerance ±1 % on the numbers (instructor); counts are exact. test_ch19_21.py re-derives the numbers from the sentences."""
import math
from engine import round_sig
from _sheet import *

import re as _re
def _complex_id(P):     # "[Fe(H₂O)₆]²⁺" -> "Fe(H2O)6_2+" (the page's id; the shell URL-encodes the "+")
    m = _re.search(r"\[([^\]]+)\]([⁰¹²³⁴⁵⁶⁷⁸⁹]*[⁺⁻])?", P["text"])
    if not m: return ""
    body = m.group(1).translate(str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")); ch = (m.group(2) or "").translate(str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻", "0123456789+-"))
    return body + ("_" + ch if ch else "")
ID = "ch19_cft"
TITLE = 'Crystal field theory: d electrons, spin, magnetism and colour'
RELATION_TEXT = 'd count from the oxidation state; strong-field ligands pair electrons in t₂g (low spin); Δoct = hc/λ per ion, times Nₐ per mole'
KINDS = ['spin', 'colour', 'geometry']
EQ = [
  {"id": "eq_ehc",   "text": r"\( E = \dfrac{hc}{\lambda} \)"},
  {"id": "eq_cfse",  "text": r"\( \Delta_{oct} \text{ per mole} = N_A \times \Delta_{oct} \text{ per ion} \)"},
  {"id": "eq_ox",    "text": r"\( \text{oxidation state} = \text{charge of the complex} - \sum \text{ligand charges} \)"},
  {"id": "eq_halflife", "text": r"\( t_{1/2} = \dfrac{0.693}{\lambda} \)"},
  {"id": "eq_decay", "text": r"\( \ln\dfrac{N_t}{N_0} = -\lambda t \)"},
  {"id": "eq_emc2",  "text": r"\( E = mc^2 \)"},
  {"id": "eq_defect", "text": r"\( \Delta m = Z m_p + N m_n + Z m_e - m_{atom} \)"},
  {"id": "eq_k",     "text": r"\( K = \dfrac{[\mathrm{C}]^{c}[\mathrm{D}]^{d}}{[\mathrm{A}]^{a}[\mathrm{B}]^{b}} \)"},
]
def picks(fits): return [dict(e, fits=fits.get(e["id"], [])) for e in EQ]

EQUATION_PICKS = picks({'eq_ox': ['spin', 'geometry'], 'eq_ehc': ['colour']})
CONSTANTS = [{"label": "h", "symbol": "h", "value": 6.626e-34, "unit": ""}, {"label": "c", "symbol": "c", "value": 2.998e8, "unit": ""}, {"label": "Nₐ", "symbol": "NA", "value": 6.022e23, "unit": ""}]
EQUATION_SYMBOLS = {"E": ["E"], "t": ["t"]}; EQUATION_CONSTANTS = {}
MECHANISM_WORDS = ['electron', 'd ', 'orbital', 'split', 'ligand', 'field', 'pair', 'unpaired', 'spin', 'absorb', 'light', 'colour', 'color', 'energy', 'magnet']
TRAP_NOTES = dict(TRAP_NOTES_CH16, **TRAP_NOTES_CH17, **TRAP_NOTES_CH19_21)
PROBLEMS = load(ID)
FIXED = [{"id": p["id"], "kind": p["kind"], "version": "", "status": p["status"], "text": p["text"]} for p in PROBLEMS]
STEPS = {'spin': ['ox_found', 'd_found', 'field_pick', 'spin_pick', 't2g_found', 'eg_found', 'unpaired_found', 'magnetic_pick', 'perturb_1'], 'colour': ['deltaJ_found', 'deltakJ_found', 'colour_pick', 'compare_pick', 'perturb_1'], 'geometry': ['ox_found', 'd_found', 'unpaired_found', 'magnetic_pick', 'perturb_1']}
PICK_NAMED = {}

COLOURS = ["purple", "violet", "blue", "green", "yellow", "orange", "red"]
def PICK_OPTIONS(P, st, right):
    if st == "field_pick": return [{"id": "weak", "text": "weak: a weak-field ligand, small splitting"}, {"id": "strong", "text": "strong: a strong-field ligand, large splitting"}]
    if st == "spin_pick": return [{"id": "high", "text": "high: high-spin, electrons spread out unpaired"}, {"id": "low", "text": "low: low-spin, electrons paired in t₂g"}, {"id": "no choice", "text": "no choice: the d count leaves only one arrangement"}]
    if st == "magnetic_pick": return [{"id": "paramagnetic", "text": "paramagnetic: unpaired electrons, drawn into a field"}, {"id": "diamagnetic", "text": "diamagnetic: all electrons paired"}]
    if st == "colour_pick": return [{"id": c, "text": f"{c}"} for c in COLOURS]
    if st == "compare_pick": return [{"id": "larger", "text": "larger: a bigger splitting"}, {"id": "smaller", "text": "smaller: a smaller splitting"}]
    return None
def TOLERANCE(P, st, value, unit):
    if st in ("ox_found", "d_found", "t2g_found", "eg_found", "unpaired_found"): return 0.1
    return max(0.01 * abs(value), 1e-30)                                                  # ±1 % (instructor)
SIM = lambda P: {'complex': _complex_id(P)}
def make_fixed(rng, fid): return make_fixed_from_sheet(ID, PROBLEMS, fid, STEPS, PICK_NAMED, SIM, pick_options=PICK_OPTIONS, tolerance=TOLERANCE)
def render_text(*a): raise NotImplementedError
