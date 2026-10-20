"""Chapter 16, Entropy and spontaneity: the system, the surroundings and the universe. A sheet-driven archetype: SCENARIO_CLAUDE's approved sheet (18 Oct 2026) supplies every problem's expected
values, named mistakes and right picks (archetypes/data/sheets/ch16_entropy.json); this file gives the step order, the pick options and the
registers. test_ch16.py re-derives the numbers from each problem sentence. Picks are `direction` items whose option texts begin with the
bare word the student may type."""
import math, re
from engine import round_sig
from _sheet import *

ID = "ch16_entropy"
TITLE = 'Entropy and spontaneity: the system, the surroundings and the universe'
RELATION_TEXT = 'ΔS(univ) = ΔS(sys) + ΔS(surr); ΔS(surr) = −ΔH(sys)/T; a process is spontaneous when ΔS(univ) is positive'
KINDS = ['given', 'from_table']
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

EQUATION_PICKS = picks({'eq_dsuniv': ['given', 'from_table'], 'eq_dssurr': ['given', 'from_table']})
CONSTANTS = [{"label": "R", "symbol": "R", "value": 8.314, "unit": "J/K"}]
EQUATION_SYMBOLS = {"T": ["T"], "K": ["K", "Ksp", "Kp"]}; EQUATION_CONSTANTS = {"R": 8.314}
MECHANISM_WORDS = ['entrop', 'disorder', 'arrang', 'microstat', 'spread', 'dispers', 'heat', 'surround', 'system', 'univers', 'molecul', 'gas', 'liquid', 'solid', 'order', 'random']
TRAP_NOTES = TRAP_NOTES_CH16
PROBLEMS = load(ID)
FIXED = [{"id": p["id"], "kind": p["kind"], "version": "", "status": p["status"], "text": p["text"]} for p in PROBLEMS]
STEPS = ['dSsys_found', 'sign_pick', 'dSsurr_found', 'dSuniv_found', 'verdict', 'perturb_1']
PICK_NAMED = {'sign_pick': 'SIGN_PICK_WRONG', 'verdict': 'SPONTANEITY_FROM_SYSTEM'}
SIM = lambda P: clean_params({'process': match_reaction(P['text'], SIM_IDS['entropy']), 'T': temperature_K(P['text'])})
def make_fixed(rng, fid): return make_fixed_from_sheet(ID, PROBLEMS, fid, STEPS, PICK_NAMED, SIM)
def render_text(*a): raise NotImplementedError
