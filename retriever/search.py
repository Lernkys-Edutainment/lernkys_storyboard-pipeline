"""
search.py

Search the ChromaDB collection for storyboard examples
similar to a storyboard beat.
"""

from retriever.embedding import get_embedding
from retriever.chroma_utils import get_collection

# ==========================================================
# Configuration
# ==========================================================

MAX_DISTANCE = 1.2


# ==========================================================
# Search
# ==========================================================

def search_storyboards(
    query: str,
    top_k: int = 5
) -> list[dict]:
    """
    Retrieve storyboard examples similar to the given narration.

    Args:
        query:
            Narration/beat to search for.

        top_k:
            Maximum number of examples to retrieve.

    Returns:
        List of retrieved storyboard examples sorted by similarity.
    """

    collection = get_collection()

    if collection.count() == 0:
        raise RuntimeError(
            "Chroma collection is empty. Run index_builder.py first."
        )

    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved = []

    ids = results["ids"][0]
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    for beat_id, doc, metadata, distance in zip(
        ids,
        docs,
        metas,
        distances
    ):

        # Ignore weak matches
        if distance > MAX_DISTANCE:
            continue

        retrieved.append({

            "beat_id": beat_id,

            "source_text": metadata.get(
                "source_text",
                doc
            ),

            "visual": metadata.get(
                "visual",
                ""
            ),

            "ost": metadata.get(
                "ost",
                ""
            ),

            "dialogue": metadata.get(
                "dialogue",
                ""
            ),

            "distance": round(distance, 4),

            "score": round(1 - distance, 4)

        })

    return retrieved


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    print("=" * 80)
    print("STORYBOARD SEARCH")
    print("=" * 80)

    query = input("\nEnter narration:\n\n")

    retrieved = search_storyboards(query)

    if not retrieved:

        print("\nNo relevant storyboard examples found.")

    else:

        print(f"\nRetrieved {len(retrieved)} examples.\n")

        for rank, beat in enumerate(retrieved, start=1):

            print("=" * 80)

            print(f"Rank      : {rank}")
            print(f"Beat ID   : {beat['beat_id']}")
            print(f"Distance  : {beat['distance']}")
            print(f"Score     : {beat['score']}")

            print("\nSource Text")
            print("-" * 40)
            print(beat["source_text"])

            print("\nVisual")
            print("-" * 40)
            print(beat["visual"])

            print("\nOST")
            print("-" * 40)
            print(beat["ost"])

            print("\nDialogue")
            print("-" * 40)
            print(beat["dialogue"])

            print()