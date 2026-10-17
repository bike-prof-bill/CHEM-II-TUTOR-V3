"""Chapter 15, archetype 4 of 4: complex-ion equilibria (the instructor, 17 Oct 2026: build it now). Fixed problems; placeholders
DRAFT; ships nothing until a scenario is approved. The milestones' steps: map the metal ion's binding to its ligands (the account);
let the limiting reactant run to completion (the complex formed, the ligand left); set up the small dissociation table with
Kd = 1/Kf; solve for the free metal ion; a conceptual check on how firmly the ligand holds (how many times smaller the free metal
is than before complexing).
Step map: account -> relation (the Kf expression) -> complete_found (after complete formation: [complex], [ligand left]; both,
over the total volume) -> Kd_found (1/Kf) -> table (dissociation: complex | metal | ligand) -> expression_set -> method (small x)
-> x_found (the free metal ion) -> ratio_found (how many times smaller than the metal's concentration after mixing) -> perturb_1
(more ligand: free metal falls) -> why -> meaning -> reflection.
"""
import math
from engine import round_sig
from _solubility import *
from _solubility import _D

ID = "ch15_complex"
TITLE = "Complex ions: how little free metal is left when a ligand binds it"
RELATION_TEXT = "Kf = [complex] / ([metal][ligand]^n) for formation; the dissociation runs on Kd = 1/Kf; with excess ligand the free metal ion is tiny"
KINDS = ["free_metal"]
EQ_LOCAL = {"kf": {"id": "eq_kf", "text": r"\( K_f = \dfrac{[\mathrm{ML_n}]}{[\mathrm{M}][\mathrm{L}]^{n}} \)"}, "kd": {"id": "eq_kd", "text": r"\( K_d = \dfrac{[\mathrm{M}][\mathrm{L}]^{n}}{[\mathrm{ML_n}]} = \dfrac{1}{K_f} \)"}}
EQUATION_PICKS = [dict(EQ_LOCAL["kf"], fits=KINDS), dict(EQ_LOCAL["kd"], fits=KINDS)] + picks({})
CONSTANTS = []
EQUATION_SYMBOLS = {"x": ["x", "s"], "K": ["Kd", "K_d", "Kf", "K_f", "K"]}; EQUATION_CONSTANTS = {}
MECHANISM_WORDS = MECHANISM_WORDS + ["ligand", "bind", "bond", "coordinat", "lone pair", "donat", "accept", "hold", "let go", "release"]
TRAP_NOTES = dict(TRAP_NOTES_COMMON, **{
  "KF_FOR_KD":                 {"note": "Their free metal comes from Kf used where Kd was needed (or the reciprocal was not taken).", "ask": "Which way is the reaction in your table running, and which constant belongs to that direction?"},
  "LIGAND_LEFT_IGNORED":       {"note": "Their free metal ignores the ligand left over after the complex formed.", "ask": "After the complex formed, how much ligand was still free in the solution?"},
  "LIGAND_EXPONENT_DROPPED":   {"note": "Their free metal uses the ligand's concentration to the first power though n ligands bind each metal ion.", "ask": "How many ligand molecules does each complex ion hold, and where does that number sit in the expression?"},
  "COMPLETION_NOT_ASSUMED":    {"note": "Their table starts from the metal and ligand before any complex formed, so x is not small.", "ask": "With Kf this large, what has happened to nearly all the metal ion before the table begins?"},
  "FREE_METAL_RISES_WITH_LIGAND": {"note": "They predicted more free metal when more ligand was added.", "ask": "The added ligand sits on which side of the dissociation, and which way does that push it?"},
})

def complex_(formula):
    c = dict(_D["complexes"][formula]); c["formula"] = formula
    c["words"] = {"complex": c["name"], "formula": c["formula_display"], "metal": c["metal_name"], "ligand": c["ligand_name"], "metal_ion": c["metal_display"], "ligand_formula": c["ligand_display"]}; return c
def _p(fid, formula, c_metal, v_metal, c_lig, v_lig, text, family):
    return {"id": fid, "kind": "free_metal", "cx": complex_(formula), "c_metal": c_metal, "v_metal": v_metal, "c_lig": c_lig, "v_lig": v_lig, "text": text, "family": family, "version": "", "sf": 2, "status": DRAFT}
