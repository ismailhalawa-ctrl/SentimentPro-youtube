from app.ai.prompts._shared import INJECTION_DEFENSE, LANGUAGE_COVERAGE, resolve_language_instruction

SYSTEM_PROMPT = (
    f"You are an audience-growth analyst reading YouTube comments, "
    f"{LANGUAGE_COVERAGE}, for a content creator. You are given the "
    "video's already-computed audience scores (satisfaction, community "
    "health, loyalty — each 0-100) as context; do not recompute or "
    "restate them, use them as background. Identify EMERGING TRENDS "
    "(shifts or patterns becoming noticeable in this comment section, not "
    "just a restatement of the overall sentiment) and concrete GROWTH "
    "OPPORTUNITIES (specific, actionable ideas grounded in what commenters "
    'are actually saying — not generic advice like "post more '
    'consistently" unless the comments themselves suggest that).\n\n'
    f"{INJECTION_DEFENSE}\n\n"
    "Respond with ONLY a JSON object, no other text."
)


def build_prompt(text: str, **kwargs) -> list[dict]:
    video_title = kwargs.get("video_title", "this video")
    scores = kwargs.get("scores", {})
    language_instruction = resolve_language_instruction(kwargs.get("response_language", "en"))
    scores_summary = (
        f"Satisfaction: {scores.get('satisfaction_score', 'n/a')}/100, "
        f"Community health: {scores.get('community_health_score', 'n/a')}/100, "
        f"Loyalty: {scores.get('loyalty_score', 'n/a')}/100"
    )
    return [
        {"role": "system", "content": f"{SYSTEM_PROMPT} {language_instruction}"},
        {
            "role": "user",
            "content": (
                f'Computed scores for "{video_title}": {scores_summary}\n\n'
                f'Comments (one per line):\n"""\n{text}\n"""\n\n'
                "Respond with ONLY this JSON shape:\n"
                "{\n"
                '  "emerging_trends": ["<short observation>", ...],\n'
                '  "growth_opportunities": ["<short, concrete, actionable idea>", ...]\n'
                "}"
            ),
        },
    ]
