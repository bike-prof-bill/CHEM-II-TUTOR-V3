"""Independent checks on the three chapter 15 skeletons: every placeholder's numbers re-derived by separate arithmetic; verdicts and
perturbation answers; named picks never the right answer; traps clear of their steps; every salt sourced; nothing ships."""
import sys, json, math; sys.path.insert(0, "archetypes"); import engine
import ch15_ksp as KS, ch15_common_ion as CI, ch15_qsp as QS, ch15_complex as CX, _solubility as SOL
fails = 0
def check(c, m):
    global fails
    if not c: fails += 1; print("  FAIL:", m)
near = lambda a, b, r=0.01: abs(a - b) <= r * max(abs(b), 1e-18)
def build(A):
    m = engine.read_moves(f"content_{A.ID}_moves.csv"); e = engine.read_errors(f"content_{A.ID}_errors.csv")
    check(engine.build(A, 1, 1, engine.read_openers(f"content_{A.ID}_openers.csv"), m, e)["variants"] == [], f"{A.ID}: nothing ships")
    out = engine.build(A, 1, 1, engine.read_openers(f"tests/fixtures/content_{A.ID}_openers_allkinds.csv"), m, e); V = {v["fixed_id"]: v for v in out["variants"]}
    for v in V.values():
        check(v["status"].startswith("DRAFT"), f"{v['fixed_id']}: DRAFT")
        for b in v["board"]:
            if b["kind"] in ("direction", "pick") and "options" in b:
                for o in b["options"]:
                    if o.get("names"): check(o["id"] not in b["right"], f"{v['fixed_id']} {b['id']}: named option is wrong")
        for t in v["traps"]:
            if "value" in t:
                for e in v["expected"]:
                    if e["state"] == t["state"]: check(abs(t["value"] - e["value"]) > 2 * max(t["abs_tol"], e["abs_tol"]), f"{v['fixed_id']}: trap {t['id']} clear of {e['label']}")
    return V
