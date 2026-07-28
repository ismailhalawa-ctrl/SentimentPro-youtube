from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class AssistantCitation(BaseModel):
    job_id: int
    comment_id: int
    text: str
    author: str
    like_count: int


class ToolCallTrace(BaseModel):
    tool: str
    status: Literal["success", "error"]
    arguments: dict[str, Any]
    result_summary: str


class AssistantMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    content: str
    citations_json: list[AssistantCitation]
    tool_calls_json: list[ToolCallTrace]
    created_at: datetime


class AssistantSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str | None
    created_at: datetime
    updated_at: datetime


class AssistantSessionWithMessagesResponse(AssistantSessionResponse):
    messages: list[AssistantMessageResponse]


class SendAssistantMessageRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4_000)
    job_id: int | None = None


class SendAssistantMessageResponse(BaseModel):
    status: Literal["ok", "unavailable", "error", "rate_limited"]
    reason: str | None = None
    message: AssistantMessageResponse | None = None
