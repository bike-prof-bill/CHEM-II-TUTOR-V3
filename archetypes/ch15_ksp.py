"""Chapter 15, archetype 1 of 3: Ksp and molar solubility. Fixed problems from SCENARIO_CLAUDE's sheets (approved 17 Oct 2026). The unknown is x in every student-facing word (instructor, 17 Oct). Two kinds: `s_from_ksp` (Ksp given; find s, the ion concentrations, grams per litre) and `ksp_from_s` (solubility given in
grams per litre; find s, the ion concentrations, Ksp). Step map: account -> relation (the Ksp expression) -> table (the s table: the
solid present, not counted) -> expression_set (Ksp = (a s)^a (b s)^b) -> s_found (for ksp_from_s, moles per litre from grams per litre) -> conc_found (both ions; skipped for a 1:1 salt, where they equal s)
-> [grams_found, s_from_ksp | ksp_found, ksp_from_s] -> perturb_1 (a salt sharing an ion is
added: solubility rises | falls | unchanged) -> why -> meaning -> reflection.
"""
import math
from engine import round_sig
from _solubility import *

ID = "ch15_ksp"
TITLE = "Ksp: how much of a sparingly soluble salt dissolves"
RELATION_TEXT = "Ksp = [cation]^a [anion]^b for the dissolved ions at saturation; the solid is present and not counted; s is the molar solubility"
KINDS = ["s_from_ksp", "ksp_from_s"]
EQUATION_PICKS = picks({"eq_ksp": KINDS})
CONSTANTS = []
EQUATION_SYMBOLS = {"x": ["x", "s"], "K": ["Ksp", "K_sp", "K"]}; EQUATION_CONSTANTS = {}   # s is read as the unknown x; EQUATION_CONSTANTS = {}
MECHANISM_WORDS = MECHANISM_WORDS
TRAP_NOTES = TRAP_NOTES_COMMON

def _p(fid, kind, formula, text, family, gpl=None):
    return {"id": fid, "kind": kind, "salt": salt(formula, text), "gpl": gpl, "text": text, "family": family, "version": "", "sf": 2, "status": "approved (SCENARIO_CLAUDE's sheet; instructor, 17 Oct 2026)"}
