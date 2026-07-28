NEGATION_MARKERS_AR = [
    "ما",
    "مو",
    "مب",
    "مش",
    "مافي",
    "ماكو",
    "مافيش",
    "معندي",
    "لا",
    "لن",
    "لم",
    "بلا",
    "دون",
]

NEGATION_MARKERS_EN = [
    "not",
    "no",
    "never",
    "isn't",
    "wasn't",
    "aren't",
    "weren't",
    "doesn't",
    "don't",
    "didn't",
    "won't",
    "wouldn't",
    "can't",
    "cannot",
    "couldn't",
    "shouldn't",
    "without",
]

CONTRAST_CONNECTIVES_AR = [
    "لكن",
    "بس",
    "ولكن",
    "الا ان",
    "إلا أن",
    "غير ان",
    "غير أن",
    "مع ان",
    "مع أن",
    "رغم ان",
    "رغم أن",
    "رغم",
]
CONTRAST_CONNECTIVES_EN = ["but", "however", "although", "though", "yet"]

INTERROGATIVE_MARKERS_AR = [
    "ليش",
    "ليه",
    "كيف",
    "كيفكم",
    "متى",
    "متي",
    "وين",
    "فين",
    "وش",
    "شو",
    "ايش",
    "هل",
    "لماذا",
    "كم",
]
INTERROGATIVE_MARKERS_EN = [
    "what",
    "why",
    "how",
    "when",
    "where",
    "which",
    "who",
    "is this",
    "are you",
    "do you",
    "can you",
]

_CLAUSE_PUNCTUATION = set(".!?؟،,;:\n")
_MAX_SCOPE_CHARS = 35

_NON_NEGATING_IDIOMS_AR = ["ما بين شك", "ما في شك", "ما فيه شك"]


def _connectives_for(language: str) -> list[str]:
    return CONTRAST_CONNECTIVES_EN if language == "en" else CONTRAST_CONNECTIVES_AR


def _interrogatives_for(language: str) -> list[str]:
    return INTERROGATIVE_MARKERS_EN if language == "en" else INTERROGATIVE_MARKERS_AR


def _markers_for(language: str) -> list[str]:
    return NEGATION_MARKERS_EN if language == "en" else NEGATION_MARKERS_AR


def _boundary_index_before(text: str, position: int, language: str) -> int:
    boundary = 0
    for i in range(position - 1, -1, -1):
        if text[i] in _CLAUSE_PUNCTUATION:
            boundary = i + 1
            break

    for connective in _connectives_for(language):
        idx = text.rfind(connective, 0, position)
        if idx != -1:
            end = idx + len(connective)
            if end > boundary:
                boundary = end

    for marker in _interrogatives_for(language):
        idx = text.rfind(marker, 0, position)
        if idx > boundary:
            boundary = idx

    return max(boundary, position - _MAX_SCOPE_CHARS, 0)


def negation_scope(text: str, phrase_start: int, language: str) -> str:
    start = _boundary_index_before(text, phrase_start, language)
    return text[start:phrase_start]


def _count_negation_markers(scope: str, language: str) -> int:
    if language == "ar":
        for idiom in _NON_NEGATING_IDIOMS_AR:
            scope = scope.replace(idiom, "")
    padded = f" {scope} "
    return sum(padded.count(f" {marker} ") for marker in _markers_for(language))


def is_negated(text: str, phrase_start: int, language: str) -> bool:
    scope = negation_scope(text, phrase_start, language)
    return _count_negation_markers(scope, language) % 2 == 1
