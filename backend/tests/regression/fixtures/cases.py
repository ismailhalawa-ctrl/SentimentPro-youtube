from dataclasses import dataclass


@dataclass(frozen=True)
class RegressionCase:
    text: str
    expected: str
    category: str


def _cases(category: str, expected: str, texts: list[str]) -> list[RegressionCase]:
    return [RegressionCase(text=t, expected=expected, category=category) for t in texts]


DIALECT_GULF = (
    _cases(
        "dialect_gulf",
        "positive",
        [
            "والله خوش فيديو، استمر",
            "يبيلك عافية عالشرح الزين",
            "وايد حلو الفيديو ماشاء الله",
            "طقطقة حلوة والله يا شباب",
            "زين هواي محتواك يا اخوي كمل",
        ],
    )
    + _cases(
        "dialect_gulf",
        "negative",
        [
            "الفيديو مب زين اليوم للأسف",
            "الشرح تعبان ما فهمت شي",
            "ليش ما ترد على تعليقاتنا ابد",
            "ما عجبني الفيديو اليوم بصراحة",
        ],
    )
    + _cases(
        "dialect_gulf",
        "neutral",
        [
            "متى بترفعون الحلقة الجايه",
        ],
    )
)

DIALECT_LEVANT = (
    _cases(
        "dialect_levant",
        "positive",
        [
            "منيح كتير هالفيديو تسلم ايدك",
            "يا معلم شو هالشرح الحلو",
            "روعة الفيديو الله يعطيك العافية",
            "تمام كتير يعطيك الصحة",
            "معلم يا معلم دايما مبدع",
        ],
    )
    + _cases(
        "dialect_levant",
        "negative",
        [
            "مش عاجبني هالمحتوى اليوم",
            "لسا ما نزلت الحلقة ليش تأخرتوا",
            "ما حبيت هالفيديو صراحة",
            "زعلانة من جودة الصوت اليوم",
        ],
    )
    + _cases(
        "dialect_levant",
        "neutral",
        [
            "كيفك عم تحضر هيك فيديوهات؟",
        ],
    )
)

DIALECT_EGYPTIAN = (
    _cases(
        "dialect_egyptian",
        "positive",
        [
            "جامد اوي يا كبير الفيديو ده",
            "تحفه اوي والله يا نجم",
            "حلو قوي الشرح ده ربنا يخليك",
            "يا فنان يا كبير عاش يا وحش",
            "بجد رائع تسلم ايدك يا كبير",
        ],
    )
    + _cases(
        "dialect_egyptian",
        "negative",
        [
            "مش حلو الفيديو بجد النهارده",
            "ملل فظيع مكملتش الفيديو",
            "الجودة وحشة النهارده للاسف",
        ],
    )
    + _cases(
        "dialect_egyptian",
        "neutral",
        [
            "فين الحلقة الجايه يا باشا",
            "ازاي بتعمل المونتاج ده",
        ],
    )
)

DIALECT_IRAQI = (
    _cases(
        "dialect_iraqi",
        "positive",
        [
            "روعه هواي هذا الفيديو والله",
            "زين هواي شرحك عاشت ايدك",
            "هواي حلو المحتوى استمر",
            "عاشت ايدك على الجهد الطيب",
            "چا زين الشرح ماشاء الله عليك",
        ],
    )
    + _cases(
        "dialect_iraqi",
        "negative",
        [
            "جا زين الفيديو بس الصوت خربان",
            "ماكو فايدة الفيديو مب مفيد",
            "جان اتوقع احسن من هذا",
        ],
    )
    + _cases(
        "dialect_iraqi",
        "neutral",
        [
            "جان انتظر الحلقة اليديدة",
            "شنو راح تسوي بالحلقة الجاية",
        ],
    )
)

DIALECT_MAGHREBI = (
    _cases(
        "dialect_maghrebi",
        "positive",
        [
            "زوين هاد الفيديو بزاف",
            "مليح بزاف الشرح ديالك",
            "واعر هاد المحتوى يا نجم",
            "نيشان الشرح واضح بزاف",
            "زوينة الفكرة بزاف الله يعاونك",
        ],
    )
    + _cases(
        "dialect_maghrebi",
        "negative",
        [
            "ماعجبنيش هاد الفيديو اليوم",
            "الصوت خايب اليوم للاسف",
            "ملل بزاف ماكملتش الفيديو",
        ],
    )
    + _cases(
        "dialect_maghrebi",
        "neutral",
        [
            "فين الجزء الثاني ديال الفيديو",
            "بغيت نعرف كيفاش داير هادشي",
        ],
    )
)

