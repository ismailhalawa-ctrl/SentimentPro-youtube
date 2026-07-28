import { Card, CardContent } from '@/components/ui/card';
import { CodeBlock } from './code-block';
import { cn } from '@/lib/utils';

export type HttpMethod = 'GET' | 'POST' | 'DELETE';

export interface EndpointData {
  method: HttpMethod;
  path: string;
  description: string;
  requestBody?: string;
  response: string;
}

const METHOD_STYLES: Record<HttpMethod, string> = {
  GET: 'bg-feedback-info/15 text-feedback-info',
  POST: 'bg-feedback-success/15 text-feedback-success',
  DELETE: 'bg-feedback-danger/15 text-feedback-danger',
};

export function EndpointCard({ endpoint }: { endpoint: EndpointData }) {
  return (
    <Card variant="glass" className="p-5 sm:p-6">
      <CardContent className="flex flex-col gap-4 p-0">
        <div className="flex flex-wrap items-center gap-3">
          <span
            className={cn(
              'rounded-sm px-2.5 py-1 font-mono text-xs font-semibold',
              METHOD_STYLES[endpoint.method]
            )}
          >
            {endpoint.method}
          </span>
          <code className="font-mono text-sm text-text-primary">{endpoint.path}</code>
        </div>
        <p className="text-sm text-text-secondary">{endpoint.description}</p>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {endpoint.requestBody && <CodeBlock label="Request body" code={endpoint.requestBody} />}
          <CodeBlock label="Response" code={endpoint.response} />
        </div>
      </CardContent>
    </Card>
  );
}
