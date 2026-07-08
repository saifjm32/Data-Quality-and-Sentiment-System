from transformers import pipeline

from app.application.services.sentiment_analyzer import SentimentAnalyzer
from app.domain.value_objects.sentiment_label import SentimentLabel


class HuggingFaceSentimentAnalyzer(SentimentAnalyzer):
    def __init__(self, model_name: str, neutral_threshold: float = 0.70):
        self.model_name = model_name
        self.neutral_threshold = neutral_threshold
        self.classifier = pipeline(
            "sentiment-analysis",
            model=self.model_name
        )

    def analyze(self, text: str) -> SentimentLabel:
        result = self.classifier(text)[0]

        label = result["label"].lower()
        score = float(result["score"])

        if score < self.neutral_threshold:
            return SentimentLabel.NEUTRAL

        if "positive" in label or label == "pos":
            return SentimentLabel.POSITIVE

        if "negative" in label or label == "neg":
            return SentimentLabel.NEGATIVE

        return SentimentLabel.NEUTRAL