FIXED = [   # 24 problems, four scenarios (SCENARIO_CLAUDE, approved 17 Oct 2026); the family column carries the scenario
  _p('MK1', 's_from_ksp', 'BaSO4', r"""An X-ray lab checks its barium sulfate suspension. Barium sulfate, \(\mathrm{BaSO_4}\), has \(K_{sp} = 2.3 \times 10^{-8}\) at 25 °C. Set up the table, write Ksp in terms of x, the molar solubility, and find the molar solubility, the concentration of each ion, and the grams that dissolve in a liter.""", 'The Barium Milkshake', gpl=None),
  _p('MK2', 'ksp_from_s', 'BaSO4', r"""An X-ray lab checks its barium sulfate suspension. At 25 °C, 0.035 g of barium sulfate, \(\mathrm{BaSO_4}\), dissolves in a liter of water. Set up the table, write Ksp in terms of x, the molar solubility, find the molar solubility and the concentration of each ion, and find Ksp.""", 'The Barium Milkshake', gpl=0.035),
  _p('MK3', 's_from_ksp', 'CaF2', r"""Calcium fluoride, \(\mathrm{CaF_2}\), has \(K_{sp} = 4 \times 10^{-11}\) at 25 °C. Set up the table, write Ksp in terms of x, the molar solubility, and find the molar solubility, the concentration of each ion, and the grams that dissolve in a liter.""", 'The Barium Milkshake', gpl=None),
  _p('MK4', 'ksp_from_s', 'Ag2CrO4', r"""At 25 °C, 0.044 g of silver chromate, \(\mathrm{Ag_2CrO_4}\), dissolves in a liter of water. Set up the table, write Ksp in terms of x, the molar solubility, find the molar solubility and the concentration of each ion, and find Ksp.""", 'The Barium Milkshake', gpl=0.044),
  _p('MK5', 'ksp_from_s', 'PbI2', r"""At 25 °C, 0.7 g of lead(II) iodide, \(\mathrm{PbI_2}\), dissolves in a liter of water. Set up the table, write Ksp in terms of x, the molar solubility, find the molar solubility and the concentration of each ion, and find Ksp.""", 'The Barium Milkshake', gpl=0.7),
  _p('MK6', 's_from_ksp', 'AgCl', r"""Silver chloride, \(\mathrm{AgCl}\), has \(K_{sp} = 1.6 \times 10^{-10}\) at 25 °C. Set up the table, write Ksp in terms of x, the molar solubility, and find the molar solubility, the concentration of each ion, and the grams that dissolve in a liter.""", 'The Barium Milkshake', gpl=None),
  _p('ME1', 's_from_ksp', 'Mg(OH)2', r"""Magnesium hydroxide, \(\mathrm{Mg(OH)_2}\), has \(K_{sp} = 8.9 \times 10^{-12}\) at 25 °C. Set up the table, write Ksp in terms of x, the molar solubility, and find the molar solubility, the concentration of each ion, and the grams that dissolve in a liter.""", 'Milk of Magnesia', gpl=None),
  _p('ME2', 's_from_ksp', 'BaF2', r"""Barium fluoride, \(\mathrm{BaF_2}\), has \(K_{sp} = 2.4 \times 10^{-5}\) at 25 °C. Set up the table, write Ksp in terms of x, the molar solubility, and find the molar solubility, the concentration of each ion, and the grams that dissolve in a liter.""", 'Milk of Magnesia', gpl=None),
  _p('ME3', 's_from_ksp', 'PbI2', r"""Lead(ii) iodide, \(\mathrm{PbI_2}\), has \(K_{sp} = 1.4 \times 10^{-8}\) at 25 °C. Set up the table, write Ksp in terms of x, the molar solubility, and find the molar solubility, the concentration of each ion, and the grams that dissolve in a liter.""", 'Milk of Magnesia', gpl=None),
  _p('ME4', 's_from_ksp', 'Ag2CrO4', r"""Silver chromate, \(\mathrm{Ag_2CrO_4}\), has \(K_{sp} = 9 \times 10^{-12}\) at 25 °C. Set up the table, write Ksp in terms of x, the molar solubility, and find the molar solubility, the concentration of each ion, and the grams that dissolve in a liter.""", 'Milk of Magnesia', gpl=None),
  _p('ME5', 's_from_ksp', 'Ca(OH)2', r"""Calcium hydroxide, \(\mathrm{Ca(OH)_2}\), has \(K_{sp} = 1.3 \times 10^{-6}\) at 25 °C. Set up the table, write Ksp in terms of x, the molar solubility, and find the molar solubility, the concentration of each ion, and the grams that dissolve in a liter.""", 'Milk of Magnesia', gpl=None),
  _p('ME6', 's_from_ksp', 'Ag2CO3', r"""Silver carbonate, \(\mathrm{Ag_2CO_3}\), has \(K_{sp} = 8.1 \times 10^{-12}\) at 25 °C. Set up the table, write Ksp in terms of x, the molar solubility, and find the molar solubility, the concentration of each ion, and the grams that dissolve in a liter.""", 'Milk of Magnesia', gpl=None),
  _p('KS1', 's_from_ksp', 'CaC2O4', r"""A kidney-stone lab tests calcium oxalate. Calcium oxalate (monohydrate), \(\mathrm{CaC_2O_4}\), has \(K_{sp} = 2 \times 10^{-9}\) at 25 °C. Set up the table, write Ksp in terms of x, the molar solubility, and find the molar solubility, the concentration of each ion, and the grams that dissolve in a liter.""", 'The Kidney Stone', gpl=None),
  _p('KS2', 'ksp_from_s', 'CaC2O4', r"""A kidney-stone lab tests calcium oxalate. At 25 °C, 0.0065 g of calcium oxalate (monohydrate), \(\mathrm{CaC_2O_4}\), dissolves in a liter of water. Set up the table, write Ksp in terms of x, the molar solubility, find the molar solubility and the concentration of each ion, and find Ksp.""", 'The Kidney Stone', gpl=0.0065),
  _p('KS3', 's_from_ksp', 'CaCO3', r"""Calcium carbonate, \(\mathrm{CaCO_3}\), has \(K_{sp} = 8.7 \times 10^{-9}\) at 25 °C. Set up the table, write Ksp in terms of x, the molar solubility, and find the molar solubility, the concentration of each ion, and the grams that dissolve in a liter.""", 'The Kidney Stone', gpl=None),
  _p('KS4', 'ksp_from_s', 'CaF2', r"""At 25 °C, 0.017 g of calcium fluoride, \(\mathrm{CaF_2}\), dissolves in a liter of water. Set up the table, write Ksp in terms of x, the molar solubility, find the molar solubility and the concentration of each ion, and find Ksp.""", 'The Kidney Stone', gpl=0.017),
  _p('KS5', 'ksp_from_s', 'BaF2', r"""At 25 °C, 3.2 g of barium fluoride, \(\mathrm{BaF_2}\), dissolves in a liter of water. Set up the table, write Ksp in terms of x, the molar solubility, find the molar solubility and the concentration of each ion, and find Ksp.""", 'The Kidney Stone', gpl=3.2),
  _p('KS6', 'ksp_from_s', 'Mg(OH)2', r"""At 25 °C, 0.0076 g of magnesium hydroxide, \(\mathrm{Mg(OH)_2}\), dissolves in a liter of water. Set up the table, write Ksp in terms of x, the molar solubility, find the molar solubility and the concentration of each ion, and find Ksp.""", 'The Kidney Stone', gpl=0.0076),
  _p('SH1', 's_from_ksp', 'AgCl', r"""Silver chloride, \(\mathrm{AgCl}\), has \(K_{sp} = 1.6 \times 10^{-10}\) at 25 °C. Set up the table, write Ksp in terms of x, the molar solubility, and find the molar solubility, the concentration of each ion, and the grams that dissolve in a liter.""", 'The Silver Halide Lineup', gpl=None),
  _p('SH2', 's_from_ksp', 'AgBr', r"""Silver bromide, \(\mathrm{AgBr}\), has \(K_{sp} = 5 \times 10^{-13}\) at 25 °C. Set up the table, write Ksp in terms of x, the molar solubility, and find the molar solubility, the concentration of each ion, and the grams that dissolve in a liter.""", 'The Silver Halide Lineup', gpl=None),
  _p('SH3', 's_from_ksp', 'AgI', r"""Silver iodide, \(\mathrm{AgI}\), has \(K_{sp} = 1.5 \times 10^{-16}\) at 25 °C. Set up the table, write Ksp in terms of x, the molar solubility, and find the molar solubility, the concentration of each ion, and the grams that dissolve in a liter.""", 'The Silver Halide Lineup', gpl=None),
  _p('SH4', 'ksp_from_s', 'AgCl', r"""At 25 °C, 0.0018 g of silver chloride, \(\mathrm{AgCl}\), dissolves in a liter of water. Set up the table, write Ksp in terms of x, the molar solubility, find the molar solubility and the concentration of each ion, and find Ksp.""", 'The Silver Halide Lineup', gpl=0.0018),
  _p('SH5', 'ksp_from_s', 'AgBr', r"""At 25 °C, \(1.3 \times 10^{-4}\) g of silver bromide, \(\mathrm{AgBr}\), dissolves in a liter of water. Set up the table, write Ksp in terms of x, the molar solubility, find the molar solubility and the concentration of each ion, and find Ksp.""", 'The Silver Halide Lineup', gpl=0.00013000000000000002),
  _p('SH6', 'ksp_from_s', 'Ag2CO3', r"""At 25 °C, 0.035 g of silver carbonate, \(\mathrm{Ag_2CO_3}\), dissolves in a liter of water. Set up the table, write Ksp in terms of x, the molar solubility, find the molar solubility and the concentration of each ion, and find Ksp.""", 'The Silver Halide Lineup', gpl=0.035),
]

