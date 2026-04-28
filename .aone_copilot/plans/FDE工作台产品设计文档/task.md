# FDE 工作台 PRD + 整套 HTML 原型图 任务清单

## 阶段一：基础架构（目录 + 公共资源）
- [x] 1. 创建目录结构 `docs/prototype/{pages,assets/{css,js,images}}`
- [x] 2. 创建 `docs/prototype/assets/css/theme.css`（CSS Variables + 基础组件 + 4 助手徽章）
- [x] 3. 创建 `docs/prototype/assets/css/layout.css`（Header/Nav/Main/Copilot 三列布局）
- [x] 4. 创建 `docs/prototype/assets/css/copilot.css`（Copilot 侧边栏 + 4 类卡片：actionCard/report/nextSteps/searchResults）
- [x] 5. 创建 `docs/prototype/assets/css/pages.css`（各页面专属 + 首页 hero/特性卡/模块卡/截图墙）
- [x] 6. 创建 `docs/prototype/assets/js/icons.js`（SVG sprite 50+ Lucide 图标 + icoSvg helper）
- [x] 7. 创建 `docs/prototype/assets/js/copilot.js`（4 助手 copilotConfig + renderCopilot + badgeHtml + toggleCopilot + 全部 Mock 对话）
- [x] 8. 创建 `docs/prototype/assets/js/mention.js`（@ 引用 5 类业务对象 mentionData）
- [x] 9. 创建 `docs/prototype/assets/js/nav.js`(导航高亮 + 通用初始化）

## 阶段二：HTML 页面（按依赖顺序）
- [x] 10. 创建 `docs/prototype/index.html`（产品首页：Hero + 特性卡 + 8 模块卡 + 4 助手徽章墙 + 截图墙 + Footer）
- [x] 11. 创建 `docs/prototype/pages/dashboard.html`（工作台：欢迎横幅 + 4 统计卡 + 任务看板 + 三栏）
- [x] 12. 创建 `docs/prototype/pages/tasks.html`（任务中心 + 任务助手 T）
- [x] 13. 创建 `docs/prototype/pages/project-detail.html`（项目详情 + 项目助手 P）
- [x] 14. 创建 `docs/prototype/pages/coach.html`（FDE 教练 + 教练助手 C）
- [x] 15. 创建 `docs/prototype/pages/files.html`（文件中心 + 文件助手 F + 选中态）
- [x] 16. 创建 `docs/prototype/pages/ai-chat.html`（AI 对话中心三栏）

## 阶段三：PRD 文档
- [x] 17. 创建 `docs/FDE工作台产品需求文档.md`（标准八段式：定位/画像/场景/架构/详细功能/交互规范/非功能/上线计划）

## 阶段四：验证
- [ ] 18. 浏览器打开 `docs/prototype/index.html` 实测：首页正常 → 8 模块卡跳转正常 → 6 子页布局完整 → 4 页 Copilot 正确显示 + Mock 对话渲染（人工验证）
- [ ] 19. PRD 文档自查：与原型实现完全对齐（人工验证）

---
生成时间: 2026/4/28 16:16:19
planId: 97b18f0c-ed38-473b-8413-17dba24804ab