# What the faculty preview writes to the Log sheet (15 Oct 2026), for the analysis lane

Every preview session is a normal session with three marks:
- `student_id` begins with `preview:` (the reviewer's name after it). Filter on that prefix to separate faculty from students;
  nothing from a preview touches the Rungs roster or the Mastery sheet's credit (preview sessions are guests for the roster).
- One row with `event_type = PREVIEW_CLIENT` per problem opened: `structured` holds the browser (user agent), screen and
  viewport sizes, light or dark theme, and the page address; `rung` the rung the reviewer chose.
- Rows with `event_type = COMMENT`: `student_text` is the reviewer's comment; `structured` holds the tutor's last reply (first
  300 characters), the problem id and kind, the rung and the page; `state` is the step the comment was made on; `session_id`,
  `attempt_id`, `variant_id` tie it to the turns around it. A comment with no open problem has those blank.

Everything else is the ordinary turn log, one row per turn: the reviewer's words (`student_text`), the tutor's reply
(`reply_text`), the step and stage, what was ticked (`newly`), wrong tries, named wrong turns (`trap_ids`), the model's
acceptance and the second reader's quote, timings, `rung`, `role`, `version`, and `SIM` rows for simulation use. The email
link in the yellow bar is a second channel and is not in the sheet; reviewers are asked to use the comment box.
