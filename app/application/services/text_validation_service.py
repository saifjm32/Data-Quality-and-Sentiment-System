from app.domain.entities.text_record import TextRecord
from app.domain.value_objects.validation_result import ValidationResult


class TextValidationService:
    def __init__(self, min_length: int = 3, max_length: int = 1000):
        self.min_length = min_length
        self.max_length = max_length

    def validate_single(self, record: TextRecord) -> ValidationResult:
        errors = self._validate_basic_rules(record)

        if errors:
            return ValidationResult.invalid(errors)

        return ValidationResult.valid()

    def validate_bulk(self, records: list[TextRecord]) -> list[ValidationResult]:
        results = []
        seen_record_ids = set()
        seen_texts = set()

        for record in records:
            errors = self._validate_basic_rules(record)

            record_id = record.record_id.strip()
            text = record.normalized_text().lower()

            if record_id in seen_record_ids:
                errors.append("Duplicate record ID in bulk request")
            elif record_id != "":
                seen_record_ids.add(record_id)

            if text in seen_texts:
                errors.append("Duplicate text in bulk request")
            elif text != "":
                seen_texts.add(text)

            if errors:
                results.append(ValidationResult.invalid(errors))
            else:
                results.append(ValidationResult.valid())

        return results

    def _validate_basic_rules(self, record: TextRecord) -> list[str]:
        errors = []

        if record.record_id.strip() == "":
            errors.append("Record ID is required")

        if record.normalized_source() == "":
            errors.append("Source is required")

        text = record.normalized_text()

        if text == "":
            errors.append("Text is required")
            return errors

        if len(text) < self.min_length:
            errors.append(f"Text must be at least {self.min_length} characters")

        if len(text) > self.max_length:
            errors.append(f"Text must be at most {self.max_length} characters")

        return errors