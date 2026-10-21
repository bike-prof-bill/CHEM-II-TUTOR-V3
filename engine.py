"""
engine.py  --  ONE engine for every archetype. It never learns any chemistry.

An archetype file supplies: VARIABLES, residual(), draw_state(), TRAPS, board_for(),
targets_for(), render_text(), sim_payload(), and optionally SPECIAL problem kinds.

For each variant the engine:
  1. draws a physically consistent state        (random physical variables)
  2. picks the kind of problem                  (which variable is unknown, or a special kind)
  3. picks display units and rounds the givens as the student will see them
  4. re-solves the unknown FROM THE ROUNDED GIVENS  -> the key
  5. declares EVERY number that may legitimately appear, each with a role and a dimension -> expected
     (intermediate and key values tied to a board state; the givens; the constants)
  6. computes what each wrong method would produce  -> traps
  7. validates the declaration and throws the variant away if any two numbers could be confused
     (rebuild spec, Change 2: the verifier matches against expected and traps ONLY, so the
     generator must guarantee the declaration is unambiguous)
Standard library only. Same seed -> same problems, always. Units live in units.json, not here.
"""
import json, math, random, hashlib, csv, os, itertools, re, glob

# ---------- units as data ----------
UNITS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "units.json")
UNITS = json.load(open(UNITS_PATH, encoding="utf-8"))
def _unit(u):
    if u not in UNITS["units"]: raise KeyError(f"unit {u!r} is not in units.json")
    return UNITS["units"][u]
def dim_of(unit):               return dict(UNITS["dimensions"][_unit(unit)["dimension"]]["dim"])
def dimension_of(unit):         return _unit(unit)["dimension"]
def canonical_unit(dimension):  return UNITS["dimensions"][dimension]["canonical"]
def to_canon(dimension, unit, x):
    u = _unit(unit); assert u["dimension"] == dimension, (dimension, unit)
    return x * u["factor"] + u["offset"]
def from_canon(dimension, unit, x):
    u = _unit(unit); assert u["dimension"] == dimension, (dimension, unit)
    return (x - u["offset"]) / u["factor"]
def convert(x, from_unit, to_unit):
    """x in from_unit -> value in to_unit, or None when the dimensions differ."""
    a, b = _unit(from_unit), _unit(to_unit)
    if a["dimension"] != b["dimension"]: return None
    return from_canon(b["dimension"], to_unit, to_canon(a["dimension"], from_unit, x))

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
REJECTS = {"ambiguous": 0, "trap_near_expected": 0, "given_near_key": 0}

def _forms(e):
    """Every (value, unit, abs_tol) a declared entry may be typed as."""
    return [(e["value"], e.get("unit", ""), e["abs_tol"])] + [(f["value"], f.get("unit", ""), f.get("abs_tol", e["abs_tol"])) for f in e.get("also", [])]

def _collide(a, b, tol_of, convert_too=False):
    """Could one typed input be read as both a and b? Mirrors the verifier's matcher: a typed unit must equal
    the form's unit; a bare number matches any form by value but cannot tick an entry that requires a unit.
    So two forms collide on their raw values unless their units differ AND one of the two entries requires its
    unit, because then the unit the student eventually types settles which was meant. (A quantity and the same
    quantity restated in a larger unit do not collide: the conversion is the student's step. A key that happens
    to equal a unitless constant does not collide with it: the key needs its unit.)
    With convert_too, b is also converted into a's unit: a restated given landing on the key is fortuitous
    whatever unit it is typed in. tol_of(ta, tb) gives the window, in a's unit."""
    for va, ua, ta in _forms(a):
        for vb, ub, tb in _forms(b):
            # a bare number can be read as both only if a typed unit would not settle it
            settles = (ua != ub) and ((ua and a.get("require_unit")) or (ub and b.get("require_unit")))
            if not settles and abs(va - vb) <= tol_of(ta, tb): return True
            if convert_too and ua and ub and ua != ub:
                vb2 = convert(vb, ub, ua)
                if vb2 is not None and abs(va - vb2) <= tol_of(ta, tb * abs(_unit(ub)["factor"] / _unit(ua)["factor"])): return True
    return False

# Policy switches for validate(). Both default to the reading that keeps problems whose given values happen to
# equal a conversion factor, without weakening any check the matcher relies on. See BUILD_LOG.md, step 2.
CONSTANT_COLLISIONS_REJECT = False   # True = spec read literally: an intermediate equal to a constant rejects the variant
DROP_INTERMEDIATE_EQUAL_TO_GIVEN = True   # an intermediate that equals a number on the page is not evidence; it is removed

