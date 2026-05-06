# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FDE工作台 (FDE Workbench) is a monorepo platform for Forward Deployed Engineers (FDEs). The project is in active implementation phase with frontend and backend API code in place.

**Tech Stack**: Vue 3 + TypeScript frontend | Python (FastAPI) backend | LangGraph AI orchestration | MySQL + Redis + Elasticsearch + Milvus

## Module Architecture

```
workspace/
├── web/                 # Frontend Vue 3 SPA (port 5173)
├── api/                 # Backend FastAPI business service (port 8080)
├── ai-orchestrator/     # AI orchestration service with LangGraph (port 8090)
├── shared-protos/       # Shared OpenAPI specs for type synchronization
├── infra/               # Docker/K8s/Helm/Nginx/Grafana configs
└── scripts/             # Dev/test/release/data scripts
```

## Critical Boundary Rules

```
web ←─ HTTPS REST/SSE ─→ api ←─ HTTP only ─→ ai-orchestrator
  └────── 类型生成 ──────→ shared-protos ←────── 导出 OpenAPI ─────┘
```

**CRITICAL constraints**:
- Frontend (web) MUST NOT directly access ai-orchestrator - all requests must go through api for authentication and audit
- api and ai-orchestrator communicate ONLY via HTTP - no cross-service Python imports
- Shared types go through `shared-protos/` - no cross-service direct imports of business code
- Violating these rules will result in PR rejection

## Development Commands

### Full stack startup (recommended for new developers)
```bash
cd workspace/scripts/dev
./start-all.sh
# Browser: http://localhost:5173
```

### Start dependencies only (for debugging individual services)
```bash
cd workspace/infra/docker-compose
docker-compose -f docker-compose.deps.yml up -d  # MySQL/Redis/ES/Milvus

# Then start services individually:
cd workspace/api && poetry install && poetry run uvicorn app.main:app --reload --port 8080
cd workspace/ai-orchestrator && poetry install && poetry run uvicorn app.main:app --reload --port 8090
cd workspace/web && npm install && npm run dev
```

### Frontend
```bash
cd workspace/web
npm run dev              # With MSW mock (default)
npm run dev:real         # Connect to real backend
npm run build            # Production build (vue-tsc + vite build)
npm run test             # Run all vitest tests
npm run test:coverage    # Run tests with coverage
vitest run src/stores/auth.test.ts  # Run specific test file
npm run lint             # ESLint check + fix
npm run format           # Prettier format
npm run gen:types        # Generate types from OpenAPI spec
```

### Backend
```bash
cd workspace/api
poetry install
poetry run alembic upgrade head    # Database migration
poetry run uvicorn app.main:app --reload --port 8080
poetry run pytest                  # Run all tests with coverage
poetry run pytest tests/services/test_task_service.py -v  # Run specific test
poetry run pytest -k "test_create" # Run tests matching pattern
poetry run ruff check .            # Lint
poetry run ruff check . --fix      # Lint + auto-fix
poetry run mypy app                # Type check

# Celery async tasks
poetry run celery -A app.tasks.celery_app worker --loglevel=info
poetry run celery -A app.tasks.celery_app beat --loglevel=info
```

### AI Orchestrator (when code exists)
```bash
cd workspace/ai-orchestrator
poetry install
poetry run uvicorn app.main:app --reload --port 8090
```

## Key Design Documents

Located in `docs/detail-design/`:
- `00-目录结构设计.md` - Directory structure (single source of truth for all paths)
- `01-前端详细设计.md` - Vue 3 blueprint (components/store/router/types)
- `02-后端详细设计.md` - FastAPI blueprint (API/Service/Repository/error codes)
- `03-AI接入详细设计.md` - LangGraph + RAG + prompts + tools
- `04-数据存储详细设计.md` - MySQL DDL / Redis / ES / Milvus schemas
- `05-部署运维详细设计.md` - Dockerfile / K8s / CI / monitoring

