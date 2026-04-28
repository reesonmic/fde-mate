# 修正 FDE 术语定义（对标 Palantir）

## 改动背景

用户指出 PRD 中 FDE 术语含义错误。当前文档把 FDE 解释为：
- 全称：Field Delivery Engineer
- 中文：现场交付工程师

实际上本工作台对标的是 **Palantir 公司的 FDE 岗位**：
- 全称：**Forward Deployed Engineer**
- 中文：**前线部署工程师**
- 特点：深入客户现场，融合软件工程 + 业务理解 + 数据分析，端到端解决客户复杂业务问题（数据集成 / 数据建模 / 应用搭建 / 业务咨询）

> [!NOTE]
> Palantir 的 FDE 是其商业模式的核心：不只是"交付工程师"，而是直接驻场客户、深度参与业务、与客户共同打造解决方案的复合型岗位。本工作台正是为这类工作场景设计。

## Proposed Changes

### [MODIFY] [FDE工作台产品需求文档.md](file:///Users/micreeson/Desktop/AI/fdework/docs/FDE工作台产品需求文档.md)

#### 改动 1：§1.1 一句话定位（约第 16 行）
- 原文：`面向 FDE（Field Delivery Engineer，现场交付工程师）的 AI 原生工作台...`
- 改为：`面向 FDE（Forward Deployed Engineer，前线部署工程师，对标 Palantir 同名岗位）的 AI 原生工作台...`

#### 改动 2：附录 A 术语表（约第 441 行）
- 原文：`| FDE | Field Delivery Engineer | 现场交付工程师 |`
- 改为：`| FDE | Forward Deployed Engineer | 前线部署工程师，对标 Palantir 同名核心岗位：深入客户现场，融合软件工程 + 业务理解 + 数据分析，端到端交付复杂业务解决方案 |`

### 不需要改的内容
- 全文 grep 已确认 `Field Delivery` 和 `现场交付` 仅在上述 2 处出现
- 其他位置的"FDE"作为缩写继续沿用，无需修改
- 各章节描述的工作场景（项目交付/客户沟通/技术方案/最佳实践）本身就符合 Palantir FDE 的工作定义，无需调整

## Verification Plan

### 自动验证
- PRD 全文 grep `Field Delivery|现场交付`，结果应为 0
- PRD 全文 grep `Forward Deployed|前线部署`，应能找到 2 处（§1.1 + 附录 A）
- 附录 A 术语表 FDE 行使用新定义

### 人工验证
- 通读 §1.1 和附录 A，确认表述自然、术语统一


---
生成时间: 2026/4/28 17:43:39
planId: 97b18f0c-ed38-473b-8413-17dba24804ab
plan_status: review