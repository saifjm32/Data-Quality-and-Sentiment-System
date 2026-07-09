import time

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_bulk_endpoint_processes_5000_records():
    records = [
        {
            "id": f"bulk-performance-{index}",
            "text": f"Great service number {index}"
        }
        for index in range(5000)
    ]

    start_time = time.perf_counter()

    response = client.post(
        "/records/analyze/bulk",
        json={"records": records}
    )

    elapsed_time = time.perf_counter() - start_time

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 5000
    assert data["valid"] == 5000
    assert data["invalid"] == 0
    assert data["processing_time_seconds"] >= 0
    assert data["sentiment_summary"]["positive"] == 5000
    assert data["invalid_records"] == []
    assert data["results"] is None

    print(f"Processed 5000 records in {elapsed_time:.2f} seconds")