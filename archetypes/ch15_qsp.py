"""Chapter 15, archetype 3 of 3: Qsp, will a precipitate form. Fixed problems; placeholders DRAFT; ships nothing until a scenario
is approved. Step map: account -> relation (the Qsp expression) -> conc_found (each ion's concentration after the two solutions mix,
over the total volume) -> Q_found -> verdict (precipitate forms | no precipitate | just saturated; a direction item) -> perturb_1 (more
of one ion is added: Q rises) -> why -> meaning -> reflection.
"""
import math
from engine import round_sig
from _solubility import *

ID = "ch15_qsp"
TITLE = "Qsp against Ksp: will a precipitate form"
RELATION_TEXT = "Qsp = [cation]^a [anion]^b with the concentrations after mixing; a precipitate forms when Qsp exceeds Ksp"
KINDS = ["precipitates", "stays_dissolved"]
EQUATION_PICKS = picks({"eq_qsp": KINDS, "eq_ksp": KINDS})
CONSTANTS = []
EQUATION_SYMBOLS = {"Q": ["Qsp", "Q_sp", "Q"], "K": ["Ksp", "K_sp", "K"]}; EQUATION_CONSTANTS = {}
MECHANISM_WORDS = MECHANISM_WORDS
TRAP_NOTES = TRAP_NOTES_COMMON

def _p(fid, formula, c_cat, v_cat, c_an, v_an, text, family):
    st = salt(formula); cc, ca, vt = mixed(c_cat, v_cat, c_an, v_an); Q = qsp(st, cc, ca)
    kind = "precipitates" if Q > st["Ksp"] else "stays_dissolved"
    return {"id": fid, "kind": kind, "salt": st, "c_cat": c_cat, "v_cat": v_cat, "c_an": c_an, "v_an": v_an, "text": text, "family": family, "version": "", "sf": 2, "status": DRAFT}
FIXED = [
  _p("Q1", "AgCl", 1.0e-4, 50.0, 1.0e-4, 50.0, "50.0 mL of 1.0 × 10^-4 M silver nitrate is mixed with 50.0 mL of 1.0 × 10^-4 M sodium chloride at 25 °C (Ksp of AgCl = 1.6 × 10^-10). Find each ion's concentration after mixing, find Qsp, and say whether silver chloride precipitates.", "1:1, precipitates"),
  _p("Q2", "AgCl", 2.0e-5, 100.0, 2.0e-5, 100.0, "100.0 mL of 2.0 × 10^-5 M silver nitrate is mixed with 100.0 mL of 2.0 × 10^-5 M sodium chloride at 25 °C (Ksp of AgCl = 1.6 × 10^-10). Find each ion's concentration after mixing, find Qsp, and say whether silver chloride precipitates.", "1:1, stays dissolved"),
  _p("Q3", "PbI2", 1.0e-3, 25.0, 2.0e-3, 75.0, "25.0 mL of 1.0 × 10^-3 M lead(II) nitrate is mixed with 75.0 mL of 2.0 × 10^-3 M potassium iodide at 25 °C (Ksp of PbI2 = 1.4 × 10^-8). Find each ion's concentration after mixing, find Qsp, and say whether lead(II) iodide precipitates.", "1:2, unequal volumes, stays dissolved"),
  _p("Q4", "PbI2", 1.0e-2, 25.0, 2.0e-2, 75.0, "25.0 mL of 1.0 × 10^-2 M lead(II) nitrate is mixed with 75.0 mL of 2.0 × 10^-2 M potassium iodide at 25 °C (Ksp of PbI2 = 1.4 × 10^-8). Find each ion's concentration after mixing, find Qsp, and say whether lead(II) iodide precipitates.", "1:2, unequal volumes, precipitates"),
]

def make_fixed(rng, fid):
    P = [f for f in FIXED if f["id"] == fid][0]; st = P["salt"]; a, b = st["n_cat"], st["n_an"]
    cc, ca, vt = mixed(P["c_cat"], P["v_cat"], P["c_an"], P["v_an"]); Q = qsp(st, cc, ca); forms = Q > st["Ksp"]
    expected = [E("conc_found", f"[{st['cation']}] after mixing", cc, "M", role="intermediate", require_unit=True), E("conc_found", f"[{st['anion']}] after mixing", ca, "M", role="intermediate", require_unit=True),
                E("Q_found", "Qsp", Q, "", role="key", require_unit=False, after="conc_found")]
    traps = [trap("DILUTION_IGNORED", P["c_cat"], "conc_found", "M"), trap("DILUTION_IGNORED", P["c_an"], "conc_found", "M"),
             trap("VOLUME_NOT_TOTALED", P["c_cat"] * P["v_cat"] / P["v_an"], "conc_found", "M") if P["v_cat"] != P["v_an"] else None,
             trap("DILUTION_IGNORED", qsp(st, P["c_cat"], P["c_an"]), "Q_found"), trap("Q_INVERTED", 1.0 / Q, "Q_found")]
    if max(a, b) > 1: traps += [trap("EXPONENTS_DROPPED", cc * ca, "Q_found"), trap("COEFFICIENTS_AS_MULTIPLIERS", (a * cc) * (b * ca), "Q_found")]
    traps = keep_clear(traps, expected)
    verdict = "forms" if forms else "none"
    named = {"none": "NO_PRECIPITATE_WHEN_Q_MORE"} if forms else {"forms": "PRECIPITATE_WHEN_Q_LESS"}
    board = head() + [{"state": "conc_found", "kind": "number", "register": "symbolic", "requires": ["relation_chosen"], "rule": "all", "explicit": True, "pin": True},
                      {"state": "Q_found", "kind": "number", "register": "symbolic", "requires": ["conc_found"], "explicit": True, "pin": True},
                      {"state": "verdict", "kind": "direction", "register": "macro", "requires": ["Q_found"], "options": opts("v", [("forms", "forms: a precipitate appears, Q is above Ksp"), ("none", "none: it stays dissolved, Q is below Ksp"), ("saturated", "saturated: Q equals Ksp, just at the edge")], named), "right": ["v:" + verdict], "explicit": True, "pin": True},
                      {"state": "perturb_1", "kind": "direction", "register": "macro", "requires": ["verdict"], "options": opts("p1", [("rises", "rises: Q goes up"), ("falls", "falls: Q goes down"), ("unchanged", "unchanged: Q stays the same")], {}), "right": ["p1:rises"], "explicit": True, "pin": True},
                      {"state": "perturb_1_why", "kind": "text", "register": "submicro", "requires": ["perturb_1"]}]
    tail(board, "perturb_1_why")
    return {"kind": P["kind"], "fixed_id": fid, "version": "", "status": P["status"], "context": {"family": P["family"], "Q": round_sig(Q, 4), "forms": forms, "V_total_mL": vt}, "text": P["text"],
            "givens": {"c_cat": {"value": P["c_cat"], "unit": "M"}, "V_cat": {"value": P["v_cat"], "unit": "mL"}, "c_an": {"value": P["c_an"], "unit": "M"}, "V_an": {"value": P["v_an"], "unit": "mL"}, "Ksp": {"value": st["Ksp"], "unit": ""}},
            "board": board, "targets": expected, "traps": traps, "table": None, "words": dict(st["words"]), "eq_checks": [], "reveal_with_problem": None, "sim": None,
            "sim_params": {"salt": st["formula"], "c_cat": cc, "c_an": ca}}
def render_text(*a): raise NotImplementedError
