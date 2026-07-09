from transformers import pipeline

from app.application.services.sentiment_analyzer import SentimentAnalyzer
from app.domain.value_objects.sentiment_label import SentimentLabel
from app.domain.value_objects.sentiment_result import SentimentResult


class HuggingFaceSentimentAnalyzer(SentimentAnalyzer):
    def __init__(self, model_name: str, neutral_threshold: float = 0.70):
        self.model_name = model_name
        self.neutral_threshold = neutral_threshold
        self.classifier = pipeline(
            "sentiment-analysis",
            model=self.model_name
        )

    def analyze(self, text: str) -> SentimentResult:
        return self.analyze_batch([text])[0]

    def analyze_batch(self, texts: list[str]) -> list[SentimentResult]:
        raw_results = self.classifier(texts)

        sentiment_results: list[SentimentResult] = []

        for raw_result in raw_results:
            label = raw_result["label"].lower()
            confidence = float(raw_result["score"])

            if confidence < self.neutral_threshold:
                sentiment_label = SentimentLabel.NEUTRAL
            elif "positive" in label or label == "pos":
                sentiment_label = SentimentLabel.POSITIVE
            elif "negative" in label or label == "neg":
                sentiment_label = SentimentLabel.NEGATIVE
            else:
                sentiment_label = SentimentLabel.NEUTRAL

            sentiment_results.append(
                SentimentResult(
                    label=sentiment_label,
                    confidence=round(confidence, 4),
                    model_name=self.model_name
                )
            )

        return sentiment_results