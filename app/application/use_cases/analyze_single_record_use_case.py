from app.application.services.sentiment_analyzer import SentimentAnalyzer
from app.application.services.text_validation_service import TextValidationService
from app.domain.entities.analysis_result import AnalysisResult
from app.domain.entities.text_record import TextRecord
from app.domain.repositories.analysis_repository import AnalysisRepository


class AnalyzeSingleRecordUseCase:
    def __init__(
        self,
        validator: TextValidationService,
        sentiment_analyzer: SentimentAnalyzer,
        repository: AnalysisRepository
    ):
        self.validator = validator
        self.sentiment_analyzer = sentiment_analyzer
        self.repository = repository

    def execute(self, record: TextRecord) -> AnalysisResult:
        validation_result = self.validator.validate_single(record)

        if not validation_result.is_valid:
            result = AnalysisResult(
                record_id=record.record_id,
                text=record.text,
                is_valid=False,
                errors=validation_result.errors,
                sentiment=None
            )

            self.repository.save(result)
            return result

        sentiment = self.sentiment_analyzer.analyze(record.normalized_text())

        result = AnalysisResult(
            record_id=record.record_id,
            text=record.normalized_text(),
            is_valid=True,
            errors=[],
            sentiment=sentiment
        )

        self.repository.save(result)
        return result