FIXED = [
  _p("M1", "Ag(NH3)2+", 0.010, 50.0, 1.00, 50.0, "50.0 mL of 0.010 M silver nitrate is mixed with 50.0 mL of 1.00 M ammonia at 25 °C. Kf for Ag(NH3)2+ is 1.7 × 10^7. Find the concentrations after the complex forms, set up the dissociation table, and find the free silver ion concentration.", "silver-ammine, large excess of ligand"),
  _p("M2", "Cu(NH3)4^2+", 0.020, 25.0, 2.00, 75.0, "25.0 mL of 0.020 M copper(II) sulfate is mixed with 75.0 mL of 2.00 M ammonia at 25 °C. Kf for Cu(NH3)4^2+ is 1.1 × 10^13. Find the concentrations after the complex forms, set up the dissociation table, and find the free copper(II) ion concentration.", "copper-ammine, four ligands, unequal volumes"),
  _p("M3", "Fe(SCN)^2+", 0.0010, 50.0, 0.0030, 50.0, "50.0 mL of 0.0010 M iron(III) nitrate is mixed with 50.0 mL of 0.0030 M potassium thiocyanate at 25 °C. Kf for Fe(SCN)^2+ is 8.9 × 10^2. Find the concentrations after the complex forms, set up the dissociation table, and find the free iron(III) ion concentration.", "one ligand, small Kf: x is not small"),
]

def free_metal(cx, C, L, exact=True):
    """Dissociation ML_n -> M + n L from [complex] = C with free ligand L: Kd = x (L + n x)^n / (C - x); bisection, and the small-x estimate."""
    n = cx["n_ligand"]; Kd = 1.0 / cx["Kf"]
    small = Kd * C / (L ** n)
    lo, hi = 0.0, C * 0.999999
    for _ in range(300):
        m = 0.5 * (lo + hi)
        if m * (L + n * m) ** n / (C - m) < Kd: lo = m
        else: hi = m
    x = 0.5 * (lo + hi)
    return x, small, (small / C < 0.05 and n * small / L < 0.05)

