"""
main.py

Runs the complete storyboard generation pipeline.
"""

import json
from pathlib import Path

from preprocessor.docx_reader import read_docx
from preprocessor.script_cleaner import clean_script
from preprocessor.beat_segmenter import segment_beats

from retriever.retriever import retrieve_examples

from generator.storyboard_generator import generate_storyboard
from generator.validator import validate_storyboard


INPUT_DOC = Path("sample.docx")


def main():

    print("=" * 80)
    print("STORYBOARD GENERATION PIPELINE")
    print("=" * 80)

    # ------------------------------------------------------
    # Step 1 : Read Script
    # ------------------------------------------------------

    print("\n[1/6] Reading script...")

    script = read_docx(INPUT_DOC)

    print(f"Loaded: {script['filename']}")
    print(f"Paragraphs: {len(script['paragraphs'])}")

    # ------------------------------------------------------
    # Step 2 : Clean Script
    # ------------------------------------------------------

    print("\n[2/6] Cleaning script...")

    cleaned_script = clean_script(script)

    print("✓ Script cleaned")

    # ------------------------------------------------------
    # Step 3 : Beat Segmentation
    # ------------------------------------------------------

    print("\n[3/6] Segmenting into beats...")

    beats = segment_beats(
        cleaned_script["paragraphs"]
    )

    print(f"✓ Generated {len(beats['beats'])} beats")

    # ------------------------------------------------------
    # Step 4 : Retrieve Examples
    # ------------------------------------------------------

    print("\n[4/6] Retrieving storyboard examples...")

    retrieved = retrieve_examples()

    print("✓ Retrieval complete")

    # ------------------------------------------------------
    # Step 5 : Generate Storyboard
    # ------------------------------------------------------

    print("\n[5/6] Generating storyboard...")

    storyboard = generate_storyboard()

    print(
        f"✓ Generated {len(storyboard['beats'])} storyboard beats"
    )

    # ------------------------------------------------------
    # Step 6 : Validate Storyboard
    # ------------------------------------------------------

    print("\n[6/6] Validating storyboard...")

    validated = validate_storyboard(storyboard)

    # ------------------------------------------------------
    # Final sanity check
    # ------------------------------------------------------

    if len(beats["beats"]) != len(validated.beats):
        raise ValueError(
            f"Beat count mismatch.\n"
            f"Segmented: {len(beats['beats'])}\n"
            f"Generated: {len(validated.beats)}"
        )

    print("✓ Storyboard validation successful")

    print("\n" + "=" * 80)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 80)

    print("\nGenerated Storyboard:")
    print("output/generated/generated_storyboard.json")


if __name__ == "__main__":
    main()