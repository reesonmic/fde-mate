# api · 后端业务服务

Python 3.11 + FastAPI + SQLAlchemy 2 + Celery + Pydantic v2。

详细设计：[02-后端详细设计.md](../../docs/detail-design/02-后端详细设计.md)

## 启动

```bash
poetry install
cp .env.example .env
poetry run alembic upgrade head    # 数据库迁移
poetry run uvicorn app.main:app --reload --port 8080

# Celery worker（异步任务）
poetry run celery -A app.tasks.celery_app worker --loglevel=info
poetry run celery -A app.tasks.celery_app beat --loglevel=info
```

## 关键依赖

- fastapi ^0.110 / uvicorn / gunicorn
- sqlalchemy ^2.0 / aiomysql / alembic
- pydantic ^2.6 / pydantic-settings
- redis / celery / apscheduler
- httpx（调用 ai-orchestrator）
- structlog / opentelemetry

## 与其他模块关系

- 被 `web/` 调用（HTTPS REST + SSE）
- 调用 `ai-orchestrator/` 通过 HTTP（`app/ai_client/`）
- 启动时导出 OpenAPI Spec 到 `shared-protos/openapi/api.json`

## 目录速览

```
app/
├── routers/      # API 路由（按业务模块）
├── schemas/      # Pydantic 请求/响应
├── services/     # 业务编排
├── repositories/ # 数据访问
├── models/       # SQLAlchemy ORM
├── tasks/        # Celery 异步任务
├── integrations/ # 外部系统适配
└── ai_client/    # 调用 ai-orchestrator
```

完整目录见 [00-目录结构设计 §五](../../docs/detail-design/00-目录结构设计.md)。
