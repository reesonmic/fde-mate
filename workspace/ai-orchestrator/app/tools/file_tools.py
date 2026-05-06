"""
F助手工具集 - File management tools.
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


class SearchFilesTool(BaseTool):
    """搜索文件."""

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="search_files",
            description="搜索文件，支持按名称、类型、标签筛选",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"},
                    "file_type": {"type": "string", "description": "文件类型 (pdf/doc/xlsx/等)"},
                    "limit": {"type": "integer", "default": 10},
                },
                "required": ["query"],
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            query = arguments.pop("query")
            params = {"q": query, **{k: v for k, v in arguments.items() if v is not None}}
            result = await _api_get("/files", params=params)
            items = result.get("items", [])
            return ToolResult(
                tool_name="search_files",
                success=True,
                content=f"找到 {result.get('total', 0)} 个文件，返回 {len(items)} 个",
                data=items,
            )
        except Exception as e:
            return ToolResult(tool_name="search_files", success=False, content=f"搜索失败: {e}")


class GetFileTreeTool(BaseTool):
    """获取文件目录树."""

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="get_file_tree",
            description="获取文件目录树结构",
            parameters={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer", "description": "项目ID（可选）"},
                },
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            params = {k: v for k, v in arguments.items() if v is not None}
            result = await _api_get("/files/tree", params=params)
            return ToolResult(
                tool_name="get_file_tree",
                success=True,
                content=f"文件目录树，共 {len(result)} 个根节点",
                data=result,
            )
        except Exception as e:
            return ToolResult(tool_name="get_file_tree", success=False, content=f"获取目录树失败: {e}")


class GetFileDetailTool(BaseTool):
    """获取文件详情."""

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="get_file_detail",
            description="获取指定文件的详细信息",
            parameters={
                "type": "object",
                "properties": {
                    "file_id": {"type": "integer", "description": "文件ID"},
                },
                "required": ["file_id"],
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            file_id = arguments["file_id"]
            result = await _api_get(f"/files/{file_id}")
            return ToolResult(
                tool_name="get_file_detail",
                success=True,
                content=f"文件: {result.get('name', '')} ({result.get('size', 0)} bytes)",
                data=result,
            )
        except Exception as e:
            return ToolResult(tool_name="get_file_detail", success=False, content=f"查询失败: {e}")


class GetFileQuotaTool(BaseTool):
    """获取文件存储配额."""

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="get_file_quota",
            description="获取当前用户的文件存储配额使用情况",
            parameters={
                "type": "object",
                "properties": {},
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            result = await _api_get("/files/quota")
            used = result.get("used", 0)
            total = result.get("total", 0)
            return ToolResult(
                tool_name="get_file_quota",
                success=True,
                content=f"存储空间: {used}/{total} bytes",
                data=result,
            )
        except Exception as e:
            return ToolResult(tool_name="get_file_quota", success=False, content=f"查询配额失败: {e}")
