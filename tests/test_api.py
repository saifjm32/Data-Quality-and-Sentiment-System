from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_endpoint_valid_record():
    response = client.post(
        "/records/analyze",
        json={
            "id": "test-1",
            "text": "Great service"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "test-1"
    assert data["valid"] is True
    assert data["errors"] == []
    assert data["sentiment"]["label"] == "positive"
    assert data["sentiment"]["confidence"] == 1.0
    assert data["sentiment"]["model_name"] == "fake-keyword-sentiment-analyzer"


def test_analyze_endpoint_invalid_record():
    response = client.post(
        "/records/analyze",
        json={
            "id": "test-2",
            "text": ""
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "test-2"
    assert data["valid"] is False
    assert "Text is required" in data["errors"]
    assert data["sentiment"] is None


def test_bulk_analyze_endpoint_summary_without_full_results():
    response = client.post(
        "/records/analyze/bulk",
        json={
            "records": [
                {
                    "id": "bulk-1",
                    "text": "Great service"
                },
                {
                    "id": "bulk-2",
                    "text": "This is terrible"
                },
                {
                    "id": "bulk-3",
                    "text": ""
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
    assert data["invalid_records"][0]["id"] == "bulk-3"
    assert data["results"] is None


def test_bulk_analyze_endpoint_can_include_full_results():
    response = client.post(
        "/records/analyze/bulk?include_results=true",
        json={
            "records": [
                {
                    "id": "bulk-full-1",
                    "text": "Great service"
                },
                {
                    "id": "bulk-full-2",
                    "text": "This is terrible"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert data["valid"] == 2
    assert data["invalid"] == 0
    assert len(data["results"]) == 2
    assert data["results"][0]["sentiment"]["label"] == "positive"
    assert data["results"][1]["sentiment"]["label"] == "negative"


def test_get_records_endpoint():
    response = client.get("/records")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_record_by_id_endpoint():
    client.post(
        "/records/analyze",
        json={
            "id": "history-test-1",
            "text": "Great service"
        }
    )

    response = client.get("/records/history-test-1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "history-test-1"
    assert data["valid"] is True
    assert data["sentiment"]["label"] == "positive"


def test_get_record_by_id_not_found():
    response = client.get("/records/does-not-exist")

    assert response.status_code == 404
    assert response.json()["detail"] == "Analysis result not found"