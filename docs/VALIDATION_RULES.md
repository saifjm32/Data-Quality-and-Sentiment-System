# Validation Rules

The system validates customer text records before sentiment analysis. This is the main business rule of the project: invalid records must not run through sentiment inference.

## Record Fields

Each record has these fields:

| Field | Type | Required | Description |
|---|---:|---:|---|
| `id` | string | Yes | Unique record identifier |
| `text` | string | Yes | Customer text to analyze |
| `source` | string | Yes | Source of the text, such as `survey`, `support`, or `review` |

## Basic Validation Rules

A record is invalid when:

| Rule | Example Error |
|---|---|
| Record ID is missing or empty | `Record ID is required` |
| Text is missing or empty | `Text is required` |
| Source is missing or empty | `Source is required` |
| Text is shorter than `MIN_TEXT_LENGTH` | `Text must be at least 3 characters` |
| Text is longer than `MAX_TEXT_LENGTH` | `Text must be at most 1000 characters` |

## Bulk Validation Rules

When records are submitted in bulk, the system also checks duplicates inside the same request.

| Rule | Example Error |
|---|---|
| Duplicate record ID in the same bulk request | `Duplicate record ID in bulk request` |
| Duplicate text in the same bulk request | `Duplicate text in bulk request` |

## History Duplicate Rules

The system also checks records already stored in history.

| Rule | Example Error |
|---|---|
| Record ID already exists in history | `Duplicate record ID in history` |
| Text already exists in history | `Duplicate text in history` |

## Invalid Record Behavior

Invalid records are not ignored. They are returned in the API response with:

- `valid: false`
- a list of validation `errors`
- `sentiment: null`

Example:

```json
{
  "id": "bad-1",
  "text": "",
  "source": "survey",
  "valid": false,
  "errors": ["Text is required"],
  "sentiment": null
}
```

## Valid Record Behavior

Valid records are sent to the sentiment analyzer.

Example:

```json
{
  "id": "good-1",
  "text": "Great service",
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

## Configurable Length Rules

The minimum and maximum text lengths are controlled by environment variables:

```env
MIN_TEXT_LENGTH=3
MAX_TEXT_LENGTH=1000
```

This makes the validation rules configurable without changing source code.
