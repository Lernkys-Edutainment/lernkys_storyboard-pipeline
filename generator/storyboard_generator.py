"""
storyboard_generator.py

Generates storyboard beats using GPT-5.5.

Input:
    output/intermediate/retrieved_examples.json

Output:
    output/generated/generated_storyboard.json
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from generator.prompt_builder import build_prompt
from generator.validator import validate_storyboard

load_dotenv()

client = OpenAI()

MODEL_NAME = os.getenv(
    "LLM_MODEL",
    "gpt-5.5"
)

INPUT_PATH = Path(
    "output/intermediate/retrieved_examples.json"
)

OUTPUT_PATH = Path(
    "output/generated/generated_storyboard.json"
)


# ==========================================================
# LLM Call
# ==========================================================

def generate_storyboard_beat(
    developer_prompt: str,
    user_prompt: str
) -> dict:
    """
    Generate a storyboard for a single beat.

    Args:
        developer_prompt:
            System instructions.

        user_prompt:
            Prompt containing the beat and retrieved examples.

    Returns:
        Generated storyboard beat as a dictionary.
    """

    response = client.responses.create(
        model=MODEL_NAME,
        instructions=developer_prompt,
        input=user_prompt,
    )

    output_text = response.output_text.strip()

    try:
        return json.loads(output_text)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"Model returned invalid JSON:\n\n{output_text}"
        ) from e


# ==========================================================
# Generate Complete Storyboard
# ==========================================================

def generate_storyboard() -> dict:
    """
    Generate storyboard for all beats.

    Returns:
        Dictionary containing validated storyboard.
    """

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Retrieved examples file not found: {INPUT_PATH}"
        )

    with open(
        INPUT_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        retrieved_data = json.load(file)

    generated_storyboard = {
        "beats": []
    }

    total = len(retrieved_data["beats"])

    print("=" * 80)
    print("GENERATING STORYBOARD")
    print("=" * 80)

    for index, beat in enumerate(
        retrieved_data["beats"],
        start=1
    ):

        developer_prompt, user_prompt = build_prompt(
            beat,
            beat["retrieved_examples"]
        )

        generated_beat = generate_storyboard_beat(
            developer_prompt,
            user_prompt
        )

        generated_storyboard["beats"].append(
            generated_beat
        )

        print(
            f"[{index}/{total}] Generated Beat {generated_beat['beat_id']}"
        )

    # ======================================================
    # Validate the complete storyboard
    # ======================================================

    print("\nValidating generated storyboard...")

    validated_storyboard = validate_storyboard(
        generated_storyboard
    )

    print("✓ Storyboard validation successful")

    # ======================================================
    # Save validated storyboard
    # ======================================================

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            validated_storyboard.model_dump(),
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n")

    print("=" * 80)
    print("STORYBOARD GENERATION COMPLETE")
    print("=" * 80)

    print(f"Saved to:\n{OUTPUT_PATH}")

    return validated_storyboard.model_dump()


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    storyboard = generate_storyboard()

    print("\nGenerated Storyboard Preview:\n")

    print(
        json.dumps(
            storyboard,
            indent=4,
            ensure_ascii=False
        )
    )