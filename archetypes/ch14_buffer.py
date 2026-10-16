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
ACETIC = acid("acetic")
MIN_ADD_ML = 0.75

def _p(fid, rx, ca, cb, V, add_base, add_acid, text, family):
    return {"id": fid, "kind": "buffer", "rx": rx, "ca": ca, "cb": cb, "V": V, "add_base": add_base, "add_acid": add_acid, "text": text, "family": family, "version": "", "sf": 2, "status": DRAFT}
FIXED = [  # add_base / add_acid: (volume in mL, concentration in M) of NaOH / HCl added to V litres of buffer
  _p("F1", ACETIC, 0.10, 0.10, 1.00, (10.0, 1.0), (10.0, 1.0),
     "A buffer is 1.00 L of 0.10 M acetic acid and 0.10 M sodium acetate at 25 °C (Ka = 1.8 × 10^-5). Find the pH. A technician then adds 10.0 mL of 1.0 M NaOH; later, 10.0 mL of 1.0 M HCl to a fresh litre. What happens to the pH each time, and what is the new pH?", "equal amounts; 0.010 mol added each way"),
  _p("F2", ACETIC, 0.20, 0.50, 0.500, (20.0, 1.0), (20.0, 1.0),
     "A buffer is 500 mL of 0.20 M acetic acid and 0.50 M sodium acetate at 25 °C (Ka = 1.8 × 10^-5). Find the ratio of base to acid and the pH. Then 20.0 mL of 1.0 M NaOH is added; to a fresh batch, 20.0 mL of 1.0 M HCl. What happens to the pH each time, and what is the new pH?", "unequal amounts; 0.020 mol added each way"),
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
        board += [direction_item(f"perturb_{n}", f"p{n}", "pH", "rises" if kind == "base" else "falls", named, prev),
                  {"state": f"perturb_{n}_why", "kind": "text", "register": "submicro", "requires": [f"perturb_{n}"]},
                  {"state": f"pH_after_{n}", "kind": "number", "register": "macro", "requires": [f"perturb_{n}_why"], "explicit": True, "pin": True}]
        prev = f"pH_after_{n}"; afters.append({"kind": kind, "mL": vol_ml, "M": conc, "pH_after": round_sig(pH2, 4)})
    traps = keep_clear(traps, expected)
    tail(board, prev)
    return {"kind": "buffer", "fixed_id": fid, "version": "", "status": P["status"], "text": P["text"],
            "context": {"family": P["family"], "pH": round_sig(pH, 4), "ratio": round_sig(ratio, 4), "additions": afters},
            "givens": {"c_acid": {"value": ca, "unit": "M"}, "c_base": {"value": cb, "unit": "M"}, "V": {"value": V, "unit": "L"}, "Ka": {"value": K, "unit": ""}},
            "board": board, "targets": expected, "traps": traps, "table": None, "words": dict(rx["words"]), "eq_checks": [], "reveal_with_problem": None, "sim": None,
            "sim_params": {"species": rx["id"], "ca": ca, "cb": cb, "V": V}}
def render_text(*a): raise NotImplementedError
