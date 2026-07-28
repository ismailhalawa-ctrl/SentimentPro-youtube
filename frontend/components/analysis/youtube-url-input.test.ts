import { describe, expect, it } from 'vitest';
import { isValidYouTubeUrl } from './youtube-url-input';

describe('isValidYouTubeUrl', () => {
  it('accepts a standard watch URL', () => {
    expect(isValidYouTubeUrl('https://www.youtube.com/watch?v=dQw4w9WgXcQ')).toBe(true);
  });

  it('accepts a URL without https:// or www.', () => {
    expect(isValidYouTubeUrl('youtube.com/watch?v=dQw4w9WgXcQ')).toBe(true);
  });

  it('accepts a youtu.be short URL', () => {
    expect(isValidYouTubeUrl('https://youtu.be/dQw4w9WgXcQ')).toBe(true);
  });

  it('accepts a shorts URL', () => {
    expect(isValidYouTubeUrl('https://www.youtube.com/shorts/dQw4w9WgXcQ')).toBe(true);
  });

  it('accepts an embed URL', () => {
    expect(isValidYouTubeUrl('https://www.youtube.com/embed/dQw4w9WgXcQ')).toBe(true);
  });

  it('accepts a mobile (m.) URL', () => {
    expect(isValidYouTubeUrl('https://m.youtube.com/watch?v=dQw4w9WgXcQ')).toBe(true);
  });

  it('accepts a watch URL with extra query params', () => {
    expect(isValidYouTubeUrl('https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s')).toBe(true);
  });

  it('rejects a completely unrelated URL', () => {
    expect(isValidYouTubeUrl('https://www.example.com/watch?v=dQw4w9WgXcQ')).toBe(false);
  });

  it('rejects a YouTube channel URL', () => {
    expect(isValidYouTubeUrl('https://www.youtube.com/@SomeChannel')).toBe(false);
  });

  it('rejects an empty string', () => {
    expect(isValidYouTubeUrl('')).toBe(false);
  });

  it('rejects a video id that is too short', () => {
    expect(isValidYouTubeUrl('https://www.youtube.com/watch?v=short')).toBe(false);
  });

  it('rejects plain text', () => {
    expect(isValidYouTubeUrl('not a url at all')).toBe(false);
  });

  it('trims surrounding whitespace before validating', () => {
    expect(isValidYouTubeUrl('  https://www.youtube.com/watch?v=dQw4w9WgXcQ  ')).toBe(true);
  });
});
