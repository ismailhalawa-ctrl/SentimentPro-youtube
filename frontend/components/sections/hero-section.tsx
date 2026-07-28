import { HeroContent } from './hero-content';
import { DashboardPreview } from './dashboard-preview/dashboard-preview';
export function HeroSection() {
  return (
    <section className="relative overflow-hidden">
      <div className="bg-radial-glow pointer-events-none absolute inset-0" />

      <div className="relative mx-auto grid max-w-7xl grid-cols-1 items-center gap-12 px-4 py-20 sm:px-6 lg:grid-cols-2 lg:px-8 lg:py-32">
        <HeroContent />
        <div className="flex justify-center lg:justify-end">
          <DashboardPreview />
        </div>
      </div>
    </section>
  );
}