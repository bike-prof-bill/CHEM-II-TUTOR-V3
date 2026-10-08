"""Independent checks on the factory. Closed forms are written separately from the engine's solver."""
import sys, math, time; sys.path.insert(0, "archetypes"); import engine, ch10_cc as A
R = 8.314; t0 = time.time(); out = engine.build(A, 100, 5000); dt = time.time() - t0; fails = 0
for v in out["variants"]:
    ok = "{" not in v["text"] and "true_substance" not in v["text"]
    for kt in [t for t in v["targets"] if t.get("is_key")]:
        ok &= all(abs(tr["value"] - kt["value"]) > 3 * kt["abs_tol"] for tr in v["traps"] if tr["for_state"] == kt["state"])
    if v["kind"] != "slope":
        k = {n: engine.to_canon(A.VARIABLES[n]["kind"], s["unit"], s["value"]) for n, s in v["givens"].items()}; u = v["kind"]
        if   u == "P2": x = k["P1"] * math.exp(-(k["dH"]/R) * (1/k["T2"] - 1/k["T1"]))
        elif u == "P1": x = k["P2"] / math.exp(-(k["dH"]/R) * (1/k["T2"] - 1/k["T1"]))
        elif u == "T2": x = 1 / (1/k["T1"] - R*math.log(k["P2"]/k["P1"])/k["dH"])
        elif u == "T1": x = 1 / (1/k["T2"] + R*math.log(k["P2"]/k["P1"])/k["dH"])
        else:           x = -R * math.log(k["P2"]/k["P1"]) / (1/k["T2"] - 1/k["T1"])
        kt = [t for t in v["targets"] if t.get("is_key")][0]
        ok &= abs(engine.from_canon(A.VARIABLES[u]["kind"], kt["unit"], x) - kt["value"]) <= 1e-4 * max(1, abs(kt["value"]))
    fails += (not ok)
n = len(out["variants"]); same = engine.build(A, 2, 7)["content_version"] == engine.build(A, 2, 7)["content_version"]
print(f"{n} variants in {dt:.2f}s | {n-fails}/{n} pass | thrown away as fortuitous: {engine.REJECTS} | same seed same output: {same}")
