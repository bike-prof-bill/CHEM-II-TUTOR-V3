# Proposed step 6 (DRAFT, awaiting the instructor's approval)

Added to the rebuild after step 3 at the instructor's request (8 Oct 2026). Four items, none in `02_REBUILD_SPEC_spine_v2.md`. Nothing here changes a decision in the handoff; it extends the spec. Runs after step 5.

## 6a. The log never loses a row

Today (`gas/Code.gs`, `append_`): if the sheet lock is not free within 3 seconds, the row is thrown away and nothing records that it happened. The analysis side cannot see the gap.

Change: a row that cannot get the lock is kept (script cache, then script properties as the fallback) and written on the next request that does get the lock; a `delayed_rows` counter is written to the sheet alongside, so the analysis side can see how many rows arrived late and when. A row is never dropped. Test: a scripted burst of 20 simultaneous turns; every row present afterwards; the counter matches.

## 6b. A student never draws the same problem twice

Today a problem is drawn at random on every "New problem". Change: the server keeps, per student id, the variant ids already served for each archetype, and draws only from the rest; when all are used, the list resets and the log records the reset. Test: 108 draws by one student cover all 108 Clausius variants with no repeat; draw 109 repeats and is logged as a reset.

## 6c. A distressed message is not answered with chemistry

Today nothing in the shell looks at a student's message for anything but chemistry. Change: a deterministic check in the first phase of every turn. If a message carries distress markers, the tutor's reply is not a chemistry question: it names a resource and the turn is logged as `DISTRESS`, with the message kept but flagged, and the problem is not advanced or penalised. The marker list, the wording of the reply, and the resources (Marshall University counseling, the 988 Suicide and Crisis Lifeline, campus safety) are the instructor's and the compliance office's to set; the mechanism is mine to build. Nothing ships with placeholder wording in this path: a DRAFT reply here would be worse than none, so this item waits for approved text before the switch is turned on.

## 6d. Warnings and outlets for federal and state requirements

Not an engineering item until the requirements are known. Candidates the instructor is collecting: FERPA (student ids and free-text messages in a Google Sheet; who can see it; retention), ADA/Section 508 (the VPAT and EEAAP in `docs/` already cover the page; the new image and simulation cards need alt text and keyboard access), West Virginia state requirements, and Marshall University policy on AI tools in instruction. Outcome of this item: a short list of what the page and the log must say or do, each traced to a rule, then built as checks like everything else.

## Order and tests

6a and 6b are small and independent; 6c waits for approved wording; 6d waits for the requirements. Each gets a regression test named for its fault, in `tests/regression/`.