EMOTIONAL = (
    _cases(
        "emotional",
        "positive",
        [
            "بكيت من القصة اللي حكيتها، الله يعطيك العافية على المحتوى",
            "الفيديو هذا أثر فيني كتير، شكرا الك",
            "ضحكت كتير من هالمقطع 😂😂",
            "انفعلت وانا اشوف الفيديو، تسلم ايدك",
            "متحمس جدا للحلقة الجاية",
            "زعلت من نهاية الفيديو المفاجئة بس بصراحة شغل حلو",
            "قلبي انكسر من القصة، الله يوفقك ع الطرح",
            "صراحة تأثرت كتير، افضل فيديو شفته",
            "فرحان جدا بهالانجاز، مبروك",
            "this video made me cry, thank you for sharing your story",
            "I felt so proud watching this, amazing work",
        ],
    )
    + _cases(
        "emotional",
        "negative",
        [
            "حزين لأن القناة صارت أقل نشاط",
            "I was so bored the whole video, nothing new",
        ],
    )
    + _cases(
        "emotional",
        "neutral",
        [
            "خايف اكمل الفيديو بس فضولي كتير",
            "قلقانة عليك من الموضوع، ان شاء الله بخير",
        ],
    )
)

CRITICISM = _cases(
    "criticism",
    "negative",
    [
        "الفيديو سيء جدا ما استفدت شي",
        "محتوى ضعيف مقارنة بالسابق",
        "تفسير خاطئ تماما للموضوع",
        "مضيعة وقت هذا الفيديو",
        "فاشل الشرح مافهمت شي",
        "نسخ من قناة ثانية بدون ذكر المصدر",
        "تقليد رخيص لقنوات ثانية",
        "جودة التصوير سيئة جدا هالمرة",
        "مونتاج ضعيف وسريع جدا",
        "الاعلانات كثيرة جدا خربت الفيديو",
        "this content feels rushed and poorly edited",
        "the explanation was completely wrong",
        "worst video on this channel so far",
        "too many ads ruined the experience",
        "this is just a copy of another channel's video",
    ],
)

SUGGESTION = _cases(
    "suggestion",
    "neutral",
    [
        "ياريت تحسن جودة الصوت بالحلقات الجايه",
        "اقترح تسوي فيديو عن هالموضوع بالتفصيل",
        "ممكن تضيفوا ترجمة عربي للفيديوهات الجايه",
        "لو تختصر المقدمة راح يكون أفضل",
        "افضل لو تسوي جزء ثاني يشرح اكثر",
        "حبذا لو ترفعون الحلقات بجودة اعلى",
        "would be great if you added subtitles",
        "maybe try a shorter intro next time",
        "suggestion: cover this topic in more depth",
        "please improve the audio quality next time",
    ],
) + _cases(
    "suggestion",
    "positive",
    [
        "ياريت تكمل السلسلة، شغل حلو لين الحين",
        "great video, maybe add timestamps next time",
    ],
)

ADMIRATION = _cases(
    "admiration",
    "positive",
    [
        "انت اسطورة حقيقية ما فيه احد مثلك",
        "الافضل بلا منازع، فخورين فيك",
        "قدوة لينا كلنا، الله يوفقك",
        "ملك المحتوى بدون منازع",
        "دايم مبدع ما تخيب املنا فيك",
        "بطل حقيقي، شغلك محترم جدا",
        "قمة الابداع في كل فيديو",
        "لا يوجد مثلك في هذا المجال",
        "you're a true legend, best creator ever",
        "nobody does it like you, absolute genius",
        "you are such an inspiration to all of us",
        "hands down the best channel out there",
    ],
)

RAMADAN = (
    _cases(
        "ramadan",
        "positive",
        [
            "رمضان كريم عليك وعلى القناة كلها",
            "محتوى رمضاني حلو، تقبل الله طاعتكم",
            "كل عام وانتم بخير، رمضان مبارك",
            "جهدكم بشهر رمضان يستاهل كل الشكر",
            "رمضان كريم، بانتظار حلقاتكم كل يوم",
        ],
    )
    + _cases(
        "ramadan",
        "negative",
        [
            "فيديوهات رمضان هالسنة اقل من المعتاد للاسف",
            "تقصير واضح بمحتوى رمضان هالسنة",
        ],
    )
    + _cases(
        "ramadan",
        "neutral",
        [
            "ياريت تسوون سلسلة رمضانية زي السنة اللي فاتت",
        ],
    )
)

RELIGIOUS = _cases(
    "religious",
    "positive",
    [
        "ماشاء الله عليك محتوى راقي ومفيد",
        "بارك الله فيك على هالمجهود الرائع",
        "جزاك الله خيرا على المعلومة القيمة",
        "الله يبارك فيك ويوفقك دائما",
        "تبارك الله عليك شرح ما شاء الله",
        "الله يعطيك العافية على تعبك معنا",
        "ربي يوفقك في مشروعك يا رب",
        "may Allah bless you for this beneficial content",
        "thank you and may God reward you for this",
        "الحمدلله استفدت كثير من هالفيديو",
    ],
)

