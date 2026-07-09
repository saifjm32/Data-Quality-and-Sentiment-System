from dataclasses import dataclass

from app.domain.entities.analysis_result import AnalysisResult


@dataclass(frozen=True)
class BulkAnalysisResult:
    total: int
    valid: int
    invalid: int
    processing_time_seconds: float
    sentiment_summary: dict[str, int]
    results: list[AnalysisResult]