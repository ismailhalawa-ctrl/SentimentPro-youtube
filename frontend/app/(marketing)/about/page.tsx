import type { Metadata } from 'next';
import { PageHero } from '@/components/marketing/page-hero';
import { AboutContent } from '@/components/about/about-content';
import { FinalCta } from '@/components/sections/final-cta';

export const metadata: Metadata = {
  title: 'About — SentimentPRO',
  description: 'An advanced audience-intelligence platform powered by specialized local models and LLMs.',
};

export default function AboutPage() {
  return (
    <>
      <PageHero
        eyebrow="About SentimentPRO"
        title="Deep audience intelligence, built for creators"
        description="An advanced YouTube comment analysis platform powered by specialized local models and large language models working together."
      />
      <AboutContent />
      <FinalCta />
    </>
  );
}
