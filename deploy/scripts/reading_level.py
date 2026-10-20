#!/usr/bin/env python3
"""Reading-level report on the instructor's moves file. Measures; never modifies.
Flesch-Kincaid grade from sentence length and a syllable heuristic, plus the long or rare words that drive it up.
Usage: python3 scripts/reading_level.py content_ch10_cc_moves.csv > docs/READING_LEVEL_ch10_cc_moves.csv"""
import csv, re, sys
COLS = ["ask", "switch_ask", "notebook_prompt", "return_ask", "park_text"]
def syllables(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w: return 0
    s = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee", "ye")): s -= 1
    return max(1, s)
def grade(text):
    sents = [x for x in re.split(r"[.?!]+", text) if x.strip()]
    words = re.findall(r"[A-Za-z][A-Za-z'\-]*", text)
    if not words or not sents: return 0, 0, 0, []
    syl = sum(syllables(w) for w in words)
    fk = 0.39 * len(words) / len(sents) + 11.8 * syl / len(words) - 15.59
    hard = sorted({w for w in words if syllables(w) >= 3 and w.lower() not in SIMPLE}, key=str.lower)
    return round(fk, 1), len(words), round(len(words) / len(sents), 1), hard
SIMPLE = {"temperature", "temperatures", "molecules", "molecule", "energy", "another", "different", "together", "anything", "everything", "because", "chemistry", "equation", "relation", "pressure", "pressures", "measured", "measurement", "measuring", "already", "exactly", "problem"}
rows = [["item", "column", "grade (Flesch-Kincaid)", "words", "words per sentence", "words of three syllables or more", "text"]]
for r in csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")):
    for c in COLS:
        t = (r.get(c) or "").strip()
        if not t: continue
        g, n, wps, hard = grade(t)
        rows.append([r["state"], c, g, n, wps, "; ".join(hard), t])
w = csv.writer(sys.stdout, lineterminator="\n"); w.writerows(rows)
