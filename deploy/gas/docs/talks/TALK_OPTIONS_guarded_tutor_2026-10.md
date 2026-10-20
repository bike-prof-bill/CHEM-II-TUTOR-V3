# A 45-minute talk on the guarded tutor: three ways to tell it (options for the instructor, 15 Oct 2026)

Audience: chemists and non-chemists. Two live systems: V2 (in CHM 212 since 18 Sept, collecting data) and V3 (five chapter 13
scenarios and chapter 10 live behind the faculty preview page). Goal you set: a compelling account of a partnership that made a
potentially valuable free tool. Below: three organising ideas, a demo plan that works for any of them, the risks, and what I can
build once you choose. Square brackets are facts only you hold.

## The one sentence every version needs
An AI that hands students answers makes them worse on the exam they take without it; one that is held to asking, checking and
recording makes them better. (Bastani et al. 2025: the unguarded chatbot raised practice scores and lowered the later test; the
guarded one kept the gain. That is the paper to put on a slide, with the numbers.) The whole project is the engineering of that
"held to".

---

## Option A: The quest, told in order (V1 → V2 → V3)
A story with three acts and a lesson at the end of each. Easiest for a mixed audience to follow; the partnership emerges as the
cast grows.

1. **Why** (6 min). The gate course; what students get wrong (not arithmetic: which way, how far, what the particles are doing);
   the office hour that cannot scale; the Bastani result.
2. **V1 and V2: the first tutors** (10 min). What you asked a chatbot to do and what it did instead [your V1 story]. V2: 29
   archetypes, five fixed steps, the problem hidden until the particle account, the two-fail ladder to the course notebook.
   What V2 taught: "deterministic checks hold; instructions to the model leak." Show V2 live: one problem, one wrong answer, the
   notebook card. The data it is collecting now [numbers from the log].
3. **V3: the guarded tutor** (14 min). The design turned inside out: a shell that knows no chemistry and checks every number,
   every equation by substitution, every table; a chemistry file per chapter; named wrong turns, each with one authored
   question; the model allowed one sentence and overruled by a second reader; every turn logged. The workshop that built it:
   you as owner of every teaching decision; the architect; the constructor; the scenario writers; the simulation builder; the
   analysis lane that measures and never modifies; the rules (no praise, nothing marked DRAFT reaches a student, OpenStax
   first, every number re-derived by a test). Demo: the Silent Beaker or the Purple Piston end to end, including a named wrong
   turn and the log row appearing.
4. **What it is worth, and what is next** (8 min). Free, open, any institution can run a copy; the scenario workshop idea;
   chapters 14 and 15 under way; the questions the log can answer by December.
5. Questions (7 min).

Strength: clear arc, the lessons land where they were learned. Risk: act 2 can become a confession about chatbots that the
chemists have heard; keep V1 to two slides.

## Option B: Seven things a tutor must refuse to do (principle first)
Each section states a rule the tutor obeys, shows the student's view of it live, and says how it is enforced in code and by whom.
Best if you want the audience to leave able to judge any AI tutor they meet.

1. It must not give the answer, ever. (Demo: ask it to. Show the authored question that comes instead.)
2. It must not take a number on trust. (Every number, unit, equation and table checked before the AI speaks; the shell's
   verdict comes first; the model writes one sentence after.)
3. It must not flatter. (Your tone phrases, approved one by one; the struck one.)
4. It must not let a student skip the particles. (The hidden problem; a vague account refused live.)
5. It must not drift from the textbook. (OpenStax first; the constants file with a source line per value; two figures in the
   data, two in the answer; the day it asked for 1.34 × 10⁻⁵ and was told 1.8 × 10⁻¹⁰ has two figures.)
6. It must not forget anything. (The log: every turn, every wrong turn by name, the comment a reviewer leaves.)
7. It must not change the teaching without the teacher. (The DRAFT gate; the factory refusing to ship; the owner of every
   decision.)
Open (5 min) with the gate course and Bastani; close (6 min) with the partnership and what is next; questions (6 min).

