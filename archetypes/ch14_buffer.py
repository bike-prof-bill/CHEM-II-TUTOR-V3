"""Chapter 14, archetype 3 of 4: Buffers. Fixed problems; placeholders DRAFT; ships nothing until a scenario is approved.
Step map: account -> relation (Henderson-Hasselbalch) -> ratio_found -> pH_found -> perturb_1 (a little strong base: pH rises |
falls | unchanged) -> why -> pH_after_1 (the number: the instructor, 15 Oct, "small but greater than 0.75 mL") -> perturb_2 (a little
strong acid) -> why -> pH_after_2 -> meaning -> reflection. The addition: a volume (> 0.75 mL) of a strong acid or base at a given
concentration, into a buffer of known volume; the added moles convert one partner into the other and the ratio moves.
"""
import math
from engine import round_sig
from _acidbase import *

ID = "ch14_buffer"
TITLE = "Buffers: why the pH barely moves, and by how much"
RELATION_TEXT = "pH = pKa + log([A-]/[HA]); an added strong acid or base converts one partner into the other"
KINDS = ["buffer"]
EQUATION_PICKS = picks({"eq_hh": KINDS})
CONSTANTS = [{"label": "Kw", "symbol": "Kw", "value": KW, "unit": ""}]
EQUATION_SYMBOLS = {"pH": ["pH"], "pKa": ["pKa", "pK_a"]}; EQUATION_CONSTANTS = {"Kw": KW}
MECHANISM_WORDS = MECHANISM_WORDS
TRAP_NOTES = TRAP_NOTES_COMMON
MIN_ADD_ML = 0.75

def _p(fid, opener, key, ca, cb, V, add, version, family, text):
    return {"id": fid, "opener": opener, "kind": "buffer", "rx": acid(key), "ca": ca, "cb": cb, "V": V, "add_base": add, "add_acid": add, "version": version, "family": family, "text": text, "sf": 2,
            "status": "approved (SCENARIO_CLAUDE's sheet; instructor, 17 Oct 2026)"}
