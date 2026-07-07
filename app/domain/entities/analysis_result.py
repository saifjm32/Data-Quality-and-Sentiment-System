from dataclasses import dataclass

from app.domain.value_objects.sentiment_label import SentimentLabel


@dataclass(frozen=True)
class AnalysisResult:
    record_id: str
    text: str
    is_valid: bool
    errors: list[str]
    sentiment: SentimentLabel | None