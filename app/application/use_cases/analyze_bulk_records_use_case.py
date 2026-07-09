import time

from app.application.services.sentiment_analyzer import SentimentAnalyzer
from app.application.services.text_validation_service import TextValidationService
from app.domain.entities.analysis_result import AnalysisResult
from app.domain.entities.bulk_analysis_result import BulkAnalysisResult
from app.domain.entities.text_record import TextRecord
from app.domain.repositories.analysis_repository import AnalysisRepository


class AnalyzeBulkRecordsUseCase:
    def __init__(
        self,
        validator: TextValidationService,
        sentiment_analyzer: SentimentAnalyzer,
        repository: AnalysisRepository
    ):
        self.validator = validator
        self.sentiment_analyzer = sentiment_analyzer
        self.repository = repository

    def execute(self, records: list[TextRecord]) -> BulkAnalysisResult:
        start_time = time.perf_counter()

        validation_results = self.validator.validate_bulk(records)

        analysis_results: list[AnalysisResult | None] = [None] * len(records)

        sentiment_summary = {
            "positive": 0,
            "negative": 0,
            "neutral": 0
        }

        valid_records: list[tuple[int, TextRecord]] = []
        invalid_count = 0

        for index, (record, validation_result) in enumerate(
            zip(records, validation_results)
        ):
            if not validation_result.is_valid:
                invalid_count += 1

                result = AnalysisResult(
                    record_id=record.record_id,
                    text=record.text,
                    is_valid=False,
                    errors=validation_result.errors,
                    sentiment=None
                )

                analysis_results[index] = result
                continue

            valid_records.append((index, record))

        valid_texts = [
            record.normalized_text()
            for _, record in valid_records
        ]

        sentiments = self.sentiment_analyzer.analyze_batch(valid_texts)

        for (index, record), sentiment in zip(valid_records, sentiments):
            sentiment_summary[sentiment.label.value] += 1

            result = AnalysisResult(
                record_id=record.record_id,
                text=record.normalized_text(),
                is_valid=True,
                errors=[],
                sentiment=sentiment
            )

            analysis_results[index] = result

        final_results = [
            result for result in analysis_results
            if result is not None
        ]

        for result in final_results:
            self.repository.save(result)

        processing_time_seconds = round(time.perf_counter() - start_time, 4)

        return BulkAnalysisResult(
            total=len(records),
            valid=len(valid_records),
            invalid=invalid_count,
            processing_time_seconds=processing_time_seconds,
            sentiment_summary=sentiment_summary,
            results=final_results
        )