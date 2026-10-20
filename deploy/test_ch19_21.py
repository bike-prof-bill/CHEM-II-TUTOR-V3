"""Chapters 19 and 21, three sheet-driven archetypes. Every sheet value, trap and pick on the board; then independent arithmetic from
each sentence: Δoct = hc/λ and × Nₐ; λ = ln2/t½, Nₜ/N₀ = e^(−λt), t = −ln(ratio)/λ; Z and N from the nuclide, the mass defect with
1.0073/1.0087/0.00055 amu, E = Δm c² and 931.5 MeV per amu, per nucleon = E/A; d count = group − oxidation state; unpaired electrons
from the d count and the spin state; ±1 % (instructor)."""
import sys, math, re
sys.path.insert(0, "archetypes"); import engine
import ch19_cft as CF, ch21_decay as DE, ch21_binding as BI
fails = 0
def check(c, m):
    global fails
    if not c: fails += 1; print("  FAIL:", m)
near = lambda a, b, r=0.01: abs(a - b) <= r * max(abs(b), 1e-300)
def shipped(A):
    m = engine.read_moves(f"content_{A.ID}_moves.csv"); e = engine.read_errors(f"content_{A.ID}_errors.csv")
    out = engine.build(A, 1, 1, engine.read_openers(f"content_{A.ID}_openers.csv"), m, e); return out, {v["fixed_id"]: v for v in out["variants"]}
