# Data Quality and Sentiment System

## Project Overview

This project is a FastAPI backend system for validating customer text records and performing sentiment analysis.

The system checks data quality first. Only valid records are sent to sentiment analysis.

It supports:

- single-record analysis
- bulk analysis up to 5,000 records
- history retrieval
- data quality validation
- duplicate detection
- configurable sentiment model
- simple UI
- automated tests

---

## Main Features

### Data Quality Checks

The system validates:

- missing or invalid record ID
- missing text
- missing source
- minimum text length
- maximum text length
- duplicate record IDs inside a bulk request
- duplicate text inside a bulk request
- duplicate record IDs already stored in history
- duplicate text already stored in history

Invalid records skip sentiment inference.

---

## Sentiment Analysis

Sentiment analysis is abstracted behind a service interface.

The system currently supports:

- fake keyword-based sentiment analyzer
- Hugging Face sentiment analyzer

The active provider is controlled through environment variables.

Example sentiment output:

```json
{
  "label": "positive",
  "confidence": 1.0,
  "model_name": "fake-keyword-sentiment-analyzer"
}
