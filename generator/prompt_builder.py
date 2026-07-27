"""
prompt_builder.py

Builds the prompts sent to the LLM for generating
a storyboard for a single beat.

Output:
    developer_prompt
    user_prompt
"""

from typing import List, Tuple

from config import (
    TALKING_HEAD_PERCENTAGE,
    ANIMATION_COMPLEXITY,
    ANIMATION_COMPLEXITY_GUIDELINES,
    CREATIVE_BRIEF,
)


# ============================================================
# Developer Prompt
# ============================================================

DEVELOPER_PROMPT = """
You are an expert instructional storyboard designer working at Lernkys Edutainment.

Your responsibility is to convert ONE educational script beat into ONE storyboard beat.

Follow these rules:

- Preserve the meaning of the narration.
- Learn the structure, tone, and level of detail from the approved storyboard examples.
- Use the retrieved examples only as references.
- Do NOT copy the retrieved examples.
- Maintain the same language as the input narration.
- Produce a visually engaging storyboard.
- Generate concise and readable OST (On Screen Text).
- Every beat MUST contain a non-empty "ost" field.
- If no on-screen text is required, return exactly: "No OST".
- Never return an empty string ("") for the ost field.
- Generate natural narration/dialogue.
- Never invent facts.
- Never omit important information.
- Preserve the provided beat_id exactly as it is.
- Return ONLY valid JSON.
- Never return Markdown.
- Never explain your reasoning.
------------------------------------------------------------
BATCH CONFIGURATION
------------------------------------------------------------

- Carefully follow the Batch Creative Brief provided in the user prompt.
- Treat the Storyboard Requirements as mandatory.
- Maintain continuity with the Previous Context.
- Follow the mandatory VISUAL TYPE specified in the user prompt.
- Follow the specified Animation Complexity.
- Maintain the requested Visual Style.
- Generate visuals suitable for the Target Audience.
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

Rules:
- The "ost" field is mandatory.
- Never return an empty string for "ost".
- If no on-screen text is required, return exactly:
  "ost": "No OST"
"""


def build_batch_creative_brief() -> str:
    """
    Build the batch-level creative brief that will be
    injected into every storyboard generation prompt.
    """

    return f"""
==================================================
BATCH CREATIVE BRIEF
==================================================

Target Audience:
{CREATIVE_BRIEF["target_audience"]}

Visual Style:
{CREATIVE_BRIEF["visual_style"]}

--------------------------------------------------
Previous Context
--------------------------------------------------

{CREATIVE_BRIEF["previous_context"]}

--------------------------------------------------
Storyboard Requirements
--------------------------------------------------

{CREATIVE_BRIEF["storyboard_requirements"]}

--------------------------------------------------
Animation Complexity
--------------------------------------------------

Selected Complexity:
{ANIMATION_COMPLEXITY}

{ANIMATION_COMPLEXITY_GUIDELINES[ANIMATION_COMPLEXITY]}

==================================================
"""

# ============================================================
# Build User Prompt
# ============================================================

def build_user_prompt(
    beat: dict,
    retrieved_examples: List[dict],
    visual_type: str = "Other"
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

    prompt += build_batch_creative_brief()
    prompt += "\n\n"

    prompt += (
        "The following Batch Creative Brief applies to the entire storyboard. " "Treat it as mandatory when generating this storyboard beat.\n\n"
    )
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
    # Visual Type
    # --------------------------------------------------------

    if visual_type == "Talking Head":
        prompt += """==================================================
VISUAL TYPE
==================================================

Talking Head (Mandatory)

Requirements:
• Presenter visible throughout the beat.
• Professional studio background.
• Presenter looks directly into camera.
• Presenter narrates naturally.
• Minimal facial expressions and hand gestures.
• No diagrams.
• No infographics.
• No animations.
• No educational graphics.

"""
    else:
        prompt += """==================================================
VISUAL TYPE
==================================================

Other Visual (Mandatory)

Requirements:
• Do NOT include a presenter.
• Select the most suitable educational visual.

Possible visual styles:
• Animation
• Infographic
• Illustration
• Activity Screen
• Reflection Screen
• Title Screen

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
5. Every beat MUST contain a non-empty "ost" field.
6. If no OST is required, return exactly "No OST".
7. Never return an empty string for ost.
8. Generate natural dialogue.
9. Maintain the same language.
10. Return ONLY valid JSON.
11. Do NOT include explanations.
12. Do NOT include Markdown.
13. Do NOT wrap JSON inside ``` blocks.
14. Follow the Batch Creative Brief provided above.
15. Follow the mandatory VISUAL TYPE specification when deciding whether this beat should include a presenter or another visual style.
16. Follow the specified Animation Complexity while designing the visual.
"""

    return prompt


# ============================================================
# Public Function
# ============================================================

def build_prompt(
    beat: dict,
    retrieved_examples: List[dict],
    visual_type: str = "Other"
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
        retrieved_examples,
        visual_type
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
        examples,
        visual_type="Talking Head"
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