from app.domain.value_objects.sentiment_label import SentimentLabel
from app.infrastructure.ml.fake_sentiment_analyzer import FakeSentimentAnalyzer


def test_fake_analyzer_returns_positive():
    analyzer = FakeSentimentAnalyzer()

    result = analyzer.analyze("Great service")

    assert result.label == SentimentLabel.POSITIVE
    assert result.confidence == 1.0
    assert result.model_name == "fake-keyword-sentiment-analyzer"


def test_fake_analyzer_returns_negative():
    analyzer = FakeSentimentAnalyzer()

    result = analyzer.analyze("This is terrible")

    assert result.label == SentimentLabel.NEGATIVE
    assert result.confidence == 1.0
    assert result.model_name == "fake-keyword-sentiment-analyzer"


def test_fake_analyzer_returns_neutral():
    analyzer = FakeSentimentAnalyzer()

    result = analyzer.analyze("The product arrived yesterday")

    assert result.label == SentimentLabel.NEUTRAL
    assert result.confidence == 0.5
    assert result.model_name == "fake-keyword-sentiment-analyzer"