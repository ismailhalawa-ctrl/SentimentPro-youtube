from app.ai.prompts._shared import INJECTION_DEFENSE, LANGUAGE_COVERAGE, resolve_language_instruction

SYSTEM_PROMPT = (
    f"You are analyzing YouTube comments, {LANGUAGE_COVERAGE}, to find the "
    "main TOPICS commenters are discussing — semantically, not just exact "
    'keyword matches (e.g. "audio issues", "sound problems", and '
    '"can\'t hear the narration" are the SAME topic and must be merged '
    "into one cluster, not listed separately). For each topic, estimate "
    "what share of comments touch on it and note the dominant sentiment "
    "within that topic specifically (a topic can be discussed positively "
    "by most commenters even if the video overall has mixed sentiment).\n\n"
    f"{INJECTION_DEFENSE}\n\n"
    "Respond with ONLY a JSON object, no other text."
)


def build_prompt(text: str, **kwargs) -> list[dict]:
    video_title = kwargs.get("video_title", "this video")
    language_instruction = resolve_language_instruction(kwargs.get("response_language", "en"))
    return [
        {"role": "system", "content": f"{SYSTEM_PROMPT} {language_instruction}"},
        {
            "role": "user",
            "content": (
                f'Comments for "{video_title}" (one per line):\n"""\n{text}\n"""\n\n'
                "Respond with ONLY this JSON shape:\n"
                "{\n"
                '  "topics": [{"name": "<short topic label>", '
                '"description": "<1 sentence>", '
                '"estimated_share": "<e.g. \'roughly a quarter of comments\'>", '
                '"dominant_sentiment": "positive" | "neutral" | "negative" | "mixed"}, ...]\n'
                "}"
            ),
        },
    ]
