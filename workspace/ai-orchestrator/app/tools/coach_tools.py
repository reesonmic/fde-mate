"""
C助手工具集 - Coach (FDE best practices, SOPs, learning paths) tools.
"""
import aiohttp
from app.tools.base import BaseTool, ToolDefinition, ToolResult
from app.config import settings

# Shared session pool
_session: aiohttp.ClientSession | None = None


async def _get_session() -> aiohttp.ClientSession:
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession()
    return _session


async def _api_get(path: str, params: dict | None = None) -> dict:
    url = f"{settings.api_base_url}{path}"
    session = await _get_session()
    async with session.get(url, params=params) as resp:
        return await resp.json()


class ListBestPracticesTool(BaseTool):
    """查询最佳实践."""

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="list_best_practices",
            description="查询 FDE 最佳实践列表，支持按标签、分类筛选",
            parameters={
                "type": "object",
                "properties": {
                    "tag": {"type": "string", "description": "标签筛选"},
                    "category": {"type": "string", "description": "分类筛选"},
                    "limit": {"type": "integer", "default": 10},
                },
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            params = {k: v for k, v in arguments.items() if v is not None}
            result = await _api_get("/coach/best-practices", params=params)
            items = result if isinstance(result, list) else result.get("items", [])
            return ToolResult(
                tool_name="list_best_practices",
                success=True,
                content=f"共 {len(items)} 条最佳实践",
                data=items,
            )
        except Exception as e:
            return ToolResult(tool_name="list_best_practices", success=False, content=f"查询失败: {e}")


class GetPracticeDetailTool(BaseTool):
    """获取最佳实践详情."""

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="get_practice_detail",
            description="获取指定最佳实践的详细内容",
            parameters={
                "type": "object",
                "properties": {
                    "practice_id": {"type": "integer", "description": "最佳实践ID"},
                },
                "required": ["practice_id"],
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            practice_id = arguments["practice_id"]
            result = await _api_get(f"/coach/best-practices/{practice_id}")
            return ToolResult(
                tool_name="get_practice_detail",
                success=True,
                content=result.get("title", ""),
                data=result,
            )
        except Exception as e:
            return ToolResult(tool_name="get_practice_detail", success=False, content=f"查询失败: {e}")


class ListSopsTool(BaseTool):
    """查询 SOP 列表."""

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="list_sops",
            description="查询标准操作流程 (SOP) 列表",
            parameters={
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "SOP 分类"},
                    "limit": {"type": "integer", "default": 10},
                },
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            params = {k: v for k, v in arguments.items() if v is not None}
            result = await _api_get("/coach/sops", params=params)
            items = result if isinstance(result, list) else result.get("items", [])
            return ToolResult(
                tool_name="list_sops",
                success=True,
                content=f"共 {len(items)} 个 SOP",
                data=items,
            )
        except Exception as e:
            return ToolResult(tool_name="list_sops", success=False, content=f"查询失败: {e}")


class GetLearningPathsTool(BaseTool):
    """查询学习路径."""

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="get_learning_paths",
            description="查询 FDE 学习路径列表",
            parameters={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "default": 10},
                },
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            params = {k: v for k, v in arguments.items() if v is not None}
            result = await _api_get("/coach/learning-paths", params=params)
            items = result if isinstance(result, list) else result.get("items", [])
            return ToolResult(
                tool_name="get_learning_paths",
                success=True,
                content=f"共 {len(items)} 条学习路径",
                data=items,
            )
        except Exception as e:
            return ToolResult(tool_name="get_learning_paths", success=False, content=f"查询失败: {e}")


class GetRecommendationsTool(BaseTool):
    """获取个性化推荐."""

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="get_recommendations",
            description="获取基于用户画像的个性化学习推荐",
            parameters={
                "type": "object",
                "properties": {},
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            result = await _api_get("/coach/recommendations")
            return ToolResult(
                tool_name="get_recommendations",
                success=True,
                content="已获取个性化推荐",
                data=result,
            )
        except Exception as e:
            return ToolResult(tool_name="get_recommendations", success=False, content=f"获取推荐失败: {e}")
