# Handoff: CHM 212 Guarded Tutor (V3)

**Written 7 October 2026**, at the close of the first design thread. Read this before anything else in the project. It holds the state of the build, every decision made and why, every decision still open, and the dates ahead.

**Owner of all teaching decisions:** the instructor (40 years teaching chemistry; Marshall University; CHM 212, General Chemistry II). The instructor reads everything and finds it overwhelming, so every deliverable separates **Needs your decision** from **Engineering**, in that order.

**Roles**
- Instructor: pedagogy, scenarios, narrative text, testing, grants.
- Fable (consulting architect): structure, the first two archetypes, the notebook window, data and analysis design, grant consulting, consultant to Opus.
- Opus (constructor): fill the remaining archetypes, clean-up. Opus drafts; the instructor approves; chemistry claims are checked with the instructor before being encoded.
- Analysis side (separate lane, historically a different model): measures, never modifies. Keep the separation.

**Standing rules**
1. No sycophancy. No praise, no padding.
2. Plain speech at the college-graduate level. Jargon only when unavoidable, then defined.
3. Two sections in every deliverable: Needs your decision (short list, with a recommendation), then Engineering (skippable).
4. Anything marked DRAFT is Fable's or Opus's placeholder and must not reach a student until the instructor approves it.
5. Do not change the teaching without asking.

---

## 1. What the tutor is, in one paragraph

A step-by-step chemistry tutor for a broad-access university course in which **the AI talks and the verifier decides**. Every number, unit, equation rearrangement and pick a student enters is checked by ordinary software against a generated answer key; the language model (Google Gemini) carries the conversation and never judges what a computer can check. The problem is hidden until the student explains, in their own words, what the particles are doing. Two wrong tries on a step send the student to the course notebook with a copy-ready prompt; they must say what they learned before continuing. A simulation built from the problem's own data opens after the value is found. Classic intelligent-tutoring verification underneath, a language model on top. In Kautz's taxonomy of neuro-symbolic systems, a loosely coupled hybrid with the symbolic part in control; in plain words for reviewers, "a hybrid tutor."

## 2. Settled vocabulary (use these words, never vary them)

