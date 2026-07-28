import type { Metadata } from 'next';
import Link from 'next/link';
import { Mail, BookOpen, HelpCircle } from 'lucide-react';
import { PageHero } from '@/components/marketing/page-hero';
import { Card, CardContent } from '@/components/ui/card';
import { ContactForm } from '@/components/contact/contact-form';

export const metadata: Metadata = {
  title: 'Contact — SentimentPRO',
  description: 'Get in touch with the SentimentPRO team.',
};

export default function ContactPage() {
  return (
    <>
      <PageHero
        eyebrow="Get in touch"
        title="I would love to hear from you"
        description="Questions about a plan, a bug, or an Enterprise quote — send me a message and I'll get back to you."
      />

      <section className="pb-24">
        <div className="mx-auto grid max-w-5xl grid-cols-1 gap-8 px-4 sm:px-6 lg:grid-cols-5 lg:px-8">
          <div className="flex flex-col gap-4 lg:col-span-2">
            <Card variant="glass" className="p-6">
              <CardContent className="flex flex-col gap-4 p-0">
                <div className="flex items-start gap-3">
                  <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-brand-500/15 text-brand-400">
                    <Mail className="h-4 w-4" />
                  </span>
                  <div>
                    <p className="text-sm font-semibold text-text-primary">Contact Me</p>
                    <p className="text-sm text-text-secondary">Ismaeelhalawa2005@gmail.com</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-brand-500/15 text-brand-400">
                    <BookOpen className="h-4 w-4" />
                  </span>
                  <div>
                    <p className="text-sm font-semibold text-text-primary">Check the docs first</p>
                    <p className="text-sm text-text-secondary">
                      Most questions about modes, limits, and exports are answered in our{' '}
                      <Link href="/docs" className="text-brand-400 hover:text-brand-500">
                        Documentation
                      </Link>
                      .
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-brand-500/15 text-brand-400">
                    <HelpCircle className="h-4 w-4" />
                  </span>
                  <div>
                    <p className="text-sm font-semibold text-text-primary">Enterprise & billing</p>
                    <p className="text-sm text-text-secondary">
                      For custom volume or billing questions, see{' '}
                      <Link href="/pricing" className="text-brand-400 hover:text-brand-500">
                        Pricing
                      </Link>{' '}
                      or mention it in your message.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="lg:col-span-3">
            <ContactForm />
          </div>
        </div>
      </section>
    </>
  );
}
