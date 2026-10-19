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
    st = salt(formula, text); cc, ca, vt = mixed(c_cat, v_cat, c_an, v_an); Q = qsp(st, cc, ca)
    kind = "precipitates" if Q > st["Ksp"] else "stays_dissolved"
    return {"id": fid, "kind": kind, "salt": st, "c_cat": c_cat, "v_cat": v_cat, "c_an": c_an, "v_an": v_an, "text": text, "family": family, "version": "", "sf": 2, "status": "approved (SCENARIO_CLAUDE's sheet; instructor, 17 Oct 2026)"}
FIXED = [   # 24 problems, four scenarios (approved 17 Oct 2026)
  _p('CT1', 'AgCl', 0.01, 1.0, 0.001, 9.0, r"""1.0 mL of 0.01 M silver nitrate is mixed with 9.0 mL of 0.001 M tap water containing chloride ion at 25 °C (\(K_{sp}\) of \(\mathrm{AgCl}\) = \(1.6 \times 10^{-10}\)). Find each ion's concentration after mixing, find Qsp, and say whether silver chloride precipitates.""", 'The Chloride Test'),
  _p('CT2', 'AgCl', 0.01, 1.0, 1e-08, 9.0, r"""1.0 mL of 0.01 M silver nitrate is mixed with 9.0 mL of \(1 \times 10^{-8}\) M deionized water containing chloride ion at 25 °C (\(K_{sp}\) of \(\mathrm{AgCl}\) = \(1.6 \times 10^{-10}\)). Find each ion's concentration after mixing, find Qsp, and say whether silver chloride precipitates.""", 'The Chloride Test'),
  _p('CT3', 'AgCl', 0.0001, 50.0, 0.0001, 50.0, r"""50.0 mL of \(1 \times 10^{-4}\) M silver nitrate is mixed with 50.0 mL of \(1 \times 10^{-4}\) M sodium chloride at 25 °C (\(K_{sp}\) of \(\mathrm{AgCl}\) = \(1.6 \times 10^{-10}\)). Find each ion's concentration after mixing, find Qsp, and say whether silver chloride precipitates.""", 'The Chloride Test'),
  _p('CT4', 'BaSO4', 0.1, 2.0, 0.0001, 18.0, r"""2.0 mL of 0.1 M barium chloride is mixed with 18.0 mL of \(1 \times 10^{-4}\) M a water sample containing sulfate ion at 25 °C (\(K_{sp}\) of \(\mathrm{BaSO_4}\) = \(2.3 \times 10^{-8}\)). Find each ion's concentration after mixing, find Qsp, and say whether barium sulfate precipitates.""", 'The Chloride Test'),
  _p('CT5', 'PbI2', 0.001, 25.0, 0.002, 75.0, r"""25.0 mL of 0.001 M lead(II) nitrate is mixed with 75.0 mL of 0.002 M potassium iodide at 25 °C (\(K_{sp}\) of \(\mathrm{PbI_2}\) = \(1.4 \times 10^{-8}\)). Find each ion's concentration after mixing, find Qsp, and say whether lead(II) iodide precipitates.""", 'The Chloride Test'),
  _p('CT6', 'Mg(OH)2', 0.001, 10.0, 0.0001, 40.0, r"""10.0 mL of 0.001 M magnesium chloride is mixed with 40.0 mL of \(1 \times 10^{-4}\) M sodium hydroxide at 25 °C (\(K_{sp}\) of \(\mathrm{Mg(OH)_2}\) = \(8.9 \times 10^{-12}\)). Find each ion's concentration after mixing, find Qsp, and say whether magnesium hydroxide precipitates.""", 'The Chloride Test'),
  _p('KR1', 'CaC2O4', 0.001, 25.0, 0.0001, 75.0, r"""25.0 mL of 0.001 M calcium chloride is mixed with 75.0 mL of \(1 \times 10^{-4}\) M sodium oxalate at 25 °C (\(K_{sp}\) of \(\mathrm{CaC_2O_4}\) = \(2 \times 10^{-9}\)). Find each ion's concentration after mixing, find Qsp, and say whether calcium oxalate (monohydrate) precipitates.""", 'The Kidney Stone Risk'),
  _p('KR2', 'CaC2O4', 0.0002, 50.0, 0.0002, 50.0, r"""50.0 mL of \(2 \times 10^{-4}\) M calcium chloride is mixed with 50.0 mL of \(2 \times 10^{-4}\) M sodium oxalate at 25 °C (\(K_{sp}\) of \(\mathrm{CaC_2O_4}\) = \(2 \times 10^{-9}\)). Find each ion's concentration after mixing, find Qsp, and say whether calcium oxalate (monohydrate) precipitates.""", 'The Kidney Stone Risk'),
  _p('KR3', 'CaC2O4', 0.0005, 10.0, 2e-05, 90.0, r"""10.0 mL of \(5 \times 10^{-4}\) M calcium chloride is mixed with 90.0 mL of \(2 \times 10^{-5}\) M sodium oxalate at 25 °C (\(K_{sp}\) of \(\mathrm{CaC_2O_4}\) = \(2 \times 10^{-9}\)). Find each ion's concentration after mixing, find Qsp, and say whether calcium oxalate (monohydrate) precipitates.""", 'The Kidney Stone Risk'),
  _p('KR4', 'CaC2O4', 5e-05, 40.0, 5e-05, 60.0, r"""40.0 mL of \(5 \times 10^{-5}\) M calcium chloride is mixed with 60.0 mL of \(5 \times 10^{-5}\) M sodium oxalate at 25 °C (\(K_{sp}\) of \(\mathrm{CaC_2O_4}\) = \(2 \times 10^{-9}\)). Find each ion's concentration after mixing, find Qsp, and say whether calcium oxalate (monohydrate) precipitates.""", 'The Kidney Stone Risk'),
  _p('KR5', 'CaC2O4', 0.0025, 20.0, 0.00025, 80.0, r"""20.0 mL of 0.0025 M calcium chloride is mixed with 80.0 mL of \(2.5 \times 10^{-4}\) M sodium oxalate at 25 °C (\(K_{sp}\) of \(\mathrm{CaC_2O_4}\) = \(2 \times 10^{-9}\)). Find each ion's concentration after mixing, find Qsp, and say whether calcium oxalate (monohydrate) precipitates.""", 'The Kidney Stone Risk'),
  _p('KR6', 'CaC2O4', 4e-05, 75.0, 4e-05, 25.0, r"""75.0 mL of \(4 \times 10^{-5}\) M calcium chloride is mixed with 25.0 mL of \(4 \times 10^{-5}\) M sodium oxalate at 25 °C (\(K_{sp}\) of \(\mathrm{CaC_2O_4}\) = \(2 \times 10^{-9}\)). Find each ion's concentration after mixing, find Qsp, and say whether calcium oxalate (monohydrate) precipitates.""", 'The Kidney Stone Risk'),
  _p('GR1', 'PbI2', 0.01, 25.0, 0.02, 75.0, r"""25.0 mL of 0.01 M lead(II) nitrate is mixed with 75.0 mL of 0.02 M potassium iodide at 25 °C (\(K_{sp}\) of \(\mathrm{PbI_2}\) = \(1.4 \times 10^{-8}\)). Find each ion's concentration after mixing, find Qsp, and say whether lead(II) iodide precipitates.""", 'The Golden Rain'),
  _p('GR2', 'PbI2', 1e-05, 50.0, 2e-05, 50.0, r"""50.0 mL of \(1 \times 10^{-5}\) M lead(II) nitrate is mixed with 50.0 mL of \(2 \times 10^{-5}\) M potassium iodide at 25 °C (\(K_{sp}\) of \(\mathrm{PbI_2}\) = \(1.4 \times 10^{-8}\)). Find each ion's concentration after mixing, find Qsp, and say whether lead(II) iodide precipitates.""", 'The Golden Rain'),
  _p('GR3', 'PbI2', 0.005, 40.0, 0.01, 60.0, r"""40.0 mL of 0.005 M lead(II) nitrate is mixed with 60.0 mL of 0.01 M potassium iodide at 25 °C (\(K_{sp}\) of \(\mathrm{PbI_2}\) = \(1.4 \times 10^{-8}\)). Find each ion's concentration after mixing, find Qsp, and say whether lead(II) iodide precipitates.""", 'The Golden Rain'),
  _p('GR4', 'CaF2', 0.001, 50.0, 0.001, 50.0, r"""50.0 mL of 0.001 M calcium nitrate is mixed with 50.0 mL of 0.001 M sodium fluoride at 25 °C (\(K_{sp}\) of \(\mathrm{CaF_2}\) = \(4 \times 10^{-11}\)). Find each ion's concentration after mixing, find Qsp, and say whether calcium fluoride precipitates.""", 'The Golden Rain'),
  _p('GR5', 'BaSO4', 0.0001, 30.0, 0.0001, 70.0, r"""30.0 mL of \(1 \times 10^{-4}\) M barium chloride is mixed with 70.0 mL of \(1 \times 10^{-4}\) M sodium sulfate at 25 °C (\(K_{sp}\) of \(\mathrm{BaSO_4}\) = \(2.3 \times 10^{-8}\)). Find each ion's concentration after mixing, find Qsp, and say whether barium sulfate precipitates.""", 'The Golden Rain'),
  _p('GR6', 'Ag2CrO4', 0.001, 50.0, 0.001, 50.0, r"""50.0 mL of 0.001 M silver nitrate is mixed with 50.0 mL of 0.001 M potassium chromate at 25 °C (\(K_{sp}\) of \(\mathrm{Ag_2CrO_4}\) = \(9 \times 10^{-12}\)). Find each ion's concentration after mixing, find Qsp, and say whether silver chromate precipitates.""", 'The Golden Rain'),
  _p('HW1', 'CaCO3', 0.002, 90.0, 0.001, 10.0, r"""90.0 mL of 0.002 M calcium chloride is mixed with 10.0 mL of 0.001 M sodium carbonate at 25 °C (\(K_{sp}\) of \(\mathrm{CaCO_3}\) = \(8.7 \times 10^{-9}\)). Find each ion's concentration after mixing, find Qsp, and say whether calcium carbonate precipitates.""", 'The Hard-Water Scale'),
  _p('HW2', 'CaCO3', 0.0001, 50.0, 5e-05, 50.0, r"""50.0 mL of \(1 \times 10^{-4}\) M calcium chloride is mixed with 50.0 mL of \(5 \times 10^{-5}\) M sodium carbonate at 25 °C (\(K_{sp}\) of \(\mathrm{CaCO_3}\) = \(8.7 \times 10^{-9}\)). Find each ion's concentration after mixing, find Qsp, and say whether calcium carbonate precipitates.""", 'The Hard-Water Scale'),
  _p('HW3', 'CaCO3', 0.0005, 80.0, 0.0002, 20.0, r"""80.0 mL of \(5 \times 10^{-4}\) M calcium chloride is mixed with 20.0 mL of \(2 \times 10^{-4}\) M sodium carbonate at 25 °C (\(K_{sp}\) of \(\mathrm{CaCO_3}\) = \(8.7 \times 10^{-9}\)). Find each ion's concentration after mixing, find Qsp, and say whether calcium carbonate precipitates.""", 'The Hard-Water Scale'),
  _p('HW4', 'Mg(OH)2', 0.002, 50.0, 0.002, 50.0, r"""50.0 mL of 0.002 M magnesium chloride is mixed with 50.0 mL of 0.002 M sodium hydroxide at 25 °C (\(K_{sp}\) of \(\mathrm{Mg(OH)_2}\) = \(8.9 \times 10^{-12}\)). Find each ion's concentration after mixing, find Qsp, and say whether magnesium hydroxide precipitates.""", 'The Hard-Water Scale'),
  _p('HW5', 'CaCO3', 3.0000000000000004e-05, 60.0, 3.0000000000000004e-05, 40.0, r"""60.0 mL of \(3 \times 10^{-5}\) M calcium chloride is mixed with 40.0 mL of \(3 \times 10^{-5}\) M sodium carbonate at 25 °C (\(K_{sp}\) of \(\mathrm{CaCO_3}\) = \(8.7 \times 10^{-9}\)). Find each ion's concentration after mixing, find Qsp, and say whether calcium carbonate precipitates.""", 'The Hard-Water Scale'),
  _p('HW6', 'CaF2', 0.0002, 25.0, 0.0002, 75.0, r"""25.0 mL of \(2 \times 10^{-4}\) M calcium chloride is mixed with 75.0 mL of \(2 \times 10^{-4}\) M sodium fluoride at 25 °C (\(K_{sp}\) of \(\mathrm{CaF_2}\) = \(4 \times 10^{-11}\)). Find each ion's concentration after mixing, find Qsp, and say whether calcium fluoride precipitates.""", 'The Hard-Water Scale'),
]

def make_fixed(rng, fid):
    P = [f for f in FIXED if f["id"] == fid][0]; st = P["salt"]; a, b = st["n_cat"], st["n_an"]
    cc, ca, vt = mixed(P["c_cat"], P["v_cat"], P["c_an"], P["v_an"]); Q = qsp(st, cc, ca); forms = Q > st["Ksp"]
    expected = [E("conc_found", f"[{st['cation']}] after mixing", cc, "M", role="intermediate", require_unit=True, after="relation_chosen"), E("conc_found", f"[{st['anion']}] after mixing", ca, "M", role="intermediate", require_unit=True, after="relation_chosen"),   # asked for by name: a diluted value may equal the other solution's given
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
