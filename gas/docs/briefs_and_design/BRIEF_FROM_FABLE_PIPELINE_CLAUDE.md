# Brief for the 2027 architecture — from the analysis side

**19 September 2026.** Written for Fable, who will architect the 2027 tutor, and
for Opus, who will construct it.

## What this is, and what it is not

I am the analysis side of this project. I have read every log row the tutor has
written since 3 September 2026, recovered the archetype of 73 graded completions
from a log that never recorded one, built the detectors that measure how the
tutor behaves, and audited the grader against its own answer key.

I have never modified the tutor. That separation was deliberate and I recommend it
continue: the side that measures should not be the side that builds, because the
most valuable thing measurement produces is disagreement with the builder's model
of their own system. That happened three times in this project and each time the
measurement was right.

**So this document is about evidence and about what the architecture must make
measurable.** It is not a pedagogical design. Where it touches the frameworks in
section 6, it says what each demands of the data, not how to teach it.

I have also recorded my own errors, in section 8. The next analysis side will be
tempted by the same three.

---

## 1. The one finding that transfers to everything

Across 133 turns of the V1 tutor, compliance with its own rules sorted cleanly by
what compliance required:

| Rule | What it asks of the model | Held? |
|---|---|---|
| Exactly one question mark | count a character while generating | 126 of 133 |
| No yes/no or lookup questions | recognise a question shape | 1 violation |
| No stock praise openers ("Spot on") | suppress a high-probability continuation | **24% violate** |
| Never confirm what you have not checked | notice you are confirming something unverified | **fails on the case it names verbatim** |
| Do not use later milestones | ignore material present in your own context | **the central failure** |

**Constraints on form hold. Constraints fighting a default leak. Constraints on
content that remains available do not hold at all.**

The corollary is sharper than the gradient and it is the thing I would put at the
top of the 2027 design. Here is a real reply:

> **Student:** 26.0 °C
> **Tutor:** What is the two-point form of the Clausius-Clapeyron equation that
> links pressure, temperature, and the heat of vaporization (ΔHvap)?

One question mark. No answer stated. The student does the work. It passes every
form check the prompt imposes — and it hands over the equation, its variables and
its constant inside the question asking for them.

**The failure survives inside the shape of the fix.** That is why V1's prompt grew
to eighteen rules with sub-letters running 3o through 3z: each patch constrained
form, the failure lived in content, and the next patch was needed.

The counter-example is in the same system. `hasAccount` is a twenty-line
deterministic function that refuses equations, bare numbers and the spreadsheet
error string `#NAME?` before the model has an opinion. Grader-versus-model
disagreement at milestone 1 was **0.0%** in every archetype but one. It is the
tightest gate in the system and it is not a rule. Milestones 2 through 5 had no
equivalent, and that is where every measured failure lives.

**Design rule for 2027: every gate should be a `hasAccount`, or it should not be
relied upon. If a behaviour must not occur, remove its precondition rather than
forbidding it.**

---

## 2. What V2 already fixed, and what that proves

V2 went live 18 September. It is not the 2027 system, but it is a controlled test
of the principle above and its results should inform the rebuild.

**One step at a time.** The model now receives only the step it is working toward,
never the full milestone list, and never the problem before step 1. This converts
the "do not spend a later milestone early" rule from a request into a fact.

**It cost nothing.** Measured across 179 turns: median latency 5,933 ms, and the
correlation between the length of the milestone block and latency was **r = −0.17**
— negative, i.e. noise. Only one archetype's workflow was ever sent, median 624
characters against a 17,761-character rule block. Withholding four of five steps
saves about 3% of the prompt. **The instinct that this would trade against
responsiveness was wrong, and the measurement is what settled it.**

**The server already knew enough to do it.** `previewChain` computes where a
student's numbers will land *before* the model is called and does not consult the
model's opinion. The correct step could be selected and sent in the same single
call. The expensive machinery was already built; it was being used one step too
late.