ex = lambda V, fid, st, i=0: [e for e in V[fid]["expected"] if e["state"] == st][i]["value"]
right = lambda V, fid, st: [b for b in V[fid]["board"] if b["id"] == st][0]["right"]
# Ksp: s = (Ksp/coef)^(1/n)
V = build(KS); check(len(V) == 5, "ksp: five placeholders")
check(near(ex(V, "S1", "s_found"), math.sqrt(1.6e-10)) and near(ex(V, "S1", "grams_found"), math.sqrt(1.6e-10) * 143.32) and not any(b["id"] == "conc_found" for b in V["S1"]["board"]), "S1 AgCl: s = root Ksp, grams per litre, no ion step for a 1:1 salt")
s2 = (4.0e-11 / 4) ** (1 / 3); check(near(ex(V, "S2", "s_found"), s2) and near(ex(V, "S2", "conc_found"), 2 * s2) and any(t["id"] == "COEFFICIENT_FORGOTTEN" and near(t["value"], (4.0e-11) ** (1 / 3)) for t in V["S2"]["traps"]), "S2 CaF2: s from 4s^3, [F-] = 2s, the 4 left out is named")
s3 = (9.0e-12 / 4) ** (1 / 3); check(near(ex(V, "S3", "s_found"), s3) and near(ex(V, "S3", "conc_found"), 2 * s3), "S3 Ag2CrO4: s from 4s^3, [Ag+] = 2s")
sk = 0.66 / 461.01; check(near(ex(V, "K1", "s_found"), sk) and near(ex(V, "K1", "ksp_found"), 4 * sk ** 3) and any(t["id"] == "GRAMS_WITHOUT_MOLAR_MASS" for t in V["K1"]["traps"]), "K1 PbI2: s from grams per litre, Ksp = 4s^3, grams typed as moles named")
check(all(right(V, f, "perturb_1") == ["p1:falls"] for f in V), "a common ion lowers solubility")
# common ion: exact vs small-s
V = build(CI); check(len(V) == 3, "common ion: three placeholders")
check(near(ex(V, "C1", "s_found"), 1.6e-10 / 0.10) and right(V, "C1", "method") == ["method:smalls"] and near(ex(V, "C1", "pure_found"), math.sqrt(1.6e-10)), "C1 AgCl in 0.10 M NaCl: s = Ksp/[Cl-], small-s holds, pure-water s for the comparison")
check(near(ex(V, "C2", "s_found"), 4.0e-11 / 0.050 ** 2, 0.02), "C2: s = Ksp/[F-]^2")
check(near(ex(V, "C3", "s_found"), math.sqrt(4.0e-11 / 0.020) / 2, 0.02), "C3: s = sqrt(Ksp/[Ca2+])/2, from Ksp = [Ca2+](2s)^2")
check(all(any(t["id"] == "COMMON_ION_IGNORED" for t in V[f]["traps"]) for f in V), "the pure-water s is named everywhere")
# Qsp
V = build(QS); check(len(V) == 4, "qsp: four placeholders")
check(near(ex(V, "Q1", "conc_found"), 5e-5) and near(ex(V, "Q1", "Q_found"), 2.5e-9) and right(V, "Q1", "verdict") == ["v:forms"], "Q1: dilution to 5e-5 each, Q 2.5e-9 > Ksp, precipitates")
check(near(ex(V, "Q2", "Q_found"), 1e-10) and right(V, "Q2", "verdict") == ["v:none"], "Q2: Q 1e-10 < 1.6e-10, stays dissolved")
check(near(ex(V, "Q3", "conc_found", 0), 2.5e-4) and near(ex(V, "Q3", "conc_found", 1), 1.5e-3) and near(ex(V, "Q3", "Q_found"), 2.5e-4 * 1.5e-3 ** 2) and right(V, "Q3", "verdict") == ["v:none"], "Q3 PbI2: unequal volumes, Q = [Pb][I]^2 below Ksp")
check(right(V, "Q4", "verdict") == ["v:forms"] and any(t["id"] == "VOLUME_NOT_TOTALED" for t in V["Q4"]["traps"]) and any(t["id"] == "EXPONENTS_DROPPED" for t in V["Q4"]["traps"]), "Q4: precipitates; the other solution's volume and the dropped exponent are named")
# complex ions: complete formation, Kd = 1/Kf, the free metal by small-x where it holds and exactly where it does not
V = build(CX); check(len(V) == 3, "complex: three placeholders")
C1, L1 = 0.005, 0.50 - 2 * 0.005; x1 = (1 / 1.7e7) * C1 / L1 ** 2
check(near(ex(V, "M1", "complete_found", 0), C1) and near(ex(V, "M1", "complete_found", 1), L1) and near(ex(V, "M1", "Kd_found"), 1 / 1.7e7) and near(ex(V, "M1", "x_found"), x1, 0.02) and right(V, "M1", "method") == ["method:smallx"], "M1 Ag(NH3)2+: complex 0.0050 M, ligand left 0.49 M, Kd 5.9e-8, free Ag+ = Kd C / L^2, small-x holds")
C2, L2 = 0.020 * 25 / 100, 2.00 * 75 / 100 - 4 * 0.005; x2 = (1 / 1.1e13) * C2 / L2 ** 4
check(near(ex(V, "M2", "x_found"), x2, 0.02) and any(t["id"] == "LIGAND_EXPONENT_DROPPED" and near(t["value"], (1 / 1.1e13) * C2 / L2, 0.02) for t in V["M2"]["traps"]) and any(t["id"] == "VOLUME_NOT_TOTALED" for t in V["M2"]["traps"]), "M2 Cu(NH3)4 2+: free Cu2+ with L^4; the ligand to the first power and the other volume are named")
Kd3 = 1 / 8.9e2; C3, L3 = 0.0005, 0.0015 - 0.0005
import math as _m; a_ = 1.0; b_ = L3 + Kd3; c_ = -Kd3 * C3; x3 = (-b_ + _m.sqrt(b_ * b_ - 4 * a_ * c_)) / (2 * a_)
check(near(ex(V, "M3", "x_found"), x3, 0.01) and right(V, "M3", "method") == ["method:exact"] and any(t["id"] == "SMALL_S_WHEN_IT_FAILS" for t in V["M3"]["traps"]) and any(t["id"] == "KF_FOR_KD" for t in V["M3"]["traps"]), "M3 Fe(SCN)2+: small Kf, the quadratic's root, small-x fails and is named, Kf-for-Kd named")
check(all(right(V, f, "perturb_1") == ["p1:falls"] for f in V) and all(any(t["id"] == "COMPLETION_NOT_ASSUMED" for t in V[f]["traps"]) for f in V), "more ligand lowers the free metal; the pre-complexing concentration is named everywhere")
# the arithmetic module against first principles
st = SOL.salt("Ag2CrO4"); check(SOL.ksp_coefficient(st) == 4 and near(SOL.ksp_from_s(st, SOL.s_from_ksp(st)), st["Ksp"]), "Ag2CrO4: (2s)^2 (s) = 4 s^3 round-trips")
D = json.load(open("archetypes/data/salts.json", encoding="utf-8")); check(all(v.get("source") for v in D["salts"].values()), "every salt has a source line")
print("ch15 (four archetypes): all checks pass" if not fails else f"ch15: {fails} FAILED"); sys.exit(1 if fails else 0)
