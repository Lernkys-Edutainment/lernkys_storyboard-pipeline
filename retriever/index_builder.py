"""
index_builder.py

Reads approved storyboard examples, generates embeddings,
and stores them in ChromaDB.
"""

import json
from pathlib import Path

from retriever.embedding import get_embedding
from retriever.chroma_utils import (
    get_collection,
    count_documents,
)

# ==========================================================
# Configuration
# ==========================================================

DATA_PATH = Path("data/processed/gold_examples.jsonl")


# ==========================================================
# Build Chroma Index
# ==========================================================

def build_database() -> None:
    """
    Read approved storyboard examples, generate embeddings,
    and store them in ChromaDB.
    """

    # Load/Create Chroma collection
    collection = get_collection()

    # Prevent accidental duplicate indexing
    if collection.count() > 0:

        print("=" * 80)
        print("COLLECTION ALREADY EXISTS")
        print("=" * 80)

        print(f"Documents already indexed: {collection.count()}")
        print("Delete/reset the collection before rebuilding.")

        return

    print("=" * 80)
    print("BUILDING CHROMA DATABASE")
    print("=" * 80)

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    indexed = 0

    with open(DATA_PATH, "r", encoding="utf-8") as file:

        for line_number, line in enumerate(file, start=1):

            try:

                record = json.loads(line)

            except json.JSONDecodeError:

                print(
                    f"Skipping invalid JSON at line {line_number}."
                )

                continue

            beat_id = str(record["beat_id"])

            source_text = record["source_text"]

            embedding = get_embedding(source_text)

            metadata = {

                "beat_id": beat_id,

                "source_text": source_text,

                "visual": record["visual"],

                "ost": record["ost"],

                "dialogue": record["dialogue"]

            }

            collection.add(

                ids=[beat_id],

                embeddings=[embedding],

                documents=[source_text],

                metadatas=[metadata]

            )

            indexed += 1

            print(
                f"Indexed {indexed} examples...",
                end="\r"
            )

    print("\n")

    print("=" * 80)
    print("INDEXING COMPLETE")
    print("=" * 80)

    print(f"Collection : {collection.name}")
    print(f"Documents  : {count_documents()}")


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    build_database()