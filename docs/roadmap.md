# Roadmap & progress

Learning path for this repo, modeled on the onboarding guides: each milestone has
**Learn** (read and type the examples) and **Steps**. Phases follow
[kickoff.md §8](kickoff.md#8-phased-roadmap).

**Sizing rule: one milestone = one PR = one demoable outcome.** Steps are commits
inside that PR, not separate PRs. Aim for roughly 150–400 lines of your code and
1–3 sessions per PR. Split only when a milestone clearly outgrows that.

Legend: `[ ]` todo · `[~]` in progress · `[x]` merged

## Status

| Phase | Milestones | Status |
| --- | --- | --- |
| 0 | M0–M2 Scaffolding, Docker, deploy | 🟡 in progress |
| 1 | M3–M4 Postgres & schema | ⚪ |
| 2 | M5–M6 Read endpoints | ⚪ |
| 3 | M7 Telegram plumbing | ⚪ |
| 4 | M8–M11 Claude integration, receipts, analysis | ⚪ |
| 5 | M12 Auth | ⚪ |
| 6 | M13 Frontend integration | ⚪ |
| 7 | M14 Hardening & observability | ⚪ |

**Current:** M1 in review (PR #2) → next M2.

---

## Phase 0 — Scaffolding

- [x] **M0 — Project setup** *(Claude, PR #1)*: uv, ruff/mypy/pytest, CI, VS Code,
  CLAUDE.md, skills, roadmap.

- [~] **M1 — Hello FastAPI + health check** *(PR #2)*: `app/main.py`,
  `GET /api/health`, first `TestClient` test.

- [ ] **M2 — Containerize & deploy**: ends with a public URL returning 200.
  - Learn: [Settings and env vars](https://fastapi.tiangolo.com/advanced/settings/),
    [Bigger applications / APIRouter](https://fastapi.tiangolo.com/tutorial/bigger-applications/),
    [Docker get-started](https://docs.docker.com/get-started/),
    [uv in Docker](https://docs.astral.sh/uv/guides/integration/docker/),
    [FastAPI in containers](https://fastapi.tiangolo.com/deployment/docker/).
    Refresher: classes, `@lru_cache`, decorators.
  - Steps:
    1. Move health to `app/routers/health.py` (`APIRouter(prefix="/api")`).
    2. `app/config.py`: `Settings` via pydantic-settings, cached dependency; a test
       that overrides it.
    3. Multi-stage `Dockerfile` (uv builder → slim runtime, non-root user) plus
       `.dockerignore`; `docker run` serves health.
    4. Deploy to a free host (Render free web service is the default candidate;
       verify current terms). Auto-deploy from `main`. Claude helps with host setup.

## Phase 1 — Database & schema

- [ ] **M3 — SQL by hand**: local Postgres, schema in raw DDL, queries you wrote.
  - Learn: [Postgres tutorial](https://www.postgresql.org/docs/current/tutorial.html),
    [data types](https://www.postgresql.org/docs/current/datatype.html),
    [constraints](https://www.postgresql.org/docs/current/ddl-constraints.html),
    [compose](https://docs.docker.com/compose/gettingstarted/).
  - Steps: `compose.yaml` with Postgres → `sql/001_schema.sql` (`categories`,
    `expenses` with `NUMERIC` amount, `currency` ARS|USD, `ars_usd_rate_at_entry`,
    `category_id` FK, `paid_by`, `occurred_on`, `raw_message`, nullable `trip_id`;
    `trips`; `corrections`) → seed categories → `sql/queries.sql` (JOIN, GROUP BY,
    `date_trunc`, run in `psql`).

- [ ] **M4 — ORM, migrations, hosted DB**
  - Learn: [SQLAlchemy ORM quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html),
    [FastAPI SQL databases](https://fastapi.tiangolo.com/tutorial/sql-databases/),
    [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html).
    Refresher: context managers, `yield`, generators.
  - Steps: `app/db.py` + `app/models.py` mirroring the DDL → Alembic initial
    migration (diff it against your DDL) → session dependency + lifespan → move
    `TestClient` into a `tests/conftest.py` fixture (`with TestClient(app)`, so
    lifespan runs) → provision Neon free, migrate → `pg_dump` backup script.
  - Keep `/api/health` DB-free (free-tier Neon must be able to scale to zero).

## Phase 2 — Core read endpoints

- [ ] **M5 — Contract base + categories + month view**
  - Learn: [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/),
    [alias generators](https://docs.pydantic.dev/latest/concepts/alias/),
    [response models](https://fastapi.tiangolo.com/tutorial/response-model/).
  - Steps: shared base model (camelCase aliases; `json_schema_serialization_defaults_required`
    so defaulted fields are *required* in the OpenAPI output) → `GET /api/categories` →
    `GET /api/months/{yyyy-mm}` (SQL aggregates, ART bucketing, `{ars, usd}`,
    `previousMonthTotal`/`deltaPercent`, null-not-omitted) → test DB fixtures.

- [ ] **M6 — Year/YTD + structured logging**
  - Steps: `GET /api/years/{yyyy}` + `GET /api/ytd` → stdlib `logging` with JSON
    output + request-id middleware
    ([logging HOWTO](https://docs.python.org/3/howto/logging.html)).

## Phase 3 — Telegram plumbing

- [ ] **M7 — Webhook receiver**: `POST /telegram/webhook`, `secret_token` check,
  filter the bot's own messages, log raw updates. Local dev via Cloudflare Tunnel
  (free) or long polling. Learn: [Bot API](https://core.telegram.org/bots/api),
  `async`/`await`, `httpx.AsyncClient`.

## Phase 4 — Claude integration

- [ ] **M8 — Extraction + guardrails**: `record_expense` / `no_action` /
  `request_clarification` tools, server-side validation, write to DB, daily call cap,
  prompt-injection and self-message tests.
- [ ] **M9 — Close the loop**: FX blue-rate capture (verify dolarapi/bluelytics
  terms), confirmation replies, `/undo`, `/edit`, `corrections` history.
- [ ] **M10 — Receipt photos** (4B): vision input, same `record_expense` tool.
- [ ] **M11 — Monthly analysis** (4C): endpoint, `monthly_analyses` cache, regenerate.

## Phase 5 — Auth

- [ ] **M12**: Google OAuth (`state` check), 2-email allowlist, HS256 JWT cookie on
  the parent domain, default-deny router dependency. Compare with Cloudflare Access.

## Phase 6 — Frontend integration

- [ ] **M13**: frontend loaders call this API; fix contract mismatches.

## Phase 7 — Hardening & observability

- [ ] **M14**: rate limiting (`slowapi`), Sentry free tier, Cloudflare-proxied
  subdomain, real cost check. If an uptime monitor probes with `HEAD`, make
  `/api/health` accept it.
- [ ] *Stretch (learning, $0):* Grafana + Loki + Prometheus locally via compose.
  Grafana Cloud free tier only if it stays $0.

**Stretch (deferred):** budgets/alerts, recurring expenses, trips planning UI,
monthly digest posted by the bot.

---

## Infra decisions (answered 2026-09-26)

- **Docker — yes.** Free, and a learning goal: a Dockerfile for deploys (portable
  across free hosts) and compose for local Postgres (dev matches prod).
- **Logs/observability — staged.** Structured stdlib logging in M6 → Sentry free tier
  in M14 → Grafana stack locally as a stretch goal.
- **Budget rule:** everything $0. The Claude API is the only pay-per-use item
  (cents per month; verify in Phase 4).

## Session log

- 2026-09-26 — Kickoff. M0 merged (PR #1). Started M1.
- 2026-09-28 — M1: app, health endpoint, first test. Covered decorators, Pydantic
  `Literal` + defaults, pytest basics, `app/` vs `src/` layout. Review findings moved
  to M2/M4/M5/M14. Re-sized the roadmap into milestones (one PR each).
