# Correspondence drafted and advice given in the first thread

Kept so the project remembers what was said to whom. Letters are summarized, not reproduced; the instructor has the sent versions.

## Letters sent or drafted

| Date | To | Content | Status |
| --- | --- | --- | --- |
| ~1 Oct 2026 | Dean | Synopsis of the tutor; CHM 212 figures (962 enrolled since Fall 2023, one in three D/F/W); each archetype opens with a numberless, equationless scenario with photo or video; request for a support letter, IRB help, Blackboard help. | Sent |
| 1 Oct 2026 | Assistant Provost of Online Education and Certification | Request for Blackboard LTI 1.3 sign-in, framed as research fidelity (sessions must be tied to enrolled, consenting students for IRB and exam matching). Netlify stays the host; Blackboard is only the sign-in door. Tutor would receive university ID and course role only, stored separately from learning data. Gradebook passback dropped. Note: an anonymous Blackboard ID alone cannot be matched to exam scores; one real identifier is needed, kept in a separate key sheet. | Sent |
| 7 Oct 2026 | IRB office | Request for a pre-submission consultation. Seven questions: review level (possible exempt category for normal educational practice), instructor-as-researcher consent handling (colleague collects consent; instructor blind until grades post), FERPA for exam scores + tutor records, sending student text to Gemini, use of sessions already logged, CITI training and timeline, whether the funder needs approval in hand by January. Also to ask: any students under 18. | Sent |
| 7 Oct 2026 | Security review form | Data stored: Student/FERPA and PII checked; PHI, financial, confidential unchecked. Comment: students type free-text chemistry answers and could type personal details; messages are sent to Google's Gemini service. | Submitted |

## Security and accessibility review: what exists

- HECVAT: none yet; can be self-completed (version 4 unified workbook; a 32-question AI section triggers when AI is declared). Ask first whether Marshall has a separate path for faculty-built tools.
- SOC 2: not applicable to a faculty-built tool; Google and Netlify publish their own reports.
- PCI AOC: not applicable; no payments.
- VPAT-format conformance report and EEAAP: written 7 Oct 2026; in this folder.
- Pending questions they will ask: who maintains the tool if the instructor is unavailable; whether Gemini API terms exclude training on student text.

## Media licensing advice given

- Wikipedia images: check each file's own license page. Public domain, CC0, CC BY: use with credit. CC BY-SA: use with credit; altered images must carry the same license. GFDL-only: skip. "Non-free" files: never.
- US federal agency media (NASA, NOAA, USGS, NIH, NIST, EPA): public domain in the US; watch for contractor or partner credits, third-party images on agency pages, agency logos, implied endorsement, identifiable people. State agencies differ.
- NIST Standard Reference Data is the exception: facts are free, wholesale copying is not.
- Ranking for the tutor: own footage → federal → CC0/PD on Commons → CC BY → CC BY-SA.
- Openers file media columns: `media_type`, `media_url` (own hosted copy, direct file link), `media_credit` (shown under image), `media_license` (code with version), `media_source_page` (proof, not shown), `media_alt` (macroscopic scene only, never molecules), `media_captions_url` (video).

## Tools Competition 2027 (Phase I)

- Track: Navigating Postsecondary Learning and Work; lane: Teaching, Learning & Skill Development. US only. Broad-access institutions emphasized.
- Six criteria: novelty; impact on learning; equity; demand; learning engineering; scale.
- Phase I abstract 750 words, due 13 Oct 2026; invitations 24 Nov; Phase II 21 Jan 2027; finalists March; pitches April; winners June. Catalyst $50k (no users required), Growth $150k (active users), Transform $300k (10,000+ users).
- Last cycle: 350+ submissions in this track, 7 winners, 2 of them teaching tools. Odds are a few percent; the abstract is still worth writing because it becomes the framing for every later proposal.
- Abstract budget agreed (750): need 110; what's new 160; student experience 130; learning science and data 150; equity and safeguarding 80; scale 60; team and funds 60.
- Still needed from the instructor to draft it: institution description, V2 usage numbers from logs, collaborator name and role, prize level.
- Their blog priorities: AI that complements thinking (predict, observe, explain); safeguarding by design (minimal data, PII separate, human review of AI-generated content, AI output labeled); public goods such as datasets, benchmarks and evaluation frameworks (the opinion-only share as a proposed field benchmark).

## Gemini Notebook facts (as of July–Oct 2026)

- NotebookLM renamed Gemini Notebook on 16 July 2026; lives at notebook.google.com; old links forward.
- Each notebook gets a secure cloud computer for code execution; live for AI Ultra and Workspace business, rolling to Pro.
- Notebook names, sources and custom instructions sync with the Gemini app. Custom instructions can tell the student notebook "explain, never solve."
- No official write API for the consumer/Workspace edition; only Enterprise has one. Unofficial clients exist and should not be built on.
- Course notebook: notebook.google.com/notebook/6458f208-db32-496a-8088-fe0c1c6cd539. Instructor is on Google AI Pro with an API key.
