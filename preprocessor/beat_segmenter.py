import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from preprocessor.beat_prompt_builder import build_prompt
from preprocessor.beat_validator import validate_beats
from preprocessor.beat_coverage_validator import validate_coverage
from pathlib import Path

load_dotenv()

client = OpenAI()

MODEL_NAME = os.getenv(
    "LLM_MODEL",
    "gpt-5.5"
)


def segment_beats(paragraphs: list[str]) -> dict:

    developer_prompt, user_prompt = build_prompt(paragraphs)

    response = client.responses.create(
        model=MODEL_NAME,
        instructions=developer_prompt,
        input=user_prompt,
    )

    output_text = response.output_text.strip()

    try:

        beat_json = json.loads(output_text)

        validated = validate_beats(beat_json)

        validated_beats = validated.model_dump()

        validate_coverage(
            original_paragraphs=paragraphs,
            beats=validated_beats
        )
        output_dir = Path("output/intermediate")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "beats.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                validated_beats,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(f"✓ Beats saved to {output_file}")

        return validated_beats

    except json.JSONDecodeError as e:

        raise ValueError(
            f"Model returned invalid JSON:\n\n{output_text}"
        ) from e


if __name__ == "__main__":

    from preprocessor.docx_reader import read_docx
    from preprocessor.script_cleaner import clean_script

    script = read_docx("sample.docx")

    cleaned = clean_script(script)

    beats = segment_beats(
        cleaned["paragraphs"]
    )

    print("=" * 80)
    print("SEGMENTED BEATS")
    print("=" * 80)

    print(
        json.dumps(
            beats,
            indent=4,
            ensure_ascii=False
        )
    )

    print("\n")
    print("=" * 80)
    print("✓ Beat Coverage Validation Passed")
    print("=" * 80)