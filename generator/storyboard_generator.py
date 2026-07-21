"""
storyboard_generator.py

Generates storyboard JSON using GPT-5.5.

Input:
    Developer Prompt
    User Prompt

Output:
    Python dictionary containing storyboard JSON.
"""

import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

MODEL_NAME = os.getenv(
    "LLM_MODEL",
    "gpt-5.5"
)


def generate_storyboard(
    developer_prompt: str,
    user_prompt: str
) -> dict:
    """
    Generate storyboard using GPT.

    Args:
        developer_prompt:
            High-level instructions for the model.

        user_prompt:
            Script + retrieved storyboard examples.

    Returns:
        Python dictionary representing the generated storyboard.

    Raises:
        ValueError:
            If the model does not return valid JSON.
    """

    response = client.responses.create(
        model=MODEL_NAME,
        instructions=developer_prompt,
        input=user_prompt,
    )

    output_text = response.output_text.strip()

    try:
        storyboard = json.loads(output_text)
        return storyboard

    except json.JSONDecodeError as e:
        raise ValueError(
            f"Model returned invalid JSON:\n\n{output_text}"
        ) from e


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    from generator.prompt_builder import build_prompt

    # Dummy retrieved example
    retrieved_examples = [
        {
            "source_text": "मेंदूचे तीन भाग आहेत.",
            "visual": "Show a rotating 3D brain divided into three labelled parts.",
            "ost": "मेंदूचे तीन भाग",
            "dialogue": "मेंदूचे तीन भाग आहेत."
        }
    ]

    script = """
हिप्पोकॅम्पस नवीन आठवणी तयार करण्यास मदत करतो.
"""

    developer_prompt, user_prompt = build_prompt(
        script,
        retrieved_examples
    )

    storyboard = generate_storyboard(
        developer_prompt,
        user_prompt
    )

    print("=" * 80)
    print("GENERATED STORYBOARD")
    print("=" * 80)

    print(
        json.dumps(
            storyboard,
            indent=4,
            ensure_ascii=False
        )
    )