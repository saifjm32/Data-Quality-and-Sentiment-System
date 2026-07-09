# API Documentation

Base URL for local development:

```text
http://127.0.0.1:8000
```

## Response Model: Sentiment

```json
{
  "label": "positive",
  "confidence": 1.0,
  "model_name": "fake-keyword-sentiment-analyzer"
}
```

`label` can be:

- `positive`
- `negative`
- `neutral`

For invalid records, `sentiment` is `null`.

## GET `/`

Returns a simple API message.

Example response:

```json
{
  "message": "Data Quality and Sentiment System API"
}
```

## GET `/health`

Returns service health status.

Example response:

```json
{
  "status": "ok"
}
```

## POST `/records/analyze`

Analyzes one text record.

### Request Body

```json
{
  "id": "record-1",
  "text": "Great service and fast support",
  "source": "survey"
}
```

### Successful Valid Response

```json
{
  "id": "record-1",
  "text": "Great service and fast support",
  "source": "survey",
  "valid": true,
  "errors": [],
  "sentiment": {
    "label": "positive",
    "confidence": 1.0,
    "model_name": "fake-keyword-sentiment-analyzer"
  }
}
```

### Invalid Response Example

Request:

```json
{
  "id": "record-2",
  "text": "",
  "source": "survey"
}
```

Response:

```json
{
  "id": "record-2",
  "text": "",
  "source": "survey",
  "valid": false,
  "errors": ["Text is required"],
  "sentiment": null
}
```

## POST `/records/analyze/bulk`

Analyzes multiple records in one request.

By default, the endpoint returns summary information and invalid records only. Full results are not returned unless `include_results=true` is passed.

### Request Body

```json
{
  "records": [
    {
      "id": "bulk-1",
      "text": "Great service",
      "source": "survey"
    },
    {
      "id": "bulk-2",
      "text": "This is terrible",
      "source": "support"
    },
    {
      "id": "bulk-3",
      "text": "",
      "source": "survey"
    }
  ]
}
```

### Response

```json
{
  "total": 3,
  "valid": 2,
  "invalid": 1,
  "processing_time_seconds": 0.0012,
  "batch_size": 32,
  "sentiment_summary": {
    "positive": 1,
    "negative": 1,
    "neutral": 0
  },
  "invalid_records": [
    {
      "id": "bulk-3",
      "text": "",
      "source": "survey",
      "valid": false,
      "errors": ["Text is required"],
      "sentiment": null
    }
  ],
  "results": null
}
```

## POST `/records/analyze/bulk?include_results=true`

Returns the summary plus all per-record results.

Use this when the client needs the sentiment output for every valid record.

## GET `/records`

Returns all saved analysis results from the current in-memory history.

Example response:

```json
[
  {
    "id": "record-1",
    "text": "Great service and fast support",
    "source": "survey",
    "valid": true,
    "errors": [],
    "sentiment": {
      "label": "positive",
      "confidence": 1.0,
      "model_name": "fake-keyword-sentiment-analyzer"
    }
  }
]
```

## GET `/records/{record_id}`

Returns one saved analysis result by record ID.

Example:

```text
GET /records/record-1
```

If the record does not exist, the API returns:

```json
{
  "detail": "Analysis result not found"
}
```

with HTTP status code `404`.

## Legacy UI-Compatible Endpoints

The project also includes hidden compatibility routes:

| Method | Endpoint | Equivalent Endpoint |
|---|---|---|
| `POST` | `/api/analyze` | `/records/analyze` |
| `POST` | `/api/analyze/bulk` | `/records/analyze/bulk` |
| `GET` | `/api/history` | `/records` |
| `GET` | `/api/history/{record_id}` | `/records/{record_id}` |

These are excluded from the OpenAPI schema but can be useful for the simple UI.
