from app.ai.preprocessors.text_cleaner import normalize_arabic_letters

PERSONAL_RELATION_NOUNS_AR = [
    normalize_arabic_letters(n)
    for n in [
        "اهلي",
        "أهلي",
        "امي",
        "أمي",
        "ابوي",
        "أبوي",
        "اختي",
        "أختي",
        "اخوي",
        "أخوي",
        "صاحبي",
        "صديقي",
        "صديقتي",
        "عائلتي",
        "زوجي",
        "زوجتي",
        "خطيبي",
        "خطيبتي",
        "جدتي",
        "جدي",
        "ولدي",
        "بنتي",
        "عمي",
        "خالي",
        "علاقتي",
        "علاقتنا",
        "زواجي",
        "طلاقي",
        "انا منفصله",
        "انا منفصل",
        "شغلي",
    ]
]

_TROUBLED_RELATIONSHIP_MARKERS_AR = [normalize_arabic_letters(w) for w in ["سيئة", "سيئه", "فاشلة"]]

LIFE_EVENT_VERBS_AR = [
    normalize_arabic_letters(v)
    for v in [
        "انفصلوا",
        "انفصلت",
        "منفصلين",
        "منفصلة",
        "منفصل",
        "توفي",
        "توفيت",
        "مات",
        "ماتت",
        "مرض",
        "مرضت",
        "مريض",
        "مريضة",
        "تعبان",
        "تعبانة",
        "تخرجت",
        "تخرجنا",
        "فقدت شغلي",
        "دخل المستشفى",
        "دخلت المستشفى",
        "طلقت",
        "اتطلقت",
        "انفصلنا",
        "اكتئاب",
        "حزين بسبب",
        "حزينة بسبب",
        "علاقتنا سيئة",
        "علاقتهم سيئة",
        "علاقته سيئة",
        "علاقتها سيئة",
        "علاقة سيئة",
        "علاقة فاشلة",
        "فاشلة",
        "فاشل",
    ]
]

VIDEO_TARGET_MARKERS_AR = [
    normalize_arabic_letters(m)
    for m in [
        "الفيديو",
        "الشرح",
        "القناة",
        "المحتوى",
        "فيديوهاتك",
        "قناتك",
        "شرحك",
        "محتواك",
        "الحلقة",
        "المقطع",
        "شغلك",
        "قناتكم",
        "فيديوكم",
    ]
]

PERSONAL_RELATION_NOUNS_EN = [
    "my mom",
    "my dad",
    "my parents",
    "my family",
    "my friend",
    "my sister",
    "my brother",
    "my partner",
    "my dog",
    "my cat",
    "my job",
    "my grandma",
    "my grandpa",
    "breakup",
]

LIFE_EVENT_VERBS_EN = [
    "passed away",
    "got divorced",
    "broke up",
    "lost my job",
    "got diagnosed",
    "went through a hard",
    "tough times",
    "in the hospital",
    "still processing it",
    "depressed",
    "not feeling well",
    "struggling with",
    "hard breakup",
]

VIDEO_TARGET_MARKERS_EN = [
    "this video",
    "the video",
    "your channel",
    "your content",
    "this channel",
    "your explanation",
    "your videos",
    "this content",
]

TARGET_VIDEO = "video"
TARGET_PERSONAL_LIFE = "personal_life"
TARGET_AMBIGUOUS = "ambiguous"


def detect_target_scope(span_text: str, language: str) -> tuple[str, float]:
    t = span_text.lower()

    has_video_marker = any(m in t for m in VIDEO_TARGET_MARKERS_AR) or any(
        m in t for m in VIDEO_TARGET_MARKERS_EN
    )
    has_personal_noun = any(n in t for n in PERSONAL_RELATION_NOUNS_AR) or any(
        n in t for n in PERSONAL_RELATION_NOUNS_EN
    )
    has_life_event = any(v in t for v in LIFE_EVENT_VERBS_AR) or any(v in t for v in LIFE_EVENT_VERBS_EN)
    has_troubled_relationship = "علاقة" in t and any(w in t for w in _TROUBLED_RELATIONSHIP_MARKERS_AR)

    if has_video_marker:
        return TARGET_VIDEO, 0.9
    if has_personal_noun and (has_life_event or has_troubled_relationship):
        return TARGET_PERSONAL_LIFE, 0.85
    return TARGET_AMBIGUOUS, 0.5
