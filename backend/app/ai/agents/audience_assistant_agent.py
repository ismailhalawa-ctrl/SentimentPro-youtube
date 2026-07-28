import json
import logging
import re
from dataclasses import dataclass, field

from app.ai.interfaces.capability import AnalysisMode, Capability
from app.ai.prompts.audience_assistant import SYSTEM_PROMPT, build_focus_instruction
from app.ai.providers.provider_registry import resolve_provider
from app.ai.tools import ToolContext, dispatch_tool_call
from app.core.config import settings
from app.services import analysis_service

logger = logging.getLogger(__name__)

_FOCUS_EXCLUDED_TOOLS = {"list_my_jobs"}

_JOB_ID_LEAK_PATTERN = re.compile(r"\bjob[_ ]?id\s*[:=]?\s*#?\d+\b", re.IGNORECASE)
_USERNAME_PATTERN = re.compile(r"@[A-Za-z0-9_.\-]+")

_MAX_TOOL_CALLS_PER_ROUND = 3
_MAX_TOTAL_TOOL_CALLS_PER_TURN = 12


@dataclass
class AgentTurnResult:
    answer: str
    citations: list[dict] = field(default_factory=list)
    tool_trace: list[dict] = field(default_factory=list)
    tokens_in: int = 0
    tokens_out: int = 0


def _summarize_tool_result(result: dict) -> str:
    if "error" in result:
        return result["error"]
    if "jobs" in result:
        return f"{len(result['jobs'])} job(s) found"
    if "matches" in result:
        return f"{len(result['matches'])} matching comment(s)"
    if "insights" in result:
        return f"{len(result['insights'])} highlight(s)"
    return "ok"


def _record_citable_comments(result: dict, seen_comments: dict[tuple, dict]) -> None:
    job_id = result.get("job_id")
    if job_id is None:
        return
    for match in result.get("matches", []):
        comment_id = match.get("comment_id")
        if comment_id is None:
            continue
        seen_comments[(job_id, comment_id)] = {
            "text": match.get("text", ""),
            "author": match.get("author", ""),
            "like_count": match.get("like_count", 0),
        }


def _strip_job_id_leaks(text: str) -> str:
    return _JOB_ID_LEAK_PATTERN.sub("this video", text)


