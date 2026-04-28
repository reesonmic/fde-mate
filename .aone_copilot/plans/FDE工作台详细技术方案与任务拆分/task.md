
# FDE 工作台详细技术方案与任务拆分 · 任务清单

## P1：目录结构设计（基础 · 优先级最高）
- [x] 创建 `docs/detail-design/00-目录结构设计.md`：完整目录树 + 9 份文档规划 + workspace 5 大模块结构 + 命名约定 + 跨模块引用约定 + 路径别名 + .gitignore
- [x] 创建 `docs/detail-design/README.md`：9 份文档导航 + 角色分流 + 任务认领流程

## P2：代码仓库骨架占位（与目录结构同步）
- [x] 创建 workspace/ 11 个关键 README 占位（workspace 总 README + 5 个一级模块 README + 5 个二级关键目录 README），落地目录树骨架

## P3：前端详细设计
- [x] 创建 `docs/detail-design/01-前端详细设计.md`：所有路径引用 P1 目录结构（完整 ~1100 行：脚手架 + 路由 + 6 类核心组件 + 类型 + Stores + APIs + Composables + CSS + 测试）

## P4：后端详细设计（部分完成 · 因长度受限被截断）
- [/] 创建 `docs/detail-design/02-后端详细设计.md`：已完成 1030 行，覆盖 §一脚手架 + §二 40+ API 签名 + §三 Pydantic + §四 Service + §五 Repository + §六中间件 + §七 30+ 异常码 + §八 SSE + §九 ActionService（最后截断在 stage 方法末尾，缺 verify/execute/cancel + §十权限 + §十一 Celery + §十二性能 + §十三测试）

## P5：AI 接入详细设计（重点 · 未开始）
- [ ] 创建 `docs/detail-design/03-AI接入详细设计.md`

## P6：数据存储详细设计（未开始）
- [ ] 创建 `docs/detail-design/04-数据存储详细设计.md`

## P7：部署运维详细设计（未开始）
- [ ] 创建 `docs/detail-design/05-部署运维详细设计.md`

## P8：AI 对话中心详细设计（未开始）
- [ ] 创建 `docs/detail-design/06-AI对话中心详细设计.md`

## P9：客户空间与文件中心详细设计（未开始）
- [ ] 创建 `docs/detail-design/07-客户空间与文件中心详细设计.md`

## P10：FDE 教练与系统设置详细设计（未开始）
- [ ] 创建 `docs/detail-design/08-FDE教练与系统设置详细设计.md`

## P11：任务总表（核心交付物 · 未开始）
- [ ] 创建 `docs/detail-design/任务总表.md`：约 100 个开发者级 Task（5 字段：ID/标题/描述/优先级/工时估算），按 M2/M3/M4 分组，含工时汇总 + 依赖图 + CSV 导入模板

## P12：定稿校验（未开始）
- [ ] 全文校验：9 份文档章节完整性 + workspace 目录到位 + 任务数量 90-110 + 路径引用准确
- [ ] read_lints 校验所有 Markdown


---
生成时间: 2026/4/28 20:19:06
planId: 