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
        errors = list(validation_result.errors)

        if validation_result.is_valid:
            errors.extend(self._find_repository_duplicate_errors(record))

        if errors:
            result = AnalysisResult(
                record_id=record.record_id,
                text=record.text,
                source=record.source,
                is_valid=False,
                errors=errors,
                sentiment=None
            )

            self.repository.save(result)
            return result

        sentiment = self.sentiment_analyzer.analyze(record.normalized_text())

        result = AnalysisResult(
            record_id=record.record_id,
            text=record.normalized_text(),
            source=record.source,
            is_valid=True,
            errors=[],
            sentiment=sentiment
        )

        self.repository.save(result)
        return result

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