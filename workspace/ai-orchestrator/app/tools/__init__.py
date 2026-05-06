"""
Tool registry for AI agent function calling.

Provides assistant-specific tool registries for T/P/C/F assistants.
"""
from app.tools.base import ToolRegistry


def get_task_tools() -> ToolRegistry:
    """T助手工具集."""
    from app.tools.task_tools import (
        ListTasksTool, CreateTaskTool, UpdateTaskTool,
        BatchUpdateTasksTool, GetTaskDetailTool,
    )
    registry = ToolRegistry()
    for tool_cls in [ListTasksTool, CreateTaskTool, UpdateTaskTool, BatchUpdateTasksTool, GetTaskDetailTool]:
        registry.register(tool_cls())
    return registry


def get_project_tools() -> ToolRegistry:
    """P助手工具集."""
    from app.tools.project_tools import (
        ListProjectsTool, GetProjectSummaryTool,
        GetWeeklyReportTool, ListProjectRisksTool, DashboardSummaryTool,
    )
    registry = ToolRegistry()
    for tool_cls in [ListProjectsTool, GetProjectSummaryTool, GetWeeklyReportTool,
                     ListProjectRisksTool, DashboardSummaryTool]:
        registry.register(tool_cls())
    return registry


def get_coach_tools() -> ToolRegistry:
    """C助手工具集."""
    from app.tools.coach_tools import (
        ListBestPracticesTool, GetPracticeDetailTool,
        ListSopsTool, GetLearningPathsTool, GetRecommendationsTool,
    )
    registry = ToolRegistry()
    for tool_cls in [ListBestPracticesTool, GetPracticeDetailTool,
                     ListSopsTool, GetLearningPathsTool, GetRecommendationsTool]:
        registry.register(tool_cls())
    return registry


def get_file_tools() -> ToolRegistry:
    """F助手工具集."""
    from app.tools.file_tools import (
        SearchFilesTool, GetFileTreeTool, GetFileDetailTool, GetFileQuotaTool,
    )
    registry = ToolRegistry()
    for tool_cls in [SearchFilesTool, GetFileTreeTool, GetFileDetailTool, GetFileQuotaTool]:
        registry.register(tool_cls())
    return registry


# Agent name -> tool registry mapping
AGENT_TOOLS_MAP = {
    "task": get_task_tools,
    "project": get_project_tools,
    "coach": get_coach_tools,
    "file": get_file_tools,
}


def get_tools_for_agent(agent_name: str) -> ToolRegistry | None:
    """Get tool registry for a specific agent."""
    factory = AGENT_TOOLS_MAP.get(agent_name)
    if factory:
        return factory()
    return None


def get_all_tool_definitions(agent_name: str | None = None) -> list[dict]:
    """Get all OpenAI-compatible tool definitions for LLM function calling."""
    if agent_name:
        registry = get_tools_for_agent(agent_name)
        if registry:
            return registry.get_definitions()
    # Return all tools
    all_defs = []
    for factory in AGENT_TOOLS_MAP.values():
        all_defs.extend(factory().get_definitions())
    return all_defs
