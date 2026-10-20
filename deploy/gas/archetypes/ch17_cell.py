"""Chapter 17, Galvanic cells: anode, cathode, the wire and the bridge, and E°cell. A sheet-driven archetype (SCENARIO_CLAUDE's design and sheet, approved 18 Oct 2026; archetypes/data/sheets/ch17_cell.json).
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

ID = "ch17_cell"
TITLE = 'Galvanic cells: anode, cathode, the wire and the bridge, and E°cell'
RELATION_TEXT = 'E°cell = E°cathode − E°anode; electrons leave the anode through the wire; anions move toward the anode in the bridge'
KINDS = ['cell', 'reaction']
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

EQUATION_PICKS = picks({'eq_ecell': ['cell', 'reaction']})
CONSTANTS = [{"label": "F", "symbol": "F", "value": 96485, "unit": ""}, {"label": "0.0592 V", "symbol": "RT_F", "value": 0.0592, "unit": "V"}]
EQUATION_SYMBOLS = {"n": ["n"], "E": ["E", "Ecell"], "Q": ["Q"]}; EQUATION_CONSTANTS = {"F": 96485}
MECHANISM_WORDS = ['electron', 'oxid', 'reduc', 'anode', 'cathode', 'ion', 'wire', 'bridge', 'flow', 'lose', 'gain', 'metal', 'dissolv', 'deposit', 'charge']
TRAP_NOTES = TRAP_NOTES_CH17
PROBLEMS = load(ID)
FIXED = [{"id": p["id"], "kind": p["kind"], "version": "", "status": p["status"], "text": p["text"]} for p in PROBLEMS]
STEPS = ['anode_pick', 'electron_pick', 'bridge_pick', 'Ecell_found', 'verdict', 'perturb_1']
PICK_NAMED = {}

def PICK_OPTIONS(P, st, right):
    if st == "anode_pick":
        two = _two(_metals(P), right); return [{"id": m, "text": f"{m}: the {m} electrode is oxidised"} for m in two]
    if st == "electron_pick":
        m = _re.match(r"from (\S+) to (\S+)", right)
        if m: a, b = m.group(1), m.group(2); return [{"id": right, "text": f"{a} to {b}: electrons leave {a} and arrive at {b}"}, {"id": f"from {b} to {a}", "text": f"{b} to {a}: electrons leave {b} and arrive at {a}"}]
    if st == "bridge_pick":
        m = _re.match(r"toward (\S+)", right)
        if m: a = m.group(1); others = [x for x in _metals(P) if x != a][:1]; b = others[0] if others else "the cathode"
        return [{"id": right, "text": f"{a} side: anions move toward {a}"}, {"id": f"toward {b}", "text": f"{b} side: anions move toward {b}"}]
    if st == "perturb_1" and right == "changes sign": return [{"id": "changes sign", "text": "changes sign: the same size, the other way"}, {"id": "stays", "text": "stays the same"}, {"id": "doubles", "text": "doubles"}]
    return None
def TOLERANCE(P, st, value, unit): return 0.01 if unit == "V" else None
SIM = lambda P: clean_params({'left': cell_metals(P['text'])[0] or P['picks'].get('anode_pick', ''), 'right': cell_metals(P['text'])[1] or next((m for m in _metals(P) if m != P['picks'].get('anode_pick')), ''), 'cl': 1, 'cr': 1})
def make_fixed(rng, fid): return make_fixed_from_sheet(ID, PROBLEMS, fid, STEPS, PICK_NAMED, SIM, pick_options=PICK_OPTIONS, tolerance=TOLERANCE)
def render_text(*a): raise NotImplementedError
