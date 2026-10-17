"""Chapter 15, archetype 2 of 3: the common ion. Fixed problems; placeholders DRAFT; ships nothing until a scenario is approved.
Step map: account -> relation (the Ksp expression) -> table (I row carries the ion already present) -> expression_set -> method
(drop s next to the common ion when it is small: the right choice when the 5 % rule holds, else the exact root) -> s_found ->
pure_found (the pure-water solubility, for the comparison) -> ratio_found (how many times smaller) -> perturb_1 (more of the common
ion: solubility falls) -> why -> meaning -> reflection.
"""
import math
from engine import round_sig
from _solubility import *

ID = "ch15_common_ion"
TITLE = "The common ion: why a salt dissolves less in a solution that already holds one of its ions"
RELATION_TEXT = "Ksp = [cation]^a [anion]^b still holds; an ion already present raises its term, so s must fall"
KINDS = ["common_cation", "common_anion"]
EQUATION_PICKS = picks({"eq_ksp": KINDS})
CONSTANTS = []
EQUATION_SYMBOLS = {"x": ["x", "s"], "K": ["Ksp", "K_sp", "K"]}; EQUATION_CONSTANTS = {}   # s is read as the unknown x; EQUATION_CONSTANTS = {}
MECHANISM_WORDS = MECHANISM_WORDS
TRAP_NOTES = TRAP_NOTES_COMMON
METHOD_OPTIONS = [{"id": "method:smalls", "text": "s is small next to the ion already present: drop it from that term, then check."},
                  {"id": "method:exact", "text": "Keep s in every term and solve the polynomial exactly."},
                  {"id": "method:pure", "text": "Ignore the ion already present and solve as in pure water."}]

def _p(fid, formula, which, c_common, source_salt, text, family):
    return {"id": fid, "kind": "common_" + which, "salt": salt(formula), "which": which, "c_common": c_common, "source_salt": source_salt, "text": text, "family": family, "version": "", "sf": 2, "status": DRAFT}
FIXED = [
  _p("C1", "AgCl", "anion", 0.10, "sodium chloride", "Silver chloride, AgCl (Ksp = 1.6 × 10^-10), is shaken with 0.10 M sodium chloride at 25 °C. Set up the table with the chloride already present, write Ksp in terms of s, and find the molar solubility. Compare it with the solubility in pure water.", "1:1 salt, common anion"),
  _p("C2", "CaF2", "anion", 0.050, "sodium fluoride", "Calcium fluoride, CaF2 (Ksp = 4.0 × 10^-11), is shaken with 0.050 M sodium fluoride at 25 °C. Set up the table with the fluoride already present, write Ksp in terms of s, and find the molar solubility. Compare it with the solubility in pure water.", "1:2 salt, common anion"),
  _p("C3", "CaF2", "cation", 0.020, "calcium nitrate", "Calcium fluoride, CaF2 (Ksp = 4.0 × 10^-11), is shaken with 0.020 M calcium nitrate at 25 °C. Set up the table with the calcium already present, write Ksp in terms of s, and find the molar solubility. Compare it with the solubility in pure water.", "1:2 salt, common cation"),
]

def make_fixed(rng, fid):
    P = [f for f in FIXED if f["id"] == fid][0]; st = P["salt"]; a, b = st["n_cat"], st["n_an"]; which = P["which"]; c0 = P["c_common"]
    r = s_with_common_ion(st, which, c0); s = r["exact"]; s_pure = s_from_ksp(st); ratio = s_pure / s
    expected = [E("s_found", "s with the common ion", s, "M", role="key", require_unit=True),
                E("pure_found", "s in pure water", s_pure, "M", role="intermediate", require_unit=True, after="s_found"),
                E("ratio_found", "how many times smaller", ratio, "", role="intermediate", require_unit=False, after="pure_found")]
    traps = [trap("COMMON_ION_IGNORED", s_pure, "s_found", "M")]
    if not r["small_ok"]: traps.append(trap("SMALL_S_WHEN_IT_FAILS", r["small"], "s_found", "M"))
    traps = keep_clear(traps, expected)
    board = head() + [{"state": "table", "kind": "table", "register": "symbolic", "requires": ["relation_chosen"], "pin": True, "explicit": True},
                      {"state": "expression_set", "kind": "equation", "register": "symbolic", "requires": ["table"], "explicit": True, "pin": True},
                      {"state": "method", "kind": "pick", "register": "symbolic", "requires": ["expression_set"], "options": METHOD_OPTIONS, "right": ["method:smalls"] if r["small_ok"] else ["method:exact"]},
                      {"state": "s_found", "kind": "number", "register": "symbolic", "requires": ["method"], "explicit": True, "pin": True},
                      {"state": "pure_found", "kind": "number", "register": "symbolic", "requires": ["s_found"], "explicit": True},
                      {"state": "ratio_found", "kind": "number", "register": "macro", "requires": ["pure_found"], "explicit": True, "pin": True},
                      {"state": "perturb_1", "kind": "direction", "register": "macro", "requires": ["ratio_found"], "options": opts("p1", [("rises", "rises: more of the solid dissolves"), ("falls", "falls: less of the solid dissolves"), ("unchanged", "unchanged: the same amount dissolves")], {"rises": "SOLUBILITY_RISES_WITH_COMMON_ION"}), "right": ["p1:falls"], "explicit": True, "pin": True},
                      {"state": "perturb_1_why", "kind": "text", "register": "submicro", "requires": ["perturb_1"]}]
    tail(board, "perturb_1_why")
    words = dict(st["words"]); words["common_ion"] = st["anion_display"] if which == "anion" else st["cation_display"]; words["source_salt"] = P["source_salt"]
    return {"kind": P["kind"], "fixed_id": fid, "version": "", "status": P["status"], "context": {"family": P["family"], "s": round_sig(s, 5), "s_pure": round_sig(s_pure, 5), "small_ok": r["small_ok"]}, "text": P["text"],
            "givens": {"Ksp": {"value": st["Ksp"], "unit": ""}, "c_common": {"value": c0, "unit": "M"}}, "board": board, "targets": expected, "traps": traps,
            "table": ice_table(st, c0, which), "words": words, "eq_checks": [expression_check(st, c0, which)], "reveal_with_problem": None, "sim": None,
            "sim_params": {"salt": st["formula"], "common": words["common_ion"], "c_common": c0}}
def render_text(*a): raise NotImplementedError
