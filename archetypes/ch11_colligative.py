"""Chapter 11, Freezing point depression (colligative properties of electrolytes). The chapter 11 pilot, built to brief 32: SCENARIO_CLAUDE's
sheet The Salted Road (approved 21 Oct 2026; archetypes/data/sheets/ch11_colligative.json). No relation pick: the step order is the
instructor's (account, moles, molality, i, the lowering, the freezing point, the prediction that opens the page, the reading taken on the
page, the gap question, the change of salt and why, the meaning). test_ch11.py re-derives every number from the sentence and Appendix A."""
from engine import round_sig
from _sheet import *

ID = "ch11_colligative"
TITLE = 'Freezing point depression: why salt melts ice, and by how many degrees'
RELATION_TEXT = 'ΔT_f = i K_f m; T_f(solution) = T_f(solvent) − ΔT_f; m = moles of solute per kilogram of solvent; i = ions per formula unit'
KINDS = ['freezing']
EQ = [
  {"id": "eq_dTf", "text": r"\( \Delta T_f = i\,K_f\,m \)"},
  {"id": "eq_molality", "text": r"\( m = \dfrac{\text{moles of solute}}{\text{kilograms of solvent}} \)"},
  {"id": "eq_Tf", "text": r"\( T_f = 0\ ^\circ\text{C} - \Delta T_f \)"},
]
EQUATION_PICKS = [dict(e, fits=["freezing"]) for e in EQ]     # shown in the Equations list; no pick step asks for one (the instructor's step order)
CONSTANTS = [{"label": "K_f (water)", "symbol": "Kf", "value": 1.86, "unit": "°C·kg/mol"}]
EQUATION_SYMBOLS = {"m": ["m", "molality"], "i": ["i"], "Kf": ["Kf", "K_f"], "dT": ["ΔT", "dT", "ΔTf", "dTf"]}; EQUATION_CONSTANTS = {"Kf": 1.86}
MECHANISM_WORDS = ['ion', 'molecule', 'block', 'crowd', 'interfer', 'dilut', 'space', 'fewer', 'reach', 'disrupt', 'slow', 'rate', 'freez', 'melt', 'surface', 'rejoin', 'refreez']
TRAP_NOTES = {}                                                 # every ask is in content_ch11_colligative_errors.csv (approved)
PROBLEMS = load(ID)
FIXED = [{"id": p["id"], "kind": p["kind"], "version": "", "status": p["status"], "text": p["text"]} for p in PROBLEMS]
STEPS = ['mol_found', 'm_found', 'i_found', 'dT_found', 'T_found', 'sim_predict', 'sim_instrument', 'sim_gap', 'perturb_1']
SIM_STUDENT = {"T_student": "T_found", "pred": "sim_predict"}   # the page's placeholders for the reveal (docs/04, 21 Oct)
# Two steps whose question the sheet gives per problem (brief 32 columns `sim instrument` and `sim gap question`); the instrument's
# student-facing sentence is the instructor's (approved 21 Oct, docs/35), with the problem's own water and the page's target reading.
PRECISION_RULE = True                                           # accept a value at the student's own precision (instructor, 21 Oct): 1.3, 1.35 and 1.347 for 1.3472; chapter 11 only while experimental
STAGE_PER_STEP = True                                           # the 21 Oct ladder counts wrong tries per step; the sheet's stage column is a label only
EXTRA_MOVES = {
  "reflection": {"stage": "close", "label_when_done": "Reflection written", "ask": "Which step was hardest for you? In one sentence, what would you tell a friend who is stuck there?",
                 "status": "approved (instructor, 18 Oct 2026; the standing reflection row of every archetype)"},
  "sim_instrument": {"stage": "simulation", "label_when_done": "Reading taken from the page",
                     "ask": "Move the salt slider until the freezing point reads {target} °C. How many grams of this salt must the crew dissolve in the problem's {water_kg} kg of meltwater for the brine to stay liquid down to {target} °C? Type the grams you read.",
                     "status": "APPROVED (instructor, 21 Oct 2026)"},
  "sim_gap": {"stage": "simulation", "label_when_done": "Gap explained", "ask": "{gap_question}", "status": "APPROVED (instructor, 21 Oct 2026)"},
}
def TOLERANCE(P, st, value, unit):
    if st == "i_found": return 0.01                             # an exact count
    return None                                                 # the sheet's precision, then the default window
def make_fixed(rng, fid): return make_fixed_from_sheet(ID, PROBLEMS, fid, STEPS, {}, None, {"sim_instrument": "macro"}, key_state="T_found", tolerance=TOLERANCE, relation=False, sim_student=SIM_STUDENT, drop_restated=True)
def render_text(*a): raise NotImplementedError
