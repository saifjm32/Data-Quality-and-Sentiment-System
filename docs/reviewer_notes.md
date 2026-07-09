# Reviewer Notes

## Summary

This project implements a Data Quality and Sentiment System using FastAPI and Clean Architecture.

The system validates customer text records before running sentiment analysis.

Invalid records skip sentiment inference.

## Required FastAPI Endpoints

The required endpoints are implemented:

```text
POST /records/analyze
POST /records/analyze/bulk
GET /records
GET /records/{record_id}
```

## Data Quality Features

The system checks:

- missing record ID
- missing text
- missing source
- minimum text length
- maximum text length
- duplicate record IDs inside bulk requests
- duplicate text inside bulk requests
- duplicate record IDs already stored in history
- duplicate text already stored in history

## Sentiment Features

Sentiment output includes:

- label
- confidence
- model name

Example:

```json
{
  "label": "positive",
  "confidence": 1.0,
  "model_name": "fake-keyword-sentiment-analyzer"
}
```

## Bulk Processing

The bulk endpoint supports 5,000 records.

Bulk response includes:

- total records
- valid records
- invalid records
- processing time
- batch size
- sentiment summary
- invalid record details

The endpoint avoids returning huge result payloads by default.

Full results can be requested using:

```text
POST /records/analyze/bulk?include_results=true
```

## Performance

Performance-related features:

- configurable batch size through `.env`
- batch-oriented sentiment processing
- model is not loaded inside routes
- efficient duplicate checks using set/dict-style logic
- processing time included in response

## UI

The simple UI is available at:

```text
http://127.0.0.1:8000/ui/
```

The UI supports:

- single-record analysis
- bulk analysis
- history viewing

## Testing Evidence

Command:

```powershell
py -m pytest
```

Result:

```text
21 passed
```

## GitHub Workflow Evidence

Pull request:

```text
https://github.com/saifjm32/Data-Quality-and-Sentiment-System/pull/2
```

The pull request demonstrates:

- feature branch usage
- meaningful commits
- PR summary
- testing evidence
- reviewer-facing documentation