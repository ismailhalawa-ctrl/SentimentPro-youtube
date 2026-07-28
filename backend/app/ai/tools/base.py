from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from app.ai.tools.context import ToolContext

ToolHandler = Callable[[dict[str, Any], ToolContext], Awaitable[dict[str, Any]]]


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: ToolHandler
    cost_tier: str = "free"