FAN = _cases(
    "fan",
    "positive",
    [
        "جيت بدري هالمره، فخور اكون هنا",
        "قناتي المفضلة بلا منازع",
        "من زمان مانزلتوا، اشتقنا للمحتوى",
        "عضو دائم بمجتمعكم وفخور بذلك",
        "been a subscriber since day one, love this channel",
        "first video of yours I watched and I'm hooked",
        "still here supporting from the start",
    ],
) + _cases(
    "fan",
    "neutral",
    [
        "اول تعليق ومتابع من زمان",
        "متابعك من اول فيديو نزلته",
        "who else is watching this in 2026",
    ],
)

FOOTBALL = (
    _cases(
        "football",
        "positive",
        [
            "التحليل التكتيكي كان ممتاز هالمرة",
            "افضل تحليل كرة قدم اشوفه بصراحة",
            "خسر فريقي بس شرحك للمباراة كان رائع",
            "توقعاتك للمباراة كانت غلط بس التحليل حلو",
            "great tactical breakdown of the match",
            "love how you break down every play, best football channel",
        ],
    )
    + _cases(
        "football",
        "negative",
        [
            "تحليلك للمباراة ضعيف اليوم بصراحة",
            "ملخص المباراة كان سريع جدا ونقص تفاصيل",
            "your match predictions have been wrong lately",
        ],
    )
    + _cases(
        "football",
        "neutral",
        [
            "متى بترفع تحليل المباراة الجاية",
        ],
    )
)

SARCASM = _cases(
    "sarcasm",
    "negative",
    [
        "واو عبقري، ما شفت شرح افضل من كذا 🙄",
        "طبعا اكيد، افضل فيديو بالتاريخ 😏",
        "يا سلام عليك يا معلم، تحفة فنية 🙄👏",
        "ما شاء الله عليك ياخي، شرح خرافي بس بالعكس تماما",
        "جامد أوي كده، هو انت جامد 🙄",
        "wow genius, never seen such amazing content 🙄",
        "sure bro, best explanation ever 😏",
        "amazing quality, truly perfect as always 🙄",
        "great job, exactly what I expected... not",
        "يا للعظمة، ما توقعت اسوأ من كذا",
        "هههههههههه شرح تحفة فنية والله",
        "hahahahaha sure, perfect as always",
    ],
)

MIXED_LANGUAGE = _cases(
    "mixed_language",
    "positive",
    [
        "3ajabny el fikra bshaklaha kter",
        "this فيديو كان رائع جدا thanks",
        "رهيب awesome content keep going",
        "tislam eedak 3al shar7",
        "ana m3jab bel content bshakl kbeer",
        "thank you كتير على المعلومة",
        "hala fik, wa7ashtna videos",
    ],
) + _cases(
    "mixed_language",
    "negative",
    [
        "el video kan 7ilw bs el sot mesh clear",
        "mesh 3ajbني الفيديو اليوم",
        "kalam fadi mafi fayde",
        "مش clear الصوت 5alas",
        "no offense بس الفيديو ملل",
    ],
)

ENGLISH = (
    _cases(
        "english",
        "positive",
        [
            "this is genuinely one of the best explanations I've seen",
            "this helped me understand the concept so much better, thank you",
            "I've watched this three times already, so good",
            "interesting perspective, never thought about it that way",
            "just here to say thanks for the free knowledge",
            "solid breakdown, appreciate the effort",
            "waiting for part two, this was great",
        ],
    )
    + _cases(
        "english",
        "negative",
        [
            "I don't think this covered the topic well enough",
            "the pacing was way too slow for my taste",
            "not your best work honestly",
            "this is factually incorrect in several places",
            "audio kept cutting out throughout the video",
        ],
    )
    + _cases(
        "english",
        "neutral",
        [
            "what software are you using for editing?",
            "can you make a follow-up video on this?",
            "could you clarify the third point? a bit confusing",
        ],
    )
)

PERSONAL_LIFE_DISCLOSURE = _cases(
    "personal_life_disclosure",
    "neutral",
    [
        "اهلي انفصلوا الاسبوع اللي طاف، صعب علي الوضع",
        "امي مريضة هالفترة وانا تعبان نفسيا",
        "فقدت شغلي الاسبوع اللي طاف، ظروف صعبة",
        "صاحبي توفي قبل اسبوع، الله يرحمه",
        "عم مر بفترة صعبة بحياتي الشخصية",
        "تخرجت هالاسبوع، فرحان بس متعب من الدراسة",
        "انفصلت عن خطيبي قبل شهر، صعب اتجاوز الموضوع",
        "ابوي دخل المستشفى امبارح، قلقانين عليه",
        "my parents got divorced last month, it's been rough",
        "I lost my job recently, tough times",
        "my dog passed away yesterday, still processing it",
        "going through a hard breakup right now",
    ],
)

