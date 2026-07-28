import type { Metadata } from 'next';
import { PageHero } from '@/components/marketing/page-hero';
import { PricingTiersSection } from '@/components/pricing/pricing-tiers-section';
import { PricingFaqSection } from '@/components/pricing/pricing-faq-section';
import { FinalCta } from '@/components/sections/final-cta';

export const metadata: Metadata = {
  title: 'Pricing — SentimentPRO',
  description: 'Simple pricing that scales from a free tier to enterprise-grade comment volumes.',
};

export default function PricingPage() {
  return (
    <>
      <PageHero
        eyebrow="Pricing"
        title="Simple pricing that scales with your channel"
        description="Start free, upgrade when you need deeper AI insights or bigger comment volumes. No hidden fees."
      />
      <PricingTiersSection />
      <PricingFaqSection />
      <FinalCta />
    </>
  );
}
