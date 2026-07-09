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

    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: str | None = os.getenv("QDRANT_API_KEY") or None

    QDRANT_COLLECTION_NAME: str = os.getenv(
        "QDRANT_COLLECTION_NAME",
        "feedback_analysis"
    )

    QDRANT_VECTOR_SIZE: int = int(
        os.getenv("QDRANT_VECTOR_SIZE", "384")
    )
    SENTIMENT_BATCH_SIZE: int = int(os.getenv("SENTIMENT_BATCH_SIZE", "32"))

    BULK_INCLUDE_RESULTS_DEFAULT: bool = (
       os.getenv("BULK_INCLUDE_RESULTS_DEFAULT", "false").lower() == "true"
) 