"""
chroma_utils.py

Utility functions for creating and loading the ChromaDB collection.
"""

import chromadb
from chromadb.api.models.Collection import Collection

# Location where Chroma stores its database
CHROMA_PATH = "data/processed/chroma"

# Name of the collection
COLLECTION_NAME = "storyboards"


def get_collection() -> Collection:
    """
    Create (if needed) and return the storyboard collection.

    Returns:
        Collection: Chroma collection object.
    """

    # Create/Open persistent database
    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    # Create collection if it doesn't exist
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection