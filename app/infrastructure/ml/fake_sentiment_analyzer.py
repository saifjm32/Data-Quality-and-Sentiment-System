from app.application.services.sentiment_analyzer import SentimentAnalyzer
from app.domain.value_objects.sentiment_label import SentimentLabel
from app.domain.value_objects.sentiment_result import SentimentResult


class FakeSentimentAnalyzer(SentimentAnalyzer):
    model_name = "fake-keyword-sentiment-analyzer"

    def analyze(self, text: str) -> SentimentResult:
        normalized_text = text.lower()

        positive_words = ["good", "great", "excellent", "love", "happy", "helpful"]
        negative_words = ["bad", "terrible", "hate", "angry", "poor", "awful"]

        for word in positive_words:
            if word in normalized_text:
                return SentimentResult(
                    label=SentimentLabel.POSITIVE,
                    confidence=1.0,
                    model_name=self.model_name
                )

        for word in negative_words:
            if word in normalized_text:
                return SentimentResult(
                    label=SentimentLabel.NEGATIVE,
                    confidence=1.0,
                    model_name=self.model_name
                )

        return SentimentResult(
            label=SentimentLabel.NEUTRAL,
            confidence=0.5,
            model_name=self.model_name
        )