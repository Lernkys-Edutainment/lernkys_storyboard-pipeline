"""
prompt_builder.py

Builds the prompts sent to the LLM.

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

Your responsibility is to convert educational scripts into high-quality storyboard beats.

Your storyboard should:

- Preserve the meaning of the script.
- Follow the style of approved storyboard examples.
- Produce clear and visually engaging scene descriptions.
- Generate concise and readable OST (On Screen Text).
- Generate natural narration/dialogue.
- Maintain the same language as the input script.
- Never invent facts.
- Never omit important information.
- Return ONLY valid JSON.
- Never return Markdown.
- Never explain your reasoning.
"""


# ============================================================
# JSON Format
# ============================================================

OUTPUT_SCHEMA = """
Return the output in the following JSON format:

{
    "beats": [
        {
            "beat_id": "generated_beat_01",
            "source_text": "...",
            "visual": "...",
            "ost": "...",
            "dialogue": "..."
        }
    ]
}
"""


# ============================================================
# Build User Prompt
# ============================================================

def build_user_prompt(
    script: str,
    retrieved_examples: List[dict]
) -> str:

    prompt = ""

    # ------------------------------
    # Output format
    # ------------------------------

    prompt += OUTPUT_SCHEMA
    prompt += "\n\n"

    # ------------------------------
    # Retrieved Examples
    # ------------------------------

    if retrieved_examples:

        prompt += (
            "Below are approved storyboard examples.\n"
            "Learn their style, structure, and level of detail.\n"
            "Do NOT copy them.\n\n"
        )

        for idx, beat in enumerate(retrieved_examples, start=1):

            prompt += f"""
==================================================
Approved Example {idx}
==================================================

Source Text:
{beat["source_text"]}

Visual:
{beat["visual"]}

OST:
{beat["ost"]}

Dialogue:
{beat["dialogue"]}

"""

    else:

        prompt += """
No similar storyboard examples were retrieved.

Generate the storyboard using your own reasoning while following the required JSON format.

"""

    # ------------------------------
    # New Script
    # ------------------------------

    prompt += f"""

==================================================
NEW SCRIPT
==================================================

{script}

"""

    # ------------------------------
    # Final Instruction
    # ------------------------------

    prompt += """
Generate a storyboard for the above script.

Return ONLY valid JSON.

Do not include explanations.

Do not include markdown.

Do not wrap the JSON inside ``` blocks.
"""

    return prompt


# ============================================================
# Public Function
# ============================================================

def build_prompt(
    script: str,
    retrieved_examples: List[dict]
) -> Tuple[str, str]:

    developer_prompt = DEVELOPER_PROMPT

    user_prompt = build_user_prompt(
        script,
        retrieved_examples
    )

    return developer_prompt, user_prompt


# ============================================================
# Testing
# ============================================================

if __name__ == "__main__":

    examples = [
        {
            "source_text": "मेंदूचे तीन भाग आहेत.",
            "visual": "Show a 3D animated brain splitting into three labelled parts.",
            "ost": "मेंदूचे तीन भाग",
            "dialogue": "मेंदूचे तीन भाग आहेत."
        }
    ]

    script = "हिप्पोकॅम्पस नवीन आठवणी तयार करण्यास मदत करतो."

    developer_prompt, user_prompt = build_prompt(
        script,
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