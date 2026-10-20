"""Chapter 17, Balancing redox equations by half-reactions. A sheet-driven archetype (SCENARIO_CLAUDE's design and sheet, approved 18 Oct 2026; archetypes/data/sheets/ch17_balancing.json).
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

ID = "ch17_balancing"
TITLE = 'Balancing redox equations by half-reactions'
RELATION_TEXT = 'split into two half-reactions, balance atoms then charge with electrons, match the electrons, add; in base, hydroxide and water'
KINDS = ['acid', 'base']
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

EQUATION_PICKS = picks({})
CONSTANTS = [{"label": "F", "symbol": "F", "value": 96485, "unit": ""}, {"label": "0.0592 V", "symbol": "RT_F", "value": 0.0592, "unit": "V"}]
EQUATION_SYMBOLS = {"n": ["n"], "E": ["E", "Ecell"], "Q": ["Q"]}; EQUATION_CONSTANTS = {"F": 96485}
MECHANISM_WORDS = ['electron', 'lose', 'gain', 'oxid', 'reduc', 'transfer', 'half', 'atom', 'charge', 'balance', 'ion', 'metal', 'dissolv']
TRAP_NOTES = TRAP_NOTES_CH17
PROBLEMS = load(ID)
FIXED = [{"id": p["id"], "kind": p["kind"], "version": "", "status": p["status"], "text": p["text"]} for p in PROBLEMS]
STEPS = ['oxidized_pick', 'e_ox_found', 'e_red_found', 'n_found', 'coeffs_found', 'perturb_1']
PICK_NAMED = {}

ELEMENTS = {"Ag","Al","Br","C","Cl","Cr","Cu","Fe","I","N","O","S","Sn","Zn","Mn","Pb","H","Ni","Co","Mg","Cd","Hg","Au","Pt","Na","K","Ca","P","Si","Bi","Sb","As","Se","Ti","V"}
def _oxidized_options(P, right):
    """The elements in the reactants, as the choices for 'which element is oxidised'."""
    lhs = P["text"].split("→")[0]
    els = []
    for m in _re.finditer(r"[A-Z][a-z]?", lhs.split("reaction")[-1] if "reaction" in lhs else lhs):
        e = m.group(0)
        if e in ELEMENTS and e not in els and e not in ("H", "O"): els.append(e)
    if right not in els: els.insert(0, right)
    return [{"id": e, "text": f"{e}: the {e} atoms lose electrons"} for e in els[:5]]
def PICK_OPTIONS(P, st, right):
    if st == "oxidized_pick": return _oxidized_options(P, right)
    if st == "perturb_1": return [{"id": "H⁺", "text": "H⁺: hydrogen is balanced with hydrogen ions (acid)"}, {"id": "OH⁻", "text": "OH⁻: in base, hydroxide ions and water balance the hydrogen"}]
    return None
def TOLERANCE(P, st, value, unit):
    return 0.1 if st in ("e_ox_found", "e_red_found", "n_found") else None            # exact integers
SIM = lambda P: {}
def make_fixed(rng, fid): return make_fixed_from_sheet(ID, PROBLEMS, fid, STEPS, PICK_NAMED, SIM, pick_options=PICK_OPTIONS, tolerance=TOLERANCE, relation=False)   # no Equations list step: balancing has no relation to pick (approved)
def render_text(*a): raise NotImplementedError
