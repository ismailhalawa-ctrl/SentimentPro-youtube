'use client';

import { useState } from 'react';
import { AlertCircle, CheckCircle2, Send } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { FormField } from '@/components/forms/form-field';
import { submitContactMessage } from '@/features/support/api/support-api';
import { ApiError } from '@/lib/api-client';

interface FormErrors {
  name?: string;
  email?: string;
  message?: string;
}

function validateEmail(email: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

interface ContactFormProps {
  initialName?: string;
  initialEmail?: string;
  hideCard?: boolean;
}

export function ContactForm({ initialName = '', initialEmail = '', hideCard = false }: ContactFormProps) {
  const [name, setName] = useState(initialName);
  const [email, setEmail] = useState(initialEmail);
  const [message, setMessage] = useState('');
  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const nextErrors: FormErrors = {};
    if (!name.trim()) nextErrors.name = 'Please enter your name.';
    if (!email) nextErrors.email = 'Please enter your email.';
    else if (!validateEmail(email)) nextErrors.email = 'Enter a valid email address.';
    if (!message.trim()) nextErrors.message = 'Please enter a message.';
    else if (message.trim().length < 10) nextErrors.message = 'Please give us a bit more detail (10+ characters).';

    setErrors(nextErrors);
    setSubmitError(null);
    if (Object.keys(nextErrors).length > 0) return;

    setIsSubmitting(true);
    try {
      await submitContactMessage({ name: name.trim(), email, message: message.trim() });
      setIsSubmitted(true);
    } catch (err) {
      setSubmitError(err instanceof ApiError ? err.message : 'Failed to send your message. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  }

  if (isSubmitted) {
    const successContent = (
      <div className="flex flex-col items-center gap-3 text-center">
        <span className="flex h-12 w-12 items-center justify-center rounded-full bg-feedback-success/15 text-feedback-success">
          <CheckCircle2 className="h-6 w-6" />
        </span>
        <p className="text-lg font-semibold text-text-primary">Message received</p>
        <p className="max-w-sm text-sm text-text-secondary">
          Thanks for reaching out, {name.split(' ')[0]}. We&rsquo;ll get back to you at {email} soon.
        </p>
        <Button
          variant="ghost"
          size="sm"
          className="mt-2"
          onClick={() => {
            setIsSubmitted(false);
            setName(initialName);
            setEmail(initialEmail);
            setMessage('');
          }}
        >
          Send another message
        </Button>
      </div>
    );

    if (hideCard) return successContent;
    return (
      <Card variant="glass" className="p-8 text-center">
        <CardContent className="p-0">{successContent}</CardContent>
      </Card>
    );
  }

  const formContent = (
    <form onSubmit={handleSubmit} noValidate className="flex flex-col gap-5">
      <FormField label="Name" htmlFor="contact-name" error={errors.name}>
        <Input
          type="text"
          placeholder="Jane Doe"
          value={name}
          onChange={(e) => setName(e.target.value)}
          state={errors.name ? 'error' : 'default'}
          autoComplete="name"
        />
      </FormField>

      <FormField label="Email" htmlFor="contact-email" error={errors.email}>
        <Input
          type="email"
          placeholder="you@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          state={errors.email ? 'error' : 'default'}
          autoComplete="email"
        />
      </FormField>

      <FormField label="Message" htmlFor="contact-message" error={errors.message}>
        <Textarea
          placeholder="How can we help?"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          state={errors.message ? 'error' : 'default'}
        />
      </FormField>

      {Object.keys(errors).length > 0 && (
        <div
          role="alert"
          className="flex items-center gap-2 rounded-sm border border-feedback-danger/30 bg-feedback-danger/10 px-3.5 py-2.5 text-sm text-feedback-danger"
        >
          <AlertCircle className="h-4 w-4 shrink-0" />
          Please fix the highlighted fields above.
        </div>
      )}

      {submitError && (
        <div
          role="alert"
          className="flex items-center gap-2 rounded-sm border border-feedback-danger/30 bg-feedback-danger/10 px-3.5 py-2.5 text-sm text-feedback-danger"
        >
          <AlertCircle className="h-4 w-4 shrink-0" />
          {submitError}
        </div>
      )}

      <Button type="submit" variant="primary" size="lg" isLoading={isSubmitting} className="w-full">
        {!isSubmitting && <Send className="h-4 w-4" />} Send Message
      </Button>
    </form>
  );

  if (hideCard) return formContent;
  return (
    <Card variant="glass" className="p-6 sm:p-8">
      <CardContent className="p-0">{formContent}</CardContent>
    </Card>
  );
}
