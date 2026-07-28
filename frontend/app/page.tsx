import { Navbar } from '@/components/layout/navbar';
import { Footer } from '@/components/layout/footer';
import { HeroSection } from '@/components/sections/hero-section';
import { TrustedTechnologies } from '@/components/sections/trusted-technologies';
import { FeaturesSection } from '@/components/sections/features-section';
import { DashboardPreviewSection } from '@/components/sections/dashboard-preview-section';
import { AiWorkflow } from '@/components/sections/ai-workflow';
import { Statistics } from '@/components/sections/statistics';
import { Testimonials } from '@/components/sections/testimonials';
import { Faq } from '@/components/sections/faq';
import { FinalCta } from '@/components/sections/final-cta';

export default function LandingPage() {
  return (
    <>
      <Navbar />
      <main>
        <HeroSection />
        <TrustedTechnologies />
        <FeaturesSection />
        <DashboardPreviewSection />
        <AiWorkflow />
        <Statistics />
        <Testimonials />
        <Faq />
        <FinalCta />
      </main>
      <Footer />
    </>
  );
}