**What would have cost latency:** splitting into two calls. That roughly doubles a
5.9-second median and should be ruled out early in any 2027 design.

**V2 also added output-side guards** — a second reading that catches the draft
stating an unearned value, handing over the setup, or endorsing a false statement
in the student's message, and rewrites the reply. These are the first *measurement
from inside* of the telling problem. Simulated rate 4–8% of turns; live rate
unknown as of this writing.

Those guards are worth keeping in principle, but note what they are: a correction
layer on a model that still wants to tell. They are cheaper than the failure and
more expensive than not having the material available. **Prefer removal to
correction wherever the choice exists.**

---

## 3. The evidence base

Numbers a 2027 design can rely on. All reproducible from the exports and the
pipeline.

**Scale.** 1,625 log rows, 3–18 September. 19 students, 73 graded completions, plus
37 unattributable (not logged in) and 37 instructor testing.

**Coverage is the binding constraint on every other conclusion.** Seven of thirty
archetypes have ever been completed by a student. Chapter 11 was 1,076 of 1,492
pre-cut rows; chapter 12 was nine. The ceiling anyone reached was five distinct
archetypes. Any per-archetype claim outside ch10 and ch11 rests on one or two
attempts.

**Self-selection is the binding constraint on inference.** The instructor's read,
which I have no evidence against: the students using the tutor voluntarily are the
ones who need it least. Every statistic here is drawn from them. No conclusion of
the form "students do not need X" is safe on this data, and the 2027 design should
not assume one.

**Three gates can fail independently on the same turn.** An instructor probe typed
`23K 293K` for two temperature conversions. −10.0 °C is 263 K. The reply praised
both and advanced the milestone.

1. `numberHits` takes the last number and asks whether it matches *any* target
   value. 293 matched. **23 was never examined**, because the function is built to
   find a match, not to audit a set. Every multi-value target had this hole.
2. The stray-number check should have caught 23. It did not: `CHEM_CONSTANTS`
   contains 22.4 with a 3% window, and |23 − 22.4| = 0.6. Measured across the
   whole accepted set, **31% of integers 1–200 and 38–44% of random decimals pass
   as legitimate working.** The set was inflated by a combinatorial closure over
   ratios, products, sums and differences of the problem's inputs.
3. The rule written specifically about this exchange did not hold, and the same
   reply opened "Spot on", which a different rule bans by name.

**Design rule: where a step asks for *n* quantities, the target must know it wants
*n* and grade the set. And the set of "numbers a student could legitimately have"
should be enumerated by the solver, which knows them, not generated
combinatorially.**

**One archetype was an outlier on two independent measures.** `ch11_osmotic` was
overruled on 22.4% of turns against 3–7% elsewhere, 50% at step 5, and also had the
most stalls — 15 unfinished attempts spread across every step. Counting found it;
counting could not explain it. The tutor side later found its step-2 target was
mislabelled. **Two unrelated signals converging on one component was the tell, and
that pattern is worth building for deliberately.**

---

## 4. What the architecture must log

Not a wish list. Each item below cost this project real work by its absence, and
V2 now satisfies the first three.

1. **The state entering the turn, not only the state after.** V1 logged the
   milestone *after* a turn and the model's claim as a *count*, so measuring
   grader-versus-model required reconstructing the previous row — which required
   having already solved item 2. One column makes it a subtraction.
2. **An explicit attempt identifier.** V1 inferred attempt boundaries from
   milestone *decreases*. In 1,625 rows there were **zero** decreases, so the
   inference never once fired and was silently untested while completion counting —
   the thing grades attach to — depended on it. Worse, `reset` wrote no log row at
   all, so abandonment left no trace unless the student sent another message.
3. **A per-row build stamp.** When the `23K` case surfaced, there was no way to
   tell from the log whether the rule about it was live at that moment. It took a
   human's memory. Two days later the same stamp caught a wrong deploy on the first
   row, before it had any data behind it. Cheapest item on the list; earned its
   keep twice in four days.
