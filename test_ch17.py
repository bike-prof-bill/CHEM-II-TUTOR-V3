"""Chapter 17, five sheet-driven archetypes. Every sheet value, trap and pick on the board; then independent arithmetic: every balanced
equation balances atom by atom and in charge with the lowest whole numbers; ΔG° = −nFE° and log K = nE°/0.0592 from the sheet's own n
and E°; Nernst E from E°, n and Q; electrolysis charge = It from the sentence, moles of electrons = Q/F, and the metal's molar mass and
electrons per ion consistent; a cell's verdict follows the sign of E°."""
import sys, json, math, re
from fractions import Fraction
from functools import reduce
sys.path.insert(0, "archetypes"); import engine
import ch17_balancing as BA, ch17_cell as CE, ch17_E_G_K as EG, ch17_nernst as NE, ch17_electrolysis as EL
fails = 0
def check(c, m):
    global fails
    if not c: fails += 1; print("  FAIL:", m)
near = lambda a, b, r=0.01: abs(a - b) <= r * max(abs(b), 1e-30) + 1e-12
F = 96485.0
SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789"); SUP = {"⁰": 0, "¹": 1, "²": 2, "³": 3, "⁴": 4, "⁵": 5, "⁶": 6, "⁷": 7, "⁸": 8, "⁹": 9}
def species(s):
    """'Cr₂O₇²⁻(aq)' -> ({'Cr': 2, 'O': 7}, -2)"""
    s = re.sub(r"\((s|l|g|aq)\)$", "", s.strip())
    charge = 0; m = re.search(r"([⁰¹²³⁴⁵⁶⁷⁸⁹]*)([⁺⁻])$", s)
    if m:
        mag = int("".join(str(SUP[c]) for c in m.group(1)) or 1); charge = mag if m.group(2) == "⁺" else -mag; s = s[:m.start()]
    s = s.translate(SUB)
    def parse(t, i=0):
        counts = {}
        while i < len(t):
            if t[i] == "(":
                inner, i = parse(t, i + 1); mm = re.match(r"\d+", t[i:]); k = int(mm.group(0)) if mm else 1; i += len(mm.group(0)) if mm else 0
                for e, n in inner.items(): counts[e] = counts.get(e, 0) + n * k
            elif t[i] == ")": return counts, i + 1
            else:
                mm = re.match(r"([A-Z][a-z]?)(\d*)", t[i:]); e = mm.group(1); n = int(mm.group(2) or 1); counts[e] = counts.get(e, 0) + n; i += len(mm.group(0))
        return counts, i
    return parse(s)[0], charge
def shipped(A):
    m = engine.read_moves(f"content_{A.ID}_moves.csv"); e = engine.read_errors(f"content_{A.ID}_errors.csv")
    out = engine.build(A, 1, 1, engine.read_openers(f"content_{A.ID}_openers.csv"), m, e); return out, {v["fixed_id"]: v for v in out["variants"]}