def _same_quantity(g, tr):
    """A given and a trap of the same dimension whose values agree, in the trap's unit, within three trap windows: a student
    who types that number with its unit has restated the given, so the trap can never be told apart from it."""
    gv = convert(g["value"], g.get("unit") or "", tr.get("unit") or "")
    if gv is None: return False
    return abs(gv - tr["value"]) <= CLEARANCE * max(tr["abs_tol"], g.get("abs_tol", 0))
def validate(v):
    """Rebuild spec, Change 2. Returns the list of reasons this variant is ambiguous; empty = ships.
    May remove an intermediate form that merely restates a given (see DROP_INTERMEDIATE_EQUAL_TO_GIVEN)."""
    E, reasons = v["expected"], []
    if DROP_INTERMEDIATE_EQUAL_TO_GIVEN:
        givens = [e for e in E if e["role"] == "given"]
        keep = []
        for e in E:
            if e["role"] == "intermediate" and not e.get("require_worked") and not e.get("after") and any(_collide(e, g, lambda ta, tb: max(ta, tb)) for g in givens):   # a worked check may equal a given (K_confirmed); an `after` entry is asked for by name once its predecessor is set (13 Oct)
                v.setdefault("dropped", []).append(e["id"]); continue
            keep.append(e)
        v["expected"] = E = keep
        for b in v["board"]:                                  # a number state must keep at least one way to be established
            if b["kind"] == "number" and not any(e.get("state") == b["state"] for e in E):
                reasons.append(("ambiguous", b["state"], "no_evidence_left"))
    for a, b in itertools.combinations(E, 2):
        if a.get("state") == b.get("state"): continue
        if not CONSTANT_COLLISIONS_REJECT and "constant" in (a["role"], b["role"]) and "key" not in (a["role"], b["role"]): continue
        if (a.get("require_worked") and b["role"] == "given") or (b.get("require_worked") and a["role"] == "given"): continue   # a worked check equal to a given: by design
        if (a.get("after") or b.get("after")) and {a["role"], b["role"]} & {"given", "constant"}: continue   # an `after` entry is live only once its predecessor is set
        if a.get("after") and b.get("after") and a["state"] != b["state"]: continue   # two items each asked for by name at their own step are never live together (chapter 16: the two routes to ΔG° agree by design)
        if _collide(a, b, lambda ta, tb: max(ta, tb)): reasons.append(("ambiguous", a["id"], b["id"]))
    for tr in v["traps"]:
        if "value" not in tr: continue                       # a bound ("above": x) is not a value and cannot collide
        for e in E:
            if e.get("state") == tr["state"] and e["value"] and tr["value"] and e.get("abs_tol", 0) >= 0.5 * abs(e["value"]) and abs(math.log10(abs(e["value"]))) >= 15:   # an item accepted as a power of ten (chapter 17's K): clear means a factor of 3 apart or the other sign
                if (e["value"] > 0) == (tr["value"] > 0) and max(abs(e["value"]), abs(tr["value"])) / min(abs(e["value"]), abs(tr["value"])) <= 3: reasons.append(("trap_near_expected", tr["id"], e["id"]))
                continue
            if e.get("state") == tr["state"] and _collide(e, tr, lambda ta, tb: CLEARANCE * ta):
                reasons.append(("trap_near_expected", tr["id"], e["id"]))
    # a trap that lies on a given is undetectable (the student may simply have restated the given): drop the trap, keep the variant
    # (the Drinking Bird, 11 Oct: kJ-with-R-in-J gives back the known pressure)
    givens_all = [e for e in E if e["role"] == "given"]
    kept = []
    for tr in v["traps"]:
        if "value" in tr and any(_same_quantity(g, tr) for g in givens_all):
            v.setdefault("traps_dropped", []).append(tr["id"]); continue
        kept.append(tr)
    v["traps"] = kept
    keys = [e for e in E if e["role"] == "key"]
    for g in (e for e in E if e["role"] == "given"):
        for k in keys:
            if _collide(k, g, lambda ta, tb: CLEARANCE * ta, convert_too=True): reasons.append(("given_near_key", g["id"], k["id"]))
    return reasons

def _slug(s):
    out = "".join(c if c.isalnum() else "_" for c in s)
    while "__" in out: out = out.replace("__", "_")
    return out.strip("_")

