# ai-orchestrator · AI 编排服务

Python 3.11 + FastAPI + LangGraph + Milvus + DashScope。

详细设计：[03-AI接入详细设计.md](../../docs/detail-design/03-AI接入详细设计.md)

## 定位

- 独立部署的 AI 编排服务（与业务 API 物理隔离）
- 多 Agent 编排（Router + 5 子 Agent：T/P/C/F/Chat）
- RAG 引擎（HybridRetriever：向量+ES+RRF+Rerank）
- 多模型路由 + 熔断 + 降级

## 启动

```bash
poetry install
cp .env.example .env
poetry run uvicorn app.main:app --reload --port 8090
```

## 关键依赖

- fastapi / langgraph ^0.0.30 / langchain ^0.1
- dashscope / openai
- pymilvus ^2.4 / sentence-transformers
- unstructured / pymupdf / python-docx
- jinja2（Prompt 模板）

## 与其他模块关系

- 被 `api/` 通过 HTTP 调用（`/ai/chat` SSE / `/ai/preview-action` / `/ai/execute-action` / `/ai/rag/*`）
- 反向调用 `api/` 查询业务数据
- **不被 `web/` 直接访问**

## 目录速览

```
app/
├── orchestrator/   # LangGraph 主图 + 子图
├── adapters/       # LlmAdapter（DashScope/IDEAlab/OpenAI/Mock）
├── prompts/        # Jinja2 Prompt 模板
├── tools/          # 16 个 Function Calling 工具
├── rag/            # 分片/Embedding/检索/Rerank
├── routing/        # 多模型路由 + 熔断
├── safety/         # 注入防御 + 输出脱敏
└── audit/          # AI 操作审计
```

完整目录见 [00-目录结构设计 §六](../../docs/detail-design/00-目录结构设计.md)。
