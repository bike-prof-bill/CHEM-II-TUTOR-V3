"""Chapter 16, Free energy: ΔG° two ways, and coupled reactions. A sheet-driven archetype: SCENARIO_CLAUDE's approved sheet (18 Oct 2026) supplies every problem's expected
values, named mistakes and right picks (archetypes/data/sheets/ch16_free_energy.json); this file gives the step order, the pick options and the
registers. test_ch16.py re-derives the numbers from each problem sentence. Picks are `direction` items whose option texts begin with the
bare word the student may type."""
import math
from engine import round_sig
from _sheet import *

ID = "ch16_free_energy"
TITLE = 'Free energy: ΔG° two ways, and coupled reactions'
RELATION_TEXT = 'ΔG° = ΔH° − TΔS°, or the sum of ΔG°f(products) minus ΔG°f(reactants); coupled reactions add their ΔG°'
KINDS = ['two_routes', 'coupled']
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

EQUATION_PICKS = picks({'eq_dg': ['two_routes'], 'eq_dgf': ['two_routes', 'coupled']})
CONSTANTS = [{"label": "R", "symbol": "R", "value": 8.314, "unit": "J/K"}]
EQUATION_SYMBOLS = {"T": ["T"], "K": ["K", "Ksp", "Kp"]}; EQUATION_CONSTANTS = {"R": 8.314}
MECHANISM_WORDS = ['energ', 'bond', 'enthalp', 'entrop', 'heat', 'free', 'spontan', 'molecul', 'gas', 'liquid', 'order', 'disorder', 'coupl', 'driv']
TRAP_NOTES = TRAP_NOTES_CH16
PROBLEMS = load(ID)
FIXED = [{"id": p["id"], "kind": p["kind"], "version": "", "status": p["status"], "text": p["text"]} for p in PROBLEMS]
STEPS = ['dH_found', 'dS_found', 'dG1_found', 'dG2_found', 'dG_found', 'dGf_found', 'verdict', 'perturb_1']
PICK_NAMED = {'perturb_1': 'EXTENSIVE_IGNORED'}
SIM = lambda P: {'reaction': P['id'], 'T': 298}
def make_fixed(rng, fid): return make_fixed_from_sheet(ID, PROBLEMS, fid, STEPS, PICK_NAMED, SIM, no_key=True)   # the two routes to ΔG° agree by design, so neither is the one key value
def render_text(*a): raise NotImplementedError