CONTRAST_MIXED_SENTIMENT = _cases(
    "contrast_mixed_sentiment",
    "neutral",
    [
        "الفيديو جميل لكن الصوت مو واضح",
        "احب المحتوى بس الموسيقى مزعجة",
        "اتفق معك بس ما احب اسلوب العرض",
        "I like the content but the editing feels rushed",
        "good explanation but way too long",
        "شرح ممتاز لكن طويل شوي",
        "great video but the audio needs work",
        "رائع بصراحة، بس ياريت تختصر شوي",
        "فنان بس ياليت الجودة تتحسن",
    ],
) + _cases(
    "contrast_mixed_sentiment",
    "negative",
    [
        "كويس لكن توقعت افضل من كذا",
        "الفكرة حلوة لكن التنفيذ ضعيف",
        "مش سيء لكن كنت اتوقع أحسن",
        "محتوى جيد لكن الاعلانات كثيرة جدا",
        "not bad but I expected more depth",
        "nice video but too many ads ruined it",
    ],
)

NEGATION = (
    _cases(
        "negation",
        "negative",
        [
            "مو حلو الفيديو خالص",
            "مش زي ما توقعت، مش كويس ابدا",
            "ما فيه شي حلو بهالفيديو للاسف",
            "مش عاجبني هالطريقة اللي بتشرح فيها المواضيع من فترة",
            "ما اعتقد ان الفيديو كان مفيد او حتى ممتع",
            "والله ما توقعت يكون بهالسوء",
            "ليش حد بيحب هالنوع من الشرح اصلا",
            "مين ممكن يحب هالفيديو غير المعجبين المتعصبين",
            "this isn't the best video you've made, not even close",
            "not gonna lie, this wasn't great",
        ],
    )
    + _cases(
        "negation",
        "neutral",
        [
            "is this seriously supposed to be good content?",
        ],
    )
    + _cases(
        "negation",
        "positive",
        [
            "ما صار ولا مرة ما استفدت من فيديوهاتك",
            "مش فاشل الفيديو، بالعكس كان حلو",
            "I wouldn't say this was a bad video at all",
            "can't say I didn't enjoy this one",
        ],
    )
)

FORMULAIC_GRIEF_RELIGIOUS = _cases(
    "formulaic_grief_religious",
    "neutral",
    [
        "الله يرحمه ويسكنه فسيح جناته",
        "البقاء لله وحده، عظم الله اجركم",
        "انا لله وانا اليه راجعون",
        "دعواتكم لي بالنجاح هالفترة",
        "يارب انجح بهالسنة، ادعولي",
        "اللهم ارحم موتانا وموتى المسلمين",
        "رحمه الله وغفر له",
        "ادعوا لي بالشفاء، الله يعافيكم",
        "please pray for my family, going through a hard time",
        "may he rest in peace, we will miss him",
    ],
)

QUESTION_DISCUSSION = _cases(
    "question_discussion",
    "neutral",
    [
        "ايش اسم البرنامج اللي تستخدمه بالمونتاج",
        "كم استغرق تصوير هالحلقة",
        "هل هذا ينطبق على كل الحالات ولا لأ",
        "وش الفرق بين الطريقتين اللي ذكرتهم",
        "انا لاحظت ان الموضوع معقد اكثر مما يبدو، شو رايكم",
        "بصراحة الموضوع فيه جدل كبير بين الناس",
        "what camera do you use for filming?",
        "how long did it take to research this topic?",
        "is this method applicable to other cases too?",
        "this is a pretty controversial topic honestly",
    ],
)

REQUEST = _cases(
    "request",
    "neutral",
    [
        "ممكن تسوي فيديو عن هالموضوع بالتفصيل",
        "لو سمحت زود مدة الحلقات شوي",
        "ابغى اعرف رايك بموضوع ثاني لو تكرمت",
        "ياريت تسوي جزء ثاني بأقرب وقت",
        "بانتظار الجزء الثاني بفارغ الصبر",
        "نزل الحلقة اليوم لو ممكن",
        "please make a part two soon",
        "could you cover this topic next episode?",
        "hoping for more content like this soon",
        "drop the next episode already please",
    ],
)

