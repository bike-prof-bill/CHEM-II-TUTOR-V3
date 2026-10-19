"""Chapter 16, five sheet-driven archetypes: every shipped problem's numbers re-derived from its own sentence where the sentence
holds the data (Appendix G values per species and the reaction; ΔH° and ΔS° for the crossover; K for ΔG° = −RT ln K), compared with
the sheet's expected values; every sheet trap present unless it coincides with a right value; picks on the board; nothing DRAFT."""
import sys, json, math, re; sys.path.insert(0, "archetypes"); import engine
import ch16_entropy as EN, ch16_free_energy as FE, ch16_spontaneity as SP, ch16_equilibrium_G as EQ, ch16_G_and_K as GK
fails = 0
def check(c, m):
    global fails
    if not c: fails += 1; print("  FAIL:", m)
near = lambda a, b, r=0.02: abs(a - b) <= r * max(abs(b), 1e-30) + 1e-12
R = 8.314
SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
def species_table(text):
    """'H₂O(l): ΔH°f (kJ/mol) -285.83; ΔG°f (kJ/mol) -237.1; S° (J/(mol·K)) 70 | H₂O(g): ...' -> {name: {dH, dG, S}}"""
    out = {}
    seg = text.split("values are:")[-1] if "values are:" in text else text.split("(Appendix G):")[-1] if "(Appendix G):" in text else text
    for part in seg.split(". ")[0].split(" | "):
        m = re.match(r"\s*([^:]+?): (.+)$", part.strip())
        if not m: continue
        name, body = m.group(1).strip(), m.group(2)
        d = {}
        for k, key in (("ΔH°f", "dH"), ("ΔG°f", "dG"), ("S°", "S")):
            mm = re.search(re.escape(k) + r" \([^)]*\) (-?[0-9.]+)", body)
            if mm: d[key] = float(mm.group(1))
        out[name] = d
    return out
def reaction(text):
    """'For aA + bB → cC + dD' -> ([(coef, name)], [(coef, name)])"""
    m = re.search(r"For (.+?) (?:at|,|the|Appendix)", text)
    if not m: return None
    lhs, rhs = m.group(1).split("→")
    def side(s):
        out = []
        for term in s.split(" + "):
            term = term.strip().rstrip(",")
            mm = re.match(r"(\d*)\s*(\S+)", term); out.append((int(mm.group(1) or 1), mm.group(2)))
        return out
    return side(lhs), side(rhs)
def delta(table, rx, key):
    (l, r) = rx
    return sum(c * table[n][key] for c, n in r) - sum(c * table[n][key] for c, n in l)
def shipped(A):
    m = engine.read_moves(f"content_{A.ID}_moves.csv"); e = engine.read_errors(f"content_{A.ID}_errors.csv")
    out = engine.build(A, 1, 1, engine.read_openers(f"content_{A.ID}_openers.csv"), m, e); return out, {v["fixed_id"]: v for v in out["variants"]}
