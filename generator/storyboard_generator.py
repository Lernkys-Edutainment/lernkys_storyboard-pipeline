import json
import os
from pathlib import Path
import streamlit as st

from dotenv import load_dotenv
from openai import OpenAI
from tqdm.auto import tqdm

from generator.prompt_builder import build_prompt
from generator.validator import validate_storyboard

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        raise RuntimeError(
            "OPENAI_API_KEY not found in environment variables or Streamlit Secrets."
        )

client = OpenAI(api_key=api_key)

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

def generate_storyboard_beat(
    developer_prompt: str,
    user_prompt: str
) -> dict:

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

def generate_storyboard(
    input_path: Path = INPUT_PATH,
    output_path: Path = OUTPUT_PATH,
    talking_head_plan: dict = None
) -> dict:

    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Retrieved examples file not found: {input_path}"
        )

    with open(
        input_path,
        "r",
        encoding="utf-8"
    ) as file:
        retrieved_data = json.load(file)

    generated_storyboard = {
        "beats": []
    }

    if talking_head_plan is None:
        from planning.talking_head_planner import create_talking_head_plan
        talking_head_plan = create_talking_head_plan(retrieved_data["beats"])

    print("=" * 80)
    print("GENERATING STORYBOARD")
    print("=" * 80)

    for beat in tqdm(
        retrieved_data["beats"],
        desc="Generating Storyboard",
        unit="beat"
    ):
        beat_id = beat.get("beat_id")
        visual_type = talking_head_plan.get(str(beat_id), "Other")

        developer_prompt, user_prompt = build_prompt(
            beat,
            beat["retrieved_examples"],
            visual_type
        )

        generated_beat = generate_storyboard_beat(
            developer_prompt,
            user_prompt
        )

        generated_beat["graphics_type"] = visual_type
        generated_storyboard["beats"].append(
            generated_beat
        )

    print()

    print("Validating generated storyboard...")

    validated_storyboard = validate_storyboard(
        generated_storyboard
    )

    print("OK: Storyboard validation successful")

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            validated_storyboard.model_dump(),
            file,
            indent=4,
            ensure_ascii=False
        )

    print()

    print("=" * 80)
    print("STORYBOARD GENERATION COMPLETE")
    print("=" * 80)

    print(f"Saved to:\n{output_path}")

    return validated_storyboard.model_dump()


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