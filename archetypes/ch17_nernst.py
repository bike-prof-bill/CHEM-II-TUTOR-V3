"""Chapter 17, The Nernst equation. A sheet-driven archetype (SCENARIO_CLAUDE's design and sheet, approved 18 Oct 2026; archetypes/data/sheets/ch17_nernst.json).
This file gives the step order, the pick options (built from each problem's own sentence where the choices are problem-specific) and the
tolerances the instructor set. test_ch17.py re-derives the numbers from the sentences and Appendix L."""
import math
from engine import round_sig
from _sheet import *

import re as _re
def _metals(P):
    """The two electrode metals of a cell problem, from 'X electrode' or 'X(s)' in the sentence; the right pick first if found."""
    found = []
    for m in _re.finditer(r"\b([A-Z][a-z]?)(?:\(s\)| electrode| metal)", P["text"]):
        if m.group(1) not in found: found.append(m.group(1))
    return found
def _two(found, right):
    other = [x for x in found if x != right]
    return [right] + other[:1] if other else [right]

ID = "ch17_nernst"
TITLE = 'The Nernst equation'
RELATION_TEXT = 'E = E°cell − (0.0592 V/n) log Q at 25 °C'
KINDS = ['cell', 'concentration']
EQ = [
  {"id": "eq_ecell", "text": r"\( E^\circ_{cell} = E^\circ_{cathode} - E^\circ_{anode} \)"},
  {"id": "eq_dg_nfe", "text": r"\( \Delta G^\circ = -nFE^\circ_{cell} \)"},
  {"id": "eq_k_e",   "text": r"\( K = 10^{\,nE^\circ_{cell}/0.0592\ \mathrm{V}} \)"},
  {"id": "eq_nernst", "text": r"\( E = E^\circ_{cell} - \dfrac{0.0592\ \mathrm{V}}{n}\log Q \)"},
  {"id": "eq_charge", "text": r"\( Q = It \)"},
  {"id": "eq_faraday", "text": r"\( n_{e^-} = \dfrac{Q}{F} \)"},
  {"id": "eq_dgk",   "text": r"\( \Delta G^\circ = -RT \ln K \)"},
  {"id": "eq_k",     "text": r"\( K = \dfrac{[\mathrm{C}]^{c}[\mathrm{D}]^{d}}{[\mathrm{A}]^{a}[\mathrm{B}]^{b}} \)"},
]
def picks(fits): return [dict(e, fits=fits.get(e["id"], [])) for e in EQ]

EQUATION_PICKS = picks({'eq_nernst': ['cell', 'concentration'], 'eq_ecell': ['cell', 'concentration']})
CONSTANTS = [{"label": "F", "symbol": "F", "value": 96485, "unit": ""}, {"label": "0.0592 V", "symbol": "RT_F", "value": 0.0592, "unit": "V"}]
EQUATION_SYMBOLS = {"n": ["n"], "E": ["E", "Ecell"], "Q": ["Q"]}; EQUATION_CONSTANTS = {"F": 96485}
MECHANISM_WORDS = ['electron', 'ion', 'concentrat', 'oxid', 'reduc', 'quotient', 'equilibr', 'driv', 'flow', 'wire', 'metal', 'dilut']
TRAP_NOTES = TRAP_NOTES_CH17
PROBLEMS = load(ID)
FIXED = [{"id": p["id"], "kind": p["kind"], "version": "", "status": p["status"], "text": p["text"]} for p in PROBLEMS]
STEPS = ['Ecell0_found', 'n_found', 'Q_found', 'E_found', 'verdict', 'perturb_1']
PICK_NAMED = {}

def PICK_OPTIONS(P, st, right):
    if st == "verdict": return [{"id": "yes", "text": "yes: E is positive, spontaneous as written"}, {"id": "no", "text": "no: E is negative, not spontaneous as written"}, {"id": "neither", "text": "neither: E is zero, the cell is at equilibrium"}]
    return None
def TOLERANCE(P, st, value, unit):
    if st == "n_found": return 0.1
    if unit == "V": return 0.01
    return None
SIM = lambda P: nernst_params(P)
def make_fixed(rng, fid): return make_fixed_from_sheet(ID, PROBLEMS, fid, STEPS, PICK_NAMED, SIM, pick_options=PICK_OPTIONS, tolerance=TOLERANCE)
def render_text(*a): raise NotImplementedError
