GRIEF_RELIGIOUS_FORMULAS_AR = [
    "الله يرحمه",
    "الله يرحمها",
    "رحمه الله",
    "رحمها الله",
    "البقاء لله",
    "عظم الله اجركم",
    "عظم الله أجركم",
    "انا لله وانا اليه راجعون",
    "إنا لله وإنا إليه راجعون",
    "اللهم ارحمه",
    "اللهم ارحمها",
    "اللهم ارحم موتانا",
    "دعواتكم",
    "ادعولي",
    "ادعوا لي",
    "يارب انجح",
    "يا رب انجح",
    "الله يعافيكم",
    "الله يشفيه",
    "الله يشفيها",
]

GRIEF_RELIGIOUS_FORMULAS_EN = [
    "rest in peace",
    "rip",
    "may he rest in peace",
    "may she rest in peace",
    "please pray for",
    "praying for my",
    "keep us in your prayers",
    "thoughts and prayers",
    "god rest his soul",
    "god rest her soul",
]

EMOTION_GRIEF_RELIGIOUS = "grief_religious"

GREETING_FORMULAS_AR = [
    "السلام عليكم",
    "السلام عليكم ورحمة الله",
    "مرحبا بالجميع",
    "هلا والله",
    "اهلا وسهلا",
]

GREETING_FORMULAS_EN = [
    "hello everyone",
    "good morning all",
    "good evening everyone",
    "hi from",
    "hey there, new subscriber",
    "greetings from",
    "hello, first time watching",
    "hi, just found this channel",
]

_GREETING_MAX_WORDS = 6


def detect_formulaic_emotion(text: str, language: str) -> tuple[bool, str | None]:
    t = text.lower()
    formulas = GRIEF_RELIGIOUS_FORMULAS_EN if language == "en" else GRIEF_RELIGIOUS_FORMULAS_AR
    other_formulas = GRIEF_RELIGIOUS_FORMULAS_AR if language == "en" else GRIEF_RELIGIOUS_FORMULAS_EN

    if any(phrase in t for phrase in formulas) or any(phrase in t for phrase in other_formulas):
        return True, EMOTION_GRIEF_RELIGIOUS
    return False, None


def detect_greeting(text: str) -> bool:
    t = text.lower().strip()
    if len(t.split()) > _GREETING_MAX_WORDS:
        return False
    return any(phrase in t for phrase in GREETING_FORMULAS_AR + GREETING_FORMULAS_EN)
