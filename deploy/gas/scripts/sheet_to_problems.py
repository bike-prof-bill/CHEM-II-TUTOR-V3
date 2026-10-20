"""Turns a SCENARIO_CLAUDE problem sheet (chapters 16+: expected values, trap values and right picks written out per problem) into
archetypes/data/sheets/<archetype>.json, which a sheet-driven archetype loads. Run: python3 scripts/sheet_to_problems.py <sheet.csv> <archetype id>.
The sheet is the instructor-approved source; the test re-derives what it can from the problem sentence."""
import csv, json, re, sys

def num(s):
    s = s.strip().replace("−", "-").replace("× 10⁻", "e-").replace("× 10", "e").replace("×10", "e")
    m = re.search(r"-?[0-9.]+(?:e[+-]?\d+)?", s); return float(m.group(0)) if m else None

def items(exp):
    out = []
    for part in [p.strip() for p in exp.split(" | ") if p.strip()]:
        m = re.match(r"(\w+)(?: \((.*)\))?: (.+)$", part)
        if not m: continue
        state, label, rest = m.group(1), (m.group(2) or "").strip(), m.group(3).strip()
        val = num(rest)
        if val is None: continue
        unit = re.sub(r"^-?[0-9.]+(?:e[+-]?\d+)?\s*", "", rest.replace("−", "-").replace("× 10⁻", "e-").replace("× 10", "e")).strip()
        shown = re.search(r"-?[0-9.]+(?:e[+-]?\d+)?", rest.replace("−", "-").replace("× 10⁻", "e-").replace("× 10", "e")).group(0)
        mant = shown.split("e")[0]; dec = len(mant.split(".")[1]) if "." in mant else 0; exp = int(shown.split("e")[1]) if "e" in shown else 0
        out.append({"state": state, "label": label, "value": val, "unit": unit, "half_ulp": 0.5 * 10 ** (-dec + exp)})   # half a unit in the last written place
    return out

def traps(tr):
    out = []
    for part in [p.strip() for p in tr.split(" | ") if p.strip()]:
        m = re.match(r"([A-Z_0-9]+) at (\w+): (.+)$", part)
        if m and num(m.group(3)) is not None: out.append({"id": m.group(1), "state": m.group(2), "value": num(m.group(3))})
    return out

def picks(pk):   # "anode_pick: Zn | electron_pick: from Zn to Cu | verdict: neither: E = 0": the value runs to the next " | "
    out = {}
    for part in [p.strip() for p in pk.split(" | ") if p.strip()]:
        m = re.match(r"(\w+): (.+)$", part)
        if m: out[m.group(1)] = m.group(2).split(":")[0].strip() if m.group(1) in ("verdict",) else m.group(2).strip()
    return out

def coeffs(exp):   # "coeffs_found (...): 3 Cu(s) + 2 HNO₃(aq) + 6 H⁺(aq) → 3 Cu²⁺(aq) + 2 NO(g) + 4 H₂O(l)" -> species, coefficients, arrow index
    m = re.search(r"coeffs_found[^:]*: ([^|]+?)(?: \| |$)", exp)
    if not m: return None
    lhs, rhs = m.group(1).split("→")
    def side(t):
        out = []
        for term in t.split(" + "):
            mm = re.match(r"\s*(\d*)\s*(\S.*?)\s*$", term.strip()); out.append((int(mm.group(1) or 1), mm.group(2)))
        return out
    L, R = side(lhs), side(rhs)
    return {"species": [n for _, n in L + R], "right": [c for c, _ in L + R], "arrow_after": len(L)}

sheet, arch = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(sheet, encoding="utf-8-sig")))
out = []
for r in rows:
    out.append({"id": r["id"], "scenario": r["scenario"], "kind": r["kind"], "text": r["problem sentence (as the student sees it)"],
                "constants": r.get("constants and their sources", ""), "expected": items(r["expected, item by item"]), "traps": traps(r["trap values (named mistakes)"]),
                "picks": picks(r["right picks"]), "coeffs": coeffs(r["expected, item by item"]), "tolerance": r.get("tolerance", ""), "sim": dict(kv.split("=", 1) for kv in [x.strip() for x in (r.get("simulation parameters") or "").split(";")] if "=" in kv), "status": r["status"]})
json.dump({"archetype": arch, "source_sheet": sheet.split("/")[-1], "problems": out}, open(f"archetypes/data/sheets/{arch}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
bad = [p["id"] for p in out if not p["expected"]]
print(f"{arch}: {len(out)} problems, {sum(len(p['expected']) for p in out)} expected items, {sum(len(p['traps']) for p in out)} traps; no expected parsed for: {bad}")
