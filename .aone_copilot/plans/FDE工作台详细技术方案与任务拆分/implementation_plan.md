
# FDE 工作台详细技术方案与任务拆分

> **执行哲学**：磨刀不误砍柴工。**先用 1 份『目录结构设计』把所有未来产物的"位置"定下来**，再基于这个骨架填充 9 份详细文档 + 100+ 任务。后续任何文档、代码、配置都有明确归属。

## User Review Required

> [!IMPORTANT]
> **本次输出包含两个层面的目录结构**：
> 1. **文档目录**：`docs/detail-design/` 下 9 份详细设计 + 任务总表
> 2. **代码仓库目录预留**：`workspace/` 下未来要落地的 monorepo 结构（前端 web/ + 后端 api/ + AI orchestrator/ + infra/ + scripts/）
>
> 即使本次不写真实代码，也通过 `.gitkeep` 和 README 占位锁定目录约定，避免后续 100+ 任务在不同 PR 中各自创建出冲突的目录。

> [!NOTE]
> 目录结构设计完成且用户确认后，再开始填充各个详细文档；这样可以保证所有文档之间的相对路径引用一开始就是稳定的。

## Proposed Changes

### 一、目录结构设计（P1 · 优先级最高 · 后续一切的基础）

#### [NEW] [00-目录结构设计.md](file:///Users/micreeson/Desktop/AI/fdework/docs/detail-design/00-目录结构设计.md)

> **本次最重要的产物**。以一份完整文档形式锁定项目所有"位置约定"。

**章节结构**：

**1. 总体目录树（仓库根目录全景）**
```
fdework/
├── docs/                           # 全部文档
│   ├── FDE工作台产品需求文档.md     # PRD（已有）
│   ├── FDE工作台技术方案.md         # 总体技术方案（已有）
│   ├── prototype/                  # HTML 原型（已有）
│   └── detail-design/              # 【本次新增】详细设计与任务
│       ├── README.md               # 文档导航
│       ├── 00-目录结构设计.md       # 本文档
│       ├── 01-前端详细设计.md
│       ├── 02-后端详细设计.md
│       ├── 03-AI接入详细设计.md
│       ├── 04-数据存储详细设计.md
│       ├── 05-部署运维详细设计.md
│       ├── 06-AI对话中心详细设计.md
│       ├── 07-客户空间与文件中心详细设计.md
│       ├── 08-FDE教练与系统设置详细设计.md
│       └── 任务总表.md              # 100+ 开发者级 Task 清单
├── workspace/                      # 【本次新增·预留】未来代码 monorepo
│   ├── README.md                   # monorepo 总览 + 启动指南
│   ├── web/                        # 前端 Vue 3 应用
│   ├── api/                        # 后端 FastAPI 业务服务
│   ├── ai-orchestrator/            # AI 编排独立服务（LangGraph）
│   ├── shared-protos/              # 跨服务共享 schema（OpenAPI/Pydantic）
│   ├── infra/                      # K8s/Helm/Terraform
│   └── scripts/                    # 一键脚本（dev/test/release）
├── .changes/                       # 变更记录（已有）
├── .aone_copilot/                  # 计划与任务（已有，AI 工作目录）
└── README.md                       # 仓库根 README（统揽）
```

**2. `docs/detail-design/` 详细规划**

| 文件 | 定位 | 字段约定 |
|---|---|---|
| README.md | 文档索引 + 阅读路径 | 按角色（FE/BE/AI/QA/OPS）分流 |
| 00-目录结构设计.md | **目录约定本身** | 所有路径源头 |
| 01-前端详细设计.md | Vue 工程蓝图 | 组件/store/路由/类型 |
| 02-后端详细设计.md | FastAPI 工程蓝图 | API/Service/Repository |
| 03-AI接入详细设计.md | LangGraph + RAG | 主图/子图/工具/Prompt |
| 04-数据存储详细设计.md | 5 库设计 | MySQL DDL/Redis/ES/Milvus/OSS |
| 05-部署运维详细设计.md | DevOps 全套 | Docker/K8s/CI/监控 |
| 06/07/08 | 业务模块深化 | 复杂模块独立成文 |
| 任务总表.md | 100+ 开发者级 Task | ID/标题/描述/优先级/工时 |

