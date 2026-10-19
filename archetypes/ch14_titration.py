"""Chapter 14, archetype 4 of 4: Titration. Fixed problems; placeholders DRAFT; ships nothing until a scenario is approved.
The instructor's four regions (15 Oct): the pure acid or base solution (the Ka or Kb equilibrium); Henderson-Hasselbalch up to just
before the equivalence point; salt hydrolysis at the equivalence point; pH set by the excess titrant after it. A strong acid with a
strong base has three: excess acid, pH 7.00, excess base.

Step map: account -> region_chosen (pick: start | before | at | after the equivalence point; computed from the moles) -> relation_chosen
(the relation that region needs) -> moles_found (moles of acid and of titrant, both, with units) -> the region's chain -> pH_found ->
side_of_7 (text: which side of 7 and why) -> meaning -> reflection.
  start:   the weak chain (table, expression, method, x, pH, percent, the 5 % check)                       [weak acid only]
  before:  ratio_found (moles of conjugate over moles of acid left) -> pH_found (Henderson-Hasselbalch)      [weak]
           excess_conc ([H3O+] from the excess acid over the total volume) -> pH_found                       [strong]
  at:      conc_found (the conjugate's concentration in the total volume) -> Kb_found (Kw/Ka) -> x_found -> pOH_found -> pH_found   [weak]
           pH_found = 7.00                                                                                   [strong]
  after:   excess_conc ([OH-] from the excess titrant over the total volume) -> pOH_found -> pH_found
"""
import math
from engine import round_sig
from _acidbase import *

ID = "ch14_titration"
TITLE = "Titration: the pH along the curve"
RELATION_TEXT = "moles decide the region; each region has its own relation: Ka, Henderson-Hasselbalch, the conjugate's Kb, or the excess over the total volume"
# one kind per pair and region, so the Equations list fits the region: the relation that region needs is the one that counts
KINDS = ["weak_start", "weak_before", "weak_at", "weak_after", "strong_before", "strong_at", "strong_after"]
EQUATION_PICKS = picks({"eq_ka": ["weak_start"], "eq_hh": ["weak_before"], "eq_kakb": ["weak_at"], "eq_excess": ["weak_after", "strong_before", "strong_after"], "eq_ph": ["strong_at"]})
CONSTANTS = [{"label": "Kw", "symbol": "Kw", "value": KW, "unit": ""}]
EQUATION_SYMBOLS = {"x": ["x"], "K": ["Ka", "K_a", "Kb", "K_b", "K"]}; EQUATION_CONSTANTS = {"Kw": KW}
MECHANISM_WORDS = MECHANISM_WORDS
TRAP_NOTES = TRAP_NOTES_COMMON
REGION_OPTIONS = [{"id": "region:start", "text": "start: no titrant yet, the acid alone"}, {"id": "region:before", "text": "before the equivalence point: some acid left, some conjugate made"},
                  {"id": "region:at", "text": "at the equivalence point: the acid is used up"}, {"id": "region:after", "text": "after the equivalence point: titrant in excess"}]
# which relation each region needs (the right pick on relation_chosen)
RELATION_FOR = {("weak", "start"): "eq_ka", ("weak", "before"): "eq_hh", ("weak", "at"): "eq_kakb", ("weak", "after"): "eq_excess",
                ("strong", "before"): "eq_excess", ("strong", "at"): "eq_ph", ("strong", "after"): "eq_excess", ("strong", "start"): "eq_ph"}

def _region(ca, va, cb, vb):
    na, nb = ca * va, cb * vb
    return "start" if nb == 0 else ("before" if nb < na - 1e-12 else ("at" if abs(nb - na) <= 1e-12 else "after"))
def _p(fid, opener, key, ca, va_ml, cb, vb_ml, version, family, text):
    rx = None if key == "HCl" else acid(key); pair = "strong" if rx is None else "weak"
    return {"id": fid, "opener": opener, "kind": f"{pair}_{_region(ca, va_ml, cb, vb_ml)}", "pair": pair, "rx": rx, "ca": ca, "va": va_ml, "cb": cb, "vb": vb_ml, "version": version, "family": family, "text": text, "sf": 2,
            "status": "approved (SCENARIO_CLAUDE's sheet; instructor, 17 Oct 2026)"}