def declare(v, A):
    """Turn the archetype's intermediates, key(s), givens and constants into the `expected` table."""
    exp, seen = [], set()
    for t in v.pop("targets"):
        role = t.pop("role", "key" if t.pop("is_key", False) else "intermediate")
        eid = ("key_" + t["state"]) if role == "key" else _slug(t["label"])
        e = {"id": eid, "role": role, "dim": dim_of(t.get("unit", ""))}; e.update(t); exp.append(e)
    for name, s in v["givens"].items():
        exp.append({"id": "g_" + name, "state": None, "role": "given", "label": name, "value": s["value"], "unit": s["unit"],
                    "dim": dim_of(s["unit"]), "abs_tol": round_sig(1e-6 * abs(s["value"]) + min(1e-9, 1e-3 * abs(s["value"])) if s["value"] else 1e-12, 3)})   # the absolute floor shrinks with tiny givens (Ksp-sized, 14 Oct): a 1e-9 floor swallowed every number near 1e-10
    for c in getattr(A, "CONSTANTS", []):
        exp.append({"id": "c_" + _slug(c["label"]), "state": None, "role": "constant", "label": c["label"], "value": c["value"],
                    "unit": c.get("unit", ""), "dim": dim_of(c.get("unit", "")), "abs_tol": c.get("abs_tol", round_sig(1e-3 * abs(c["value"]), 3))})
    for e in exp:
        if e["id"] in seen: raise RuntimeError(f"duplicate expected id {e['id']} in {A.ID}")
        seen.add(e["id"])
    v["expected"] = exp
    for tr in v["traps"]:
        if "for_state" in tr: tr["state"] = tr.pop("for_state")
    return v

def make_variant(A, seed, kind=None, tries=60, liquids=None, moves=None, fixed=None, limits=None, opener_title=None, template=None, items=None, version=None):
    rng = random.Random(seed)
    for _ in range(tries):
        if fixed is not None:                                    # a fixed problem (no random state): one shot
            v = A.make_fixed(rng, fixed)
            if v is None: break
            k = v["kind"]
        else:
            state, context = A.draw_state(rng, liquids, limits=limits, kind=kind, version=version) if limits else A.draw_state(rng, liquids, version=version)
            if version: context["version"] = version                  # the worked rung's versions of one problem kind (instructor, 12 Oct)
            k = kind or rng.choice(A.KINDS)
            if opener_title: context["opener"] = opener_title      # a trap or a sentence may belong to one scenario
            if template: context["template"] = template            # the scenario's own problem sentence
            if items: context["items"] = items                     # the scenario's optional items (+add / -remove)
            if k in getattr(A, "SPECIAL", {}):
                v = A.SPECIAL[k](rng, state, context)
            else:
                v = _standard(A, rng, state, context, k)
        if v is None: continue
        declare(v, A)                                            # steps 5-6 -> one table
        v["_kind"] = k
        if version: v["version"] = version
        stamp_board(v, A, moves, opener_title)                   # the step map as a schema
        v.pop("_kind", None)
        reasons = validate(v)                                    # step 7
        if reasons:
            for r in reasons: REJECTS[r[0]] += 1
            if fixed is not None: raise RuntimeError(f"{A.ID}: fixed problem {fixed} is ambiguous: {reasons}")
            continue
        v.update({"variant_id": f"{A.ID}:{seed}", "archetype_id": A.ID, "seed": seed, "kind": k})
        return v
    raise RuntimeError(f"no acceptable variant for seed {seed}")

