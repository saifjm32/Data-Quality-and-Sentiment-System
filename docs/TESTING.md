# Testing Documentation

The project includes automated tests using Pytest.

## Run All Tests

```bash
pytest
```

Windows:

```powershell
py -m pytest
```

## Test Files

| File | Purpose |
|---|---|
| `tests/test_validation_service.py` | Tests validation rules and duplicate detection |
| `tests/test_sentiment_analyzer.py` | Tests sentiment analyzer behavior |
| `tests/test_api.py` | Tests API endpoints and response shape |
| `tests/test_bulk_performance.py` | Tests 5,000-record bulk processing |

## What the Tests Prove

The tests prove that:

- Valid records pass validation
- Empty text fails validation
- Missing source fails validation
- Missing record ID fails validation
- Short text fails validation
- Long text fails validation
- Duplicate record IDs fail inside bulk requests
- Duplicate text fails inside bulk requests
- Single-record API returns sentiment for valid records
- Invalid records return errors and skip sentiment
- Bulk API returns correct totals
- Bulk API can return summary only
- Bulk API can include full results with `include_results=true`
- History can be retrieved
- Missing history records return `404`
- The system can process 5,000 bulk records

## Example Test Command Output

```text
21 passed
```

This means Pytest ran 21 tests and all of them passed. No tested behavior failed.

## Bulk Performance Test

The bulk performance test creates 5,000 records and posts them to:

```text
POST /records/analyze/bulk
```

The expected result is:

```json
{
  "total": 5000,
  "valid": 5000,
  "invalid": 0,
  "batch_size": 32,
  "sentiment_summary": {
    "positive": 5000,
    "negative": 0,
    "neutral": 0
  },
  "invalid_records": [],
  "results": null
}
```

## Recommended Testing Before Demo

Before showing the project to a trainer or reviewer, run:

```bash
pytest
```

Then run the API:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Use Swagger UI to manually test:

1. `POST /records/analyze`
2. `POST /records/analyze/bulk`
3. `GET /records`
4. `GET /records/{record_id}`