def _strip_accounted_for_usernames(text: str, citations: list[dict]) -> str:
    cited_authors = {c["author"] for c in citations if c.get("author")}
    if not cited_authors:
        return text

    cleaned = _USERNAME_PATTERN.sub(lambda m: "" if m.group(0) in cited_authors else m.group(0), text)
    if cleaned == text:
        return text

    cleaned = re.sub(r",\s*,", ",", cleaned)
    cleaned = re.sub(r",\s*(and|or)\b", r" \1", cleaned)
    cleaned = re.sub(r"\b(and|or)\s+(and|or)\b", r"\1", cleaned)
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
    cleaned = re.sub(r"\s+([.,;:!?])", r"\1", cleaned)
    cleaned = re.sub(r"(?m)^[ \t]*[-•]\s*$\n?", "", cleaned)
    cleaned = re.sub(r"\(\s*\)", "", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def _sanitize_answer_text(text: str, citations: list[dict]) -> str:
    text = _strip_job_id_leaks(text)
    text = _strip_accounted_for_usernames(text, citations)
    return text


def _finalize(
    content: str | None,
    seen_comments: dict[tuple, dict],
    tool_trace: list[dict],
    tokens_in: int = 0,
    tokens_out: int = 0,
) -> AgentTurnResult:
    if not content or not content.strip():
        return AgentTurnResult(
            answer="I wasn't able to generate a response for that — please try rephrasing your question.",
            tool_trace=tool_trace,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
        )

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return AgentTurnResult(
            answer=_sanitize_answer_text(content.strip(), []),
            tool_trace=tool_trace,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
        )

    answer = parsed.get("answer") if isinstance(parsed, dict) else None
    if not answer:
        answer = content.strip()

    raw_citations = parsed.get("citations", []) if isinstance(parsed, dict) else []
    citations = []
    for raw in raw_citations:
        if not isinstance(raw, dict):
            continue
        key = (raw.get("job_id"), raw.get("comment_id"))
        hydrated = seen_comments.get(key)
        if hydrated is not None:
            citations.append(
                {
                    "job_id": key[0],
                    "comment_id": key[1],
                    "text": hydrated["text"],
                    "author": hydrated["author"],
                    "like_count": hydrated["like_count"],
                }
            )

    answer = _sanitize_answer_text(answer, citations)

    return AgentTurnResult(
        answer=answer, citations=citations, tool_trace=tool_trace, tokens_in=tokens_in, tokens_out=tokens_out
    )


def _tool_cache_key(name: str, raw_arguments: str) -> tuple:
    parsed = _safe_parse_arguments(raw_arguments)
    try:
        canonical = json.dumps(parsed, sort_keys=True)
    except TypeError:
        canonical = raw_arguments
    return (name, canonical)


def _accumulate_usage(turn: dict, tokens_in: int, tokens_out: int) -> tuple[int, int]:
    usage = turn.get("token_usage") or {}
    return tokens_in + (usage.get("prompt_tokens") or 0), tokens_out + (usage.get("completion_tokens") or 0)


async def run_agent_turn(question: str, history: list[dict], ctx: ToolContext) -> AgentTurnResult:
    provider = resolve_provider(Capability.AUDIENCE_ASSISTANT, AnalysisMode.SMART, "auto")

    system_prompt = SYSTEM_PROMPT
    excluded_tools: set[str] = set()

    if ctx.target_job_id is not None:
        job = analysis_service.get_job(ctx.db, job_id=ctx.target_job_id, owner_id=ctx.user_id)
        if job is None:
            raise LookupError("That video was not found or is not accessible.")
        system_prompt = f"{SYSTEM_PROMPT}\n\n{build_focus_instruction(job.video_title)}"
        excluded_tools = _FOCUS_EXCLUDED_TOOLS

    trimmed_history = history[-settings.audience_assistant_history_limit :]
    state = provider.build_conversation_state(system_prompt, trimmed_history, question)

    tool_trace: list[dict] = []
    seen_comments: dict[tuple, dict] = {}
    result_cache: dict[tuple, dict] = {}
    tokens_in = 0
    tokens_out = 0
    total_tool_calls = 0

    max_rounds = settings.audience_assistant_max_tool_calls

    for _round_index in range(max_rounds):
        turn = await provider.generate_step(state, force_final=False, excluded_tools=excluded_tools)
        tokens_in, tokens_out = _accumulate_usage(turn, tokens_in, tokens_out)

        if not turn["tool_calls"]:
            return _finalize(turn["content"], seen_comments, tool_trace, tokens_in, tokens_out)

        requested_calls = turn["tool_calls"]
        if len(requested_calls) > _MAX_TOOL_CALLS_PER_ROUND:
            logger.warning(
                "Audience assistant requested %d tool calls in one round, capping to %d",
                len(requested_calls),
                _MAX_TOOL_CALLS_PER_ROUND,
            )
            requested_calls = requested_calls[:_MAX_TOOL_CALLS_PER_ROUND]

        remaining_budget = _MAX_TOTAL_TOOL_CALLS_PER_TURN - total_tool_calls
        if remaining_budget <= 0:
            logger.warning(
                "Audience assistant hit the per-turn tool-call cap (%d) before this round",
                _MAX_TOTAL_TOOL_CALLS_PER_TURN,
            )
            break
        if len(requested_calls) > remaining_budget:
            requested_calls = requested_calls[:remaining_budget]

        tool_results = []
        for call in requested_calls:
            cache_key = _tool_cache_key(call["name"], call["arguments"])
            cached_result = result_cache.get(cache_key)
            cache_hit = cached_result is not None
            if cached_result is not None:
                result = cached_result
            else:
                result = await dispatch_tool_call(call["name"], call["arguments"], ctx)
                result_cache[cache_key] = result
                total_tool_calls += 1

            success = "error" not in result

            summary = _summarize_tool_result(result)
            tool_trace.append(
                {
                    "tool": call["name"],
                    "status": "success" if success else "error",
                    "arguments": _safe_parse_arguments(call["arguments"]),
                    "result_summary": f"{summary} (cached)" if cache_hit else summary,
                }
            )

            if call["name"] == "search_comments" and success:
                _record_citable_comments(result, seen_comments)

            tool_results.append({"id": call["id"], "name": call["name"], "content": json.dumps(result)})

        state = provider.append_tool_round(state, requested_calls, tool_results, turn["_raw"])

        if total_tool_calls >= _MAX_TOTAL_TOOL_CALLS_PER_TURN:
            logger.warning(
                "Audience assistant hit the per-turn tool-call cap (%d)", _MAX_TOTAL_TOOL_CALLS_PER_TURN
            )
            break

    logger.warning("Audience assistant turn hit the max tool-call round cap (%d rounds)", max_rounds)
    final_turn = await provider.generate_step(state, force_final=True, excluded_tools=excluded_tools)
    tokens_in, tokens_out = _accumulate_usage(final_turn, tokens_in, tokens_out)
    return _finalize(final_turn["content"], seen_comments, tool_trace, tokens_in, tokens_out)


def _safe_parse_arguments(raw_arguments: str) -> dict:
    try:
        parsed = json.loads(raw_arguments) if raw_arguments else {}
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}
