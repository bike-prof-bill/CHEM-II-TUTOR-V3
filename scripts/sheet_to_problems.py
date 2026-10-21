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
    """'I_OMITTED (GC2-M-06) at i_found: 1' -> value trap with its registry id; 'PERTURB_I_IGNORED at perturb_1: unchanged' -> a named
    wrong pick (no number), kept under 'pick' so the archetype can name that option (brief 32, 21 Oct)."""
    out = []
    for part in [p.strip() for p in tr.split(" | ") if p.strip()]:
        m = re.match(r"([A-Z_0-9]+)(?: \(([^)]*)\))? at (\w+): (.+)$", part)
        if not m: continue
        rec = {"id": m.group(1), "state": m.group(3)}
        if m.group(2): rec["registry"] = m.group(2).strip()
        v = num(m.group(4))
        if v is not None: rec["value"] = v
        else: rec["pick"] = m.group(4).strip().split()[0].strip(",.;")
        out.append(rec)
    return out

def picks(pk):   # "anode_pick: Zn | electron_pick: from Zn to Cu | verdict: neither: E = 0": the value runs to the next " | "
    out = {}
    for part in [p.strip() for p in pk.split(" | ") if p.strip()]:
        m = re.match(r"(\w+): (.+)$", part)
        if m:
            v = m.group(2).split(":")[0].strip() if m.group(1) in ("verdict",) else m.group(2).strip()
            if re.match(r"^(rises|falls|unchanged|forward|reverse|neither|doubles|halves|yes|no|positive|negative|zero|first|second|into|out|disappearing|appearing)\b", v): v = v.split()[0].strip(",.;")   # a bare direction word followed by a note ("falls (the same moles of CaCl₂) — why: ...", 21 Oct)
            out[m.group(1)] = v
    return out

def instrument(cell):
    """'Move `salt_g` until `Tf_readout` reads −10.0 °C. ... Checked value: 235.6 g; accept any whole number of grams from 235 to 236 ...'
    -> the control, the reading and its target, the expected value with its unit, and the accepted window."""
    if not cell or not cell.strip(): return None
    ids = re.findall(r"`(\w+)`", cell)
    tgt = re.search(r"reads? (−?-?[0-9.]+)\s*(°C|K|atm|torr|M|mol/kg|g|%)?", cell)
    chk = re.search(r"Checked value:\s*(−?-?[0-9.]+)\s*([A-Za-z°/%]+)", cell)
    win = re.search(r"from (−?-?[0-9.]+) to (−?-?[0-9.]+)", cell)
    out = {"control": ids[0] if ids else "", "reading": ids[1] if len(ids) > 1 else "", "text": cell.strip()}
    if tgt: out["target"] = num(tgt.group(1)); out["target_unit"] = tgt.group(2) or ""
    if chk: out["value"] = num(chk.group(1)); out["unit"] = chk.group(2)
    if win: lo, hi = num(win.group(1)), num(win.group(2)); out["value"] = (lo + hi) / 2; out["abs_tol"] = (hi - lo) / 2 + 0.1   # 235 to 236 -> 235.5 ± 0.6: both whole numbers inside, their neighbours outside
    return out

def predict(cell):
    """'If the crew spread twice ... : rises | falls | unchanged. Right: falls.' -> options and the right one."""
    if not cell or not cell.strip(): return None
    m = re.search(r"Right:\s*(\w+)", cell); opts = re.search(r":\s*([\w ]+(?:\s*\|\s*\w+)+)\s*\.", cell)
    return {"right": m.group(1).strip() if m else "", "options": [o.strip() for o in opts.group(1).split("|")] if opts else [], "text": cell.split(":")[0].strip() if ":" in cell else cell.strip()}

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
                "picks": picks(r["right picks"]), "coeffs": coeffs(r["expected, item by item"]), "tolerance": r.get("tolerance", ""), "sim": dict(kv.split("=", 1) for kv in [x.strip() for x in (r.get("simulation parameters") or "").split(";")] if "=" in kv), "status": r["status"],
                # brief 32 (21 Oct): difficulty, the nearest end-of-chapter problem, the simulation sequence, the exam item, the worked companion
                "difficulty": (r.get("difficulty") or "").strip(), "nearest_eoc": (r.get("nearest EOC") or "").strip(),
                "sim_predict": predict(r.get("sim predict")), "sim_reveal": (r.get("sim reveal") or "").strip(), "sim_instrument": instrument(r.get("sim instrument")),
                "sim_gap": (r.get("sim gap question") or "").strip(), "sim_opens_at": (r.get("sim opens at") or "").strip(), "exam_item": (r.get("exam item") or "").strip(),
                "companion": ((r.get("worked companion") or "").strip().split()[0].strip("(,") if (r.get("worked companion") or "").strip() else "")})
json.dump({"archetype": arch, "source_sheet": sheet.split("/")[-1], "problems": out}, open(f"archetypes/data/sheets/{arch}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
bad = [p["id"] for p in out if not p["expected"]]
for p in out:   # a trap that is a pick must name a state in picks; a value trap must name a numbered state
    for t in p["traps"]:
        if "pick" in t and t["state"] not in p["picks"]: print(f"  WARNING {p['id']}: pick trap {t['id']} at {t['state']} names no pick")
print(f"{arch}: {len(out)} problems, {sum(len(p['expected']) for p in out)} expected items, {sum(len(p['traps']) for p in out)} traps; no expected parsed for: {bad}")
