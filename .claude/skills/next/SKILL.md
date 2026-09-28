---
name: next
description: Pick up the next roadmap milestone and set it up as a guided exercise (concept, reading, spec, acceptance criteria). Use when the user says /next, "what's next", or starts a new work session.
---

# /next — set up the next exercise

1. Read `docs/roadmap.md` → find the first `[ ]`/`[~]` milestone (or the one named in
   `$ARGUMENTS`). Check `git status` / `gh pr list` so you don't restart something open.
2. If the previous milestone's PR is merged but not ticked, tick it (`[x]`) and update **Current**.
3. Present, concisely:
   - **Goal** — one sentence, and why it matters for the app.
   - **Concepts** — the 2–4 Python/FastAPI/SQL/Docker ideas involved, each with a JS
     analogy where one exists (see `python-fastapi` skill), plus the reading links.
   - **Warm-up (optional)** — a 5-minute IPython/REPL experiment for rusty concepts.
   - **Spec** — files to create/touch, function/endpoint signatures, behavior.
     A milestone is **one PR**: present its steps in order, each ending in a commit
     (and a runnable check). Guide one step at a time; don't open a PR per step.
   - **Acceptance criteria** — checklist that `/review-pr` will hold them to.
   - **Branch name** to create.
4. Stop. Let the user write the code. When a step works, have them commit it
   (or offer to) on the milestone branch; `/ship` opens the PR once all steps are done. Answer questions with the hint ladder.
