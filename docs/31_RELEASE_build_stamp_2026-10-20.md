# Release: the build stamp (20 Oct 2026)

The alive reply and every log row carried `V3-0.1-20260919-01` since 19 Sept. The stamp now lives in one file, `BUILD_STAMP`, at
the top of the repository; `run.py` writes it into `gas/Shell_version.gs`. Each release sets that file; nothing else changes.
No teaching change. Shell version unchanged (a819f89c).

## 1. Repository
Drop `CURRENT_repository_copy_into_CHEM-II-TUTOR-V3.zip` (Replace), then `make test`. The line to look for:
`shell version a819f89c (Code.gs f3f8ed41) | build stamp V3-0.1-20261020-01`

## 2. Apps Script: two files, both replace
| file | new or replace |
|---|---|
| Code | replace |
| Shell_version | replace |

Paste both before saving either, then New version (not a new deployment). Reload /exec. Expect `"build":"V3-0.1-20261020-01"`,
shell_expected and shell_actual `a819f89c`, and 23 archetypes (if you have pasted the two missing ones; otherwise 21).
If the reply shows `"build":"Shell_version not pasted"`, Shell_version.gs is the old one.

## 3. Netlify
No change.
