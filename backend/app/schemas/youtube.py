from typing import Literal

from pydantic import BaseModel, Field


class UrlValidateRequest(BaseModel):
    url: str


class UrlValidateResponse(BaseModel):
    is_valid: bool
    video_id: str | None = None


class VideoInfoRequest(BaseModel):
    url: str


class VideoInfoResponse(BaseModel):
    video_id: str
    title: str
    channel_title: str
    thumbnail_url: str
    published_at: str
    view_count: int
    like_count: int
    comment_count: int
    comments_enabled: bool
    region_restricted: bool


class CommentsRequest(BaseModel):
    url: str
    max_results: int = Field(default=100, ge=1, le=1_000_000)
    order: Literal["relevance", "time"] = "relevance"
    include_replies: bool = False
    page_token: str | None = None


class CommentItem(BaseModel):
    comment_id: str
    author_display_name: str
    author_profile_image_url: str
    text_display: str
    like_count: int
    published_at: str
    is_reply: bool = False


class CommentsResponse(BaseModel):
    video_id: str
    comments: list[CommentItem]
    total_fetched: int
    next_page_token: str | None = None
    has_more: bool