**3. `workspace/web/` 前端目录**（详细到每个文件夹的职责）

```
web/
├── public/                         # 静态资源
├── src/
│   ├── apis/                       # HTTP 客户端 + Mock 切换
│   │   ├── http.ts
│   │   ├── sse.ts
│   │   ├── modules/                # 按业务模块分（task/project/customer/file/copilot）
│   │   └── mock/                   # Mock 数据（开发期）
│   ├── assets/                     # 图片/字体/图标
│   ├── components/
│   │   ├── common/                 # 通用组件（HealthRing/StatusDot 等）
│   │   ├── layout/                 # AppLayout/AppHeader/AppNav
│   │   ├── copilot/                # CopilotPanel + 4 卡片 + MentionPicker
│   │   └── business/               # 业务组件（KanbanCard/FileThumb 等）
│   ├── composables/                # useSSEChat/useCopilot/useMention
│   ├── pages/                      # 路由页面（按业务模块分文件夹）
│   │   ├── dashboard/
│   │   ├── tasks/
│   │   ├── projects/
│   │   ├── customers/
│   │   ├── files/
│   │   ├── coach/
│   │   ├── chat/
│   │   └── settings/
│   ├── router/                     # Vue Router 路由表
│   ├── stores/                     # Pinia stores（按域分）
│   ├── styles/                     # CSS 设计 token + 重置
│   ├── types/                      # TS 类型定义（business/api/copilot）
│   ├── utils/                      # 工具函数
│   ├── App.vue
│   └── main.ts
├── tests/                          # vitest 单元测试
├── .env.example                    # 环境变量样板
├── .eslintrc.cjs
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md                       # 前端启动指南
```

**4. `workspace/api/` 后端目录**

```
api/
├── app/
│   ├── main.py                     # FastAPI 入口
│   ├── config/                     # Settings（pydantic-settings）
│   ├── deps/                       # FastAPI Depends（auth/db/redis/acl）
│   ├── middleware/                 # 中间件
│   ├── exceptions/                 # 业务异常 + 统一异常处理
│   ├── routers/                    # API 路由（按业务模块分）
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── tasks.py
│   │   ├── projects.py
│   │   ├── customers.py
│   │   ├── files.py
│   │   ├── coach.py
│   │   ├── copilot.py
│   │   └── mentions.py
│   ├── schemas/                    # Pydantic 请求/响应模型
│   ├── services/                   # 业务编排层
│   ├── repositories/               # 数据访问层（SQLAlchemy）
│   ├── models/                     # ORM 模型
│   ├── tasks/                      # Celery 任务
│   ├── integrations/               # 外部系统适配（Aone/CRM/OSS）
│   └── utils/
├── alembic/                        # 数据库迁移
│   ├── versions/
│   ├── env.py
│   └── alembic.ini
├── tests/                          # pytest 测试
├── pyproject.toml                  # Poetry
├── Dockerfile
├── .env.example
└── README.md
```

**5. `workspace/ai-orchestrator/` AI 服务目录**

```
ai-orchestrator/
├── app/
│   ├── main.py                     # FastAPI 入口（独立服务）
│   ├── orchestrator/               # LangGraph 编排核心
│   │   ├── main_graph.py           # 主图
│   │   ├── state.py                # CopilotState
│   │   └── subgraphs/              # 5 子 Agent（tasks/project/coach/files/chat）
│   ├── adapters/                   # LlmAdapter 抽象 + 4 实现
│   │   ├── base.py
│   │   ├── dashscope.py
│   │   ├── idealab.py
│   │   ├── openai.py
│   │   └── mock.py
│   ├── prompts/                    # Jinja2 模板
│   │   ├── tasks.j2
│   │   ├── project.j2
│   │   ├── coach.j2
│   │   ├── files.j2
│   │   └── chat.j2
│   ├── tools/                      # Function Calling 工具（16 个）
│   ├── rag/                        # RAG 引擎
│   │   ├── chunker.py
│   │   ├── embedder.py
│   │   ├── retriever.py
│   │   ├── reranker.py
│   │   └── parsers/                # 6 类文件解析
│   ├── routing/                    # 多模型路由 + 熔断
│   ├── safety/                     # 注入防御 + 输出脱敏
│   ├── audit/                      # AI 操作审计
│   └── config/
├── tests/
├── pyproject.toml
├── Dockerfile
└── README.md
```

