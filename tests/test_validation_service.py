from app.application.services.text_validation_service import TextValidationService
from app.domain.entities.text_record import TextRecord


def test_valid_record_passes_validation():
    validator = TextValidationService()

    record = TextRecord(
        record_id="1",
        text="Great service",
        source="survey"
    )

    result = validator.validate_single(record)

    assert result.is_valid is True
    assert result.errors == []


def test_empty_text_fails_validation():
    validator = TextValidationService()

    record = TextRecord(
        record_id="1",
        text="",
        source="survey"
    )

    result = validator.validate_single(record)

    assert result.is_valid is False
    assert "Text is required" in result.errors


def test_missing_source_fails_validation():
    validator = TextValidationService()

    record = TextRecord(
        record_id="1",
        text="Great service"
    )

    result = validator.validate_single(record)

    assert result.is_valid is False
    assert "Source is required" in result.errors


def test_missing_record_id_fails_validation():
    validator = TextValidationService()

    record = TextRecord(
        record_id="",
        text="Great service",
        source="survey"
    )

    result = validator.validate_single(record)

    assert result.is_valid is False
    assert "Record ID is required" in result.errors


def test_short_text_fails_validation():
    validator = TextValidationService(min_length=3)

    record = TextRecord(
        record_id="1",
        text="ok",
        source="survey"
    )

    result = validator.validate_single(record)

    assert result.is_valid is False
    assert "Text must be at least 3 characters" in result.errors


def test_long_text_fails_validation():
    validator = TextValidationService(max_length=10)

    record = TextRecord(
        record_id="1",
        text="This text is definitely too long",
        source="survey"
    )

    result = validator.validate_single(record)

    assert result.is_valid is False
    assert "Text must be at most 10 characters" in result.errors


def test_duplicate_record_id_fails_bulk_validation():
    validator = TextValidationService()

    records = [
        TextRecord(
            record_id="1",
            text="Great service one",
            source="survey"
        ),
        TextRecord(
            record_id="1",
            text="Another message",
            source="survey"
        ),
    ]

    results = validator.validate_bulk(records)

    assert results[0].is_valid is True
    assert results[1].is_valid is False
    assert "Duplicate record ID in bulk request" in results[1].errors


def test_duplicate_text_fails_bulk_validation():
    validator = TextValidationService()

    records = [
        TextRecord(
            record_id="1",
            text="Great service",
            source="survey"
        ),
        TextRecord(
            record_id="2",
            text="Great service",
            source="support"
        ),
    ]

    results = validator.validate_bulk(records)

    assert results[0].is_valid is True
    assert results[1].is_valid is False
    assert "Duplicate text in bulk request" in results[1].errors