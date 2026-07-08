from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_endpoint_valid_record():
    response = client.post(
        "/api/analyze",
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
    assert data["sentiment"] in ["positive", "negative", "neutral"]


def test_analyze_endpoint_invalid_record():
    response = client.post(
        "/api/analyze",
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


def test_bulk_analyze_endpoint():
    response = client.post(
        "/api/analyze/bulk",
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
    assert len(data["results"]) == 3