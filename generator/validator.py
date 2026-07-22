"""
validator.py

Validates storyboard JSON returned by the LLM.
"""

import json
from pydantic import ValidationError

from schemas.storyboard_schema import Storyboard


def validate_storyboard(storyboard: dict) -> Storyboard:
    """
    Validate the generated storyboard.

    Args:
        storyboard:
            Dictionary returned by generate_storyboard()

    Returns:
        Validated Storyboard object.

    Raises:
        ValidationError:
            If the JSON structure does not match the schema.

        ValueError:
            If required fields are empty.
    """

    try:
        validated = Storyboard.model_validate(storyboard)

    except ValidationError as e:
        print("\n" + "=" * 80)
        print("STORYBOARD VALIDATION FAILED")
        print("=" * 80)
        print(e)
        print()
        raise

    # ----------------------------------------------------------
    # Semantic validation
    # ----------------------------------------------------------

    if len(validated.beats) == 0:
        raise ValueError("Storyboard contains no beats.")

    for beat in validated.beats:

        if not beat.beat_id:
            raise ValueError("Beat ID cannot be empty.")

        if not beat.source_text.strip():
            raise ValueError(
                f"Beat {beat.beat_id}: source_text is empty."
            )

        if not beat.visual.strip():
            raise ValueError(
                f"Beat {beat.beat_id}: visual is empty."
            )

        if not beat.ost.strip():
            raise ValueError(
                f"Beat {beat.beat_id}: ost is empty."
            )

        if not beat.dialogue.strip():
            raise ValueError(
                f"Beat {beat.beat_id}: dialogue is empty."
            )

    return validated


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    sample = {
        "beats": [
            {
                "beat_id": "generated_beat_01",
                "source_text": "मेंदूचे तीन भाग आहेत.",
                "visual": "Show a rotating 3D brain.",
                "ost": "मेंदूचे तीन भाग",
                "dialogue": "मेंदूचे तीन भाग आहेत."
            }
        ]
    }

    validated = validate_storyboard(sample)

    print("\n" + "=" * 80)
    print("VALIDATION SUCCESSFUL")
    print("=" * 80)

    print(
        json.dumps(
            validated.model_dump(),
            indent=4,
            ensure_ascii=False
        )
    )

    print("\nFirst Beat Visual:")
    print(validated.beats[0].visual)