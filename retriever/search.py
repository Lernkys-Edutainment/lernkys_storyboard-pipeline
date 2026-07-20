"""
search.py

Search the ChromaDB collection for storyboard examples
similar to a user's script/query.
"""

from retriever.embedding import get_embedding
from retriever.chroma_utils import get_collection

MAX_DISTANCE = 1.2


def search_storyboards(query: str, top_k: int = 5) -> list[dict]:
    """
    Retrieve the most relevant storyboard beats.

    Args:
        query: User script/query.
        top_k: Number of nearest neighbours to retrieve.

    Returns:
        List of storyboard beats sorted by similarity.
    """

    collection = get_collection()

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
        ids, docs, metas, distances
    ):

        # Ignore irrelevant results
        if distance > MAX_DISTANCE:
            continue

        retrieved.append({
            "beat_id": beat_id,
            "source_text": doc,
            "visual": metadata.get("visual", ""),
            "ost": metadata.get("ost", ""),
            "dialogue": metadata.get("dialogue", ""),
            "distance": distance,
        })

    return retrieved


if __name__ == "__main__":

    query = input("Enter script: ")

    retrieved = search_storyboards(query)

    print("\nTop Matches\n")

    if not retrieved:
        print("No relevant storyboard examples found.")
    else:

        for rank, beat in enumerate(retrieved, start=1):

            print("=" * 70)
            print(f"Rank      : {rank}")
            print(f"Beat ID   : {beat['beat_id']}")
            print(f"Distance  : {beat['distance']:.4f}")

            print("\nSource Text:")
            print(beat["source_text"])

            print("\nVisual:")
            print(beat["visual"])

            print("\nOST:")
            print(beat["ost"])

            print("\nDialogue:")
            print(beat["dialogue"])

            print()