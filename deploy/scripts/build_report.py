#!/usr/bin/env python3
"""Build report (rebuild spec, Definition of done). Measures the shipped bundles; changes nothing.
Per archetype and overall: opinion-only share three ways, generation share, gate mix by face, every opinion-judged item.
Definitions (Fable, 11 Oct 2026; accepted by the instructor 12 Oct as the first version):
  gate of an item: text -> G2 (computer keyword gate + model + second reader), pick/direction -> G1, number/equation/table -> G0,
                   reflection -> none (never graded). The same table as gas/log.gs.
  opinion-only item: one whose acceptance rests on the model's judgement (G2). G3 (model alone, no computer gate) is not used.
  by step:        opinion-only items / graded items, averaged over variants.
  by credit gate: opinion-only items among credit_gate items / credit_gate items.
  by exposure:    opinion-only items / graded items, weighted by how often each variant is drawn (uniform draw within an archetype).
  generation share: variants made by the generator / all variants (fixed problems count as not generated).
Run: python3 scripts/build_report.py   (also `make report`)."""
import json, glob, os, collections
GATE = {"text": "G2", "pick": "G1", "direction": "G1", "number": "G0", "equation": "G0", "table": "G0", "reflection": "none"}
def live(v):   # branch items not under any picked option are still counted here: the report is about what a student MAY meet
    return v["board"]
def report(path):
    b = json.load(open(path)); V = b["variants"]; name = b.get("archetype_id") or os.path.basename(path).split(".")[0]
    per_step, per_cg, faces, opinion_items = [], [], collections.Counter(), {}
    for v in V:
        items = [i for i in live(v) if GATE[i["kind"]] != "none"]
        op = [i for i in items if GATE[i["kind"]] == "G2"]
        per_step.append(len(op) / len(items))
        cg = [i for i in items if i.get("credit_gate")]
        if cg: per_cg.append(sum(1 for i in cg if GATE[i["kind"]] == "G2") / len(cg))
        for i in live(v): faces[(i["face"], GATE[i["kind"]])] += 1
        for i in op: opinion_items[i["id"]] = i
    gen = sum(1 for v in V if "fixed_id" not in v) / len(V)
    return {"name": name, "n": len(V), "by_step": sum(per_step) / len(per_step), "by_credit_gate": (sum(per_cg) / len(per_cg)) if per_cg else float("nan"),
            "by_exposure": sum(per_step) / len(per_step), "generation_share": gen, "faces": faces, "opinion_items": opinion_items}
def show(r):
    print(f"\n[{r['name']}] {r['n']} variants")
    print(f"  opinion-only share   by step {r['by_step']:.2f}   by credit gate {r['by_credit_gate']:.2f}   by exposure {r['by_exposure']:.2f}")
    print(f"  generation share     {r['generation_share']:.2f}")
    tot = sum(r["faces"].values()); print("  gate mix by face     " + "  ".join(f"{f}/{g} {n/tot:.2f}" for (f, g), n in sorted(r["faces"].items())))
    print("  opinion-judged items (G2; model + second reader behind a keyword gate):")
    for i in r["opinion_items"].values(): print(f"    {i['id']:16s} face {i['face']:7s} register {i['register']:9s} credit_gate {i.get('credit_gate', False)}")
rs = [report(p) for p in sorted(glob.glob("output/*.bundle.json"))]
for r in rs: show(r)
n = sum(r["n"] for r in rs)
print(f"\n[overall] {n} variants | opinion-only by step {sum(r['by_step']*r['n'] for r in rs)/n:.2f} | generation share {sum(r['generation_share']*r['n'] for r in rs)/n:.2f}")
print("No G3 (model-only, no computer gate) item exists in any archetype.")
