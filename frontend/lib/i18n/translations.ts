export type Locale = 'en' | 'ar';

export const translations = {
  en: {
    common: {
      loading: 'Loading…',
      loggingOut: 'Logging out…',
      logOut: 'Log out',
      settings: 'Settings',
      backToAnalysis: 'Back to Analysis',
      invalidYoutubeUrl: 'Enter a valid YouTube video URL (e.g. youtube.com/watch?v=...)',
    },
    nav: {
      dashboard: 'Dashboard',
      newAnalysis: 'New Analysis',
      audienceAssistant: 'Channel Assistant',
      history: 'History',
      reports: 'Reports',
      settings: 'Settings',
    },
    languageToggle: {
      label: 'Language',
      en: 'English',
      ar: 'Arabic',
    },
    dashboardShell: {
      loadingSession: 'Loading your session…',
    },
    audienceAssistant: {
      focusArea: {
        label: 'Focus Area',
        allVideos: 'All Analyzed Videos',
      },
      askAboutVideo: 'Ask the AI Assistant about this video',
    },
    newAnalysis: {
      title: 'New Analysis',
      subtitle: 'Paste a YouTube link to analyze its comments using real-time AI processing.',
      urlLabel: 'YouTube Video URL',
      urlLabelA: 'YouTube Video URL — A',
      urlLabelB: 'YouTube Video URL — B',
      configTitle: 'Analysis Configuration',
      analysisMode: {
        label: 'Analysis Mode',
        single: 'Single Video',
        compare: 'Compare Videos',
      },
      sentimentEngine: {
        label: 'Sentiment Engine',
        fast: 'Fast',
        fastDesc: 'Local AI models only — quickest, no API key needed.',
        hybrid: 'Hybrid',
        hybridDesc:
          'Local AI first, escalates uncertain or dialectal Arabic/sarcastic comments to a smarter AI. Recommended for Arabic dialect content.',
        smart: 'Smart',
        smartDesc: 'Every comment goes through a full AI model — most accurate, requires an AI provider API key.',
        processingNotice:
          'Note: This mode requires more processing time compared to Fast Mode, but it delivers highly precise, deep, and sophisticated analytical insights.',
      },
      maxComments: {
        label: 'Maximum Comments',
        all: 'All',
      },
      sorting: {
        label: 'Comment Sorting (YouTube API)',
        relevance: 'Top Relevant',
        time: 'Newest First',
      },
      includeReplies: 'Include comment replies inside threads',
      languagePref: {
        label: 'Language Preference',
        auto: 'Auto Detect',
        ar: 'Arabic',
        en: 'English',
      },
      nlpFeatures: {
        title: 'NLP Pipeline Features',
        keywordExtraction: 'Enable Keyword Extraction',
        generateReport: 'Enable Report Generation',
      },
      startButton: {
        start: 'Start Analysis',
        analyzing: 'Analyzing…',
      },
      videoA: 'Video A',
      videoB: 'Video B',
      videoFallback: 'Video',
      progressLabel: 'Analysis Progress',
      errorPrefix: 'Error:',
      complete: {
        banner: 'Analysis Complete! {title} — {count} comments processed.',
        viewHistory: 'View in History',
      },
    },
  },
  ar: {
    common: {
      loading: 'جارٍ التحميل…',
      loggingOut: 'جارٍ تسجيل الخروج…',
      logOut: 'تسجيل الخروج',
      settings: 'الإعدادات',
      backToAnalysis: 'العودة إلى التحليل',
      invalidYoutubeUrl: 'أدخل رابط فيديو يوتيوب صالحًا (مثال: youtube.com/watch?v=...)',
    },
    nav: {
      dashboard: 'لوحة التحكم',
      newAnalysis: 'تحليل جديد',
      audienceAssistant: 'مساعد القناة',
      history: 'السجل',
      reports: 'التقارير',
      settings: 'الإعدادات',
    },
    languageToggle: {
      label: 'اللغة',
      en: 'الإنجليزية',
      ar: 'العربية',
    },
    dashboardShell: {
      loadingSession: 'جارٍ تحميل جلستك…',
    },
    audienceAssistant: {
      focusArea: {
        label: 'مجال التركيز',
        allVideos: 'كل الفيديوهات المحللة',
      },
      askAboutVideo: 'اسأل المساعد الذكي عن هذا الفيديو',
    },
    newAnalysis: {
      title: 'تحليل جديد',
      subtitle: 'الصق رابط فيديو يوتيوب لتحليل تعليقاته باستخدام الذكاء الاصطناعي في الوقت الفعلي.',
      urlLabel: 'رابط فيديو يوتيوب',
      urlLabelA: 'رابط فيديو يوتيوب — أ',
      urlLabelB: 'رابط فيديو يوتيوب — ب',
      configTitle: 'إعدادات التحليل',
      analysisMode: {
        label: 'وضع التحليل',
        single: 'فيديو واحد',
        compare: 'مقارنة فيديوهات',
      },
      sentimentEngine: {
        label: 'محرك تحليل المشاعر',
        fast: 'سريع',
        fastDesc: 'نماذج ذكاء اصطناعي محلية فقط — الأسرع، لا يتطلب مفتاح API.',
        hybrid: 'مختلط',
        hybridDesc:
          'يبدأ بالنماذج المحلية ثم يحوّل التعليقات غير الواضحة أو اللهجات العربية أو التعليقات الساخرة إلى ذكاء اصطناعي أقوى. موصى به للمحتوى باللهجات العربية.',
        smart: 'ذكي',
        smartDesc: 'كل تعليق يمر عبر نموذج ذكاء اصطناعي كامل — الأكثر دقة، يتطلب مفتاح API لمزوّد ذكاء اصطناعي.',
        processingNotice:
          'يرجى العلم أن هذا الطور يحتاج إلى وقت أطول في المعالجة مقارنة بالطور السريع (Fast Mode)، ولكنه يوفر لك نتائج تفصيلية فائقة الدقة والعمق.',
      },
      maxComments: {
        label: 'الحد الأقصى للتعليقات',
        all: 'الكل',
      },
      sorting: {
        label: 'ترتيب التعليقات (YouTube API)',
        relevance: 'الأكثر صلة',
        time: 'الأحدث أولاً',
      },
      includeReplies: 'تضمين الردود داخل سلاسل التعليقات',
      languagePref: {
        label: 'تفضيل اللغة',
        auto: 'كشف تلقائي',
        ar: 'العربية',
        en: 'الإنجليزية',
      },
      nlpFeatures: {
        title: 'ميزات معالجة اللغة الطبيعية',
        keywordExtraction: 'تفعيل استخراج الكلمات المفتاحية',
        generateReport: 'تفعيل إنشاء التقرير',
      },
      startButton: {
        start: 'بدء التحليل',
        analyzing: 'جارٍ التحليل…',
      },
      videoA: 'الفيديو أ',
      videoB: 'الفيديو ب',
      videoFallback: 'الفيديو',
      progressLabel: 'تقدّم التحليل',
      errorPrefix: 'خطأ:',
      complete: {
        banner: 'اكتمل التحليل! {title} — تم معالجة {count} تعليق.',
        viewHistory: 'عرض في السجل',
      },
    },
  },
} as const;
