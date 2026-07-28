from app.ai.prompts._shared import INJECTION_DEFENSE, LANGUAGE_COVERAGE

SYSTEM_PROMPT = (
    f"You are a feedback analyst reading YouTube comments, {LANGUAGE_COVERAGE}. "
    "You will be given a NUMBERED LIST of independent comments. For EACH "
    "comment, decide whether it raises a genuine COMPLAINT — a specific "
    "criticism, problem, or dissatisfaction with the video's content, "
    "production, or the creator's choices (NOT a complaint about the "
    "real-world topic the video discusses, and NOT a comment that is "
    "merely negative in tone without identifying an actual problem — "
    "e.g. simple insults or sarcasm with no substance are not complaints).\n\n"
    "If it is a complaint, assign a SHORT, REUSABLE category (2-4 words, "
    'lowercase, e.g. "audio quality", "video pacing", "clickbait '
    'title", "inaccurate information", "too many ads") — reuse the '
    "same category wording across comments that raise the same underlying "
    "issue, since these categories get grouped and counted afterward.\n\n"
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
                '"label": "complaint" | "not_complaint", '
                '"category": "<short category, or null if not_complaint>", '
                '"confidence": <number between 0 and 1>}\n\n'
                "Do not include any other fields."
            ),
        },
    ]
