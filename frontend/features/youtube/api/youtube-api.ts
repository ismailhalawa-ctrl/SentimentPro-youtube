import { apiClient } from '@/lib/api-client';
import type {
  CommentsRequestPayload,
  CommentsResult,
  UrlValidateResult,
  VideoInfo,
} from '@/features/youtube/types';

export function validateUrlRequest(url: string): Promise<UrlValidateResult> {
  return apiClient<UrlValidateResult>('/api/v1/youtube/validate', {
    method: 'POST',
    body: { url },
  });
}

export function videoInfoRequest(url: string): Promise<VideoInfo> {
  return apiClient<VideoInfo>('/api/v1/youtube/video-info', {
    method: 'POST',
    body: { url },
  });
}

export function commentsRequest(payload: CommentsRequestPayload): Promise<CommentsResult> {
  return apiClient<CommentsResult>('/api/v1/youtube/comments', {
    method: 'POST',
    body: payload,
  });
}
