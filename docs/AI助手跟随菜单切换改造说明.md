# AI 助手跟随菜单切换改造

## 📋 改动概述

将 AI 助手从**顶部 Tab 切换**改为**跟随左侧菜单自动切换**，提升用户体验。

### 改动前
- 右侧 AI 助手面板顶部有 Tab 栏（T助手、P助手、C助手、F助手）
- 用户需要手动点击 Tab 切换助手
- 助手与当前页面可能不匹配

### 改动后
- 移除顶部 Tab 栏
- AI 助手自动跟随左侧菜单切换
- 当前菜单对应的助手自动显示在右侧面板
- 显示助手图标、名称和描述

---

## 🔧 技术实现

### 1. 修改文件清单

| 文件 | 改动说明 |
|------|----------|
| `src/components/copilot/CopilotPanel.vue` | 移除 Tabs，改为接收 props.assistantKey |
| `src/components/layout/AppLayout.vue` | 传递路由对应的助手 key |
| `src/router/index.ts` | 更新路由 meta.copilot 映射 |

### 2. 菜单与助手映射关系

| 菜单路径 | 菜单名称 | 助手 Key | 助手名称 |
|----------|----------|----------|----------|
| `/dashboard` | 仪表盘 | `chat` | 全局对话 |
| `/tasks` | 任务管理 | `task` | T助手 |
| `/projects` | 项目空间 | `project` | P助手 |
| `/customers` | 客户空间 | `chat` | 全局对话 |
| `/files` | 文件中心 | `file` | F助手 |
| `/coach` | FDE教练 | `coach` | C助手 |
| `/settings` | 系统设置 | `chat` | 全局对话 |

### 3. 核心代码变更

#### CopilotPanel.vue
```vue
<!-- 之前：使用 Tabs 手动切换 -->
<Tabs v-model:activeKey="activeTab" size="small">
  <Tabs.TabPane v-for="assistant in assistants" :key="assistant.key">
    ...
  </Tabs.TabPane>
</Tabs>

<!-- 现在：接收外部传入的助手 key -->
<div class="copilot-header-info">
  <div class="copilot-header-icon">{{ assistantConfig?.icon }}</div>
  <div class="copilot-header-content">
    <div class="copilot-header-name">{{ assistantConfig?.name }}</div>
    <div class="copilot-header-desc">{{ assistantConfig?.description }}</div>
  </div>
</div>
```

#### AppLayout.vue
```vue
<!-- 传递路由对应的助手 key -->
<CopilotPanel v-if="showCopilot" :assistant-key="copilotKey" class="app-copilot" />

<script setup>
const copilotKey = computed(() => (route.meta.copilot as string) || 'chat')
</script>
```

#### router/index.ts
```typescript
// 每个路由添加 meta.copilot 字段
{ 
  path: 'tasks', 
  meta: { 
    title: '任务中心', 
    copilot: 'task'  // 对应 T助手
  } 
}
```

---

## 🎨 UI 效果

### 助手面板头部（改动后）

```
┌─────────────────────────────────────┐
│ 📋  T助手                    [清空]  │
│     任务管理助手 - 帮助管理任务...   │
├─────────────────────────────────────┤
│                                     │
│         消息列表区域                 │
│                                     │
├─────────────────────────────────────┤
│         输入框区域                   │
└─────────────────────────────────────┘
```

### 样式特点
- **图标**: 24px 助手 emoji 图标
- **名称**: 14px 粗体显示助手名称
- **描述**: 11px 灰色显示助手描述
- **背景**: 浅灰色背景区分内容区

---

## ✅ 优势

1. **自动化**: 无需手动切换，助手自动匹配当前页面
2. **一致性**: 助手功能与页面功能保持一致
3. **简洁性**: 移除 Tab 栏，界面更简洁
4. **可扩展**: 新增页面只需在路由添加 `copilot` 字段

---

## 🔍 测试验证

### 测试步骤
1. 启动前端开发服务器
2. 访问不同菜单页面
3. 验证右侧助手面板自动切换
4. 验证助手名称、图标、描述正确显示
5. 验证消息会话独立（每个助手独立会话）

### 测试用例

| 测试场景 | 预期结果 |
|----------|----------|
| 进入任务管理页 | 显示 T助手 📋 |
| 进入项目空间页 | 显示 P助手 📁 |
| 进入 FDE 教练页 | 显示 C助手 👨‍🏫 |
| 进入文件中心页 | 显示 F助手 📄 |
| 进入仪表盘页 | 显示 全局对话 💬 |
| 在助手内发送消息 | 消息保存在对应助手会话 |
| 切换页面后再切回 | 保留之前的对话历史 |

---

## 📝 注意事项

1. **助手配置**: 确保 `src/config/assistants.ts` 中所有助手都有正确的 key
2. **路由配置**: 新增页面时务必添加 `meta.copilot` 字段
3. **会话保持**: 切换页面不会清空助手会话，历史消息保留
4. **降级处理**: 如果路由未配置 copilot，默认使用 `chat`（全局对话）

---

## 🚀 后续优化建议

1. **动画过渡**: 添加助手切换动画效果
2. **快捷提示**: 首次切换时显示助手能力提示
3. **上下文感知**: 根据页面内容自动添加上下文标签
4. **快捷键**: 支持快捷键快速切换助手

---

**改动日期**: 2026-05-08  
**改动类型**: 功能优化  
**影响范围**: 前端 UI 交互  
**向后兼容**: ✅ 是（API 无变更）
