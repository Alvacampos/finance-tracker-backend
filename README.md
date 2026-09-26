# finance-tracker-backend

Private two-person household finance tracker: expenses come in through a Telegram
group, get parsed by the Claude API, land in Postgres, and are served to a read-only
dashboard through a FastAPI API.

- Design & decisions: [docs/kickoff.md](docs/kickoff.md)
- Roadmap & progress: [docs/roadmap.md](docs/roadmap.md)

## Setup

Requires [uv](https://docs.astral.sh/uv/) (it installs the right Python version for you).

```bash
uv sync                          # create .venv and install dependencies
cp .env.example .env             # fill in values as phases require them
uv run fastapi dev app/main.py   # http://localhost:8000/docs
```

## Checks

```bash
uv run ruff format && uv run ruff check   # format + lint
uv run mypy                                # type check
uv run pytest                              # tests
```

CI runs the same checks on every pull request.
