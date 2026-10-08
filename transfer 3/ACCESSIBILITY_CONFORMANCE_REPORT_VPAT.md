# CHM 212 Guarded Tutor — Accessibility Conformance Report

VPAT® 2.5 format, WCAG 2.1 edition · 7 October 2026 · prepared by the instructor-developer

## Product information

| Item | Detail |
| --- | --- |
| Product | CHM 212 Guarded Tutor (instructor-developed; not a commercial product) |
| Version evaluated | V3 prototype, build V3-0.1-20260919, Clausius-Clapeyron module |
| Scope | The student-facing web page: chat, problem panel, equation picker, pinned equations, notebook refresher card, plots and probe, settings dialog |
| Not in scope | The current classroom version (V2); the external course notebook (a Google product with its own accessibility documentation); scenario photos and videos, which are not yet produced |
| Description | A step-by-step chemistry tutor. Software checks every number, unit and equation a student enters; an AI model handles only the conversation. Text-based throughout: students type answers and equations rather than drawing them. |
| Contact | [Instructor name], Department of Chemistry, Marshall University, [email] |
| Report date | 7 October 2026 |

**Evaluation methods.** An automated scan with the axe-core accessibility engine on each screen state (opening question, problem shown, equation picker open, notebook card, settings dialog), followed by a manual review of every WCAG 2.1 Level A and AA success criterion against the page source and its behavior in a desktop browser. Keyboard-only operation was checked. Testing with a screen reader (NVDA, VoiceOver) has not yet been done; remarks say where that leaves a result uncertain.

## Applicable standards and terms

The tutor was evaluated against **WCAG 2.1 Level A and Level AA**. Level AAA was not evaluated. Revised Section 508 incorporates WCAG 2.0 AA by reference, which WCAG 2.1 AA includes.

| Term | Meaning in this report |
| --- | --- |
| Supports | The tutor meets the criterion without known defects. |
| Partially Supports | Some functionality does not meet the criterion. The remark says what, and the gap list gives the fix and date. |
| Does Not Support | Most functionality does not meet the criterion. |
| Not Applicable | The criterion does not apply to this tutor as it stands, for example audio or video, which it does not yet contain. |

**Result in one line:** of 50 criteria, 30 Support, 11 Partially Support, 0 Do Not Support, and 9 are Not Applicable. The automated scan found no violations; the 11 partial results came from the manual review.

## WCAG 2.1 Level A

| Criterion | Conformance | Remarks |
| --- | --- | --- |
| 1.1.1 Non-text Content | Partially Supports | Buttons, fields and dialogs have text names. The two plots are canvas images with no text alternative; the fitted line's equation is given in text, but the six measured points appear only in the plot. |
| 1.2.1 Audio-only and Video-only (Prerecorded) | Not Applicable | No audio or video yet. Planned scenario media will be captioned and described. |
| 1.2.2 Captions (Prerecorded) | Not Applicable | As 1.2.1. |
| 1.2.3 Audio Description or Media Alternative (Prerecorded) | Not Applicable | As 1.2.1. |
| 1.3.1 Info and Relationships | Partially Supports | Headings, labels and landmarks are marked up. Chat messages show who wrote them only by color and position, not in text a screen reader announces. The two symbol-key rows are named groups without a group role. |
| 1.3.2 Meaningful Sequence | Supports | Reading order follows the visual order. |
| 1.3.3 Sensory Characteristics | Partially Supports | Three messages refer to location only: "the problem is now on the left", "plots at left", "open on the left". |
| 1.4.1 Use of Color | Supports | Plot series differ by marker shape and line style as well as color, with a legend. |
| 1.4.2 Audio Control | Not Applicable | No audio. |
| 2.1.1 Keyboard | Supports | Every control, both dialogs and the plot probe slider work from the keyboard. Enter sends; Shift+Enter makes a new line. |
| 2.1.2 No Keyboard Trap | Supports | Dialogs close with Escape and return focus. |
| 2.1.4 Character Key Shortcuts | Supports | No single-character shortcuts. |
| 2.2.1 Timing Adjustable | Partially Supports | No timed tasks. A session expires after 6 hours without activity and cannot be extended; work then restarts with a new problem. |
| 2.2.2 Pause, Stop, Hide | Supports | No moving, blinking or auto-updating content. |
| 2.3.1 Three Flashes or Below Threshold | Supports | No flashing content. |
| 2.4.1 Bypass Blocks | Partially Supports | Header and main regions are marked, but there is no skip link, and 26 symbol keys sit before the message box in tab order. |
| 2.4.2 Page Titled | Supports | Page title names the tutor and version. |
| 2.4.3 Focus Order | Partially Supports | Focus returns to the message box after each send. When the notebook card appears, focus does not move to it; its text is announced but its buttons must be found. |
| 2.4.4 Link Purpose (In Context) | Supports | "Notebook" and "Open notebook" are clear in context. |
| 2.5.1 Pointer Gestures | Supports | No multipoint or path gestures. |
| 2.5.2 Pointer Cancellation | Supports | Native buttons act on release. |
| 2.5.3 Label in Name | Supports | Accessible names match visible labels. |
| 2.5.4 Motion Actuation | Not Applicable | No motion input. |
| 3.1.1 Language of Page | Supports | Page language is set to English. |
| 3.2.1 On Focus | Supports | Focus never changes context. |
| 3.2.2 On Input | Supports | Choosing from the problem-kind menu changes nothing until New problem is pressed. |
| 3.3.1 Error Identification | Supports | Connection, sign-in and input errors are described in text in the chat. |
| 3.3.2 Labels or Instructions | Supports | All fields are labeled; the message box states what to type. |
| 4.1.1 Parsing | Partially Supports | The "Open notebook" control places a button inside a link, which is invalid nesting. |
| 4.1.2 Name, Role, Value | Partially Supports | As 4.1.1 and 1.3.1; the plots expose no role or name. Not yet confirmed with a screen reader. |