FIXED = [   # 24 problems: The Vinegar Lab (worked; HCl offer), The Kombucha Check (exam, six at equivalence), The Stockroom Standard (strong), The Sour Whey (lactic acid, all four regions)
  _p('V1', 'The Vinegar Lab', 'acetic', 0.08, 25.0, 0.1, 20.0, 'weak', 'core: at equivalence (worked)', r"""In the lab, a 25.00 mL sample of 0.0800 M acetic acid, \(\mathrm{CH_3COOH}\) (\(K_a = 1.8 \times 10^{-5}\)), from diluted vinegar is titrated with 0.100 M NaOH at 25 °C. 20.00 mL of the base has been added. Where on the curve is this, and what is the pH?"""),
  _p('V2', 'The Vinegar Lab', 'HCl', 0.08, 25.0, 0.1, 20.0, 'strong', 'variant: HCl at equivalence (worked offer)', r"""In the lab, a 25.00 mL sample of 0.0800 M hydrochloric acid, \(\mathrm{HCl}\), is titrated with 0.100 M NaOH at 25 °C. 20.00 mL of the base has been added. Where on the curve is this, and what is the pH?"""),
  _p('V3', 'The Vinegar Lab', 'acetic', 0.08, 25.0, 0.1, 0.0, '', 'start: the acid alone', r"""In the lab, a 25.00 mL sample of 0.0800 M acetic acid, \(\mathrm{CH_3COOH}\) (\(K_a = 1.8 \times 10^{-5}\)), from diluted vinegar is titrated with 0.100 M NaOH at 25 °C. No base has been added yet. Where on the curve is this, and what is the pH?"""),
  _p('V4', 'The Vinegar Lab', 'acetic', 0.08, 25.0, 0.1, 15.0, '', 'before equivalence', r"""In the lab, a 25.00 mL sample of 0.0800 M acetic acid, \(\mathrm{CH_3COOH}\) (\(K_a = 1.8 \times 10^{-5}\)), from diluted vinegar is titrated with 0.100 M NaOH at 25 °C. 15.00 mL of the base has been added. Where on the curve is this, and what is the pH?"""),
  _p('V5', 'The Vinegar Lab', 'acetic', 0.08, 25.0, 0.1, 25.0, '', 'after equivalence', r"""In the lab, a 25.00 mL sample of 0.0800 M acetic acid, \(\mathrm{CH_3COOH}\) (\(K_a = 1.8 \times 10^{-5}\)), from diluted vinegar is titrated with 0.100 M NaOH at 25 °C. 25.00 mL of the base has been added. Where on the curve is this, and what is the pH?"""),
  _p('V6', 'The Vinegar Lab', 'HCl', 0.08, 25.0, 0.1, 15.0, '', 'strong acid, before equivalence', r"""In the lab, a 25.00 mL sample of 0.0800 M hydrochloric acid, \(\mathrm{HCl}\), is titrated with 0.100 M NaOH at 25 °C. 15.00 mL of the base has been added. Where on the curve is this, and what is the pH?"""),
  _p('K1', 'The Kombucha Check', 'acetic', 0.03, 20.0, 0.1, 6.0, '', 'weak acid at equivalence (exam: every version the same concepts)', r"""A 20.00 mL aliquot of raw kombucha, taken as 0.03 M acetic acid, \(\mathrm{CH_3COOH}\) (\(K_a = 1.8 \times 10^{-5}\)), is titrated with 0.100 M NaOH at 25 °C. The phenolphthalein endpoint comes at 6.00 mL. Where on the curve is this, and what is the pH?"""),
  _p('K2', 'The Kombucha Check', 'acetic', 0.035, 20.0, 0.1, 7.0, '', 'weak acid at equivalence (exam: every version the same concepts)', r"""A 20.00 mL aliquot of raw kombucha, taken as 0.035 M acetic acid, \(\mathrm{CH_3COOH}\) (\(K_a = 1.8 \times 10^{-5}\)), is titrated with 0.100 M NaOH at 25 °C. The phenolphthalein endpoint comes at 7.00 mL. Where on the curve is this, and what is the pH?"""),
  _p('K3', 'The Kombucha Check', 'acetic', 0.04, 20.0, 0.1, 8.0, '', 'weak acid at equivalence (exam: every version the same concepts)', r"""A 20.00 mL aliquot of raw kombucha, taken as 0.04 M acetic acid, \(\mathrm{CH_3COOH}\) (\(K_a = 1.8 \times 10^{-5}\)), is titrated with 0.100 M NaOH at 25 °C. The phenolphthalein endpoint comes at 8.00 mL. Where on the curve is this, and what is the pH?"""),
  _p('K4', 'The Kombucha Check', 'acetic', 0.045, 20.0, 0.1, 9.0, '', 'weak acid at equivalence (exam: every version the same concepts)', r"""A 20.00 mL aliquot of raw kombucha, taken as 0.045 M acetic acid, \(\mathrm{CH_3COOH}\) (\(K_a = 1.8 \times 10^{-5}\)), is titrated with 0.100 M NaOH at 25 °C. The phenolphthalein endpoint comes at 9.00 mL. Where on the curve is this, and what is the pH?"""),
  _p('K5', 'The Kombucha Check', 'acetic', 0.0325, 20.0, 0.1, 6.5, '', 'weak acid at equivalence (exam: every version the same concepts)', r"""A 20.00 mL aliquot of raw kombucha, taken as 0.0325 M acetic acid, \(\mathrm{CH_3COOH}\) (\(K_a = 1.8 \times 10^{-5}\)), is titrated with 0.100 M NaOH at 25 °C. The phenolphthalein endpoint comes at 6.50 mL. Where on the curve is this, and what is the pH?"""),
  _p('K6', 'The Kombucha Check', 'acetic', 0.0375, 20.0, 0.1, 7.5, '', 'weak acid at equivalence (exam: every version the same concepts)', r"""A 20.00 mL aliquot of raw kombucha, taken as 0.0375 M acetic acid, \(\mathrm{CH_3COOH}\) (\(K_a = 1.8 \times 10^{-5}\)), is titrated with 0.100 M NaOH at 25 °C. The phenolphthalein endpoint comes at 7.50 mL. Where on the curve is this, and what is the pH?"""),
  _p('S1', 'The Stockroom Standard', 'HCl', 2.0, 10.0, 1.0, 5.0, '', 'strong: before', r"""The stockroom titrates a 10.00 mL sample of 2.00 M hydrochloric acid, \(\mathrm{HCl}\), with 1.000 M NaOH at 25 °C. 5.00 mL of the base has been added. Where on the curve is this, and what is the pH?"""),
  _p('S2', 'The Stockroom Standard', 'HCl', 2.0, 10.0, 1.0, 15.0, '', 'strong: before', r"""The stockroom titrates a 10.00 mL sample of 2.00 M hydrochloric acid, \(\mathrm{HCl}\), with 1.000 M NaOH at 25 °C. 15.00 mL of the base has been added. Where on the curve is this, and what is the pH?"""),
  _p('S3', 'The Stockroom Standard', 'HCl', 2.0, 10.0, 1.0, 19.5, '', 'strong: before', r"""The stockroom titrates a 10.00 mL sample of 2.00 M hydrochloric acid, \(\mathrm{HCl}\), with 1.000 M NaOH at 25 °C. 19.50 mL of the base has been added. Where on the curve is this, and what is the pH?"""),
  _p('S4', 'The Stockroom Standard', 'HCl', 2.0, 10.0, 1.0, 20.0, '', 'strong: at', r"""The stockroom titrates a 10.00 mL sample of 2.00 M hydrochloric acid, \(\mathrm{HCl}\), with 1.000 M NaOH at 25 °C. 20.00 mL of the base has been added. Where on the curve is this, and what is the pH?"""),
  _p('S5', 'The Stockroom Standard', 'HCl', 2.0, 10.0, 1.0, 22.0, '', 'strong: after', r"""The stockroom titrates a 10.00 mL sample of 2.00 M hydrochloric acid, \(\mathrm{HCl}\), with 1.000 M NaOH at 25 °C. 22.00 mL of the base has been added. Where on the curve is this, and what is the pH?"""),
  _p('S6', 'The Stockroom Standard', 'HCl', 2.0, 10.0, 1.0, 30.0, '', 'strong: after', r"""The stockroom titrates a 10.00 mL sample of 2.00 M hydrochloric acid, \(\mathrm{HCl}\), with 1.000 M NaOH at 25 °C. 30.00 mL of the base has been added. Where on the curve is this, and what is the pH?"""),
  _p('W1', 'The Sour Whey', 'lactic', 0.1, 10.0, 0.05, 0.0, '', 'weak: start', r"""A 10.00 mL sample of 0.100 M lactic acid (\(K_a = 1.36 \times 10^{-4}\)) is titrated with 0.0500 M NaOH at 25 °C. No base has been added yet. Where on the curve is this, and what is the pH?"""),
  _p('W2', 'The Sour Whey', 'lactic', 0.1, 10.0, 0.05, 5.0, '', 'weak: before', r"""A 10.00 mL sample of 0.100 M lactic acid (\(K_a = 1.36 \times 10^{-4}\)) is titrated with 0.0500 M NaOH at 25 °C. 5.00 mL of the base has been added. Where on the curve is this, and what is the pH?"""),
  _p('W3', 'The Sour Whey', 'lactic', 0.1, 10.0, 0.05, 15.0, '', 'weak: before', r"""A 10.00 mL sample of 0.100 M lactic acid (\(K_a = 1.36 \times 10^{-4}\)) is titrated with 0.0500 M NaOH at 25 °C. 15.00 mL of the base has been added. Where on the curve is this, and what is the pH?"""),
  _p('W4', 'The Sour Whey', 'lactic', 0.1, 10.0, 0.05, 20.0, '', 'weak: at', r"""A 10.00 mL sample of 0.100 M lactic acid (\(K_a = 1.36 \times 10^{-4}\)) is titrated with 0.0500 M NaOH at 25 °C. 20.00 mL of the base has been added. Where on the curve is this, and what is the pH?"""),
  _p('W5', 'The Sour Whey', 'lactic', 0.1, 10.0, 0.05, 10.0, '', 'weak: before', r"""A 10.00 mL sample of 0.100 M lactic acid (\(K_a = 1.36 \times 10^{-4}\)) is titrated with 0.0500 M NaOH at 25 °C. 10.00 mL of the base has been added. Where on the curve is this, and what is the pH?"""),
  _p('W6', 'The Sour Whey', 'lactic', 0.1, 10.0, 0.05, 25.0, '', 'weak: after', r"""A 10.00 mL sample of 0.100 M lactic acid (\(K_a = 1.36 \times 10^{-4}\)) is titrated with 0.0500 M NaOH at 25 °C. 25.00 mL of the base has been added. Where on the curve is this, and what is the pH?"""),
]