def ex(v, st): return [e_["value"] for e_ in v["expected"] if e_["state"] == st]
h, c, NA = 6.626e-34, 2.998e8, 6.022e23
GROUP = {"Sc": 3, "Ti": 4, "V": 5, "Cr": 6, "Mn": 7, "Fe": 8, "Co": 9, "Ni": 10, "Cu": 11, "Zn": 12, "Ru": 8, "Rh": 9, "Pd": 10, "Ag": 11, "Pt": 10, "Au": 11}
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789"); SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
done = 0
for A in (CF, DE, BI):
    out, V = shipped(A)
    check(len(V) == 24 and len(out["openers"]) == 4 and all(not v["status"].startswith("DRAFT") for v in V.values()), f"{A.ID}: 24 problems under 4 scenarios ship, none DRAFT")
    for P in A.PROBLEMS:
        v = V[P["id"]]; t = P["text"]
        for e_ in P["expected"]: check(any(near(x, e_["value"], 1e-6) for x in ex(v, e_["state"])), f"{P['id']}: {e_['state']} = {e_['value']}")
        for st, right in P["picks"].items():
            b = [x for x in v["board"] if x["id"] == st]; check(b and b[0]["right"] == [f"{st}:{right}"] and any(o["id"] == f"{st}:{right}" for o in b[0]["options"]), f"{P['id']}: pick {st} = {right}")
        have = {(x["id"], x["state"]) for x in v["traps"]}
        for tr in P["traps"]:
            if (tr["id"], tr["state"]) not in have: check(any(abs(tr["value"] - x) <= 3 * max(0.02 * abs(x), 0.1 if x == int(x) and abs(x) < 50 else 0) for x in ex(v, tr["state"])) or tr["value"] == 0, f"{P['id']}: trap {tr['id']} at {tr['state']} = {tr['value']} missing and not within clearance")
        if A is CF and P["kind"] == "colour":
            lam = float(re.search(r"at ([0-9.]+) nm", t).group(1)) * 1e-9; E = h * c / lam
            check(near(ex(v, "deltaJ_found")[0], E, 0.005) and near(ex(v, "deltakJ_found")[0], E * NA / 1000, 0.005), f"{P['id']}: Δoct = hc/λ, and per mole"); done += 1
        if A is CF and P["kind"] in ("spin", "geometry"):
            m = re.search(r"\[([A-Z][a-z]?)", t); metal = m.group(1); ox = ex(v, "ox_found")[0]; d = ex(v, "d_found")[0]
            check(d == GROUP[metal] - ox, f"{P['id']}: d count = group {GROUP[metal]} − oxidation state {ox}"); done += 1
            if P["kind"] == "spin":
                t2g, eg, un = ex(v, "t2g_found")[0], ex(v, "eg_found")[0], ex(v, "unpaired_found")[0]; spin = P["picks"].get("spin_pick")
                check(t2g + eg == d, f"{P['id']}: t₂g + e_g = d"); 
                if spin == "low": want_t2g = min(d, 6)
                elif spin == "high": want_t2g = min(d, 3) + max(0, min(d - 5, 3))
                else: want_t2g = t2g
                want_un = (sum(1 for k in range(int(want_t2g)) if k < 3) - sum(1 for k in range(int(want_t2g)) if k >= 3)) + (sum(1 for k in range(int(d - want_t2g)) if k < 2) - sum(1 for k in range(int(d - want_t2g)) if k >= 2))
                check(t2g == want_t2g and un == want_un, f"{P['id']}: {spin}-spin d{int(d)}: t₂g {t2g} (want {want_t2g}), unpaired {un} (want {want_un})"); done += 2
            check(P["picks"]["magnetic_pick"] == ("paramagnetic" if ex(v, "unpaired_found")[0] > 0 else "diamagnetic"), f"{P['id']}: magnetism follows the unpaired count"); done += 1
        if A is DE:
            mh = re.search(r"half-life (?:of [^0-9]*)?(?:is )?([0-9.]+(?:e[+-]?\d+)?) (years|days|hours|minutes|seconds|y|d|h|min|s)\b", t)
            lam_list = ex(v, "lambda_found")
            if mh and lam_list: check(near(lam_list[0], math.log(2) / float(mh.group(1)), 0.005), f"{P['id']}: λ = ln 2 / t½ = {math.log(2) / float(mh.group(1)):.4g}"); done += 1
            lam = lam_list[0] if lam_list else (math.log(2) / float(mh.group(1)) if mh else None)
            mt = re.search(r"after ([0-9.]+(?:e[+-]?\d+)?) (years|days|hours|minutes|y|d|h|min)\b", t)
            if ex(v, "fraction_found") and mt and lam: check(near(ex(v, "fraction_found")[0], math.exp(-lam * float(mt.group(1))), 0.01), f"{P['id']}: Nₜ/N₀ = e^(−λt)"); done += 1
            if ex(v, "time_found") and ex(v, "ratio_found") and lam: check(near(ex(v, "time_found")[0], -math.log(ex(v, "ratio_found")[0]) / lam, 0.01), f"{P['id']}: t = −ln(ratio)/λ"); done += 1
        if A is BI:
            Z, N = ex(v, "Z_found")[0], ex(v, "N_found")[0]
            mz = re.search(r"([⁰¹²³⁴⁵⁶⁷⁸⁹]+)([₀₁₂₃₄₅₆₇₈₉]+)", t)
            if mz: Acount, Zt = int(mz.group(1).translate(SUP)), int(mz.group(2).translate(SUB)); check(Z == Zt and N == Acount - Zt, f"{P['id']}: Z {Zt}, N {Acount - Zt} from the nuclide"); done += 1
            mm = float(re.search(r"is ([0-9.]+) amu", t).group(1)); dm = Z * (1.0073 + 0.00055) + N * 1.0087 - mm
            check(abs(ex(v, "defect_found")[0] - dm) <= 0.0002 + 0.01 * abs(dm), f"{P['id']}: mass defect = {dm:.5f} amu"); done += 1
            dmk = ex(v, "defect_found")[0] * 1.6605e-27; check(near(ex(v, "EJ_found")[0], dmk * c * c, 0.01), f"{P['id']}: E = Δm c²")
            check(near(ex(v, "EMeV_found")[0], ex(v, "defect_found")[0] * 931.5, 0.01) and near(ex(v, "per_found")[0], ex(v, "EMeV_found")[0] / (Z + N), 0.005), f"{P['id']}: 931.5 MeV per amu; per nucleon = E/A"); done += 2
check(done >= 120, f"independent checks run: {done}")
print(f"ch19 and ch21 (three archetypes, 72 problems; {done} independent checks): all checks pass" if not fails else f"ch19/21: {fails} FAILED"); sys.exit(1 if fails else 0)
