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
            errors = list(validation_result.errors)

            if validation_result.is_valid:
                errors.extend(self._find_repository_duplicate_errors(record))

            if errors:
                invalid_count += 1

                result = AnalysisResult(
                    record_id=record.record_id,
                    text=record.text,
                    source=record.source,
                    is_valid=False,
                    errors=errors,
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
                source=record.source,
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

        return BulkAnalysisResult(
            total=len(records),
            valid=len(valid_records),
            invalid=invalid_count,
            processing_time_seconds=round(time.perf_counter() - start_time, 4),
            sentiment_summary=sentiment_summary,
            results=final_results
        )

    def _find_repository_duplicate_errors(self, record: TextRecord) -> list[str]:
        errors = []

        record_id = record.record_id.strip()
        text = record.normalized_text().lower()

        if record_id and self.repository.get_by_record_id(record_id) is not None:
            errors.append("Duplicate record ID in history")

        for existing_result in self.repository.get_all():
            if existing_result.text.strip().lower() == text and text != "":
                errors.append("Duplicate text in history")
                break

        return errors