Strength: memorable, portable, honest about failure modes. Risk: seven demos is too many live; do three live and show the others
as 20-second clips.

## Option C: One problem, start to finish (the demo is the talk)
Put a student's twelve minutes with one problem on the screen and pause at each step to say what is happening underneath and
who built it. The Purple Piston (a gas cylinder, a volume change, an equilibrium that does not move) suits a mixed audience:
everyone has squeezed a syringe.

- The scene and the hidden problem (why: Johnstone's triad; the particle account; V2's best-evidenced move).
- The Equations list with no names (recognising the equation is the work).
- The number steps: a wrong one typed on purpose; the named wrong turn; the one question; the second wrong try; the notebook
  card; the return.
- The direction prediction; the ICE table checked cell by cell; the quadratic's phantom root named.
- The two perturbations; the meaning; the reflection; the credit rule.
- Then the Log sheet: the twelve minutes as rows; what the analysis lane will do with a semester of them.
Open (6 min) with the course and Bastani; after the walk (25 min), the partnership (8 min): who wrote which part of what the
audience just saw, with the rules; questions (6 min).

Strength: nothing abstract; the non-chemists see a student think. Risk: a live walk of 25 minutes needs a rehearsed script and a
fallback recording; and chemists may want more breadth (one slide of the chapter map answers that).

## Recommendation
**Option A with Option C's walk as its act 3 demo.** The order gives the non-chemists the reason and the chemists the
history; one long rehearsed demo beats several short ones; the partnership story sits naturally at the point where the cast
grew. If the room is mostly chemists, Option B.

---

## The demo plan (any option)
- **V2, live:** one problem from a chapter the class is on now; type one wrong answer; show the notebook card. One minute.
  Point at the data: [n] students, [n] attempts since 18 Sept.
- **V3, live, on the faculty preview site:** your name in the box, the yellow bar visible ("not for students"), Worked rung
  for the first pass if you want the steps shown, Independent for the real walk. The Purple Piston P1a (the volume change) or
  the Silent Beaker A1 (the tracer). Have the Log sheet open in a second tab, filtered to `preview:` plus your name, and
  refresh once after the wrong turn so the audience sees the row.
- **The gallery page** for the pictures and simulations, if a chemist asks what the students see.
- **Fallbacks, in order:** (1) a second browser already signed in and on the page; (2) the local stand-in on your laptop (no
  internet needed: `node gas/local_server.js` and the page with its settings pointed at localhost); (3) a screen recording of
  the full walk, made in the rehearsal, cut into the three clips the talk needs. Record the rehearsal regardless.
- **Three things that go wrong at talks:** the hall's Wi-Fi blocks Google scripts (the recording saves you); someone asks you
  to type a rude or off-topic message (the guard answers plainly; it is a good moment, not a bad one, so plan it); a chemist
  disputes a constant (the source line is on the slide for the one you use).

## Slides (about 22 for Option A)
Title · the gate course · what students get wrong (one slide, three quotes from V2 logs) · the office hour that cannot scale ·
Bastani 2025 (the one chart) · V1 (one slide) · V2: what it does (one picture of the page) · V2: what it taught · V2 data today ·
V3: the idea in one picture (shell / chemistry file / model allowed one sentence) · the named wrong turns (a list, with one
authored question) · the log (one row explained) · the workshop: roles · the rules · a day in the build (one story: the figures
rule; or the exam scenario that was never excluded) · demo title card · what it is worth (free, open, any institution) · the
scenario workshop · chapters 14 and 15 · questions.

## What I can build once you choose
- The slide deck as a file (PowerPoint, or a Claude Doc / page you can project), text and figures from the project, your
  brackets left for you.
- A rehearsed demo script: the exact problem, the exact wrong answers to type, what the tutor will say (the deterministic
  replies are fixed; the AI sentence varies), and the fallback clips' cue points.
- A one-page handout with the site address for faculty and the Bastani citation.
- A short "how it was built" appendix for the chemists who ask: the test suites, the parity proofs, the baseline.
