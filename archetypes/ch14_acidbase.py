"""Chapter 14, archetype 2 of 4: Acids & Bases (weak acids and weak bases). Fixed problems; placeholders DRAFT; ships nothing until
a scenario is approved. Step map: account -> relation (the Ka or Kb expression) -> table -> expression_set -> method (small-x when the
5 % rule holds, else quadratic) -> x_found -> (pOH_found) -> pH_found -> percent_found -> approx_checked -> perturb_1 (tenfold
dilution: percent ionised rises) -> why -> perturb_2 (the conjugate salt: pH rises for an acid, falls for a base) -> why -> meaning -> reflection.
"""
import math
from engine import round_sig
from _acidbase import *

ID = "ch14_acidbase"
TITLE = "Acids and bases: how far a weak acid or base ionises"
RELATION_TEXT = "Ka and Kb are equilibrium constants for the transfer of one proton to or from water; pH = -log[H3O+]"
KINDS = ["weak_acid", "weak_base"]
EQUATION_PICKS = picks({"eq_ka": ["weak_acid"], "eq_kb": ["weak_base"]})
CONSTANTS = [{"label": "Kw", "symbol": "Kw", "value": KW, "unit": ""}]
EQUATION_SYMBOLS = {"x": ["x"], "K": ["Ka", "K_a", "Kb", "K_b", "K"]}; EQUATION_CONSTANTS = {"Kw": KW}
MECHANISM_WORDS = MECHANISM_WORDS
TRAP_NOTES = TRAP_NOTES_COMMON
ACETIC, HNO2, HOCl, NH3, CH3NH2 = acid("acetic"), acid("nitrous"), acid("hypochlorous"), base("ammonia"), base("methylamine")

def _p(fid, rx, conc, text, family): return {"id": fid, "kind": "weak_" + rx["kind"], "rx": rx, "conc": conc, "text": text, "family": family, "version": "", "sf": 2, "status": DRAFT}
FIXED = [
  _p("W1", ACETIC, 0.10, "Household vinegar is about 0.10 M acetic acid, CH3COOH, with Ka = 1.8 × 10^-5 at 25 °C. Set up the ICE table, find [H3O+] and the pH, and find the percent ionised.", "weak acid, 5 % rule holds"),
  _p("W2", HNO2, 0.0050, "A 0.0050 M solution of nitrous acid, HNO2 (Ka = 4.5 × 10^-4), is prepared at 25 °C. Set up the ICE table, find [H3O+] and the pH, and find the percent ionised.", "weak acid, 5 % rule fails: quadratic"),
  _p("W3", HOCl, 0.050, "Pool water is treated to 0.050 M hypochlorous acid, HOCl (Ka = 2.9 × 10^-8), at 25 °C. Set up the ICE table, find [H3O+] and the pH, and find the percent ionised.", "weak acid, very small Ka"),
  _p("B1", NH3, 0.25, "Window cleaner holds 0.25 M ammonia, NH3, with Kb = 1.8 × 10^-5 at 25 °C. Set up the ICE table, find [OH-], the pOH, the pH, and the percent ionised.", "weak base, 5 % rule holds"),
  _p("B2", CH3NH2, 0.010, "A 0.010 M solution of methylamine, CH3NH2 (Kb = 4.4 × 10^-4), is prepared at 25 °C. Set up the ICE table, find [OH-], the pOH, the pH, and the percent ionised.", "weak base, 5 % rule fails: quadratic"),
]

def make_fixed(rng, fid):
    P = [f for f in FIXED if f["id"] == fid][0]; rx = P["rx"]; c = P["conc"]; is_acid = rx["kind"] == "acid"
    expected, traps, board = [], [], head()
    prev, w, table, eqc = weak_chain(rx, c, expected, traps, board, "relation_chosen")
    traps = keep_clear(traps, expected)
    named1 = {"falls": "DILUTION_IONIZATION_FALLS"}; named2 = {"falls": "CONJUGATE_LOWERS_PH"} if is_acid else {"rises": "CONJUGATE_RAISES_PH"}
    board += [direction_item("perturb_1", "p1", "percent ionised", "rises", named1, prev), {"state": "perturb_1_why", "kind": "text", "register": "submicro", "requires": ["perturb_1"]},
              direction_item("perturb_2", "p2", "pH", "rises" if is_acid else "falls", named2, "perturb_1_why"), {"state": "perturb_2_why", "kind": "text", "register": "submicro", "requires": ["perturb_2"]}]
    tail(board, "perturb_2_why")
    return {"kind": P["kind"], "fixed_id": fid, "version": "", "status": P["status"], "text": P["text"],
            "context": {"family": P["family"], "x": round_sig(w["x"], 5), "pH": round_sig(w["pH"], 4), "percent": round_sig(w["percent"], 4), "approx_ok": w["approx_ok"]},
            "givens": {"c": {"value": c, "unit": "M"}, ("Ka" if is_acid else "Kb"): {"value": rx["K"], "unit": ""}}, "board": board, "targets": expected, "traps": traps, "table": table,
            "words": dict(rx["words"]), "eq_checks": [eqc], "reveal_with_problem": None, "sim": None, "sim_params": {"species": rx["id"], "c": c, "K": rx["K"]}}
def render_text(*a): raise NotImplementedError