def _standard(A, rng, state, context, unknown):
    shown, hidden, fixed = {}, set((context or {}).get("hidden", [])), (context or {}).get("fixed_units", {})
    for name, spec in A.VARIABLES.items():
        if name == unknown: continue
        unit = fixed.get(name) or A.pick_unit(rng, name, shown)
        shown[name] = {"value": round_shown(from_canon(spec["kind"], unit, state[name]), spec["round"][unit]), "unit": unit}
    known = {n: to_canon(A.VARIABLES[n]["kind"], s["unit"], s["value"]) for n, s in shown.items()}
    for h in hidden: shown.pop(h, None)                          # known to the solver, not printed (the vent's pressure comes from its depth)
    extra = dict((context or {}).get("extra_givens", {}))        # printed instead (the depth)
    uspec = A.VARIABLES[unknown]
    key_canon = solve_for(A.residual, known, unknown, *uspec["bounds"])
    if key_canon is None: return None
    full = dict(known); full[unknown] = key_canon
    if abs(A.residual(full, {})) > 1e-9 or not A.acceptable(full, context): return None
    ans_unit = rng.choice(uspec["answer_units"])
    targets = A.targets_for(full, shown, unknown, ans_unit)
    if hasattr(A, "extra_targets"): targets += A.extra_targets(full, shown, unknown, ans_unit, context)
    key = [t for t in targets if t.get("role") == "key"][0]
    traps = []
    for t in A.TRAPS:
        if not t["applies"](shown, unknown): continue
        if t.get("openers") and context.get("opener") not in t["openers"]: continue        # a trap that belongs to one scenario
        val = t["value"](A, shown, known, unknown, ans_unit, key["value"])
        if val is None or not math.isfinite(val): continue
        # the trap's window scales with its own value: the key's window was handed to a trap at 0.84 torr (a ratio typed as the answer)
        # and matched every small number (the instructor's Drinking Bird run, 11 Oct); never wider than the key's own window
        tol = key["abs_tol"] if abs(val) >= abs(key["value"]) or key["value"] == 0 else key["abs_tol"] * abs(val) / abs(key["value"])
        traps.append({"id": t["id"], "state": key["state"], "value": round_sig(val, 5), "unit": ans_unit,
                      "abs_tol": round_sig(max(tol, 0.005 * abs(val)), 3)})
    context["_full"] = full; board = A.board_for(shown, unknown, context); context.pop("_full", None)   # the board rule may need the solved state
    return {"context": context, "text": A.render_text(shown, unknown, ans_unit, context), "givens": dict(shown, **extra),
            "sim_params": A.sim_params(full, shown, unknown, ans_unit, context) if hasattr(A, "sim_params") else {},   # {name: value} for a simulation's address
            "board": board, "targets": targets, "traps": traps,
            "reveal_with_problem": None, "sim": A.sim_payload(full, unknown, rng),
            "eq_checks": A.equation_check(rng, unknown)}

# ---------- the step map as a schema (rebuild spec, Change 1) ----------
FACE_OF_KIND = {"pick": "choice", "direction": "choice", "number": "check", "equation": "check", "table": "check", "coefficients": "check", "text": "why", "reflection": "why"}
KINDS_OF_ITEM = set(FACE_OF_KIND)

def stamp_board(v, A, moves, opener_title=None):
    """Every item gets the full schema: id, stage, kind, register, face, requires, branch, label_when_done, pin,
    explicit, credit_gate. `stage` and `label_when_done` come from the instructor's moves file (by item id, the
    scenario's own row first, then the archetype row); an item with no stage is its own stage."""
    base = _moves_for_kind(moves or {}, v.get("kind") or v.get("_kind"))
    over = getattr(moves, "by_opener", {}).get(opener_title, {}) if moves else {}
    moves = {k: dict(base.get(k, {}), **over.get(k, {})) for k in set(base) | set(over)}
    seen = set()
    for b in v["board"]:
        b["id"] = b.get("id") or b["state"]; b["state"] = b["id"]
        if b["id"] in seen: raise RuntimeError(f"{A.ID}: duplicate step-map item {b['id']}")
        seen.add(b["id"])
        if b["kind"] not in KINDS_OF_ITEM: raise RuntimeError(f"{A.ID}: item {b['id']} has unknown kind {b['kind']}")
        row = moves.get(b["id"], {})
        b["stage"] = b["id"] if getattr(A, "STAGE_PER_STEP", False) else ((row.get("stage") or "").strip() or b.get("stage") or b["id"])   # brief 32 archetypes: the ladder counts per step, not per stage
        b["face"] = b.get("face") or FACE_OF_KIND[b["kind"]]
        b.setdefault("requires", []); b.setdefault("branch", None); b.setdefault("pin", False)
        b.setdefault("explicit", False); b.setdefault("credit_gate", False)
        b["label_when_done"] = (row.get("label_when_done") or "").strip() or b.get("label_when_done") or ""
        if b["kind"] in ("pick", "direction") and not b.get("options") and not b.get("options_from"):
            raise RuntimeError(f"{A.ID}: {b['kind']} item {b['id']} declares no options")
    if getattr(A, "PRECISION_RULE", False): v["precision_rule"] = True       # the student's-own-precision acceptance (instructor, 21 Oct; chapter 11 only while experimental)
    ids = seen
    for b in v["board"]:
        for r in b["requires"]:
            if r not in ids: raise RuntimeError(f"{A.ID}: item {b['id']} requires unknown item {r}")
        for opt, items in (b["branch"] or {}).items():
            for it in items:
                if it not in ids: raise RuntimeError(f"{A.ID}: branch {b['id']}:{opt} names unknown item {it}")
    return v

