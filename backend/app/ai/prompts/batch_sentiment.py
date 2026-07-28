from app.ai.prompts._shared import CONTEXTUAL_NUANCE, INJECTION_DEFENSE, LANGUAGE_COVERAGE

SYSTEM_PROMPT = (
    f"You are a sentiment classifier and audience insight analyst for YouTube comments, "
    f"{LANGUAGE_COVERAGE}. You will be given a NUMBERED LIST of independent comments, sampled "
    "to represent the full comment section of one video. Classify the commenter's sentiment "
    "TOWARD THE VIDEO, ITS CREATOR, OR THEIR OWN EXPERIENCE WATCHING IT for EACH comment "
    "separately — not the literal positivity/negativity of the topic it discusses, and not "
    "influenced by any other comment in the list.\n\n"
    f"{CONTEXTUAL_NUANCE}\n\n"
    f"{INJECTION_DEFENSE}\n\n"
    "You will also write 4 to 6 short, specific, video-level insights grounded in the actual "
    "comment text and any aggregate statistics you're given — name concrete topics, praise, or "
    "complaints the audience actually raised. Never invent a statistic you weren't given."
)


def build_prompt(texts: list[str], aggregate_stats: dict | None = None, **kwargs) -> list[dict]:
    numbered = "\n".join(f'{i}. """{t}"""' for i, t in enumerate(texts))

    stats_block = ""
    if aggregate_stats:
        stats_block = (
            "\n\nAggregate statistics for the full comment set this sample was drawn from "
            f"({aggregate_stats.get('total_comments', len(texts)):,} comments): "
            f"{aggregate_stats.get('positive_pct', 0)}% positive, "
            f"{aggregate_stats.get('neutral_pct', 0)}% neutral, "
            f"{aggregate_stats.get('negative_pct', 0)}% negative, "
            f"dominant language {aggregate_stats.get('top_language', 'unknown')}."
        )

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Comments ({len(texts)} total):\n{numbered}"
                f"{stats_block}\n\n"
                "Respond with ONLY a JSON object, no other text, shaped:\n"
                '{"comments": [{"index": <the comment\'s number above>, '
                '"label": "positive" | "neutral" | "negative", '
                '"confidence": <number between 0 and 1>}, ...], '
                '"ai_insights": ["<insight 1>", "<insight 2>", ...]}\n\n'
                f"comments must contain EXACTLY one object per input comment, {len(texts)} total, "
                "in any order. ai_insights must contain between 4 and 6 short strings. Do not "
                "include any other fields."
            ),
        },
    ]
