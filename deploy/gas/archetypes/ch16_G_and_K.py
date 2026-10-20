"""Chapter 16, Free energy and the equilibrium constant. A sheet-driven archetype: SCENARIO_CLAUDE's approved sheet (18 Oct 2026) supplies every problem's expected
values, named mistakes and right picks (archetypes/data/sheets/ch16_G_and_K.json); this file gives the step order, the pick options and the
registers. test_ch16.py re-derives the numbers from each problem sentence. Picks are `direction` items whose option texts begin with the
bare word the student may type."""
import math, re
from engine import round_sig
from _sheet import *

ID = "ch16_G_and_K"
TITLE = 'Free energy and the equilibrium constant'
RELATION_TEXT = 'ΔG° = −RT ln K, so K = e^(−ΔG°/RT); a negative ΔG° means K above 1 and products favored'
KINDS = ['K_from_G', 'G_from_K']
EQ = [
  {"id": "eq_dsuniv", "text": r"\( \Delta S_{univ} = \Delta S_{sys} + \Delta S_{surr} \)"},
  {"id": "eq_dssurr", "text": r"\( \Delta S_{surr} = \dfrac{-\Delta H_{sys}}{T} \)"},
  {"id": "eq_dg",     "text": r"\( \Delta G^\circ = \Delta H^\circ - T\Delta S^\circ \)"},
  {"id": "eq_dgf",    "text": r"\( \Delta G^\circ = \sum \Delta G^\circ_f(\text{products}) - \sum \Delta G^\circ_f(\text{reactants}) \)"},
  {"id": "eq_dgq",    "text": r"\( \Delta G = \Delta G^\circ + RT \ln Q \)"},
  {"id": "eq_dgk",    "text": r"\( \Delta G^\circ = -RT \ln K \)"},
  {"id": "eq_cc",     "text": r"\( \ln\dfrac{P_2}{P_1} = -\dfrac{\Delta H}{R}\left(\dfrac{1}{T_2} - \dfrac{1}{T_1}\right) \)"},
  {"id": "eq_k",      "text": r"\( K = \dfrac{[\mathrm{C}]^{c}[\mathrm{D}]^{d}}{[\mathrm{A}]^{a}[\mathrm{B}]^{b}} \)"},
]
def picks(fits):
    return [dict(e, fits=fits.get(e["id"], [])) for e in EQ]

EQUATION_PICKS = picks({'eq_dgf': ['K_from_G'], 'eq_dgk': ['K_from_G', 'G_from_K']})
CONSTANTS = [{"label": "R", "symbol": "R", "value": 8.314, "unit": "J/K"}]
EQUATION_SYMBOLS = {"T": ["T"], "K": ["K", "Ksp", "Kp"]}; EQUATION_CONSTANTS = {"R": 8.314}
MECHANISM_WORDS = ['energ', 'free', 'equilibr', 'constant', 'product', 'reactant', 'favor', 'molecul', 'ion', 'dissolv', 'gas', 'forward', 'reverse', 'rate', 'equal']
TRAP_NOTES = TRAP_NOTES_CH16
PROBLEMS = load(ID)
FIXED = [{"id": p["id"], "kind": p["kind"], "version": "", "status": p["status"], "text": p["text"]} for p in PROBLEMS]
STEPS = ['dG0_found', 'K_found', 'favored', 'perturb_1']
PICK_NAMED = {}
SIM = lambda P: clean_params({'reaction': reaction_for_page(P, 'G_and_Q')})
def make_fixed(rng, fid): return make_fixed_from_sheet(ID, PROBLEMS, fid, STEPS, PICK_NAMED, SIM)
def render_text(*a): raise NotImplementedError