def make_fixed(rng, fid):
    P = [f for f in FIXED if f["id"] == fid][0]; st = P["salt"]; a, b = st["n_cat"], st["n_an"]; kind = P["kind"]
    s = s_from_ksp(st) if kind == "s_from_ksp" else P["gpl"] / st["molar_mass"]
    Ksp_calc = ksp_from_s(st, s); c_cat, c_an = ions_at(st, s); gpl = grams_per_litre(st, s)
    expected, traps = [], []
    board = head() + [{"state": "table", "kind": "table", "register": "symbolic", "requires": ["relation_chosen"], "pin": True, "explicit": True},
                      {"state": "expression_set", "kind": "equation", "register": "symbolic", "requires": ["table"], "explicit": True, "pin": True}]
    prev = "expression_set"
    if kind == "ksp_from_s":                        # grams per litre to moles per litre is s itself: one step, with the molar mass error named on it
        expected.append(E("s_found", "x, the molar solubility (moles per litre from grams per litre)", s, "M", role="intermediate", require_unit=True))
        traps.append(trap("GRAMS_WITHOUT_MOLAR_MASS", P["gpl"], "s_found", "M"))
    else:
        expected.append(E("s_found", "x, the molar solubility", s, "M", role="key", require_unit=True))
        coef = ksp_coefficient(st)
        traps += [trap("ROOT_FORGOTTEN", st["Ksp"] / coef, "s_found", "M"), trap("COEFFICIENT_FORGOTTEN", st["Ksp"] ** (1.0 / st["n_ions"]), "s_found", "M") if coef > 1 else None]
    board.append({"state": "s_found", "kind": "number", "register": "symbolic", "requires": [prev], "explicit": True, "pin": True}); prev = "s_found"
    if max(a, b) > 1:                               # only the ion that forms more than once per unit is asked for; the other equals s
        if a > 1: expected.append(E("conc_found", f"[{st['cation']}]", c_cat, "M", role="intermediate", require_unit=True, after="s_found"))
        if b > 1: expected.append(E("conc_found", f"[{st['anion']}]", c_an, "M", role="intermediate", require_unit=True, after="s_found"))
        traps.append(trap("S_FOR_ION", s, "conc_found", "M"))
        board.append({"state": "conc_found", "kind": "number", "register": "symbolic", "requires": [prev], "rule": "all", "explicit": True, "pin": True}); prev = "conc_found"
    if kind == "s_from_ksp":
        expected.append(E("grams_found", "grams dissolved per litre", gpl, "g/L", role="intermediate", require_unit=True, after=prev))   # after the ion step, or after s for a 1:1 salt
        traps.append(trap("GRAMS_WITHOUT_MOLAR_MASS", s, "grams_found", "g/L"))
        board.append({"state": "grams_found", "kind": "number", "register": "macro", "requires": [prev], "explicit": True, "pin": True}); prev = "grams_found"
    else:
        expected.append(E("ksp_found", "Ksp", Ksp_calc, "", role="key", require_unit=False, after=prev))
        traps += [trap("COEFFICIENT_FORGOTTEN", s ** st["n_ions"], "ksp_found") if ksp_coefficient(st) > 1 else None, trap("EXPONENTS_DROPPED", c_cat * c_an, "ksp_found") if max(a, b) > 1 else None]
        board.append({"state": "ksp_found", "kind": "number", "register": "macro", "requires": [prev], "explicit": True, "pin": True}); prev = "ksp_found"
    traps = keep_clear(traps, expected)
    named = {"rises": "SOLUBILITY_RISES_WITH_COMMON_ION"}
    board += [{"state": "perturb_1", "kind": "direction", "register": "macro", "requires": [prev], "options": opts("p1", [("rises", "rises: more of the solid dissolves"), ("falls", "falls: less of the solid dissolves"), ("unchanged", "unchanged: the same amount dissolves")], named), "right": ["p1:falls"], "explicit": True, "pin": True},
              {"state": "perturb_1_why", "kind": "text", "register": "submicro", "requires": ["perturb_1"]}]
    tail(board, "perturb_1_why")
    givens = {"Ksp": {"value": st["Ksp"], "unit": ""}} if kind == "s_from_ksp" else {"grams_per_litre": {"value": P["gpl"], "unit": "g/L"}}
    givens["molar_mass"] = {"value": st["molar_mass"], "unit": "g/mol"}
    return {"kind": kind, "fixed_id": fid, "version": "", "status": P["status"], "context": {"family": P["family"], "s": round_sig(s, 5), "Ksp": round_sig(Ksp_calc, 4)}, "text": P["text"],
            "givens": givens, "board": board, "targets": expected, "traps": traps, "table": ice_table(st), "words": dict(st["words"]), "eq_checks": [expression_check(st)],
            "reveal_with_problem": None, "sim": None, "sim_params": {"salt": st["formula"], "Ksp": st["Ksp"]}}
def render_text(*a): raise NotImplementedError
