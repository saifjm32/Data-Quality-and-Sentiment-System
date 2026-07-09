# Setup and Run Guide

This guide explains how to install, configure, and run the Data Quality and Sentiment System locally.

## 1. Clone the Repository

```bash
git clone https://github.com/saifjm32/Data-Quality-and-Sentiment-System.git
cd Data-Quality-and-Sentiment-System
```

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it.

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If dependency installation fails because of `httpx2`, replace it with `httpx` in `requirements.txt`, then run the install command again.

## 4. Create the Environment File

Copy the example environment file.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Recommended local demo configuration:

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

## 5. Run the API

```bash
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

## 6. Useful URLs

| URL | Purpose |
|---|---|
| `http://127.0.0.1:8000/` | Root API message |
| `http://127.0.0.1:8000/health` | Health check |
| `http://127.0.0.1:8000/docs` | Swagger/OpenAPI documentation |
| `http://127.0.0.1:8000/ui/` | Simple UI |

## 7. Run Tests

```bash
pytest
```

Windows:

```powershell
py -m pytest
```

## 8. Demo Flow

Use this flow when showing the project:

1. Open `/docs` to show the API documentation.
2. Send a valid single-record request to `/records/analyze`.
3. Send an invalid single-record request with empty text and show that sentiment is skipped.
4. Send a bulk request with valid and invalid records.
5. Open `/records` to show saved history.
6. Open `/ui/` to show the simple frontend.
7. Run `pytest` to show the automated tests passing.
