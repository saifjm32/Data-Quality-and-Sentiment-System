from dataclasses import dataclass

from app.domain.value_objects.sentiment_label import SentimentLabel


@dataclass(frozen=True)
class SentimentResult:
    label: SentimentLabel
    confidence: float
    model_name: str