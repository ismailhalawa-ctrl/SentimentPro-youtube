import type { Metadata } from 'next';
import { PageHero } from '@/components/marketing/page-hero';
import { LegalSection, type LegalSectionData } from '@/components/marketing/legal-section';

export const metadata: Metadata = {
  title: 'Privacy Policy — SentimentPRO',
  description: 'How SentimentPRO collects, uses, and protects your data, including Google and YouTube data.',
};

const LAST_UPDATED = 'July 14, 2026';

const SECTIONS: LegalSectionData[] = [
  {
    heading: 'Overview',
    body: (
      <p>
        This Privacy Policy explains what data SentimentPRO collects when you use our YouTube
        comment sentiment analysis platform, why we collect it, and the choices you have —
        including how to export or permanently delete it.
      </p>
    ),
  },
  {
    heading: 'Information We Collect',
    body: (
      <ul>
        <li><strong>Account information:</strong> name, email address, and a hashed password (or, if you sign in with Google, your Google account&rsquo;s name, email, and profile picture).</li>
        <li><strong>Submitted video URLs:</strong> the YouTube links you choose to analyze.</li>
        <li><strong>YouTube comment data:</strong> publicly available comment text, author display name, like count, and publish date, retrieved via the YouTube Data API v3 for videos you submit.</li>
        <li><strong>Generated analysis data:</strong> sentiment scores, spam/sarcasm flags, keywords, topics, AI-generated summaries, and your AI assistant chat history for each analysis.</li>
        <li><strong>Usage data:</strong> basic technical data (IP address, browser type, session timestamps) needed to keep the Service secure and reliable.</li>
      </ul>
    ),
  },
  {
    heading: 'How We Use Google User Data',
    body: (
      <>
        <p>
          SentimentPRO&rsquo;s use and transfer of information received from Google APIs adheres to
          the{' '}
          <a href="https://developers.google.com/terms/api-services-user-data-policy" target="_blank" rel="noreferrer">
            Google API Services User Data Policy
          </a>
          , including the Limited Use requirements. Concretely:
        </p>
        <ul>
          <li>Google profile data (name, email, picture) is used only to create and authenticate your SentimentPRO account.</li>
          <li>We do not use Google account data for advertising, and we do not sell it to third parties.</li>
          <li>We do not allow humans to read Google user data except with your consent, to investigate abuse reported to us, or to comply with the law.</li>
        </ul>
      </>
    ),
  },
  {
    heading: 'Data Retention & Deletion',
    body: (
      <>
        <p>
          Analysis jobs, their comments, AI insights, and chat history are retained until you delete
          them. You are always in control:
        </p>
        <ul>
          <li>Delete a single analysis at any time from the History page — this permanently removes its comments, insights, chat history, and vector search index.</li>
          <li>Use &ldquo;Clear All History&rdquo; to permanently delete every analysis on your account in one action.</li>
          <li>Deleting your account (Settings) permanently removes your account record along with all associated analyses.</li>
        </ul>
        <p>Deletion is immediate and permanent — we do not keep a recoverable backup of deleted analyses.</p>
      </>
    ),
  },
  {
    heading: 'Third-Party Services We Use',
    body: (
      <ul>
        <li><strong>YouTube Data API v3</strong> — to retrieve public comment data for videos you submit.</li>
        <li><strong>OpenAI / Google Gemini</strong> — used only for Hybrid- and Smart-mode analysis and the AI comment assistant, and only when you choose those modes; comment text relevant to your request is sent to whichever provider is configured.</li>
        <li><strong>Local, self-hosted models</strong> — Fast Mode sentiment analysis runs on models hosted on our own infrastructure and never leaves our servers.</li>
        <li><strong>Vector search index</strong> — comment embeddings used to power the AI assistant are stored in a search index scoped to each analysis, and purged when that analysis is deleted.</li>
      </ul>
    ),
  },
  {
    heading: 'Security',
    body: (
      <p>
        Passwords are stored using industry-standard hashing, sessions are authenticated via
        httpOnly cookies, and access to analysis data is scoped to the account that created it. No
        method of transmission or storage is 100% secure, but we apply reasonable technical and
        organizational safeguards appropriate to the sensitivity of the data involved.
      </p>
    ),
  },
  {
    heading: "Children's Privacy",
    body: (
      <p>
        SentimentPRO is not directed at children under 16, and we do not knowingly collect account
        information from them. If you believe a child has created an account, please contact us so
        we can remove it.
      </p>
    ),
  },
  {
    heading: 'International Data Transfers',
    body: (
      <p>
        Depending on where our infrastructure and third-party providers are located, your data may
        be processed in a country other than your own. Where required, we rely on appropriate
        safeguards for such transfers under applicable data protection law.
      </p>
    ),
  },
  {
    heading: 'Your Rights',
    body: (
      <ul>
        <li>Access and export your analysis data at any time via CSV, Excel, or PDF export.</li>
        <li>Delete individual analyses or your entire history from the History page.</li>
        <li>Request access, correction, or deletion of your account information by contacting us.</li>
        <li>Depending on your jurisdiction, you may have additional rights under laws such as the GDPR or CCPA.</li>
      </ul>
    ),
  },
  {
    heading: 'Cookies',
    body: (
      <p>
        We use a single essential, httpOnly session cookie to keep you signed in. We do not use
        third-party advertising or tracking cookies.
      </p>
    ),
  },
  {
    heading: 'Changes to This Policy',
    body: (
      <p>
        We may update this Privacy Policy from time to time. Material changes will be reflected by
        updating the &ldquo;last updated&rdquo; date above.
      </p>
    ),
  },
  {
    heading: 'Contact',
    body: (
      <p>
        Questions about this Privacy Policy or a data request? Reach out via our{' '}
        <a href="/contact">Contact page</a>.
      </p>
    ),
  },
];

export default function PrivacyPage() {
  return (
    <>
      <PageHero
        eyebrow="Legal"
        title="Privacy Policy"
        description={`Last updated ${LAST_UPDATED}. How we handle your data, including Google and YouTube data.`}
      />
      <div className="mx-auto max-w-3xl px-4 pb-24 sm:px-6 lg:px-8">
        {SECTIONS.map((section, index) => (
          <LegalSection key={section.heading} index={index} {...section} />
        ))}
      </div>
    </>
  );
}
