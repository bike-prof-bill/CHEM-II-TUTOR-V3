#!/usr/bin/env python3
"""Write every authored string in the repository to one sorted text file.

Authored = text a student or the instructor could read. Three sources:

  1. Every non-empty cell of every content_*.csv (openers, moves). One line per
     cell, keyed by the row's first column and the column header, so adding a
     column (the step-3 `stage` column) adds lines but alters none.
  2. Named objects in archetypes/ch10_cc.py that hold content rather than code:
     TITLE, RELATION_TEXT, SUBSTANCES (liquids table), EQUATION_PICKS,
     TRAP_NOTES, ASK, and the trap ids. Serialised as JSON, one line per entry.
     Keyed by name, not by file, so moving one to a data file in step 2 is a
     manifest change, not a baseline change.
  3. Any string literal in archetypes/ch10_cc.py of 20+ characters containing a
     space, docstrings excluded: prose inside functions (the slope problem sentence).

Usage:
    python3 scripts/snapshot_content.py content/BASELINE_authored.txt   # once, at the first commit
    python3 scripts/snapshot_content.py content/CURRENT_authored.txt    # any time; check_content.sh compares

Deterministic: same inputs, same bytes.
"""
import ast
import csv
import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_GLOBS = ["content_*.csv", "content/*.csv"]
MODULES = {                      # module -> names of authored objects
    "ch10_cc": ["TITLE", "RELATION_TEXT", "SUBSTANCES", "EQUATION_PICKS", "TRAP_NOTES", "ASK"],
    "ch13_ice": ["TITLE", "RELATION_TEXT", "EQUATION_PICKS", "TRAP_NOTES"],
}
TRAP_ID_MODULES = ["ch10_cc"]    # modules whose TRAPS list carries authored ids (ch13_ice's trap ids live in its code paths)
PROSE_FILES = ["archetypes/*.py"]
JSON_TABLES = ["archetypes/data/substances.json"]   # universal data: one line per record
PROSE_MIN = 20


def esc(s):
    return str(s).replace("\n", "\\n").replace("\t", "\\t")


def csv_cells(path):
    rows = list(csv.reader(path.open(newline="", encoding="utf-8-sig")))
    header, hrow = None, None
    for i, r in enumerate(rows):
        if sum(1 for c in r if c.strip()) >= 2:
            header, hrow = r, i
            break
    name = path.name
    for i, r in enumerate(rows):
        if header is None or i <= hrow:
            continue
        key = r[0].strip() if r and r[0].strip() else f"row{i}"
        for j, c in enumerate(r):
            if not c.strip():
                continue
            col = header[j].strip() if j < len(header) and header[j].strip() else f"col{j}"
            yield f"csv\t{name}\t{esc(key)}\t{esc(col)}\t{esc(c)}"


def module_objects():
    sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "archetypes"))
    for mod, names in MODULES.items():
        M = importlib.import_module(mod)
        for n in names:
            v = getattr(M, n)
            if isinstance(v, dict):
                for k in sorted(v):
                    yield f"obj\t{mod}.{n}\t{esc(k)}\t{json.dumps(v[k], ensure_ascii=False, sort_keys=True)}"
            elif isinstance(v, (list, tuple)):
                for item in v:
                    yield f"obj\t{mod}.{n}\t-\t{json.dumps(item, ensure_ascii=False, sort_keys=True)}"
            else:
                yield f"obj\t{mod}.{n}\t-\t{json.dumps(v, ensure_ascii=False)}"
    for mod in TRAP_ID_MODULES:
        M = importlib.import_module(mod)
        for t in M.TRAPS:
            yield f"obj\t{mod}.TRAPS.id\t-\t{json.dumps(t['id'])}"


def prose_literals():
    for pat in PROSE_FILES:
        for p in sorted(ROOT.glob(pat)):
            tree = ast.parse(p.read_text(encoding="utf-8"))
            docstrings = {id(n.value) for n in ast.walk(tree)          # docstrings are code commentary, not content
                          if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str)}
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstrings:
                    s = node.value.strip()
                    if len(s) >= PROSE_MIN and " " in s:
                        yield f"prose\t{p.stem}\t-\t{esc(s)}"


def json_records():
    for pat in JSON_TABLES:
        for p in sorted(ROOT.glob(pat)):
            doc = json.load(p.open(encoding="utf-8"))
            for name in sorted(doc.get("substances", {})):
                rec = {k: v for k, v in doc["substances"][name].items() if k != "source"}
                yield f"json\t{p.name}\t{esc(name)}\t{json.dumps(rec, ensure_ascii=False, sort_keys=True)}"

def collect():
    lines = []
    lines.extend(json_records())
    for pat in CSV_GLOBS:
        for p in sorted(ROOT.glob(pat)):
            lines.extend(csv_cells(p))
    lines.extend(module_objects())
    lines.extend(prose_literals())
    return sorted(set(lines))


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = ROOT / sys.argv[1]
    lines = collect()
    if not lines:
        sys.exit("snapshot_content: nothing found; check CSV_GLOBS and MODULES.")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(lines)} authored strings -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