## WCAG 2.1 Level AA

| Criterion | Conformance | Remarks |
| --- | --- | --- |
| 1.2.4 Captions (Live) | Not Applicable | No live media. |
| 1.2.5 Audio Description (Prerecorded) | Not Applicable | No video yet. Planned scenario videos will carry a text description of what is shown. |
| 1.3.4 Orientation | Supports | Works in portrait and landscape; a single-column layout is used below 820 px. |
| 1.3.5 Identify Input Purpose | Supports | The only personal field is a student ID, which has no standard input purpose. |
| 1.4.3 Contrast (Minimum) | Supports | Lowest text contrast measured 5.3:1. Disabled controls are exempt. |
| 1.4.4 Resize Text | Supports | Tested at the equivalent of 200% zoom (640 px wide): no loss of content or function. |
| 1.4.5 Images of Text | Supports | No images of text; equations are real text. |
| 1.4.10 Reflow | Partially Supports | At 320 px wide the page scrolls sideways by 21 px, and the chat area becomes very small. |
| 1.4.11 Non-text Contrast | Partially Supports | Buttons and the focus outline pass (7.8:1). Borders of the message box and text fields measure 1.4:1 against 3:1 required. |
| 1.4.12 Text Spacing | Supports | No text was clipped with increased line, letter and word spacing applied. |
| 1.4.13 Content on Hover or Focus | Partially Supports | Plot tooltips appear on hover and cannot be dismissed with Escape. |
| 2.4.5 Multiple Ways | Not Applicable | A single-page application, not a set of pages. |
| 2.4.6 Headings and Labels | Supports | Headings and labels describe their content. |
| 2.4.7 Focus Visible | Supports | A 2 px outline at 7.8:1 contrast marks the focused control. |
| 3.1.2 Language of Parts | Supports | All text is English; Greek letters are used as symbols. |
| 3.2.3 Consistent Navigation | Not Applicable | Single page. |
| 3.2.4 Consistent Identification | Supports | Controls keep the same names throughout. |
| 3.3.3 Error Suggestion | Supports | Input errors get a specific suggestion ("what are the units?", "retype with brackets"). The tutor deliberately does not supply correct answers; the criterion exempts suggestions that would defeat the purpose of the content. |
| 3.3.4 Error Prevention (Legal, Financial, Data) | Supports | Answers are checked before they count: a missing unit, an unreadable equation or a question is never counted as a wrong attempt, and the student can correct it. |
| 4.1.3 Status Messages | Supports | The chat and progress meter are live regions; new messages and progress are announced without moving focus. |

## Known gaps and remediation

Every partial result has a known fix. Ten are small page changes due 15 December 2026; the session limit is fixed on the new host by 31 January 2027.

| Gap | Criteria | Fix | Target date |
| --- | --- | --- | --- |
| Plots have no text alternative | 1.1.1, 4.1.2 | A "Show as table" button under each plot listing every point; a one-sentence summary as the plot's accessible name | 15 Dec 2026 |
| Speaker not announced in chat | 1.3.1 | Hidden "Tutor:" and "You:" labels on each message | 15 Dec 2026 |
| Symbol-key groups lack a role | 1.3.1, 4.1.2 | Add a group role | 15 Dec 2026 |
| Location-only wording | 1.3.3 | "in the Problem panel" instead of "on the left" | 15 Dec 2026 |
| No skip link; 26 keys before the message box | 2.4.1, 2.4.3 | "Skip to message box" link; move key rows after the box in tab order | 15 Dec 2026 |
| Focus not moved to the notebook card | 2.4.3 | Move focus to the card's heading when it appears | 15 Dec 2026 |
| Button nested inside a link | 4.1.1, 4.1.2 | Replace with a single link styled as a button | 15 Dec 2026 |
| Sideways scroll at 320 px | 1.4.10 | Remove the 340 px minimum column width on narrow screens | 15 Dec 2026 |
| Low-contrast field borders | 1.4.11 | Darken field borders to at least 3:1 | 15 Dec 2026 |
| Tooltips not dismissable | 1.4.13 | Close tooltips on Escape | 15 Dec 2026 |
| Session expires after 6 idle hours | 2.2.1 | Keep progress for at least 24 hours on the new host | 31 Jan 2027 |

**Testing still to do.** Screen-reader testing with NVDA (Windows) and VoiceOver (Mac and iOS), including how typed and pinned equations are read aloud, by 15 Jan 2027. Every scenario photo and video will carry alt text, captions and a text description before it reaches students. An external accessibility audit is planned in the first funded year.

## Scope and disclaimer

This report describes the V3 prototype as of 7 October 2026 and was prepared by the developer, not an independent auditor. It covers the tutor's own web page only. The course notebook is a Google product and is covered by Google's accessibility documentation. VPAT® is a registered service mark of the Information Technology Industry Council (ITI); this report follows its format but is not issued by ITI.
