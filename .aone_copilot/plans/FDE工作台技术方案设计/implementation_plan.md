
# FDE 工作台技术方案设计

基于已发布的 PRD v1.0，输出一份独立、完整、可落地的全栈技术方案文档。后端采用 **Python（FastAPI + LangChain/LangGraph）** 技术栈，最大化发挥 Python AI 生态优势，支撑 PRD 中 4 个页面级 Copilot + 全局 AI 对话中心 + 多 Agent 编排 + RAG + Function Calling 等高级 AI 能力。

## User Review Required

> [!IMPORTANT]
> **后端技术栈决策已确认**：纯 Python（FastAPI + LangChain + LangGraph），团队全栈背景可承接，AI 复杂度定位为高级（多 Agent 编排 + 自定义 Embedding）。

> [!WARNING]
> Python 后端在阿里内部生态接入（Aone/CRM/OSS）方面 SDK 不如 Java 完善，方案中将单独说明对接策略（HTTP API / 阿里云 SDK Python 版 / 必要时引入 Java Sidecar）。

## Proposed Changes

### 文档输出

#### [NEW] [FDE工作台技术方案.md](file:///Users/micreeson/Desktop/AI/fdework/docs/FDE工作台技术方案.md)

新建独立技术方案文档，结构如下：

**一、文档信息**
- 版本 / 状态 / 关联 PRD v1.0 / 修订记录
- 与 PRD、原型 docs/prototype/ 的对应关系
- 技术栈一句话定位：**Vue 3 + TypeScript 前端 / Python（FastAPI + LangGraph） 后端 / 阿里 AI 网关 + 抽象 SDK / MySQL + Redis + Milvus + OSS**

**二、整体架构**
- 5 层架构图（Mermaid）
  - L1 接入层：Nginx + API Gateway（鉴权/限流）
  - L2 前端层：Vue 3 SPA（部署在 Nginx 静态资源 + CDN）
  - L3 后端服务层：FastAPI 应用集群（业务 API + AI Orchestrator）
  - L4 AI 中台层：统一 AI Gateway SDK + LangGraph Agent 编排 + RAG 引擎
  - L5 数据层：MySQL（业务）+ Redis（缓存/会话）+ Milvus（向量）+ Elasticsearch（全文）+ OSS（文件）
- 部署拓扑图（K8s 微服务化部署）
- 4 条核心数据流图（Mermaid sequenceDiagram）：
  1. 页面加载 → REST API → DB
  2. Copilot 对话 → SSE 流式 → AI Gateway → LLM
  3. AI 写操作 → Function Calling → actionCard 预览 → 二次确认 → 业务 API
  4. 文件 RAG → 上传 → Unstructured 解析 → 分片 → Embedding → Milvus

**三、前端技术方案（Vue 3 + TypeScript）**
- **技术栈选型表**
  | 类别 | 选型 | 版本 |
  |---|---|---|
  | 框架 | Vue 3 | 3.4+ |
  | 语言 | TypeScript | 5.x（strict 模式） |
  | 构建 | Vite | 5.x |
  | UI 库 | Ant Design Vue | 4.x |
  | 状态管理 | Pinia | 2.x |
  | 路由 | Vue Router | 4.x（history 模式） |
  | HTTP | Axios | 1.x（拦截器+重试） |
  | SSE | @microsoft/fetch-event-source | latest |
  | 图标 | Lucide Vue Next | latest |
  | 编辑器 | TipTap | 2.x（@ 引用 + AI 增强） |
  | Markdown | markdown-it + Shiki | latest |
  | 工具 | VueUse / dayjs / lodash-es | latest |
- **目录结构**：标准 src/ 布局（api / components / composables / stores / router / views / types / utils / styles / assets）
- **核心组件设计**
  - `<AppLayout>` Grid 三栏布局（Header 60 + Nav 220 + Main 1fr + Copilot 400/56/0）
  - `<CopilotPanel>` 4 助手统一壳 + 子组件 `<ContextTags>` `<MessageStream>` `<SuggestionChips>` `<MentionInput>`
  - `<MessageRenderer>` 多态渲染器：text / actionCard / report / nextSteps / searchResults
  - `<MentionPicker>` 5 类业务对象 @ 弹窗
  - 业务页面壳：`<TaskKanban>` `<ProjectDetail>` `<CustomerSpace>` `<CoachHub>` `<FileExplorer>`
