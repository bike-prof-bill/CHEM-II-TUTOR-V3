"""
engine.py  --  ONE engine for every archetype. It never learns any chemistry.

An archetype file supplies: VARIABLES, residual(), draw_state(), TRAPS, board_for(),
targets_for(), render_text(), sim_payload(), and optionally SPECIAL problem kinds.

For each variant the engine:
  1. draws a physically consistent state        (random physical variables)
  2. picks the kind of problem                  (which variable is unknown, or a special kind)
  3. picks display units and rounds the givens as the student will see them
  4. re-solves the unknown FROM THE ROUNDED GIVENS  -> the key
  5. lists every number a student can legitimately produce, each tied to a board state -> targets
  6. computes what each wrong method would produce  -> traps
  7. throws the variant away if a wrong method, or a restated given, lands near the key
Standard library only. Same seed -> same problems, always.
"""
import json, math, random, hashlib, csv

UNITS = {
    "temperature": {"to":   {"K": lambda x: x, "degC": lambda x: x + 273.15},
                    "from": {"K": lambda x: x, "degC": lambda x: x - 273.15}},
    "pressure":    {"to":   {"atm": lambda x: x, "torr": lambda x: x / 760.0, "kPa": lambda x: x / 101.325},
                    "from": {"atm": lambda x: x, "torr": lambda x: x * 760.0, "kPa": lambda x: x * 101.325}},
    "molar_energy":{"to":   {"J/mol": lambda x: x, "kJ/mol": lambda x: x * 1000.0},
                    "from": {"J/mol": lambda x: x, "kJ/mol": lambda x: x / 1000.0}},
}
def to_canon(kind, unit, x):   return UNITS[kind]["to"][unit](x)
def from_canon(kind, unit, x): return UNITS[kind]["from"][unit](x)

def round_sig(x, n):
    if x == 0 or not math.isfinite(x): return x
    return round(x, n - 1 - int(math.floor(math.log10(abs(x)))))
def round_shown(x, spec):
    return round(x, spec["dp"]) if "dp" in spec else round_sig(x, spec["sig"])

def solve_for(residual, known, unknown, lo, hi, flags=None):
    """Value of `unknown` in [lo, hi] that makes the residual zero. Any relation, any variable."""
    def f(x):
        v = dict(known); v[unknown] = x
        try:
            r = residual(v, flags or {})
            return r if math.isfinite(r) else None
        except (ValueError, ZeroDivisionError, OverflowError):
            return None
    N = 400
    log_scale = lo > 0 and hi / lo > 50
    pts = [lo * (hi / lo) ** (i / N) if log_scale else lo + (hi - lo) * i / N for i in range(N + 1)]
    px, pf = None, None
    for x in pts:
        fx = f(x)
        if fx is None: px, pf = None, None; continue
        if pf is not None and (pf == 0 or pf * fx < 0):
            a, b, fa = px, x, pf
            for _ in range(200):
                m = 0.5 * (a + b); fm = f(m)
                if fm is None: break
                if fa * fm <= 0: b = m
                else: a, fa = m, fm
            return 0.5 * (a + b)
        px, pf = x, fx
    return None

CLEARANCE = 3          # a wrong-method number must sit this many grading windows from the key
REJECTS = {"fortuitous": 0}

def make_variant(A, seed, kind=None, tries=60, liquids=None):
    rng = random.Random(seed)
    for _ in range(tries):
        state, context = A.draw_state(rng, liquids)
        k = kind or rng.choice(A.KINDS)
        if k in getattr(A, "SPECIAL", {}):
            v = A.SPECIAL[k](rng, state, context)
        else:
            v = _standard(A, rng, state, context, k)
        if v is None: continue
        key_targets = [t for t in v["targets"] if t.get("is_key")]
        bad = False
        for kt in key_targets:                                   # step 7
            for tr in v["traps"]:
                if tr["for_state"] == kt["state"] and abs(tr["value"] - kt["value"]) <= CLEARANCE * kt["abs_tol"]: bad = True
            for g in v.get("_givens_in_key_units", {}).get(kt["state"], []):
                if abs(g - kt["value"]) <= CLEARANCE * kt["abs_tol"]: bad = True
        v.pop("_givens_in_key_units", None)
        if bad: REJECTS["fortuitous"] += 1; continue
        v.update({"variant_id": f"{A.ID}:{seed}", "archetype_id": A.ID, "seed": seed, "kind": k})
        return v
    raise RuntimeError(f"no acceptable variant for seed {seed}")

