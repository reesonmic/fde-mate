
# FDE 工作台测试用例编写计划

承接已完成的产品需求文档（PRD v1.0）+ 原型图（7 页）+ 技术方案，全面输出可执行的测试用例库。

## User Review Required

> [!IMPORTANT]
> **本计划只产出"测试用例文档"，不实际执行测试、不编写自动化测试代码、不接入测试管理平台**。
> 自动化脚本（Playwright/Pytest/Vitest）属于后续任务，本次不涉及。

> [!NOTE]
> **依据来源**：
> - PRD 全文：[FDE工作台产品需求文档.md](file:///Users/micreeson/Desktop/AI/fdework/docs/FDE工作台产品需求文档.md)（473 行，已读取）
> - 原型 7 页：[docs/prototype/pages/](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/pages)（dashboard/tasks/project-detail/coach/customers/files/ai-chat）
> - API 列表：[02-后端详细设计.md §二](file:///Users/micreeson/Desktop/AI/fdework/docs/detail-design/02-后端详细设计.md)（40+ API 完整签名）

## Proposed Changes

### 一、目录结构（新增）

新增 `docs/test-cases/` 目录，落位约 11 份测试用例文档 + 1 份总索引：

```
docs/test-cases/
├── README.md                    # 总索引（用例分布 + 用例编号规则 + 优先级说明 + 执行顺序）
├── 00-通用规范.md                # 用例编号/优先级/前置数据/账号矩阵/全局浏览器配置
├── 01-工作台.md                  # Dashboard（无 Copilot）
├── 02-任务中心-T助手.md          # Tasks 模块 + T 任务助手
├── 03-项目空间-P助手.md          # Project 模块 + P 项目助手
├── 04-客户空间.md                # Customer（无 Copilot）
├── 05-FDE教练-C助手.md           # Coach 模块 + C 教练专家 AI
├── 06-文件中心-F助手.md          # Files 模块 + F 文件助手
├── 07-AI对话中心.md              # 三栏布局 + 模式切换 + @引用
├── 08-系统设置.md                # 个人/通知/AI 模型设置
├── 09-Copilot通用与二次确认.md   # 4 助手共性 + actionCard + 4 类 AI 卡片
└── 10-跨模块通用.md              # 登录/权限/导航/搜索/响应式/兼容性
```

### 二、用例字段规范（00-通用规范.md 中明确）

每条用例统一 7 个基础字段：

| 字段 | 取值范围 | 说明 |
|------|---------|------|
| 用例 ID | TC-{模块}-{类型}-{NNN} | 模块：DASH/TASK/PROJ/CUST/COACH/FILE/CHAT/SET/COP/COMM；类型：F=功能/I=接口/U=UI |
| 模块 | 8 大模块 + Copilot/通用 | 对应文档归属 |
| 标题 | 一句话描述 | 30 字内 |
| 优先级 | P0/P1/P2/P3 | P0=阻塞主流程；P1=核心功能；P2=次要功能；P3=边缘场景 |
| 前置条件 | 账号/数据/页面状态 | 引用通用规范的账号矩阵 |
| 测试步骤 | 编号步骤列表 | 每步一行，明确操作对象 |
| 预期结果 | 编号预期列表 | 与步骤一一对应 |

### 三、用例分布与数量预估（约 410 条）

---

#### [NEW] [README.md](file:///Users/micreeson/Desktop/AI/fdework/docs/test-cases/README.md)

**作用**：测试用例总索引

**核心内容**：
- 11 份文档目录（带链接）
- 用例编号规则速查表
- 优先级定义（P0-P3）
- 推荐执行顺序（冒烟 → P0 → P1 → P2/P3）
- 用例总数汇总表（按模块/优先级/类型统计）
- 与 PRD/原型/技术方案的对应关系

---

#### [NEW] [00-通用规范.md](file:///Users/micreeson/Desktop/AI/fdework/docs/test-cases/00-通用规范.md)

**作用**：所有用例文档共用规范基线

**核心内容**：
- 用例 ID 编号规则（TC-{模块}-{类型}-{NNN}）
- 7 个基础字段定义与示例
- 优先级定义与使用场景（P0/P1/P2/P3）
- **测试账号矩阵**（基于 PRD §2.1）：
  | 账号 | 角色 | 用途 |
  |---|---|---|
  | fde_p5_01 | P5 初级 FDE | 权限受限测试 |
  | fde_p6_01 | P6 资深 FDE | 主流程测试 |
  | fde_p7_01 | P7 TL | 团队管理/全局视图测试 |
  | admin_01 | 系统管理员 | 配置/审计测试 |
- **测试数据基线**（推荐种子数据：3 个客户/2 个项目/10 个任务/5 个文件/3 个最佳实践）
- **浏览器矩阵**（PRD §7.3）：Chrome 100+ / Safari 15+ / Edge 100+
- **分辨率矩阵**（PRD §6.4）：1280×800 / 1440×900 / 1920×1080

---

#### [NEW] [01-工作台.md](file:///Users/micreeson/Desktop/AI/fdework/docs/test-cases/01-工作台.md)

**作用**：Dashboard 模块用例（无 Copilot）

**用例数预估**：~30 条

**覆盖功能点**（参考 [dashboard.html](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/pages/dashboard.html) + PRD §场景 1）：
- 欢迎横幅（今日聚焦：P0 任务/客户会议/周报数）
- "帮我准备晨会"按钮（生成晨会摘要）
- 4 张统计卡（任务/项目/客户/文件计数）
- 最近任务列表（默认 10 条）
- 最近项目列表（默认 5 条）
- 通知列表 / 关键事件流
- 跳转交互（点卡片跳子模块）

**用例类型分布**：功能 18 + UI 8 + 接口 4

---

#### [NEW] [02-任务中心-T助手.md](file:///Users/micreeson/Desktop/AI/fdework/docs/test-cases/02-任务中心-T助手.md)

**作用**：任务模块 CRUD + T 任务助手对话

**用例数预估**：~55 条

**覆盖功能点**：
- 任务列表（关键词/状态/责任人/项目/优先级 5 维筛选）
- 任务详情（基本信息/评论/历史）
- 任务 CRUD（创建/更新/删除）
- 批量操作（批量更新状态、批量指派）
- **批量更新 > 10 项触发二次确认**（PRD §6.2.4）
- T 助手 4 大对话场景（PRD §5.2.2）：欢迎语 / 创建任务（actionCard）/ 批量延期（actionCard + impact）/ 工作量分析（report）

**接口用例**（基于 02-后端详细设计.md §2.4）：
- POST /tasks 参数校验（标题非空/长度 ≤ 200/优先级枚举）
- POST /tasks/batch-update-status 高危 actionId 校验
- 越权访问（FDE 访问其他人任务返回 403）

**用例类型分布**：功能 30 + UI 12 + 接口 13

---

#### [NEW] [03-项目空间-P助手.md](file:///Users/micreeson/Desktop/AI/fdework/docs/test-cases/03-项目空间-P助手.md)

**作用**：项目模块 + P 项目助手

**用例数预估**：~55 条

**覆盖功能点**（参考 [project-detail.html](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/pages/project-detail.html) + PRD §5.3）：
- 项目列表 / 项目详情头（健康度环 SVG）
- 7 Tabs（概览/任务/里程碑/文件/风险/团队/时间线）
- 里程碑时间轴（M1-M5 状态色）
- 项目成员管理（添加/移除）
- 风险列表（红黄绿分级 + 处理人）
- 周报触发生成（异步任务）
- P 助手 4 场景：欢迎语 / 风险分析（report）/ 修改负责人（actionCard）/ 周报生成

**用例类型分布**：功能 30 + UI 14 + 接口 11

---

#### [NEW] [04-客户空间.md](file:///Users/micreeson/Desktop/AI/fdework/docs/test-cases/04-客户空间.md)

**作用**：客户模块（v1.0 无 Copilot）

**用例数预估**：~35 条

**覆盖功能点**（参考 [customers.html](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/pages/customers.html) + PRD §5.5）：
- 4 张统计卡（战略客户/在交付项目/季度商机/健康度告警）
- 双栏：360px 客户列表 + 客户详情
- 4 筛选 tab（全部/战略/重点/一般）
- customer-overview banner（logo + 3 KPI）
- 5 Tabs（概览/联系人/商机/历史项目/文件）
- 联系人 CRUD
- 数据脱敏（PRD §7.4 客户敏感数据脱敏展示）

**用例类型分布**：功能 18 + UI 12 + 接口 5

---

#### [NEW] [05-FDE教练-C助手.md](file:///Users/micreeson/Desktop/AI/fdework/docs/test-cases/05-FDE教练-C助手.md)

**作用**：教练模块 + C 教练专家 AI

**用例数预估**：~45 条

**覆盖功能点**（参考 [coach.html](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/pages/coach.html) + PRD §5.4）：
- page-header + "向专家提问"按钮（聚焦 Copilot 输入框）
- 4 大入口卡（专家 AI/最佳实践/方法论/学习路径，顶部 3px 渐变条）
- 最佳实践 5 场景 tabs（项目启动/客户沟通/技术方案/风险管控/验收交付）
- 实践卡详情 + 评分
- SOP 库 + 下载（计数 +1）
- 学习路径 + 章节进度更新（章节解锁顺序）
- 个性化推荐（基于项目阶段）
- C 助手 4 场景：欢迎语（86 案例 + 128 SOP 提示）/ Next Step（nextSteps 卡）/ 最佳实践（report）/ 专家咨询

**用例类型分布**：功能 22 + UI 13 + 接口 10

---

#### [NEW] [06-文件中心-F助手.md](file:///Users/micreeson/Desktop/AI/fdework/docs/test-cases/06-文件中心-F助手.md)

**作用**：文件模块 + F 文件助手

**用例数预估**：~50 条

**覆盖功能点**（参考 [files.html](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/pages/files.html) + PRD §5.6）：
- 文件树（个人/项目/客户/共享/回收站）
- 路径面包屑动态展示
- 6 类文件类型彩色图标（folder/pdf/doc/xls/ppt/img）
- 选中态（橙边框 + "已选"角标）
- 容量进度条（已用/总量）
- OSS STS 上传凭证 + 分片上传（含上传完成回调触发 RAG 索引）
- 批量删除 / 批量归档（批量 > 10 项二次确认）
- 配额超限提示
- F 助手 4 场景：欢迎语 / 智能搜索（searchResults）/ 文档总结（report）/ 批量归档（actionCard + impact）

**用例类型分布**：功能 28 + UI 12 + 接口 10

---

#### [NEW] [07-AI对话中心.md](file:///Users/micreeson/Desktop/AI/fdework/docs/test-cases/07-AI对话中心.md)

**作用**：独立 AI 对话页用例

**用例数预估**：~50 条

**覆盖功能点**（参考 [ai-chat.html](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/pages/ai-chat.html) + PRD §5.7）：
- 三栏布局（左历史 / 中对话 / 右上下文）
- 历史列表分组（今天/昨天/更早）+ 历史搜索 + 删除会话
- 对话模式切换（智能/创意/严谨）+ 模式参数差异
- **SSE 流式响应**：首 token < 1s（PRD §7.1）/ 中途断流恢复 / 流式取消
- @ 引用 5 类 tab（项目/任务/客户/文件/案例）+ 弹窗响应 < 100ms
- 引用 tag 单独移除
- 上下文持久化与恢复
- 对话导出
- 消息反馈（👍/👎）

**用例类型分布**：功能 25 + UI 13 + 接口 12

---

#### [NEW] [08-系统设置.md](file:///Users/micreeson/Desktop/AI/fdework/docs/test-cases/08-系统设置.md)

**作用**：用户设置模块

**用例数预估**：~25 条

**覆盖功能点**：
- 个人偏好（昵称/邮箱/头像）
- 修改密码（旧密码校验 + 新密码强度 + 二次确认）
- 通知配置（钉钉/邮件/站内信开关）
- AI 模型选择（GPT-4 / Claude / 通义千问）
- 登录/登出 / Token 刷新

**用例类型分布**：功能 15 + UI 4 + 接口 6

---

#### [NEW] [09-Copilot通用与二次确认.md](file:///Users/micreeson/Desktop/AI/fdework/docs/test-cases/09-Copilot通用与二次确认.md)

**作用**：4 助手共性能力 + 写操作核心机制

**用例数预估**：~40 条

**覆盖功能点**（PRD §6.2 + §6.3）：
- Copilot 三态宽度（默认 400px / 折叠 56px / 隐藏 0px）
- 助手随页面切换（< 200ms）
- Context 区自动感知 + 手动 @ 添加 + tag 单独移除
- 4 个推荐建议 chip 一键发送
- 输入工具栏（@/ 附件 / AI 增强 / 发送）
- **二次确认机制完整覆盖**：
  - actionCard 字段对比（旧值 del / 新值 add）
  - 状态徽章（待确认/执行中/已完成）
  - impact 折叠展开
  - 60s actionId 过期（HTTP 410 BIZ_ACTION_EXPIRED）
  - 用户不匹配（HTTP 403 BIZ_ACTION_USER_MISMATCH）
  - 工具名不匹配（HTTP 422 BIZ_ACTION_TOOL_MISMATCH）
  - 取消操作流程
- **4 类 AI 卡片渲染**（actionCard/report/nextSteps/searchResults）
- AI 服务降级（断流时显示 mock + 友好提示）
- 助手徽章 4 尺寸（sm/md/lg/xl）

**用例类型分布**：功能 20 + UI 8 + 接口 12

---

#### [NEW] [10-跨模块通用.md](file:///Users/micreeson/Desktop/AI/fdework/docs/test-cases/10-跨模块通用.md)

**作用**：跨模块共性 + 非功能性

**用例数预估**：~25 条

**覆盖功能点**：
- 登录/登出/Token 过期跳转
- 全局导航 8 模块切换（< 200ms）
- 全局搜索（多模块对象聚合）
- **数据隔离权限**（PRD §7.4，个人/项目/客户三级 ACL）
- 暗色模式（v1.1 不做，本期验证降级表现）
- 浏览器兼容性（Chrome/Safari/Edge）
- 分辨率适配（1280×800 / 1440×900 / 1920×1080）
- 性能基线验证：首屏 < 1.5s / 页面切换 < 200ms / @ 弹窗 < 100ms / SSE 首 token < 1s（PRD §7.1）
- 安全基线（XSS/CSRF/越权 401/403）

**用例类型分布**：功能 12 + UI 4 + 接口 9

---

### 四、用例数量汇总

| 文档 | 模块 | 功能 | UI | 接口 | 合计 |
|------|------|------|------|------|------|
| 01 | 工作台 | 18 | 8 | 4 | 30 |
| 02 | 任务中心 + T | 30 | 12 | 13 | 55 |
| 03 | 项目空间 + P | 30 | 14 | 11 | 55 |
| 04 | 客户空间 | 18 | 12 | 5 | 35 |
| 05 | FDE 教练 + C | 22 | 13 | 10 | 45 |
| 06 | 文件中心 + F | 28 | 12 | 10 | 50 |
| 07 | AI 对话中心 | 25 | 13 | 12 | 50 |
| 08 | 系统设置 | 15 | 4 | 6 | 25 |
| 09 | Copilot 通用 + 二次确认 | 20 | 8 | 12 | 40 |
| 10 | 跨模块通用 | 12 | 4 | 9 | 25 |
| **合计** | | **218** | **100** | **92** | **410** |

### 五、用例样例（以 TC-TASK-F-001 为例，确认风格）

```markdown
### TC-TASK-F-001 创建普通任务（主流程）

| 字段 | 值 |
|------|-----|
| 模块 | 任务中心 |
| 优先级 | P0 |
| 类型 | 功能 |
| 前置条件 | 1. 已用 fde_p6_01 登录；2. 已存在项目"阿里云A数据中台"（id=10001） |

**测试步骤**：
1. 进入「任务中心」页面，点击右上角「+ 新建任务」
2. 输入标题"完成客户A的POC方案"，优先级选 P0，截止日期选明天，关联项目选"阿里云A数据中台"
3. 点击「保存」

**预期结果**：
1. 弹窗打开，必填项标"*"
2. 表单各字段值正确填入并显示项目下拉
3. 弹窗关闭，列表顶部出现新任务，状态=todo，创建者=fde_p6_01，HTTP 201
```

## Verification Plan

### Automated Tests
- 不涉及（本期只产出文档）

### Manual Verification
执行完成后请逐项验证：
- [ ] 11 份文档全部落位 `docs/test-cases/`
- [ ] README.md 11 个链接全部可点击且文件存在
- [ ] 用例总数 ≥ 380 条（预算 410，浮动 ±10%）
- [ ] 用例 ID 全局唯一无重复
- [ ] 每条用例 7 个基础字段全部填写
- [ ] P0 用例数 ≥ 80（覆盖各模块主流程）
- [ ] 关键非功能性指标（PRD §7）有专项用例
- [ ] 4 类 AI 卡片（actionCard/report/nextSteps/searchResults）渲染各有专项用例
- [ ] 二次确认机制 5 种异常路径（过期/用户不匹配/工具不匹配/不存在/取消）全部覆盖
- [ ] read_lints 校验所有 Markdown 无错误


---
生成时间: 2026/4/28 21:55:48
planId: 
plan_status: review