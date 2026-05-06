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


def get_system_prompt(agent_name: str, mode: str = "smart") -> str:
    """Get the system prompt for a specific agent."""
    if agent_name not in KNOWN_AGENTS:
        agent_name = "chat"
    template = _load_template(agent_name)
    return prompt_env.from_string(template).render(mode=mode)


def render_prompt(template_name: str, **kwargs: str) -> str:
    """Render a named prompt template with the given variables."""
    template = _load_template(template_name)
    return prompt_env.from_string(template).render(**kwargs)


def reload_templates() -> None:
    """Clear template cache (useful for development)."""
    _loaded_templates.clear()