| Word | Meaning |
|---|---|
| **Tutor shell** | Everything that knows no chemistry: verifier, step-map logic, page, notebook hand-off, log. Problems of any discipline hang on it. Always "tutor shell," never bare "shell." |
| **Verifier** | `Core.gs`. Reads what the student typed or picked, checks it, ticks steps, counts wrong tries, issues the notebook card, checks the AI's reply before the student sees it. |
| **Problem generator** (was "factory") | Python, run on the instructor's machine before deployment. Makes problems, keys, legitimate in-between values, and the wrong value each known mistake produces. Never runs during tutoring. |
| **Step map** (was "board") | The list of things a student must establish for one problem, plus one rule: what must come before what. Built per problem; any order the rule allows is fine. |
| **Archetype** | A problem type (Clausius-Clapeyron is one). One chemistry file each. 29 planned. |
| **Variant** | One generated problem. **Kind** = which quantity is unknown. |
| **Opener** | The numberless, equationless scenario question that starts every problem. |
| **Moves file** | The tutor's script: one row per step-map item, one column per thing the tutor may say. The instructor's narrative lives here. |
| **Trap** | A known wrong turn, recognized by the number or equation form it produces. |
| **Gate** | How a step is checked: G0 deterministic value, G1 structural pick, G2 computer gate + AI + second reader, G3 AI only. |
| **Park** | A step handed over after two wrong tries post-notebook; problem continues, attempt earns no credit. |
| **Pinned** | Kept on screen for the rest of the problem (the chosen relation, the student's rearranged equation). |
| **Register** | Johnstone's account the step is in: macro, submicro, symbolic, inference. |
| **Face** | Which of three pedagogical faces a step shows: choice (decision-based), check (state-space), why (mechanistic-epistemic). Logged per step, never per archetype. |

## 3. Pedagogy, as the instructor defined it (19 Sept)

Johnstone's triad is the one fixed thing. The three frameworks are not mutually exclusive and are not tagged by hand; every step has all three faces, logged.
- **Decision-based learning**: learning a sequence of actions; given what I know, what should I do next. Decisions are part of learning. (Sansom, Suh & Plummer 2019, J. Chem. Educ. 96, 445.)
- **Phase/state space**: a system described by a few deterministic variables forming states, with physically viable paths between them; an operation transforms one state into another. Good for equilibrium, thermodynamics, phase diagrams.
- **Mechanistic-epistemic**: cause-and-effect at the molecular level; constructing and justifying chemical knowledge is part of the activity.
- Instructor's words: "Names are only names." "Rules are for fools, do what works." The student's mind should flow naturally with the problem; each archetype can be solved for any contained variable, and that is where problem-solving begins.

Literature already gathered (see SCHOLARSHIP.txt): Bastani et al. 2025 (unguarded chatbot: practice gains, post-test losses; guarded version keeps the gain), Fan et al. 2025 (metacognitive laziness), Kestin et al. 2025, SocraticAI (Sunil & Thakkar 2025). ITS lineage: Anderson et al. 1995 (doi 10.1207/s15327809jls0402_2), Aleven et al. 2016 (doi 10.1007/s40593-015-0088-2), Mitrovic 2012 (doi 10.1007/s11257-011-9105-9), Brown & Burton 1978 (doi 10.1207/s15516709cog0202_4), Murray 1999 (tutor shells), Garcez & Lamb 2023 (doi 10.1007/s10462-023-10448-w), Kautz 2022 (doi 10.1002/aaai.12036).

## 4. State of the build (7 Oct 2026)

**V2** (Apps Script + static page, 29 archetypes, five fixed milestones): live in CHM 212 since 18 Sept 2026. Untouched by V3 work. Its lesson, confirmed in the code: deterministic checks hold, instructions to the model leak.

**V3**, one archetype complete end to end, in the zip `v3_ch10_cc`:
- `engine.py` + `archetypes/ch10_cc.py`: generator. 6 kinds (T2, P2, T1, P1, ΔHvap, slope-from-six-points). 17 liquids hung from normal boiling points (values from memory, not NIST; check). Mixed units on purpose (70% °C, 85% kJ, 70% mismatched pressure units). Key solved from the rounded givens. Traps: Celsius unconverted, kJ vs R in J, sign flipped, log for ln, pressure units mixed, slope sign kept, 1 atm or kPa in a torr line, plus equation-form traps. A variant is thrown away if any wrong method or restated given lands within three grading windows of the key (0 of 500 lost for Clausius; Raoult will lose many). Openers and variants align: each opener names its liquids; every problem is born attached to one opener. Same seed, same problems.
- `gas/Core.gs`: the verifier. Step map with ordering rule; number reader; equation checker by substitution (any valid arrangement passes; true-but-not-isolated is progress, not a wrong try; dropped sign and log-for-ln named; unbracketed denominator wrong); mandatory rearrangement for the unknown, pinned; right number typed early is kept and counts when the rearrangement lands; two-fail ladder (switch question → notebook card with no model call → return gate requiring a sentence → two more → park); second AI reader can overrule the first on the two free-text steps; leak guard rewrites once then falls back to the instructor's authored question; one log row per event with register, face, gate, tries, traps, guards, after-notebook flag, both AI verdicts, build stamp, content fingerprint.
- `gas/Code.gs`: Google wiring only (Sheet, cache, Gemini with fallback model, `setupV3`, `checkModels`).
- `gas/local_server.js`: stand-in server; runs the whole thing locally in plain mode (no Google, no AI).
- `index.html`: chat, hidden problem, Equations pick (7 unnamed equations incl. Arrhenius and van't Hoff look-alikes), pinned symbols card, notebook card (Copy / Open notebook / I'm back), two plots (ln P vs 1/T and P vs T) fed from the server, probe slider whose use is logged, Greek and math key rows, settings dialog.
- Content: `content_ch10_cc_openers.csv` (instructor's six Ch 10 scenarios with keywords, plus `liquids` and `kinds` columns), `content_ch10_cc_moves.csv` (13 rows, **all DRAFT**).
- Tests: `test_ch10_cc.py` (600 of 600 keys agree with closed-form solutions), `gas/test_core.js` (47 scripted-student checks pass, incl. all 108 variants completable and a random-equation regression).
- Install: `INSTALL_CHEAT_SHEET.md`. Route A local (Node), Route B Apps Script with Gemini. Neither yet done by the instructor; the Apps Script project for V3 is to be new and separate from V2.
- Accessibility: conformance report (VPAT 2.5 format) and EEAAP written 7 Oct; 30 Support / 11 Partially / 0 Does Not / 9 N/A; axe scan clean; eleven gaps with fixes dated 15 Dec 2026 and 31 Jan 2027. Both exported into this transfer folder.

**Not yet built, by design:** ICE (the second archetype, to prove "one engine, one chemistry file"); any other archetype; V2's units-through-arithmetic engine; V2's handed-over-setup guard and freshness note; recall mode; slope-kind "unidentified liquid" handling; scenario media; Google sign-in; LTI; Netlify; production build that refuses DRAFT rows; banned-phrase check on AI replies; exam-mode variant printing.

## 5. Decisions made (with the reason, so they are not relitigated)

| Decision | Choice | Why |
|---|---|---|
| Fixed five milestones vs step map | **Step map.** Any order the dependency rule allows. | Forced fives produced filler steps; students' minds should follow the problem. Instructor: "a new twist." |
| Problem opening | Keep V2's hidden problem until a particle account is given, for every archetype. | Best-evidenced move in V2. |
| Pedagogy tags | Per step, three faces logged, never per archetype; the CSV milestone table is only a first guess. | The CSV predates V2's fixes and reintroduces step-5s V2 removed. |
| Generator language | Python, instructor's machine. Runtime JavaScript. | Apps Script and Netlify don't run Python; latency is zero because the generator never runs live. |
| Unknowns | All five fair game, plus slope-from-data. | "Only linguistic how we state initial and final." |
| Grading windows | ±1 K on temperatures; 2% elsewhere. | Instructor. |
| Fortuitous answers | Reject the whole variant if a wrong method or restated given lands within 3 windows of the key. | 2% is only fair when wrong roads don't land near the right place. |
| Pressure units | Mismatched 70% of the time. | Instructor intent. |
| Liquids | Hang from normal boiling points; ignore the textbook's 20 °C table. | ΔHvap is tabulated at the boiling point. |
| Rearrangement | Mandatory, checked by substitution, pinned. Slope kind needs two (ΔHvap from slope; T from line). | Instructor. |
| Equation list | 7 unnamed equations incl. Arrhenius and van't Hoff look-alikes. | Recognizing the equation is part of the work (V2 rule). |
| Wrong-try ladder | 2 fails → notebook → return sentence → 2 more → park (not "finished"). Fails counted **per stage**, logged per item. | Park keeps the student learning and keeps later-stage data; a stage ladder avoids three notebook trips inside one stage. |
| What counts as a fail | Wrong answers only; not questions, unit slips, retries, unreadable or true-but-unfinished algebra. | Otherwise the notebook fires on typos and good questions. |
| Notebook prompt | A template the instructor approves, never written live by the model; digit strings matching the problem stripped; every use logged. Purely practice, never graded. | A model-written prompt is one more leak path. |
| Notebook integration | Copy-prompt plus Drive-folder sources. No API dependence. | No official write API for consumer/Workspace Gemini Notebook (renamed from NotebookLM 16 July 2026). Notebook link: notebook.google.com/notebook/6458f208-db32-496a-8088-fe0c1c6cd539 |
| Simulations | Predict first; sim opens after the value regardless of whether the prediction was right; student's own values plotted on the true curve; manipulation logged. | A wrong prediction followed by the sim is the best teaching moment. |
| Videos/images | Macroscopic event only, never molecules. Any host via `media_url`; Drive now. Seven media columns planned on the openers file (type, url, credit, license, source page, alt, captions). | A molecule video answers the submicroscopic question. |
| Media licensing | Own footage → US federal (NASA/NOAA, public domain) → CC0/PD on Commons → CC BY → CC BY-SA. Never "non-free" Wikipedia files. Credit always. | |
| Exam | Two items per archetype: one practiced scenario, one **frozen** scenario that never enters the tutor, same numbers-vary generator. Practiced minus frozen per student = transfer gap. | Direct within-student transfer measure; no control section needed. |
| The one number | Transfer gap is "is it working." Opinion-only share (fraction of steps gated by model opinion) is "can we trust the instrument," reported on every build with Generation Share beside it. First-try clear rate is the weekly pulse. | USA alone can hit zero by making everything multiple choice. |
| Led vs recall | Instructor assigns for research. "Flailing switch" (recall → led after 2 counted fails per attempt) is a lesson for the student, logged but not a study variable. | Students who trigger the switch are weaker by definition. |
| Identity | Google sign-in for December; Blackboard LTI after Netlify if an admin will register it; tutor accepts any identity source. Blackboard is only the sign-in door; Netlify stays the host. | Typed IDs cannot carry credit or research. |
| Hosting | Google Apps Script now; Netlify end of December; Edge Functions or verdict-first streaming (stream the deterministic verdict, hold the AI sentence). | Sync functions cap at 10–26 s; guards and token streaming conflict. |
| Second archetype | ICE. | Not a single equation; the real test of the tutor shell. |
| Production builds | Must refuse DRAFT rows. | Nothing unapproved ships by accident. |
| Model names | gemini-3.6-flash, fallback gemini-3.5-flash (as V2); `checkModels` verifies. | |
| Opus brief | Held until the instructor has hand-tested the archetype. | What ten minutes of testing finds will change it more than more writing. |

## 6. Decisions still open (in the order they bite)

1. **Opener-to-liquid pairing** (my first guess: rubbing alcohol = 2-propanol, perfume = ethanol, the rest water). 14 of 17 liquids have no scenario and are never asked.
2. **"Unidentified liquid"** in ΔHvap and slope kinds clashes with a named scenario. Options: the `kinds` column; a "mystery liquid" scenario; name it and accept look-up risk.
3. **Keyword strictness.** "It is more volatile" passes the computer gate on the rubbing-alcohol opener because *volatility* is a keyword. Fix: mechanism-only keywords, or require two hits. One number in `Core.gs`.
4. **Recall mode:** build it or not; if so, instructor assigns.
5. **Stage VI metacognitive question** (pick the hardest step + one sentence): include as a required, ungraded close?
6. **Trap questions, equation list, problem sentences, liquids table:** all DRAFT in `archetypes/ch10_cc.py`.
7. **The 13 moves rows:** all DRAFT. The instructor plans to replace most scenarios too.
8. Whether a Blackboard admin will register an LTI tool (asked of the Assistant Provost of Online Education, 1 Oct).
9. IRB path (consultation requested 7 Oct). Whether any CHM 212 students are under 18.
10. Google plan: Pro, with an API key. Notebook code execution availability depends on plan tier.

## 7. Dates

| Date | What |
|---|---|
| 13 Oct 2026 | Tools Competition Phase I abstract (750 words; track: Postsecondary Learning and Work, lane Teaching/Learning/Skill Development; Catalyst level unless V2 use justifies Growth). Submit by 9 Oct. Office hours 6, 8, 12 Oct. |
| 24 Nov 2026 | Phase II invitations. |
| 15 Dec 2026 | Ten accessibility fixes due (per conformance report). |
| End Dec 2026 | Netlify migration. |
| 15 Jan 2027 | Screen-reader testing (NVDA, VoiceOver). |
| 21 Jan 2027 | Phase II proposal, if invited. LTI build. |
| 31 Jan 2027 | Session persistence ≥ 24 h on new host. |
| Spring 2027 | Pilot; two archetypes × two scenarios minimum. |

## 8. Institutional facts gathered

- CHM 212 since Fall 2023: 962 enrolled; D 78, F 48, W 202 (34% DFW). Marshall's W deadline is the second-to-last week, so W is inflated and the combined figure is the honest one.
- V2 live 18 Sept 2026; V1 before it. Logs exist for adoption numbers.
- Dean letter sent (synopsis + request for support letter, IRB help, Blackboard help). Assistant Provost letter sent (LTI sign-in for research fidelity). IRB consultation letter sent.
- Security questionnaire answers: HECVAT can be self-completed (v4 unified workbook; AI section triggers); SOC 2 and PCI AOC not applicable to a faculty-built tool; data classes stored: Student/FERPA and PII, no PHI, no financial.
- Student messages go to Gemini. Confirm whether the plan's API terms exclude training use before writing it anywhere.

## 9. Known weak points, stated plainly

- Content authoring is the bottleneck, not code: ~29 archetypes × ~5 items × (ask, switch, notebook prompt, return, park, traps, options), several hundred approved strings. Cut archetypes before cutting approval.
- Option lists are hints. Write-then-pick and shared palettes reduce this; they don't remove it.
- Adoption is the likeliest failure (Khanmigo ~15% open rate). Exam-linked credit and own-lab-data problems are the levers.
- Single maintainer. A named collaborator is needed for the abstract, the IRB, and the security review.
- The units table and unit-name list in the engine are still chemistry-flavored; generalizing them is the first job before a second discipline.
- The two free-text steps (opening account, closing inference) remain opinion-judged. Future: a classifier trained on the instructor's graded answers gives them a measured error rate; needs a term of logs first.

## 10. How to start the next chat in this project

Begin with: "Read 00_HANDOFF_READ_FIRST.md. I want to work on [X]." Then the task. Expect the two-section reply format. If the task is building, the first build task is ICE in a new chemistry file with no changes to `engine.py` or `Core.gs`; if anything in the shell has to change, that is a finding to report, not a thing to do silently.
