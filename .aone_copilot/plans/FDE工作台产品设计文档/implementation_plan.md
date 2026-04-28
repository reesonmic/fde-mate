# FDE 工作台产品需求文档 + 整套 HTML 原型图（v1.0 正式产出物）

## 改造背景

历经 .changes/ 下的多轮 prototype 迭代，FDE 工作台的产品形态、4 个 Copilot 体系（任务 T 蓝 / 项目 P 紫 / 教练 C 青 / 文件 F 橙）已稳定。现需在仓库根目录新建 `docs/` 文件夹，沉淀两份正式交付物：

1. **`docs/FDE工作台产品需求文档.md`** - 标准 PRD 八段式
2. **`docs/prototype/`** - 整套 HTML 原型图，**单首页 + 子页跳转模式**

> [!IMPORTANT]
> 本次交付物**不包含**用户最近提到的"工作台助手 W"功能，聚焦 4 个稳定 Copilot 体系（T/P/C/F）。W 助手另议。

> [!NOTE]
> 现有 `.changes/新增-FDE工作台-20260428/prototype/index.html` 是单文件多页面 SPA 模式，作为本次新原型的**视觉与交互蓝本**，新原型重新拆分为**多文件分页结构**并升级精致度。

## Proposed Changes

### 1. 目录结构

```
docs/
├── FDE工作台产品需求文档.md          # PRD 主文档
└── prototype/
    ├── index.html                    # 产品首页（介绍 + 模块导航 + 截图墙）
    ├── pages/
    │   ├── dashboard.html            # 工作台
    │   ├── tasks.html                # 任务中心（含任务助手 T）
    │   ├── project-detail.html       # 项目详情（含项目助手 P）
    │   ├── coach.html                # FDE 教练（含教练助手 C）
    │   ├── files.html                # 文件中心（含文件助手 F）
    │   └── ai-chat.html              # AI 对话中心（全局）
    └── assets/
        ├── css/
        │   ├── theme.css             # 设计令牌 + 基础组件（按钮/卡片/标签/徽章/dot）
        │   ├── layout.css            # 全局布局（Header / 左侧 Nav / 主区 / 右侧 Copilot）
        │   ├── pages.css             # 各页面专属样式
        │   └── copilot.css           # AI Copilot 侧边栏样式
        ├── js/
        │   ├── icons.js              # SVG sprite（Lucide 风格）
        │   ├── copilot.js            # Copilot 配置（4 助手）+ renderCopilot
        │   ├── mention.js            # @ 引用弹窗
        │   └── nav.js                # 导航高亮 / 页面通用初始化
        └── images/                   # （可选）截图占位
```

### 2. PRD 文档（标准八段式）

#### [NEW] [FDE工作台产品需求文档.md](file:///Users/micreeson/Desktop/AI/fdework/docs/FDE工作台产品需求文档.md)

