"""
T助手工具集 - Task management tools.
"""
import aiohttp
from app.tools.base import BaseTool, ToolDefinition, ToolCall, ToolResult
from app.config import settings

# Shared session pool - initialized on first use
_session: aiohttp.ClientSession | None = None


async def _get_session() -> aiohttp.ClientSession:
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession()
    return _session


async def _api_get(path: str, params: dict | None = None) -> dict:
    """Call business API via HTTP."""
    url = f"{settings.api_base_url}{path}"
    session = await _get_session()
    async with session.get(url, params=params) as resp:
        return await resp.json()


async def _api_post(path: str, data: dict | None = None) -> dict:
    """Call business API via HTTP."""
    url = f"{settings.api_base_url}{path}"
    session = await _get_session()
    async with session.post(url, json=data) as resp:
        return await resp.json()


async def _api_put(path: str, data: dict | None = None) -> dict:
    """Call business API via HTTP PUT."""
    url = f"{settings.api_base_url}{path}"
    session = await _get_session()
    async with session.put(url, json=data) as resp:
        return await resp.json()


class ListTasksTool(BaseTool):
    """查询任务列表."""

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="list_tasks",
            description="查询用户的任务列表，支持按状态、优先级、项目筛选",
            parameters={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["todo", "doing", "done", "cancelled"], "description": "任务状态"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"], "description": "优先级"},
                    "project_id": {"type": "integer", "description": "项目ID"},
                    "limit": {"type": "integer", "default": 20, "description": "返回数量"},
                },
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            params = {k: v for k, v in arguments.items() if v is not None}
            result = await _api_get("/tasks", params=params)
            items = result.get("items", [])
            return ToolResult(
                tool_name="list_tasks",
                success=True,
                content=f"共 {result.get('total', 0)} 条任务，返回 {len(items)} 条",
                data=items,
            )
        except Exception as e:
            return ToolResult(tool_name="list_tasks", success=False, content=f"查询失败: {e}")


class UpdateTaskTool(BaseTool):
    """更新任务状态/属性."""

    @property
    def is_write_tool(self) -> bool:
        return True

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="update_task",
            description="更新任务的状态、优先级、截止时间、描述等信息",
            parameters={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "任务ID"},
                    "status": {"type": "string", "enum": ["todo", "doing", "done", "cancelled"], "description": "新状态"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"], "description": "新优先级"},
                    "title": {"type": "string", "description": "新标题"},
                    "description": {"type": "string", "description": "新描述"},
                    "deadline": {"type": "string", "description": "新截止时间 (ISO 8601)"},
                },
                "required": ["task_id"],
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            task_id = arguments.pop("task_id")
            result = await _api_put(f"/tasks/{task_id}", data=arguments)
            return ToolResult(
                tool_name="update_task",
                success=True,
                content=f"任务 {task_id} 已更新",
                data=result,
            )
        except Exception as e:
            return ToolResult(tool_name="update_task", success=False, content=f"更新失败: {e}")


class CreateTaskTool(BaseTool):
    """创建新任务."""

    @property
    def is_write_tool(self) -> bool:
        return True

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="create_task",
            description="创建一个新的任务",
            parameters={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "任务标题"},
                    "description": {"type": "string", "description": "任务描述"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"], "default": "medium"},
                    "project_id": {"type": "integer", "description": "所属项目ID"},
                    "deadline": {"type": "string", "description": "截止时间 (ISO 8601)"},
                    "assignee_id": {"type": "integer", "description": "指派人ID"},
                },
                "required": ["title"],
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            result = await _api_post("/tasks", data=arguments)
            return ToolResult(
                tool_name="create_task",
                success=True,
                content=f"任务已创建: {result.get('title', '')}",
                data=result,
            )
        except Exception as e:
            return ToolResult(tool_name="create_task", success=False, content=f"创建失败: {e}")


class BatchUpdateTasksTool(BaseTool):
    """批量更新任务状态."""

    @property
    def is_write_tool(self) -> bool:
        return True

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="batch_update_tasks",
            description="批量更新多个任务的状态（如批量完成、批量开始）",
            parameters={
                "type": "object",
                "properties": {
                    "task_ids": {"type": "array", "items": {"type": "integer"}, "description": "任务ID列表"},
                    "status": {"type": "string", "enum": ["todo", "doing", "done", "cancelled"], "description": "新状态"},
                },
                "required": ["task_ids", "status"],
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            result = await _api_post("/tasks/batch-update-status", data=arguments)
            count = len(arguments.get("task_ids", []))
            return ToolResult(
                tool_name="batch_update_tasks",
                success=True,
                content=f"已批量更新 {count} 个任务状态为 {arguments['status']}",
                data=result,
            )
        except Exception as e:
            return ToolResult(tool_name="batch_update_tasks", success=False, content=f"批量更新失败: {e}")


class GetTaskDetailTool(BaseTool):
    """获取任务详情."""

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="get_task_detail",
            description="获取指定任务的详细信息",
            parameters={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "任务ID"},
                },
                "required": ["task_id"],
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            task_id = arguments["task_id"]
            result = await _api_get(f"/tasks/{task_id}")
            return ToolResult(
                tool_name="get_task_detail",
                success=True,
                content=f"任务详情: {result.get('title', '')} - {result.get('status', '')}",
                data=result,
            )
        except Exception as e:
            return ToolResult(tool_name="get_task_detail", success=False, content=f"查询失败: {e}")