REPORTED_REGRESSION = [
    RegressionCase("الله عليك يا عبقري 👏☺️", "positive", "reported_regression"),
    RegressionCase("يا سلام ❤😂", "positive", "reported_regression"),
    RegressionCase("الف رحمه ع والديك", "neutral", "reported_regression"),
    RegressionCase(
        "اريد شرح كتاب you are about to make a terrible mistake", "neutral", "reported_regression"
    ),
    RegressionCase("الله يسعدك", "positive", "reported_regression"),
    RegressionCase("شكرا لك", "positive", "reported_regression"),
    RegressionCase("بارك الله فيك", "positive", "reported_regression"),
    RegressionCase("فيديو جميل", "positive", "reported_regression"),
    RegressionCase("ممتاز جدا", "positive", "reported_regression"),
    RegressionCase("أحسنت", "positive", "reported_regression"),
]

SARCASM_FALSE_POSITIVE_GUARD = _cases(
    "sarcasm_false_positive_guard",
    "positive",
    [
        "برافو عليك 👏",
        "تمام كتير 👌",
        "زين والله 👏",
        "الله يعطيك العافية 👏",
        "يا هلا فيك 👏",
        "amazing quality 👌",
        "perfect as always 👌",
        "عبقري فعلا هالشرح 👏",
        "يا سلام عليك 👌",
        "برافو عليك يا بطل 👏",
        "احسنت والله 👏",
        "تسلم ايدك يا عبقري",
        "الله يبارك فيك يا معلم 👏",
        "great job explaining this 👌",
        "طبعا رائع كالعادة",
        "أكيد من افضل الفيديوهات",
    ],
)

POSITIVE_GENERAL = _cases(
    "positive_general",
    "positive",
    [
        "شكرا جزيلا على المعلومة",
        "استفدت كثيرا من هذا الفيديو",
        "محتوى راقي ومفيد جدا",
        "متابع دائم ولن اتوقف",
        "هذا افضل شرح شاهدته",
        "الله يوفقك دائما",
        "استمر بهذا العطاء",
        "قناة تستحق كل الدعم",
        "شرح واضح ومباشر شكرا",
        "تعلمت منك الكثير",
        "فيديو مفيد جدا شكرا لك",
        "هذا بالضبط ما كنت ابحث عنه",
        "احب اسلوبك في الشرح",
        "من افضل القنوات التعليمية",
        "جزاك الله كل خير على المجهود",
        "this is exactly what I needed, thank you",
        "great explanation, very clear",
        "you made this so much easier to understand",
        "loved every second of this video",
        "this channel deserves way more subscribers",
        "i learned so much from this, thanks",
        "your content keeps getting better",
        "well explained, appreciate the effort",
        "this is gold, thank you so much",
        "you always deliver quality content",
        "هذا الفيديو غير حياتي للأفضل",
        "كل فيديو تنزله افضل من اللي قبله",
        "لن اجد شرح احسن من كذا",
        "قيمة حقيقية تقدمها لنا شكرا",
        "بصراحة محتوى يستاهل المشاهدة",
    ],
)

NEUTRAL_GENERAL = _cases(
    "neutral_general",
    "neutral",
    [
        "الفيديو مدته عشر دقائق",
        "نزل الفيديو الساعة السادسة مساء",
        "هذا الموضوع تم تناوله من قبل",
        "شاهدت الفيديو على الهاتف",
        "الفيديو متوفر بجودة عالية",
        "the video is about ten minutes long",
        "this was uploaded last week",
        "watching this on my phone",
        "the topic has been covered before",
        "this video has english subtitles",
        "found this through a recommendation",
        "sharing this with a friend",
        "not sure if this applies to everyone",
        "will need to watch this again later",
        "this is part of a longer series",
        "شاهدت الجزء الاول قبل هذا",
        "الموضوع معقد وله جوانب متعددة",
        "هذا شرح لمرحلة معينة فقط",
        "الفيديو يحتاج وقت لفهمه بالكامل",
        "لسا ما خلصت مشاهدة الفيديو كامل",
        "this is the third video in the series",
        "i bookmarked this for later",
        "there are different opinions on this topic",
        "the comments section has more context",
        "this was recorded a while ago it seems",
    ],
)

