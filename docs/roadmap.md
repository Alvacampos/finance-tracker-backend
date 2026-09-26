# Roadmap & progress

Learning path for this repo, modeled on the onboarding guides' format: each section has
**Learn** (read + type the examples) and a **Task** (one PR each). Phases follow
[kickoff.md §8](kickoff.md#8-phased-roadmap). Each phase ends with something running.

Legend: `[ ]` todo · `[~]` in progress · `[x]` merged

## Status

| Phase | Theme | Status |
| --- | --- | --- |
| 0 | Scaffolding, Docker, deploy | 🟡 in progress |
| 1 | Postgres & schema (SQL → SQLAlchemy → Alembic) | ⚪ |
| 2 | Read endpoints + tests | ⚪ |
| 3 | Telegram plumbing | ⚪ |
| 4 | Claude integration (+ 4B receipts, 4C analysis) | ⚪ |
| 5 | Auth (Google OAuth, allowlist) | ⚪ |
| 6 | Frontend integration | ⚪ |
| 7 | Hardening & observability | ⚪ |

**Current:** Task 1 — hello world + health check.

---

## Phase 0 — Scaffolding

- [~] **Task 0 — Project setup** *(Claude)*: uv project, ruff/mypy/pytest config, CI,
  VS Code config, CLAUDE.md, skills, this roadmap.

- [ ] **Task 1 — Hello FastAPI + health check** *(you)*
  - Learn: [FastAPI First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/),
    [Testing](https://fastapi.tiangolo.com/tutorial/testing/),
    refresher on [type hints](https://docs.python.org/3/library/typing.html) and modules/packages.
  - Build: `app/main.py` with the `FastAPI()` app; `GET /api/health` → `{"status": "ok"}`;
    `tests/test_health.py` using `TestClient`. Passes `/ship` checks.

- [ ] **Task 2 — Config with pydantic-settings** *(you)*
  - Learn: [Settings and env vars](https://fastapi.tiangolo.com/advanced/settings/),
    Python refresher: classes, `@lru_cache`, decorators.
  - Build: `app/config.py` `Settings` class (env name, log level to start), loaded via a
    cached dependency; health reports `env`. Test that overrides settings.

- [ ] **Task 3 — Dockerfile** *(you)*
  - Learn: [Docker get-started](https://docs.docker.com/get-started/) (images, layers,
    build cache), [uv in Docker](https://docs.astral.sh/uv/guides/integration/docker/),
    [FastAPI in containers](https://fastapi.tiangolo.com/deployment/docker/).
  - Build: multi-stage `Dockerfile` (uv builder → slim runtime, non-root user),
    `.dockerignore`. `docker build` + `docker run` → health check responds.

- [ ] **Task 4 — Deploy** *(you, Claude assists with host setup)*
  - Pick a free host (verify current terms: Render free web service is the default
    candidate; supports Docker, sleeps after idle). Auto-deploy from `main`.
  - Done when: public URL `/api/health` returns 200.

## Phase 1 — Database & schema

- [ ] **Task 5 — Local Postgres with docker-compose + raw SQL DDL** *(you)*
  - Learn: [Postgres tutorial](https://www.postgresql.org/docs/current/tutorial.html),
    [data types](https://www.postgresql.org/docs/current/datatype.html),
    [constraints](https://www.postgresql.org/docs/current/ddl-constraints.html),
    [compose](https://docs.docker.com/compose/gettingstarted/).
  - Build: `compose.yaml` with Postgres; `sql/001_schema.sql` by hand: `categories`,
    `expenses` (`NUMERIC` amount, `currency` ARS|USD, `ars_usd_rate_at_entry`,
    `category_id` FK, `paid_by`, `occurred_on`, `raw_message`, nullable `trip_id`),
    `trips`, `corrections`. Seed categories. Practice queries in `psql`
    (JOIN, GROUP BY, date_trunc) — save them in `sql/queries.sql`.

- [ ] **Task 6 — SQLAlchemy 2.x models + session dependency** *(you)*
  - Learn: [SQLAlchemy ORM quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html),
    [FastAPI SQL databases](https://fastapi.tiangolo.com/tutorial/sql-databases/),
    refresher: context managers / `yield`, generators.
  - Build: `app/db.py`, `app/models.py` mirroring the DDL exactly.

- [ ] **Task 7 — Alembic + Neon** *(you)*
  - Learn: [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html).
  - Build: initial migration equivalent to the DDL (diff them!); provision Neon free
    Postgres; migrate prod; backup script with `pg_dump`.

## Phase 2 — Core read endpoints

- [ ] **Task 8 — Response schemas (camelCase) + `GET /api/categories`** *(you)*
  - Learn: [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/),
    [alias generators](https://docs.pydantic.dev/latest/concepts/alias/),
    [response models](https://fastapi.tiangolo.com/tutorial/response-model/).
- [ ] **Task 9 — `GET /api/months/{yyyy-mm}`** *(you)* — SQL aggregates, ART timezone
  bucketing, `{ars, usd}` money, `previousMonthTotal`/`deltaPercent`, null-not-omitted.
  Test DB fixtures in pytest.
- [ ] **Task 10 — `GET /api/years/{yyyy}` + `GET /api/ytd`** *(you)*
- [ ] **Task 11 — Structured logging** *(you)* — stdlib `logging`, JSON output,
  request-id middleware. Learn: [logging HOWTO](https://docs.python.org/3/howto/logging.html).

## Phase 3 — Telegram plumbing

- [ ] **Task 12 — Webhook receiver** *(you)* — `POST /telegram/webhook`, `secret_token`
  header check, filter bot's own messages, log raw updates. Local dev via
  Cloudflare Tunnel (free) or long polling. Learn: [Bot API](https://core.telegram.org/bots/api),
  `async`/`await` + `httpx.AsyncClient`.

## Phase 4 — Claude integration

- [ ] **Task 13 — Tool-use extraction** — `record_expense` / `no_action` /
  `request_clarification` tools, server-side validation, write to DB.
- [ ] **Task 14 — Guardrails** — daily call cap, self-message filter tests, prompt-injection tests.
- [ ] **Task 15 — FX rate capture** (blue rate, cached) — verify dolarapi/bluelytics terms.
- [ ] **Task 16 — Confirmation replies + `/undo` + `/edit`** + `corrections` history.
- [ ] **4B — Receipt photos** (vision, same tool).
- [ ] **4C — Monthly analysis endpoint** + `monthly_analyses` cache + regenerate.

## Phase 5 — Auth

- [ ] Google OAuth (`state` check), 2-email allowlist, HS256 JWT cookie on parent
  domain, default-deny router dependency. Compare with Cloudflare Access afterwards.

## Phase 6 — Frontend integration

- [ ] Frontend loaders call this API; fix contract mismatches found.

## Phase 7 — Hardening & observability

- [ ] Rate limiting (`slowapi`), Sentry free tier for errors, Cloudflare-proxied
  subdomain, real cost check.
- [ ] *Stretch (learning, $0):* Grafana + Loki + Prometheus locally via compose,
  scraping the app's logs/metrics. Grafana Cloud free tier only if it stays $0.

**Stretch (deferred):** budgets/alerts, recurring expenses, trips planning UI,
monthly digest posted by the bot.

---

## Infra decisions (answered 2026-09-26)

- **Docker — yes.** Free, and it's a learning goal: Dockerfile for deploys (portable
  across free hosts) and compose for local Postgres (dev = prod engine).
- **Logs/observability — staged.** Structured stdlib logging from Phase 2 (free,
  foundational) → Sentry free tier in Phase 7 → Grafana stack locally as a stretch.
  Hosted Grafana is overkill for a 2-person app; only if free.
- **Budget rule:** everything $0. Claude API is the only pay-per-use item (cents/month,
  verify in Phase 4).

## Session log

- 2026-09-26 — Kickoff. Project setup (Task 0). Next: Task 1.
