from fastapi import APIRouter, HTTPException

from app.application.services.text_validation_service import TextValidationService
from app.application.use_cases.analyze_bulk_records_use_case import AnalyzeBulkRecordsUseCase
from app.application.use_cases.analyze_single_record_use_case import AnalyzeSingleRecordUseCase
from app.domain.entities.analysis_result import AnalysisResult
from app.domain.entities.text_record import TextRecord
from app.infrastructure.config.app_config import AppConfig
from app.infrastructure.ml.sentiment_analyzer_factory import create_sentiment_analyzer
from app.infrastructure.repositories.in_memory_analysis_repository import InMemoryAnalysisRepository
from app.presentation.schemas.analysis_schema import (
    AnalyzeRequest,
    AnalyzeResponse,
    BulkAnalyzeRequest,
    BulkAnalyzeResponse,
    SentimentResponse,
)


router = APIRouter(tags=["Records"])


validator = TextValidationService(
    min_length=AppConfig.MIN_TEXT_LENGTH,
    max_length=AppConfig.MAX_TEXT_LENGTH
)

sentiment_analyzer = create_sentiment_analyzer()
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
    sentiment_response = None
    

    if result.sentiment is not None:
        sentiment_response = SentimentResponse(
            label=result.sentiment.label.value,
            confidence=result.sentiment.confidence,
            model_name=result.sentiment.model_name
        )

    return AnalyzeResponse(
       id=result.record_id,
       text=result.text,
       source=result.source,
       valid=result.is_valid,
       errors=result.errors,
       sentiment=sentiment_response
)
    


@router.post("/records/analyze", response_model=AnalyzeResponse)
@router.post("/api/analyze", response_model=AnalyzeResponse, include_in_schema=False)
async def analyze_record(request: AnalyzeRequest) -> AnalyzeResponse:
    record = TextRecord(
        record_id=request.id,
        text=request.text,
        source=request.source
)
    

    result = analyze_single_use_case.execute(record)

    return to_response(result)


@router.post("/records/analyze/bulk", response_model=BulkAnalyzeResponse)
@router.post(
    "/api/analyze/bulk",
    response_model=BulkAnalyzeResponse,
    include_in_schema=False
)
async def analyze_bulk_records(
    request: BulkAnalyzeRequest,
    include_results: bool = AppConfig.BULK_INCLUDE_RESULTS_DEFAULT
) -> BulkAnalyzeResponse:
    records = [
       TextRecord(
           record_id=item.id,
           text=item.text,
           source=item.source
      )
      for item in request.records
]

    result = analyze_bulk_use_case.execute(records)

    invalid_records = [
        to_response(item)
        for item in result.results
        if not item.is_valid
    ]

    response_results = None

    if include_results:
        response_results = [
            to_response(item)
            for item in result.results
        ]

    return BulkAnalyzeResponse(
        total=result.total,
        valid=result.valid,
        invalid=result.invalid,
        processing_time_seconds=result.processing_time_seconds,
        sentiment_summary=result.sentiment_summary,
        invalid_records=invalid_records,
        results=response_results
    )


@router.get("/records", response_model=list[AnalyzeResponse])
@router.get("/api/history", response_model=list[AnalyzeResponse], include_in_schema=False)
async def get_records() -> list[AnalyzeResponse]:
    results = repository.get_all()

    return [to_response(result) for result in results]


@router.get("/records/{record_id}", response_model=AnalyzeResponse)
@router.get(
    "/api/history/{record_id}",
    response_model=AnalyzeResponse,
    include_in_schema=False
)
async def get_record_by_id(record_id: str) -> AnalyzeResponse:
    result = repository.get_by_record_id(record_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis result not found"
        )

    return to_response(result)