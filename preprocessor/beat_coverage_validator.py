import re

def normalize(text: str) -> str:

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def validate_coverage(
    original_paragraphs: list[str],
    beats: dict
) -> bool:

    original_text = "\n".join(original_paragraphs)

    beat_text = "\n".join(
        beat["text"]
        for beat in beats["beats"]
    )

    original_text = normalize(original_text)

    beat_text = normalize(beat_text)

    if original_text != beat_text:

        raise ValueError(
            "\nCoverage validation failed.\n"
            "Narration changed during beat segmentation."
        )

    return True