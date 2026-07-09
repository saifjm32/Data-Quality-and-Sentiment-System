from dataclasses import dataclass

from app.domain.value_objects.sentiment_result import SentimentResult


@dataclass(frozen=True)
class AnalysisResult:
    record_id: str
    text: str
    source: str | None
    is_valid: bool
    errors: list[str]
    sentiment: SentimentResult | None