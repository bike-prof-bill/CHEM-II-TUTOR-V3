"""Chapter 14, archetype 1 of 4: pH & pOH (strong acids and bases). Fixed problems: 36, from SCENARIO_CLAUDE's sheets approved
15 Oct 2026 (The Corn Soak, worked, with a two-hydroxide offer; Concrete Burn, exam; Off the Scale and The Stockroom Morning,
floaters). Many give moles in a volume: the ion concentration is n / V times the ions per formula, so the formula concentration is
not a given and the "ions per formula ignored" and "moles typed as M" errors can be caught. Step map: account -> relation (pH = -log[H3O+]) -> ion_found (the ion concentration from the formula, counting
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

def _p(fid, opener, formula, conc, n, V, version, family, text):
    s = strong(formula)
    return {"id": fid, "opener": opener, "kind": "strong_" + s["kind"], "strong": formula, "conc": conc, "n": n, "V": V, "version": version, "text": text, "family": family, "sf": 2,
            "status": "approved (SCENARIO_CLAUDE's sheet; instructor, 15 Oct 2026)"}
FIXED = [
  _p('N1a', 'Off the Scale', 'HCl', 1.5, None, None, '', 'acid above 1 M', r"""A bottle holds 1.5 M hydrochloric acid, \(\mathrm{HCl}\), at 25 °C. Find \([\mathrm{H_3O^+}]\), the pH and the pOH."""),
  _p('N1b', 'Off the Scale', 'HNO3', 2.5, None, None, '', 'acid above 1 M', r"""A bottle holds 2.5 M nitric acid, \(\mathrm{HNO_3}\), at 25 °C. Find \([\mathrm{H_3O^+}]\), the pH and the pOH."""),
  _p('N1c', 'Off the Scale', 'HCl', 4.0, None, None, '', 'acid above 1 M', r"""A bottle holds 4.0 M hydrochloric acid, \(\mathrm{HCl}\), at 25 °C. Find \([\mathrm{H_3O^+}]\), the pH and the pOH."""),
  _p('N2a', 'Off the Scale', 'HCl', 0.3, None, None, '', 'acid, everyday range', r"""A bottle holds 0.300 M hydrochloric acid, \(\mathrm{HCl}\), at 25 °C. Find \([\mathrm{H_3O^+}]\), the pH and the pOH."""),
  _p('N2b', 'Off the Scale', 'HNO3', 0.025, None, None, '', 'acid, everyday range', r"""A bottle holds 0.025 M nitric acid, \(\mathrm{HNO_3}\), at 25 °C. Find \([\mathrm{H_3O^+}]\), the pH and the pOH."""),
  _p('N2c', 'Off the Scale', 'HCl', 0.004, None, None, '', 'acid, everyday range', r"""A bottle holds 0.0040 M hydrochloric acid, \(\mathrm{HCl}\), at 25 °C. Find \([\mathrm{H_3O^+}]\), the pH and the pOH."""),
  _p('N3a', 'Off the Scale', 'HCl', 0.00025, None, None, '', 'dilute acid', r"""A bottle holds \(2.5 \times 10^{-4}\) M hydrochloric acid, \(\mathrm{HCl}\), at 25 °C. Find \([\mathrm{H_3O^+}]\), the pH and the pOH."""),
  _p('N3b', 'Off the Scale', 'HNO3', 3.2000000000000005e-05, None, None, '', 'dilute acid', r"""A bottle holds \(3.2 \times 10^{-5}\) M nitric acid, \(\mathrm{HNO_3}\), at 25 °C. Find \([\mathrm{H_3O^+}]\), the pH and the pOH."""),
  _p('N3c', 'Off the Scale', 'HCl', 0.0005, None, None, '', 'dilute acid', r"""A bottle holds \(5.0 \times 10^{-4}\) M hydrochloric acid, \(\mathrm{HCl}\), at 25 °C. Find \([\mathrm{H_3O^+}]\), the pH and the pOH."""),
  _p('N4a', 'Off the Scale', 'NaOH', 0.025, None, None, '', 'base, everyday range', r"""A bottle holds 0.0250 M sodium hydroxide, \(\mathrm{NaOH}\), at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('N4b', 'Off the Scale', 'KOH', 0.05, None, None, '', 'base, everyday range', r"""A bottle holds 0.050 M potassium hydroxide, \(\mathrm{KOH}\), at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('N4c', 'Off the Scale', 'NaOH', 0.003, None, None, '', 'base, everyday range', r"""A bottle holds 0.0030 M sodium hydroxide, \(\mathrm{NaOH}\), at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('N5a', 'Off the Scale', 'NaOH', 1.5, None, None, '', 'base above 1 M', r"""A bottle holds 1.5 M sodium hydroxide, \(\mathrm{NaOH}\), at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('N5b', 'Off the Scale', 'KOH', 3.0, None, None, '', 'base above 1 M', r"""A bottle holds 3.0 M potassium hydroxide, \(\mathrm{KOH}\), at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('N5c', 'Off the Scale', 'NaOH', 4.0, None, None, '', 'base above 1 M', r"""A bottle holds 4.0 M sodium hydroxide, \(\mathrm{NaOH}\), at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('N6a', 'Off the Scale', 'Ba(OH)2', None, 2e-05, 0.5, '', 'two hydroxides per formula, moles in a volume', r"""A student dissolves \(2.00 \times 10^{-5}\) mol of barium hydroxide, \(\mathrm{Ba(OH)_2}\), in water to make 0.500 L of solution at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('N6b', 'Off the Scale', 'Ba(OH)2', None, 0.0025, 0.5, '', 'two hydroxides per formula, moles in a volume', r"""A student dissolves 0.00250 mol of barium hydroxide, \(\mathrm{Ba(OH)_2}\), in water to make 0.500 L of solution at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('N6c', 'Off the Scale', 'Ba(OH)2', None, 0.0075, 0.5, '', 'two hydroxides per formula, moles in a volume', r"""A student dissolves 0.00750 mol of barium hydroxide, \(\mathrm{Ba(OH)_2}\), in water to make 0.500 L of solution at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('W1', 'The Corn Soak', 'NaOH', None, 0.003, 0.5, 'one_hydroxide', 'core: monohydroxide (worked)', r"""A cook makes a corn soak with lye. 0.003 mol of sodium hydroxide, \(\mathrm{NaOH}\), is dissolved in water to make 0.5 L of solution at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('W2', 'The Corn Soak', 'Ca(OH)2', None, 0.003, 0.5, 'two_hydroxides', 'variant: two hydroxides (worked offer)', r"""A cook makes a corn soak with pickling lime. 0.003 mol of calcium hydroxide, \(\mathrm{Ca(OH)_2}\), is dissolved in water to make 0.5 L of solution at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('W3', 'The Corn Soak', 'HCl', 0.002, None, None, '', 'strong acid', r"""Stomach acid is modeled as hydrochloric acid. A solution is 0.002 M hydrochloric acid, \(\mathrm{HCl}\), at 25 °C. Find \([\mathrm{H_3O^+}]\), the pH and the pOH."""),
  _p('W4', 'The Corn Soak', 'HCl', 0.01, None, None, '', 'strong acid', r"""A solution is 0.01 M hydrochloric acid, \(\mathrm{HCl}\), at 25 °C. Find \([\mathrm{H_3O^+}]\), the pH and the pOH."""),
  _p('W5', 'The Corn Soak', 'Ca(OH)2', None, 0.002, 0.5, '', 'two hydroxides', r"""0.002 mol of calcium hydroxide, \(\mathrm{Ca(OH)_2}\), is dissolved in water to make 0.5 L of solution at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('W6', 'The Corn Soak', 'KOH', 0.02, None, None, '', 'monohydroxide', r"""A solution is 0.02 M potassium hydroxide, \(\mathrm{KOH}\), at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('R1', 'The Stockroom Morning', 'NaOH', None, 0.002, 0.5, '', 'monohydroxide', r"""0.002 mol of sodium hydroxide, \(\mathrm{NaOH}\), is dissolved in water to make 0.5 L of solution at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('R2', 'The Stockroom Morning', 'Ba(OH)2', None, 0.002, 0.5, '', 'two hydroxides', r"""0.002 mol of barium hydroxide, \(\mathrm{Ba(OH)_2}\), is dissolved in water to make 0.5 L of solution at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('R3', 'The Stockroom Morning', 'Ca(OH)2', None, 0.0015, 0.5, '', 'two hydroxides', r"""0.0015 mol of calcium hydroxide, \(\mathrm{Ca(OH)_2}\), is dissolved in water to make 0.5 L of solution at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('R4', 'The Stockroom Morning', 'HNO3', 0.006, None, None, '', 'strong acid', r"""A solution is 0.006 M nitric acid, \(\mathrm{HNO_3}\), at 25 °C. Find \([\mathrm{H_3O^+}]\), the pH and the pOH."""),
  _p('R5', 'The Stockroom Morning', 'HCl', 0.05, None, None, '', 'strong acid', r"""A solution is 0.05 M hydrochloric acid, \(\mathrm{HCl}\), at 25 °C. Find \([\mathrm{H_3O^+}]\), the pH and the pOH."""),
  _p('R6', 'The Stockroom Morning', 'KOH', 0.002, None, None, '', 'monohydroxide', r"""A solution is 0.002 M potassium hydroxide, \(\mathrm{KOH}\), at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('E1', 'Concrete Burn', 'Ca(OH)2', None, 0.0025, 0.5, '', 'two hydroxides, moles in a volume (exam: every version the same concepts)', r"""A lab models the water in wet concrete with calcium hydroxide. 0.0025 mol of calcium hydroxide, \(\mathrm{Ca(OH)_2}\), is dissolved in water to make 0.5 L of solution at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('E2', 'Concrete Burn', 'Ca(OH)2', None, 0.001, 0.25, '', 'two hydroxides, moles in a volume (exam: every version the same concepts)', r"""A lab models the water in wet concrete with calcium hydroxide. 0.001 mol of calcium hydroxide, \(\mathrm{Ca(OH)_2}\), is dissolved in water to make 0.25 L of solution at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('E3', 'Concrete Burn', 'Ca(OH)2', None, 0.0005, 0.2, '', 'two hydroxides, moles in a volume (exam: every version the same concepts)', r"""A lab models the water in wet concrete with calcium hydroxide. 0.0005 mol of calcium hydroxide, \(\mathrm{Ca(OH)_2}\), is dissolved in water to make 0.2 L of solution at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('E4', 'Concrete Burn', 'Ca(OH)2', None, 0.009, 1.5, '', 'two hydroxides, moles in a volume (exam: every version the same concepts)', r"""A lab models the water in wet concrete with calcium hydroxide. 0.009 mol of calcium hydroxide, \(\mathrm{Ca(OH)_2}\), is dissolved in water to make 1.5 L of solution at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('E5', 'Concrete Burn', 'Ca(OH)2', None, 0.0015, 0.75, '', 'two hydroxides, moles in a volume (exam: every version the same concepts)', r"""A lab models the water in wet concrete with calcium hydroxide. 0.0015 mol of calcium hydroxide, \(\mathrm{Ca(OH)_2}\), is dissolved in water to make 0.75 L of solution at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
  _p('E6', 'Concrete Burn', 'Ca(OH)2', None, 0.012, 4.0, '', 'two hydroxides, moles in a volume (exam: every version the same concepts)', r"""A lab models the water in wet concrete with calcium hydroxide. 0.012 mol of calcium hydroxide, \(\mathrm{Ca(OH)_2}\), is dissolved in water to make 4 L of solution at 25 °C. Find \([\mathrm{OH^-}]\), the pH and the pOH."""),
]

def make_fixed(rng, fid):
    P = [f for f in FIXED if f["id"] == fid][0]; s = strong(P["strong"]); k = s["ions_per_formula"]; is_acid = s["kind"] == "acid"
    by_moles = P["n"] is not None
    c_formula = P["n"] / P["V"] if by_moles else P["conc"]; c = c_formula * k
    h = c if is_acid else KW / c; pH = pH_of(h); pOH = 14 - pH; ion = "[H3O+]" if is_acid else "[OH-]"
    expected = [E("ion_found", f"{ion} from the formula", c, "M", role="intermediate", require_unit=True, after="relation_chosen"),
                E("pH_found", "pH", pH, "", role="key", require_unit=False, after="ion_found"),
                E("pOH_found", "pOH", pOH, "", role="intermediate", require_unit=False, after="pH_found")]
    traps = []
    if not is_acid: traps.append(trap("POH_TYPED_AS_PH", pOH, "pH_found"))
    if k > 1: traps.append(trap("IONS_PER_FORMULA_IGNORED", c_formula, "ion_found", "M"))        # detectable only when c_formula is not itself a given (moles problems)
    if by_moles:
        traps.append(trap("MOLES_NOT_CONCENTRATION", P["n"] * k, "ion_found", "M"))            # the moles typed as M (times the ions per formula)
        if k > 1: traps.append(trap("MOLES_NOT_CONCENTRATION", P["n"], "ion_found", "M"))
    if pH < 0: traps.append(trap("PH_SIGN_DROPPED", -pH, "pH_found"))                           # a pH below zero written positive (Off the Scale)
    if pOH < 0: traps += [trap("POH_SIGN_DROPPED", -pOH, "pOH_found"), trap("POH_SIGN_DROPPED", 28 - pH, "pH_found")]
    ln_pH = -math.log(h) if is_acid else 14 + math.log(c)                                         # the natural logarithm used where log was meant
    traps.append(trap("LN_FOR_LOG", ln_pH, "pH_found"))
    traps = keep_clear(traps, expected)
    named = {"falls" if is_acid else "rises": "DILUTION_AWAY_FROM_7"}                              # dilution moves every pH toward 7
    board = head() + [{"state": "ion_found", "kind": "number", "register": "symbolic", "requires": ["relation_chosen"], "explicit": True, "pin": True},
                      {"state": "pH_found", "kind": "number", "register": "macro", "requires": ["ion_found"], "explicit": True, "pin": True},
                      {"state": "pOH_found", "kind": "number", "register": "symbolic", "requires": ["pH_found"], "explicit": True},
                      direction_item("perturb_1", "p1", "pH", "rises" if is_acid else "falls", named, "pOH_found"),
                      {"state": "perturb_1_why", "kind": "text", "register": "submicro", "requires": ["perturb_1"]}]
    tail(board, "perturb_1_why")
    givens = {"n": {"value": P["n"], "unit": "mol"}, "V": {"value": P["V"], "unit": "L"}} if by_moles else {"c": {"value": P["conc"], "unit": "M"}}
    return {"kind": P["kind"], "fixed_id": fid, "version": P["version"], "status": P["status"], "context": {"family": P["family"], "pH": round_sig(pH, 4), "c_formula": round_sig(c_formula, 5)}, "text": P["text"],
            "givens": givens, "board": board, "targets": expected, "traps": traps, "table": None, "words": {"substance": s["name"], "formula": P["strong"]},
            "eq_checks": [], "reveal_with_problem": None, "sim": None, "sim_params": {"strong": P["strong"], "c": round_sig(c_formula, 6)}}
def render_text(*a): raise NotImplementedError