- **Pinia stores**：useUserStore / useNavStore / useCopilotStore（每页独立 sessionId + context + messages）/ useChatStore（全局 AI 对话）
- **Mock → 真实 API 切换**：基于 `VITE_API_MODE=mock|real` 环境变量，统一在 Axios 拦截层切换

**四、后端技术方案（Python · FastAPI + LangGraph）**
- **技术栈选型表**
  | 类别 | 选型 | 版本 | 选型说明 |
  |---|---|---|---|
  | 语言 | Python | 3.11+ | 性能优于 3.10，async 完善 |
  | Web 框架 | FastAPI | 0.110+ | 原生 async、自动 OpenAPI、Pydantic v2 |
  | ASGI 服务器 | Uvicorn + Gunicorn | latest | 多进程 + 异步并发 |
  | ORM | SQLAlchemy 2.0 + Alembic | 2.x | async 模式 + 迁移 |
  | 数据校验 | Pydantic | v2 | FastAPI 内置 |
  | 数据库 | MySQL | 8.0 | aiomysql 驱动 |
  | 缓存 | Redis | 7.x | redis-py async |
  | 消息队列 | RocketMQ / Kafka | - | 异步任务/审计日志 |
  | 全文检索 | Elasticsearch | 8.x | elasticsearch-py async |
  | 向量库 | **Milvus** | 2.4+ | RAG 主选，pymilvus |
  | 对象存储 | OSS | - | oss2 SDK |
  | API 文档 | FastAPI 内置 Swagger UI | - | - |
  | 认证 | OAuth2 + JWT | - | python-jose |
  | 任务调度 | APScheduler / Celery | - | 周报定时生成 |
  | AI 编排 | **LangChain + LangGraph** | latest | 多 Agent 编排核心 |
  | LLM 客户端 | OpenAI SDK / DashScope SDK | latest | 多模型适配 |
  | Embedding | sentence-transformers / DashScope Embedding | latest | 自定义模型支持 |
  | 文档解析 | Unstructured / PyMuPDF / python-docx | latest | RAG 文档预处理 |
  | 监控 | OpenTelemetry + Prometheus | latest | 调用链 + 指标 |
- **分层架构**（Clean Architecture）
  ```
  ┌─────────────────────────────────────┐
  │  api/         FastAPI Router 层      │
  │  schemas/     Pydantic DTO          │
  │  services/    业务编排服务           │
  │  domain/      领域模型 + 业务规则     │
  │  repositories/ 数据访问层            │
  │  infrastructure/ MySQL/Redis/OSS 等  │
  │  ai/          AI 抽象层 + Agent      │
  │  core/        配置/异常/日志/中间件   │
  └─────────────────────────────────────┘
  ```
- **8 大业务模块包结构**（app/）：dashboard / task / project / customer / coach / file / chat / system + ai（核心 AI 层）+ common
- **核心 RESTful API 设计**（约 40 个端点，按模块列出关键接口）
  - `GET /api/v1/dashboard/summary` 工作台聚合数据
  - `GET/POST /api/v1/tasks` + `PATCH /api/v1/tasks/batch` 批量操作
  - `GET /api/v1/projects/{id}` 项目详情（含健康度环数据）
  - `POST /api/v1/copilot/chat` SSE 流式对话主接口
  - `POST /api/v1/copilot/preview-action` actionCard 预览生成
  - `POST /api/v1/copilot/execute-action` 二次确认后执行
  - `GET /api/v1/mentions/search?type=&keyword=` 5 类对象 @ 搜索
  - `POST /api/v1/files/upload` + `POST /api/v1/files/{id}/index` RAG 索引
- **数据模型设计**（核心表 ER 图 Mermaid）
  - 用户/角色：fde_user, fde_role
  - 任务：task, task_assignee, task_history
  - 项目：project, project_member, milestone, risk
  - 客户：customer, customer_contact, opportunity
  - 文件：file_meta, file_version, file_chunk（向量分片元数据）
  - 教练：best_practice, sop, learning_path
  - AI：ai_session, ai_message, ai_action_log（写操作审计）, ai_feedback, ai_tool_call
