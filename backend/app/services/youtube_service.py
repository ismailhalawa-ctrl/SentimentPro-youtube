import asyncio
import re
from urllib.parse import parse_qs, urlparse

import httpx

from app.core.config import settings

YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"
VIDEO_ID_PATTERN = re.compile(r"^[\w-]{11}$")


class YouTubeApiError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


def extract_video_id(url: str) -> str | None:
    url = url.strip()
    if not url:
        return None
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    host = parsed.netloc.lower()
    for prefix in ("www.", "m."):
        if host.startswith(prefix):
            host = host[len(prefix) :]

    video_id: str | None = None

    if host == "youtu.be":
        video_id = parsed.path.lstrip("/").split("/")[0]
    elif host in ("youtube.com", "music.youtube.com"):
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [None])[0]
        elif parsed.path.startswith("/shorts/"):
            video_id = parsed.path.removeprefix("/shorts/").split("/")[0]
        elif parsed.path.startswith("/embed/"):
            video_id = parsed.path.removeprefix("/embed/").split("/")[0]

    if video_id and VIDEO_ID_PATTERN.fullmatch(video_id):
        return video_id
    return None


def _require_api_key() -> str:
    if not settings.youtube_api_key:
        raise YouTubeApiError(
            status_code=503,
            message="YouTube integration is not configured on the server.",
        )
    return settings.youtube_api_key


def _map_youtube_error(response: httpx.Response) -> YouTubeApiError:
    try:
        body = response.json()
        reasons = {e.get("reason") for e in body.get("error", {}).get("errors", [])}
    except Exception:
        reasons = set()

    if "quotaExceeded" in reasons or "dailyLimitExceeded" in reasons:
        return YouTubeApiError(503, "YouTube API quota exceeded. Try again later.")
    if "commentsDisabled" in reasons:
        return YouTubeApiError(409, "Comments are disabled for this video.")
    if "videoNotFound" in reasons:
        return YouTubeApiError(404, "Video not found.")
    if "forbidden" in reasons or response.status_code == 403:
        return YouTubeApiError(403, "This video's comments cannot be accessed.")

    return YouTubeApiError(502, "YouTube API returned an unexpected error. Please try again.")


async def fetch_video_info(video_id: str) -> dict:
    api_key = _require_api_key()

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(
            f"{YOUTUBE_API_BASE}/videos",
            params={
                "part": "snippet,statistics,contentDetails,status",
                "id": video_id,
                "key": api_key,
            },
        )

    if response.status_code != 200:
        raise _map_youtube_error(response)

    items = response.json().get("items", [])
    if not items:
        raise YouTubeApiError(404, "Video not found or is private.")

    item = items[0]
    snippet = item.get("snippet", {})
    statistics = item.get("statistics", {})
    content_details = item.get("contentDetails", {})

    thumbnails = snippet.get("thumbnails", {})
    thumbnail_url = (
        thumbnails.get("high") or thumbnails.get("medium") or thumbnails.get("default") or {}
    ).get("url", "")

    return {
        "video_id": video_id,
        "title": snippet.get("title", ""),
        "channel_title": snippet.get("channelTitle", ""),
        "thumbnail_url": thumbnail_url,
        "published_at": snippet.get("publishedAt", ""),
        "view_count": int(statistics.get("viewCount", 0)),
        "like_count": int(statistics.get("likeCount", 0)),
        "comment_count": int(statistics.get("commentCount", 0)),
        "comments_enabled": "commentCount" in statistics,
        "region_restricted": bool(content_details.get("regionRestriction")),
    }


async def fetch_comments(
    video_id: str,
    max_results: int,
    order: str,
    include_replies: bool,
    page_token: str | None,
    cancel_event: asyncio.Event | None = None,
) -> dict:
    api_key = _require_api_key()

    page_size = min(100, max_results)
    comments: list[dict] = []
    seen_comment_ids: set[str] = set()
    next_token = page_token
    current_order = order
    fallback_order_tried = False

    async with httpx.AsyncClient(timeout=10) as client:
        while len(comments) < max_results:
            if cancel_event is not None and cancel_event.is_set():
                break

            remaining = max_results - len(comments)
            response = await client.get(
                f"{YOUTUBE_API_BASE}/commentThreads",
                params={
                    "part": "snippet,replies" if include_replies else "snippet",
                    "videoId": video_id,
                    "maxResults": min(page_size, remaining),
                    "order": current_order,
                    "key": api_key,
                    **({"pageToken": next_token} if next_token else {}),
                },
            )

            if response.status_code != 200:
                if comments:
                    break
                raise _map_youtube_error(response)

            body = response.json()

            for thread in body.get("items", []):
                comment_id = thread["snippet"]["topLevelComment"]["id"]
                if comment_id in seen_comment_ids:
                    continue
                seen_comment_ids.add(comment_id)

                top_comment = thread["snippet"]["topLevelComment"]["snippet"]
                comments.append(
                    {
                        "comment_id": comment_id,
                        "author_display_name": top_comment.get("authorDisplayName", ""),
                        "author_profile_image_url": top_comment.get("authorProfileImageUrl", ""),
                        "text_display": top_comment.get("textOriginal", ""),
                        "like_count": int(top_comment.get("likeCount", 0)),
                        "published_at": top_comment.get("publishedAt", ""),
                        "is_reply": False,
                    }
                )

                if include_replies:
                    for reply in thread.get("replies", {}).get("comments", []):
                        reply_id = reply.get("id", "")
                        if reply_id in seen_comment_ids:
                            continue
                        seen_comment_ids.add(reply_id)

                        reply_snippet = reply.get("snippet", {})
                        comments.append(
                            {
                                "comment_id": reply_id,
                                "author_display_name": reply_snippet.get("authorDisplayName", ""),
                                "author_profile_image_url": reply_snippet.get("authorProfileImageUrl", ""),
                                "text_display": reply_snippet.get("textOriginal", ""),
                                "like_count": int(reply_snippet.get("likeCount", 0)),
                                "published_at": reply_snippet.get("publishedAt", ""),
                                "is_reply": True,
                            }
                        )

            next_token = body.get("nextPageToken")
            if next_token:
                continue

            if not fallback_order_tried and current_order != "time" and len(comments) < max_results:
                current_order = "time"
                next_token = None
                fallback_order_tried = True
                continue

            break

    return {
        "video_id": video_id,
        "comments": comments[:max_results],
        "total_fetched": len(comments[:max_results]),
        "next_page_token": next_token,
        "has_more": next_token is not None and len(comments) >= max_results,
    }
