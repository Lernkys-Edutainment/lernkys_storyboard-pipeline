"""
main.py

End-to-end storyboard generation pipeline.

Flow:

Script
    ↓
Retrieve Similar Storyboards
    ↓
Build Prompt
    ↓
Generate Storyboard
    ↓
Validate Storyboard
    ↓
Save Output
"""

import json
import os

from retriever.search import search_storyboards
from generator.prompt_builder import build_prompt
from generator.storyboard_generator import generate_storyboard
from generator.validator import validate_storyboard


OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "storyboard.json")


def save_storyboard(storyboard):
    """
    Save validated storyboard as JSON.
    """

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            storyboard.model_dump(),
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nStoryboard saved to: {OUTPUT_FILE}")


def main():

    print("=" * 70)
    print("LERNKYS STORYBOARD GENERATION PIPELINE")
    print("=" * 70)

    script = input("\nEnter script:\n\n")

    if not script.strip():

        print("Script cannot be empty.")
        return

    print("\nSearching similar storyboard examples...")

    retrieved_examples = search_storyboards(script)

    print(f"Retrieved {len(retrieved_examples)} example(s).")

    print("\nBuilding prompt...")

    developer_prompt, user_prompt = build_prompt(
        script,
        retrieved_examples
    )

    print("Generating storyboard...\n")

    storyboard = generate_storyboard(
        developer_prompt,
        user_prompt
    )

    print("Validating storyboard...")

    validated_storyboard = validate_storyboard(
        storyboard
    )

    print("Validation Successful!\n")

    print("=" * 70)
    print("GENERATED STORYBOARD")
    print("=" * 70)

    print(
        json.dumps(
            validated_storyboard.model_dump(),
            indent=4,
            ensure_ascii=False
        )
    )

    save_storyboard(validated_storyboard)


if __name__ == "__main__":
    main()