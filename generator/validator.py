"""
validator.py

Validates storyboard JSON returned by the LLM.
"""

from schemas.storyboard_schema import Storyboard
import json 

def validate_storyboard(storyboard: dict) -> Storyboard:
    """
    Validate storyboard JSON.

    Args:
        storyboard:
            Dictionary returned by generate_storyboard()

    Returns:
        Validated Storyboard object.

    Raises:
        ValidationError if the JSON is invalid.
    """

    return Storyboard.model_validate(storyboard)


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

    print(
    json.dumps(
        validated.model_dump(),
        indent=4,
        ensure_ascii=False
    )
)

    print()

    print(validated.beats[0].visual)