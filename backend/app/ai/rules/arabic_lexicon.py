import re

from app.ai.preprocessors.text_cleaner import normalize_arabic_letters
from app.ai.rules.negation import is_negated

_ARABIC_LETTER_CLASS = "ء-غف-ي"


def compile_word_boundary_pattern(phrase: str) -> re.Pattern:
    escaped = re.escape(phrase.lower())
    return re.compile(rf"(?<![{_ARABIC_LETTER_CLASS}]){escaped}(?![{_ARABIC_LETTER_CLASS}])")


INTENSIFIER_MARKERS = [
    normalize_arabic_letters(m)
    for m in [
        "جدا",
        "جداً",
        "جدًا",
        "كتير",
        "كثير",
        "مره",
        "مرة",
        "وايد",
        "بزاف",
        "هواي",
        "قوي",
        "قوى",
        "أوي",
        "اوي",
        "خالص",
        "تمام",
        "فوق العادة",
        "جداً جداً",
        "بشدة",
        "للغايه",
        "للغاية",
    ]
]

PRAISE_PHRASES = [
    "رائع",
    "رائعه",
    "رائعة",
    "ممتاز",
    "ممتازه",
    "روعة",
    "روعه",
    "جميل",
    "جميله",
    "حلو",
    "حلوه",
    "تحفة",
    "تحفه",
    "مبدع",
    "مبدعه",
    "استمر",
    "استمري",
    "كمل",
    "أكمل",
    "اكمل",
    "الله يعطيك العافية",
    "يعطيك العافية",
    "يعطيك العافيه",
    "بارك الله فيك",
    "احسنت",
    "أحسنت",
    "برافو",
    "شكرا",
    "شكراً",
    "تسلم ايدك",
    "تسلم إيدك",
    "يسلمو",
    "يسلموا",
    "نايس",
    "حرفيا رائع",
    "افضل قناة",
    "أفضل قناة",
    "افضل يوتيوبر",
    "قناة مميزة",
    "محتوى راقي",
    "محتوى قيم",
    "استفدت كتير",
    "استفدت كثيرا",
    "معلومة قيمة",
    "شرح ممتاز",
    "شرح واضح",
    "الله يبارك فيك",
    "تبارك الله",
    "خيالي",
    "اسطوري",
    "خرافي",
    "مبهر",
    "مذهل",
    "ولا اروع",
    "ولا أروع",
    "احلى قناة",
    "أحلى قناة",
    "بجد رائع",
    "مرجع اساسي",
    "واضحة جدا",
    "تتفوق على نفسك",
    "تفوق التوقعات",
    "لا استغني عن",
    "عاجبني",
    "مفيد او حتى ممتع",
    "استفدت",
    "احب المحتوى",
    "متابع دائم",
    "بالضبط ما كنت ابحث عنه",
    "لن اجد شرح احسن",
]

CRITICISM_PHRASES = [
    "سيء",
    "سيئة",
    "سيئه",
    "زبالة",
    "زباله",
    "وحش",
    "خايس",
    "خايسة",
    "ما عجبني",
    "ما حبيت",
    "مو حلو",
    "مب زين",
    "مش حلو",
    "مش كويس",
    "قليل الادب",
    "قليل الأدب",
    "محتوى ضعيف",
    "ملل",
    "ممل",
    "مملة",
    "مضيعة وقت",
    "مضيعه وقت",
    "تقليد المحتوى",
    "نسخ",
    "سرقة محتوى",
    "مقرف",
    "تافه",
    "تافهة",
    "بايظ",
    "زفت",
    "قذر",
    "احتيال",
    "نصب",
    "كذب",
    "مزيف",
    "ضعيف",
    "ضعيفة",
    "ماعجبنيش",
    "خاطئ",
    "لم افهم شيئا",
    "اضعت وقتي",
    "مشوش",
    "لن اتابع",
    "غير مسموع",
    "غير كافي",
    "لا يوجد اي جهد",
    "المحتوى مكرر",
    "لا انصح",
    "سطحي",
    "لم يستحق",
]

COMPLAINT_PHRASES = [
    "الاعلانات كتير",
    "الإعلانات كثيرة",
    "صوت مو واضح",
    "الصوت مش واضح",
    "جودة سيئة",
    "جودة ضعيفة",
    "التأخير",
    "تأخرتوا",
    "ليش تأخرتوا",
    "وين الحلقة",
    "متى الحلقة الجاية",
    "نزلوا متاخر",
    "الحلقة قصيرة",
    "قصيرة جدا",
    "مافي تفاعل",
    "ما تردون",
    "محد يرد",
    "لا احد يرد",
    "الصوت مو واضح",
    "مزعج",
    "مزعجة",
    "ما ترد",
    "ونقص تفاصيل",
]

