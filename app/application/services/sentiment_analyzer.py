from abc import ABC, abstractmethod

from app.domain.value_objects.sentiment_label import SentimentLabel


class SentimentAnalyzer(ABC):

    @abstractmethod
    def analyze(self, text: str) -> SentimentLabel:
        pass

    def analyze_batch(self, texts: list[str]) -> list[SentimentLabel]:
        return [self.analyze(text) for text in texts]