"""Loader for archetypes/data/substances.json, the universal substance table. Chemistry files import this; the shell never does.
Underscore prefix: run.py does not treat this file as an archetype."""
import json, os
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "substances.json")
_DOC = json.load(open(PATH, encoding="utf-8"))
SUBSTANCES = _DOC["substances"]

def get(name, *fields):
    """Values of the named fields for one substance; raises if the substance or a field is missing (no silent defaults)."""
    if name not in SUBSTANCES: raise KeyError(f"substance {name!r} is not in substances.json")
    rec = SUBSTANCES[name]; out = []
    for f in fields:
        if f not in rec: raise KeyError(f"substances.json: {name} has no field {f!r}; the instructor must supply it before an archetype can use it")
        out.append(rec[f])
    return out if len(fields) != 1 else out[0]
