---
name: python-fastapi
description: Python 3.14 + FastAPI + Pydantic + SQLAlchemy conventions and teaching notes for this repo. Load when explaining a Python/FastAPI concept, setting an exercise, or reviewing Python code here.
---

# Python & FastAPI — conventions and teaching notes

The user is a strong JS/TS dev relearning Python. Explain via JS analogies, then
where the analogy breaks. Never hand over the solution (see CLAUDE.md hint ladder).

## JS → Python map (use when teaching)

| JS/TS | Python | Gotcha |
| --- | --- | --- |
| `const x = {a: 1}` | `x = {"a": 1}` (dict) | keys are strings/hashables; `x["a"]` not `x.a` |
| `arr.map/filter` | comprehension `[f(v) for v in xs if p(v)]` | prefer comprehension over `map()` |
| `undefined`/`null` | `None` | no `undefined`; missing dict key raises `KeyError` → `.get()` |
| `===` | `==`; `is` for `None` | `x is None`, never `x == None` |
| Zod schema | Pydantic `BaseModel` | validates *and* coerces; `model_validate`, `model_dump` |
| TS types | type hints | not enforced at runtime — mypy checks statically |
| higher-order fn | decorator `@deco` | `@app.get(...)` registers a route |
| `async function` | `async def` | blocking calls in `async def` freeze the loop; use sync `def` for blocking I/O (FastAPI runs it in a threadpool) |
| `try/finally`, cleanup | `with` context manager / `yield` dependency | FastAPI deps with `yield` = setup + teardown |
| `import x from` | `from pkg.mod import x` | packages need to be importable (`app/`, `tests/`) |
| `npm`/`package.json` | `uv` / `pyproject.toml` + `uv.lock` | `uv run` ≈ `npx` inside the project env |
| Jest | pytest | plain `assert`; fixtures instead of beforeEach |
| `0.1 + 0.2` float issue | same | money → `Decimal`, never `float` |

## Conventions to enforce

- Type hints on every function (mypy strict). `list[int]`, `X | None` (not `Optional`).
- `Annotated[...]` style for FastAPI params and dependencies:
  `SessionDep = Annotated[Session, Depends(get_session)]`.
- Separate schemas: `*Create`, `*Update`, `*Response`; never return ORM objects raw
  without a `response_model`.
- camelCase on the wire: base model with
  `ConfigDict(alias_generator=to_camel, populate_by_name=True)`; routes
  serialize by alias. Nullable = present and `null`.
- Routers per domain in `app/routers/`, included in `app/main.py`. Prefix `/api`.
- Config via `pydantic-settings` `Settings`, read once through a cached dependency.
- SQLAlchemy 2.x style: `Mapped[...]`, `mapped_column`, `select()` — not legacy `Query`.
- Errors: raise `HTTPException` with precise status codes; validate path params
  (`yyyy-mm` pattern) with `Path(pattern=...)` or a typed parser.
- Timezone-aware datetimes only (`datetime.now(UTC)`, `ZoneInfo("America/Argentina/Buenos_Aires")`).
- Tests: `TestClient`, `app.dependency_overrides` for DB/settings; one behavior per test;
  test names describe behavior (`test_month_excludes_trip_expenses`).
- Logging via `logging.getLogger(__name__)`, never `print`.

## Refresher topics to weave in when they come up

Comprehensions, unpacking, f-strings, `dataclasses` vs Pydantic, generators/`yield`,
context managers, decorators & `functools.wraps`/`lru_cache`, exceptions & custom
exception classes, `async`/`await` & event loop, `enum.StrEnum`, `pathlib`,
`match` statements, modules vs packages & `__init__.py`.
