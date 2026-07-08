import os

from dotenv import load_dotenv


load_dotenv()


class AppConfig:
    SENTIMENT_PROVIDER: str = os.getenv("SENTIMENT_PROVIDER", "fake")
    SENTIMENT_MODEL: str = os.getenv(
        "SENTIMENT_MODEL",
        "distilbert-base-uncased-finetuned-sst-2-english"
    )
    SENTIMENT_NEUTRAL_THRESHOLD: float = float(
        os.getenv("SENTIMENT_NEUTRAL_THRESHOLD", "0.70")
    )
    MIN_TEXT_LENGTH: int = int(os.getenv("MIN_TEXT_LENGTH", "3"))
    MAX_TEXT_LENGTH: int = int(os.getenv("MAX_TEXT_LENGTH", "1000"))