from app.application.services.sentiment_analyzer import SentimentAnalyzer
from app.infrastructure.config.app_config import AppConfig
from app.infrastructure.ml.fake_sentiment_analyzer import FakeSentimentAnalyzer
from app.infrastructure.ml.huggingface_sentiment_analyzer import HuggingFaceSentimentAnalyzer


def create_sentiment_analyzer() -> SentimentAnalyzer:
    provider = AppConfig.SENTIMENT_PROVIDER.lower()

    if provider == "huggingface":
        return HuggingFaceSentimentAnalyzer(
            model_name=AppConfig.SENTIMENT_MODEL,
            neutral_threshold=AppConfig.SENTIMENT_NEUTRAL_THRESHOLD
        )

    return FakeSentimentAnalyzer()