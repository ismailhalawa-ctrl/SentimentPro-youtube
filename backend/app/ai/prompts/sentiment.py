from app.ai.prompts._shared import CONTEXTUAL_NUANCE, INJECTION_DEFENSE, LANGUAGE_COVERAGE

SYSTEM_PROMPT = (
    f"You are a sentiment classifier for YouTube comments, {LANGUAGE_COVERAGE}. "
    "Classify the commenter's sentiment TOWARD THE VIDEO, ITS CREATOR, OR "
    "THEIR OWN EXPERIENCE WATCHING IT — not the literal positivity/"
    "negativity of the topic the video or comment discusses.\n\n"
    f"{CONTEXTUAL_NUANCE}\n\n"
    f"{INJECTION_DEFENSE}\n\n"
    "Respond with ONLY a JSON object, no other text."
)


def build_prompt(text: str, **kwargs) -> list[dict]:
    language = kwargs.get("language", "auto-detect")
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f'Comment (detected language: {language}):\n"""\n{text}\n"""\n\n'
                "Respond with ONLY this JSON shape:\n"
                '{"label": "positive" | "neutral" | "negative", '
                '"confidence": <number between 0 and 1>, '
                '"reasoning": "<one short sentence>"}'
            ),
        },
    ]