REQUEST_ANTICIPATION_PHRASES = [
    "ممكن",
    "لو سمحت",
    "لو سمحتوا",
    "ابغى",
    "أبغى",
    "ابي",
    "أبي",
    "عايز",
    "عاوز",
    "بدي",
    "بدنا",
    "نزل",
    "تنزل",
    "ينزل",
    "انزل",
    "أنزل",
    "نزلوا",
    "الجزء الثاني",
    "الجزء التاني",
    "جزء ثاني",
    "متى الحلقة",
    "وين الحلقة الجايه",
    "يوميا",
    "كل يوم",
    "بسرعة لو سمحت",
    "ما تفوتنا",
    "لا تتأخر",
    "بانتظار الجزء",
    "بانتظار المزيد",
    "نفسي اشوف",
    "نفسي أشوف",
    "ياريت تكمل",
    "ياريت تسوي",
]

DISAPPOINTMENT_PHRASES = [
    "للأسف",
    "للاسف",
    "بصراحة خيبة أمل",
    "خيبة أمل",
    "خيبة امل",
    "توقعت أحسن",
    "توقعت احسن",
    "توقعت افضل",
    "زعلان",
    "زعلانة",
    "حزين",
    "حزينة",
    "يا خسارة",
    "يا حرام",
    "محبط",
    "محبطة",
    "خذلتونا",
    "خذلني",
    "ما توقعت",
    "نزل مستواكم",
    "تراجع المستوى",
    "حسبي الله",
    "شر البلية",
    "توقعت محتوى افضل",
    "قديمة وغير محدثة",
    "ليس المستوى المعتاد",
    "تراجع واضح",
    "اتوقع احسن",
]

CONSTRUCTIVE_CRITICISM_PHRASES = [
    "يحتاج تحسين",
    "تحتاج تحسين",
    "يحتاج شغل اكثر",
    "يحتاج شغل أكثر",
    "طويل شوي",
    "طويل شويه",
    "مو مرتب",
    "ملخبط",
    "ينقصه امثلة",
    "ينقصه أمثلة",
    "التنظيم مو مرتب",
    "تختصر",
]

ADMIRATION_PHRASES = [
    "أسطورة",
    "اسطورة",
    "ملك",
    "ملكة",
    "قدوة",
    "فخورين فيك",
    "نفتخر فيك",
    "الأفضل",
    "الافضل",
    "ولا مرة خيبتنا",
    "دايم مبدع",
    "دائما مبدع",
    "قمة الابداع",
    "قمة الإبداع",
    "لا يوجد مثلك",
    "أنت الأفضل",
    "انت الافضل",
    "أسطوره حقيقية",
    "بطل",
    "بطلة",
    "متلك",
    "زيك",
    "بحالك",
]

RELIGIOUS_POSITIVE_PHRASES = [
    "ماشاء الله",
    "ما شاء الله",
    "الحمدلله",
    "الحمد لله",
    "بارك الله فيك",
    "الله يبارك فيك",
    "جزاك الله خير",
    "جزاك الله خيرا",
    "الله يوفقك",
    "ربي يحفظك",
    "الله يخليك",
    "الله يعطيك العافية",
    "تبارك الرحمن",
    "ما شاء الله عليك",
    "الله يسعدك",
    "ربنا يكرمك",
    "الله يجزاك خير",
    "الله يعينك",
    "رمضان كريم",
    "رمضان مبارك",
]

EARLY_ENGAGEMENT_PHRASES = [
    "جيت بدري",
    "جيت بكري",
    "جيت بكير",
    "اول تعليق",
    "أول تعليق",
    "قبل الجميع",
    "اول مشاهد",
    "أول مشاهد",
    "من الثانية الاولى",
    "من الثانيه الاولى",
    "من الدقيقة الأولى",
    "من الدقيقه الاولى",
    "سبقت الكل",
    "قبل الترند",
    "جيت من اول",
    "اول واحد",
    "أول واحد",
    "سبقتكم",
]

