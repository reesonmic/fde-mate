"""
P助手工具集 - Project management tools.
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


async def _api_post(path: str, data: dict | None = None) -> dict:
    url = f"{settings.api_base_url}{path}"
    session = await _get_session()
    async with session.post(url, json=data) as resp:
        return await resp.json()


class ListProjectsTool(BaseTool):
    """查询项目列表."""

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="list_projects",
            description="查询用户参与的项目列表",
            parameters={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["active", "archived"], "description": "项目状态"},
                    "limit": {"type": "integer", "default": 20},
                    "page": {"type": "integer", "default": 1},
                },
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            params = {k: v for k, v in arguments.items() if v is not None}
            result = await _api_get("/projects", params=params)
            items = result.get("items", [])
            return ToolResult(
                tool_name="list_projects",
                success=True,
                content=f"共 {result.get('total', 0)} 个项目",
                data=items,
            )
        except Exception as e:
            return ToolResult(tool_name="list_projects", success=False, content=f"查询失败: {e}")


class GetProjectSummaryTool(BaseTool):
    """获取项目摘要/健康度."""

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="get_project_summary",
            description="获取指定项目的详细信息，包括健康度、风险、进度等",
            parameters={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer", "description": "项目ID"},
                },
                "required": ["project_id"],
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            project_id = arguments["project_id"]
            info = await _api_get(f"/projects/{project_id}")
            health = await _api_get(f"/projects/{project_id}/health")
            members = await _api_get(f"/projects/{project_id}/members")
            return ToolResult(
                tool_name="get_project_summary",
                success=True,
                content=f"项目 {info.get('name', '')}: 健康度 {health.get('score', 'N/A')}",
                data={"info": info, "health": health, "members": members},
            )
        except Exception as e:
            return ToolResult(tool_name="get_project_summary", success=False, content=f"查询失败: {e}")


class GetWeeklyReportTool(BaseTool):
    """获取项目周报."""

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="get_weekly_report",
            description="获取指定项目的周报/月报数据",
            parameters={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer", "description": "项目ID"},
                    "week": {"type": "string", "description": "周数 (如 2026-W17)"},
                },
                "required": ["project_id"],
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            project_id = arguments["project_id"]
            result = await _api_get(f"/projects/{project_id}/weekly-reports")
            return ToolResult(
                tool_name="get_weekly_report",
                success=True,
                content=f"已获取项目 {project_id} 的周报",
                data=result,
            )
        except Exception as e:
            return ToolResult(tool_name="get_weekly_report", success=False, content=f"获取周报失败: {e}")


class ListProjectRisksTool(BaseTool):
    """查询项目风险."""

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="list_project_risks",
            description="查询项目的风险清单",
            parameters={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer", "description": "项目ID"},
                },
                "required": ["project_id"],
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            project_id = arguments["project_id"]
            info = await _api_get(f"/projects/{project_id}")
            risks = info.get("risks", [])
            return ToolResult(
                tool_name="list_project_risks",
                success=True,
                content=f"项目 {info.get('name', '')} 有 {len(risks)} 个风险项",
                data=risks,
            )
        except Exception as e:
            return ToolResult(tool_name="list_project_risks", success=False, content=f"查询风险失败: {e}")


class DashboardSummaryTool(BaseTool):
    """获取工作台摘要."""

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="dashboard_summary",
            description="获取工作台的摘要信息，包括任务数、项目数、客户数等",
            parameters={
                "type": "object",
                "properties": {},
            },
        )

    async def call(self, arguments: dict) -> ToolResult:
        try:
            result = await _api_get("/dashboard/summary")
            return ToolResult(
                tool_name="dashboard_summary",
                success=True,
                content=f"任务 {result.get('task_count', 0)} | 项目 {result.get('project_count', 0)} | 客户 {result.get('customer_count', 0)}",
                data=result,
            )
        except Exception as e:
            return ToolResult(tool_name="dashboard_summary", success=False, content=f"查询摘要失败: {e}")