4. **Resolve the unit of pedagogy in the row.** V1 logged chapter and a problem
   name that was `?` almost everywhere. Recovering the archetype for 73 graded
   completions took a two-channel matcher against the answer key and a hand review.
   It worked — zero misclassifications, zero unresolved completions — but it should
   never have been necessary.
5. **Every server decision as a token, never as prose.** A stable token can be
   grouped on. Reconstructing intent from reply text is unreliable, because the
   model only sometimes quotes what it was told.
6. **One token per event, not one token per turn.** V2's first build wrote a single
   token by precedence, which silenced the output-side guards on any turn that also
   had a grader trap or an equation error — **biased toward zero exactly in the
   struggling-student population the measurement exists to examine.** Fixed by a
   separate comma-joined column. In 2027, assume several things can be true about
   one turn and log accordingly from the start.
7. **Append-only, headers stable by name, new fields appended never inserted.** The
   V1 log went 12 → 14 → 16 → 21 columns in two weeks and nothing downstream broke,
   because everything reads by header name.

---

## 5. The framework stack multiplies state, and the logging must anticipate it

The 2027 design nests Decision-Based Learning, a thermodynamic state-space account,
and a mechanistic-epistemic frame onto Johnstone's triad, selected by situation.

I am not the right author for how those interact pedagogically. I can say what they
do to the data, and it is the single largest architectural consequence in this
document.

**V1 had one dimension of state per turn: a milestone, 1 to 5.** Everything measured
in this project is a projection of that one number — where students stall, whether
the scaffold works, how often the grader overrules the model. One dimension is why
the analysis was tractable.

**The 2027 stack has at least four**, and they are not independent:

- **Johnstone register** — macroscopic, submicroscopic, symbolic. V1's milestones
  already encoded this implicitly: step 1 submicroscopic, 2–3 symbolic, 4
  macroscopic, 5 the inference back. It was implicit, which is why "where do
  students stall" could be answered but "which register breaks them" could only be
  inferred from step number.
- **DBL decision node** — which decision the student is at, which alternatives were
  live, which they chose, and whether the choice was right *for a reason* or right
  by luck.
- **State-space position** — where the system is, which variables are fixed, which
  path was taken, whether the student treats a state function as path-dependent.
- **Epistemic move** — is the student asserting a mechanism, inferring from
  measurement, or reporting a convention.

**Log all four explicitly, per turn, as tokens.** Do not encode them positionally in
a step number and expect them to be recovered later. This project spent significant
effort recovering an archetype that was never written down; recovering an epistemic
move from reply text would be far harder and less reliable.

Two specific consequences.

**DBL is structurally the best fit for the finding in section 1.** A decision node
with enumerated alternatives is a `hasAccount`-shaped gate: the set of admissible
next moves is finite, server-side, and checkable without the model's cooperation.
A tutor that must select from an enumerated decision set cannot hand over an answer
that is not in the set. **Where the 2027 design can express a step as a decision
among known alternatives, it should — not only pedagogically but because it makes
the gate structural.**

**Framework is matched per archetype and fixed in code** (instructor, 19 Sept), and
the matching is drawn from published work on which problem types are best handled in
which frame. That makes the match a hypothesis, not an arbitrary assignment, and it
retires the comparison I first asked for. "Does DBL outperform the state-space
frame" is not a question that literature poses, and randomising archetypes across
frameworks would test something nobody claims.

The answerable question is **whether a given archetype is correctly matched**, and a
mismatch is visible without randomisation: elevated stalls, elevated overrule, or a
deeper scaffold ladder than comparable archetypes. That is the same shape as the
`ch11_osmotic` signal, which was found by exactly this kind of comparison and led to
a mislabelled target.

**The frameworks are already present in V1 and V2, unnamed.** Three examples,
verbatim from the V1 prompt and workflow:

- **Decision-Based Learning** — rule 3x: *"When a task requires choosing which data
  to use — which two trials to compare, which two points to take, which
  half-reaction to pick — never name the ones to use. Deciding which comparison
  isolates one variable IS the skill being tested."* That is a decision node with
  enumerated alternatives and the decision as the learning object.
- **State-space** — the ICE workflow: *"everything changes in stoichiometric
  proportion, so a single unknown tracks all of it. The ICE table is bookkeeping for
  that one change."* Initial and equilibrium as states, x as the path.
- **Mechanistic-epistemic** — rule 14 on step 5: *"ask what that reading licenses
  them to claim about particles they never saw, and how much confidence it
  supports."*

So the 2027 change is not new pedagogy. It is making latent structure explicit — and
the analytic payoff is direct: **explicit structure is loggable, and loggable
structure is testable.** V1 could answer "where do students stall" but never "which
register breaks them", because the register was implicit in a step number.

**This also supplies a better test than randomisation, using data that already
exists.** Seven archetypes have a V1 baseline. The same archetype before and after
its framework is named and made explicit is a within-archetype comparison, so the
framework-archetype confounding disappears entirely. `ch13_ice` under an unnamed
state-space against `ch13_ice` under an explicit one is a real experiment with a
real control, and it costs nothing but keeping the archetype identifier stable
across the rebuild — which section 7 requires anyway for the exam match.

### Where the frameworks actually sit, and why it matters more than it looks

Instructor, 19 Sept: **the numeric steps are deterministic; the pedagogies are
initiated on the other steps.**

That is the most consequential structural fact in the design, because it means the
frameworks are being installed precisely in the region where V1 had no gate at all.
On a words-only step `gradeMessage` returns `NO_KEY`, `grantMilestones` passes it
through on the model's judgment, and grader-versus-model cannot even be computed.
Step 5 is unanchored in 25 of 30 archetypes and is the credit gate. Every measured
failure in this project lives in that region.

So the frameworks are not an addition alongside the existing gates. **They are
candidates for the gate that has never existed**, and that makes them the answer to
the question left open in section 1: what is step 2–5's `hasAccount`?

A decision node with enumerated alternatives is a structural gate for a non-numeric
step. The admissible set is finite, server-side, and checkable without asking the
model to behave. That is the same shape as `hasAccount` and it is available in a
place where no numeric target can ever be.

**The design implication is direct.** Where a framework can express a words-only
step as a bounded choice — which comparison isolates the variable, which state the
system moved to, whether this claim is a mechanism or a convention — it should, and
the server should check the choice. Where it cannot, the step remains
model-gated and should be logged as such, so that the ungated surface is known
rather than assumed.

### Tagging

**Tag per step, not per archetype.** The frameworks already vary within an archetype
in V1: rule 3x fires only at the steps where trials or half-reactions are chosen,
while rule 14 makes step 5 mechanistic-epistemic in every archetype regardless of
what the earlier steps do. A five-slot tag per archetype costs the same to build and
matches the structure that is already there.

Numeric steps take a `deterministic` tag rather than a framework. This is not
bookkeeping: it makes the ungated surface countable. "What fraction of steps in this
course are gated only by the model's judgment" is currently unanswerable and should
not be.

**Write the tag into the log row as a token.** If tags live in configuration rather
than in code, a re-tag may not move the build stamp, and the instrument will have
changed invisibly. That is exactly the failure that made rule 3r undatable against
the `23K` case. One token per row and a re-tag is self-documenting wherever the tag
lives.

### Re-tagging protocol

Being able to change a tag and observe the effect is the most valuable experimental
capability in this design. It has one hazard, and the instructor has already chosen
the clean form.

**Pre-register.** Decide in advance which archetype, which step, which alternative
framework, and for how long. Write it down before the switch.

The reason is `ch11_osmotic`. It had a 22% overrule rate, the most stalls of any
archetype, and a mislabelled step-2 target that has since been fixed. Re-tag it
today and any improvement is unattributable between the tag and the fix. **An
archetype re-tagged because it looked bad will look better afterwards whether or not
the tag did anything** — regression to the mean is indistinguishable from effect.