**6. `workspace/shared-protos/` 共享协议目录**

```
shared-protos/
├── openapi/                        # 后端导出的 OpenAPI Spec
│   └── api.json                    # 由 api/ 生成，前端按此生成 ts 类型
├── schemas/                        # Pydantic 共享模型（auth/user 等）
└── README.md                       # 协议同步流程
```

**7. `workspace/infra/` 基础设施目录**

```
infra/
├── docker-compose/                 # 本地一键启动
│   ├── docker-compose.yml          # 全栈本地启动
│   └── docker-compose.deps.yml     # 仅依赖（MySQL/Redis/ES/Milvus）
├── k8s/                            # K8s 原始 YAML
│   ├── base/                       # Kustomize base
│   └── overlays/                   # test/staging/prod
├── helm/                           # Helm Chart
│   └── fde-workspace/
├── nginx/                          # Nginx 配置
├── grafana/                        # Dashboard JSON
├── prometheus/                     # 告警规则
└── README.md
```

**8. `workspace/scripts/` 脚本目录**

```
scripts/
├── dev/                            # 本地开发（一键启动/停止/重置数据）
├── test/                           # 测试脚本（覆盖率/性能压测）
├── release/                        # 发布相关
├── data/                           # 数据初始化（种子数据/案例库导入）
└── ci/                             # CI 用脚本
```

**9. 命名约定**
- 文件命名：snake_case（Python）/ kebab-case（前端 .vue 组件除外）/ PascalCase（Vue 组件 + TS 类型）
- 目录命名：kebab-case（仓库根/前端）/ snake_case（Python 包名）
- 数据库表：snake_case + 业务前缀（fde_user / task / project）
- API 路径：kebab-case + 复数名词（`/api/v1/tasks`）
- Git 分支：`feat/M2-FE-001-app-layout`（与任务总表 ID 对齐）

**10. `.gitignore` 全局规范**

**11. 跨模块引用约定**
- 前端引用后端 API：通过 shared-protos/openapi/api.json 自动生成 TS 类型
- 业务 API 调用 AI：仅通过 ai-orchestrator HTTP 接口（不直接 import）
- AI 服务调用业务数据：仅通过 api 暴露的内部接口
- 任何跨服务直接 import = 禁止

**12. 路径别名规范（前端 `@/` / 后端 `app.xxx`）**

**13. 与本次详细设计文档的映射关系（导航表）**

> 该文档完成后，01-08 详细设计文档中所有"涉及文件路径"的部分都引用本文档锁定的位置，避免散落。

#### [NEW] [README.md](file:///Users/micreeson/Desktop/AI/fdework/docs/detail-design/README.md)

详细设计目录索引：
- 9 份文档导航 + 阅读顺序建议
- 按角色（FE/BE/AI/QA/OPS）分流推荐
- 与总体方案、PRD、原型、`workspace/` 代码骨架的关系图
- 任务认领流程（从任务总表选 Task → 创建 feature 分支 → PR → 合并）

---

### 二、8 份模块详细设计文档（基于目录骨架填充）

> 全部文档中"涉及文件路径"字段都基于 `00-目录结构设计.md` 中的约定。

#### [NEW] [01-前端详细设计.md](file:///Users/micreeson/Desktop/AI/fdework/docs/detail-design/01-前端详细设计.md)
工程脚手架 + 完整目录映射 + 路由表 + 10+ 核心组件详细设计 + TS 类型全集 + 4 Pinia stores + API 封装 + Composables + CSS token + 测试

#### [NEW] [02-后端详细设计.md](file:///Users/micreeson/Desktop/AI/fdework/docs/detail-design/02-后端详细设计.md)
脚手架 + 40+ API 完整签名 + Pydantic 全集 + Service/Repository 层 + 中间件 + 异常码体系（≥30 个）+ SSE 实现 + 二次确认完整代码 + 权限模型 + Celery 任务

#### [NEW] [03-AI接入详细设计.md](file:///Users/micreeson/Desktop/AI/fdework/docs/detail-design/03-AI接入详细设计.md)
LangGraph 主图 + 5 子 Agent + LlmAdapter 4 实现 + 5 助手 Prompt 全文（每个 ≥100 行）+ 16 工具完整定义 + RAG 完整代码 + 路由 YAML + 熔断 + 安全模块

