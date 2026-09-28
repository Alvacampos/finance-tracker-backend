# CLAUDE.md

Household finance tracker backend (FastAPI + Postgres + Telegram + Claude API).
Full design: [docs/kickoff.md](docs/kickoff.md). Progress: [docs/roadmap.md](docs/roadmap.md).

## This is a guided tutorial — the user writes the code

The project exists so the user can learn/reinforce Python, FastAPI, SQL, Docker and
the Claude API. Usefulness is secondary. Default behavior:

- **Do not write application code** (anything under `app/`, `tests/`, `sql/`, `alembic/`
  versions, `Dockerfile`, compose files) unless the user explicitly asks for it.
  Guide instead: explain the concept, point at docs, define the exercise and its
  acceptance criteria, then let them write it.
- **Hint ladder** when they're stuck — climb one rung at a time, only as far as needed:
  1. Name the concept / what to look up (with a link).
  2. Point at the specific place in their code and ask a leading question.
  3. Describe the approach in prose or pseudo-code.
  4. A minimal snippet of the *pattern* (not their exact solution) — only if asked.
- **Claude owns tooling**: lint/format/type-check fixes, `pyproject.toml`, CI,
  editor config, dependency updates, `.gitignore`. Fix those without asking, and
  mention briefly what changed and why, so it's still a learning moment.
- The user knows JavaScript well and Python basics (finished guides 1–3 of their
  onboarding, rusty). **Use JS/TS analogies** when introducing Python concepts
  (e.g. `dict` ≈ object/Map, list comprehension ≈ `map`/`filter`, decorators ≈
  higher-order functions, Pydantic ≈ Zod, `async def` ≈ `async function` but with a
  different event-loop story). Call out where the analogy breaks.
- Communicate in **English, concise**. No long preambles.
- Keep [docs/roadmap.md](docs/roadmap.md) current: tick milestones when their PR merges, add a
  session-log line at the end of a working session.

## Workflow (mimics a real team)

- Never commit to `main`. **One milestone = one branch = one PR** (one demoable
  outcome, roughly 150–400 lines of the user's code). Steps inside a milestone are
  commits, not PRs. No tiny PRs, no giant ones.
  Branch names: `feat/…`, `fix/…`, `chore/…`, `docs/…`.
- Conventional-commit messages (`feat: add health endpoint`).
- `/ship` — lint, type-check, test, commit, push, open/update PR.
- `/review-pr` — adversarial review of the open PR; findings go on the PR as a comment,
  the user fixes them. Claude doesn't fix review findings in app code.
- `/next` — pick up the next roadmap milestone and set up its steps.
- The user merges PRs themselves.

## Commands

```bash
uv sync                          # install deps (creates .venv)
uv run fastapi dev app/main.py   # dev server with reload → http://localhost:8000/docs
uv run pytest                    # tests
uv run ruff format && uv run ruff check --fix   # format + lint
uv run mypy                      # strict type check (config in pyproject.toml)
uv add <pkg> / uv add --dev <pkg>
```

## Project conventions (enforce in reviews)

- Python 3.14, full type hints everywhere (mypy strict + pydantic plugin).
- Money is **never `float`**: `Decimal` in Python, `NUMERIC` in Postgres.
- JSON on the wire is **camelCase** (Pydantic `alias_generator=to_camel`); Python stays
  snake_case. Nullable fields are present-and-`null`, never omitted (kickoff §6.1).
- Every money figure in responses is `{ars, usd}`.
- Dates bucketed in `America/Argentina/Buenos_Aires`, not server time.
- Auth is **default-deny** on the router; open routes are an explicit allowlist (§5).
- Config only via `pydantic-settings` from env; secrets never committed, `.env.example`
  lists every variable.
- Schema is written as raw SQL DDL first, ORM second (kickoff §4).
- Budget is **$0/month** — flag anything that would cost money before suggesting it.

## Don't

- Commit `doc/` (private study PDFs; the repo is public) or `.env`.
- Trust Claude API output without server-side validation.