def ex(v, st): return [e_["value"] for e_ in v["expected"] if e_["state"] == st]
derived = 0
for A in (EN, FE, SP, EQ, GK):
    out, V = shipped(A)
    check(len(V) == 24 and len(out["openers"]) == 4 and all(not v["status"].startswith("DRAFT") for v in V.values()), f"{A.ID}: 24 problems under 4 scenarios ship, none DRAFT")
    for P in A.PROBLEMS:
        v = V[P["id"]]; t = P["text"]
        # every sheet item is on the board with its value; every pick is a direction item with the sheet's right answer
        for e_ in P["expected"]: check(any(near(x, e_["value"], 1e-6) for x in ex(v, e_["state"])), f"{P['id']}: {e_['state']} = {e_['value']}")
        for st, right in P["picks"].items():
            b = [x for x in v["board"] if x["id"] == st]; check(b and b[0]["right"] == [f"{st}:{right}"] and b[0]["kind"] == "direction", f"{P['id']}: pick {st} = {right}")
        have = {(x["id"], x["state"]) for x in v["traps"]}
        for tr in P["traps"]:
            if (tr["id"], tr["state"]) not in have: check(any(abs(tr["value"] - x) <= 3 * max(0.02 * abs(x), 1e-9) for x in ex(v, tr["state"])), f"{P['id']}: trap {tr['id']} at {tr['state']} missing and not within clearance of the right value")
        # re-derive from the sentence
        tab = species_table(t); rx = reaction(t)
        if tab and rx and all(n in tab for side in rx for _, n in side):
            if "dH_found" in [e_["state"] for e_ in P["expected"]] and all("dH" in tab[n] for side in rx for _, n in side):
                dH = delta(tab, rx, "dH"); check(near(ex(v, "dH_found")[0], dH, 0.005), f"{P['id']}: ΔH° from the table = {dH:.4g}"); derived += 1
            if "dS_found" in [e_["state"] for e_ in P["expected"]] and all("S" in tab[n] for side in rx for _, n in side):
                dS = delta(tab, rx, "S"); check(near(ex(v, "dS_found")[0], dS, 0.005), f"{P['id']}: ΔS° from the table = {dS:.4g}"); derived += 1
                if ex(v, "dG_found") and A is FE:
                    dG = delta(tab, rx, "dH") - 298 * dS / 1000; check(near(ex(v, "dG_found")[0], dG, 0.01), f"{P['id']}: ΔG° = ΔH° − TΔS° = {dG:.4g}"); derived += 1
                if ex(v, "Teq_found"):
                    T = delta(tab, rx, "dH") * 1000 / dS; check(near(ex(v, "Teq_found")[0], T, 0.005) and near(ex(v, "TeqC_found")[0], T - 273.15, 0.01), f"{P['id']}: T at ΔG° = 0 is {T:.4g} K"); derived += 1
            if ex(v, "dGf_found") and all("dG" in tab[n] for side in rx for _, n in side):
                dGf = delta(tab, rx, "dG"); check(near(ex(v, "dGf_found")[0], dGf, 0.005), f"{P['id']}: ΔG° from ΔG°f = {dGf:.4g}"); derived += 1
            if ex(v, "dG0_found") and A is GK and all("dG" in tab[n] for side in rx for _, n in side):
                dG0 = delta(tab, rx, "dG"); check(near(ex(v, "dG0_found")[0], dG0, 0.005), f"{P['id']}: ΔG° = {dG0:.4g}"); derived += 1
                if ex(v, "K_found"): check(near(ex(v, "K_found")[0], math.exp(-dG0 * 1000 / (R * 298)), 0.03), f"{P['id']}: K = exp(−ΔG°/RT)"); derived += 1
        m = re.search(r"ΔH° = (-?[0-9.]+) kJ and ΔS° = (-?[0-9.]+) J/K", t)
        if m and ex(v, "Tcross_found"):
            dH, dS = float(m.group(1)), float(m.group(2)); check(near(ex(v, "Tcross_found")[0], dH * 1000 / dS, 0.005), f"{P['id']}: T cross = ΔH°/ΔS°"); derived += 1
            mT = re.search(r"ΔG° at ([0-9.]+) K", t)
            if mT: check(near(ex(v, "dG_found")[0], dH - float(mT.group(1)) * dS / 1000, 0.02), f"{P['id']}: ΔG° at {mT.group(1)} K"); derived += 1
        m = re.search(r"ΔH = \+?(-?[0-9.]+) kJ\). Find ΔS\(surr\) and ΔS\(univ\) at .*?\(([0-9.]+) K\)", t)
        if m and ex(v, "dSsurr_found"):
            dH, T = float(m.group(1)), float(m.group(2)); check(near(ex(v, "dSsurr_found")[0], -dH * 1000 / T, 0.005), f"{P['id']}: ΔS(surr) = −ΔH/T"); derived += 1
        m = re.search(r"K(?:sp|p|c)? = \\\(([0-9.]+) \\times 10\^\{(-?\d+)\}\\\)", t)
        if m and A is GK and P["kind"] == "G_from_K":
            K = float(m.group(1)) * 10 ** int(m.group(2)); check(near(ex(v, "dG0_found")[0], -R * 298 * math.log(K) / 1000, 0.01), f"{P['id']}: ΔG° = −RT ln K"); derived += 1
check(derived >= 60, f"re-derived {derived} values from the sentences (expected at least 60)")
print(f"ch16 (five archetypes, 120 problems; {derived} values re-derived): all checks pass" if not fails else f"ch16: {fails} FAILED"); sys.exit(1 if fails else 0)
