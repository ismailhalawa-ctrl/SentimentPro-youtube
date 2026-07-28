from app.ai.prompts._shared import INJECTION_DEFENSE, LANGUAGE_COVERAGE

SYSTEM_PROMPT = (
    f"You are a feedback analyst reading YouTube comments, {LANGUAGE_COVERAGE}. "
    "You will be given a NUMBERED LIST of independent comments. For EACH "
    "comment, decide whether it raises a genuine SUGGESTION — a specific, "
    "constructive proposal for what the creator could do differently or "
    "next (a topic to cover, a format change, a feature/tool request), "
    "NOT a general compliment or complaint with no actionable proposal.\n\n"
    "If it is a suggestion, assign a SHORT, REUSABLE category (2-4 words, "
    'lowercase, e.g. "add timestamps", "cover topic X", "longer '
    'videos", "more frequent uploads") — reuse the same category '
    "wording across comments proposing the same thing, since these "
    "categories get grouped and counted afterward. Also set "
    '"is_feature_request" true when the suggestion is specifically about '
    "a channel/video FORMAT or TOOL (timestamps, captions, playlists, "
    "upload schedule) rather than a content topic to cover.\n\n"
    f"{INJECTION_DEFENSE}\n\n"
    "Respond with ONLY a JSON array, no other text. The array MUST contain "
    "EXACTLY one object per input comment, using the comment's original "
    'number as "index".'
)


def build_prompt(texts: list[str], **kwargs) -> list[dict]:
    numbered = "\n".join(f'{i}. """{t}"""' for i, t in enumerate(texts))
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Comments ({len(texts)} total):\n{numbered}\n\n"
                f"Respond with ONLY a JSON array of exactly {len(texts)} objects, "
                "each shaped:\n"
                '{"index": <the comment\'s number above>, '
                '"label": "suggestion" | "not_suggestion", '
                '"category": "<short category, or null if not_suggestion>", '
                '"is_feature_request": <true | false>, '
                '"confidence": <number between 0 and 1>}\n\n'
                "Do not include any other fields."
            ),
        },
    ]
