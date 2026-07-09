from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def unique_id(prefix: str) -> str:
    return f"{prefix}-{uuid4()}"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_endpoint_valid_record():
    record_id = unique_id("single-valid")

    response = client.post(
        "/records/analyze",
        json={
            "id": record_id,
            "text": f"Great service from customer {record_id}",
            "source": "survey"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == record_id
    assert data["source"] == "survey"
    assert data["valid"] is True
    assert data["errors"] == []
    assert data["sentiment"]["label"] == "positive"
    assert data["sentiment"]["confidence"] == 1.0
    assert data["sentiment"]["model_name"] == "fake-keyword-sentiment-analyzer"


def test_analyze_endpoint_invalid_record_empty_text():
    record_id = unique_id("single-invalid")

    response = client.post(
        "/records/analyze",
        json={
            "id": record_id,
            "text": "",
            "source": "survey"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == record_id
    assert data["source"] == "survey"
    assert data["valid"] is False
    assert "Text is required" in data["errors"]
    assert data["sentiment"] is None


def test_analyze_endpoint_missing_source():
    record_id = unique_id("missing-source")

    response = client.post(
        "/records/analyze",
        json={
            "id": record_id,
            "text": f"Great service from customer {record_id}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == record_id
    assert data["source"] is None
    assert data["valid"] is False
    assert "Source is required" in data["errors"]
    assert data["sentiment"] is None


def test_bulk_analyze_endpoint_summary_without_full_results():
    first_id = unique_id("bulk-summary-1")
    second_id = unique_id("bulk-summary-2")
    third_id = unique_id("bulk-summary-3")

    response = client.post(
        "/records/analyze/bulk",
        json={
            "records": [
                {
                    "id": first_id,
                    "text": f"Great service from bulk record {first_id}",
                    "source": "survey"
                },
                {
                    "id": second_id,
                    "text": f"This is terrible from bulk record {second_id}",
                    "source": "support"
                },
                {
                    "id": third_id,
                    "text": "",
                    "source": "survey"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 3
    assert data["valid"] == 2
    assert data["invalid"] == 1
    assert data["processing_time_seconds"] >= 0
    assert data["sentiment_summary"]["positive"] == 1
    assert data["sentiment_summary"]["negative"] == 1
    assert data["sentiment_summary"]["neutral"] == 0
    assert len(data["invalid_records"]) == 1
    assert data["invalid_records"][0]["id"] == third_id
    assert "Text is required" in data["invalid_records"][0]["errors"]
    assert data["results"] is None


def test_bulk_analyze_endpoint_can_include_full_results():
    first_id = unique_id("bulk-full-1")
    second_id = unique_id("bulk-full-2")

    response = client.post(
        "/records/analyze/bulk?include_results=true",
        json={
            "records": [
                {
                    "id": first_id,
                    "text": f"Great service from full bulk record {first_id}",
                    "source": "survey"
                },
                {
                    "id": second_id,
                    "text": f"This is terrible from full bulk record {second_id}",
                    "source": "support"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert data["valid"] == 2
    assert data["invalid"] == 0
    assert data["processing_time_seconds"] >= 0
    assert data["batch_size"] == 32
    assert data["invalid_records"] == []
    assert len(data["results"]) == 2
    assert data["results"][0]["sentiment"]["label"] == "positive"
    assert data["results"][1]["sentiment"]["label"] == "negative"


def test_get_records_endpoint():
    response = client.get("/records")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_record_by_id_endpoint():
    record_id = unique_id("history-test")

    client.post(
        "/records/analyze",
        json={
            "id": record_id,
            "text": f"Great service from history record {record_id}",
            "source": "survey"
        }
    )

    response = client.get(f"/records/{record_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == record_id
    assert data["source"] == "survey"
    assert data["valid"] is True
    assert data["sentiment"]["label"] == "positive"


def test_get_record_by_id_not_found():
    missing_id = unique_id("does-not-exist")

    response = client.get(f"/records/{missing_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Analysis result not found"