- **关键技术点**
  - **SSE 流式响应**：FastAPI `StreamingResponse` + `text/event-stream`，async generator 直接转发 LLM Token 流
  - **写操作二次确认**：actionId UUID + Redis 缓存 60s + 幂等校验 + 审计落库
  - **多租户与权限**：基于 `Depends(current_user)` + 项目/客户级 ACL + RBAC
  - **异步任务**：Celery + Redis broker（周报生成 / 文件 RAG 索引）

**五、AI 接入方案（核心章节 · 多 Agent 编排）**

> 这是本方案最核心的章节，充分发挥 Python AI 生态优势。

- **AI 抽象层架构**
  ```
  ┌───────────────────────────────────────────────┐
  │  CopilotOrchestrator（统一入口）              │
  │  - chat_stream(assistant_id, ctx, msg)        │
  │  - preview_action(intent) → actionCard        │
  │  - rag(query, scope) → relevant_docs          │
  └────────────────────┬──────────────────────────┘
                       │
  ┌────────────────────▼──────────────────────────┐
  │  LangGraph Agent 编排层（StateGraph）          │
  │  ┌──────────────────────────────────────────┐ │
  │  │ Router Agent → 意图识别                   │ │
  │  │ ├─ T 任务 Agent  (CRUD/批量/分析子图)     │ │
  │  │ ├─ P 项目 Agent  (风险/周报/调整子图)     │ │
  │  │ ├─ C 教练 Agent  (问答/Next Step/SOP 子图)│ │
  │  │ ├─ F 文件 Agent  (搜索/总结/对比/归档子图)│ │
  │  │ └─ Global Chat Agent (跨场景/多 @ 引用)   │ │
  │  └──────────────────────────────────────────┘ │
  └────────────────────┬──────────────────────────┘
                       │
  ┌────────────────────▼──────────────────────────┐
  │  LlmAdapter 抽象接口（Strategy 模式）          │
  │  - completion_stream(req) → AsyncIterator     │
  │  - completion(req) → Response                 │
  │  - embedding(texts) → vectors                 │
  └─┬─────────┬──────────┬──────────┬─────────────┘
    │         │          │          │
  IDEAlab DashScope   OpenAI     Mock
  Adapter  Adapter   Adapter   Adapter
  ```
- **统一 AI 网关选型**
  - 主路：阿里 IDE-IDEAlab（内部）
  - 公有云路：DashScope（通义千问 Max/Plus + qwen-embedding-v2）
  - 备路：OpenAI 兼容协议（GPT-4 / Claude）
  - 降级路：本地 Mock（对应原型 copilot.js 配置静态化）
- **LangGraph 多 Agent 编排详解**
  - **StateGraph 设计**：状态字段（user_msg / assistant_id / context / tool_calls / messages / final_response）
  - **节点设计**：router_node / agent_nodes / tool_executor_node / preview_node / response_node
  - **条件边（conditional_edges）**：基于意图分发到对应 Agent，写操作分发到 preview_node
  - **每个助手的子图（Subgraph）**：
    - T 任务 Agent：`分析意图 → 查询任务库 → 生成 actionCard / report → 流式输出`
    - P 项目 Agent：`绑定项目 → 健康度分析 → 风险召回 → 生成 report / 周报草稿`
    - C 教练 Agent（10 年专家身份）：`理解问题 → 案例库 RAG 召回 → SOP 匹配 → 生成 nextSteps / report`
    - F 文件 Agent：`感知路径/选中 → RAG 召回 → 多模态分析 → 生成 searchResults / 对比报告`
- **4 助手 Prompt 模板设计**
  - 使用 LangChain `ChatPromptTemplate` + Jinja2 占位符
  - System Prompt 模板示例（C 教练）：
    ```
    你是一位拥有 10 年 FDE 交付经验的资深前线部署工程师...
    当前用户：{user_name}（{user_level}）
    当前项目：{project_name}（{project_phase}，健康度 {health_score}）
    可用工具：{available_tools}
    回答原则：基于项目背景给出针对性建议，引用最佳实践库...
    ```
  - 模板版本化管理：存放于 `app/ai/prompts/` 目录，按助手分文件
