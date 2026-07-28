const BR_TAG_RE = /<br\s*\/?>/gi;
const HTML_TAG_RE = /<[^>]+>/g;
const HTML_ENTITIES: Record<string, string> = {
  '&amp;': '&',
  '&lt;': '<',
  '&gt;': '>',
  '&quot;': '"',
  '&#39;': "'",
  '&apos;': "'",
};
const HTML_ENTITY_RE = /&amp;|&lt;|&gt;|&quot;|&#39;|&apos;/g;

export function sanitizeCommentText(text: string): string {
  return text
    .replace(BR_TAG_RE, '\n')
    .replace(HTML_TAG_RE, '')
    .replace(HTML_ENTITY_RE, (entity) => HTML_ENTITIES[entity] ?? entity);
}
