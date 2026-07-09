from pydantic import BaseModel


class SentimentResponse(BaseModel):
    label: str
    confidence: float
    model_name: str


class AnalyzeRequest(BaseModel):
    id: str
    text: str


class AnalyzeResponse(BaseModel):
    id: str
    text: str
    valid: bool
    errors: list[str]
    sentiment: SentimentResponse | None


class BulkAnalyzeRequest(BaseModel):
    records: list[AnalyzeRequest]


class BulkAnalyzeResponse(BaseModel):
    total: int
    valid: int
    invalid: int
    processing_time_seconds: float
    sentiment_summary: dict[str, int]
    invalid_records: list[AnalyzeResponse]
    results: list[AnalyzeResponse] | None = None