def read_openers(path):
    """Instructor's CSV: title, question, model answer, target concept, keywords."""
    out = []
    for r in csv.reader(open(path, encoding="utf-8-sig")):
        if len(r) >= 5 and r[1].strip().endswith("?"):
            kw = r[4]; mech = []
            if "||" in kw and re.search(r"(?i)particle", kw):                 # brief 32 (21 Oct): "PARTICLE (one needed): a, b || MECHANISM (one needed): c, d" -> two lists, one hit from each
                parts = [x.split(":", 1)[-1] for x in kw.split("||")]
                kw = parts[0]; mech = [k.strip() for k in parts[1].replace(";", ",").split(",") if k.strip()] if len(parts) > 1 else []
            out.append({"title": r[0].strip(), "question": r[1].strip(), "model_answer": r[2].strip(),
                        "target": r[3].strip(), "keywords": [k.strip() for k in kw.replace(";", ",").split(",") if k.strip()], **({"mechanism": mech} if mech else {}),
                        "liquids": [x.strip() for x in (r[5] if len(r) > 5 else "").split(";") if x.strip()],
                        "kinds":   [x.strip() for x in (r[6] if len(r) > 6 else "").split(";") if x.strip()]})
            out[-1]["fits"] = out[-1]["liquids"]        # what this scenario fits: liquids for one archetype, problem ids for another
            col = lambda j: (r[j].strip() if len(r) > j else "")
            out[-1]["media"] = {"image_with_question": col(7), "image_after_account": col(8), "image_alt": col(9),
                                "simulation": col(10), "simulation_opens": (col(11) or "meaning").lower(), "credit": col(13)}   # instructor's pictures and simulation, optional
            out[-1]["label_words"] = [x.strip() for x in col(12).replace(",", ";").split(";") if x.strip()]   # naming without mechanism (SCENARIO_CLAUDE, 9 Oct)
            out[-1]["role"] = (col(15).lower().strip() or "floater")
            if col(16) and not col(16).upper().startswith(("APPROVED", "DRAFT")): out[-1]["samples"] = col(16)   # brief 32: sample student answers (test data; never shown)   # worked | exam | floater (instructor, 12-13 Oct); the exam scenario is served once, unannounced, at Independent
            out[-1]["items"] = {"add": [x[1:].strip() for x in col(14).replace(",", ";").split(";") if x.strip().startswith("+")],
                                "remove": [x[1:].strip() for x in col(14).replace(",", ";").split(";") if x.strip().startswith("-")]}   # per-scenario sub-list (instructor, 10 Oct)
    return out

def read_moves(path):
    """Instructor's CSV: one row per step-map item, keyed by the `state` column (the item id). A row whose
    `state` is `stage:<name>` gives stage-level defaults for switch_ask, notebook_prompt, return_ask, park_text.
    A row with the `opener` column filled applies to that scenario only (per-scenario override, 10 Oct); its
    non-empty cells replace the archetype row's. Returns the archetype rows; overrides hang on `.by_opener`."""
    moves, by_opener = {}, {}
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        state = r.get("state", "").strip()
        if not state: continue
        opener = next((v.strip() for k, v in r.items() if k and k.lower().startswith("opener") and v), "")
        row = {("show" if k.lower().startswith("show") else "version" if k.lower().startswith("version") else "pivot_question" if k.lower().startswith("pivot question") else "pivot_keywords" if k.lower().startswith("pivot keywords") else "samples" if k.lower().startswith("sample answers") else k): v
               for k, v in r.items() if k and not k.lower().startswith("opener")}   # long headers carry their rule; the shell sees `show`, `version`, `pivot_question`, `pivot_keywords`, `openstax` (brief 32)
        ver = next((v.strip().lower() for k, v in r.items() if k and k.lower().startswith("version") and v), "")
        if ver and ver != "both": state = state + "@v:" + ver            # a row for one version of the worked rung (instructor, 12 Oct)
        # two rows for one key (a scenario's wording row and its show row, 13 Oct) merge: a filled cell wins, the first row's kept
        if opener: d = by_opener.setdefault(opener, {}).setdefault(state, {}); [d.setdefault(k, v) for k, v in row.items() if v]
        else: d = moves.setdefault(state, {}); [d.setdefault(k, v) for k, v in row.items() if v]   # "item@P1;P2" is an archetype row for those kinds only
    moves = _Moves(moves); moves.by_opener = by_opener
    return moves

