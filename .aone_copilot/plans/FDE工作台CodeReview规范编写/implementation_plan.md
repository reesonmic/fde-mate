# FDE 工作台 Code Review 规范编写计划

承接已完成的详细设计与测试用例库，输出 Code Review 规范体系，为后续编码阶段建立质量门槛。

## User Review Required

> [!IMPORTANT]
> **本计划只产出"CR 规范文档"，不修改 ESLint/Ruff/Mypy 等工具配置文件，不接入 CI/CD 卡点脚本**。
> 工具链落地（pre-commit hook、CI 集成）、CR 度量平台对接、Reviewer 培训等属于后续运维任务，本次不涉及。

> [!NOTE]
> **依据来源**：
> - 总体技术方案：[FDE工作台技术方案.md](file:///Users/micreeson/Desktop/AI/fdework/docs/FDE工作台技术方案.md)（确定 Vue3+TS / Python+FastAPI / LangGraph 技术栈）
> - 前端详细设计：[01-前端详细设计.md](file:///Users/micreeson/Desktop/AI/fdework/docs/detail-design/01-前端详细设计.md)（含 ESLint/Prettier/TypeScript 配置）
> - 后端详细设计：[02-后端详细设计.md](file:///Users/micreeson/Desktop/AI/fdework/docs/detail-design/02-后端详细设计.md)（含 Ruff/Mypy/异常码体系）
> - 跨服务边界约定：[workspace/README.md §三](file:///Users/micreeson/Desktop/AI/fdework/workspace/README.md)（web→api→ai-orchestrator 单向依赖）
> - Skill 引用：[alibaba-java-coding-guidelines-skill](file:///Users/micreeson/.claude/skills/alibaba-java-coding-guidelines-skill/SKILL.md)（不直接套用，但参考其 Checklist 结构）

## Proposed Changes

### 一、目录结构（新增）

新增 `docs/code-review/` 目录，落位 4 份 CR 规范文档 + 1 份 README 索引：

```
docs/code-review/
├── README.md                  # 总索引（4 份文档导航 + 适用栈对照 + Checklist 速查）
├── 00-通用规范.md              # CR 通用规范（适用全栈：流程/分类Checklist 6 大类/反模式/CR 哲学）
├── 01-前端CR规范.md            # Vue 3 + TypeScript + Pinia 专项
├── 02-后端CR规范.md            # Python + FastAPI + SQLAlchemy + Celery 专项
└── 03-AI代码CR规范.md          # LangGraph Agent + Prompt + RAG + LlmAdapter 专项
```

### 二、Checklist 6 大类（贯穿 4 份文档）

每份文档统一按 6 大类组织 Checklist，每条规则配 1-2 段 good/bad 代码对照：

| 类别 | 重点关注 |
|------|---------|
| **功能正确性** | 边界值/空值/并发/事务/幂等 |
| **可读性** | 命名/注释/函数长度/复杂度/重复代码 |
| **性能** | N+1 查询/无效循环/缓存使用/异步阻塞/前端首屏 |
| **安全** | 注入/越权/敏感信息/Prompt 注入/凭证泄漏 |
| **测试** | 单测覆盖/边界用例/Mock 合理性/E2E 覆盖 |
| **文档** | API 文档/复杂逻辑注释/CHANGELOG/前端 JSDoc |

---

#### [NEW] [README.md](file:///Users/micreeson/Desktop/AI/fdework/docs/code-review/README.md)

**作用**：CR 规范库总索引

**核心内容**（约 150 行）：
- 4 份文档导航（带链接 + 适用对象）
- CR 哲学（5 条核心理念，简短）
- 适用栈对照表（按子工程 web/api/ai-orchestrator 选择文档）
- 分类 Checklist 速查（6 大类 × 4 文档 = 24 节速查）
- CR 工作流极简版（3 步：发起 PR → Review → 合并）
- 与详细设计/测试用例库的关联说明
- 修订记录

---

#### [NEW] [00-通用规范.md](file:///Users/micreeson/Desktop/AI/fdework/docs/code-review/00-通用规范.md)

**作用**：所有 CR 共用规范基线

**预算行数**：~900 行

**核心内容**：

##### 一、CR 哲学与基本原则（~80 行）
- CR 不是挑刺，是协作演进
- Review 代码不是 Review 人
- 评论分级：blocking / nit / question / praise
- 提交者职责 vs Reviewer 职责
- 时长目标：< 24h 响应、< 400 行 PR

##### 二、6 大类通用 Checklist（~600 行，每类 ~100 行）

**1. 功能正确性**
- ✅ 边界值（空数组/null/0/最大值）必须显式处理
- ✅ 异常路径必有处理或日志
- ✅ 事务边界明确（DB 操作组）
- 配 good/bad 示例（伪代码 + 真实片段）

**2. 可读性**
- ✅ 命名表意（forbid 单字母/数字后缀）
- ✅ 函数 < 50 行 / 圈复杂度 < 10
- ✅ 注释解释"为什么"，不是"做什么"
- ✅ 禁用魔法数字（必须提取常量）

**3. 性能**
- ✅ 循环内禁止 IO/查询
- ✅ 大列表必须分页
- ✅ 前端首屏 < 1.5s（PRD §7.1）/ API P95 < 500ms

**4. 安全**
- ✅ 用户输入必经校验
- ✅ 输出必经 escape（XSS）
- ✅ SQL/NoSQL 必用参数化
- ✅ 敏感字段（password/token）禁止入日志
- ✅ 越权检查（行级 ACL）

**5. 测试**
- ✅ 新增功能必带单测
- ✅ 修复 bug 必带回归用例
- ✅ Mock 不可滥用（外部依赖必 mock，内部协作不 mock）
- ✅ 覆盖率门槛：核心 ≥ 80% / 整体 ≥ 60%

**6. 文档**
- ✅ Public API 必有 docstring/JSDoc
- ✅ 复杂业务逻辑必有内联注释
- ✅ 破坏性变更必更新 CHANGELOG
- ✅ 配置变更必更新 .env.example

##### 三、CR 流程规范（~150 行）
- 分支策略：feat/{ID}-{slug} / fix/{ID}-{slug} / hotfix/{slug}
- PR 模板（必填字段：背景/方案/影响/测试/截图）
- Reviewer 指派：≥1 人 same-stack + ≥1 人 cross-stack（核心模块）
- 合并门槛：所有 blocking 已解决 + 至少 1 个 LGTM + CI 全绿
- 评论分级使用规范

##### 四、反模式案例库（~50 行 + 示例）
- 5 个常见反模式（God Function / Magic Number / Silent Catch / 重复代码 / 过早优化）
- 每个反模式配 bad / good 对照

##### 五、Checklist 速查表（~20 行）
- 6 大类共 ~30 条快速勾选项

---

#### [NEW] [01-前端CR规范.md](file:///Users/micreeson/Desktop/AI/fdework/docs/code-review/01-前端CR规范.md)

**作用**：Vue 3 + TypeScript + Pinia + Ant Design Vue 专项 CR 规范

**预算行数**：~1200 行

**核心内容**：

##### 一、Vue 组件规范（~250 行）
- ✅ 组件名 PascalCase / 文件名 kebab-case 二选一统一
- ✅ Composition API + `<script setup lang="ts">` 强制
- ✅ Props 必带类型 + 默认值（withDefaults）
- ✅ Emits 必声明
- ✅ 单文件 < 300 行（超过拆子组件）
- 含 4 段 good/bad（基础组件 / 业务组件 / Copilot 组件 / 表单组件）

##### 二、TypeScript 类型规范（~200 行）
- ✅ 禁用 `any`（必要时用 `unknown` + 类型守卫）
- ✅ API 类型从 OpenAPI 自动生成（`shared-protos/openapi/api.json`）
- ✅ 类型 import 用 `import type`
- ✅ 复杂泛型必加注释

##### 三、状态管理（Pinia）（~150 行）
- ✅ Store 按业务域拆分（不按页面拆）
- ✅ State 不含派生数据（用 getters）
- ✅ Action 必处理异常（try/catch + toast）
- ✅ 跨 Store 调用必经 root，禁止循环依赖

##### 四、API 调用（~150 行）
- ✅ 必经 `apis/http.ts` 实例
- ✅ SSE 必经 `apis/sse.ts`
- ✅ 错误统一拦截器处理 + 业务级 try/catch
- ✅ Mock 数据走 MSW（VITE_USE_MOCK=true 切换）

##### 五、性能（~150 行）
- ✅ 列表 v-for 必带 `:key`（不用 index）
- ✅ 大列表用虚拟滚动（vue-virtual-scroller）
- ✅ 图片 lazy loading
- ✅ 路由级 + 组件级懒加载（() => import()）
- ✅ 避免在 template 内调用方法（用 computed）

##### 六、安全（~100 行）
- ✅ v-html 必经 DOMPurify（PRD §7.4）
- ✅ 跳转 URL 必白名单校验
- ✅ localStorage 禁存 token / 敏感信息（用 httpOnly cookie）

##### 七、测试（~100 行）
- ✅ 组件单测用 @vue/test-utils
- ✅ 关键交互必有 e2e（Playwright）

##### 八、Copilot 专项（~100 行）
- ✅ actionCard 渲染必校验 actionId 存在性
- ✅ SSE 中断必有友好提示 + 重试入口
- ✅ @ 引用 tag 必有移除按钮

---

#### [NEW] [02-后端CR规范.md](file:///Users/micreeson/Desktop/AI/fdework/docs/code-review/02-后端CR规范.md)

**作用**：Python + FastAPI + SQLAlchemy + Celery 专项 CR 规范

**预算行数**：~1300 行

**核心内容**：

##### 一、API 设计（~200 行）
- ✅ 路由必带版本号 `/api/v1/*`
- ✅ Request/Response 必用 Pydantic schema（不用 dict）
- ✅ 状态码遵循 REST 语义（200/201/204/4xx/5xx）
- ✅ 复杂查询用 query params + Pydantic 校验
- ✅ POST/PUT/DELETE 必带幂等性考虑（actionId 机制）

##### 二、Service / Repository 分层（~200 行）
- ✅ Controller 不含业务逻辑（只做参数校验 + 调 Service）
- ✅ Service 不直接拼 SQL（必经 Repository）
- ✅ Repository 只关心数据，禁含业务规则
- ✅ 跨模块调用走 Service，禁止跨 Repository 调用

##### 三、数据库（~250 行）
- ✅ 必用 SQLAlchemy ORM（禁裸 SQL，例外需 review approve）
- ✅ N+1 查询必用 `selectinload` / `joinedload`
- ✅ 大表查询必带 LIMIT
- ✅ 事务边界明确（`async with session.begin()`）
- ✅ Alembic migration 必有 downgrade
- ✅ 索引设计必经 review

##### 四、异常处理（~200 行）
- ✅ 业务异常必用 `BizException` + `ErrorCode`（02-后端详细设计.md §7.2）
- ✅ 错误码必在 `exceptions/codes.py` 集中定义（前缀 BIZ_/SYS_）
- ✅ 禁止 `except Exception: pass`
- ✅ 日志必含 traceId（structlog）

##### 五、安全（~200 行）
- ✅ 所有非 /auth 路由必经 `Depends(current_user)`
- ✅ 行级权限必经 `require_role` 或自定义 Depends
- ✅ 用户输入必经 Pydantic 校验
- ✅ 密码必用 bcrypt
- ✅ JWT 密钥必从 settings 读取（禁硬编码）
- ✅ 敏感字段（password/token/sk）禁止入日志

##### 六、性能（~150 行）
- ✅ I/O 操作必用 `async`
- ✅ Celery 任务必带超时 + 重试策略
- ✅ Redis 缓存键必带 TTL
- ✅ 大文件用 streaming response

##### 七、测试（~150 行）
- ✅ pytest + pytest-asyncio
- ✅ DB 测试用 testcontainers
- ✅ 覆盖率门槛：Service ≥ 80% / Repository ≥ 70%

##### 八、跨服务通信（~150 行）
- ✅ api → ai-orchestrator 必用 httpx + 超时 + 重试
- ✅ 禁止 Python 跨服务 import（workspace/README.md §三）
- ✅ 共享类型走 shared-protos

---

#### [NEW] [03-AI代码CR规范.md](file:///Users/micreeson/Desktop/AI/fdework/docs/code-review/03-AI代码CR规范.md)

**作用**：LangGraph + Prompt + RAG + LlmAdapter 专项

**预算行数**：~1100 行

**核心内容**：

##### 一、LangGraph Agent 规范（~250 行）
- ✅ Subgraph 单一职责（每个助手一个 Subgraph）
- ✅ State 用 TypedDict 严格类型
- ✅ Node 必处理异常（不让整个 graph 崩）
- ✅ 中间状态必有 checkpoint（便于断点续跑）

##### 二、Prompt 工程（~250 行）
- ✅ Prompt 必版本化（`prompts/v1/agent_t.md`）
- ✅ Prompt 必含 system + few-shot + 输出格式约束
- ✅ 禁止 hardcode 在 .py 文件中（必从文件加载）
- ✅ 变量插入必用 `{var}` 占位 + Jinja2 模板
- ✅ Prompt 长度控制（避免突破 context window）

##### 三、Function Calling / Tools（~200 行）
- ✅ Tool schema 必含 description + 参数说明
- ✅ Tool 执行必有超时 + 异常封装
- ✅ 危险 Tool（写操作）必走二次确认（actionCard）
- ✅ Tool 调用日志必含 input/output

##### 四、RAG 规范（~200 行）
- ✅ Embedding 必批量调用（避免单条循环）
- ✅ Milvus 检索必带 metadata filter（用户/项目隔离）
- ✅ Rerank 必有 fallback（rerank 失败用原始 score）
- ✅ Chunk 大小 / overlap 必有配置项

##### 五、LlmAdapter 抽象层（~150 行）
- ✅ 所有 LLM 调用必经 LlmAdapter（禁止直接调 SDK）
- ✅ 必支持 mock provider（测试环境）
- ✅ 必带 token 计费埋点
- ✅ 必带降级策略（主 provider 失败切备用）

##### 六、安全（Prompt 注入 / 敏感数据）（~150 行）
- ✅ 用户输入入 Prompt 前必脱敏（正则替换手机号/邮箱）
- ✅ 系统 Prompt 与用户输入必有明确分隔符
- ✅ Tool 调用结果必校验（防 Prompt 注入）
- ✅ 客户敏感数据（PRD §7.4）入 RAG 前必经审计

##### 七、测试（~100 行）
- ✅ Agent 必有 evaluation set（典型 case 集合）
- ✅ Prompt 变更必跑 regression（对比新旧输出）
- ✅ 二次确认机制必有 actionId 失效场景测试

## Verification Plan

### Automated Tests
- 不涉及（本期只产出文档）

### Manual Verification
执行完成后请逐项验证：
- [ ] 5 份文档全部落位 `docs/code-review/`（README + 00 + 01 + 02 + 03）
- [ ] README.md 4 个链接全部可点击且文件存在
- [ ] 4 份规范每份均按 6 大类组织 Checklist
- [ ] 每条规则配 1-2 段 good/bad 代码对照
- [ ] 4 份规范行数：00 ~900 / 01 ~1200 / 02 ~1300 / 03 ~1100（±15%）
- [ ] 引用的技术细节（异常码 / 跨服务边界 / 性能基线）均能在详细设计中找到对应来源
- [ ] read_lints 校验所有 Markdown 无错误

---
生成时间: 2026/4/28 22:44:38
planId: 
plan_status: review