import re

_LINK_RE = re.compile(r"https?://\S+|www\.\S+", re.I)
_PHONE_RE = re.compile(r"(?<!\d)\d{10,}(?!\d)")
_WHATSAPP_RE = re.compile(r"(?:whatsapp|واتس\s*اب|واتساب)[^\d]*(\+?\d[\d\s\-]{7,})", re.I)
_ALL_CAPS_RE = re.compile(r"\b[A-Z]{5,}\b")
_PROMO_RE = re.compile(
    r"\b(check\s+(?:my|out\s+my)|visit\s+my\s+channel|sub(?:scribe)?\s+(?:to\s+)?my|"
    r"link\s+in\s+(?:bio|description)|زور\s+قناتي|تابع\s+قناتي|اشترك\s+في\s+قناتي)\b",
    re.I,
)

SPAM_EN_STRONG = {
    "buy now",
    "click here",
    "earn money online",
    "dm me for",
    "check my channel",
    "visit my channel",
    "link in bio",
    "link in description",
    "make money",
    "earn $",
    "100% free",
    "limited offer",
    "act now",
    "whatsapp me",
    "join telegram",
    "forex signals",
    "crypto signals",
    "binary options",
    "investment opportunity",
    "giveaway winner",
    "you have been selected",
    "congratulations you won",
}

SPAM_EN_WEAK = {
    "subscribe",
    "follow me",
    "giveaway",
    "free",
    "crypto",
    "bitcoin",
    "forex",
    "telegram",
    "promotion",
    "invest",
}

SPAM_AR_STRONG = {
    "اكسب المال",
    "ربح المال",
    "زور قناتي",
    "تابع قناتي",
    "اشترك في قناتي",
    "رابط في البايو",
    "رابط في الوصف",
    "استثمار مضمون",
    "ربح مضمون",
    "فرصة استثمار",
    "رابح 100%",
    "فرصة ذهبية",
    "تواصل معي واتساب",
}

SPAM_AR_WEAK = {
    "اشترك",
    "تابعني",
    "جائزة",
    "واتساب",
    "تيليجرام",
    "تداول",
    "استثمار",
    "كريبتو",
}


def detect_spam(text: str) -> tuple[bool, str]:
    raw = str(text).strip()
    if not raw:
        return False, ""

    t_lower = raw.lower()
    word_count = len(t_lower.split())

    links = _LINK_RE.findall(t_lower)
    if len(links) >= 2:
        return True, "Multiple links"
    if len(links) == 1 and word_count <= 6:
        return True, "Suspicious link"

    if _WHATSAPP_RE.search(raw):
        return True, "WhatsApp number"
    if _PHONE_RE.search(t_lower):
        return True, "Phone number"

    if _PROMO_RE.search(t_lower):
        return True, "Promotional comment"

    for phrase in SPAM_EN_STRONG:
        if phrase in t_lower:
            return True, "Spam keywords"
    for phrase in SPAM_AR_STRONG:
        if phrase in t_lower:
            return True, "Spam keywords"

    weak_hits = 0
    for word in SPAM_EN_WEAK:
        if re.search(rf"\b{re.escape(word)}\b", t_lower):
            weak_hits += 1
    for word in SPAM_AR_WEAK:
        if word in t_lower:
            weak_hits += 1
    if weak_hits >= 3:
        return True, "Multiple spam keywords"

    emoji_count = len(re.findall(r"[\U0001F300-\U0001FAFF]", raw))
    if emoji_count >= 12:
        return True, "Excessive emojis"

    if re.search(r"(?!ه{3,}|ha{3,}|هه{3,})(.)\1{12,}", t_lower):
        return True, "Excessive repeated characters"

    words = t_lower.split()
    if len(words) >= 15:
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.30:
            return True, "Repeated content"

    caps_words = _ALL_CAPS_RE.findall(raw)
    if len(caps_words) >= 4 and word_count <= 12:
        return True, "Excessive caps"

    return False, ""
