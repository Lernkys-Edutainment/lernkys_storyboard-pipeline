"""
chroma_utils.py

Utility functions for creating and managing the ChromaDB collection.
"""

import os

import chromadb
from chromadb.api.models.Collection import Collection
from dotenv import load_dotenv

load_dotenv()

# ==========================================================
# Configuration
# ==========================================================

CHROMA_PATH = os.getenv(
    "CHROMA_PATH",
    "data/processed/chroma"
)

COLLECTION_NAME = os.getenv(
    "CHROMA_COLLECTION",
    "storyboards"
)

# Ensure the database directory exists
os.makedirs(CHROMA_PATH, exist_ok=True)


# ==========================================================
# Collection
# ==========================================================

def get_collection() -> Collection:
    """
    Create (if needed) and return the Chroma collection.

    Returns:
        Collection:
            Chroma collection object.
    """

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


# ==========================================================
# Utility Functions
# ==========================================================

def count_documents() -> int:
    """
    Return the number of indexed documents.

    Returns:
        int:
            Number of documents stored in the collection.
    """

    collection = get_collection()

    return collection.count()


def reset_collection() -> None:
    """
    Delete and recreate the collection.

    Useful while rebuilding the vector index during development.
    """

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    try:
        client.delete_collection(
            COLLECTION_NAME
        )

        print(f"Deleted collection '{COLLECTION_NAME}'.")

    except Exception:
        print("Collection does not exist. Creating a new one.")

    client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    print(f"Created collection '{COLLECTION_NAME}'.")


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    collection = get_collection()

    print("=" * 80)
    print("CHROMA COLLECTION")
    print("=" * 80)

    print(f"Collection Name : {collection.name}")
    print(f"Documents       : {count_documents()}")