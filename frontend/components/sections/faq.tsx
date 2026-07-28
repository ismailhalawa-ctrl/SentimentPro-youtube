'use client';

import { useState } from 'react';
import { FaqItem, type FaqItemData } from '@/components/faq/faq-item';
import { SectionHeading } from '@/components/ui/section-heading';

const FAQS: FaqItemData[] = [
  {
    question: 'What is YouTube Comment Sentiment Analyzer PRO?',
    answer:
      'It\'s a platform that analyzes YouTube comments at scale, turning raw audience reactions into sentiment scores, insights, and exportable reports.',
  },
  {
    question: 'How does the AI sentiment analysis work?',
    answer:
      'Each comment is passed through trained NLP models that classify it as positive, neutral, or negative, along with a confidence score for that prediction.',
  },
  {
    question: 'Which AI models are used?',
    answer:
      'The platform uses transformer models, including MARBERT for Arabic comments and BERT-based models for English, chosen for their accuracy on short, informal text.',
  },
  {
    question: 'Can it detect spam and toxic comments?',
    answer:
      'Yes. A dedicated spam detection layer flags likely spam and low-quality comments separately from sentiment, so they don\'t skew your results.',
  },
  {
    question: 'Can I export analysis reports?',
    answer:
      'Yes. You can generate professional PDF reports for sharing, or export the raw analyzed data as CSV for your own tools and pipelines.',
  },
  {
    question: 'Does it support multiple languages?',
    answer:
      'The platform currently supports Arabic and English through its dual-model setup, with more languages planned.',
  },
  {
    question: 'Is my YouTube data stored?',
    answer:
      'Comments are processed to generate your analysis and results. Refer to the platform\'s data policy for full retention and storage details.',
  },
  {
    question: 'Who is this platform designed for?',
    answer:
      'It\'s built for content creators tracking audience reaction, researchers studying online discourse, and marketing teams monitoring campaign response.',
  },
];

export function Faq() {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  return (
    <section className="relative py-20 sm:py-28">
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
        <SectionHeading
          eyebrow="Frequently asked questions"
          title="Everything you need to know"
          className="text-center"
        />

        <div className="mt-12 flex flex-col gap-4">
          {FAQS.map((item, index) => (
            <FaqItem
              key={item.question}
              item={item}
              index={index}
              isOpen={openIndex === index}
              onToggle={() => setOpenIndex(openIndex === index ? null : index)}
            />
          ))}
        </div>
      </div>
    </section>
  );
}