```markdown
# FDE 工作台产品需求文档 v1.0

## 1. 产品定位
- 一句话：面向 FDE（Field Delivery Engineer 现场交付工程师）的 AI 原生工作台，让交付更可控、更高效、更专业。
- 解决问题：信息分散（任务/项目/客户/文件四处找）、能力依赖个人经验（新人难成长）、AI 时代的工具孤岛（AI 助手散落）。
- 价值主张：① 一站式工作中枢 ② AI Copilot 嵌入每一个核心场景 ③ 沉淀方法论 + 案例库 + 智能教练

## 2. 用户画像
- **核心用户**：FDE 交付工程师（P5-P7），日均处理 5-10 个任务、并行 2-4 个交付项目
- **典型痛点**：跨系统切换成本高、客户沟通缺乏专业话术训练、文档管理混乱
- **使用场景**：晨会准备、任务跟进、客户沟通、方案撰写、案例学习

## 3. 核心场景
- 场景 1：晨间一站式查看 - 工作台聚合任务/项目/学习
- 场景 2：AI 协助任务管理 - 任务助手 T 创建/批量调整
- 场景 3：项目实施 + 风险预警 - 项目助手 P 智能分析
- 场景 4：FDE 能力成长 - 教练助手 C 个性化指导 + AI 对练
- 场景 5：智能文件管理 - 文件助手 F 搜索/总结/归档

## 4. 功能架构

### 4.1 8 大功能模块
- 工作台 / 任务中心 / 项目空间 / 客户空间 / FDE 教练 / 文件中心 / AI 对话 / 系统设置

### 4.2 4 个页面级 AI Copilot
| 助手 | 字母 | 配色 | 服务页面 | 核心能力 |
|------|------|------|----------|----------|
| 任务助手 T | T | 蓝 #1677FF | 任务中心 | 创建/查询/批量调整/工作量分析 |
| 项目助手 P | P | 紫 #722ED1 | 项目详情 | 风险分析/周报/成员调整/里程碑 |
| 教练助手 C | C | 青 #13C2C2 | FDE 教练 | Next Step/案例推荐/AI 对练 |
| 文件助手 F | F | 橙 #FA8C16 | 文件中心 | 智能搜索/文档总结/批量归档/RAG 问答 |

### 4.3 全局 AI 对话中心
- 跨场景对话历史 + 三种对话模式（智能/创意/严谨）+ @ 引用任意业务对象

## 5. 详细功能（按页面 + 按助手）

### 5.1 工作台（Dashboard）
- 5.1.1 欢迎横幅（蓝色渐变 + 个性化问候）
- 5.1.2 4 张统计卡（待办任务/在交付项目/项目健康度/AI 对练时长）
- 5.1.3 任务看板（4 列拖拽：待办/进行中/复核中/已完成）
- 5.1.4 今日日程 / 项目进度 / 学习推荐 三栏

### 5.2 任务中心 + 任务助手 T
- 5.2.1 任务列表（4 列状态切换 + 优先级 P0/P1/P2 + 截止时间）
- 5.2.2 工具栏：导入 / 新建任务 / 视图切换
- 5.2.3 **任务助手 T**（蓝色 T 徽章）
  - 上下文：当前任务列表上下文
  - 4 段 Mock 对话：欢迎 / 创建 P0 任务 / 批量延期 / 工作量分析

### 5.3 项目详情 + 项目助手 P
- 5.3.1 项目信息头（健康度环 + 关键指标）
- 5.3.2 5 个里程碑时间轴
- 5.3.3 项目成员 + 风险列表 + 关键文档
- 5.3.4 **项目助手 P**（紫色 P 徽章）
  - 上下文：自动绑定当前项目
  - 4 段 Mock 对话：欢迎 / 风险分析 report / 修改负责人 actionCard / 周报生成

### 5.4 FDE 教练 + 教练助手 C
- 5.4.1 4 大入口卡（方法论库 / 学习路径 / 案例库 / AI 对练）
- 5.4.2 推荐学习卡片
- 5.4.3 4 个 AI 对练剧本
- 5.4.4 **教练助手 C**（青色 C 徽章）
  - 上下文：当前项目阶段 + 我的等级
  - 4 段 Mock 对话：欢迎 / Next Step nextSteps / 启动 AI 对练

### 5.5 文件中心 + 文件助手 F
- 5.5.1 文件树（个人空间 / 项目空间 / 客户空间 / 共享 / 回收站）
- 5.5.2 文件网格（folder/pdf/doc/xls/ppt/img 多色文件类型）
- 5.5.3 选中态视觉（橙色边框 + "已选"角标）
- 5.5.4 **文件助手 F**（橙色 F 徽章）
  - 上下文：当前路径 + 选中文件
  - 4 段 Mock 对话：欢迎 / 智能搜索 searchResults / 文档总结 report / 批量归档 actionCard

### 5.6 AI 对话中心
- 5.6.1 三栏布局（左侧历史 + 中间对话 + 右侧上下文）
- 5.6.2 三种对话模式 tab
- 5.6.3 @ 引用 5 类业务对象（项目/任务/客户/文件/案例）

## 6. 交互规范

### 6.1 设计系统
- **色彩**：主色 #1677FF / 4 助手色（T 蓝 / P 紫 / C 青 / F 橙）/ 6 文件类型色 / 4 状态色
- **图标**：Lucide 风格线性 SVG（24x24 viewBox / 1.5px stroke）
- **徽章**：渐变方块字母徽章，3 种尺寸（24/32/40px）
- **状态 dot**：6px 圆点 + 光晕，4 种状态（success/warning/danger/info）

### 6.2 Copilot 交互规范
- 默认右侧展开 400px / 折叠 56px
- 上下文 tag 区（自动感知 + 可手动 @ 添加）
- 推荐 chip（4 条建议问题）
- 输入工具栏（@ / 附件 / AI 增强）
- 写操作必须先预览 actionCard，确认后才执行

### 6.3 响应式
- 主断点：桌面端（≥1280px），目标分辨率 1440x900

## 7. 非功能性需求

### 7.1 性能
- 首屏加载 < 1.5s（不含 AI 响应）
- AI 助手切换 < 200ms
- @ 引用弹窗响应 < 100ms

### 7.2 可用性
- 7×24 可用性 ≥ 99.9%
- AI 服务降级方案（断流时显示离线 mock）

### 7.3 兼容性
- Chrome 100+ / Safari 15+ / Edge 100+
- 暗色模式（v1.1 规划，本期不做）

### 7.4 安全
- 所有客户数据脱敏展示
- AI 对话写操作二次确认

## 8. 上线计划

### 8.1 里程碑
- M1（第 4 周）：6 个核心页面 + 4 助手 Mock 对话上线（本次原型阶段）
- M2（第 8 周）：4 助手对接真实 LLM（GPT-4 / Claude / 通义千问）
- M3（第 12 周）：@ 引用对接真实业务数据 + 工作台助手 W
- M4（第 16 周）：AI 对练接入语音 / 周报自动归档

### 8.2 验收指标
- DAU 占比 > 60%（FDE 团队覆盖率）
- AI 助手日均交互次数 > 8 次/人
- 任务平均创建时长缩短 50%
- FDE 新人 onboard 周期缩短 30%
```

