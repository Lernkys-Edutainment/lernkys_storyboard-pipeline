"""
prompt_builder.py

Builds the prompts sent to the LLM for generating
a storyboard for a single beat.

Output:
    developer_prompt
    user_prompt
"""

from typing import List, Tuple


# ============================================================
# Developer Prompt
# ============================================================

DEVELOPER_PROMPT = """
You are an expert instructional storyboard designer working at Lernkys Edutainment.

Your responsibility is to convert ONE educational script beat into ONE storyboard beat.

Follow these rules:

- Preserve the meaning of the narration.
- Follow the style of the approved storyboard examples.
- Use the retrieved examples only as references.
- Do NOT copy the retrieved examples.
- Maintain the same language as the input narration.
- Produce a visually engaging storyboard.
- Generate concise and readable OST (On Screen Text).
- Generate natural narration/dialogue.
- Never invent facts.
- Never omit important information.
- Preserve the provided beat_id exactly as it is.
- Return ONLY valid JSON.
- Never return Markdown.
- Never explain your reasoning.
"""


# ============================================================
# Output Schema
# ============================================================

OUTPUT_SCHEMA = """
Return ONLY valid JSON in the following format:

{
    "beat_id": "...",
    "source_text": "...",
    "visual": "...",
    "ost": "...",
    "dialogue": "..."
}
"""


# ============================================================
# Build User Prompt
# ============================================================

def build_user_prompt(
    beat: dict,
    retrieved_examples: List[dict]
) -> str:
    """
    Build the user prompt for a single storyboard beat.

    Args:
        beat:
            Dictionary containing:
                beat_id
                text

        retrieved_examples:
            Similar approved storyboard examples.

    Returns:
        User prompt.
    """

    prompt = ""

    # --------------------------------------------------------
    # Output Format
    # --------------------------------------------------------

    prompt += OUTPUT_SCHEMA
    prompt += "\n\n"

    # --------------------------------------------------------
    # Retrieved Examples
    # --------------------------------------------------------

    if retrieved_examples:

        prompt += (
            "Below are approved storyboard examples.\n"
            "Study their writing style, level of detail, and structure.\n"
            "Use them only as inspiration.\n"
            "Do NOT copy any content.\n\n"
        )

        for idx, example in enumerate(retrieved_examples, start=1):

            prompt += f"""
==================================================
APPROVED EXAMPLE {idx}
==================================================

Source Text:
{example["source_text"]}

Visual:
{example["visual"]}

OST:
{example["ost"]}

Dialogue:
{example["dialogue"]}

"""

    else:

        prompt += """
No similar storyboard examples were retrieved.

Generate the storyboard using your own reasoning while
following the required JSON format.

"""

    # --------------------------------------------------------
    # Current Beat
    # --------------------------------------------------------

    prompt += f"""
==================================================
CURRENT BEAT
==================================================

Beat ID:
{beat["beat_id"]}

Narration:
{beat["text"]}

"""

    # --------------------------------------------------------
    # Final Instructions
    # --------------------------------------------------------

    prompt += """
Generate ONE storyboard beat.

Requirements:

1. Keep the same beat_id.
2. Copy the narration exactly into source_text.
3. Generate a detailed visual.
4. Generate concise OST.
5. Generate natural dialogue.
6. Maintain the same language.
7. Return ONLY valid JSON.
8. Do NOT include explanations.
9. Do NOT include Markdown.
10. Do NOT wrap JSON inside ``` blocks.
"""

    return prompt


# ============================================================
# Public Function
# ============================================================

def build_prompt(
    beat: dict,
    retrieved_examples: List[dict]
) -> Tuple[str, str]:
    """
    Build prompts for GPT.

    Args:
        beat:
            Beat dictionary.

        retrieved_examples:
            Retrieved storyboard examples.

    Returns:
        (developer_prompt, user_prompt)
    """

    developer_prompt = DEVELOPER_PROMPT

    user_prompt = build_user_prompt(
        beat,
        retrieved_examples
    )

    return developer_prompt, user_prompt


# ============================================================
# Testing
# ============================================================

if __name__ == "__main__":

    beat = {
        "beat_id": "beat_001",
        "text": "हिप्पोकॅम्पस नवीन आठवणी तयार करण्यास मदत करतो."
    }

    examples = [
        {
            "source_text": "मेंदूचे तीन भाग आहेत.",
            "visual": "Show a 3D animated brain splitting into three labelled parts.",
            "ost": "मेंदूचे तीन भाग",
            "dialogue": "मेंदूचे तीन भाग आहेत."
        }
    ]

    developer_prompt, user_prompt = build_prompt(
        beat,
        examples
    )

    print("=" * 80)
    print("DEVELOPER PROMPT")
    print("=" * 80)
    print(developer_prompt)

    print()

    print("=" * 80)
    print("USER PROMPT")
    print("=" * 80)
    print(user_prompt)