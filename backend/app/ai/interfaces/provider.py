from abc import ABC, abstractmethod

from app.ai.interfaces.capability import AnalysisMode, Capability
from app.ai.interfaces.result import AnalysisResult


class AIProvider(ABC):
    provider_id: str
    capability: Capability
    mode: AnalysisMode

    @abstractmethod
    async def run(self, text: str, **kwargs) -> AnalysisResult:
        raise NotImplementedError

    async def run_batch(self, texts: list[str], **kwargs) -> list[AnalysisResult]:
        return [await self.run(text, **kwargs) for text in texts]

    def is_available(self) -> bool:
        return True

    def build_conversation_state(self, system_prompt: str, history: list[dict], question: str) -> object:
        raise NotImplementedError(f"{type(self).__name__} does not support conversational state.")

    async def generate_step(
        self, state: object, force_final: bool = False, excluded_tools: set[str] | None = None
    ) -> dict:
        raise NotImplementedError(f"{type(self).__name__} does not support conversational generation.")

    def append_tool_round(
        self, state: object, tool_calls: list[dict], tool_results: list[dict], raw: object
    ) -> object:
        raise NotImplementedError(f"{type(self).__name__} does not support conversational tool rounds.")