### 3. HTML 原型图

#### [NEW] [docs/prototype/index.html](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/index.html) - 产品首页

```html
<!-- 结构：
1. 顶部 Hero 区：产品 Logo + Slogan + CTA（"进入工作台"按钮）
2. 产品介绍：3 张特性卡片（一站式工作 / AI Copilot / FDE 成长）
3. 模块导航：8 张卡片（每张含图标+标题+描述+"进入" 按钮，跳转到 pages/xxx.html）
4. AI Copilot 体系展示：4 助手徽章墙（T/P/C/F 横排，各含徽章+名称+定位+核心能力）
5. 截图墙：6 张核心页面预览缩略图（点击放大或跳转子页）
6. 底部 Footer：版本信息 / 更新日志链接
-->
```

#### [NEW] [docs/prototype/pages/dashboard.html](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/pages/dashboard.html) - 工作台

完整页面结构（左 Nav + 主区欢迎横幅 + 4 统计卡 + 任务看板 + 三栏），从现有 `.changes/.../prototype/index.html` 抽取 Dashboard 部分并升级。

#### [NEW] [docs/prototype/pages/tasks.html](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/pages/tasks.html) - 任务中心 + T 助手

页面 + 右侧任务助手 T。

#### [NEW] [docs/prototype/pages/project-detail.html](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/pages/project-detail.html) - 项目详情 + P 助手

#### [NEW] [docs/prototype/pages/coach.html](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/pages/coach.html) - FDE 教练 + C 助手

#### [NEW] [docs/prototype/pages/files.html](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/pages/files.html) - 文件中心 + F 助手

#### [NEW] [docs/prototype/pages/ai-chat.html](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/pages/ai-chat.html) - AI 对话中心

### 4. 公共资源（CSS / JS）

#### [NEW] [docs/prototype/assets/css/theme.css](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/assets/css/theme.css)
- CSS Variables（主色、4 助手徽章渐变、6 文件类型色、状态色、间距、圆角、阴影）
- 基础组件（.btn / .tag / .card / .assistant-badge / .status-dot / .ico）

#### [NEW] [docs/prototype/assets/css/layout.css](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/assets/css/layout.css)
- 全局布局（.header / .nav / .main / .copilot 三列）
- 通用页面骨架（.page-header / .page-title / .page-body）

