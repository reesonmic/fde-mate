"""
LLM provider wrapper - supports DashScope, OpenAI, and Mock.
"""
from abc import ABC, abstractmethod
from typing import AsyncIterator

from app.config import settings


class LlmProvider(ABC):
    @abstractmethod
    async def stream(self, messages: list[dict]) -> AsyncIterator[str]:
        pass


class DashScopeLlm(LlmProvider):
    """DashScope (通义千问) streaming LLM."""

    def __init__(self) -> None:
        from langchain_openai import ChatOpenAI
        self._model = ChatOpenAI(
            model=settings.dashscope_model,
            openai_api_key=settings.dashscope_api_key,
            openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
            streaming=True,
            timeout=30,
        )

    async def stream(self, messages: list[dict]) -> AsyncIterator[str]:
        async for chunk in self._model.astream(messages):
            content = chunk.content
            if content:
                yield str(content)


class OpenAiLlm(LlmProvider):
    """OpenAI streaming LLM."""

    def __init__(self) -> None:
        from langchain_openai import ChatOpenAI
        self._model = ChatOpenAI(
            model=settings.openai_model,
            openai_api_key=settings.openai_api_key,
            streaming=True,
            timeout=30,
        )

    async def stream(self, messages: list[dict]) -> AsyncIterator[str]:
        async for chunk in self._model.astream(messages):
            content = chunk.content
            if content:
                yield str(content)


class MockLlm(LlmProvider):
    """Mock LLM for development/testing."""

    async def stream(self, messages: list[dict]) -> AsyncIterator[str]:
        last_user = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                last_user = msg.get("content", "")
                break

        response = self._get_mock_response(last_user)
        for char in response:
            yield char

    def _get_mock_response(self, query: str) -> str:
        """Simple mock responses based on query keywords."""
        q = query.lower()
        if "任务" in query or "task" in q:
            return (
                f"收到关于任务的查询：「{query}」。\n\n"
                "当前有以下建议：\n"
                "1. 查看本周的待办任务\n"
                "2. 分析任务风险\n"
                "3. 生成任务周报\n\n"
                "请确认是否需要执行具体操作？"
            )
        elif "周报" in query or "报告" in query:
            return (
                f"收到报告生成请求：「{query}」。\n\n"
                "**本周工作摘要**\n"
                "- 完成任务 12 个\n"
                "- 进行中任务 5 个\n"
                "- 延期风险任务 2 个\n\n"
                "是否需要生成详细报告？"
            )
        elif "最佳实践" in query:
            return (
                f"收到最佳实践查询：「{query}」。\n\n"
                "以下是 FDE 最佳实践推荐：\n"
                "1. **代码审查** - 每次 PR 至少需要 2 个 reviewer\n"
                "2. **文档同步** - 每次需求变更后及时更新设计文档\n"
                "3. **风险预警** - 每周一更新风险清单\n"
                "4. **客户沟通** - 每周至少 1 次客户进度同步"
            )
        else:
            return (
                f"我收到了您的问题：「{query}」。\n\n"
                "这是一个模拟回复。AI Orchestrator 已成功启动并可以处理请求。"
                "配置真实 LLM API Key 后，我将提供智能回复。"
            )


def get_llm() -> LlmProvider:
    """Get LLM provider based on configuration."""
    provider = settings.llm_provider
    if provider == "dashscope":
        if not settings.dashscope_api_key:
            return MockLlm()
        return DashScopeLlm()
    elif provider == "openai":
        if not settings.openai_api_key:
            return MockLlm()
        return OpenAiLlm()
    return MockLlm()
