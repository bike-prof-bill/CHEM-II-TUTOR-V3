"""Chapter 14, archetype 1 of 4: pH & pOH (strong acids and bases). Fixed problems; placeholders DRAFT; ships nothing until a
scenario is approved. Step map: account -> relation (pH = -log[H3O+]) -> ion_found (the ion concentration from the formula, counting
ions per formula unit) -> pH_found -> pOH_found -> perturb_1 (tenfold dilution: pH rises | falls | unchanged) -> why -> meaning -> reflection.
"""
import math
from engine import round_sig
from _acidbase import *

ID = "ch14_ph"
TITLE = "pH and pOH: strong acids and bases"
RELATION_TEXT = "pH = -log[H3O+]; pOH = -log[OH-]; pH + pOH = 14.00 at 25 °C; a strong acid or base is fully ionised"
KINDS = ["strong_acid", "strong_base"]
EQUATION_PICKS = picks({"eq_ph": KINDS, "eq_kw": KINDS})
CONSTANTS = [{"label": "Kw", "symbol": "Kw", "value": KW, "unit": ""}]
EQUATION_SYMBOLS = {"pH": ["pH"], "pOH": ["pOH"]}; EQUATION_CONSTANTS = {"Kw": KW}
MECHANISM_WORDS = MECHANISM_WORDS
TRAP_NOTES = TRAP_NOTES_COMMON

def _p(fid, formula, conc, text, family):
    s = strong(formula); return {"id": fid, "kind": "strong_" + s["kind"], "strong": formula, "conc": conc, "text": text, "family": family, "version": "", "sf": 2, "status": DRAFT}
FIXED = [
  _p("S1", "HCl", 0.0025, "A technician dissolves hydrochloric acid in water to make 0.0025 M HCl at 25 °C. The probe reads a pH. Find [H3O+], the pH and the pOH.", "strong acid"),
  _p("S2", "NaOH", 0.010, "A cleaning bath is 0.010 M sodium hydroxide at 25 °C. Find [OH-], the pOH and the pH.", "strong base"),
  _p("S3", "Ba(OH)2", 0.0050, "A saturated limewater stand-in is 0.0050 M barium hydroxide at 25 °C. Find [OH-], the pOH and the pH.", "strong base, two hydroxides per formula"),
]

def make_fixed(rng, fid):
    P = [f for f in FIXED if f["id"] == fid][0]; s = strong(P["strong"]); n = s["ions_per_formula"]; c = P["conc"] * n; is_acid = s["kind"] == "acid"
    h = c if is_acid else KW / c; pH = pH_of(h); pOH = 14 - pH; ion = "[H3O+]" if is_acid else "[OH-]"
    expected = [E("ion_found", f"{ion} from the formula", c, "M", role="intermediate", require_unit=True, after="relation_chosen"),
                E("pH_found", "pH", pH, "", role="key", require_unit=False, after="ion_found"),
                E("pOH_found", "pOH", pOH, "", role="intermediate", require_unit=False, after="pH_found")]
    traps = []
    if not is_acid: traps.append(trap("POH_TYPED_AS_PH", pOH, "pH_found"))
    if n > 1: traps.append(trap("IONS_PER_FORMULA_IGNORED", P["conc"], "ion_found", "M"))
    traps = keep_clear(traps, expected)
    board = head() + [{"state": "ion_found", "kind": "number", "register": "symbolic", "requires": ["relation_chosen"], "explicit": True, "pin": True},
                      {"state": "pH_found", "kind": "number", "register": "macro", "requires": ["ion_found"], "explicit": True, "pin": True},
                      {"state": "pOH_found", "kind": "number", "register": "symbolic", "requires": ["pH_found"], "explicit": True},
                      direction_item("perturb_1", "p1", "pH", "rises" if is_acid else "falls", {}, "pOH_found"),
                      {"state": "perturb_1_why", "kind": "text", "register": "submicro", "requires": ["perturb_1"]}]
    tail(board, "perturb_1_why")
    return {"kind": P["kind"], "fixed_id": fid, "version": "", "status": P["status"], "context": {"family": P["family"], "pH": round_sig(pH, 4)}, "text": P["text"],
            "givens": {"c": {"value": P["conc"], "unit": "M"}}, "board": board, "targets": expected, "traps": traps, "table": None, "words": {"substance": s["name"], "formula": P["strong"]},
            "eq_checks": [], "reveal_with_problem": None, "sim": None, "sim_params": {"strong": P["strong"], "c": P["conc"]}}
def render_text(*a): raise NotImplementedError
