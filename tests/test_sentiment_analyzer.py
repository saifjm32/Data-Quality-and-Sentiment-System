from app.domain.value_objects.sentiment_label import SentimentLabel
from app.infrastructure.ml.fake_sentiment_analyzer import FakeSentimentAnalyzer


def test_fake_analyzer_returns_positive():
    analyzer = FakeSentimentAnalyzer()

    result = analyzer.analyze("Great service")

    assert result == SentimentLabel.POSITIVE


def test_fake_analyzer_returns_negative():
    analyzer = FakeSentimentAnalyzer()

    result = analyzer.analyze("This is terrible")

    assert result == SentimentLabel.NEGATIVE


def test_fake_analyzer_returns_neutral():
    analyzer = FakeSentimentAnalyzer()

    result = analyzer.analyze("The product arrived yesterday")

    assert result == SentimentLabel.NEUTRAL