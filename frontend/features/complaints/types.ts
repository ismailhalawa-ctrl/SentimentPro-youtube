export interface RankedCategory {
  category: string;
  count: number;
  total_likes: number;
  example_comment_ids: number[];
}

export interface ExtractedCommentItem {
  comment_id: number;
  text: string;
  category: string | null;
  confidence: number | null;
  is_feature_request: boolean | null;
}

export interface CommentExtractionPayload {
  ranked_categories: RankedCategory[];
  items: ExtractedCommentItem[];
}