- **RAG 流程详解**（针对 F 助手 + C 助手）
  ```
  上传文档 → Unstructured 解析（PDF/Word/Excel/PPT）
        ↓
  RecursiveCharacterTextSplitter 分片（chunk_size=512, overlap=64）
        ↓
  DashScope Embedding（text-embedding-v2, 1536 维）
        ↓
  Milvus 向量库存储（Collection: fde_documents, 索引: HNSW）
        ↓
  查询时：query embedding → top_k=10 召回 → BGE Reranker → 注入 Prompt
  ```
  - 向量库 Schema：file_id / chunk_id / project_id / customer_id / content / embedding / metadata
  - 权限过滤：基于 project_id/customer_id 在向量检索时做 partition 过滤
- **Function Calling / Tool Use 设计**（actionCard 生成核心）
  - 使用 LangChain `@tool` 装饰器定义业务工具
  - 5 类核心工具：
    | 工具 | 助手归属 | 功能 |
    |---|---|---|
    | `create_task` | T | 创建任务 → 返回 actionCard |
    | `batch_update_tasks` | T | 批量更新 → 返回 actionCard + impact list |
    | `analyze_project_risks` | P | 风险分析 → 返回 report |
    | `generate_weekly_report` | P | 周报生成 → 返回结构化文档 |
    | `mention_search` | 全部 | @ 引用搜索 → 返回搜索结果 |
    | `archive_files` | F | 批量归档 → 返回 actionCard + impact list |
  - 工具输出经 Pydantic Schema 校验后转 actionCard JSON
- **多模型路由策略**
  - 路由维度：助手类型 / 用户等级 / 任务复杂度 / 成本预算
  - 实现：`ModelRouter` 类 + YAML 配置（`app/ai/config/model_routing.yaml`）+ Apollo 动态生效
  - 路由示例：
    ```yaml
    coach_assistant:
      primary: dashscope/qwen-max
      fallback: idealab/claude-4-opus
      mock: local/coach_mock.json
    file_assistant_rag:
      primary: dashscope/qwen-plus  # RAG 场景用便宜模型
    ```
- **降级与容错**
  - 网关熔断：使用 `circuit-breaker` 库，失败率 > 50% 自动熔断 30s
  - 离线 Mock：从 `docs/prototype/assets/js/copilot.js` 同步预设回复到 `app/ai/mock/` 目录
  - SLA 监控：每次 LLM 调用记录 latency / token 消耗 / 失败原因到 Prometheus
- **AI 安全与审计**
  - 输入侧：Prompt Injection 检测（关键词黑名单 + LLM 二次校验）
  - 输出侧：敏感信息脱敏（客户名/手机号正则）
  - 审计：所有 tool_call / action_execute 落 `ai_action_log` 表，保存 7 年

**六、数据存储方案**
- **MySQL 主库**：业务数据（任务/项目/客户/用户/AI 会话元数据）
- **Redis**：Session / actionId 缓存 / SSE 连接管理 / 限流计数 / 热点排行
- **Elasticsearch**：任务/文件全文检索 + @ 引用搜索（5 类对象统一索引）
- **Milvus 向量库**：RAG 文档 Embedding（FDE 案例库 + 用户上传文档）
- **OSS**：原始文件 + 用户头像 + 周报导出
- **数据迁移**：Alembic 管理 DDL，PRD 8 大模块对应 SQL 脚本
- **数据隔离**：基于 `tenant_id` + `project_acl` 表的双层隔离

**七、部署与运维方案**
- **环境分层**：本地（Docker Compose + Mock）/ 测试 / 预发 / 生产
- **容器化**：
  - 前端：Vue 构建产物 + Nginx 镜像（多阶段构建）
  - 后端：Python 3.11-slim + Uvicorn + Gunicorn 镜像
  - AI 服务可拆分为独立 Pod（高内存配置）
