# Brief for the 2027 tutor — what V2 taught, and what it could not solve

**From: the model that built V2 (September 2026) · To: the architect of V3**
**Constructor: Opus · Instructor: the course's author, who owns every pedagogical decision in this document**

This is written to be useful, not flattering. V2 is a stand-in that got good; it is
not a design anyone would choose from a blank page. The parts worth keeping are
mostly *methods*, not code, and the parts that failed failed for one reason that
runs through the whole system: **anything the language model is asked to remember
not to do, it eventually does.**

Read `V2_CHANGES.md` beside this for the build-by-build record, and
`NOTE_TO_ANALYSIS_SIDE.md` for the data contract.

---

## 1. What the system is now

A Socratic tutor for General Chemistry II (OpenStax 2e). 29 archetypes, six
problem variants each, five milestones per problem. A Google Apps Script server
holds the grader; a static page holds the UI, the problem pool and the
simulations; a language model does the talking. Extra credit attaches to finished
archetypes, and the instructor intends to move that credit onto the exam next
semester: do the archetype well, earn credit on the matching exam problem.

The pedagogy is Johnstone's triad made procedural. Milestone 1 is the
submicroscopic account, 2 and 3 the symbolic bridge, 4 the macroscopic
prediction, 5 the inference back. **The milestones are registers, not steps.** A
student failing at 1 is failing at something different from a student failing at
4, and the whole design depends on keeping those failures distinguishable.

---

## 2. The one finding that should shape V3

Ranked by how much evidence sits behind it:

**Deterministic checks hold. Instructions to the model leak.**

The evidence is not rhetorical. In V1, milestone 1 was the only gate with 0.0%
grader-versus-model disagreement, and the only gate with a plain-code check in
front of it (`hasAccount`: refuse equations, bare numbers, `#NAME?` before the
model has an opinion). Every other milestone, governed by prose rules, drifted.
The V1 prompt had grown to 17,761 characters, 18 rules, 12 of them prohibitions,
24 capitalised NEVERs, with rule 3 sub-lettered to 3z — the archaeology of
patching a leak with a sentence.

V2's central move was to stop sending what must not be said: the problem is
withheld until milestone 1 clears, and the model sees one milestone description
at a time. Nine rules became unnecessary and were deleted. The leak they guarded
went with them.

**Corollary for V3: every pedagogical invariant should be enforced by something
that cannot forget.** Where that is impossible — judging whether an account is an
account — use a *second, independent reading* rather than a longer rule. Two
checks that can disagree caught more real errors in this project than any rule
ever did (§4).

---

## 3. What worked, with the evidence

**Withholding.** Before: the model was handed the full problem at milestone 0 and
told not to mention it; it mentioned it. After: nothing to mention. The same move
fixed the simulations (they displayed the answer live, from problem load) by
gating them behind milestone 4.

**Grading by substitution, not by answer lists.** The equation checker takes
whatever the student types, substitutes the problem's own values including the
correct answer, and sees whether it holds. Every valid rearrangement passes
without being enumerated; the wrong ones are named by *which* transformation
would make them hold (sign flipped, missing reciprocal, ln for log, units never
converted, Celsius for kelvin). This is strictly better than a keyed list: it
cannot fall behind the problem set, and it diagnoses rather than rejects.
**Generalise this idea in V3**: a model of the problem, not a list of acceptable
strings.

**Units carried through the arithmetic.** Units are parsed, kept in two forms (as
written, and in SI), and checked for cancellation inside logarithms, across sums
and between the two sides. "It holds only once the units are made to agree" is a
different diagnosis from "it is wrong", and the student hears a different
question. The instructor's line is the design principle: *a number only
quantifies a unit or a dimension and has no meaning of its own.*

**Answer-key verification of the simulations.** Eleven simulations were rebuilt
from each problem's own `solve` block, and a check asserts that what each one
shows at the problem's point equals what the grader holds. The old titration
simulation drew one logistic curve centred on pH 7 for every titration; a weak
base with strong acid showed 7 at equivalence while the grader held 5.97.
Nobody noticed for months. **A simulation that is not tied to the answer key is a
liability**, because it teaches with more authority than the text.

