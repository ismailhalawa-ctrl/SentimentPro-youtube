from app.ai.prompts._shared import INJECTION_DEFENSE, resolve_language_instruction

SYSTEM_PROMPT = (
    "You are an audience research analyst reading YouTube comments "
    "(Arabic — all major dialects, English, and mixed-language) to "
    "profile the commenting audience for a content creator. Base every "
    "claim on patterns actually visible in the comments provided — do "
    "not invent demographic details the comments don't support.\n\n"
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
                '  "personality_profile": "<2-3 sentence narrative describing the commenting audience>",\n'
                '  "viewer_segments": [{"name": "<short label>", "description": "<1 sentence>", '
                '"estimated_share": "<e.g. \'roughly a third\'>"}, ...],\n'
                '  "behavior_notes": ["<short observation about how this audience engages>", ...],\n'
                '  "emotional_trend": "<1-2 sentence narrative on the dominant emotional tone and any shifts>"\n'
                "}"
            ),
        },
    ]