def ex(v, st): return [e_["value"] for e_ in v["expected"] if e_["state"] == st]
MOLAR = {"Ag": 107.87, "Cu": 63.55, "Zn": 65.38, "Cr": 52.00, "Ni": 58.69, "Al": 26.98, "Au": 196.97, "Sn": 118.71, "Pb": 207.2, "Fe": 55.85, "Co": 58.93, "Cd": 112.41, "Mg": 24.31, "Na": 22.99, "Mn": 54.94, "Pt": 195.08, "Rh": 102.91}
done = 0
for A in (BA, CE, EG, NE, EL):
    out, V = shipped(A)
    check(len(V) == 24 and len(out["openers"]) == 4 and all(not v["status"].startswith("DRAFT") for v in V.values()), f"{A.ID}: 24 problems under 4 scenarios ship, none DRAFT")
    for P in A.PROBLEMS:
        v = V[P["id"]]
        for e_ in P["expected"]:
            if e_["state"] == "coeffs_found": continue
            check(any(near(x, e_["value"], 1e-6) for x in ex(v, e_["state"])), f"{P['id']}: {e_['state']} = {e_['value']}")
        for st, right in P["picks"].items():
            b = [x for x in v["board"] if x["id"] == st]; check(b and b[0]["right"] == [f"{st}:{right}"] and any(o["id"] == f"{st}:{right}" for o in b[0]["options"]), f"{P['id']}: pick {st} = {right}")
        have = {(x["id"], x["state"]) for x in v["traps"]}
        for tr in P["traps"]:
            if (tr["id"], tr["state"]) not in have: check(any(abs(tr["value"] - x) <= 3 * max(0.02 * abs(x), 0.01, 1e-9) for x in ex(v, tr["state"])), f"{P['id']}: trap {tr['id']} at {tr['state']} missing and not within clearance of the right value")
        if A is BA:
            cf = P["coeffs"]; b = [x for x in v["board"] if x["id"] == "coeffs_found"][0]
            check(b["kind"] == "coefficients" and b["right"] == cf["right"] and b["species"] == cf["species"], f"{P['id']}: coefficient row on the board")
            tot = {}; q = 0
            for i, (sp, c) in enumerate(zip(cf["species"], cf["right"])):
                sign = 1 if i < cf["arrow_after"] else -1; at, ch = species(sp)
                for el, n in at.items(): tot[el] = tot.get(el, 0) + sign * c * n
                q += sign * c * ch
            check(all(n == 0 for n in tot.values()) and q == 0, f"{P['id']}: balances in atoms {dict((k, n) for k, n in tot.items() if n)} and charge {q}")
            check(reduce(math.gcd, cf["right"]) == 1, f"{P['id']}: lowest whole numbers")
            n_ = ex(v, "n_found")[0]; check(n_ % ex(v, "e_ox_found")[0] == 0 and n_ % ex(v, "e_red_found")[0] == 0, f"{P['id']}: n is a common multiple of the two half-reactions' electrons"); done += 1
        if A is EG:
            n_, E_ = ex(v, "n_found")[0], ex(v, "Ecell_found")[0]
            check(near(ex(v, "dG_found")[0], -n_ * F * E_ / 1000, 0.01), f"{P['id']}: ΔG° = −nFE°")
            check(abs(math.log10(ex(v, "K_found")[0]) - n_ * E_ / 0.0592) < 0.05, f"{P['id']}: log K = nE°/0.0592")
            check(P["picks"]["favored"] == ("products" if E_ > 0 else "reactants"), f"{P['id']}: favored follows the sign of E°"); done += 3
        if A is NE:
            E0, n_, Q, E = ex(v, "Ecell0_found")[0], ex(v, "n_found")[0], ex(v, "Q_found")[0], ex(v, "E_found")[0]
            check(abs(E - (E0 - 0.0592 / n_ * math.log10(Q))) <= 0.0015, f"{P['id']}: E = E° − (0.0592/n) log Q ({E} vs {E0 - 0.0592 / n_ * math.log10(Q):.4f})")
            want = "yes" if E > 0.0005 else ("no" if E < -0.0005 else "neither"); check(P["picks"]["verdict"] == want, f"{P['id']}: verdict follows the sign of E"); done += 2
        if A is CE and "verdict" in P["picks"]:
            check(P["picks"]["verdict"] == ("yes" if ex(v, "Ecell_found")[0] > 0 else "no"), f"{P['id']}: verdict follows E°cell"); done += 1
        if A is EL:
            t = P["text"]; mI = re.search(r"current of ([0-9.]+) A", t); mt = re.search(r"for ([0-9.]+) (h|min|s)\b", t); mm = re.search(r"deposits? (?:[0-9.]+ g of )?([A-Z][a-z]?) from", t)
            Qc, ne_ = ex(v, "charge_found")[0], ex(v, "mol_e_found")[0]
            if mI and mt and P["kind"] == "mass":
                secs = float(mt.group(1)) * {"h": 3600, "min": 60, "s": 1}[mt.group(2)]; check(near(Qc, float(mI.group(1)) * secs, 0.005), f"{P['id']}: charge = It"); done += 1
            check(near(ne_, Qc / F, 0.005), f"{P['id']}: moles of electrons = Q/F"); done += 1
            nm = ex(v, "mol_metal_found")[0]; ratio = ne_ / nm; check(abs(ratio - round(ratio)) < 0.02 and round(ratio) in (1, 2, 3), f"{P['id']}: whole electrons per ion ({ratio:.3f})")
            metal = re.search(r"from ([A-Z][a-z]?)", t)
            if metal and metal.group(1) in MOLAR: check(near(ex(v, "mass_found")[0] / nm, MOLAR[metal.group(1)], 0.006) if ex(v, "mass_found") else True, f"{P['id']}: molar mass of {metal.group(1)}")
            if P["kind"] == "time" and mI: check(near(ex(v, "time_found")[0], Qc / float(mI.group(1)), 0.005) and near(ex(v, "time_h_found")[0], ex(v, "time_found")[0] / 3600, 0.005), f"{P['id']}: t = Q/I, and in hours"); done += 1
check(done >= 150, f"independent checks run: {done}")
print(f"ch17 (five archetypes, 120 problems; {done} independent checks): all checks pass" if not fails else f"ch17: {fails} FAILED"); sys.exit(1 if fails else 0)
