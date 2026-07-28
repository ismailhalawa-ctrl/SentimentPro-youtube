import type { Metadata } from 'next';
import Link from 'next/link';
import { BookOpen } from 'lucide-react';
import { PageHero } from '@/components/marketing/page-hero';
import { Button } from '@/components/ui/button';
import { DocsContent } from '@/components/docs/docs-content';

export const metadata: Metadata = {
  title: 'Documentation — SentimentPRO',
  description: 'How Fast, Hybrid, and Smart analysis modes work, and how to use the AI comment assistant.',
};

export default function DocsPage() {
  return (
    <>
      <PageHero
        eyebrow="Documentation"
        title="Everything you need to analyze like a pro"
        description="A step-by-step guide to running analyses, understanding modes, and getting the most out of the AI assistant."
      />
      <div className="mx-auto -mt-12 flex max-w-7xl justify-center px-4 sm:px-6 lg:px-8">
        <Link href="/api-reference" passHref>
          <Button variant="secondary" size="sm">
            <BookOpen className="h-3.5 w-3.5" /> Looking for the API Reference?
          </Button>
        </Link>
      </div>
      <DocsContent />
    </>
  );
}
