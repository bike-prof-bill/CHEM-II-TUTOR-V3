# The 2027 tutor, in plain English

**For:** the instructor · **Status:** first draft, 19 Sept 2026. Nothing is settled until you rule on Section 1.

---

## 1. What I need you to decide

Thirteen items. Each has my recommendation. "Agree" is a complete answer.

1. **How every problem opens.** V2 hides the problem until the student has said what the particles are doing. Your newer milestone table drops that for many topics and starts with "pull the data out of the problem." *Recommend: keep V2's opening everywhere.* It is the best-proven thing you have.
2. **Always five steps?** *Recommend: four to six, whatever the topic honestly needs.* Forcing five created filler steps. The last step is always the one that earns credit.
3. **Typing versus picking.** A computer can check a pick but picking is easier than recalling. A computer cannot check a typed explanation. *Recommend: the student types first, then picks.* The pick decides whether they move on. The typing is saved and used later. When the two disagree, that is the most interesting thing in your data.
4. **What happens when a student is stuck.** *Recommend:* first wrong answer → the tutor re-asks from a different angle (particles, symbols, or measurement, whichever they were not using). Second wrong answer → they get a prompt to run in the course notebook. The old ladder, including the rung that handed over the setup, is retired.
5. **What counts as a wrong answer.** *Recommend: only genuine wrong attempts.* Asking a question, forgetting a unit on a correct number, or a dropped connection do not count.
6. **Stuck again after the notebook.** *Recommend: "park" the step.* Show the setup, record that this attempt earned no credit, flag it for you, and let them start a fresh version.
7. **Who writes the notebook prompt.** *Recommend: you do, once per step, as a fill-in form.* If the AI writes it on the spot, it can slip the answer in. A form cannot, and it is instant.
8. **The credit step.** Today the AI alone decides whether a student earns credit. *Recommend: never again.* Credit needs a checkable pick plus a written explanation that two separate AI readers must agree on.
9. **The one number.** See Section 3. *Recommend: exam performance without the tool, compared within each student.*
10. **Simulations.** *Recommend: the student must commit to a prediction before the simulation opens.* Then it shows the true curve, their own numbers on it, and their prediction.
11. **Which three topics to build first.** *Recommend:* equilibrium tables (ICE), method of initial rates, and either freezing/boiling point change or titration. One for each teaching approach. Swap toward any that match a lab.
12. **Student login.** Students now type an ID. *Recommend: school Google sign-in* before any exam credit depends on this.
13. **A real experiment (optional).** Randomly give each student a set of topics that carry credit. That turns your main number from "a pattern" into "a result." Needs ethics-board approval.

**Things only you can supply:**
- Your own three-sentence definition of each teaching approach (decision-based, state-space, mechanistic-epistemic). Decision-based learning has published backing. The other two are your ideas, and a journal will want them defined so someone else could apply them.
- The lab list: which experiments, in what order, what students measure.
- Which term this launches, and how many students.
- Whether your college gives students Google accounts that can open NotebookLM. (Google seems to be renaming it "Gemini Notebook." Only the business edition lets software talk to it directly.)
- Whether an ethics board is involved.
- Files mentioned in the handoffs that I did not get: the V2 change record, the note to the analysis side, the test suite, the simulated students, your model answers for the opening questions. I also did not find a separate "two chapters of initial questions" file. The only opening questions I saw are the ones inside the server code.

---

## 2. The plan in one page

**The lesson from V2:** when the AI is told not to do something, it eventually does it. When a plain computer check stands in the way, it cannot. Both earlier reports say this and the code confirms it.

**So V3 asks one thing of every step in every problem: what could a computer check here?**

Your three teaching approaches turn out to be the answer. Each one supplies something checkable for steps that never had a check:

| Approach | What the student does | What the computer checks |
|---|---|---|
| Decision-based | Chooses among options you wrote (which trials to compare, which equation fits) | Whether the choice is in the correct set |
| State-space | Fills in a before / change / after table; predicts a direction | Each cell; whether the direction is right; whether the change is physically possible |
| Mechanistic | Selects which particles are present; links a claim to the measurement that supports it; then explains | The selection and the link. The explanation gets two AI readers |
| Plain calculation | Types a number with units | The number and the units, as V2 already does |

**Every step gets three labels**, and all three are written into every line of the log:
- which view of chemistry it is in (what you can measure, what the particles do, the symbols, or the final inference)
- which teaching approach governs it
- how it is checked (by computer, by computer plus AI, or by AI alone)

Your newer milestone table labels a whole topic with one approach. This labels each step. A titration problem can start mechanistic, turn decision-based, then become calculation.

**The AI's job shrinks.** It no longer judges picks or numbers. It no longer invents questions you could have written. It phrases things, acknowledges what the student said, and handles unexpected questions. If it still says something it should not, it gets one rewrite. If the rewrite also fails, the student simply sees your pre-written question. So a bad AI sentence never has to reach a student.