def _moves_for_kind(moves, kind):
    """Archetype rows that apply to one problem kind: `item@K1;K2` wins over `item` for those kinds."""
    out = {k: v for k, v in moves.items() if "@" not in k}
    for k, v in moves.items():
        if "@" in k:
            item, kinds = k.split("@", 1)
            if kind in [x.strip() for x in kinds.replace(",", ";").split(";")]: out[item] = dict(out.get(item, {}), **{a: b for a, b in v.items() if b})
    return out
class _Moves(dict): pass

def read_errors(path):
    """Named-error questions: note and ask per error id; a row with `opener` filled applies to that scenario only."""
    base, by_opener = {}, {}
    if not os.path.exists(path): return base, by_opener
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        eid = r.get("error id", "").strip()
        if not eid: continue
        ask = next((v for k, v in r.items() if k and k.lower().startswith("ask")), "") or ""    # "ask (if no model, ...)" or "ask (one question; never names the fix)" (21 Oct)
        cells = {k: v for k, v in (("note", r.get("note (what the tutor is told)", "").strip()), ("ask", ask.strip()), ("registry", (r.get("registry id") or "").strip())) if v}
        op = r.get("opener (blank = every scenario)", "").strip()
        (by_opener.setdefault(op, {}) if op else base).setdefault(eid, {}).update(cells)
    return base, by_opener

def read_accounts(path):
    """Brief 32 (21 Oct): the wrong particle accounts the second reader may name, per scenario: id, registry id, what the account amounts
    to, the tutor's repair question. Rows with the opener column blank apply to every scenario of the archetype."""
    out = {}
    if not os.path.exists(path): return out
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        aid = (r.get("account id") or "").strip()
        if not aid: continue
        get = lambda pref: next((v for k, v in r.items() if k and k.lower().startswith(pref)), "") or ""
        op = get("opener").strip()
        out.setdefault(op, []).append({"id": aid, "registry": get("registry").strip(), "account": get("the account").strip(), "repair": get("repair").strip()})
    return out

def read_limits(path):
    """Generator limits per opener and liquid. `known point` is "boiling point" (known state = the normal boiling point, at standard pressure)
    or "temperature" (known state = a temperature drawn from [known lo, hi], with the model's pressure there). The other
    temperature is drawn from [other lo, hi], as an offset from the known temperature when `offset` is yes. `min gap` is the
    smallest allowed difference between the two temperatures (the archetype's default otherwise)."""
    out = {}
    if not os.path.exists(path): return out
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        g = lambda key: next((v.strip() for k, v in r.items() if k and k.lower().startswith(key)), "")
        op, liq = g("opener"), g("liquid")
        if not op or not liq: continue
        f = lambda key, default=None: (float(g(key)) if g(key) not in ("", None) else default)
        out.setdefault(op, {})[liq] = {"known_point": "boiling point" if "boil" in g("known point").lower() else "temperature",
                                       "known_lo_C": f("known temperature, low"), "known_hi_C": f("known temperature, high"),
                                       "lo_C": f("other temperature, low"), "hi_C": f("other temperature, high"),
                                       "offset": g("other is an offset").lower().startswith("y"), "min_gap": f("minimum gap", 2.0),
                                       "other_by": "depth" if g("other set by").lower().startswith("depth") else "temperature",
                                       "depth_lo_m": f("depth low"), "depth_hi_m": f("depth high"), "depth_step_m": f("depth step", 10.0)}
    return out

def read_sentences(path):
    """Per-scenario problem-sentence templates (SCENARIO_CLAUDE, 10 Oct): opener -> {kind -> template}. Placeholders in braces."""
    out = {}
    if not os.path.exists(path): return out
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        op = r.get("opener", "").strip(); t = r.get("template (placeholders in braces)", "").strip()
        if not op or not t: continue
        kinds = [k.strip() for k in r.get("problem kinds", "").replace(",", ";").split(";") if k.strip()] or ["*"]
        ver = next((v.strip().lower() for k, v in r.items() if k and k.lower().startswith("version") and v), "")   # worked-rung versions (instructor, 12 Oct)
        for k in kinds: out.setdefault(op, {})[k + ("@" + ver if ver else "")] = t
    return out

def _merge_trap_notes(notes, errors):
    out = {k: dict(v) for k, v in notes.items()}
    for eid, cells in errors.items(): out.setdefault(eid, {}).update(cells)
    return out