#### [NEW] [docs/prototype/assets/css/pages.css](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/assets/css/pages.css)
- 各页面专属样式（dashboard 看板、tasks 列表、project 时间轴、coach 入口卡、files 网格、ai-chat 三栏）
- 首页 index.html 专属（hero / 特性卡 / 模块卡 / 截图墙）

#### [NEW] [docs/prototype/assets/css/copilot.css](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/assets/css/copilot.css)
- AI Copilot 侧边栏（header/context/body/input/footer/collapsed）
- actionCard / report / nextSteps / searchResults 4 类卡片

#### [NEW] [docs/prototype/assets/js/icons.js](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/assets/js/icons.js)
- SVG sprite 注入（50+ Lucide 图标）+ icoSvg(id, cls) 工具函数

#### [NEW] [docs/prototype/assets/js/copilot.js](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/assets/js/copilot.js)
- copilotConfig（4 助手配置：tasks / project-detail / coach / files）
- renderCopilot(pageId) + badgeHtml() + toggleCopilot()
- 4 助手 Mock 对话内容（欢迎语 + 写操作 actionCard + report 卡 + nextSteps + searchResults）

#### [NEW] [docs/prototype/assets/js/mention.js](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/assets/js/mention.js)
- @ 引用弹窗（5 类业务对象 mentionData：project / task / customer / file / case）

#### [NEW] [docs/prototype/assets/js/nav.js](file:///Users/micreeson/Desktop/AI/fdework/docs/prototype/assets/js/nav.js)
- 导航高亮（基于当前 HTML 文件名）
- 通用初始化（注入 sprite / 渲染 Copilot / 绑定 @ 弹窗）

### 5. 子页面统一模板

每个 pages/*.html 都遵循统一模板：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>页面名 - FDE 工作台</title>
  <link rel="stylesheet" href="../assets/css/theme.css">
  <link rel="stylesheet" href="../assets/css/layout.css">
  <link rel="stylesheet" href="../assets/css/pages.css">
  <link rel="stylesheet" href="../assets/css/copilot.css">
</head>
<body data-page="xxx">
  <!-- icons sprite 注入位 -->
  <div id="svg-sprite-mount"></div>
  <!-- Header -->
  <header class="header">...</header>
  <!-- Nav -->
  <aside class="nav">...</aside>
  <!-- Main 页面专属内容 -->
  <main class="main">...</main>
  <!-- Copilot -->
  <aside class="copilot" id="copilot">...</aside>
  <!-- @ 引用弹窗 -->
  <div id="mention-modal">...</div>

  <script src="../assets/js/icons.js"></script>
  <script src="../assets/js/copilot.js"></script>
  <script src="../assets/js/mention.js"></script>
  <script src="../assets/js/nav.js"></script>
</body>
</html>
```

`<body data-page="xxx">` 中的 `xxx` 用于 nav.js 自动高亮 + copilot.js 选择对应配置渲染。

## Verification Plan

### 自动验证
- 浏览器打开 `docs/prototype/index.html`，首页正常展示（Hero / 特性卡 / 模块卡 / 4 助手徽章墙 / 截图墙）
- 点击任意模块卡片跳转到对应 pages/xxx.html
- 6 个子页面 Header/Nav/Main 布局正常，Tasks/Project/Coach/Files 4 页右侧 Copilot 正确渲染（T/P/C/F 4 色徽章）
- Dashboard 和 AI 对话中心右侧 Copilot 隐藏（无配置）
- 各助手 Mock 对话内容、操作预览卡、@ 引用弹窗等交互正常

### 人工验证
- PRD 文档八段式完整，与原型实现一致
- 4 助手色彩矩阵协调（T 蓝 / P 紫 / C 青 / F 橙）
- 整体精致度高于现有 .changes 下的 prototype（更适合作为正式交付物）
- 多文件结构便于后续按页面分头维护

> [!WARNING]
> 本次输出物**完全独立**于 `.changes/新增-FDE工作台-20260428/prototype/index.html`，不修改原文件，老原型可保留作为开发草稿。


---
生成时间: 2026/4/28 16:16:19
planId: 97b18f0c-ed38-473b-8413-17dba24804ab
plan_status: review