The clean protocol: choose an archetype where the literature is genuinely ambiguous
about the frame, not one that is performing badly. Tag it one way for a defined
period, switch, compare within archetype. Exploratory re-tags are still worth doing —
exploration finds things — but they must be labelled exploratory in the log, and no
conclusion should cross that label.

**Log the tag as a token regardless.**---

## 6. The two notebooks

The design calls for a knowledge-ground notebook for students and an analysis
notebook for the instructor. They have opposite requirements and should not share
an architecture.

### (a) The knowledge-ground notebook

The round trip is sound: the tutor diagnoses a gap, points the student at the
notebook with a focused question, the student builds something, and returns to have
it interrogated. That makes the tutor an examiner rather than a source, which is
the right role.

**Looking things up is legitimate work, and the existing design already says so.**
The Equations list carries no names and no chapters, precisely so that recognising
the right equation is part of the task; the Data Appendix makes students find their
own constants; V1's rule 12 has the student locate the equation rather than be given
it. A grounded notebook is continuous with that, not a breach of it. Students have
had books for as long as there has been chemistry, and treating information access
as leakage would be both wrong and unteachable.

The distinction that matters is not availability but **specificity**. "What is
Raoult's law" is looking something up. "Work this problem" is not, and the line
between them is whether the corpus contains worked instances of the problems in the
pool.

Three requirements follow, and they are narrower than they first appear.

1. **The corpus must be disjoint from the answer key.** Principles, general
   derivations, the textbook, worked examples of *other* problems — all fine, all
   how a student would use a book. Worked instances of the problems in the pool are
   the single exclusion, and it is the only one needed.
2. **Its contents should be enumerable by the tutor side**, so the equivalent of
   `unearnedValues` can be computed against what the student could legitimately have
   obtained. Right now that function checks against the problem's own values. With a
   notebook in the loop, "what a student could reasonably know" is a larger set — and
   in most cases it should simply be treated as known, which is the point of having
   a library.
3. **Round trips should be logged as events.** A student returning with a synthesis
   is a different kind of turn from a student answering a question, and the
   epistemic status of what they say is different. If that is invisible in the log,
   every measure of "did the student produce this themselves" is corrupted.

There is also an opportunity here. The exam-credit scheme's known exploit — a
student pasting from another tab shows flat perfection where a real learner shows a
curve — becomes tractable if notebook interactions are logged. The signature of a
learner using the notebook well is *distinguishable* from a paster; the signature of
a paster using an unlogged notebook is not.

### (b) The analysis notebook

This exists and works. Transcripts are exported one file per archetype per era, each
turn annotated with the grader state in force — entering and leaving step, scaffold
rung, turn kind, trap diagnosed, whether the grader overruled the model. Without
that context a reader cannot distinguish a tutor that correctly withheld credit from
one that was simply wrong.

The division that matters: **if the answer is a number, it comes from the pipeline.
If the answer is a sentence, it comes from the notebook.** Language models produce
confident wrong totals; never ask this one "how many". The counting layer is
reproducible by anyone with the CSV, which is the point — the instructor does not
have to trust the analyst to check the gradebook.

**Two things the 2027 design should make automatic**, both currently manual: the
transcript export should be a native output of the tutor rather than a
reconstruction by the pipeline, and it should carry the four state dimensions from
section 5 rather than one.

---

## 7. Simulations, the Lab, and the thing this project has never had

**Simulations.** V2 opens them only after step 4, built from each problem's own
data. That ordering is correct and follows directly from section 1: a manipulable
simulation available at step 1 is the problem's answer in visual form. Tighter
manipulation in 2027 raises the stakes — a slider that reveals the relationship
before the student has articulated it has handed over step 1 and cannot be
instructed not to. **Gate simulation state the way step content is gated, and log
which manipulations the student actually performed.** Those manipulations are
evidence about reasoning and are currently invisible.

