from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.ai.interfaces.capability import AnalysisMode, Capability


@dataclass
class AnalysisResult:
    capability: Capability
    provider_id: str
    mode: AnalysisMode
    label: str | None
    confidence: float | None
    processing_time_ms: float | None = None
    data: dict = field(default_factory=dict)
    raw_output: dict | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
