"""Chapter 15, four archetypes: every shipped problem checked against SCENARIO_CLAUDE's sheets (approved 17 Oct 2026): expected
values, trap values, right picks; constants sourced; no DRAFT; the arithmetic module against first principles."""
import sys, json, math, csv, re; sys.path.insert(0, "archetypes"); import engine
import ch15_ksp as KS, ch15_common_ion as CI, ch15_qsp as QS, ch15_complex as CX, _solubility as SOL
fails = 0
def check(c, m):
    global fails
    if not c: fails += 1; print("  FAIL:", m)
def num(s):
    m = re.search(r"-?[0-9.]+(?:e[+-]?\d+)?", s); return float(m.group(0))
def items(exp):   # "state (label): value unit | ..."
    out = []
    for part in exp.split("|"):
        m = re.match(r"\s*(\w+)(?: \(([^)]*)\))?: (.+)", part.strip())
        if m: out.append((m.group(1), m.group(2) or "", num(m.group(3))))
    return out
def traps(tr):
    out = []
    for part in tr.split("|"):
        m = re.match(r"\s*([A-Z_0-9]+) at (\w+): (.+)", part.strip())
        if m: out.append((m.group(1), m.group(2), num(m.group(3))))
    return out
def picks(pk):
    return dict(re.findall(r"(\w+): ([\w:]+)", pk))
near = lambda a, b, r=0.02: abs(a - b) <= r * max(abs(b), 1e-30)
SHEETS = {KS: "ch15_ksp_problems.csv", CI: "ch15_common_ion_problems.csv", QS: "ch15_qsp_problems.csv", CX: "ch15_complex_problems.csv"}
for A, sheet in SHEETS.items():
    m = engine.read_moves(f"content_{A.ID}_moves.csv"); e = engine.read_errors(f"content_{A.ID}_errors.csv")
    out = engine.build(A, 1, 1, engine.read_openers(f"content_{A.ID}_openers.csv"), m, e); V = {v["fixed_id"]: v for v in out["variants"]}
    check(len(V) == 24 and len(out["openers"]) == 4 and all(not v["status"].startswith("DRAFT") for v in V.values()), f"{A.ID}: 24 problems under 4 scenarios ship, none DRAFT")
    rows = list(csv.DictReader(open("docs/handoff_examples/" + sheet, encoding="utf-8-sig")))
    check(set(r["id"] for r in rows) == set(V), f"{A.ID}: the sheet's ids are the build's ids")
    for r in rows:
        v = V[r["id"]]; exp = {e_["state"]: [] for e_ in v["expected"]}
        for e_ in v["expected"]: exp[e_["state"]].append(e_["value"])
        for st, label, val in items(r["expected, item by item"]):
            if st in ("region", "method", "approx_checked"): continue
            got = exp.get(st, [])
            check(any(near(g_, val) for g_ in got), f"{r['id']}: {st} {label} = {val} (build has {got})")
        have = {(t["id"], t["state"]) for t in v["traps"]}
        gset = {round(g_["value"], 12) for g_ in v["givens"].values() if isinstance(g_, dict) and "value" in g_}
        for tid, st, val in traps(r["trap values (named mistakes)"]):
            if (tid, st) not in have:
                on_given = any(near(val, g_, 0.15) for g_ in gset) or any(near(val, x_, 0.06) for x_ in exp.get(st, []))   # within the clearance of a given (restated given) or of the right value: undetectable by design
                check(on_given, f"{r['id']}: trap {tid} at {st} = {val} missing and not explained by a given or the expected value")
        for item, right in picks(r["right picks"]).items():
            b = [x_ for x_ in v["board"] if x_["id"] == item]
            check(b and b[0]["right"] == [right], f"{r['id']}: {item} right = {right}")
        check(v["kind"] == r["kind"], f"{r['id']}: kind {r['kind']}")
    check(not any("^" in (x_["eq_checks"][0]["park_text"] if x_["eq_checks"] else "") for x_ in V.values()), f"{A.ID}: no caret in a park text")
st = SOL.salt("Ag2CrO4"); check(SOL.ksp_coefficient(st) == 4 and near(SOL.ksp_from_s(st, SOL.s_from_ksp(st)), st["Ksp"], 1e-9), "Ag2CrO4: (2x)^2 (x) = 4 x^3 round-trips")
D = json.load(open("archetypes/data/salts.json", encoding="utf-8"))
check(all(v.get("source") and "confirmed" in v["source"] for v in D["salts"].values()), "every salt confirmed against Appendix J")
check(D["complexes"]["Cu(NH3)4^2+"]["Kf"] == 1.7e13 and "unused" in D["complexes"]["Zn(NH3)4^2+"]["source"], "the Cu correction is in; the unconfirmed zinc complex is marked unused")
print("ch15 (four archetypes, 96 problems): all checks pass" if not fails else f"ch15: {fails} FAILED"); sys.exit(1 if fails else 0)