NEGATIVE_GENERAL = _cases(
    "negative_general",
    "negative",
    [
        "لم افهم شيئا من هذا الشرح",
        "معلومات مغلوطة بشكل واضح",
        "اضعت وقتي بمشاهدة هذا",
        "الشرح مشوش وغير منظم",
        "توقعت محتوى افضل من هذا بكثير",
        "لن اتابع هذه القناة بعد اليوم",
        "جودة الفيديو سيئة جدا هذه المرة",
        "الصوت غير مسموع في اغلب الفيديو",
        "هذا اسوأ شرح شاهدته لهذا الموضوع",
        "المعلومات قديمة وغير محدثة",
        "this explanation made things more confusing",
        "i regret watching this video",
        "the information here is outdated",
        "this was a complete waste of my time",
        "worst tutorial i've seen on this topic",
        "the audio quality ruined this video",
        "i expected so much more from this channel",
        "this content adds nothing new",
        "unsubscribing after this video",
        "the explanation was all over the place",
        "هذا التوضيح غير كافي على الاطلاق",
        "لا يوجد اي جهد واضح في هذا الفيديو",
        "خيبة امل كبيرة هذه الحلقة",
        "المحتوى مكرر من فيديوهات سابقة",
        "لا انصح احد بمشاهدة هذا الفيديو",
        "الشرح سطحي ولا يغطي الموضوع",
        "هذا ليس المستوى المعتاد لقناتك",
        "تراجع واضح في جودة المحتوى",
        "معلومات ناقصة وغير دقيقة",
        "لم يستحق وقت المشاهدة بصراحة",
    ],
)

EMOJI_HEAVY = (
    _cases(
        "emoji_heavy",
        "positive",
        [
            "🔥🔥🔥🔥🔥",
            "😍😍😍😍",
            "❤️❤️❤️ رهيب",
            "👏👏👏👏 برافو",
            "🥳🎉🎉🎉",
            "💯💯💯",
            "🙌🙌🙌 يعطيك العافية",
            "😍🔥❤️",
            "👍👍",
            "🙏🙏🙏 شكرا",
            "✨✨✨ رائع",
            "😭😭😭 اشتقنالك",
        ],
    )
    + _cases(
        "emoji_heavy",
        "negative",
        [
            "👎👎👎",
            "🤮🤮🤮",
            "😡😡😡",
            "💀💀💀 سيء",
            "🗑️🗑️🗑️",
            "❌❌❌ مش عاجبني",
            "💔💔 للاسف",
            "😢😢 خيبة امل",
            "😍 بس 😡 الصوت سيء",
            "🔥 لكن للاسف السرعة ملل",
        ],
    )
    + _cases(
        "emoji_heavy",
        "neutral",
        [
            "🤔🤔",
            "👀👀👀",
        ],
    )
)

GREETING = _cases(
    "greeting",
    "neutral",
    [
        "السلام عليكم",
        "مرحبا بالجميع",
        "هلا والله",
        "صباح الخير للجميع",
        "مساء الخير",
        "hello everyone",
        "hi from Egypt",
        "good morning all",
        "hey there, new subscriber here",
        "greetings from Morocco",
        "اهلا وسهلا",
        "hello, first time watching",
        "hi, just found this channel",
        "good evening everyone",
        "السلام عليكم ورحمة الله",
    ],
)

PRAISE_EXTRA = _cases(
    "praise_extra",
    "positive",
    [
        "لا يوجد افضل منك في هذا المجال",
        "شرحك دايما فوق الوصف",
        "من متابعينك القدامى وفخور بذلك",
        "قناتك مرجع اساسي لي",
        "استاذ حقيقي في مجاله",
        "لغة الشرح عندك واضحة جدا",
        "طريقة عرضك للمعلومة مبدعة",
        "دايما تتفوق على نفسك",
        "you set the bar so high",
        "your teaching style is unmatched",
        "this is masterclass level content",
        "you explain things better than my professors",
        "the production quality here is top tier",
        "your dedication to quality shows",
        "you never disappoint with your uploads",
        "قيمة المحتوى تفوق التوقعات دائما",
        "لا استغني عن قناتك ابدا",
        "الاسلوب راقي والمحتوى اروع",
        "your videos are a masterclass",
        "one of the few channels worth the notification bell",
    ],
)

RELIGIOUS_EXTRA = _cases(
    "religious_extra",
    "positive",
    [
        "الله يجزاك خير الجزاء",
        "ربي يحفظك ويوفقك دائما",
        "تقبل الله منك هذا العمل",
        "الله يكتب اجرك على هذا المجهود",
        "دعواتي لك بالتوفيق في مشاريعك القادمة",
        "بارك الله في وقتك ومجهودك",
        "الله يعينك على تقديم المزيد",
        "ما شاء الله تبارك الله شرح رائع",
        "الله يديم عليك الصحة والعافية",
        "جزاكم الله خيرا على هذا الطرح القيم",
        "may Allah reward you for this effort",
        "God bless this channel and its content",
        "thank you and may God increase your knowledge",
        "الله يوفقك في الدارين",
        "ربنا يبارك في جهدك ووقتك",
    ],
)

