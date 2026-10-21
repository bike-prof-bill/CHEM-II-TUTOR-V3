#!/usr/bin/env python3
"""Check every cleaned OpenStax chapter in reference/openstax (docs/33 format: first line `# Chapter N`).
Checks: numbered sections present and in order; worked examples numbered 1..N with no gap; every figure link points at a file
and every figure file is linked; exercises numbered 1..N with no gap or repeat; no fi/fl ligature errors ("grst", "specigc").
Fails (exit 1) on any defect, so a chapter the explainer will quote cannot drift unnoticed."""
import os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "openstax")
LIG = re.compile(r"\b\w*(grst|igc|sufg|efgc|coefg|degn|conggur|regect|inguence|modigc|simplig|specig|classig|identig|satisg|gow)\w*\b")
OK_LIG = {"designed", "aligned", "resigned", "assigned", "signed", "foreign", "reign", "sovereign", "campaign", "benign", "malign", "consigned", "design", "designs", "designer", "designing", "redesigned", "undersigned", "glow", "glows", "glowing", "slow", "slower", "slowly", "flow", "flows", "below", "allow", "allows", "allowed", "follow", "follows", "following", "yellow", "hollow", "shallow", "swallow"}
def check(path):
    s = open(path, encoding="utf-8").read(); errs = []
    m = re.match(r"# Chapter (\d+) ", s)
    if not m: return ["first line is not '# Chapter N Title'"]
    ch = m.group(1)
    secs = [int(x) for x in re.findall(rf"^## {ch}\.(\d+) ", s, re.M)]
    if secs != list(range(1, len(secs) + 1)) or not secs: errs.append(f"sections {secs}")
    for name in ("Key Terms", "Key Equations", "Summary", "Exercises"):
        if f"\n## {name}\n" not in s: errs.append(f"no '## {name}' heading")
    ex = [int(x) for x in re.findall(rf"^### Example {ch}\.(\d+) ", s, re.M)]
    if ex != list(range(1, len(ex) + 1)): errs.append(f"examples {ex}")
    links = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", s)
    base = os.path.dirname(path)
    for l in links:
        if not os.path.exists(os.path.join(base, l)): errs.append(f"figure link to missing file {l}")
    figdir = os.path.join(base, "figures", f"ch{ch}")
    if os.path.isdir(figdir):
        used = {os.path.basename(l) for l in links}
        for f in sorted(os.listdir(figdir)):
            if f not in used and not f.startswith("."): errs.append(f"figure file not linked: {f}")
    caps = re.findall(rf"^\*\*Figure {ch}\.(\d+)\*\*", s, re.M)
    if len(caps) != len(set(caps)): errs.append("a figure caption repeats")
    exer = s.split("\n## Exercises\n", 1)[-1]
    nums = [int(x) for x in re.findall(r"^\*\*(\d+)\.\*\*", exer, re.M)]
    if nums != list(range(1, len(nums) + 1)): errs.append(f"exercises not 1..N: {len(nums)} found, max {max(nums) if nums else 0}")
    lig = sorted({w for w in LIG.findall(s) if False} | {m.group(0) for m in LIG.finditer(s) if m.group(0).lower() not in OK_LIG})
    if lig: errs.append(f"ligature suspects {lig[:10]}")
    if re.search(r"<span id=|#page-", s): errs.append("conversion anchors or dead page links remain")
    return errs, dict(sections=len(secs), examples=len(ex), figures=len(links), exercises=len(nums))
def main():
    bad = 0; n = 0
    for f in sorted(os.listdir(ROOT)):
        if not f.endswith(".md") or f == "ATTRIBUTION.md": continue
        p = os.path.join(ROOT, f)
        if not open(p, encoding="utf-8").readline().startswith("# Chapter "): continue   # older conversions are not checked
        n += 1; r = check(p)
        errs, stats = (r, {}) if isinstance(r, list) else r
        if errs: bad += 1; print(f"textbook: {f}: " + "; ".join(errs))
        else: print(f"textbook: {f}: {stats['sections']} sections, {stats['examples']} examples, {stats['figures']} figures, {stats['exercises']} exercises | ok")
    print(f"textbook: {n} cleaned chapter(s), {bad} with defects")
    sys.exit(1 if bad else 0)
if __name__ == "__main__": main()
