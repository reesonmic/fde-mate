"""
Base tool definitions for AI agent function calling.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolDefinition:
    """OpenAI-compatible tool definition for function calling."""
    name: str
    description: str
    parameters: dict  # JSON Schema for parameters


@dataclass
class ToolCall:
    """A request to call a tool."""
    name: str
    arguments: dict


@dataclass
class ToolResult:
    """Result from a tool call."""
    tool_name: str
    success: bool
    content: str
    data: Any = None


class BaseTool(ABC):
    """Base class for all callable tools."""

    @property
    def definition(self) -> ToolDefinition:
        pass

    @abstractmethod
    async def call(self, arguments: dict) -> ToolResult:
        ...

    @property
    def is_write_tool(self) -> bool:
        """Whether this tool modifies data (requires actionCard confirmation)."""
        return False


class ToolRegistry:
    """Registry for tool definitions and execution."""

    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        self._tools[tool.definition.name] = tool

    def get(self, name: str) -> BaseTool | None:
        return self._tools.get(name)

    def get_definitions(self) -> list[dict]:
        """Get OpenAI-compatible tool definitions for LLM function calling."""
        defs = []
        for tool in self._tools.values():
            defs.append({
                "type": "function",
                "function": {
                    "name": tool.definition.name,
                    "description": tool.definition.description,
                    "parameters": tool.definition.parameters,
                }
            })
        return defs

    async def execute(self, name: str, arguments: dict) -> ToolResult:
        tool = self._tools.get(name)
        if not tool:
            return ToolResult(
                tool_name=name,
                success=False,
                content=f"Unknown tool: {name}",
            )
        return await tool.call(arguments)

    def is_write_tool(self, name: str) -> bool:
        tool = self._tools.get(name)
        return tool.is_write_tool if tool else False
