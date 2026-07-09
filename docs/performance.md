# Bulk Processing Performance

## Purpose

This document explains the bulk processing capability of the system.

The project requirement is to support bulk analysis for up to 5,000 records. The system includes a test that sends 5,000 records to the bulk endpoint.

## Endpoint Tested

```text
POST /records/analyze/bulk
```

## Expected Behavior

For 5,000 valid records, the response should include:

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

## Why Results Are Omitted by Default

For large bulk requests, returning every individual result can make the response very large. The system therefore returns summary information by default.

To include every record result, use:

```text
POST /records/analyze/bulk?include_results=true
```

## Batch Size

The sentiment batch size is configurable through:

```env
SENTIMENT_BATCH_SIZE=32
```

This allows the system to process valid bulk records in batches instead of one at a time.

## Performance Testing Command

Run:

```bash
pytest tests/test_bulk_performance.py
```

Windows:

```powershell
py -m pytest tests/test_bulk_performance.py
```