**The answer key leaves the web page.** Right now every answer sits in the page source where a curious student can read it, and the simulations are hidden only by a flag in the browser. In V3 the server holds the problems and releases each piece only when it has been earned. This happens in the first build, not after the move to Netlify.

**The notebooks.**
- *Student notebook:* after two wrong tries, a card appears with a ready prompt, a copy button, a link, and an "I'm back" button. The prompt asks for the idea and an example using a *different* reaction. When they return, they must say what they learned before continuing. The notebook holds the textbook, lab manual, and your notes, and never worked solutions to the tutor's own problems. A script checks that.
- *Your analysis notebook:* each week the tutor writes labelled transcripts into a Drive folder that the notebook reads. Names are replaced with codes first. Rule: **numbers come from the spreadsheet, sentences come from the notebook.** Never ask the notebook "how many." The "heat map" of trouble spots is a spreadsheet tab.
- There is no supported way for software to push data into the ordinary notebook. Copy-and-paste and Drive folders are the dependable routes, so that is what the design uses.

**Simulations.** One set of chemistry equations drives both the grader and the picture, so they cannot disagree (V1's titration curve was wrong for months and nobody noticed). Three linked panels: particles, symbols, instrument. The student's own numbers are drawn on the true curve. What they drag and for how long is logged. The titration widget you sent has a good lab feel but is tied to Google's preview system and to one fixed acid. Keep the look; rebuild the insides.

**Lab.** Waiting on your lab list. The main idea: a problem version where the student types in *their own* measurements and the tutor works out the right answer from those. Their data points appear on the simulation. That is the one kind of problem another chatbot tab cannot help with.

**Platform.** Build in Google first, with the chemistry brain written as a separate piece that does not care where it runs. Moving to Netlify then means swapping the wiring, not rewriting. One correction to the earlier blueprint: you cannot both stream the AI's words instantly *and* check them before the student sees them. The fix is to show the computer's verdict at once ("263 K, checked") and hold the AI's sentence for the second or two the checks take.

**Build order.** Decisions → three pilot topics written out in a spreadsheet you approve → rebuild V2's core cleanly → add the new checks → add the stuck-student path and student notebook → simulations → analysis exports → live pilot with real students → remaining 26 topics → Netlify. The lab runs alongside once I have the list. Each stage ends with a short decision list for you.

---

## 3. "What is the one number?"

You proposed the share of the course that is checked only by the AI's opinion. It is a good number and it should be reported on every build. **It is not the number that tells you this is working.**

Reason: it describes the tool, not the students. You could drive it to zero by making everything multiple choice. The course would be perfectly checked and would teach recognition instead of reasoning.

What it *does* tell you is how far to trust every other number. So it comes first, as a quality rating on the instrument.

Three numbers, three jobs:

| Number | Question it answers | How |
|---|---|---|
| **Transfer gap** | Did they learn? | On the exam, with no tutor: each student's score on topics they completed cleanly, minus their score on topics they did not. Each student is their own comparison, so "only strong students use it" mostly cancels out. |
| **Opinion-only share** | Can we trust our data? | Share of steps checked by AI opinion alone. Reported overall, **and for credit steps alone**, and by where students actually spend their turns. |
| **First-try rate** | How is this week going? | Share of checked steps passed on the first attempt without the notebook. |

Where V2 stands today, roughly: over half of all steps are opinion-only, and **every credit step is.** That second figure is the one to fix first.

A companion number guards against cheating the metric: the share of steps where the student must *produce* something rather than pick. If opinion-only falls because producing fell, that is not progress.

Honest limit: the transfer gap needs enough students and enough matched exam questions. One term may not be enough. Keep topic names identical across the tutor, the exams, and the lab so terms can be pooled.

---

## 4. Where I disagree with the documents you sent

- **Your milestone table is older than V2's fixes.** It brings back two final steps V2 removed on purpose (a back-substitution check, and "audit logic using half-life intuition," which the builder's report calls "not a question"). Treat V2's current step text as the starting point, and the table as a first guess at which approach fits which topic.
- **Some labels are forced.** "Thermodynamic driving force: convert to Kelvin" is a unit conversion.
- **The reference list needs work before a reviewer sees it.** One review article is cited on every row. The source given for the mechanistic approach is a study of simulations. I have named some leads in the engineering document for you to check; I have not verified them and you should not cite them on my word.
- **The Gemini blueprint** mixes up "which teaching approach" with "which view of chemistry"; has the AI write the notebook prompt; promises a live heat map inside the notebook; and promises instant streaming alongside pre-checking. The last two cannot be done as described.

---

## 5. Biggest risks

1. **Your time.** Several hundred short pieces of teaching text need your approval. If that is too much, build fewer topics. Do not skip the approval.
2. **Option lists are hints.** Showing choices narrows the field. Type-first helps; it does not cure it.
3. **Students may not use it.** The research you collected says this is the likeliest failure. Exam-linked credit and own-lab-data problems are the two levers here. Neither is proven.
4. **The notebook product is shifting** (renaming, access rules). The prompt also works against the textbook. The "tell me what you learned" step on return is the part that matters.