#### [NEW] [04-数据存储详细设计.md](file:///Users/micreeson/Desktop/AI/fdework/docs/detail-design/04-数据存储详细设计.md)
25+ 张表完整 DDL + 索引清单 + Alembic 规范 + Redis Key 规范 + ES mapping + Milvus Schema + OSS 目录 + 数据初始化脚本 + 备份策略

#### [NEW] [05-部署运维详细设计.md](file:///Users/micreeson/Desktop/AI/fdework/docs/detail-design/05-部署运维详细设计.md)
3 份 Dockerfile + docker-compose + K8s 完整 YAML + Helm + Nginx 全文 + .gitlab-ci.yml + ArgoCD + 告警规则 + 应急预案

#### [NEW] [06-AI对话中心详细设计.md](file:///Users/micreeson/Desktop/AI/fdework/docs/detail-design/06-AI对话中心详细设计.md)
三栏布局 + 历史管理 + 三种模式 + @ 引用完整实现 + 上下文持久化 + 导出 + 状态隔离

#### [NEW] [07-客户空间与文件中心详细设计.md](file:///Users/micreeson/Desktop/AI/fdework/docs/detail-design/07-客户空间与文件中心详细设计.md)
双栏布局 + 5 Tabs + 文件树 + 分片上传 + RAG 触发 + 批量操作 + 容量进度

#### [NEW] [08-FDE教练与系统设置详细设计.md](file:///Users/micreeson/Desktop/AI/fdework/docs/detail-design/08-FDE教练与系统设置详细设计.md)
4 入口卡 + 最佳实践库 + SOP 库 + 学习路径 + 推荐算法 + C 助手 prompt 全文 + 86 案例 / 128 SOP 数据建模 + 系统设置

---

### 三、代码仓库骨架占位（可选 · 与目录结构同步落地）

> 用 `.gitkeep` + 各级 README.md 把 `workspace/` 目录树落到磁盘上，确保后续 100+ 任务认领时直接 `cd workspace/web/` 即可开工，不会出现"应该建在哪"的扯皮。

#### [NEW] workspace 关键 README 占位（11 个）
- `workspace/README.md`（monorepo 总览）
- `workspace/web/README.md`
- `workspace/api/README.md`
- `workspace/ai-orchestrator/README.md`
- `workspace/shared-protos/README.md`
- `workspace/infra/README.md`
- `workspace/scripts/README.md`
- + 4 个二级目录 README（web/src、api/app、ai-orchestrator/app、infra/k8s）

每个 README 简短说明：定位 / 启动方式 / 关键依赖 / 与其他模块的关系。

---

### 四、任务总表（核心交付物）

#### [NEW] [任务总表.md](file:///Users/micreeson/Desktop/AI/fdework/docs/detail-design/任务总表.md)

按 M2 / M3 / M4 三个里程碑组织，约 **100 个开发者级 Task**，每个 Task 5 个字段（**ID / 标题 / 描述 / 优先级 / 工时估算**）。

每个 Task 的"描述"字段会引用 `00-目录结构设计.md` 中的具体路径（例如："在 `workspace/web/src/components/layout/AppLayout.vue` 中实现 Grid 三栏布局"），确保任务一拿到手就知道在哪里写代码。

**Part 1**：M2/M3/M4 三阶段任务清单（约 100 个）
**Part 2**：里程碑工时汇总
**Part 3**：任务依赖图（Mermaid）
**Part 4**：Aone/Jira CSV 导入模板

## Verification Plan

### 自动化检查
- 目录结构设计文档完成后用 file_grep 校验关键章节标题
- workspace/ 目录创建后用 list_directory 确认 11 个二级目录全部到位
- 9 份详细设计文档的"涉及文件路径"字段全部能在目录结构设计中找到对应位置
- 任务总表 Task 数量在 90-110 之间

### 人工验证
- **用户先审阅 P1 目录结构设计文档**（关键决策点 → 用户确认后才进入 P2-P10）
- 检查 workspace/ 命名是否符合阿里规范
- 验证任务总表能直接派发到具体研发人员


---
生成时间: 2026/4/28 20:19:06
planId: 
plan_status: review