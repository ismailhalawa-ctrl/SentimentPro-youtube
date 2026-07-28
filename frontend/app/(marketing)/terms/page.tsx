import type { Metadata } from 'next';
import { PageHero } from '@/components/marketing/page-hero';
import { LegalSection, type LegalSectionData } from '@/components/marketing/legal-section';

export const metadata: Metadata = {
  title: 'Terms of Service — SentimentPRO',
  description: 'The terms that govern your use of the SentimentPRO YouTube comment analysis platform.',
};

const LAST_UPDATED = 'July 14, 2026';

const SECTIONS: LegalSectionData[] = [
  {
    heading: 'Acceptance of Terms',
    body: (
      <p>
        By creating an account or otherwise accessing SentimentPRO (the &ldquo;Service&rdquo;), you agree
        to be bound by these Terms of Service and our{' '}
        <a href="/privacy">Privacy Policy</a>. If you do not agree, please do not use the Service.
      </p>
    ),
  },
  {
    heading: 'Description of Service',
    body: (
      <>
        <p>
          SentimentPRO analyzes publicly available YouTube comments on videos you submit, using a
          combination of locally-hosted transformer models (Fast Mode), selective escalation to
          large language model providers (Hybrid Mode), and full LLM-driven analysis (Smart Mode),
          to surface sentiment, spam, sarcasm, keyword, topic, and audience-intelligence insights.
          The Service also offers an AI comment assistant that answers natural-language questions
          grounded in a video&rsquo;s analyzed comments via retrieval-augmented generation (RAG).
        </p>
        <p>
          Analysis quality, available comment volume, and feature access vary by plan — see our{' '}
          <a href="/pricing">Pricing</a> page for current tier details.
        </p>
      </>
    ),
  },
  {
    heading: 'Accounts & Eligibility',
    body: (
      <ul>
        <li>You must provide accurate registration information and keep your credentials secure.</li>
        <li>You are responsible for all activity that occurs under your account.</li>
        <li>You must be at least 16 years old, or the age of digital consent in your jurisdiction, to create an account.</li>
        <li>We may suspend or terminate accounts used in violation of these Terms.</li>
      </ul>
    ),
  },
  {
    heading: 'Google Account & YouTube Data API Services',
    body: (
      <>
        <p>
          SentimentPRO&rsquo;s &ldquo;Continue with Google&rdquo; sign-in and video analysis features use
          Google&rsquo;s OAuth 2.0 and the YouTube Data API v3. By connecting a Google account or
          submitting a YouTube video for analysis, you acknowledge that:
        </p>
        <ul>
          <li>
            Sign-in via Google only requests your basic profile information (name, email, profile
            picture) to create or authenticate your account — we never post, comment, or take any
            action on YouTube on your behalf.
          </li>
          <li>
            Video analysis reads publicly available comment data (comment text, author display
            name, like count, publish date) through the YouTube Data API for videos you explicitly
            submit — we do not access private or unlisted content you don&rsquo;t provide a link to.
          </li>
          <li>
            Your use of YouTube data through SentimentPRO is also subject to the{' '}
            <a href="https://www.youtube.com/t/terms" target="_blank" rel="noreferrer">
              YouTube Terms of Service
            </a>{' '}
            and Google&rsquo;s{' '}
            <a href="https://policies.google.com/privacy" target="_blank" rel="noreferrer">
              Privacy Policy
            </a>
            .
          </li>
        </ul>
      </>
    ),
  },
  {
    heading: 'Subscription Plans & Payment',
    body: (
      <ul>
        <li>The Free tier is available at no cost, subject to the comment-volume and feature limits described on our Pricing page.</li>
        <li>Paid tiers (Creator/Pro and Enterprise) are billed on a recurring basis until cancelled; prices are shown before checkout and may change with advance notice.</li>
        <li>Enterprise pricing and volume commitments are governed by a separate order form or agreement where applicable.</li>
        <li>Fees are non-refundable except where required by law or expressly stated otherwise at purchase.</li>
      </ul>
    ),
  },
  {
    heading: 'Acceptable Use & API Rate Limits',
    body: (
      <>
        <p>You agree not to:</p>
        <ul>
          <li>Use the Service to harass, defame, or build a profile of a private individual identified in comment data.</li>
          <li>Attempt to circumvent per-plan comment-volume limits, request-rate limits, or queue priority rules.</li>
          <li>Reverse-engineer, scrape, or resell access to the Service or its underlying models without written permission.</li>
          <li>Submit videos or content for the purpose of generating misleading, defamatory, or unlawful analysis output.</li>
        </ul>
        <p>
          Each plan enforces its own comment-volume ceiling per analysis and a fair-use request rate;
          exceeding these limits may result in queued, throttled, or rejected requests.
        </p>
      </>
    ),
  },
  {
    heading: 'User Content & AI-Generated Output',
    body: (
      <p>
        You retain no ownership claim over third-party YouTube comment data processed by the
        Service. Sentiment scores, summaries, insights, and chat-assistant answers generated by
        SentimentPRO are provided &ldquo;as is&rdquo; for your informational use; AI-generated content
        may contain inaccuracies and should not be treated as a substitute for your own judgment,
        especially for decisions with legal, financial, or reputational consequences.
      </p>
    ),
  },
  {
    heading: 'Intellectual Property',
    body: (
      <p>
        SentimentPRO, its logo, and its underlying software are the property of their respective
        owners and are protected by applicable intellectual property laws. Nothing in these Terms
        grants you rights to our trademarks, source code, or trained models beyond what is
        necessary to use the Service as intended.
      </p>
    ),
  },
  {
    heading: 'Third-Party AI Providers',
    body: (
      <p>
        Hybrid and Smart mode analysis, and the AI comment assistant, may route data to third-party
        large language model providers (such as OpenAI or Google Gemini) strictly to generate the
        analysis or answer you requested. These providers process data under their own terms; see
        our <a href="/privacy">Privacy Policy</a> for details on what is shared and why.
      </p>
    ),
  },
  {
    heading: 'Disclaimers & Limitation of Liability',
    body: (
      <p>
        The Service is provided &ldquo;as is&rdquo; without warranties of any kind, express or implied,
        including accuracy, fitness for a particular purpose, or uninterrupted availability. To the
        maximum extent permitted by law, SentimentPRO shall not be liable for indirect, incidental,
        or consequential damages arising from your use of the Service or reliance on its analysis
        output.
      </p>
    ),
  },
  {
    heading: 'Termination',
    body: (
      <p>
        You may stop using the Service and delete your account at any time from Settings. We may
        suspend or terminate access for violation of these Terms, non-payment on a paid plan, or
        extended account inactivity, with notice where reasonably practicable.
      </p>
    ),
  },
  {
    heading: 'Changes to These Terms',
    body: (
      <p>
        We may update these Terms from time to time. Material changes will be reflected by updating
        the &ldquo;last updated&rdquo; date above; continued use of the Service after changes take effect
        constitutes acceptance of the revised Terms.
      </p>
    ),
  },
  {
    heading: 'Governing Law',
    body: (
      <p>
        These Terms are governed by the laws of the jurisdiction in which SentimentPRO is
        registered to operate, without regard to conflict-of-law principles, unless otherwise
        required by applicable local law.
      </p>
    ),
  },
  {
    heading: 'Contact',
    body: (
      <p>
        Questions about these Terms? Reach out via our <a href="/contact">Contact page</a>.
      </p>
    ),
  },
];

export default function TermsPage() {
  return (
    <>
      <PageHero
        eyebrow="Legal"
        title="Terms of Service"
        description={`Last updated ${LAST_UPDATED}. Please read these terms carefully before using SentimentPRO.`}
      />
      <div className="mx-auto max-w-3xl px-4 pb-24 sm:px-6 lg:px-8">
        {SECTIONS.map((section, index) => (
          <LegalSection key={section.heading} index={index} {...section} />
        ))}
      </div>
    </>
  );
}
