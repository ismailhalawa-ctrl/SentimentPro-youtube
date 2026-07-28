from app.ai.preprocessors.text_cleaner import normalize_arabic_letters
from app.ai.rules.arabic_lexicon import REQUEST_ANTICIPATION_PHRASES
from app.ai.rules.english_lexicon import REQUEST_ANTICIPATION_PHRASES_EN
from app.ai.rules.negation import INTERROGATIVE_MARKERS_AR, INTERROGATIVE_MARKERS_EN
from app.ai.rules.target_scope import PERSONAL_RELATION_NOUNS_AR, PERSONAL_RELATION_NOUNS_EN

DISAGREEMENT_MARKERS_AR = [
    normalize_arabic_letters(m)
    for m in [
        "بصراحة ما اتفق معك",
        "اختلف معك",
        "اخالفك الرأي",
        "مع احترامي بخالفك",
        "ما اتفق مع كلامك",
        "بخالفك الرأي",
        "برأيي المختلف",
        "مع كامل احترامي بخالفك",
    ]
]
DISAGREEMENT_MARKERS_EN = [
    "i disagree",
    "i don't think that's right",
    "respectfully disagree",
    "i don't agree",
    "not sure i agree",
    "with respect, i disagree",
    "i'd push back on that",
]

INTENT_QUESTION = "question"
INTENT_REQUEST = "request"
INTENT_DISCUSSION = "discussion"
INTENT_DISAGREEMENT = "disagreement"
INTENT_OPINION = "opinion"

_DISCUSSION_MIN_WORDS = 5


def _is_disagreement(text: str) -> bool:
    t = text.lower()
    return any(m in t for m in DISAGREEMENT_MARKERS_AR + DISAGREEMENT_MARKERS_EN)


def _is_question(text: str) -> bool:
    if "؟" in text or "?" in text:
        return True
    t = f" {text.lower().strip()} "
    return any(
        f" {m} " in t or t.strip().startswith(f"{m} ")
        for m in INTERROGATIVE_MARKERS_AR + INTERROGATIVE_MARKERS_EN
    )


def _is_request(text: str, language: str) -> bool:
    t = text.lower()
    phrases = REQUEST_ANTICIPATION_PHRASES_EN if language == "en" else REQUEST_ANTICIPATION_PHRASES
    return any(phrase.lower() in t for phrase in phrases)


def _is_discussion(text: str) -> bool:
    t = text.lower()
    nouns = PERSONAL_RELATION_NOUNS_AR + PERSONAL_RELATION_NOUNS_EN
    return any(n in t for n in nouns) and len(text.split()) >= _DISCUSSION_MIN_WORDS


def detect_intent(text: str, language: str) -> str:
    if _is_disagreement(text):
        return INTENT_DISAGREEMENT
    if _is_question(text):
        return INTENT_QUESTION
    if _is_request(text, language):
        return INTENT_REQUEST
    if _is_discussion(text):
        return INTENT_DISCUSSION
    return INTENT_OPINION