QUESTION_EXTRA = _cases(
    "question_extra",
    "neutral",
    [
        "هل يوجد جزء ثاني لهذا الموضوع",
        "متى تفكر تسوي فيديو عن هذا",
        "وش رايك لو تجرب موضوع مشابه",
        "كيف اقدر اطبق هذي الفكرة عمليا",
        "ليش اخترت هذا الموضوع بالتحديد",
        "هل هذا ينطبق على كل اللغات",
        "ايش المصادر اللي اعتمدت عليها",
        "متى موعد الحلقة الجاية بالضبط",
        "what tools did you use for this?",
        "how do you prepare for each video?",
        "is there a written guide for this too?",
        "why did this take so long to upload?",
        "what's your workflow like?",
        "when is the next part coming out?",
        "could you list your sources?",
    ],
)

REQUEST_EXTRA = _cases(
    "request_extra",
    "neutral",
    [
        "ممكن تسوي سلسلة كاملة عن هذا الموضوع",
        "لو تكرمت زود امثلة اكثر بالفيديو الجاي",
        "ياليت تشرح هذي النقطة بشكل مفصل اكثر",
        "ابغى فيديو يغطي الجزء المتقدم من الموضوع",
        "ممكن ترفع جودة الصوت بالتسجيلات الجايه",
        "لو سمحت ضيف فهرسة للفيديو",
        "ياريت تسوي مقارنة بين الطريقتين",
        "ابي اعرف رايك بموضوع ثاني متعلق بهذا",
        "could you slow down a bit in the next video?",
        "please add chapters to make navigation easier",
        "would you consider doing a live session?",
        "can you link the tools you mentioned?",
        "please cover the beginner basics first",
        "hoping you make a series out of this",
        "could you compare this with the other method?",
    ],
)

DIALECTAL_EXTRA = _cases(
    "dialectal_extra",
    "positive",
    [
        "خوش شغل والله يعطيك العافية",
        "ما قصرت والله يا طويل العمر",
        "هالمحتوى يستاهل المتابعة",
        "تسلم يمينك على الطرح",
        "زين سويت لين الحين",
        "ما بين شك انو محتواك حلو كتير",
        "يا ريت كل القنوات متلك",
        "كتير استفدت منك يعطيك العافية",
        "معلم بجد ما بضاهيك حدا",
        "تبارك الله عليك محتوى مميز",
        "ربنا يخليك لينا يا كبير",
        "بجد مفيش زيك في الشرح",
        "الشغل ده تحفة من غير مبالغة",
        "ده افضل شرح شوفته بجد",
        "ماشاء الله عليك مجهود جبار",
        "الله يخليك الينا هواي زين",
        "ماكو احسن منك بيه",
        "شغلك دايما بمستوى عالي",
        "عاشت ايدك على هذا الجهد",
        "الله يوفقك دنيا وآخرة",
        "الله يحفظك ليا بزاف",
        "ماكاينش حتى واحد بحالك",
        "الخدمة ديالك نظيفة بزاف",
        "بارك الله فيك على هاد المجهود",
        "الله يعاونك ديما",
    ],
)

MIXED_SENTIMENT_EXTRA = _cases(
    "mixed_sentiment_extra",
    "neutral",
    [
        "المحتوى قيم لكن طريقة العرض تحتاج تحسين",
        "استفدت من المعلومة بس التنظيم مو مرتب",
        "شرح جيد لكن ينقصه امثلة عملية",
        "great topic choice but the delivery needs work",
        "solid research but the video is too long",
        "nice effort but missed the key details",
        "الموضوع مهم بس الشرح ملخبط شوي",
        "فكرة ممتازة بس التطبيق يحتاج شغل اكثر",
        "genuinely informative but way too repetitive",
        "appreciate the effort but the pacing is off",
        "good breakdown but the audio was distracting",
    ],
) + _cases(
    "mixed_sentiment_extra",
    "negative",
    [
        "فكرة الفيديو حلوة بس التنفيذ بطيء",
        "good points but poorly organized",
        "معلومة صح بس طريقة الايصال ضعيفة",
        "بداية قوية لكن النهاية كانت خيبة امل",
    ],
)

NEGATION_EXTRA = _cases(
    "negation_extra",
    "positive",
    [
        "مو صحيح انو المحتوى كذا سيء",
        "ما اقول ان الفيديو كان ممل",
        "ما هو صحيح ان الشرح كان ممل",
        "لا اعتقد ان المحتوى كان ضعيف",
        "ما في شي سيء بهالفيديو",
        "not saying this was a bad video",
        "I don't think this was terrible",
        "this wasn't a waste of time at all",
        "can't say this was boring",
    ],
) + _cases(
    "negation_extra",
    "negative",
    [
        "مو حلو تسوون كذا بالفيديوهات الجايه",
    ],
)

