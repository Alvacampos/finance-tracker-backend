---
name: review-pr
description: Adversarial code review of the current branch's PR (or a given PR number). Finds bugs, security holes, contract violations and non-idiomatic Python, posts the findings on the PR, and leaves the fixing to the user. Use when the user says /review-pr, asks for a review, or after /ship.
argument-hint: "[PR number] [--recheck]"
---

# /review-pr — adversarial review, user fixes

Act like a demanding senior reviewer whose job is to find what's wrong, not to
approve. Findings teach; **you never fix app code** (lint-only nits excepted — those
belong to /ship).

## Gather

```bash
gh pr view $ARGUMENTS --json number,title,body,headRefName,baseRefName,url
gh pr diff $ARGUMENTS
gh pr checks $ARGUMENTS
```

Read the full changed files, not just hunks — bugs hide in the unchanged context. Load
the `python-fastapi` skill conventions and the relevant sections of `docs/kickoff.md`
and `docs/roadmap.md` (the PR's acceptance criteria).

## Attack surface — try to break it

1. **Correctness:** edge cases (empty month, month boundaries, Dec→Jan, leap years,
   `None`, zero, negative amounts, duplicate Telegram updates), off-by-one, timezone
   (ART vs UTC), `Decimal` vs `float`, wrong status codes.
2. **Security:** secrets in code/logs, missing auth on a route (default-deny?),
   webhook secret check, SQL injection via string formatting, trusting model output,
   bot-self-message loop, user input in logs.
3. **Contract:** matches kickoff §6/§6.1 exactly — camelCase, `{ars, usd}`,
   null-not-omitted, field names, shapes.
4. **Tests:** does a test fail if the code is broken? Missing edge-case tests? Tests
   that test the mock instead of behavior?
5. **Python idioms & design:** blocking calls in `async def`, mutable default args,
   broad `except`, leaking ORM objects, missing type precision, naming, dead code,
   things that'll hurt in the next phase.
6. **Acceptance criteria** from the roadmap item — anything missing?

Only report things you can justify with a concrete failure scenario or a real
convention. No padding; zero findings is a valid result — but look hard first.

## Report

Numbered findings, most severe first:

```
### 1. [blocker|major|minor|nit] Short title — `path/file.py:42`
What's wrong + concrete scenario that breaks it.
Hint: concept/doc link or leading question (hint ladder rung 1–2, NOT the fix).
```

Then a one-line verdict: `Changes requested` or `Ready to merge`.

Post it on the PR: `gh pr review <n> --comment --body-file <tmpfile>` (GitHub doesn't
allow requesting changes on your own PR, so comment). Also print a short summary in chat.

## Re-check (`--recheck` or "I fixed it")

Fetch the new diff, verify each previous finding individually (fixed / partially /
not fixed — with evidence), look for regressions the fixes introduced, post a follow-up
comment. When everything's resolved: say it's ready for the user to merge, and after
they merge, tick the item `[x]` in `docs/roadmap.md` on the next branch.
