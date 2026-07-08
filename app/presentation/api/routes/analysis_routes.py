from fastapi import APIRouter, HTTPException

from app.application.services.text_validation_service import TextValidationService
from app.application.use_cases.analyze_bulk_records_use_case import AnalyzeBulkRecordsUseCase
from app.application.use_cases.analyze_single_record_use_case import AnalyzeSingleRecordUseCase
from app.domain.entities.analysis_result import AnalysisResult
from app.domain.entities.text_record import TextRecord
from app.infrastructure.ml.fake_sentiment_analyzer import FakeSentimentAnalyzer
from app.infrastructure.repositories.in_memory_analysis_repository import InMemoryAnalysisRepository
from app.presentation.schemas.analysis_schema import (
    AnalyzeRequest,
    AnalyzeResponse,
    BulkAnalyzeRequest,
    BulkAnalyzeResponse,
)


router = APIRouter(prefix="/api", tags=["Analysis"])


validator = TextValidationService()
sentiment_analyzer = FakeSentimentAnalyzer()
repository = InMemoryAnalysisRepository()

analyze_single_use_case = AnalyzeSingleRecordUseCase(
    validator=validator,
    sentiment_analyzer=sentiment_analyzer,
    repository=repository
)

analyze_bulk_use_case = AnalyzeBulkRecordsUseCase(
    validator=validator,
    sentiment_analyzer=sentiment_analyzer,
    repository=repository
)


def to_response(result: AnalysisResult) -> AnalyzeResponse:
    return AnalyzeResponse(
        id=result.record_id,
        text=result.text,
        valid=result.is_valid,
        errors=result.errors,
        sentiment=result.sentiment.value if result.sentiment else None
    )


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_record(request: AnalyzeRequest) -> AnalyzeResponse:
    record = TextRecord(
        record_id=request.id,
        text=request.text
    )

    result = analyze_single_use_case.execute(record)

    return to_response(result)


@router.post("/analyze/bulk", response_model=BulkAnalyzeResponse)
def analyze_bulk_records(request: BulkAnalyzeRequest) -> BulkAnalyzeResponse:
    records = [
        TextRecord(record_id=item.id, text=item.text)
        for item in request.records
    ]

    result = analyze_bulk_use_case.execute(records)

    return BulkAnalyzeResponse(
        total=result.total,
        valid=result.valid,
        invalid=result.invalid,
        sentiment_summary=result.sentiment_summary,
        results=[to_response(item) for item in result.results]
    )


@router.get("/history", response_model=list[AnalyzeResponse])
def get_history() -> list[AnalyzeResponse]:
    results = repository.get_all()

    return [to_response(result) for result in results]


@router.get("/history/{record_id}", response_model=AnalyzeResponse)
def get_history_by_record_id(record_id: str) -> AnalyzeResponse:
    result = repository.get_by_record_id(record_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis result not found"
        )

    return to_response(result)