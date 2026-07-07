from app.application.services.sentiment_analyzer import SentimentAnalyzer
from app.domain.value_objects.sentiment_label import SentimentLabel


class FakeSentimentAnalyzer(SentimentAnalyzer):
    def analyze(self, text: str) -> SentimentLabel:
        normalized_text = text.lower()

        positive_words = ["good", "great", "excellent", "love", "happy", "helpful"]
        negative_words = ["bad", "terrible", "hate", "angry", "poor", "awful"]

        for word in positive_words:
            if word in normalized_text:
                return SentimentLabel.POSITIVE

        for word in negative_words:
            if word in normalized_text:
                return SentimentLabel.NEGATIVE

        return SentimentLabel.NEUTRAL