DISAGREEMENT = _cases(
    "disagreement",
    "neutral",
    [
        "بصراحة ما اتفق معك بهالنقطة بس المحتوى بشكل عام حلو",
        "اختلف معك بخصوص الطريقة اللي اشرحت فيها",
        "اخالفك الرأي بس احترم وجهة نظرك",
        "مع احترامي بخالفك في هذي النقطة",
        "ما اتفق مع كلامك عن الموضوع",
        "i disagree with your take on this",
        "i don't think that's right, but i respect the effort",
        "respectfully disagree with the conclusion here",
        "i don't agree with the second point you made",
        "not sure i agree, but interesting perspective",
    ],
)

REAL_WORLD_RELATIONSHIP_CHANNEL = (
    _cases(
        "real_world_relationship_channel",
        "neutral",
        [
            "انا منفصله وعلاقتي كانت فاشلة لكن انصح المتزوجين نصايح افضل من ناس يلي عاشت علاقات "
            "زوجية دائما الا مايكون طرف مأذنب",
            "كلني افشل بكل شيء.",
            "علاقة امي وابوي سيئة ولا اعتبرها حب واستحالة انظر لهم بهذي النظرة ارتباطهم للمجتمع ليس لهم",
            "انت وقاعد تشرح هل مثال تبع أمها وأبو أنا اجيت لا اخود مثالك على ارض الواقع بس كانو "
            "اهلي منفصلين من سنوات للأسف وكتير بشعة كانت طفولتي",
            "لو سمحت ممكن شرح كتاب خرافه العادي",
            "يعني الزواج التقليدي نهايته حب حقيقي",
            "مو قد نزلت عن هذا الكتاب؟ ليه رجعت نزلت عنه",
        ],
    )
    + _cases(
        "real_world_relationship_channel",
        "positive",
        [
            "ألف شكر لك وتحية لجهودك .. أختلف معك في نقطة واحدة .. ليس كل من فشل في علاقته .. "
            "غير مؤهل لإعطاء نصيحة .. وليس كل فاشل في علاقة لا يتمنى الخير لمن ينصحهم .. "
            "الحب رزق من الله يهبه لمن يشاء",
            "ياخي والله إن كلامك عجيب برافو عليك 👏🏻",
            "يا سلام ياناصر على التنزيل المستمر",
            "حلقه في وقتها جدا مفيده وكنت متحمسه لها مره وما توقعتك تسويها لكن كفو شفت الناس "
            "ترشح لك في التعليقات ذا الكتاب ❤❤",
        ],
    )
    + _cases(
        "real_world_relationship_channel",
        "negative",
        [
            "٢٤ دقيقه عبث تعيد نفس الموال",
            "الموسيقى مزعجة جداااااا",
            "للابد الموسيقى تخرب فيديوهاتك😭😭😭",
            "شوف رجاء صوتك مش جميل، وانا متأكد انك عارف ان صوتك مش جميل، لذلك لا تغني مرة اخرى رجاء",
            "كلام الكتاب كان ينبلع شوي بس اول ما انت تكلمت كلامك صار مو واقعي ابدًا وعن سالفه "
            "الهدايا لا تحرض عالبخل ترتيبك غلط بغلط خلي فمك لمعيش",
            "ناصر في مشكلة عالويب سايت ماقدرت سجل دخول 😢",
            "يناصر اتواصل مع الموظفين دوبمكافين ما يرد احد عليا اطلب قهوه محد رد عليا",
        ],
    )
)

ALL_CASES: list[RegressionCase] = (
    REAL_WORLD_RELATIONSHIP_CHANNEL
    + DIALECT_GULF
    + DIALECT_LEVANT
    + DIALECT_EGYPTIAN
    + DIALECT_IRAQI
    + DIALECT_MAGHREBI
    + EMOTIONAL
    + CRITICISM
    + SUGGESTION
    + ADMIRATION
    + RAMADAN
    + RELIGIOUS
    + FAN
    + FOOTBALL
    + SARCASM
    + MIXED_LANGUAGE
    + ENGLISH
    + PERSONAL_LIFE_DISCLOSURE
    + CONTRAST_MIXED_SENTIMENT
    + NEGATION
    + FORMULAIC_GRIEF_RELIGIOUS
    + QUESTION_DISCUSSION
    + REQUEST
    + REPORTED_REGRESSION
    + SARCASM_FALSE_POSITIVE_GUARD
    + POSITIVE_GENERAL
    + NEUTRAL_GENERAL
    + NEGATIVE_GENERAL
    + EMOJI_HEAVY
    + GREETING
    + PRAISE_EXTRA
    + RELIGIOUS_EXTRA
    + QUESTION_EXTRA
    + REQUEST_EXTRA
    + DIALECTAL_EXTRA
    + MIXED_SENTIMENT_EXTRA
    + NEGATION_EXTRA
    + DISAGREEMENT
)
