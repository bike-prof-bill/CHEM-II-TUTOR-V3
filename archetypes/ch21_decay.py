"""Chapter 21, Radioactive decay and half-life. A sheet-driven archetype (SCENARIO_CLAUDE's design and sheet, approved 18 Oct 2026; archetypes/data/sheets/ch21_decay.json).
Tolerance ±1 % on the numbers (instructor); counts are exact. test_ch19_21.py re-derives the numbers from the sentences."""
import math, re
from engine import round_sig
from _sheet import *

ID = "ch21_decay"
TITLE = 'Radioactive decay and half-life'
RELATION_TEXT = 'λ = 0.693/t½; ln(Nₜ/N₀) = −λt'
KINDS = ['fraction', 'time', 'dating', 'rock']
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

EQUATION_PICKS = picks({'eq_halflife': ['fraction', 'time', 'dating', 'rock'], 'eq_decay': ['fraction', 'time', 'dating', 'rock']})
CONSTANTS = [{"label": "h", "symbol": "h", "value": 6.626e-34, "unit": ""}, {"label": "c", "symbol": "c", "value": 2.998e8, "unit": ""}, {"label": "Nₐ", "symbol": "NA", "value": 6.022e23, "unit": ""}]
EQUATION_SYMBOLS = {"E": ["E"], "t": ["t"]}; EQUATION_CONSTANTS = {}
MECHANISM_WORDS = ['nucle', 'nucleus', 'decay', 'half', 'random', 'probab', 'atom', 'emit', 'radioact', 'fraction', 'isotope', 'parent', 'daughter']
TRAP_NOTES = dict(TRAP_NOTES_CH16, **TRAP_NOTES_CH17, **TRAP_NOTES_CH19_21)
PROBLEMS = load(ID)
FIXED = [{"id": p["id"], "kind": p["kind"], "version": "", "status": p["status"], "text": p["text"]} for p in PROBLEMS]
STEPS = {'fraction': ['lambda_found', 'fraction_found', 'mass_found', 'perturb_1'], 'time': ['lambda_found', 'ratio_found', 'time_found', 'perturb_1'], 'dating': ['lambda_found', 'ratio_found', 'time_found', 'perturb_1'], 'rock': ['mol_now_found', 'mol_decayed_found', 'ratio_found', 'time_found', 'perturb_1']}
PICK_NAMED = {}

def PICK_OPTIONS(P, st, right): return None
def TOLERANCE(P, st, value, unit): return max(0.01 * abs(value), 1e-30)                  # ±1 % (instructor)
SIM = lambda P: clean_params({'isotope': isotope_of(P['text']), 'mode': {'fraction': 'decay', 'time': 'dating', 'dating': 'dating', 'rock': 'rock'}[P['kind']], 't': first_number(P['text'], r'after ([0-9.]+(?:e[+-]?\d+)?) ') or next((e['value'] for e in P['expected'] if e['state'] == 'time_found'), None), 'ratio': next((e['value'] for e in P['expected'] if e['state'] == 'ratio_found'), None), 'm0': first_number(P['text'], r'([0-9.]+) g sample') or first_number(P['text'], r'sample of ([0-9.]+) g') or first_number(P['text'], r'starts with ([0-9.]+) g'), 'parent': (re.search(r'(U-238|Rb-87)', P['text']) or [None, ''])[1] if re.search(r'(U-238|Rb-87)', P['text']) else '', 'gp': first_number(P['text'], r'([0-9.]+(?:e[+-]?\d+)?) g of (?:U-238|Rb-87)'), 'gd': first_number(P['text'], r'([0-9.]+(?:e[+-]?\d+)?) g of (?:Pb-206|Sr-87)')})
def make_fixed(rng, fid): return make_fixed_from_sheet(ID, PROBLEMS, fid, STEPS, PICK_NAMED, SIM, pick_options=PICK_OPTIONS, tolerance=TOLERANCE)
def render_text(*a): raise NotImplementedError
