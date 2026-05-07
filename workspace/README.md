# FDE 工作台 · 代码 Monorepo

> 本目录是 FDE 工作台的**全部代码实现**。详细目录约定见 [docs/detail-design/00-目录结构设计.md](../docs/detail-design/00-目录结构设计.md)。

---

## 一、模块总览

| 子目录 | 定位 | 技术栈 | 端口 |
|---|---|---|---|
| [`web/`](./web/) | 前端 SPA | Vue 3 + TypeScript + Vite + Pinia | 5173（dev） |
| [`api/`](./api/) | 后端业务服务 | Python + FastAPI + SQLAlchemy + Celery | 8080 |
| [`ai-orchestrator/`](./ai-orchestrator/) | AI 编排服务 | Python + FastAPI + LangGraph + Milvus | 8090 |
| [`shared-protos/`](./shared-protos/) | 共享协议（OpenAPI Spec） | JSON / YAML | - |
| [`infra/`](./infra/) | 基础设施 | Docker / K8s / Helm / Nginx | - |
| [`scripts/`](./scripts/) | 一键脚本 | Bash / Python | - |

---

## 二、本地一键启动

### 启动全部服务（推荐新人）

```bash
cd workspace/scripts/dev
./start-all.sh
# 浏览器访问 http://localhost:5173
```

### 仅启动依赖（自己起前端/后端调试）

```bash
cd workspace/infra/docker-compose
docker-compose -f docker-compose.deps.yml up -d
# 启动 MySQL/Redis/ES/Milvus 容器

# 然后分别启动各服务
cd workspace/api && poetry install && poetry run uvicorn app.main:app --reload --port 8080
cd workspace/ai-orchestrator && poetry install && poetry run uvicorn app.main:app --reload --port 8090
cd workspace/web && npm install && npm run dev
```

---

## 三、跨模块边界（重要）

```
web ←─ HTTPS REST/SSE ─→ api ←─ HTTP only ─→ ai-orchestrator
  └────── 类型生成 ──────→ shared-protos ←────── 导出 OpenAPI ─────┘
```

> [!CAUTION]
> 1. **web 不直接访问 ai-orchestrator**（必须经 api 转发，便于鉴权与审计）
> 2. **api 与 ai-orchestrator 仅通过 HTTP 通信**，禁止 Python 跨服务 import
> 3. 共享类型走 `shared-protos/`，禁止跨服务直接 import 业务代码

详见 [00-目录结构设计 §12](../docs/detail-design/00-目录结构设计.md)。

---

## 四、详细设计文档

| 模块 | 详细设计 | 状态 |
|---|---|---|
| 目录约定 | [00-目录结构设计.md](../docs/detail-design/00-目录结构设计.md) | v1.1 ✅ |
| 前端 | [01-前端详细设计.md](../docs/detail-design/01-前端详细设计.md) | v1.1 ✅ |
| 后端 | [02-后端详细设计.md](../docs/detail-design/02-后端详细设计.md) | v1.1 ✅ |
| AI 简版 | [03-AI接入详细设计.md](../docs/detail-design/03-AI接入详细设计.md) | v1.0 ✅（产品/QA 入门）|
| AI 详版 | [03-AI编排服务详细设计.md](../docs/detail-design/03-AI编排服务详细设计.md) | v1.1 ✅（AI 工程师工程蓝图）|
| 部署 | [05-部署运维详细设计.md](../docs/detail-design/05-部署运维详细设计.md) | v1.0 ✅ |
| 数据存储（04）| - | ⏳ 待编写（DDL 已落地于 `api/alembic/versions/001_initial.py`）|
| AI 对话中心（06）| - | ⏳ 待编写 |
| 客户/文件（07）| - | ⏳ 待编写 |
| 教练/设置（08）| - | ⏳ 待编写 |

---

## 五、子目录实施状态

| 子目录 | 已落地内容 |
|---|---|
| `web/` | 10 类 page + 7 store + 9 API 模块 + 2 composable + 22 component + http/sse/mock 全套（v1.1）|
| `api/` | 10 router + ai_client + 5 integrations + 13 service + 5 celery 任务 + alembic 18 表完整 DDL（v1.1）|
| `ai-orchestrator/` | 6 endpoint + LangGraph agent_node + 3 LLM provider + 熔断器 + 双闸门 + 审计 + 混合 RAG + 4 Agent x 19 工具（v1.1）|
| `shared-protos/` | 当前仅 README 占位，OpenAPI Spec 尚未导出 |
| `infra/` | `docker-compose/` + `k8s/`（具体 manifest 数量见目录）|
| `scripts/` | `dev/start-all.sh` 一键启动脚本 |

---

## 六、首次启动数据库迁移

```bash
cd workspace/api
poetry install
# 1) 初始化数据库（执行 alembic 迁移生成 18 张业务表）
poetry run alembic upgrade head
# 2) 启动服务
poetry run uvicorn app.main:app --reload --port 8080
```

> Alembic 配置见 `workspace/api/alembic.ini`，初始迁移见 `workspace/api/alembic/versions/001_initial.py`。

---

## 七、任务清单

所有可认领的开发任务在 [任务总表.md](../docs/detail-design/任务总表.md)。
认领流程见 [docs/detail-design/README.md §4](../docs/detail-design/README.md)。
