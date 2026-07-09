# Architecture Documentation

## Overview

The system uses a clean architecture style. The main goal is to separate business rules from framework code and infrastructure details.

The application is organized into four main layers:

```text
presentation → application → domain ← infrastructure
```

## Layer Responsibilities

### 1. Presentation Layer

Location:

```text
app/presentation/
```

Responsibilities:

- Defines FastAPI routes
- Defines request and response schemas
- Converts API input into domain entities
- Converts domain results into API responses

Important files:

```text
app/presentation/api/routes/analysis_routes.py
app/presentation/schemas/analysis_schema.py
```

### 2. Application Layer

Location:

```text
app/application/
```

Responsibilities:

- Coordinates use cases
- Applies validation before sentiment analysis
- Calls sentiment analyzer only for valid records
- Saves results through repository interface
- Handles bulk processing and batch sentiment inference

Important files:

```text
app/application/services/text_validation_service.py
app/application/services/sentiment_analyzer.py
app/application/use_cases/analyze_single_record_use_case.py
app/application/use_cases/analyze_bulk_records_use_case.py
```

### 3. Domain Layer

Location:

```text
app/domain/
```

Responsibilities:

- Defines core business entities
- Defines value objects
- Defines repository contracts
- Keeps business concepts independent from FastAPI or external tools

Examples:

```text
TextRecord
AnalysisResult
SentimentResult
ValidationResult
AnalysisRepository
```

### 4. Infrastructure Layer

Location:

```text
app/infrastructure/
```

Responsibilities:

- Reads configuration from environment variables
- Provides concrete sentiment analyzer implementations
- Provides repository implementation
- Creates analyzer instance using a factory

Important files:

```text
app/infrastructure/config/app_config.py
app/infrastructure/ml/sentiment_analyzer_factory.py
app/infrastructure/repositories/in_memory_analysis_repository.py
```

## Request Flow

### Single Record Flow

```text
POST /records/analyze
   ↓
AnalyzeRequest schema
   ↓
TextRecord entity
   ↓
AnalyzeSingleRecordUseCase
   ↓
TextValidationService.validate_single()
   ↓
If invalid:
   create AnalysisResult with errors and sentiment=null
   save result
   return response

If valid:
   run sentiment_analyzer.analyze()
   create AnalysisResult with sentiment
   save result
   return response
```

### Bulk Record Flow

```text
POST /records/analyze/bulk
   ↓
BulkAnalyzeRequest schema
   ↓
List[TextRecord]
   ↓
AnalyzeBulkRecordsUseCase
   ↓
TextValidationService.validate_bulk()
   ↓
Separate valid and invalid records
   ↓
Only valid records are sent to analyze_batch()
   ↓
Build summary counts
   ↓
Save all results
   ↓
Return BulkAnalyzeResponse
```

## Why This Design Is Good

### Validation Is Isolated

All text quality rules are handled by `TextValidationService`. This makes the rules easy to test and change.

### Sentiment Is Abstracted

The application depends on a sentiment analyzer interface instead of depending directly on Hugging Face. This allows the project to switch between fake and real sentiment providers.

### Repository Is Abstracted

The use cases depend on a repository contract. The current implementation stores results in memory, but the design can later support Qdrant, PostgreSQL, SQLite, or another database.

### Bulk Processing Is Efficient

Bulk analysis validates all records first and only sends valid text into sentiment inference. This avoids wasting model calls on invalid data.

## Current Storage Behavior

The project currently uses an in-memory analysis repository. This means history is available while the server is running, but data is reset when the server restarts.

## Extension Ideas

Possible future improvements:

- Add persistent database storage
- Add authentication
- Add pagination for `/records`
- Add CSV upload support
- Add Docker support
- Add CI workflow using GitHub Actions
- Add better frontend styling
- Add structured logging