# ---------- the textbook, for the "More info" button (brief 32, 21 Oct) ----------
_TEXTBOOK = {}
def textbook_file(chapter):
    fs = sorted(glob.glob(os.path.join(os.path.dirname(__file__), "reference", "openstax", f"Chapter{int(chapter)}_*.md")))
    return fs[0] if fs else None
def _clean_passage(lines, cap=1800):
    out = []
    for l in lines:
        if l.startswith("![") or l.startswith("### ") or l.startswith("## "): continue
        out.append(l.rstrip())
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
    if len(text) > cap:
        cut = text.rfind("\n\n", 0, cap); text = text[:cut if cut > cap // 2 else cap].rstrip() + " …"
    return text
def textbook_passage(ref):
    """'11.4, Example 11.13 (step 1)' | '11.4, Freezing Point Depression (Figure 11.21)' | '11.4, Colligative Properties of Electrolytes (Table 11.3)'
    -> {ref, title, text} from the cleaned OpenStax chapter in reference/openstax, or None when the reference does not resolve (the build
    reports it). The text is the book's, cut to about 1800 characters at a paragraph break; figures become their captions."""
    ref = (ref or "").strip()
    m = re.match(r"(\d+)\.(\d+)\s*(?:,\s*(.*))?$", ref)
    if not m: return None
    ch, sec, rest = m.group(1), m.group(2), (m.group(3) or "").strip()
    f = textbook_file(ch)
    if not f: return None
    if f not in _TEXTBOOK: _TEXTBOOK[f] = open(f, encoding="utf-8").read().split("\n")
    L = _TEXTBOOK[f]
    def block(start):                       # lines from a heading to the next heading of the same or higher level
        lvl = len(L[start]) - len(L[start].lstrip("#"))
        end = start + 1
        while end < len(L) and not (L[end].startswith("#") and (len(L[end]) - len(L[end].lstrip("#"))) <= lvl): end += 1
        return L[start:end]
    sec_i = next((i for i, l in enumerate(L) if re.match(rf"## {ch}\.{sec}\b", l)), None)
    if sec_i is None: return None
    sec_lines = block(sec_i); sec_title = L[sec_i].lstrip("# ").strip()
    pieces, titles = [], []
    ex = re.search(r"Example (\d+\.\d+)", rest)
    name = re.sub(r"\s*\(.*?\)\s*", " ", rest).strip() if rest else ""
    name = re.sub(r"^Example \d+\.\d+.*$", "", name).strip()
    if ex:
        i = next((j for j, l in enumerate(L) if l.startswith(f"### Example {ex.group(1)} ")), None)
        if i is not None: pieces.append(_clean_passage(block(i)[1:])); titles.append(L[i].lstrip("# ").strip())
    if name and not ex:
        i = next((j for j, l in enumerate(L[:sec_i + len(sec_lines)]) if j > sec_i and l.startswith("### ") and l.lstrip("# ").strip().lower().startswith(name.lower())), None)
        if i is not None: pieces.append(_clean_passage(block(i)[1:])); titles.append(L[i].lstrip("# ").strip())
    fig = re.search(r"Figure (\d+\.\d+)", rest)
    if fig:
        cap = next((l for l in L if l.startswith(f"**Figure {fig.group(1)}**")), None)
        if cap: pieces.append(cap.replace("**", ""))
    tab = re.search(r"Table (\d+\.\d+)", rest)
    if tab:
        i = next((j for j, l in enumerate(sec_lines) if f"Table {tab.group(1)}" in l and not l.startswith("### ")), None)
        if i is not None:
            rows = [l for l in sec_lines[i:i + 40] if l.startswith("|")][:24]
            pieces.append(_clean_passage([sec_lines[i]] + rows, cap=2600))
    if not pieces: pieces.append(_clean_passage(sec_lines[1:], cap=1500)); titles.append(sec_title)
    return {"ref": ref, "title": titles[0] if titles else sec_title, "section": sec_title, "text": "\n\n".join(p for p in pieces if p)}

def build(A, n_per_kind, seed0=1, openers=None, moves=None, errors=None, limits=None, sentences=None, accounts=None):
    """OPENERS AND VARIANTS ALIGN (instructor, 20 Sept). Problems are made FOR a scenario: each opener names the
    liquids it fits, and every variant is born attached to one opener. No opener, no problem."""
    variants, seed = [], seed0
    extra = getattr(A, "EXTRA_MOVES", None)                      # brief 32: an archetype's own rows for steps the sheet gives per problem (the instrument task, the gap question)
    if extra:
        if moves is None: moves = _Moves({}); moves.by_opener = {}
        for k, row in extra.items(): moves.setdefault(k, {}); [moves[k].setdefault(a, b) for a, b in row.items() if b]
    fixed_pool = getattr(A, "FIXED", None)                       # a list of fixed problems instead of a generator
    known = [f["id"] for f in fixed_pool] if fixed_pool else [s[0] for s in A.SUBSTANCES]
    if openers:
        for oi, op in enumerate(openers):
            bad = [x for x in op["fits"] if x not in known]
            if bad or not op["fits"]: raise SystemExit(f"Opener '{op['title']}': the fits column is empty or names something unknown {bad}. Known: {known}")
            if fixed_pool:
                for fid in op["fits"]:
                    v = make_variant(A, seed, moves=moves, fixed=fid, opener_title=op["title"]); v["opener_index"] = oi; variants.append(v); seed += 1
            else:
                lim = (limits or {}).get(op["title"]); tpl = (sentences or {}).get(op["title"], {})
                for k in (op["kinds"] or A.KINDS):
                    versions = sorted({key.split("@", 1)[1] for key in tpl if key.startswith(k + "@")})   # a kind with versioned sentences is made in every version
                    for ver in (versions or [None]):
                        for _ in range(n_per_kind):
                            t = (tpl.get(k + "@" + ver) if ver else None) or tpl.get(k) or tpl.get("*")
                            v = make_variant(A, seed, k, liquids=op["fits"], moves=moves, limits=lim, opener_title=op["title"], template=t, items=op.get("items"), version=ver); v["opener_index"] = oi; variants.append(v); seed += 1
    elif fixed_pool and openers is None:                        # no openers file at all; an openers file with no row builds nothing (no opener, no problem)
        for f in fixed_pool: variants.append(make_variant(A, seed, moves=moves, fixed=f["id"])); seed += 1
    elif not fixed_pool:
        for k in A.KINDS:
            for _ in range(n_per_kind): variants.append(make_variant(A, seed, k, moves=moves)); seed += 1
    out = {"contract": 3, "archetype_id": A.ID, "title": A.TITLE, "relation": A.RELATION_TEXT, "notebook_url": A.NOTEBOOK_URL,
           "kinds": list(A.KINDS), "mechanism_words": list(getattr(A, "MECHANISM_WORDS", [])),
           "equation_picks": A.EQUATION_PICKS, "trap_notes": _merge_trap_notes(A.TRAP_NOTES, (errors or ({}, {}))[0]), "trap_notes_by_opener": (errors or ({}, {}))[1],
           "equation_symbols": A.EQUATION_SYMBOLS, "equation_constants": A.EQUATION_CONSTANTS, "openers": openers or [],
           "moves": dict(moves or {}), "moves_by_opener": getattr(moves, "by_opener", {}) if moves else {}, "variants": variants}
    for op in out["openers"]:                                   # brief 32: the wrong accounts the reader may name, this scenario's then the archetype's (absent when none: older bundles keep their content version)
        wa = list((accounts or {}).get(op["title"], [])) + list((accounts or {}).get("", []))
        if wa: op["wrong_accounts"] = wa
    # brief 32 (21 Oct): sample student answers are test data and never ship; the textbook anchors become passages for "More info"
    samples = {"openers": {}, "moves": {}}
    for op in out["openers"]:
        if op.get("samples"): samples["openers"][op["title"]] = op.pop("samples")
    for key, row in list(out["moves"].items()):
        if isinstance(row, dict) and row.get("samples"): samples["moves"][key] = row.pop("samples")
    for op_title, rows in out["moves_by_opener"].items():
        for key, row in rows.items():
            if isinstance(row, dict) and row.get("samples"): samples["moves"][f"{key}@{op_title}"] = row.pop("samples")
    out["samples"] = None
    passages, unresolved = {}, []
    for key, row in out["moves"].items():
        ref = row.get("openstax") if isinstance(row, dict) else None
        if ref:
            pz = textbook_passage(ref)
            if pz: passages[key] = pz
            else: unresolved.append(f"{key}: {ref}")
    if passages or unresolved: out["passages"] = passages; out["passages_unresolved"] = unresolved
    out.pop("samples", None)
    out["content_version"] = hashlib.sha1(json.dumps(out, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:10]
    out["samples"] = samples
    return out
