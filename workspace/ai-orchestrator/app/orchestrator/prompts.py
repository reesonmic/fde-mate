"""
Prompt template management using Jinja2.

Prompts are stored as versioned markdown files under prompts/v{N}/*.md.
The active version is controlled by PROMPT_VERSION constant.
"""
from pathlib import Path
from jinja2 import BaseLoader, Environment, FileSystemLoader

PROMPT_VERSION = "v1"

_prompt_dir = Path(__file__).parent / "prompts" / PROMPT_VERSION

# Jinja2 environment - use FileSystemLoader for versioned directory
prompt_env = Environment(
    loader=FileSystemLoader(_prompt_dir),
    trim_blocks=True,
    lstrip_blocks=True,
)

# Pre-load all known agent prompts
KNOWN_AGENTS = ["task", "project", "coach", "file", "chat"]

# Cache loaded templates
_loaded_templates: dict[str, str] = {}


def _load_template(name: str) -> str:
    """Load a prompt template from the versioned directory."""
    if name not in _loaded_templates:
        path = _prompt_dir / f"{name}.md"
        if not path.exists():
            raise FileNotFoundError(f"Prompt template not found: {name} (looked in {path})")
        _loaded_templates[name] = path.read_text(encoding="utf-8")
    return _loaded_templates[name]


def get_system_prompt(agent_name: str, mode: str = "smart", context: dict | None = None) -> str:
    """Get the system prompt for a specific agent.
    
    Args:
        agent_name: Agent name (task/project/coach/file/chat)
        mode: Response mode (smart/creative/rigorous)
        context: Page context data from frontend (optional)
    """
    if agent_name not in KNOWN_AGENTS:
        agent_name = "chat"
    template = _load_template(agent_name)
    
    # 构建渲染变量
    render_vars = {"mode": mode}
    
    # 如果有上下文数据，添加到提示词中
    if context:
        import json
        # 将上下文格式化为可读的文本
        context_text = _format_context(context)
        if context_text:
            render_vars["context_text"] = context_text
    
    return prompt_env.from_string(template).render(**render_vars)


def _format_context(context: dict, max_length: int = 3000) -> str:
    """将上下文数据格式化为可读的文本。
    
    Args:
        context: 页面上下文数据
        max_length: 最大长度（避免 token 超限）
    
    Returns:
        格式化后的上下文文本
    """
    if not context:
        return ""
    
    parts = []
    
    # 页面类型
    if page := context.get("currentPage"):
        page_names = {
            "projects-list": "项目列表页",
            "tasks-list": "任务中心页",
            "customers": "客户空间页",
            "files": "文件中心页",
            "project-detail": "项目详情页",
        }
        parts.append(f"**当前页面**: {page_names.get(page, page)}")
    
    # 项目列表
    if "projects" in context:
        projects = context["projects"]
        total = context.get("totalProjects", len(projects))
        parts.append(f"\n**项目总数**: {total}")
        
        if isinstance(projects, list) and projects:
            parts.append("\n**项目列表**:")
            for i, p in enumerate(projects[:10], 1):  # 最多显示10个
                name = p.get("name", "未命名")
                phase = p.get("phase", "未知")
                health = p.get("health", "--")
                owner = p.get("owner", "未指定")
                parts.append(f"{i}. {name} (阶段: {phase}, 健康度: {health}, 负责人: {owner})")
            if len(projects) > 10:
                parts.append(f"... 还有 {len(projects) - 10} 个项目")
    
    # 任务列表
    if "tasks" in context:
        tasks = context["tasks"]
        total = context.get("totalTasks", len(tasks))
        parts.append(f"\n**任务总数**: {total}")
        
        # 统计信息
        if status_stats := context.get("statusStats"):
            parts.append("\n**任务状态分布**:")
            status_names = {
                "todo": "待办",
                "in_progress": "进行中",
                "review": "审核中",
                "blocked": "已阻塞",
                "done": "已完成",
            }
            for status, count in status_stats.items():
                if count > 0:
                    parts.append(f"- {status_names.get(status, status)}: {count} 个")
        
        if priority_stats := context.get("priorityStats"):
            parts.append("\n**任务优先级分布**:")
            for priority, count in priority_stats.items():
                if count > 0:
                    parts.append(f"- {priority.upper()}: {count} 个")
        
        if isinstance(tasks, list) and tasks:
            parts.append("\n**任务列表**:")
            for i, t in enumerate(tasks[:15], 1):  # 最多显示15个
                title = t.get("title", "未命名")
                status = t.get("status", "未知")
                priority = t.get("priority", "--")
                assignee = t.get("assignee", "未指定")
                due = t.get("dueDate", "无截止日期")
                parts.append(f"{i}. {title} [{priority.upper()}] (状态: {status}, 负责人: {assignee}, 截止: {due})")
            if len(tasks) > 15:
                parts.append(f"... 还有 {len(tasks) - 15} 个任务")
    
    # 筛选条件
    if filters := context.get("filters"):
        parts.append("\n**当前筛选条件**:")
        if filters.get("status"):
            parts.append(f"- 状态: {', '.join(filters['status'])}")
        if filters.get("priority"):
            parts.append(f"- 优先级: {', '.join(filters['priority'])}")
        if filters.get("keyword"):
            parts.append(f"- 关键词: {filters['keyword']}")
    
    # 合并并限制长度
    result = "\n".join(parts)
    if len(result) > max_length:
        result = result[:max_length] + "\n...（上下文已截断）"
    
    return result


def render_prompt(template_name: str, **kwargs: str) -> str:
    """Render a named prompt template with the given variables."""
    template = _load_template(template_name)
    return prompt_env.from_string(template).render(**kwargs)


def reload_templates() -> None:
    """Clear template cache (useful for development)."""
    _loaded_templates.clear()
