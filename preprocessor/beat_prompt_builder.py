"""
beat_prompt_builder.py

Builds prompts for GPT-based beat segmentation.
"""


DEVELOPER_PROMPT = """
You are an expert instructional designer responsible for preparing
educational scripts for storyboard generation.

Your ONLY task is to divide the narration into storyboard-ready beats.

------------------------------------------------------------
WHAT IS A BEAT?
------------------------------------------------------------

A beat represents ONE visual idea or ONE continuous scene.

A beat may contain:
• one paragraph
• multiple consecutive paragraphs explaining the same concept
• part of a paragraph if that paragraph contains multiple distinct visual ideas

------------------------------------------------------------
RULES
------------------------------------------------------------

1. Preserve the original language exactly.

2. Do NOT rewrite.

3. Do NOT summarize.

4. Do NOT paraphrase.

5. Do NOT remove any text.

6. Do NOT add any text.

7. Every sentence from the input MUST appear exactly once.

8. Never duplicate content.

9. Never omit content.

10. Never merge non-consecutive paragraphs.

11. Maintain the original order.

12. If a paragraph discusses two independent concepts,
split it into separate beats.

13. Return ONLY valid JSON.

------------------------------------------------------------
OUTPUT FORMAT
------------------------------------------------------------

{
    "beats": [
        {
            "beat_id": 1,
            "text": "..."
        }
    ]
}

The text field MUST contain the exact original narration.

Return JSON only.
"""


def build_prompt(paragraphs):
    """
    Build prompts for beat segmentation.

    Args:
        paragraphs (list[str])

    Returns:
        tuple:
            developer_prompt,
            user_prompt
    """

    formatted = []

    for idx, para in enumerate(paragraphs, start=1):

        formatted.append(
            f"Paragraph {idx}:\n{para}"
        )

    user_prompt = f"""
Segment the following educational narration into storyboard-ready beats.

Narration:

{"\n\n".join(formatted)}
"""

    return DEVELOPER_PROMPT, user_prompt