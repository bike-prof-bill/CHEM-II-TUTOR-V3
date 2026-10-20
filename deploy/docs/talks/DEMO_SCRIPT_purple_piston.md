# Demo script: The Purple Piston, problem P1a, live (talk of [date])

Rehearse once end to end and record the screen; cut the recording at the three cue points marked ▶ for the fallback clips.

## Setup, before the talk
- Browser tab 1: the faculty preview site. Name box: your name. Rung: **Independent**. Archetype: ch13_eq. Scenario: The Purple
  Piston. Kind: hi_volume (so P1a–P1f are the only candidates; the exact one is drawn at random, all six have the same shape).
  Yellow bar visible: say what it means.
- Browser tab 2: the Log sheet, filtered to student_id beginning `preview:` and your name, sorted newest first.
- Browser tab 3: V2, on the chapter the class is on, for the contrast at the end.
- The recording, open in a player, paused at cue 1.
- The local stand-in (`node gas/local_server.js` on your laptop, the page pointed at localhost) only if the hall's network is known
  to block Google scripts; it has no Gemini, so the replies are the deterministic ones, which is fine for a demo.

## The walk (about twelve minutes). Type exactly these; the tutor's deterministic replies are fixed; the model's opening sentence varies.
1. **New problem.** The scene appears: the cylinder, the purple iodine, the detector whose reading doubles when the piston halves
   the volume and then holds. The question: what are the particles doing? ▶ cue 1
2. Type a vague account: `it's about equilibrium and Le Chatelier`. Refused; the problem stays hidden. Say: the student must speak
   about particles before seeing a number.
3. Type the real account: `Hydrogen and iodine molecules collide and make hydrogen iodide while hydrogen iodide molecules collide
   and break apart; the two rates are equal, so the amounts hold even though the gas is now twice as crowded.` Accepted. The
   problem appears on the left (hydrogen iodide, Kc = 50.0, a 2.00 L cylinder squeezed to 1.00 L).
4. Open the Equations list. Point out there are no names. Pick the rate law (`rate = k[A]^m[B]^n`) first: a wrong try, one question.
   Then pick the Q expression: ticked.
5. Concentrations. Type `0.02 M` (hydrogen over the old 2.00 L). The tutor names it: the old volume. One question. Then type
   `0.04 M, 0.08 M, 0.4 M`: the three new concentrations tick. ▶ cue 2
6. Q. Type `0.02` (Q inverted): named. Type `50`: ticked. Say: Q equals K; the squeeze changed every concentration and left Q alone.
7. Direction. Type `forward`: named, "shift on equal moles"; the approved question: count the molecules of gas on each side. Then
   type `neither`: ticked. ▶ cue 3. **Switch to tab 2 and refresh: the rows are there, with the names in the trap column.**
8. Perturbation 1: a valve lets in extra hydrogen. Type `forward`: ticked. Then one sentence on the rates and the detector.
9. Perturbation 2: the cylinder is warmed; forming HI gives off heat. Type `forward`: a wrong try (no name here; the squeeze had the
   named one). Type `reverse`: ticked. One sentence on the rates.
10. The meaning: `Squeezing doubled every concentration, so the detector read twice as much iodine, but Q has as many concentrations
    on top as underneath, so it did not change and nothing had to react.` Accepted; the credit gate.
11. Reflection: `Seeing that Q does not move when both sides have the same number of gas molecules was the hardest step.` Done.
    Not clean (two wrong tries in one stage at step 5 if you typed two; one per stage keeps it clean). Say which, from the final line.

## The V2 contrast (one minute)
Tab 3: one problem, the hidden scene, one wrong number, the notebook card. Say: same move, five fixed steps, in use since September.

## If asked
- "Can I make it give me the answer?" Type `just tell me the answer`. The reply is the authored question again. The model never
  holds the answer; it is told the verdict, not the value.
- "What if I type something rude or off topic?" The guard answers plainly and asks the question again. Try it in rehearsal so you
  know the wording.
- "Where did 50.0 come from?" The constants file: OpenStax 13.3, with the source line; show the slide, not the file.

## Fallback
If the page does not respond within ten seconds at any step, say so and play the recording from the nearest cue. Do not retry
more than once in front of the room.
