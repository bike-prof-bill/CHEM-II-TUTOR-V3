# Updating the repository from a step zip

Mac, GitHub Desktop, Safari. Same routine every step. About five minutes.

## What you are doing, in one sentence

The zip holds the complete repository as it should be after the step; you replace your local copy's files with it, then GitHub Desktop sends the difference to github.com, where the tests run.

## Before you start, once per step

- Download the zip from the chat (the file card named `stepN_copy_into_repository`). It lands in **Downloads**.
- Double-click it. A folder of the same name appears. Open it.
- Press **Cmd + Shift + .** (period) so the greyed hidden items show. You should see `.github` and `.gitignore` among the files. If you don't, press the keys again.

## Part 1: replace the files

1. Open GitHub Desktop. Top left, **Current repository** should name the tutor repository. If not, click it and choose the repository from the list.
2. Menu bar at the top of the screen: **Repository → Show in Finder** (or press **Cmd + Shift + F**). Your repository folder opens in a second Finder window. It contains `engine.py`, `gas`, `docs`, a greyed `.git`, and so on.
3. Go to the unzipped folder window. Click once on any file, then press **Cmd + A**. Everything in the unzipped folder is selected, including `.github` and `.gitignore`. (There is no `.git` in a zip from me; if you see one, stop and tell me.)
4. Drag the selection onto the repository window and let go.
5. Finder asks about items with the same name. Choose **Replace**. If offered a box "Apply to all," tick it first. (**Replace** is correct for folders too: the zip's folders are complete, so nothing you need is lost. Do not choose **Merge** or **Keep both**.)
6. Wait for the copy to finish. Close the unzipped folder window; you can trash the zip and the unzipped folder afterwards.

What this does not touch: the hidden `.git` folder (your history and connection to github.com), `REPOSITORY.md` (left out because you have edited it), and the `media/` folder (left out because its files are yours and Simulation_Claude's).

## Simulations and pictures: the `media/` folder is yours

Files from Simulation_Claude (and your pictures) go into `media/<archetype>/` by hand, then commit and push. My zips never contain `media/`, so dropping a zip in can never overwrite a newer simulator with an older one. Whenever you save a new or changed file into `media/`, attach the same file to a message to me so my copy matches yours; the wiring (which opener uses which file, and when it opens) is in the openers file and does arrive in my zips.

## Part 2: commit and push

7. Back in GitHub Desktop. The left panel lists the changed files, with a count at the top. Zero changes means Part 1 landed in the wrong folder: redo step 2 and check the window's title is the repository's name.
8. Bottom left, in the box **Summary (required)**, type the message I give at the end of the step report, for example `Step 3: schema, stages, branching`.
9. Click the blue **Commit to main**.
10. Top bar: click **Push origin**. Wait until the arrow stops moving. If the button says **Fetch origin** instead, the push already happened.

## Part 3: watch the tests

11. Menu bar: **Repository → View on GitHub**. Safari opens the repository page.
12. Click the **Actions** tab (top row: Code · Issues · Pull requests · Actions …).
13. The newest run is at the top, named **tests**, with your commit message beside it. A yellow dot means running; reload after a minute. Click the run's title.
14. Boxes, one per job. All must be green except **purity**, which is allowed to show a warning until step 3 says otherwise. The step report tells you how many jobs to expect.
15. Tell me what you see. If a box is red: click it, click the red line inside, and copy the last twenty lines or so into the chat.

## If something is off

- **No `tests` run appears** after a minute: on the Actions tab, if you see "Get started with GitHub Actions," the switch is off. **Settings → Actions → General → Allow all actions and reusable workflows → Save**, then push anything (or edit a file on github.com and commit) to trigger a run.
- **The front page shows one folder containing everything**: the unzipped folder itself was dragged in rather than its contents. Open that folder, select all, drag the contents up one level beside `.git`, trash the empty folder, commit, push.
- **GitHub Desktop shows `.DS_Store`** in the changes: harmless. It is a Finder housekeeping file and is ignored from step 2 onward; if it still appears, right-click it → **Ignore file**.
- **Push is refused** ("rejected" or "behind"): click **Fetch origin**, then **Pull origin**, then **Push origin** again. If that produces a conflict message, stop and paste it to me.

## Things never to do

- Don't delete or move `.git`.
- Don't type a GitHub access token into the chat.
- Don't regenerate `content/BASELINE_authored.txt` (`make baseline`); it is the before-snapshot the whole rebuild is checked against.
- Don't edit `gas/Archetype_ch10_cc.gs`, `gas/Units.gs` or `output/ch10_cc.bundle.json` by hand; they are generated and CI will fail. Edit the sources and run `make generate`, or leave it to me.