FIXED = [   # 24 problems: The Stubborn Beaker (worked; acetate, formate, hypochlorite, nitrite), The Sprint (exam, the blood buffer), The Eye Drops (phosphate), Half a Buffer (ammonia/ammonium)
  _p('B1', 'The Stubborn Beaker', 'acetic', 0.1, 0.1, 1.0, (15.0, 1.0), 'equal', 'core: equal amounts (worked)', r"""A buffer is 1.00 L of 0.10 M acetic acid, \(\mathrm{CH_3COOH}\), and 0.10 M sodium acetate, \(\mathrm{NaCH_3COO}\), at 25 °C. \(K_a = 1.8 \times 10^{-5}\). Find the ratio of base to acid, and the pH. Then 15.0 mL of 1.0 M NaOH is added. In a fresh batch, 15.0 mL of 1.0 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('B2', 'The Stubborn Beaker', 'acetic', 0.1, 0.3, 1.0, (15.0, 1.0), 'unequal', 'variant: unequal amounts, base three times the acid (worked offer)', r"""A buffer is 1.00 L of 0.10 M acetic acid, \(\mathrm{CH_3COOH}\), and 0.30 M sodium acetate, \(\mathrm{NaCH_3COO}\), at 25 °C. \(K_a = 1.8 \times 10^{-5}\). Find the ratio of base to acid, and the pH. Then 15.0 mL of 1.0 M NaOH is added. In a fresh batch, 15.0 mL of 1.0 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('B3', 'The Stubborn Beaker', 'formic', 0.25, 0.15, 0.5, (10.0, 1.0), '', 'acid in excess', r"""A buffer is 0.500 L of 0.25 M formic acid, \(\mathrm{HCOOH}\), and 0.15 M sodium formate, \(\mathrm{NaHCOO}\), at 25 °C. \(K_a = 1.8 \times 10^{-4}\). Find the ratio of base to acid, and the pH. Then 10.0 mL of 1.0 M NaOH is added. In a fresh batch, 10.0 mL of 1.0 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('B4', 'The Stubborn Beaker', 'hypochlorous', 0.05, 0.05, 0.25, (1.5, 1.0), '', 'equal amounts, a high pKa', r"""A buffer is 0.250 L of 0.05 M hypochlorous acid, \(\mathrm{HClO}\), and 0.05 M sodium hypochlorite, \(\mathrm{NaClO}\), at 25 °C. \(K_a = 2.9 \times 10^{-8}\). Find the ratio of base to acid, and the pH. Then 1.5 mL of 1.0 M NaOH is added. In a fresh batch, 1.5 mL of 1.0 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('B5', 'The Stubborn Beaker', 'nitrous', 0.15, 0.3, 1.0, (20.0, 1.0), '', 'base in excess', r"""A buffer is 1.00 L of 0.15 M nitrous acid, \(\mathrm{HNO_2}\), and 0.30 M sodium nitrite, \(\mathrm{NaNO_2}\), at 25 °C. \(K_a = 4.6 \times 10^{-4}\). Find the ratio of base to acid, and the pH. Then 20.0 mL of 1.0 M NaOH is added. In a fresh batch, 20.0 mL of 1.0 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('B6', 'The Stubborn Beaker', 'acetic', 0.4, 0.1, 0.5, (10.0, 1.0), '', 'acid four times the base', r"""A buffer is 0.500 L of 0.40 M acetic acid, \(\mathrm{CH_3COOH}\), and 0.10 M sodium acetate, \(\mathrm{NaCH_3COO}\), at 25 °C. \(K_a = 1.8 \times 10^{-5}\). Find the ratio of base to acid, and the pH. Then 10.0 mL of 1.0 M NaOH is added. In a fresh batch, 10.0 mL of 1.0 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('S1', 'The Sprint', 'carbonic_blood', 0.0012, 0.024, 1.0, (2.0, 0.1), '', 'blood buffer, both additions (exam: every version the same concepts)', r"""A lab models blood plasma at body temperature as 1.00 L of 0.024 M sodium bicarbonate, \(\mathrm{NaHCO_3}\), and 0.0012 M carbonic acid, \(\mathrm{H_2CO_3}\). At body temperature, \(\mathrm{p}K_a = 6.1\). Find the ratio of base to acid, and the pH. Then 2 mL of 0.10 M NaOH is added. In a fresh batch, 2 mL of 0.10 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('S2', 'The Sprint', 'carbonic_blood', 0.0013, 0.025, 0.5, (1.2, 0.1), '', 'blood buffer, both additions (exam: every version the same concepts)', r"""A lab models blood plasma at body temperature as 0.500 L of 0.025 M sodium bicarbonate, \(\mathrm{NaHCO_3}\), and 0.0013 M carbonic acid, \(\mathrm{H_2CO_3}\). At body temperature, \(\mathrm{p}K_a = 6.1\). Find the ratio of base to acid, and the pH. Then 1.2 mL of 0.10 M NaOH is added. In a fresh batch, 1.2 mL of 0.10 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('S3', 'The Sprint', 'carbonic_blood', 0.0015, 0.024, 1.0, (2.5, 0.1), '', 'blood buffer, both additions (exam: every version the same concepts)', r"""A lab models blood plasma at body temperature as 1.00 L of 0.024 M sodium bicarbonate, \(\mathrm{NaHCO_3}\), and 0.0015 M carbonic acid, \(\mathrm{H_2CO_3}\). At body temperature, \(\mathrm{p}K_a = 6.1\). Find the ratio of base to acid, and the pH. Then 2.5 mL of 0.10 M NaOH is added. In a fresh batch, 2.5 mL of 0.10 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('S4', 'The Sprint', 'carbonic_blood', 0.001, 0.022, 1.0, (2.0, 0.1), '', 'blood buffer, both additions (exam: every version the same concepts)', r"""A lab models blood plasma at body temperature as 1.00 L of 0.022 M sodium bicarbonate, \(\mathrm{NaHCO_3}\), and 0.0010 M carbonic acid, \(\mathrm{H_2CO_3}\). At body temperature, \(\mathrm{p}K_a = 6.1\). Find the ratio of base to acid, and the pH. Then 2 mL of 0.10 M NaOH is added. In a fresh batch, 2 mL of 0.10 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('S5', 'The Sprint', 'carbonic_blood', 0.0012, 0.026, 2.0, (4.0, 0.1), '', 'blood buffer, both additions (exam: every version the same concepts)', r"""A lab models blood plasma at body temperature as 2.00 L of 0.026 M sodium bicarbonate, \(\mathrm{NaHCO_3}\), and 0.0012 M carbonic acid, \(\mathrm{H_2CO_3}\). At body temperature, \(\mathrm{p}K_a = 6.1\). Find the ratio of base to acid, and the pH. Then 4 mL of 0.10 M NaOH is added. In a fresh batch, 4 mL of 0.10 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('S6', 'The Sprint', 'carbonic_blood', 0.0014, 0.025, 0.25, (0.8, 0.1), '', 'blood buffer, both additions (exam: every version the same concepts)', r"""A lab models blood plasma at body temperature as 0.250 L of 0.025 M sodium bicarbonate, \(\mathrm{NaHCO_3}\), and 0.0014 M carbonic acid, \(\mathrm{H_2CO_3}\). At body temperature, \(\mathrm{p}K_a = 6.1\). Find the ratio of base to acid, and the pH. Then 0.8 mL of 0.10 M NaOH is added. In a fresh batch, 0.8 mL of 0.10 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('P1', 'The Eye Drops', 'dihydrogen_phosphate', 0.1, 0.1, 1.0, (15.0, 1.0), '', 'equal amounts', r"""A buffer is 1.00 L of 0.100 M sodium dihydrogen phosphate, \(\mathrm{NaH_2PO_4}\), and 0.100 M sodium hydrogen phosphate, \(\mathrm{Na_2HPO_4}\), at 25 °C. For \(\mathrm{H_2PO_4^-}\), \(K_a = 6.2 \times 10^{-8}\). Find the ratio of base to acid, and the pH. Then 15 mL of 1 M NaOH is added. In a fresh batch, 15 mL of 1 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('P2', 'The Eye Drops', 'dihydrogen_phosphate', 0.04, 0.06, 0.5, (3.0, 1.0), '', "ratio 1.5 (the lens solution's pH)", r"""A buffer is 0.500 L of 0.040 M sodium dihydrogen phosphate, \(\mathrm{NaH_2PO_4}\), and 0.060 M sodium hydrogen phosphate, \(\mathrm{Na_2HPO_4}\), at 25 °C. For \(\mathrm{H_2PO_4^-}\), \(K_a = 6.2 \times 10^{-8}\). Find the ratio of base to acid, and the pH. Then 3 mL of 1 M NaOH is added. In a fresh batch, 3 mL of 1 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('P3', 'The Eye Drops', 'dihydrogen_phosphate', 0.2, 0.1, 0.25, (5.0, 1.0), '', 'acid in excess', r"""A buffer is 0.250 L of 0.200 M sodium dihydrogen phosphate, \(\mathrm{NaH_2PO_4}\), and 0.100 M sodium hydrogen phosphate, \(\mathrm{Na_2HPO_4}\), at 25 °C. For \(\mathrm{H_2PO_4^-}\), \(K_a = 6.2 \times 10^{-8}\). Find the ratio of base to acid, and the pH. Then 5 mL of 1 M NaOH is added. In a fresh batch, 5 mL of 1 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('P4', 'The Eye Drops', 'dihydrogen_phosphate', 0.05, 0.15, 1.0, (10.0, 1.0), '', 'base in excess', r"""A buffer is 1.00 L of 0.050 M sodium dihydrogen phosphate, \(\mathrm{NaH_2PO_4}\), and 0.150 M sodium hydrogen phosphate, \(\mathrm{Na_2HPO_4}\), at 25 °C. For \(\mathrm{H_2PO_4^-}\), \(K_a = 6.2 \times 10^{-8}\). Find the ratio of base to acid, and the pH. Then 10 mL of 1 M NaOH is added. In a fresh batch, 10 mL of 1 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('P5', 'The Eye Drops', 'dihydrogen_phosphate', 0.025, 0.025, 0.1, (2.5, 0.1), '', 'dilute buffer, 0.10 M additions', r"""A buffer is 0.100 L of 0.025 M sodium dihydrogen phosphate, \(\mathrm{NaH_2PO_4}\), and 0.025 M sodium hydrogen phosphate, \(\mathrm{Na_2HPO_4}\), at 25 °C. For \(\mathrm{H_2PO_4^-}\), \(K_a = 6.2 \times 10^{-8}\). Find the ratio of base to acid, and the pH. Then 2.5 mL of 0.1 M NaOH is added. In a fresh batch, 2.5 mL of 0.1 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('P6', 'The Eye Drops', 'dihydrogen_phosphate', 0.08, 0.12, 0.25, (2.0, 1.0), '', 'ratio 1.5, a small volume', r"""A buffer is 0.250 L of 0.080 M sodium dihydrogen phosphate, \(\mathrm{NaH_2PO_4}\), and 0.120 M sodium hydrogen phosphate, \(\mathrm{Na_2HPO_4}\), at 25 °C. For \(\mathrm{H_2PO_4^-}\), \(K_a = 6.2 \times 10^{-8}\). Find the ratio of base to acid, and the pH. Then 2 mL of 1 M NaOH is added. In a fresh batch, 2 mL of 1 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('A1', 'Half a Buffer', 'ammonium', 0.1, 0.1, 1.0, (15.0, 1.0), '', 'equal amounts', r"""A buffer is 1.00 L of 0.10 M ammonia, \(\mathrm{NH_3}\), and 0.10 M ammonium chloride, \(\mathrm{NH_4Cl}\), at 25 °C. For ammonia, \(K_b = 1.8 \times 10^{-5}\). Find the ratio of base to acid, and the pH. Then 15 mL of 1.0 M NaOH is added. In a fresh batch, 15 mL of 1.0 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('A2', 'Half a Buffer', 'ammonium', 0.1, 0.3, 0.5, (8.0, 1.0), '', 'base three times the acid', r"""A buffer is 0.500 L of 0.30 M ammonia, \(\mathrm{NH_3}\), and 0.10 M ammonium chloride, \(\mathrm{NH_4Cl}\), at 25 °C. For ammonia, \(K_b = 1.8 \times 10^{-5}\). Find the ratio of base to acid, and the pH. Then 8 mL of 1.0 M NaOH is added. In a fresh batch, 8 mL of 1.0 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('A3', 'Half a Buffer', 'ammonium', 0.2, 0.1, 0.25, (4.0, 1.0), '', 'acid twice the base', r"""A buffer is 0.250 L of 0.10 M ammonia, \(\mathrm{NH_3}\), and 0.20 M ammonium chloride, \(\mathrm{NH_4Cl}\), at 25 °C. For ammonia, \(K_b = 1.8 \times 10^{-5}\). Find the ratio of base to acid, and the pH. Then 4 mL of 1.0 M NaOH is added. In a fresh batch, 4 mL of 1.0 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('A4', 'Half a Buffer', 'ammonium', 0.05, 0.1, 1.0, (8.0, 1.0), '', 'base twice the acid', r"""A buffer is 1.00 L of 0.10 M ammonia, \(\mathrm{NH_3}\), and 0.05 M ammonium chloride, \(\mathrm{NH_4Cl}\), at 25 °C. For ammonia, \(K_b = 1.8 \times 10^{-5}\). Find the ratio of base to acid, and the pH. Then 8 mL of 1.0 M NaOH is added. In a fresh batch, 8 mL of 1.0 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('A5', 'Half a Buffer', 'ammonium', 0.15, 0.15, 0.1, (1.5, 1.0), '', 'equal amounts, small volume', r"""A buffer is 0.100 L of 0.15 M ammonia, \(\mathrm{NH_3}\), and 0.15 M ammonium chloride, \(\mathrm{NH_4Cl}\), at 25 °C. For ammonia, \(K_b = 1.8 \times 10^{-5}\). Find the ratio of base to acid, and the pH. Then 1.5 mL of 1.0 M NaOH is added. In a fresh batch, 1.5 mL of 1.0 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
  _p('A6', 'Half a Buffer', 'ammonium', 0.25, 0.15, 0.5, (10.0, 1.0), '', 'acid in excess', r"""A buffer is 0.500 L of 0.15 M ammonia, \(\mathrm{NH_3}\), and 0.25 M ammonium chloride, \(\mathrm{NH_4Cl}\), at 25 °C. For ammonia, \(K_b = 1.8 \times 10^{-5}\). Find the ratio of base to acid, and the pH. Then 10 mL of 1.0 M NaOH is added. In a fresh batch, 10 mL of 1.0 M HCl is added. Which way does the pH move each time, and what is the new pH?"""),
]

def _after(K, na, nb, n_add, kind):             # moles after a strong base (converts acid to base) or strong acid (base to acid)
    if kind == "base": na2, nb2 = na - n_add, nb + n_add
    else: na2, nb2 = na + n_add, nb - n_add
    if na2 <= 0 or nb2 <= 0: raise RuntimeError("the addition exhausts a buffer partner: not a small addition")
    return hh_pH(K, nb2 / na2), na2, nb2

def make_fixed(rng, fid):
    P = [f for f in FIXED if f["id"] == fid][0]; rx = P["rx"]; K = rx["K"]; ca, cb, V = P["ca"], P["cb"], P["V"]
    ratio = cb / ca; pKa = -math.log10(K); pH = hh_pH(K, ratio); na, nb = ca * V, cb * V
    expected = [E("ratio_found", "[A-]/[HA]", ratio, "", role="intermediate", require_unit=False, after="relation_chosen"),
                E("pH_found", "pH", pH, "", role="key", require_unit=False, after="ratio_found")]
    traps = [trap("RATIO_INVERTED", hh_pH(K, 1 / ratio), "pH_found"), trap("RATIO_INVERTED", 1 / ratio, "ratio_found") if abs(ratio - 1) > 1e-9 else None,
             trap("PKA_TYPED_AS_PH", pKa, "pH_found") if abs(ratio - 1) > 1e-9 else None, trap("LOG_FORGOTTEN", pKa + ratio, "pH_found")]
    pKb = 14 - pKa if rx["id"] == "ammonium" else None                  # a basic buffer: pKb + log(ratio) offered as the pH (KB_USED_AS_KA, approved 17 Oct)
    if pKb is not None: traps.append(trap("KB_USED_AS_KA", pKb + math.log10(ratio), "pH_found"))
    board = head() + [{"state": "ratio_found", "kind": "number", "register": "symbolic", "requires": ["relation_chosen"], "explicit": True, "pin": True},
                      {"state": "pH_found", "kind": "number", "register": "macro", "requires": ["ratio_found"], "explicit": True, "pin": True}]
    prev = "pH_found"; afters = []
    for n, (kind, add, named) in enumerate((("base", P["add_base"], {"unchanged": "BUFFER_PH_FIXED"}), ("acid", P["add_acid"], {"unchanged": "BUFFER_PH_FIXED"})), start=1):
        vol_ml, conc = add
        if vol_ml <= MIN_ADD_ML: raise RuntimeError(f"{ID}: {fid} adds {vol_ml} mL; the instructor's floor is more than {MIN_ADD_ML} mL")
        n_add = vol_ml / 1000 * conc
        pH2, na2, nb2 = _after(K, na, nb, n_add, kind)
        if abs(pH2 - pH) <= 2 * PH_TOL: raise RuntimeError(f"{ID}: {fid}: the {kind} addition moves the pH by only {abs(pH2 - pH):.3f}; the tutor reads pH to {PH_TOL}, so make the addition larger (it must stay small next to the buffer)")
        expected.append(E(f"pH_after_{n}", f"pH after the {'base' if kind == 'base' else 'acid'}", pH2, "", role="intermediate", require_unit=False, after=f"perturb_{n}_why"))
        # named: the added moles treated as free in the solution (no buffer action), and the direction of change ignored (ratio moved the wrong way)
        V2 = V + vol_ml / 1000
        free = (14 - pH_of(n_add / V2)) if kind == "base" else pH_of(n_add / V2)
        traps += [trap("ADDED_NOT_CONSUMED", free, f"pH_after_{n}"), trap("RATIO_INVERTED", hh_pH(K, na2 / nb2), f"pH_after_{n}")]
        if pKb is not None: traps.append(trap("KB_USED_AS_KA", pKb + math.log10(nb2 / na2), f"pH_after_{n}"))
        board += [direction_item(f"perturb_{n}", f"p{n}", "pH", "rises" if kind == "base" else "falls", named, prev),
                  {"state": f"perturb_{n}_why", "kind": "text", "register": "submicro", "requires": [f"perturb_{n}"]},
                  {"state": f"pH_after_{n}", "kind": "number", "register": "macro", "requires": [f"perturb_{n}_why"], "explicit": True, "pin": True}]
        prev = f"pH_after_{n}"; afters.append({"kind": kind, "mL": vol_ml, "M": conc, "pH_after": round_sig(pH2, 4)})
    traps = keep_clear(traps, expected)
    tail(board, prev)
    return {"kind": "buffer", "fixed_id": fid, "version": P["version"], "status": P["status"], "text": P["text"],
            "context": {"family": P["family"], "pH": round_sig(pH, 4), "ratio": round_sig(ratio, 4), "additions": afters},
            "givens": {"c_acid": {"value": ca, "unit": "M"}, "c_base": {"value": cb, "unit": "M"}, "V": {"value": V, "unit": "L"}, "Ka": {"value": K, "unit": ""}},
            "board": board, "targets": expected, "traps": traps, "table": None, "words": dict(rx["words"], base=rx["conjugate_name"] if False else rx["words"].get("conjugate", "")), "eq_checks": [], "reveal_with_problem": None, "sim": None,
            "sim_params": {"species": {"carbonic_blood": "blood", "dihydrogen_phosphate": "phosphate", "ammonium": "ammonium"}.get(rx["id"], rx["id"]), "ca": ca, "cb": cb, "V": V}}
def render_text(*a): raise NotImplementedError
