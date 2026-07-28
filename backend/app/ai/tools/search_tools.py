from app.ai.rag.retriever import RetrievalError, retrieve_relevant_comments
from app.ai.tools._shared import resolve_owned_job
from app.ai.tools.base import Tool
from app.ai.tools.context import ToolContext
from app.ai.tools.registry import register_tool

_MAX_RESULTS = 15
_MAX_TEXT_CHARS = 400


def _truncate(text: str) -> str:
    if len(text) <= _MAX_TEXT_CHARS:
        return text
    return text[:_MAX_TEXT_CHARS].rstrip() + "…"


async def _search_comments(args: dict, ctx: ToolContext) -> dict:
    job = resolve_owned_job(args, ctx)
    if isinstance(job, dict):
        return job

    query = args.get("query")
    if not query or not str(query).strip():
        return {"error": "query is required."}

    try:
        top_k = max(1, min(int(args.get("top_k", 10)), _MAX_RESULTS))
    except (TypeError, ValueError):
        top_k = 10

    try:
        matches = await retrieve_relevant_comments(ctx.db, job.id, str(query), top_k=top_k)
    except RetrievalError as exc:
        return {"error": str(exc)}

    return {
        "job_id": job.id,
        "matches": [
            {
                "comment_id": match["comment_id"],
                "text": _truncate(match["text"]),
                "author": match["author"],
                "like_count": match["like_count"],
                "score": round(match["score"], 4),
            }
            for match in matches
        ],
    }


register_tool(
    Tool(
        name="search_comments",
        description=(
            "Semantically search one analyzed video's comments for a topic or "
            "question. Returns the most relevant comments with author, like count, "
            "and relevance score. Requires the video to already be indexed."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "job_id": {"type": "integer", "description": "The analysis job id."},
                "query": {"type": "string", "description": "What to search for."},
                "top_k": {
                    "type": "integer",
                    "description": f"Number of results to return (1-{_MAX_RESULTS}).",
                    "default": 10,
                },
            },
            "required": ["job_id", "query"],
        },
        handler=_search_comments,
        cost_tier="embedding",
    )
)
