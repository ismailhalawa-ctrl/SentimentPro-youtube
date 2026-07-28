from app.ai.interfaces.capability import CAPABILITY_SCOPE, AnalysisMode, Capability, ResultScope
from app.ai.interfaces.result import AnalysisResult
from app.ai.pipelines.analysis_pipeline import run_analysis, run_analysis_batch


async def run_capability(text: str, capability: Capability, mode: AnalysisMode) -> AnalysisResult:
    return await run_analysis(text=text, capability=capability, mode=mode)


async def run_capability_batch(
    texts: list[str], capability: Capability, mode: AnalysisMode, aggregate_stats: dict | None = None
) -> list[AnalysisResult]:
    return await run_analysis_batch(
        texts=texts, capability=capability, mode=mode, aggregate_stats=aggregate_stats
    )


def get_result_scope(capability: Capability) -> ResultScope:
    return CAPABILITY_SCOPE[capability]
