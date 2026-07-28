'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';
import { FooterColumn, type FooterLink } from '@/components/footer/footer-column';
import { SocialLinks } from '@/components/footer/social-links';

const PRODUCT_LINKS: FooterLink[] = [
  { label: 'Features', href: '/#features' },
  { label: 'Dashboard', href: '/dashboard' },
  { label: 'Analytics', href: '/dashboard' },
  { label: 'Reports', href: '/dashboard/reports' },
];

const RESOURCE_LINKS: FooterLink[] = [
  { label: 'Documentation', href: '/docs' },
  { label: 'GitHub', href: 'https://github.com/ismailhalawa-ctrl' },
  { label: 'API Reference', href: '/api-reference' },
];

const COMPANY_LINKS: FooterLink[] = [
  { label: 'About', href: '/about' },
  { label: 'Contact', href: '/contact' },
  { label: 'Terms of Service', href: '/terms' },
  { label: 'Privacy Policy', href: '/privacy' },
];

export function Footer() {
  return (
    <footer className="relative border-t border-border-subtle">
      <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-5"
        >
          <div className="flex flex-col gap-4 lg:col-span-2">

            {}
            <Link
              href="/"
              onClick={(e) => {
                e.preventDefault();
                window.scrollTo({
                  top: 0,
                  behavior: 'smooth',
                });
              }}
              className="flex items-center gap-2 w-fit"
            >
              <span className="flex h-8 w-8 items-center justify-center rounded-md bg-gradient-brand">
                <Sparkles className="h-4 w-4 text-text-primary" />
              </span>
              <span className="text-base font-semibold text-text-primary">
                Sentiment<span className="text-brand-400">PRO</span>
              </span>
            </Link>

            <p className="max-w-xs text-sm text-text-secondary">
              AI-powered YouTube comment analysis platform using advanced NLP models.
            </p>
            <SocialLinks />
          </div>

          <FooterColumn title="Product" links={PRODUCT_LINKS} />
          <FooterColumn title="Resources" links={RESOURCE_LINKS} />
          <FooterColumn title="Company" links={COMPANY_LINKS} />
        </motion.div>

        <div className="mt-12 flex flex-col items-center justify-between gap-4 border-t border-border-subtle pt-6 sm:flex-row">
          <p className="text-sm text-text-muted">
            © {new Date().getFullYear()} SentimentPRO. All rights reserved.
          </p>
          <div className="flex items-center gap-2 text-xs text-text-muted">
            <span className="h-2 w-2 rounded-full bg-sentiment-positive" />
            All systems operational
          </div>
        </div>
      </div>
    </footer>
  );
}