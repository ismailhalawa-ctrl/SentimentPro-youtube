from app.ai.interfaces.result import AnalysisResult


def normalize_result(result: AnalysisResult) -> AnalysisResult:
    if result.confidence is not None:
        result.confidence = max(0.0, min(1.0, result.confidence))
    if result.processing_time_ms is not None and result.processing_time_ms < 0:
        result.processing_time_ms = None
    if result.data is None:
        result.data = {}
    return result
