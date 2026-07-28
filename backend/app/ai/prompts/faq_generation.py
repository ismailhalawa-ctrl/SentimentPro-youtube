from app.ai.prompts._shared import INJECTION_DEFENSE, LANGUAGE_COVERAGE, resolve_language_instruction

SYSTEM_PROMPT = (
    f"You are analyzing YouTube comments, {LANGUAGE_COVERAGE}, to find "
    "questions viewers are repeatedly asking about the video, so the "
    "creator can address them once instead of replying individually. "
    "Only include questions that actually appear (in substance, even if "
    "worded differently) across MULTIPLE comments — a single one-off "
    "question from one viewer doesn't belong in a FAQ. Write a short, "
    "genuinely useful answer for each, based only on what's reasonably "
    "inferable from the video's context and the comments themselves — if "
    "the real answer isn't knowable from the comments alone, say so "
    "briefly rather than inventing specifics.\n\n"
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
                '  "faqs": [{"question": "<the recurring question, phrased clearly>", '
                '"answer": "<short, grounded answer>", '
                '"times_asked_estimate": <rough integer count of how many comments raised this>}, ...]\n'
                "}"
            ),
        },
    ]
