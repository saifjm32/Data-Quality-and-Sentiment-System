from abc import ABC, abstractmethod

from app.domain.value_objects.sentiment_result import SentimentResult


class SentimentAnalyzer(ABC):

    @abstractmethod
    def analyze(self, text: str) -> SentimentResult:
        pass

    def analyze_batch(self, texts: list[str]) -> list[SentimentResult]:
        return [self.analyze(text) for text in texts]