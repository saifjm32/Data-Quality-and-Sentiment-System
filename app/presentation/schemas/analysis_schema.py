from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    id: str
    text: str


class AnalyzeResponse(BaseModel):
    id: str
    text: str
    valid: bool
    errors: list[str]
    sentiment: str | None


class BulkAnalyzeRequest(BaseModel):
    records: list[AnalyzeRequest]


class BulkAnalyzeResponse(BaseModel):
    total: int
    valid: int
    invalid: int
    sentiment_summary: dict[str, int]
    results: list[AnalyzeResponse]