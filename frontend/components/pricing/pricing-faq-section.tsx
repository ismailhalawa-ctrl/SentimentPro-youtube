'use client';

import { useState } from 'react';
import { SectionHeading } from '@/components/ui/section-heading';
import { FaqItem, type FaqItemData } from '@/components/faq/faq-item';

const PRICING_FAQS: FaqItemData[] = [
  {
    question: 'What counts as a "comment" toward my plan limit?',
    answer:
      'Every top-level comment and reply that gets pulled into an analysis counts once toward that analysis\'s comment limit. Limits apply per analysis, not cumulatively across your account.',
  },
  {
    question: 'Can I switch plans at any time?',
    answer:
      'Yes. You can upgrade or downgrade from Settings at any time — changes take effect at the start of your next billing cycle.',
  },
  {
    question: 'Do you offer a free trial of the Pro plan?',
    answer:
      'The Free tier itself works as an open-ended trial of the core analysis experience. Reach out via Contact if you\'d like a time-boxed trial of Pro-tier features before committing.',
  },
  {
    question: "What happens if an analysis exceeds my plan's comment limit?",
    answer:
      "We analyze up to your plan's limit and let you know the video had more comments available — upgrading re-runs the analysis against the full comment set.",
  },
  {
    question: 'Is there a refund policy?',
    answer:
      'Paid subscriptions can be cancelled at any time to stop future billing. Reach out via Contact for billing questions specific to your account.',
  },
  {
    question: 'How is Enterprise pricing determined?',
    answer:
      'Enterprise pricing is based on comment volume, concurrency/queue priority needs, and support requirements. Contact Sales for a quote tailored to your usage.',
  },
];

export function PricingFaqSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  return (
    <section className="relative pb-20 sm:pb-28">
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
        <SectionHeading
          eyebrow="Pricing questions"
          title="Frequently asked questions"
          className="text-center"
        />
        <div className="mt-12 flex flex-col gap-4">
          {PRICING_FAQS.map((item, index) => (
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
