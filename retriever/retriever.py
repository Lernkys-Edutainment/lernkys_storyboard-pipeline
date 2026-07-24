"""
retrieve.py

Retrieves the most relevant storyboard examples for every
beat generated from the script and saves the results.
"""

import json
from pathlib import Path

from retriever.search import search_storyboards

# ==========================================================
# Configuration
# ==========================================================

BEATS_PATH = Path("output/intermediate/beats.json")

OUTPUT_PATH = Path(
    "output/intermediate/retrieved_examples.json"
)


# ==========================================================
# Retrieval
# ==========================================================

def retrieve_examples(
    beats_path: Path = BEATS_PATH,
    output_path: Path = OUTPUT_PATH,
    top_k: int = 5
) -> dict:
    """
    Retrieve storyboard examples for every beat.

    Args:
        beats_path:
            Path to the beats JSON file.
        output_path:
            Path where retrieval results should be saved.
        top_k:
            Number of storyboard examples to retrieve.

    Returns:
        Dictionary containing retrieved examples for each beat.
    """

    beats_path = Path(beats_path)
    output_path = Path(output_path)

    if not beats_path.exists():

        raise FileNotFoundError(
            f"Beats file not found: {beats_path}"
        )

    with open(
        beats_path,
        "r",
        encoding="utf-8"
    ) as file:

        beats_data = json.load(file)

    retrieved_output = {
        "beats": []
    }

    print("=" * 80)
    print("RETRIEVING STORYBOARD EXAMPLES")
    print("=" * 80)

    total = len(beats_data["beats"])

    for index, beat in enumerate(
        beats_data["beats"],
        start=1
    ):

        beat_id = beat["beat_id"]
        narration = beat["text"]

        examples = search_storyboards(
            narration,
            top_k=top_k
        )

        retrieved_output["beats"].append({

            "beat_id": beat_id,

            "text": narration,

            "retrieved_examples": examples

        })

        print(
            f"[{index}/{total}] Retrieved "
            f"{len(examples)} examples "
            f"for Beat {beat_id}"
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            retrieved_output,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n")

    print("=" * 80)
    print("RETRIEVAL COMPLETE")
    print("=" * 80)

    print(
        f"Saved results to:\n{output_path}"
    )

    return retrieved_output


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    retrieve_examples(BEATS_PATH, OUTPUT_PATH, top_k=5)