from app.ai.prompts._shared import INJECTION_DEFENSE, resolve_language_instruction

SYSTEM_PROMPT = (
    "You are an analyst summarizing YouTube comment sentiment for a "
    "content creator, across Arabic (all major dialects), English, and "
    "mixed-language comments. Write for someone who has not read the "
    "comments themselves.\n\n"
    f"{INJECTION_DEFENSE}\n\n"
    "Respond with ONLY a JSON object, no other text."
)

_PROTECTED_ENUM_CAVEAT = (
    " Do NOT translate the overall_sentiment_label value itself — it must "
    "stay exactly one of the literal English tokens positive, neutral, "
    "negative, or mixed, since the frontend matches on that exact string."
)


def build_prompt(text: str, **kwargs) -> list[dict]:
    video_title = kwargs.get("video_title", "this video")
    language_instruction = resolve_language_instruction(kwargs.get("response_language", "en"))
    language_instruction += _PROTECTED_ENUM_CAVEAT
    return [
        {"role": "system", "content": f"{SYSTEM_PROMPT} {language_instruction}"},
        {
            "role": "user",
            "content": (
                f'Comments for "{video_title}" (one per line):\n"""\n{text}\n"""\n\n'
                "Respond with ONLY this JSON shape:\n"
                "{\n"
                '  "overview": "<2-4 sentence plain-language summary>",\n'
                '  "key_positives": ["<short point>", ...],\n'
                '  "key_negatives": ["<short point>", ...],\n'
                '  "notable_trends": ["<short point>", ...],\n'
                '  "overall_sentiment_label": "positive" | "neutral" | "negative" | "mixed"\n'
                "}"
            ),
        },
    ]