def make_fixed(rng, fid):
    P = [f for f in FIXED if f["id"] == fid][0]; cx = P["cx"]; n = cx["n_ligand"]; Kd = 1.0 / cx["Kf"]
    cm, cl, vt = mixed(P["c_metal"], P["v_metal"], P["c_lig"], P["v_lig"])
    if cl < n * cm: raise RuntimeError(f"{ID}: {fid}: the ligand is limiting; this archetype assumes the ligand in excess")
    C = cm; L = cl - n * cm                                  # complete formation: all the metal becomes complex; the ligand left over
    x, x_small, small_ok = free_metal(cx, C, L); ratio = cm / x
    expected = [E("complete_found", f"[{cx['formula']}] after complete formation", C, "M", role="intermediate", require_unit=True),
                E("complete_found", f"[{cx['ligand']}] left over", L, "M", role="intermediate", require_unit=True, abs_tol=round_sig(max(window(L), 1.1 * n * cm if n * cm / cl < 0.05 else 0), 3)),   # with a large excess, the ligand before and after formation agree within the amount consumed
                E("Kd_found", "Kd = 1/Kf", Kd, "", role="intermediate", require_unit=False, after="complete_found"),
                E("x_found", f"free [{cx['metal']}]", x, "M", role="key", require_unit=True),
                E("ratio_found", "how many times smaller than before complexing", ratio, "", role="intermediate", require_unit=False, after="x_found")]
    traps = [trap("DILUTION_IGNORED", P["c_metal"], "complete_found", "M"), trap("DILUTION_IGNORED", P["c_lig"], "complete_found", "M"),
             trap("LIGAND_LEFT_IGNORED", cl, "complete_found", "M"),
             trap("VOLUME_NOT_TOTALED", P["c_metal"] * P["v_metal"] / P["v_lig"], "complete_found", "M") if P["v_metal"] != P["v_lig"] else None,
             trap("KF_FOR_KD", cx["Kf"] * C / (L ** n), "x_found", "M") if cx["Kf"] * C / (L ** n) < 1e3 else None,
             trap("LIGAND_EXPONENT_DROPPED", Kd * C / L, "x_found", "M") if n > 1 else None,
             trap("LIGAND_LEFT_IGNORED", Kd * C / (cl ** n), "x_found", "M"),
             trap("COMPLETION_NOT_ASSUMED", cm, "x_found", "M")]
    if not small_ok: traps.append(trap("SMALL_S_WHEN_IT_FAILS", x_small, "x_found", "M"))
    traps = keep_clear(traps, expected)
    table = {"species": [cx["formula"], cx["metal"], cx["ligand"]], "rows": {"I": [g(C), "0", g(L)], "C": ["-x", "+x", f"+{n if n > 1 else ''}x"], "E": [f"{g(C)} - x", "x", f"{g(L)} + {n if n > 1 else ''}x"]},
             "named": ([{"id": "COEFFICIENT_DROPPED_IN_TABLE", "row": "C", "cells": ["-x", "+x", "+x"]}] if n > 1 else []) + [{"id": "COMPLETION_NOT_ASSUMED", "row": "I", "cells": [g(0), g(cm), g(cl)]}], "zero_species": [1]}
    def form(exp_ok, mult_ok):
        def f(xx): return xx * (L + (n if mult_ok else 1) * xx) ** (n if exp_ok else 1) / (C - xx)
        return f
    def states(f): return [{"x": round_sig(xx, 9), "K": round_sig(f(xx), 9)} for xx in (0.5 * x, 1.0 * x, 1.5 * x)]
    eqc = {"state": "expression_set", "unknown": "K", "true": states(form(True, True)), "alt": [], "bent": ({"COEFF_NOT_EXPONENT": states(form(False, True)), "EXPONENT_NOT_IN_TABLE": states(form(True, False))} if n > 1 else {}),
           "literal_for": {"K": Kd}, "park_text": f"{Kd:.3g} = x · ({g(L)} + {n if n > 1 else ''}x){'^' + str(n) if n > 1 else ''} / ({g(C)} - x)"}
    board = head() + [{"state": "complete_found", "kind": "number", "register": "symbolic", "requires": ["relation_chosen"], "rule": "all", "explicit": True, "pin": True},
                      {"state": "Kd_found", "kind": "number", "register": "symbolic", "requires": ["complete_found"], "explicit": True},
                      {"state": "table", "kind": "table", "register": "symbolic", "requires": ["Kd_found"], "pin": True, "explicit": True},
                      {"state": "expression_set", "kind": "equation", "register": "symbolic", "requires": ["table"], "explicit": True, "pin": True},
                      {"state": "method", "kind": "pick", "register": "symbolic", "requires": ["expression_set"],
                       "options": [{"id": "method:smallx", "text": "x is small next to the complex and the ligand left: drop it from both, then check."}, {"id": "method:exact", "text": "Keep x in every term and solve exactly."}, {"id": "method:formation", "text": "Start from the metal and ligand before any complex formed and solve the formation table."}],
                       "right": ["method:smallx"] if small_ok else ["method:exact"]},
                      {"state": "x_found", "kind": "number", "register": "symbolic", "requires": ["method"], "explicit": True, "pin": True},
                      {"state": "ratio_found", "kind": "number", "register": "macro", "requires": ["x_found"], "explicit": True, "pin": True},
                      {"state": "perturb_1", "kind": "direction", "register": "macro", "requires": ["ratio_found"], "options": opts("p1", [("rises", "rises: more free metal ion"), ("falls", "falls: less free metal ion"), ("unchanged", "unchanged: the same free metal ion")], {"rises": "FREE_METAL_RISES_WITH_LIGAND"}), "right": ["p1:falls"], "explicit": True, "pin": True},
                      {"state": "perturb_1_why", "kind": "text", "register": "submicro", "requires": ["perturb_1"]}]
    tail(board, "perturb_1_why")
    return {"kind": "free_metal", "fixed_id": fid, "version": "", "status": P["status"], "context": {"family": P["family"], "x": round_sig(x, 5), "small_ok": small_ok, "C": round_sig(C, 5), "L": round_sig(L, 5)}, "text": P["text"],
            "givens": {"c_metal": {"value": P["c_metal"], "unit": "M"}, "V_metal": {"value": P["v_metal"], "unit": "mL"}, "c_ligand": {"value": P["c_lig"], "unit": "M"}, "V_ligand": {"value": P["v_lig"], "unit": "mL"}, "Kf": {"value": cx["Kf"], "unit": ""}},
            "board": board, "targets": expected, "traps": traps, "table": table, "words": dict(cx["words"]), "eq_checks": [eqc], "reveal_with_problem": None, "sim": None,
            "sim_params": {"complex": cx["formula"], "C": round_sig(C, 5), "L": round_sig(L, 5), "Kf": cx["Kf"]}}
def render_text(*a): raise NotImplementedError