**The Lab, and the outcome measure.** This is the most important gap in the whole
project and the 2027 design is the first chance to close it.

**Everything measured so far is process, not outcome.** Stalls, rungs, overrule
rates, guard firings, completions — all of it describes what happened inside the
tutor. **Not one number in this project is evidence that any student learned
anything.** I have been careful to never imply otherwise, and the next analysis side
should be equally careful.

The instructor's plan for extra credit — do the archetype well, get credit on the
matching exam problem — creates the first real outcome variable this project has
ever had. Matched at the archetype level, it makes possible the question everything
else has only approached: does doing well here predict doing well there, and does
the tutor's own competence measure (`Clean run`: reached step 5 without needing the
setup handed over) actually predict it?

**Design requirement: the archetype identifier used in the tutor must be the same
identifier used on the exam item and in the Lab.** If those are three vocabularies
requiring a mapping table, the mapping will rot and the outcome measure will be
lost. This project already spent real effort recovering an identifier that was never
written down.

A caution on the same scheme: it has a known exploit, and attaching credit to a
measure changes the behaviour being measured. The paster hypothesis is sound but
currently untestable — self-reported student IDs and thin per-archetype data. Build
the logging that would make it testable *before* credit depends on it, not after.

---

## 8. What this analysis got wrong

Recorded because the failure modes recur and the next analyst will meet all three.

**Ran current definitions against old data.** 392 of 397 candidates from the
later-milestone detector were scored against step definitions that did not exist
when those replies were written — the equation-finding step had moved between steps
in the interim. All 392 were discarded. The handoff I was working from warns about
exactly this in its own third section. I made the error anyway. **Any detector that
reads its own definitions out of the code must record which build of the code it
read, and refuse to score rows from a different build.**

**Asserted a problem that dissolved on inspection.** I claimed the grader was
feeding the model values the student never wrote, and designed a filter around it.
On tracing the code: the flagged value comes from the student's own message, trap
text is scrubbed of numerics, and the offline suite enforces both. What caught it
was sending the claim to the tutor side as a question rather than as a finding.
**The lane separation is what made that recoverable.**

**Mistook a naming convention for a wrong deploy.** I compared the build stamp in a
file I had been sent against the stamp in the deployed row, and reported a mismatch.
The two files were the same build with different labels, one per project. I inferred
from a convention I had half-guessed. **Build stamps should encode project and
version in documented fields, not in a letter suffix whose meaning must be
reconstructed.**

---

## 9. What exists and is handed over

**Pipeline** — clean, dedupe, ID corrections, attempt segmentation, two-channel
archetype recovery, credit ledgers, spreadsheet exports, later-milestone detector,
transcript exporter, and an Apps Script weekly export that runs unattended. All
read by header name; the log has changed shape four times without breaking.

**Frozen V1 record** — 73 completions, per archetype, every one resolved, zero known
misclassifications, provenance hashed. Grades rest on it.

**Reports** — the observations document (the three-gate failure, the compliance
gradient, the latency measurement), the replicate test protocol, the detector
report, the backfill findings, the notebook guide, the logging requirements, and the
analysis handoff.

**Reading corpus** — transcripts by archetype and era, each turn annotated with
grader state.

---

## 10. The one thing I would carry forward above the rest

The two most useful findings in this project both came from building a second,
independent check and watching the two disagree.

Archetype recovery used numeric fingerprints *and* vocabulary. They disagreed on two
completed attempts; the vocabulary channel was right, and two students would
otherwise have been credited for the wrong archetype.

The grader-versus-model column exists for the same reason — two judgments of the
same thing, and the gap between them is the signal. It is what surfaced the osmotic
anomaly, which surfaced the mislabelled target, which was the open question nobody
had been able to answer by counting.

A single check tells you what it believes. Two checks tell you when to stop
believing.

**For 2027: wherever a judgment matters, arrange for a second one with an unrelated
failure mode, and log both.** Not for redundancy. For the disagreement.