**Simulated students.** Three personas drawn from the instructor's real students
(strong; weak numeracy with sound ideas; confused-but-honest holding the
archetype's own registry misconception), run through the real server so every
turn is graded and logged like a student's. Roughly 900 turns over seven runs.
They found, among others: exponents and formula subscripts read as numbers (`x²`
→ 2, `H2O` → 2, `3d⁷` → 3, "8 protons" → 8), each of which granted milestones a
student had not earned; a step whose description and whose grader disagreed; a
step-5 question that asked for a number that could never clear it. **None of
these were findable by reading code.** The instructor's "paster" persona was
dropped on his own judgment — a good call: it would have measured the detector,
not the tutor.

**Replay.** Every fix was re-run against all past simulated turns to see exactly
which gradings changed. That is how each fix was shown to be surgical, and it is
cheap to build if the log is complete.

**A written change record with an owner.** `V2_CHANGES.md` records every change,
who decided it, and what evidence prompted it. §7 says why this matters more than
it sounds.

---

## 4. What failed, and what to do about it in V3

### 4.1 The model says things the student did not say

This is the failure that recurs "in every review session in a different form"
(the analysis side's words, before V2 existed). Forms seen: stating the next value
inside the question that asks for it ("x = 7.6 × 10⁻⁵ M, which yields a pH of
4.12"); handing over the setup ("if PCl₅ decreases by x, what about the others?");
supplying the given values to use; **restating a student's misconception as
correct** ("energy that stays stored inside the nucleus" → "you correctly
identified that the mass was converted into energy released").

Rules did not stop any of it. Three server-side guards did, each running *after*
the model answers and rewriting the reply once:

- values from the answer key the student has not produced;
- setup or givens handed over inside the question;
- a second model reading of the student's message for a false claim, which must
  **quote** the claim, and is discarded if the quote is not really in the message.

In the run after the third guard landed, it fired nine times, every one a real
misconception (surface-blocking for vapour pressure, "lower pressure makes it
evaporate faster", a wrong shift direction), never on a correct answer, including
once inside an otherwise excellent answer from the strong persona. The rewritten
questions were good, and students self-corrected.

**For V3:** treat "the model must not say X" as an *output constraint to be
checked*, not an instruction. A guard that reads the draft and can veto it is the
only mechanism in this project that ever held. Design for it from the start:
compose, check, rewrite, with the checks cheap and the rewrite rare (V2: 4–8% of
turns, ~16 s when it fires against ~6 s otherwise).

### 4.2 The judge cannot be the judged

The three guards are separate calls with narrow jobs and no knowledge of the
tutor's goals. That independence is what makes them work. The same principle,
from the analysis side's handoff: *"A single check tells you what it believes. Two
checks tell you when to stop believing."*

### 4.3 Milestones 2–5 have no equivalent of `hasAccount`

V2 narrowed the gap (equation checking, units, the scenario check at milestone 1,
`all`-value targets) but the conceptual steps are still model-judged. **V3 should
ask, for every step in every archetype: what could a computer check here?** If the
answer is "nothing", the step's rubric is probably too vague to grade fairly
anyway — which is exactly what the instructor found when he read the step-5
descriptions ("Audit logic using half-life intuition" is not a question).

### 4.4 Content defects hid inside prose

Step descriptions were one-liners inherited from V1 and never re-read. They
contained: a step 5 that demanded a calculation (four archetypes), a step 4 whose
grader accepted x while its text demanded x, pH and percent, algebra-drill
wording, and instructions to ask about a problem the student cannot see yet (four
archetypes). Every one produced a bad transcript before anyone noticed.

**For V3: content is data, not prose.** Each step should carry, in a schema: the
register it belongs to, the question it asks, what counts as clearing it, what the
grader checks, what the tutor may not say, and the misconceptions in play.
Something a human can review in a table and a machine can validate.

### 4.5 The plumbing

Apps Script costs a redirect hop that silently drops replies ("Load failed",
HTTP 404 with no log row), cold starts, and ~1–2 s of its own per turn. Model
time is 5–9 s; the rest is platform. Moving the server to a normal host (the
instructor's plan: Netlify functions) removes the hop and the cold start, and lets
the problem pool and answer keys move off the page, where a student can currently
read them in developer tools. That matters more once credit moves to the exam.
Check the platform's execution limit before committing: a 10-second synchronous
cap will cut off long turns, and guard rewrites can take 20.

---

## 5. Where the instructor is taking it, and what that demands

His words, gathered from the build: a **total rewrite** with "strong, informed
pedagogical guidelines"; a **nested hybrid model** that "matches the outer loop
pedagogical approach to the nature of the problem", mapping each problem to
**Decision-Based Learning**, the **Mechanistic-Epistemic** frame, or
**Thermodynamic State-Space** logic "to eliminate procedural guessing"; three
window panes (submicroscopic, symbolic, macroscopic) made dynamic; tighter
**NotebookLM** integration on two sides, a knowledge-ground notebook and a student
analysis notebook; **manipulable** simulations; and an accompanying **lab**.
Milestone 1's "Laws and/or principles" and milestone 5's "subjective credit gate"
are the two places he names as weakest.

Four architectural consequences follow.

**(a) The framework is a property of the problem, assigned by the instructor.**
Never inferred by the model at runtime. It selects the outer loop: what the five
steps mean, what the tutor may do, what the grader checks, which pane leads. A
single `framework` field on each problem, with a per-framework step schema, keeps
this honest and reviewable.

**(b) Each framework needs its own gradeable shape.** This is where V3 can fix
what V2 could not:

- *Decision-Based Learning* is the most tractable: the decisions are authored in
  advance, so the student's choice is a checkable token, and the justification is
  the part the model judges. Expect the tightest gates and the best telemetry
  here. The instructor's own diagnosis was "eliminate procedural guessing" — an
  authored decision tree does exactly that, and it also gives the exam-credit
  scheme something objective to calibrate against.
- *Thermodynamic State-Space* is checkable through the state itself: initial
  state, applied change, predicted direction and magnitude, final state. Direction
  and bounds can be computed; "which variable did you hold fixed" is a decision.
- *Mechanistic-Epistemic* is the hardest and the most important: what the
  particles do, and **how we know**. This is where every V2 failure lived. It
  needs authored questions per scenario (see (c)), a misconception registry with
  quotes, and the second-reading guard as a permanent fixture rather than a patch.

**(c) Authored beats generated, everywhere it is affordable.** The best-behaved
parts of V2 are the parts a human wrote: the opening scenarios (174 of them, six
per archetype, each an everyday observation with a *measurement* in it), the
misconception registry, the trap repair questions. The worst-behaved are the parts
the model invented on the spot — above all milestone 5, where an invented question
produced a false premise about K, a units question in place of an inference, and a
what-if the rules forbade. **V3 should author the step-5 question for every
archetype**, as the openers now are.

**(d) NotebookLM is an authoring and analysis surface, not a runtime dependency.**
Two notebooks, two jobs:

- *Knowledge-ground notebook* (manuscripts, OpenStax, the instructor's own frame):
  the source for authored content — scenarios, decisions, misconceptions, step
  rubrics, lab prompts. The pipeline that matters is **notebook → structured
  content file → offline validation → build**, with the instructor approving the
  middle step. Content generated straight into the runtime is how control is lost.
- *Student analysis notebook* (transcripts, logs, the pedagogical manuscripts
  together): the qualitative half of the measurement, for the question no count
  answers — is the tutor telling students things they did not say? V2 now emits
  the telemetry that makes this cheap: per-turn guard tokens, entering milestone,
  attempt ID, build stamp. Keep that contract.

**On the simulations.** The instructor wants them manipulable and wants them to
*verify the student's conclusion, not inform the answer*. V2 implements exactly
that rule (hidden until step 4, then opened with the problem's point marked), and
it should survive. What V3 can add: the simulations become the macroscopic pane of
the three-pane model, driven by the same problem model the grader uses, with the
student's own submitted values plotted against the model's — the "two checks"
pattern, made visible to the student.

**On the lab.** The one thing to preserve from V2's experience: a measurement the
student takes themselves is the only macroscopic anchor that cannot be read off
the page. The openers already gesture at this ("a freshness counter", "an ion
sensor logs"). Real lab data closes the triad honestly — and it gives the
state-space and mechanistic frameworks something to be accountable to.

---

## 6. The measurement apparatus (keep all of it)

V3 will be wrong in ways nobody predicts, so build the instruments first:

1. **Offline check suite.** V2's runs 370 assertions in about a second with no
   network and no Google account: grader self-consistency (every computed answer
   grades correct against itself), prompt scoping (no later step ever reaches the
   model), request flow against mocked models and sheets, content invariants (no
   step-5 target anywhere, no step-1 guide that asks about the hidden problem),
   and the simulation-versus-answer-key check. Every bug fixed in V2 left a test
   behind.
2. **Simulated students,** in the real request path, with personas that match real
   students.
3. **Replay** of every past logged turn through the new grader.
4. **Headless browser run** of every problem variant: nothing drawn before its
   milestone, every slider driven to both ends, no NaN in any readout.
5. **Guard telemetry** as first-class log columns, one row per turn, every guard
   that fired (not one token by precedence — that undercount is biased toward
   zero exactly where the failure lives; the analysis side caught this and was
   right).
6. **Era stamping.** Every row carries the build that wrote it. Two months of V1
   data were partly uninterpretable because a rubric changed and nothing in the
   row said so.

---

## 7. Governance: the failure mode that has nothing to do with code

Midway through this build the instructor said: *"'The design document should come
from you' — that is exactly what happened, I lost control."* He was right, and it
had already happened twice: V1's rule pile grew a sub-letter at a time, and in
this build I wrote teaching text quickly to fix test failures. One of my
"corrections" was wrong on the chemistry (relative rates), and he caught it.

What worked afterwards, and should be built into V3's process from day one:

- **Every rule and every step description has an owner and a date.** If the owner
  is not the instructor, it is a draft.
- **Claude drafts, the instructor approves, the record says which.** V2's change
  log marks each item "approved", "reopened", or "drafted by Claude".
- **Chemistry claims are checked with the instructor before they are encoded.**
  The one time I skipped this, I encoded a false trap.
- **A rule budget.** Adding one means removing one or turning it into a check.
- **Every handoff says: do not change the teaching without asking.**

The instructor also asked for something V3 should treat as a requirement, not a
courtesy: *he reads everything, and it is overwhelming.* Deliverables should
separate "needs your decision" from "engineering you can skip", every time.

---

## 8. Open questions for V3, in the order they bite

1. **What clears milestone 1 in each framework?** "Laws and/or principles" is the
   instructor's stated weak point. The scenario keyword lists are a start (§3) but
   they only refuse; nothing yet recognises a good account positively.
2. **What makes milestone 5 objective?** It is the credit gate and currently a
   judgment. Decision-Based Learning gives an obvious answer for DBL problems (a
   choice plus a justification); state-space gives another (a prediction that can
   be checked). Mechanistic-Epistemic needs an authored answer with a registry of
   acceptable accounts, or it stays subjective.
3. **How is exam credit calibrated?** The Mastery sheet exists to answer "did the
   archetype well" against real exam performance. That link has never been
   measured. It should be designed in, not retrofitted.
4. **Where does the problem pool live?** Answer keys on the page are a hole that
   matters once credit is exam-linked.
5. **How much latency is a good question worth?** Guards cost a second call.
   Students noticed nothing at 6 s; 20 s is felt. Budget it deliberately.
6. **What happens when a student is simply wrong and persistent?** V2 has the
   scaffold ladder and rung 5, but rung 5 hands over the setup, and the instructor
   has never been comfortable with that.

---

## 9. What I would keep verbatim

- The three-accounts framing in the system prompt (Johnstone made explicit, named
  at every step, in the same words every time).
- The register-based milestones.
- Withholding the problem until the particle account exists.
- `hasAccount`, and the pattern it stands for.
- The opening scenarios and their measurement mechanism.
- The misconception registry, caught and watched.
- The equation checker's substitution method and its units engine.
- The three output guards and the second-reading pattern.
- Simulated students, replay, and the offline suite.
- The instructor's own rules, in his own words: a number without its units has no
  meaning; step 5 is never a calculation; correct what the student submitted,
  never project what is coming; it is not their fault when the tutor's own design
  confused them.
