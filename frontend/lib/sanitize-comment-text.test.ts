import { describe, expect, it } from 'vitest';
import { sanitizeCommentText } from './sanitize-comment-text';

describe('sanitizeCommentText', () => {
  it('converts <br> tags to newlines', () => {
    expect(sanitizeCommentText('line one<br>line two')).toBe('line one\nline two');
    expect(sanitizeCommentText('line one<br/>line two')).toBe('line one\nline two');
    expect(sanitizeCommentText('line one<br />line two')).toBe('line one\nline two');
  });

  it('strips arbitrary HTML tags', () => {
    expect(sanitizeCommentText('<b>bold</b> and <i>italic</i>')).toBe('bold and italic');
  });

  it('strips a script tag entirely rather than leaving executable content', () => {
    const result = sanitizeCommentText('hello <script>alert(1)</script> world');
    expect(result).not.toContain('<script>');
    expect(result).not.toContain('</script>');
  });

  it('strips an img tag with an onerror handler', () => {
    const result = sanitizeCommentText('<img src=x onerror="alert(1)">');
    expect(result).not.toContain('<img');
    expect(result).not.toContain('onerror');
  });

  it('decodes known HTML entities', () => {
    expect(sanitizeCommentText('&amp;')).toBe('&');
    expect(sanitizeCommentText('&lt;')).toBe('<');
    expect(sanitizeCommentText('&gt;')).toBe('>');
    expect(sanitizeCommentText('&quot;')).toBe('"');
    expect(sanitizeCommentText('&#39;')).toBe("'");
    expect(sanitizeCommentText('&apos;')).toBe("'");
  });

  it('leaves unknown entities untouched', () => {
    expect(sanitizeCommentText('&nbsp;')).toBe('&nbsp;');
  });

  it('leaves plain text completely unchanged', () => {
    const plain = 'This video was really helpful, thanks!';
    expect(sanitizeCommentText(plain)).toBe(plain);
  });

  it('handles an empty string', () => {
    expect(sanitizeCommentText('')).toBe('');
  });

  it('handles combined tags and entities together', () => {
    const input = '<b>5 &lt; 10</b><br>and &amp; that is true';
    expect(sanitizeCommentText(input)).toBe('5 < 10\nand & that is true');
  });
});