- **K8s 部署**：
  - 业务 API Pod × 3（4C8G）
  - AI Orchestrator Pod × 2（8C16G，需要更多内存加载 Embedding 模型）
  - Milvus Standalone / Cluster 模式
- **CI/CD**：GitLab Pipeline → 构建 → pytest 测试 → 镜像推送 → ArgoCD 部署
- **监控**：
  - APM：OpenTelemetry → ARMS / Jaeger
  - 日志：SLS（结构化 JSON 日志）
  - AI 调用监控：Prometheus + Grafana 面板（Token 消耗 / 响应时长 / 失败率 / 模型分布）
- **配置中心**：Apollo / Nacos
- **安全合规**：
  - 数据脱敏：客户敏感字段 AES 加密存储
  - AI 审计：所有写操作落库 + 7 年存储
  - JWT + RBAC + 项目/客户 ACL 三级权限

**八、阿里内部生态对接策略（Python 后端特别说明）**

> [!IMPORTANT]
> Python 后端在阿里内部生态接入时需要特别处理。

| 系统 | Python 接入策略 |
|---|---|
| Aone（任务/代码） | OpenAPI HTTP 调用，使用 httpx 异步客户端 |
| 内部 CRM | OpenAPI 网关 + JWT 鉴权 |
| OSS | 阿里云官方 oss2 Python SDK（成熟） |
| Apollo 配置中心 | pyapollo 客户端 |
| Nacos | nacos-sdk-python |
| Sentinel 限流 | 通过 API 网关层接入（Sidecar 模式） |
| 钉钉 / 语雀 | OpenAPI HTTP |
| IDE-IDEAlab | OpenAPI（OpenAI 兼容协议） |

**九、与原型对应的实施切片**
- 按 PRD 8.1 里程碑映射技术任务
- M1（已完成）：原型 HTML
- M2（LLM 接入）：FastAPI 骨架 + 4 助手 LangGraph 子图 + SSE 接入 + 5 个核心 API
- M3（业务数据接入）：@ 引用真实数据（Aone/CRM/OSS）+ Milvus RAG + Function Calling 工具实现
- M4（高级能力）：多 Agent 协作（跨助手任务编排）+ 周报自动归档 + 语音 + 暗色模式

**十、关键技术风险与应对**
| 风险 | 等级 | 应对 |
|---|---|---|
| LLM SLA 不稳定 | 高 | 多模型路由 + 熔断 + Mock 降级 |
| 写操作误执行 | 高 | actionId + 二次确认 + 审计 + Pydantic Schema 校验 |
| Python GIL 性能瓶颈 | 中 | async I/O 全异步 + Gunicorn 多 worker + AI 服务独立部署 |
| Milvus 向量库运维成本 | 中 | 初期使用 Standalone，规模上来后切 Cluster |
| RAG 召回准确率 | 中 | BGE Reranker + 阈值过滤 + 混合检索（向量 + ES） |
| 阿里内部 Java 生态对接 | 中 | 关键服务用 HTTP API，必要时引入 Java Sidecar |
| Prompt Injection 攻击 | 中 | 关键词检测 + LLM 二次校验 + 输出脱敏 |

**十一、附录**
- 术语对齐 PRD 附录 A
- 关键技术调研链接（FastAPI / LangGraph / Milvus / DashScope 官方文档）
- Python 关键依赖 requirements.txt 示例
- 修订记录

## Verification Plan

### 自动化检查
- 文档生成后，使用 file_grep 校验关键章节标题数量（11 个一级章节）
- 检查 Mermaid 代码块语法（GitLab/Yuque/语雀渲染兼容）
- 检查所有 PRD 引用路径准确性

### 人工验证
- 用户审阅文档 → 确认 5 大维度（前端/后端/AI/数据/部署）覆盖完整
- 与 PRD §4-§7 章节交叉验证（功能、设计系统、性能、安全要求是否技术上可落地）
- 重点确认 AI 章节（§5）的 LangGraph 多 Agent 编排设计是否清晰
- 确认 §8 阿里内部生态对接策略的可行性


---
生成时间: 2026/4/28 19:54:06
planId: 
plan_status: review