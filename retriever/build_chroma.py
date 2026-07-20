"""
build_chroma.py

Reads approved storyboard examples, generates embeddings,
and stores them in ChromaDB.
"""

import json
from pathlib import Path

from retriever.embedding import get_embedding
from retriever.chroma_utils import get_collection

# Path to your JSONL file
DATA_PATH = Path("data/processed/gold_examples.jsonl")


def build_database():

    # Load/Create Chroma collection
    collection = get_collection()

    # Optional: prevent duplicate indexing
    if collection.count() > 0:
        print(f"Collection already contains {collection.count()} records.")
        print("Delete the database first if you want to rebuild.")
        return

    print("Reading dataset...")

    with open(DATA_PATH, "r", encoding="utf-8") as file:

        for line in file:

            record = json.loads(line)

            beat_id = record["beat_id"]
            source_text = record["source_text"]

            embedding = get_embedding(source_text)

            metadata = {
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

    print(f"Successfully indexed {collection.count()} storyboard beats.")


if __name__ == "__main__":
    build_database()