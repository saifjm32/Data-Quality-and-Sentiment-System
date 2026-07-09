# Qdrant Collection Setup

## Purpose

Qdrant was prepared as an infrastructure option for vector-based storage and future semantic search.

A Qdrant collection can store embedded customer feedback records and related analysis metadata.

## Intended Collection

```text
feedback_analysis
```

## Intended Vector Configuration

```text
Vector size: 384
Distance: Cosine
```

## Environment Variables

```env
QDRANT_URL=http://192.168.2.49:6335
QDRANT_API_KEY=
QDRANT_COLLECTION_NAME=feedback_analysis
QDRANT_VECTOR_SIZE=384
```

## Setup Script

The setup script is located at:

```text
app/infrastructure/repositories/qdrant_collection_setup.py
```

Run command:

```powershell
py -m app.infrastructure.repositories.qdrant_collection_setup
```

## Local Testing Status

The Qdrant dashboard was visible in the browser during development.

However, the Qdrant API endpoint could not be reached from PowerShell/Python during local testing.

The following command timed out:

```powershell
Invoke-WebRequest http://192.168.2.49:6335/collections -TimeoutSec 10
```

Because of this connectivity issue, the collection creation script could not complete in the local environment.

## Manual Collection Creation

When Qdrant connectivity is available, create the collection manually or through the setup script using:

```text
Name: feedback_analysis
Vector size: 384
Distance: Cosine
```

## Future Use

Future work can store analyzed feedback records as Qdrant points with:

- vector embedding
- record ID
- original text
- source
- validation status
- sentiment label
- confidence score
- model name
- validation errors

## Current Project Status

Qdrant setup is documented and prepared, but the main project currently uses an in-memory repository for history.