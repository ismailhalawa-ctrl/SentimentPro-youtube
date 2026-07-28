'use client';

import { useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';

export default function AssistantPage() {
  const params = useParams<{ jobId: string }>();
  const router = useRouter();
  const jobId = Number(params.jobId);

  useEffect(() => {
    router.replace(
      Number.isFinite(jobId) ? `/dashboard/audience-assistant?jobId=${jobId}` : '/dashboard/audience-assistant'
    );
  }, [jobId, router]);

  return null;
}
