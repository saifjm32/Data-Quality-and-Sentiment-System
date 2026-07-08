from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.infrastructure.config.app_config import AppConfig


def create_qdrant_collection() -> None:
    client = QdrantClient(
        url=AppConfig.QDRANT_URL,
        api_key=AppConfig.QDRANT_API_KEY
    )

    collection_name = AppConfig.QDRANT_COLLECTION_NAME

    if client.collection_exists(collection_name):
        print(f"Collection already exists: {collection_name}")
        return

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=AppConfig.QDRANT_VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )

    print(f"Collection created: {collection_name}")


if __name__ == "__main__":
    create_qdrant_collection()