def make_fixed(rng, fid):
    P = [f for f in FIXED if f["id"] == fid][0]; weak = P["rx"] is not None; pair = P["pair"]
    na, nb = P["ca"] * P["va"] / 1000, P["cb"] * P["vb"] / 1000; Vt = (P["va"] + P["vb"]) / 1000
    region = _region(P["ca"], P["va"], P["cb"], P["vb"])
    expected, traps, board, table, eqc = [], [], [], None, []
    board += [{"state": "account_given", "kind": "text", "register": "submicro", "requires": []},
              {"state": "region_chosen", "kind": "pick", "register": "macro", "requires": ["account_given"], "options": REGION_OPTIONS, "right": ["region:" + region], "explicit": True, "pin": True},
              {"state": "relation_chosen", "kind": "pick", "register": "symbolic", "requires": ["region_chosen"], "options_from": "equation_picks", "pin": True}]
    # the moles are the hinge of every region (except the start): both, with units
    if region != "start":
        expected += [E("moles_found", "moles of acid in the sample", na, "mol", role="intermediate", require_unit=True), E("moles_found", "moles of base added", nb, "mol", role="intermediate", require_unit=True)]
        traps.append(trap("MOLES_FROM_ONE_SOLUTION", P["ca"] * (P["va"] + P["vb"]) / 1000, "moles_found", "mol"))
        board.append({"state": "moles_found", "kind": "number", "register": "symbolic", "requires": ["relation_chosen"], "rule": "all", "explicit": True, "pin": True}); prev = "moles_found"
    else: prev = "relation_chosen"
    pH = None
    if weak and region == "start":
        prev, w, table, e1 = weak_chain(P["rx"], P["ca"], expected, traps, board, prev); eqc = [e1]; pH = w["pH"]
    elif weak and region == "before":
        n_left, n_conj = na - nb, nb; ratio = n_conj / n_left; pH = hh_pH(P["rx"]["K"], ratio)
        expected += [E("ratio_found", "moles of conjugate over moles of acid left", ratio, "", role="intermediate", require_unit=False, after="moles_found"), E("pH_found", "pH", pH, "", role="key", require_unit=False, after="ratio_found")]
        traps += [trap("RATIO_INVERTED", 1 / ratio, "ratio_found") if abs(ratio - 1) > 1e-9 else None, trap("RATIO_INVERTED", hh_pH(P["rx"]["K"], 1 / ratio), "pH_found") if abs(ratio - 1) > 1e-9 else None,
                  trap("PH_FROM_FORMAL_CONCENTRATION", pH_of(n_left / Vt), "pH_found")]
        board += [{"state": "ratio_found", "kind": "number", "register": "symbolic", "requires": [prev], "explicit": True, "pin": True}, {"state": "pH_found", "kind": "number", "register": "macro", "requires": ["ratio_found"], "explicit": True, "pin": True}]
        prev = "pH_found"
    elif weak and region == "at":
        c_conj = na / Vt; Kb = KW / P["rx"]["K"]; x = math.sqrt(Kb * c_conj); pOH = pH_of(x); pH = 14 - pOH
        expected += [E("conc_found", "the conjugate base's concentration in the total volume", c_conj, "M", role="intermediate", require_unit=True, after="moles_found"),
                     E("Kb_found", "Kb of the conjugate base", Kb, "", role="intermediate", require_unit=False, after="conc_found"),
                     E("x_found", "x = [OH-]", x, "M", role="intermediate", require_unit=True, after="Kb_found"),
                     E("pOH_found", "pOH", pOH, "", role="intermediate", require_unit=False, after="x_found"), E("pH_found", "pH", pH, "", role="key", require_unit=False, after="pOH_found")]
        traps += [trap("VOLUME_NOT_TOTALED", na / (P["va"] / 1000), "conc_found", "M"), trap("KA_FOR_HYDROLYSIS", math.sqrt(P["rx"]["K"] * c_conj), "x_found", "M"),
                  trap("PH_7_AT_EQUIVALENCE", 7.0, "pH_found"), trap("POH_TYPED_AS_PH", pOH, "pH_found"), trap("HH_AT_EQUIVALENCE", -math.log10(P["rx"]["K"]), "pH_found")]
        board += [{"state": "conc_found", "kind": "number", "register": "symbolic", "requires": [prev], "explicit": True, "pin": True},
                  {"state": "Kb_found", "kind": "number", "register": "symbolic", "requires": ["conc_found"], "explicit": True},
                  {"state": "x_found", "kind": "number", "register": "symbolic", "requires": ["Kb_found"], "explicit": True},
                  {"state": "pOH_found", "kind": "number", "register": "symbolic", "requires": ["x_found"], "explicit": True},
                  {"state": "pH_found", "kind": "number", "register": "macro", "requires": ["pOH_found"], "explicit": True, "pin": True}]
        prev = "pH_found"
    elif region == "after":
        c_oh = (nb - na) / Vt; pOH = pH_of(c_oh); pH = 14 - pOH
        expected += [E("excess_conc", "[OH-] from the excess base over the total volume", c_oh, "M", role="intermediate", require_unit=True, after="moles_found"),
                     E("pOH_found", "pOH", pOH, "", role="intermediate", require_unit=False, after="excess_conc"), E("pH_found", "pH", pH, "", role="key", require_unit=False, after="pOH_found")]
        traps += [trap("VOLUME_NOT_TOTALED", (nb - na) / (P["va"] / 1000), "excess_conc", "M"), trap("POH_TYPED_AS_PH", pOH, "pH_found"), trap("MOLES_FROM_ONE_SOLUTION", nb / Vt, "excess_conc", "M")]
        board += [{"state": "excess_conc", "kind": "number", "register": "symbolic", "requires": [prev], "explicit": True, "pin": True},
                  {"state": "pOH_found", "kind": "number", "register": "symbolic", "requires": ["excess_conc"], "explicit": True},
                  {"state": "pH_found", "kind": "number", "register": "macro", "requires": ["pOH_found"], "explicit": True, "pin": True}]
        prev = "pH_found"
    elif not weak and region == "before":
        c_h = (na - nb) / Vt; pH = pH_of(c_h)
        expected += [E("excess_conc", "[H3O+] from the excess acid over the total volume", c_h, "M", role="intermediate", require_unit=True, after="moles_found"), E("pH_found", "pH", pH, "", role="key", require_unit=False, after="excess_conc")]
        traps += [trap("VOLUME_NOT_TOTALED", (na - nb) / (P["va"] / 1000), "excess_conc", "M"), trap("MOLES_FROM_ONE_SOLUTION", na / Vt, "excess_conc", "M")]
        board += [{"state": "excess_conc", "kind": "number", "register": "symbolic", "requires": [prev], "explicit": True, "pin": True}, {"state": "pH_found", "kind": "number", "register": "macro", "requires": ["excess_conc"], "explicit": True, "pin": True}]
        prev = "pH_found"
    elif not weak and region == "at":
        pH = 7.0
        expected += [E("pH_found", "pH", pH, "", role="key", require_unit=False, after="moles_found")]
        board += [{"state": "pH_found", "kind": "number", "register": "macro", "requires": [prev], "explicit": True, "pin": True}]; prev = "pH_found"
    else:
        raise RuntimeError(f"{ID}: {fid}: region {region} for a {pair} pair is not built")
    traps = keep_clear(traps, expected)
    board += [{"state": "side_of_7", "kind": "text", "register": "inference", "requires": [prev]}]
    tail(board, "side_of_7")
    words = dict(P["rx"]["words"]) if weak else {"acid": "hydrochloric acid", "formula": "HCl", "conjugate": "chloride ion"}
    return {"kind": P["kind"], "fixed_id": fid, "version": P["version"], "status": P["status"], "text": P["text"],
            "context": {"family": P["family"], "region": region, "pH": round_sig(pH, 4), "n_acid": round_sig(na, 5), "n_base": round_sig(nb, 5), "V_total_L": round_sig(Vt, 5)},
            "givens": {"c_acid": {"value": P["ca"], "unit": "M"}, "V_acid": {"value": P["va"], "unit": "mL"}, "c_base": {"value": P["cb"], "unit": "M"}, **({"V_base": {"value": P["vb"], "unit": "mL"}} if P["vb"] else {}), **({"Ka": {"value": P["rx"]["K"], "unit": ""}} if weak else {})},
            "board": board, "targets": expected, "traps": traps, "table": table, "words": words, "eq_checks": eqc, "reveal_with_problem": None, "sim": None,
            "sim_params": {"pair": pair, "species": (P["rx"]["id"] if weak else "HCl"), "ca": P["ca"], "va": P["va"], "cb": P["cb"], "vb": P["vb"]}}
def render_text(*a): raise NotImplementedError
