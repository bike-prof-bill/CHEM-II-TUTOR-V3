"""Chapter 21, Nuclear binding energy. A sheet-driven archetype (SCENARIO_CLAUDE's design and sheet, approved 18 Oct 2026; archetypes/data/sheets/ch21_binding.json).
Tolerance ±1 % on the numbers (instructor); counts are exact. test_ch19_21.py re-derives the numbers from the sentences."""
import math, re
from engine import round_sig
from _sheet import *

ID = "ch21_binding"
TITLE = 'Nuclear binding energy'
RELATION_TEXT = 'mass defect = Z(mp + me) + N mn − m(atom); E = Δm c²; 1 amu = 931.5 MeV; per nucleon = E/A'
KINDS = ['binding']
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

EQUATION_PICKS = picks({'eq_defect': ['binding'], 'eq_emc2': ['binding']})
CONSTANTS = [{"label": "h", "symbol": "h", "value": 6.626e-34, "unit": ""}, {"label": "c", "symbol": "c", "value": 2.998e8, "unit": ""}, {"label": "Nₐ", "symbol": "NA", "value": 6.022e23, "unit": ""}]
EQUATION_SYMBOLS = {"E": ["E"], "t": ["t"]}; EQUATION_CONSTANTS = {}
MECHANISM_WORDS = ['nucle', 'nucleus', 'proton', 'neutron', 'mass', 'defect', 'bind', 'energy', 'strong force', 'held', 'nucleon', 'fusion', 'fission', 'iron']
TRAP_NOTES = dict(TRAP_NOTES_CH16, **TRAP_NOTES_CH17, **TRAP_NOTES_CH19_21)
PROBLEMS = load(ID)
FIXED = [{"id": p["id"], "kind": p["kind"], "version": "", "status": p["status"], "text": p["text"]} for p in PROBLEMS]
STEPS = ['Z_found', 'N_found', 'defect_found', 'EJ_found', 'EMeV_found', 'per_found', 'perturb_1']
PICK_NAMED = {}

def PICK_OPTIONS(P, st, right):
    if st == "perturb_1": return [{"id": "yes", "text": "yes: a larger total always means more per nucleon"}, {"id": "no", "text": "no: per nucleon peaks near iron and then falls"}]
    return None
def TOLERANCE(P, st, value, unit):
    if st in ("Z_found", "N_found"): return 0.1
    return max(0.01 * abs(value), 1e-30)                                                  # ±1 % (instructor)
SIM = lambda P: clean_params({'nuclide': nuclide_of(P['text'])})
def make_fixed(rng, fid): return make_fixed_from_sheet(ID, PROBLEMS, fid, STEPS, PICK_NAMED, SIM, pick_options=PICK_OPTIONS, tolerance=TOLERANCE)
def render_text(*a): raise NotImplementedError
