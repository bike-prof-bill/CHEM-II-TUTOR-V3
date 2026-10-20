"""Chapter 14, archetype 2 of 4: Acids & Bases (weak acids and weak bases). Fixed problems: 12, from SCENARIO_CLAUDE's sheets
approved 16-17 Oct 2026 (Same Label, Different pH, worked, with the failing-rule offer; The Fishy Bowl, exam, every version holding the
5 % rule by the instructor's decision; The Weak Acid That Eats Glass and The Bleach Puzzle, floaters: the bleach problems give Ka of the
partner acid and Kw, and the base's Kb in the data file is Kw/Ka). Step map: account -> relation (the Ka or Kb expression) -> table -> expression_set -> method (small-x when the
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
def _p(fid, opener, kind, key, conc, version, family, text):
    rx = acid(key) if kind == "acid" else base(key)
    return {"id": fid, "opener": opener, "kind": "weak_" + kind, "rx": rx, "conc": conc, "version": version, "family": family, "text": text, "sf": 2,
            "status": "approved (SCENARIO_CLAUDE's sheet; instructor, 16-17 Oct 2026)"}
FIXED = [   # 24 problems, four scenarios (Same Label worked, Fishy Bowl exam, Weak Acid That Eats Glass and Bleach Puzzle floaters)
  _p('K1', 'Same Label, Different pH', 'acid', 'acetic', 0.1, 'holds', 'core: 5 % rule holds (worked)', r"""For the lab, the stockroom worker makes 0.10 M acetic acid, acetic acid, \(\mathrm{CH_3COOH}\), at 25 °C. \(K_a = \) \(1.8 \times 10^{-5}\). Set up the ICE table. Find \([\mathrm{H_3O^+}]\), the pH and the percent ionized. Then check the 5 % rule."""),
  _p('K2', 'Same Label, Different pH', 'acid', 'acetic', 0.0005, 'fails', 'variant: 5 % rule fails, quadratic (worked offer)', r"""She dilutes some acetic acid all the way to 0.00050 M, acetic acid, \(\mathrm{CH_3COOH}\), at 25 °C. \(K_a = \) \(1.8 \times 10^{-5}\). Set up the ICE table. Find \([\mathrm{H_3O^+}]\), the pH and the percent ionized. Then check the 5 % rule."""),
  _p('K3', 'Same Label, Different pH', 'acid', 'formic', 0.5, '', 'weak acid, rule holds', r"""A bottle holds 0.50 M formic acid, formic acid, \(\mathrm{HCOOH}\), at 25 °C. \(K_a = \) \(1.8 \times 10^{-4}\). Set up the ICE table. Find \([\mathrm{H_3O^+}]\), the pH and the percent ionized. Then check the 5 % rule."""),
  _p('K4', 'Same Label, Different pH', 'acid', 'hypochlorous', 0.05, '', 'weak acid, very small Ka', r"""A bottle holds 0.050 M hypochlorous acid, hypochlorous acid, \(\mathrm{HClO}\), at 25 °C. \(K_a = \) \(2.9 \times 10^{-8}\). Set up the ICE table. Find \([\mathrm{H_3O^+}]\), the pH and the percent ionized. Then check the 5 % rule."""),
  _p('K5', 'Same Label, Different pH', 'acid', 'hydrofluoric', 0.02, '', 'weak acid, rule fails, quadratic', r"""A plastic bottle holds 0.020 M hydrofluoric acid, hydrofluoric acid, \(\mathrm{HF}\), at 25 °C. \(K_a = \) \(6.4 \times 10^{-4}\). Set up the ICE table. Find \([\mathrm{H_3O^+}]\), the pH and the percent ionized. Then check the 5 % rule."""),
  _p('K6', 'Same Label, Different pH', 'base', 'ammonia', 0.15, '', 'weak base, rule holds', r"""A bottle holds 0.15 M ammonia, ammonia, \(\mathrm{NH_3}\), at 25 °C. \(K_b = \) \(1.8 \times 10^{-5}\). Set up the ICE table. Find \([\mathrm{OH^-}]\), the pOH, the pH and the percent ionized. Then check the 5 % rule."""),
  _p('X1', 'The Fishy Bowl', 'base', 'trimethylamine', 0.1, '', 'weak base, 5 % rule holds (exam: every version the same concepts)', r"""A lab models fish rinse water with 0.1 M trimethylamine, \(\mathrm{(CH_3)_3N}\), at 25 °C. \(K_b = 6.3 \times 10^{-5}\). Set up the ICE table. Find \([\mathrm{OH^-}]\), the pOH, the pH and the percent ionized. Then check the 5 % rule."""),
  _p('X2', 'The Fishy Bowl', 'base', 'trimethylamine', 0.25, '', 'weak base, 5 % rule holds (exam: every version the same concepts)', r"""A lab models fish rinse water with 0.25 M trimethylamine, \(\mathrm{(CH_3)_3N}\), at 25 °C. \(K_b = 6.3 \times 10^{-5}\). Set up the ICE table. Find \([\mathrm{OH^-}]\), the pOH, the pH and the percent ionized. Then check the 5 % rule."""),
  _p('X3', 'The Fishy Bowl', 'base', 'ammonia', 0.2, '', 'weak base, 5 % rule holds (exam: every version the same concepts)', r"""A lab models fish rinse water with 0.2 M ammonia, \(\mathrm{NH_3}\), at 25 °C. \(K_b = 1.8 \times 10^{-5}\). Set up the ICE table. Find \([\mathrm{OH^-}]\), the pOH, the pH and the percent ionized. Then check the 5 % rule."""),
  _p('X4', 'The Fishy Bowl', 'base', 'ammonia', 0.05, '', 'weak base, 5 % rule holds (exam: every version the same concepts)', r"""A lab models fish rinse water with 0.05 M ammonia, \(\mathrm{NH_3}\), at 25 °C. \(K_b = 1.8 \times 10^{-5}\). Set up the ICE table. Find \([\mathrm{OH^-}]\), the pOH, the pH and the percent ionized. Then check the 5 % rule."""),
  _p('X5', 'The Fishy Bowl', 'base', 'methylamine', 0.5, '', 'weak base, 5 % rule holds (exam: every version the same concepts)', r"""A lab models fish rinse water with 0.5 M methylamine, \(\mathrm{CH_3NH_2}\), at 25 °C. \(K_b = 4.4 \times 10^{-4}\). Set up the ICE table. Find \([\mathrm{OH^-}]\), the pOH, the pH and the percent ionized. Then check the 5 % rule."""),
  _p('X6', 'The Fishy Bowl', 'base', 'dimethylamine', 0.8, '', 'weak base, 5 % rule holds (exam: every version the same concepts)', r"""A lab models fish rinse water with 0.8 M dimethylamine, \(\mathrm{(CH_3)_2NH}\), at 25 °C. \(K_b = 5.9 \times 10^{-4}\). Set up the ICE table. Find \([\mathrm{OH^-}]\), the pOH, the pH and the percent ionized. Then check the 5 % rule."""),
  _p('H1', 'The Weak Acid That Eats Glass', 'acid', 'hydrofluoric', 1.0, '', 'weak acid, 5 % rule holds', r"""A plastic bottle holds 1 M hydrofluoric acid, \(\mathrm{HF}\), at 25 °C. \(K_a = 6.4 \times 10^{-4}\). Set up the ICE table. Find \([\mathrm{H_3O^+}]\), the pH and the percent ionized. Then check the 5 % rule."""),
  _p('H2', 'The Weak Acid That Eats Glass', 'acid', 'hydrofluoric', 0.1, '', 'weak acid, 5 % rule fails', r"""A plastic bottle holds 0.1 M hydrofluoric acid, \(\mathrm{HF}\), at 25 °C. \(K_a = 6.4 \times 10^{-4}\). Set up the ICE table. Find \([\mathrm{H_3O^+}]\), the pH and the percent ionized. Then check the 5 % rule."""),
  _p('H3', 'The Weak Acid That Eats Glass', 'acid', 'hydrofluoric', 0.05, '', 'weak acid, 5 % rule fails', r"""A plastic bottle holds 0.05 M hydrofluoric acid, \(\mathrm{HF}\), at 25 °C. \(K_a = 6.4 \times 10^{-4}\). Set up the ICE table. Find \([\mathrm{H_3O^+}]\), the pH and the percent ionized. Then check the 5 % rule."""),
  _p('H4', 'The Weak Acid That Eats Glass', 'acid', 'hydrofluoric', 0.5, '', 'weak acid, 5 % rule holds', r"""A plastic bottle holds 0.5 M hydrofluoric acid, \(\mathrm{HF}\), at 25 °C. \(K_a = 6.4 \times 10^{-4}\). Set up the ICE table. Find \([\mathrm{H_3O^+}]\), the pH and the percent ionized. Then check the 5 % rule."""),
  _p('H5', 'The Weak Acid That Eats Glass', 'acid', 'nitrous', 0.02, '', 'weak acid, 5 % rule fails', r"""A plastic bottle holds 0.02 M nitrous acid, \(\mathrm{HNO_2}\), at 25 °C. \(K_a = 4.6 \times 10^{-4}\). Set up the ICE table. Find \([\mathrm{H_3O^+}]\), the pH and the percent ionized. Then check the 5 % rule."""),
  _p('H6', 'The Weak Acid That Eats Glass', 'acid', 'formic', 0.3, '', 'weak acid, 5 % rule holds', r"""A plastic bottle holds 0.3 M formic acid, \(\mathrm{HCOOH}\), at 25 °C. \(K_a = 1.8 \times 10^{-4}\). Set up the ICE table. Find \([\mathrm{H_3O^+}]\), the pH and the percent ionized. Then check the 5 % rule."""),
  _p('C1', 'The Bleach Puzzle', 'base', 'hypochlorite', 0.7, '', 'weak base, 5 % rule holds', r"""A solution is 0.7 M sodium hypochlorite, \(\mathrm{NaClO}\), at 25 °C. For hypochlorous acid, \(K_a = 2.9 \times 10^{-8}\); \(K_w = 1.0 \times 10^{-14}\). Find Kb for the anion. Set up the ICE table. Find \([\mathrm{OH^-}]\), the pOH, the pH and the percent ionized. Then check the 5 % rule."""),
  _p('C2', 'The Bleach Puzzle', 'base', 'hypochlorite', 0.1, '', 'weak base, 5 % rule holds', r"""A solution is 0.1 M sodium hypochlorite, \(\mathrm{NaClO}\), at 25 °C. For hypochlorous acid, \(K_a = 2.9 \times 10^{-8}\); \(K_w = 1.0 \times 10^{-14}\). Find Kb for the anion. Set up the ICE table. Find \([\mathrm{OH^-}]\), the pOH, the pH and the percent ionized. Then check the 5 % rule."""),
  _p('C3', 'The Bleach Puzzle', 'base', 'acetate', 0.5, '', 'weak base, 5 % rule holds', r"""A solution is 0.5 M sodium acetate, \(\mathrm{NaCH_3COO}\), at 25 °C. For acetic acid, \(K_a = 1.8 \times 10^{-5}\); \(K_w = 1.0 \times 10^{-14}\). Find Kb for the anion. Set up the ICE table. Find \([\mathrm{OH^-}]\), the pOH, the pH and the percent ionized. Then check the 5 % rule."""),
  _p('C4', 'The Bleach Puzzle', 'base', 'acetate', 0.1, '', 'weak base, 5 % rule holds', r"""A solution is 0.1 M sodium acetate, \(\mathrm{NaCH_3COO}\), at 25 °C. For acetic acid, \(K_a = 1.8 \times 10^{-5}\); \(K_w = 1.0 \times 10^{-14}\). Find Kb for the anion. Set up the ICE table. Find \([\mathrm{OH^-}]\), the pOH, the pH and the percent ionized. Then check the 5 % rule."""),
  _p('C5', 'The Bleach Puzzle', 'base', 'methylamine', 0.01, '', 'weak base, 5 % rule fails', r"""A lab solution is 0.01 M methylamine, \(\mathrm{CH_3NH_2}\), at 25 °C. \(K_b = 4.4 \times 10^{-4}\). Set up the ICE table. Find \([\mathrm{OH^-}]\), the pOH, the pH and the percent ionized. Then check the 5 % rule."""),
  _p('C6', 'The Bleach Puzzle', 'base', 'hypochlorite', 0.02, '', 'weak base, 5 % rule holds', r"""A solution is 0.02 M sodium hypochlorite, \(\mathrm{NaClO}\), at 25 °C. For hypochlorous acid, \(K_a = 2.9 \times 10^{-8}\); \(K_w = 1.0 \times 10^{-14}\). Find Kb for the anion. Set up the ICE table. Find \([\mathrm{OH^-}]\), the pOH, the pH and the percent ionized. Then check the 5 % rule."""),
]

def make_fixed(rng, fid):
    P = [f for f in FIXED if f["id"] == fid][0]; rx = P["rx"]; c = P["conc"]; is_acid = rx["kind"] == "acid"
    expected, traps, board = [], [], head()
    prev = "relation_chosen"
    if not is_acid and "K_a" in P["text"] and "K_b" not in P["text"]:      # the problem gives Ka of the partner acid: Kb = Kw/Ka is a step (instructor, 19 Oct)
        Ka_partner = KW / rx["K"]
        expected.append(E("Kb_found", "Kb of the base, from Kw and the partner's Ka", rx["K"], "", role="intermediate", require_unit=False, after="relation_chosen"))
        traps.append(trap("KA_USED_AS_KB", Ka_partner, "Kb_found"))
        board.append({"state": "Kb_found", "kind": "number", "register": "symbolic", "requires": ["relation_chosen"], "explicit": True, "pin": True}); prev = "Kb_found"
    prev, w, table, eqc = weak_chain(rx, c, expected, traps, board, prev)
    if not is_acid: traps.append(trap("POH_TYPED_AS_PH", w["pOH"], "pH_found"))     # asked for by the sheet; fires only if the pOH was not already established as a step
    traps = keep_clear(traps, expected)
    named1 = {"falls": "DILUTION_IONIZATION_FALLS"}; named2 = {"falls": "CONJUGATE_LOWERS_PH"} if is_acid else {"rises": "CONJUGATE_RAISES_PH"}
    board += [direction_item("perturb_1", "p1", "percent ionised", "rises", named1, prev), {"state": "perturb_1_why", "kind": "text", "register": "submicro", "requires": ["perturb_1"]},
              direction_item("perturb_2", "p2", "pH", "rises" if is_acid else "falls", named2, "perturb_1_why"), {"state": "perturb_2_why", "kind": "text", "register": "submicro", "requires": ["perturb_2"]}]
    tail(board, "perturb_2_why")
    return {"kind": P["kind"], "fixed_id": fid, "version": P["version"], "status": P["status"], "text": P["text"],
            "context": {"family": P["family"], "x": round_sig(w["x"], 5), "pH": round_sig(w["pH"], 4), "percent": round_sig(w["percent"], 4), "approx_ok": w["approx_ok"]},
            "givens": {"c": {"value": c, "unit": "M"}, ("Ka" if is_acid else "Kb"): {"value": rx["K"], "unit": ""}}, "board": board, "targets": expected, "traps": traps, "table": table,
            "words": dict(rx["words"]), "eq_checks": [eqc], "reveal_with_problem": None, "sim": None, "sim_params": {"species": rx["id"], "c": c, "K": rx["K"]}}
def render_text(*a): raise NotImplementedError