LONGING_AFFECTION_PHRASES = [
    "اشتقنا",
    "اشتقتلك",
    "اشتقنالك",
    "اشتقت",
    "افتقدناك",
    "افتقدنالك",
    "وحشتنا",
    "وحشتونا",
    "وحشتيني",
    "غايبين",
    "زمان ما شفناك",
    "زمان ماشفناك",
    "من زمان ما نزلت",
    "وينك",
    "فينك",
    "وينكم",
    "من زمان عنا",
    "اشتقنا لك",
    "اشتقنا لفيديوهاتك",
    "اشتقنا للحلقات",
]

DIALECT_PRAISE_PHRASES = {
    "gulf": ["زين", "خوش", "يبيلك عافية", "ماشاء الله عليك", "طقطقة", "وايد حلو", "زين هواي"],
    "levant": ["منيح", "كتير حلو", "تمام كتير", "معلم", "يا معلم", "زلمة", "منيحة كتير"],
    "egyptian": ["جامد", "حلو قوي", "تحفه اوي", "جامد اوي", "يا نجم", "فنان يا كبير"],
    "iraqi": ["زين هواي", "روعه هواي", "هواي حلو", "چا زين", "عاشت ايدك"],
    "maghrebi": ["مليح", "زوين", "واعر", "نيشان", "بزاف مزيان", "زوينة", "نظيفة"],
}

_ALL_DIALECT_PRAISE = [phrase for phrases in DIALECT_PRAISE_PHRASES.values() for phrase in phrases]

_CATEGORY_PHRASES = {
    "praise": (PRAISE_PHRASES + _ALL_DIALECT_PRAISE, "positive", "strong"),
    "admiration": (ADMIRATION_PHRASES, "positive", "strong"),
    "religious": (RELIGIOUS_POSITIVE_PHRASES, "positive", "moderate"),
    "longing_affection": (LONGING_AFFECTION_PHRASES, "positive", "strong"),
    "early_engagement": (EARLY_ENGAGEMENT_PHRASES, "positive", "moderate"),
    "request_anticipation": (REQUEST_ANTICIPATION_PHRASES, "positive", "weak"),
    "criticism": (CRITICISM_PHRASES, "negative", "strong"),
    "complaint": (COMPLAINT_PHRASES, "negative", "moderate"),
    "disappointment": (DISAPPOINTMENT_PHRASES, "negative", "strong"),
    "constructive_criticism": (CONSTRUCTIVE_CRITICISM_PHRASES, "negative", "moderate"),
}

_CATEGORY_PHRASES = {
    category: ([normalize_arabic_letters(phrase) for phrase in phrases], polarity, strength)
    for category, (phrases, polarity, strength) in _CATEGORY_PHRASES.items()
}

_CATEGORY_PATTERNS = {
    category: (
        [(phrase, compile_word_boundary_pattern(phrase)) for phrase in phrases],
        polarity,
        strength,
    )
    for category, (phrases, polarity, strength) in _CATEGORY_PHRASES.items()
}

_STRENGTH_RANK = {"weak": 0, "moderate": 1, "strong": 2}
_OPPOSITE = {"positive": "negative", "negative": "positive"}


def _has_intensifier(text: str) -> bool:
    return any(marker in text for marker in INTENSIFIER_MARKERS)


_DOWNGRADE = {"strong": "moderate", "moderate": "weak", "weak": "weak"}


def analyze_arabic_text(text: str) -> dict:
    t = text.lower()
    matches: list[tuple[str, str, str]] = []

    for category, (phrase_patterns, polarity, strength) in _CATEGORY_PATTERNS.items():
        for _phrase, pattern in phrase_patterns:
            found = pattern.search(t)
            if found is None:
                continue
            idx = found.start()

            effective_polarity = polarity
            effective_strength = strength

            if is_negated(t, idx, "ar"):
                effective_polarity = _OPPOSITE[polarity]
                effective_strength = "moderate"
            elif _has_intensifier(t) and effective_strength == "weak":
                effective_strength = "moderate"

            matches.append((category, effective_polarity, effective_strength))
            break

    if not matches:
        return {"polarity": None, "strength": "weak", "category": None, "mixed": False}

    has_positive = any(polarity == "positive" for _, polarity, _ in matches)
    has_negative = any(polarity == "negative" for _, polarity, _ in matches)
    mixed = has_positive and has_negative

    category, polarity, strength = max(matches, key=lambda m: _STRENGTH_RANK[m[2]])
    if mixed:
        strength = _DOWNGRADE[strength]

    return {"polarity": polarity, "strength": strength, "category": category, "mixed": mixed}