def _standard(A, rng, state, context, unknown):
    shown = {}
    for name, spec in A.VARIABLES.items():
        if name == unknown: continue
        unit = A.pick_unit(rng, name, shown)
        shown[name] = {"value": round_shown(from_canon(spec["kind"], unit, state[name]), spec["round"][unit]), "unit": unit}
    known = {n: to_canon(A.VARIABLES[n]["kind"], s["unit"], s["value"]) for n, s in shown.items()}
    uspec = A.VARIABLES[unknown]
    key_canon = solve_for(A.residual, known, unknown, *uspec["bounds"])
    if key_canon is None: return None
    full = dict(known); full[unknown] = key_canon
    if abs(A.residual(full, {})) > 1e-9 or not A.acceptable(full): return None
    ans_unit = rng.choice(uspec["answer_units"])
    targets = A.targets_for(full, shown, unknown, ans_unit)
    key = [t for t in targets if t.get("is_key")][0]
    traps = []
    for t in A.TRAPS:
        if not t["applies"](shown, unknown): continue
        val = t["value"](A, shown, known, unknown, ans_unit, key["value"])
        if val is None or not math.isfinite(val): continue
        traps.append({"id": t["id"], "for_state": key["state"], "value": round_sig(val, 5), "unit": ans_unit,
                      "abs_tol": round_sig(max(key["abs_tol"], 0.01 * abs(val)), 3)})
    same_kind = [from_canon(uspec["kind"], ans_unit, to_canon(uspec["kind"], s["unit"], s["value"]))
                 for n, s in shown.items() if A.VARIABLES[n]["kind"] == uspec["kind"]]
    return {"context": context, "text": A.render_text(shown, unknown, ans_unit, context), "givens": shown,
            "board": A.board_for(shown, unknown), "targets": targets, "traps": traps,
            "reveal_with_problem": None, "sim": A.sim_payload(full, unknown, rng),
            "eq_checks": A.equation_check(rng, unknown),
            "_givens_in_key_units": {key["state"]: same_kind}}

def read_openers(path):
    """Instructor's CSV: title, question, model answer, target concept, keywords."""
    out = []
    for r in csv.reader(open(path, encoding="utf-8-sig")):
        if len(r) >= 5 and r[1].strip().endswith("?"):
            out.append({"title": r[0].strip(), "question": r[1].strip(), "model_answer": r[2].strip(),
                        "target": r[3].strip(), "keywords": [k.strip() for k in r[4].split(",") if k.strip()],
                        "liquids": [x.strip() for x in (r[5] if len(r) > 5 else "").split(";") if x.strip()],
                        "kinds":   [x.strip() for x in (r[6] if len(r) > 6 else "").split(";") if x.strip()]})
    return out

def read_moves(path):
    """Instructor's CSV: one row per board state. The narrative lives here."""
    return {r["state"]: r for r in csv.DictReader(open(path, encoding="utf-8-sig"))}

def build(A, n_per_kind, seed0=1, openers=None, moves=None):
    """OPENERS AND VARIANTS ALIGN (instructor, 20 Sept). Problems are made FOR a scenario: each opener names the
    liquids it fits, and every variant is born attached to one opener. No opener, no problem."""
    variants, seed = [], seed0
    if openers:
        known = [s[0] for s in A.SUBSTANCES]
        for oi, op in enumerate(openers):
            bad = [x for x in op["liquids"] if x not in known]
            if bad or not op["liquids"]: raise SystemExit(f"Opener '{op['title']}': liquids column is empty or names an unknown liquid {bad}. Known: {known}")
            for k in (op["kinds"] or A.KINDS):
                for _ in range(n_per_kind):
                    v = make_variant(A, seed, k, liquids=op["liquids"]); v["opener_index"] = oi; variants.append(v); seed += 1
    else:
        for k in A.KINDS:
            for _ in range(n_per_kind): variants.append(make_variant(A, seed, k)); seed += 1
    out = {"archetype_id": A.ID, "title": A.TITLE, "relation": A.RELATION_TEXT, "notebook_url": A.NOTEBOOK_URL,
           "equation_picks": A.EQUATION_PICKS, "trap_notes": A.TRAP_NOTES, "equation_symbols": A.EQUATION_SYMBOLS, "equation_constants": A.EQUATION_CONSTANTS, "openers": openers or [], "moves": moves or {}, "variants": variants}
    out["content_version"] = hashlib.sha1(json.dumps(out, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:10]
    return out
