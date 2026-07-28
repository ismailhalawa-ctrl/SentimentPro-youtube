import asyncio
import json
import logging

import jsonschema

from app.ai.tools.base import Tool
from app.ai.tools.context import ToolContext

logger = logging.getLogger(__name__)

TOOL_REGISTRY: dict[str, Tool] = {}

_TOOL_TIMEOUT_SECONDS = 8.0

_GEMINI_TYPE_MAP = {
    "object": "OBJECT",
    "string": "STRING",
    "integer": "INTEGER",
    "number": "NUMBER",
    "boolean": "BOOLEAN",
    "array": "ARRAY",
}


def register_tool(tool: Tool) -> Tool:
    TOOL_REGISTRY[tool.name] = tool
    return tool


def _to_gemini_schema(schema: dict) -> dict:
    converted: dict = {}

    schema_type = schema.get("type")
    if schema_type in _GEMINI_TYPE_MAP:
        converted["type"] = _GEMINI_TYPE_MAP[schema_type]

    if description := schema.get("description"):
        converted["description"] = description

    if enum := schema.get("enum"):
        converted["enum"] = enum

    if properties := schema.get("properties"):
        converted["properties"] = {key: _to_gemini_schema(value) for key, value in properties.items()}

    if required := schema.get("required"):
        converted["required"] = required

    if items := schema.get("items"):
        converted["items"] = _to_gemini_schema(items)

    return converted


def get_tool_schemas(provider: str, exclude: set[str] | None = None) -> list[dict]:
    exclude = exclude or set()
    tools = [tool for tool in TOOL_REGISTRY.values() if tool.name not in exclude]

    if provider == "gemini":
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": _to_gemini_schema(tool.input_schema),
            }
            for tool in tools
        ]

    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema,
            },
        }
        for tool in tools
    ]


def _validate_arguments(tool: Tool, arguments: dict) -> str | None:
    try:
        jsonschema.validate(instance=arguments, schema=tool.input_schema)
    except jsonschema.exceptions.ValidationError as exc:
        path = "/".join(str(p) for p in exc.path) or "arguments"
        return f"{path}: {exc.message}"
    return None


async def dispatch_tool_call(name: str, raw_arguments: str, ctx: ToolContext) -> dict:
    tool = TOOL_REGISTRY.get(name)
    if tool is None:
        return {"error": f"Unknown tool '{name}'."}

    try:
        arguments = json.loads(raw_arguments) if raw_arguments else {}
    except json.JSONDecodeError:
        return {"error": f"Tool '{name}' received arguments that were not valid JSON."}

    if not isinstance(arguments, dict):
        return {"error": f"Tool '{name}' expects a JSON object of arguments."}

    if ctx.target_job_id is not None and "job_id" in tool.input_schema.get("properties", {}):
        arguments.setdefault("job_id", ctx.target_job_id)

    validation_error = _validate_arguments(tool, arguments)
    if validation_error:
        return {"error": f"Tool '{name}' received invalid arguments ({validation_error})."}

    try:
        return await asyncio.wait_for(tool.handler(arguments, ctx), timeout=_TOOL_TIMEOUT_SECONDS)
    except TimeoutError:
        logger.warning("Tool '%s' timed out after %.1fs", name, _TOOL_TIMEOUT_SECONDS)
        return {"error": f"Tool '{name}' took too long to respond."}
    except Exception:
        logger.exception("Tool '%s' raised an unexpected error", name)
        return {"error": f"Tool '{name}' failed unexpectedly."}
