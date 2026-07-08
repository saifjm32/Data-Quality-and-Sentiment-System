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
        validation_results = self.validator.validate_bulk(records)

        analysis_results: list[AnalysisResult] = []

        sentiment_summary = {
            "positive": 0,
            "negative": 0,
            "neutral": 0
        }

        valid_count = 0
        invalid_count = 0

        for record, validation_result in zip(records, validation_results):
            if not validation_result.is_valid:
                invalid_count += 1

                result = AnalysisResult(
                    record_id=record.record_id,
                    text=record.text,
                    is_valid=False,
                    errors=validation_result.errors,
                    sentiment=None
                )

                self.repository.save(result)
                analysis_results.append(result)
                continue

            sentiment = self.sentiment_analyzer.analyze(record.normalized_text())

            valid_count += 1
            sentiment_summary[sentiment.value] += 1

            result = AnalysisResult(
                record_id=record.record_id,
                text=record.normalized_text(),
                is_valid=True,
                errors=[],
                sentiment=sentiment
            )

            self.repository.save(result)
            analysis_results.append(result)

        return BulkAnalysisResult(
            total=len(records),
            valid=valid_count,
            invalid=invalid_count,
            sentiment_summary=sentiment_summary,
            results=analysis_results
        )