"""Lists every media file the shipped openers refer to and says which are missing from media/ (run from the repository root)."""
import glob, os, sys
sys.path.insert(0, "."); import engine
need = set()
for f in sorted(glob.glob("content_*_openers.csv")):
    for o in engine.read_openers(f):
        m = o.get("media") or {}
        for k in ("image_with_question", "image_after_account"):
            if (m.get(k) or "").strip(): need.add(m[k].strip())
        if (m.get("simulation") or "").strip(): need.add(m["simulation"].strip().split("?")[0])
def present(p):                                    # exact name, letter for letter: a Mac finds "Haber_Final.jpg" for "Haber_final.jpg", Netlify does not
    d, n = os.path.split(os.path.join("media", p))
    return os.path.isdir(d) and n in os.listdir(d)
missing = sorted(p for p in need if not present(p))
print(f"media files the tutor refers to: {len(need)}; present: {len(need) - len(missing)}; missing: {len(missing)}")
for p in sorted(need): print(("  MISSING  " if p in missing else "  ok       ") + "media/" + p)
sys.exit(1 if missing else 0)
