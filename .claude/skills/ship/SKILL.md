---
name: ship
description: Lint, format, type-check and test, then commit, push the feature branch and open or update its PR. Use when the user says /ship or asks to commit/push their work.
disable-model-invocation: true
argument-hint: "[optional commit message]"
---

# /ship — checks → commit → push → PR

1. **Branch guard.** `git branch --show-current`. If on `main`, stop and propose a branch
   name (`feat/…`, `fix/…`, `chore/…`, `docs/…`) based on the diff; create it once the
   user agrees. Never commit to `main`.
2. **Checks** (run in order, in the repo root):
   ```bash
   uv sync --locked
   uv run ruff format
   uv run ruff check --fix
   uv run mypy
   uv run pytest        # exit code 5 (no tests collected) is OK
   ```
3. **Fixing failures — the split matters (this is a tutorial):**
   - Formatting, lint and type-annotation issues: **fix them yourself** (tooling is
     Claude's job). Don't change behavior. Afterwards list each fix in one line with
     the rule id and why it exists (e.g. `B008: function call in default arg — evaluated
     once at import time`).
   - Failing tests or a lint/type error that reveals a *logic* bug: **don't fix**. Stop,
     explain what failed and why, give a hint (CLAUDE.md hint ladder), and let the user fix it.
4. **Review the diff** (`git status`, `git diff`): make sure no `.env`, secrets, `doc/`,
   or stray files are staged. Stage explicit paths, not `git add -A` blindly.
5. **Roadmap:** if this work completes or advances a roadmap milestone, update
   `docs/roadmap.md` (`[~]` while the PR is open) in the same commit.
6. **Commit** with a conventional-commit message (use `$ARGUMENTS` if given), ending
   with the attribution trailer from the system prompt.
7. **Push:** `git push -u origin HEAD`.
8. **PR:** `gh pr view` — if one exists, just report its URL and the CI status. Otherwise
   `gh pr create` with:
   - Title = conventional-commit style summary.
   - Body: `## What` (bullets), `## Why` (roadmap milestone, e.g. "Roadmap M2"),
     `## How to test` (commands), `## Learned` (1–3 bullets of concepts practiced),
     then the attribution line.
9. Report: PR URL, checks run, what Claude auto-fixed, and suggest `/review-pr`.
