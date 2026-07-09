# Reviewer Guide

This guide helps a trainer, evaluator, or reviewer understand the project quickly.

## Project Summary

The Data Quality and Sentiment System is a FastAPI backend that validates customer text records before running sentiment analysis.

The main idea is simple:

```text
Bad data should not be sent to the sentiment model.
```

The system supports single-record analysis, bulk analysis, validation, duplicate detection, configurable sentiment providers, history retrieval, a simple UI, and automated tests.

## Main Evidence to Show

### 1. FastAPI App

Run:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Show the available endpoints:

- `POST /records/analyze`
- `POST /records/analyze/bulk`
- `GET /records`
- `GET /records/{record_id}`
- `GET /health`

### 2. Single Valid Record

Use this request:

```json
{
  "id": "demo-1",
  "text": "Great service and helpful support",
  "source": "survey"
}
```

Expected result:

- `valid` is `true`
- `errors` is empty
- `sentiment` is returned

### 3. Single Invalid Record

Use this request:

```json
{
  "id": "demo-2",
  "text": "",
  "source": "survey"
}
```

Expected result:

- `valid` is `false`
- `errors` contains `Text is required`
- `sentiment` is `null`

Explain that this proves invalid records skip sentiment inference.

### 4. Bulk Analysis

Use this request:

```json
{
  "records": [
    {
      "id": "bulk-demo-1",
      "text": "Great service",
      "source": "survey"
    },
    {
      "id": "bulk-demo-2",
      "text": "This is terrible",
      "source": "support"
    },
    {
      "id": "bulk-demo-3",
      "text": "",
      "source": "survey"
    }
  ]
}
```

Expected result:

- `total` is `3`
- `valid` is `2`
- `invalid` is `1`
- `sentiment_summary` shows positive and negative counts
- `invalid_records` contains the bad record
- `results` is `null` by default

### 5. Full Bulk Results

Use:

```text
POST /records/analyze/bulk?include_results=true
```

Explain that this returns all individual results when needed.

### 6. History Retrieval

Open:

```text
GET /records
```

Then open:

```text
GET /records/{record_id}
```

Explain that analyzed records are saved in the current in-memory repository.

### 7. Simple UI

Open:

```text
http://127.0.0.1:8000/ui/
```

Show that the project has a simple frontend for using the API.

### 8. Tests

Run:

```bash
pytest
```

or:

```powershell
py -m pytest
```

Explain:

```text
21 passed
```

This means all 21 automated tests passed.

## Key Design Decisions

### Data Quality First

The system validates data before sentiment analysis. This prevents bad records from wasting model inference.

### Clean Architecture

The project separates code into:

- Presentation layer
- Application/use-case layer
- Domain layer
- Infrastructure layer

This makes the code easier to test, maintain, and extend.

### Configurable Sentiment Provider

The active sentiment analyzer is selected through environment variables. This allows fast local testing with the fake analyzer and real model inference with Hugging Face.

### Bulk Efficiency

Bulk processing validates all records first, then only sends valid records to the sentiment analyzer in batches.

## Suggested Explanation Script

You can say:

> This project is a FastAPI backend for customer feedback analysis. The important part is that it does not blindly send every record to sentiment analysis. First, it validates record ID, text, source, length rules, duplicate IDs, and duplicate text. If the record is invalid, it returns errors and skips sentiment. If it is valid, it sends the normalized text to the active sentiment analyzer. The analyzer is configurable, so I can use a fake provider for testing or a Hugging Face model for real inference. The system supports single analysis, bulk analysis up to 5,000 records, history retrieval, a simple UI, and automated tests.

## Possible Reviewer Questions

### Why did you use a fake sentiment analyzer?

For fast and deterministic testing. The fake analyzer makes tests reliable because the output is predictable.

### Why also support Hugging Face?

To show that the system can use a real machine learning model when needed.

### Why skip invalid records?

Because sentiment analysis should only run on usable text data. This saves compute and protects the quality of the results.

### Why use clean architecture?

It separates business logic from FastAPI and infrastructure. This makes the code easier to test and easier to extend later.

### What would you improve next?

Possible improvements:

- Persistent database storage
- Authentication
- Pagination
- CSV upload
- Docker setup
- GitHub Actions CI
- Better UI design
