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