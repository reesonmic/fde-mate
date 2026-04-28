# web · 前端应用

Vue 3 + TypeScript + Vite + Pinia + Ant Design Vue。

详细设计：[01-前端详细设计.md](../../docs/detail-design/01-前端详细设计.md)

## 启动

```bash
npm install
cp .env.example .env.development
npm run dev          # 开发模式（默认 Mock，VITE_USE_MOCK=true）
npm run dev:real     # 连真实后端
npm run build        # 生产构建
npm run test         # 单元测试
npm run gen:types    # 从 shared-protos/openapi/api.json 生成 TS 类型
```

## 关键依赖

- vue ^3.4 / vue-router ^4 / pinia ^2
- vite ^5 / typescript ^5
- ant-design-vue ^4
- axios ^1 / @microsoft/fetch-event-source（SSE）
- msw ^2（Mock Service Worker）
- vitest（测试）

## 与其他模块关系

- 调用 `api/` 通过 HTTPS REST + SSE
- 类型来源于 `shared-protos/openapi/api.json`
- **不直接调用 `ai-orchestrator/`**

## 目录速览

```
src/
├── apis/         # HTTP 客户端 + Mock
├── components/   # common/layout/copilot/business
├── composables/  # useSSEChat / useCopilot / useMention
├── pages/        # 路由页面（按业务域）
├── router/       # Vue Router
├── stores/       # Pinia
├── styles/       # CSS token
└── types/        # TS 类型
```

完整目录见 [00-目录结构设计 §四](../../docs/detail-design/00-目录结构设计.md)。
