import re
from collections import Counter

ARABIC_STOP = {
    "في",
    "من",
    "على",
    "إلى",
    "الى",
    "عن",
    "مع",
    "هذا",
    "هذه",
    "هو",
    "هي",
    "أن",
    "ان",
    "كان",
    "لي",
    "لك",
    "له",
    "لها",
    "نحن",
    "أنت",
    "انت",
    "أنا",
    "انا",
    "هم",
    "عند",
    "كل",
    "قد",
    "لم",
    "لا",
    "ما",
    "يا",
    "اي",
    "اللي",
    "الي",
    "وان",
    "وفي",
    "وهو",
    "وهي",
    "انه",
    "بس",
    "زي",
    "عشان",
    "علشان",
    "دا",
    "ده",
    "دي",
    "مش",
    "مو",
    "مب",
    "وش",
    "يلي",
    "حتى",
    "حتا",
    "لو",
    "لان",
    "لأن",
    "بعد",
    "قبل",
    "فيه",
    "فيها",
    "منه",
    "منها",
    "عليه",
    "عليها",
}
ENGLISH_STOP = {
    "the",
    "a",
    "an",
    "is",
    "it",
    "this",
    "that",
    "to",
    "and",
    "of",
    "in",
    "for",
    "on",
    "with",
    "i",
    "you",
    "we",
    "are",
    "was",
    "be",
    "have",
    "not",
    "but",
    "your",
    "they",
    "he",
    "she",
    "at",
    "by",
    "as",
    "do",
    "so",
    "if",
    "or",
    "its",
    "me",
    "my",
    "just",
    "very",
}
STOP_WORDS = ARABIC_STOP | ENGLISH_STOP

COMMON_NOISE_WORDS = {
    "youtube",
    "video",
    "videos",
    "channel",
    "comment",
    "comments",
    "watching",
    "viewer",
    "watch",
    "like",
    "liked",
    "subscribe",
    "lol",
    "lmao",
    "haha",
    "omg",
    "wow",
    "yeah",
    "yep",
    "ok",
    "okay",
    "one",
    "two",
    "three",
    "good",
    "great",
    "nice",
    "make",
    "فيديو",
    "الفيديو",
    "يوتيوب",
    "القناة",
    "قناة",
    "تعليق",
    "التعليق",
    "مشاهد",
    "متابع",
    "شاهد",
    "يشاهد",
    "يتابع",
    "تابع",
    "هههه",
    "ههههه",
    "هههههه",
    "هههههههه",
    "جميل",
    "حلو",
    "تمام",
    "مرحبا",
    "اهلا",
}

TOPIC_KEYWORDS = {
    "التمثيل / Acting": ["تمثيل", "ممثل", "ممثلة", "اداء", "actor", "acting", "performance", "cast"],
    "الموسيقى / Music": ["موسيقى", "اغنية", "أغنية", "صوت", "music", "song", "soundtrack", "beat"],
    "الإيقاع / Pacing": ["طويل", "قصير", "ممل", "مملة", "بطيء", "slow", "fast", "boring", "pacing"],
    "التصوير / Visuals": ["كاميرا", "تصوير", "لقطة", "camera", "cinematography", "shot", "visual"],
    "الإضاءة / Lighting": ["اضاءة", "إضاءة", "lighting", "light", "dark", "bright"],
    "الذكاء الاصطناعي / AI": ["ai", "chatgpt", "gpt", "llm", "ذكاء اصطناعي", "ذكاء"],
    "الألعاب / Gaming": ["game", "gaming", "لعبة", "العاب", "gamer", "gameplay"],
    "التعليم / Education": ["تعليم", "شرح", "درس", "course", "lesson", "tutorial", "learn"],
    "القصة / Story": ["قصة", "حبكة", "story", "plot", "script", "ending", "نهاية"],
    "الإخراج / Direction": ["مخرج", "إخراج", "director", "direction", "scene"],
}

_AR_NORM = str.maketrans("أإآاى", "ااااي")


def _normalize_ar(word: str) -> str:
    word = word.translate(_AR_NORM)
    word = re.sub(r"ة$", "ه", word)
    word = re.sub(r"[ؐ-ًؚ-ٟ]", "", word)
    return word


def get_top_words(texts: list[str], top_n: int = 20) -> list[tuple[str, int]]:
    word_freq: Counter = Counter()

    for text in texts:
        for raw_word in str(text).split():
            word = re.sub(r"[^\w؀-ۿ]", "", raw_word).lower().strip()
            if not word:
                continue
            if re.fullmatch(r"[\d._]+", word):
                continue
            is_arabic_word = bool(re.search(r"[؀-ۿ]", word))
            if len(word) < 3:
                continue
            if word in STOP_WORDS or word in COMMON_NOISE_WORDS:
                continue

            key = _normalize_ar(word) if is_arabic_word else word
            if key in COMMON_NOISE_WORDS:
                continue

            word_freq[key] += 1

    return word_freq.most_common(top_n)


def get_topics(texts: list[str]) -> dict[str, int]:
    topics: dict[str, int] = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        count = 0
        for text in texts:
            text_lower = str(text).lower()
            found = False
            for kw in keywords:
                kw_lower = kw.lower()
                pattern = (
                    rf"\b{re.escape(kw_lower)}\b" if re.search(r"[a-zA-Z]", kw_lower) else re.escape(kw_lower)
                )
                if re.search(pattern, text_lower):
                    found = True
                    break
            if found:
                count += 1
        if count > 0:
            topics[topic] = count
    return dict(sorted(topics.items(), key=lambda x: x[1], reverse=True))
