export interface VideoInfo {
  video_id: string;
  title: string;
  channel_title: string;
  thumbnail_url: string;
  published_at: string;
  view_count: number;
  like_count: number;
  comment_count: number;
  comments_enabled: boolean;
  region_restricted: boolean;
}

export interface UrlValidateResult {
  is_valid: boolean;
  video_id: string | null;
}

export interface CommentItem {
  comment_id: string;
  author_display_name: string;
  author_profile_image_url: string;
  text_display: string;
  like_count: number;
  published_at: string;
  is_reply: boolean;
}

export interface CommentsResult {
  video_id: string;
  comments: CommentItem[];
  total_fetched: number;
  next_page_token: string | null;
  has_more: boolean;
}

export interface CommentsRequestPayload {
  url: string;
  max_results?: number;
  order?: 'relevance' | 'time';
  include_replies?: boolean;
  page_token?: string;
}
