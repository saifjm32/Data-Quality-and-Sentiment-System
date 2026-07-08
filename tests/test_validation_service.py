from app.application.services.text_validation_service import TextValidationService
from app.domain.entities.text_record import TextRecord


def test_valid_record_passes_validation():
    validator = TextValidationService()

    record = TextRecord(record_id="1", text="Great service")

    result = validator.validate_single(record)

    assert result.is_valid is True
    assert result.errors == []


def test_empty_text_fails_validation():
    validator = TextValidationService()

    record = TextRecord(record_id="1", text="")

    result = validator.validate_single(record)

    assert result.is_valid is False
    assert "Text is required" in result.errors


def test_duplicate_record_id_fails_bulk_validation():
    validator = TextValidationService()

    records = [
        TextRecord(record_id="1", text="Great service"),
        TextRecord(record_id="1", text="Another message"),
    ]

    results = validator.validate_bulk(records)

    assert results[0].is_valid is True
    assert results[1].is_valid is False
    assert "Duplicate record ID" in results[1].errors