**Task tracking**: `docs/detail-design/任务总表.md` (~100 tasks with IDs like `M2-FE-001`)

## Naming Conventions

| Category | Convention | Example |
|----------|------------|---------|
| Python files | snake_case.py | `task_service.py` |
| Python classes | PascalCase | `TaskService` |
| Python functions/vars | snake_case | `get_task_by_id` |
| Python constants | UPPER_SNAKE | `MAX_TOKEN_LIMIT` |
| TS/Vue files | kebab-case.ts / PascalCase.vue | `use-sse-chat.ts` / `AppLayout.vue` |
| TS types | PascalCase | `TaskDTO` |
| CSS classes | kebab-case | `.copilot-panel` |
| REST API paths | kebab-case + plural nouns | `/api/v1/tasks` |
| Git branches | `feat/{Task-ID}-{kebab-desc}` | `feat/M2-FE-001-app-layout` |
| Git commits | Conventional Commits | `feat(task): add batch update api` |
| Database tables | snake_case | `fde_user` / `task` |
| K8s resources | kebab-case | `fde-api` |

## Path Aliases

### Frontend (vite.config.ts)
- `@/` → `src/`
- `@apis/` → `src/apis/`
- `@components/` → `src/components/`
- `@stores/` → `src/stores/`
- `@types/` → `src/types/`

### Backend Python
- Top package: `app`
- Import style: `from app.services.task_service import TaskService`
- Relative imports only within same package

## Error Code System

Business errors (BIZ_xxx): 4xx HTTP status
- 1000-1999: General
- 2000-2999: Auth/permissions
- 3000-3999: Tasks
- 4000-4999: Projects
- 5000-5999: Customers
- 6000-6999: Files
- 7000-7999: Coach
- 8000-8999: AI/Copilot

System errors (SYS_xxx): 5xx HTTP status (9000-9999)

## AI Copilot System

4 assistants per page:
- **T助手** (tasks): Task CRUD, batch operations
- **P助手** (project): Weekly reports, risk analysis
- **C助手** (coach): Expert consultation, best practices
- **F助手** (files): Smart search, file comparison

All AI write operations require **二次确认** (double confirmation) via actionCard mechanism:
1. Preview action → generates `actionId` (60s TTL in Redis)
2. User confirms → execute with `actionId`
3. Handle 5 error cases: not found, expired, user mismatch, tool mismatch, cancelled

## Test Case Structure

Test cases in `docs/test-cases/` (~410 cases):
- ID format: `TC-{MODULE}-{TYPE}-{NNN}` (e.g., `TC-TASK-F-001`)
- Types: F (功能/function), I (接口/interface), U (UI)
- Priorities: P0 (blocking), P1 (core), P2 (minor), P3 (edge)
- Modules: DASH, TASK, PROJ, CUST, COACH, FILE, CHAT, SET, COP, COMM

## Branch Workflow

1. Claim task from `任务总表.md`
2. Create branch: `feat/{Task-ID}-{kebab-desc}`
3. Implement code in `workspace/` corresponding directory
4. Self-test → submit MR with title matching Task title
5. Link Task ID in MR description

## Code Review Guidelines

Located in `docs/code-review/`:
- `00-通用规范.md` - CR philosophy, 6-category checklist, comment prefixes (blocking/nit/question/suggestion/praise)
- `01-前端CR规范.md` - Vue reactive, TS types, Pinia, performance, security, testing
- `02-后端CR规范.md` - API design, layering, DB, error codes, security, cross-service communication
- `03-AI代码CR规范.md` - LangGraph agents, prompts, function calling, RAG, AI safety

Key CR rules:
- PR ≤ 400 lines (max 800 lines requires split)
- Reviewer responds within 24h
- Use comment prefixes: `[blocking]` (must fix), `[nit]` (minor), `[question]`, `[suggestion]`, `[praise]`
- Approve = endorsing the code