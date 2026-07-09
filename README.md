# Data Quality and Sentiment System

A FastAPI backend system for validating customer text records and performing sentiment analysis.

The system follows a data-quality-first pipeline: each record is validated before sentiment inference. Invalid records are returned with validation errors and do not run through the sentiment analyzer.

## Features

- Analyze a single customer text record
- Analyze bulk records up to 5,000 records per request
- Validate data quality before sentiment analysis
- Detect duplicate record IDs and duplicate text
- Skip sentiment inference for invalid records
- Store and retrieve analysis history
- Switch sentiment provider using environment variables
- Use a fake keyword-based analyzer for fast local testing
- Use a Hugging Face analyzer for real model inference
- Simple browser UI served from `/ui`
- Automated test suite covering validation, API behavior, sentiment, and bulk performance

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- Transformers / Torch for the Hugging Face sentiment provider
- python-dotenv for environment configuration

## Project Structure

```text
Data-Quality-and-Sentiment-System/
├── app/
│   ├── application/
│   │   ├── services/
│   │   └── use_cases/
│   ├── domain/
│   │   ├── entities/
│   │   ├── repositories/
│   │   └── value_objects/
│   ├── infrastructure/
│   │   ├── config/
│   │   ├── ml/
│   │   └── repositories/
│   ├── presentation/
│   │   ├── api/
│   │   └── schemas/
│   └── main.py
├── docs/
├── tests/
├── ui/
├── .env.example
├── requirements.txt
└── README.md
```

## How the System Works

```text
Client request
   ↓
FastAPI route
   ↓
Pydantic request schema
   ↓
Use case
   ↓
Text validation service
   ↓
If invalid: return errors and skip sentiment
If valid: run sentiment analyzer
   ↓
Save result in repository
   ↓
Return API response
```

## Validation Rules

Each record is checked for:

- Missing or empty record ID
- Missing or empty text
- Missing or empty source
- Text shorter than the configured minimum length
- Text longer than the configured maximum length
- Duplicate record IDs inside the same bulk request
- Duplicate text inside the same bulk request
- Duplicate record IDs already saved in history
- Duplicate text already saved in history

Invalid records are still returned in the response, but their `sentiment` field is `null`.

## Sentiment Providers

The sentiment analyzer is abstracted behind a service interface. The active provider is selected through environment variables.

Supported providers:

| Provider | Purpose |
|---|---|
| `fake` | Fast local testing using keyword-based rules |
| `huggingface` | Real sentiment inference using a Hugging Face model |

Example sentiment output:

```json
{
  "label": "positive",
  "confidence": 1.0,
  "model_name": "fake-keyword-sentiment-analyzer"
}
```

## Setup

Clone the repository:

```bash
git clone https://github.com/saifjm32/Data-Quality-and-Sentiment-System.git
cd Data-Quality-and-Sentiment-System
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your local environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

## Environment Variables

Example `.env` configuration:

```env
SENTIMENT_PROVIDER=fake
SENTIMENT_MODEL=distilbert-base-uncased-finetuned-sst-2-english
SENTIMENT_NEUTRAL_THRESHOLD=0.70
SENTIMENT_BATCH_SIZE=32
BULK_INCLUDE_RESULTS_DEFAULT=false
MIN_TEXT_LENGTH=3
MAX_TEXT_LENGTH=1000
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
QDRANT_COLLECTION_NAME=feedback_analysis
QDRANT_VECTOR_SIZE=384
```

For local testing and demos, use:

```env
SENTIMENT_PROVIDER=fake
```

For Hugging Face inference, use:

```env
SENTIMENT_PROVIDER=huggingface
```

## Running the Application

Run the API server:

```bash
uvicorn app.main:app --reload
```

Open these URLs:

| URL | Purpose |
|---|---|
| `http://127.0.0.1:8000/` | Root health message |
| `http://127.0.0.1:8000/health` | Health check |
| `http://127.0.0.1:8000/docs` | Interactive Swagger API docs |
| `http://127.0.0.1:8000/ui/` | Simple browser UI |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root API message |
| `GET` | `/health` | Health check |
| `POST` | `/records/analyze` | Analyze one record |
| `POST` | `/records/analyze/bulk` | Analyze multiple records |
| `GET` | `/records` | Retrieve all saved analysis results |
| `GET` | `/records/{record_id}` | Retrieve one saved analysis result by ID |

## Single Record Example

Request:

```bash
curl -X POST "http://127.0.0.1:8000/records/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "record-1",
    "text": "Great service and fast support",
    "source": "survey"
  }'
```

Response:

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

## Bulk Analysis Example

Request:

```bash
curl -X POST "http://127.0.0.1:8000/records/analyze/bulk" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

Response:

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

To include full per-record results in a bulk response:

```text
POST /records/analyze/bulk?include_results=true
```

## Running Tests

Run the full test suite:

```bash
pytest
```

Or on Windows:

```powershell
py -m pytest
```

The tests cover:

- Single-record API behavior
- Bulk API behavior
- Validation rules
- Duplicate detection
- Sentiment analyzer behavior
- 5,000-record bulk processing
- History retrieval

## Documentation

Additional documentation is available in the `docs/` folder:

- `docs/SETUP_AND_RUN.md`
- `docs/API.md`
- `docs/ARCHITECTURE.md`
- `docs/VALIDATION_RULES.md`
- `docs/TESTING.md`
- `docs/REVIEWER_GUIDE.md`

## Notes

This project is designed as a backend evaluation project. The most important design decision is that validation is performed before sentiment analysis, so the system avoids running inference on bad data.
