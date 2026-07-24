from pathlib import Path

from preprocessor.docx_reader import read_docx
from preprocessor.script_cleaner import clean_script
from preprocessor.beat_segmenter import segment_beats
from retriever.retriever import retrieve_examples
from generator.storyboard_generator import generate_storyboard
from generator.validator import validate_storyboard
from renderer.docx_renderer import render_storyboard


def process_script(input_doc: Path, output_dir: Path = None):
    input_doc = Path(input_doc)
    
    if output_dir is None:
        # Backward compatibility mode using original paths
        cleaned_script_path = Path("output/intermediate/cleaned_script.json")
        beats_path = Path("output/intermediate/beats.json")
        retrieved_examples_path = Path("output/intermediate/retrieved_examples.json")
        generated_storyboard_path = Path("output/generated/generated_storyboard.json")
        generated_storyboard_docx = Path("output/generated/generated_storyboard.docx")
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        cleaned_script_path = output_dir / "cleaned_script.json"
        beats_path = output_dir / "beats.json"
        retrieved_examples_path = output_dir / "retrieved_examples.json"
        generated_storyboard_path = output_dir / "generated_storyboard.json"
        generated_storyboard_docx = output_dir / "generated_storyboard.docx"

    print("=" * 80)
    print(f"PROCESSING : {input_doc.name}")
    print("=" * 80)

    print("\n[1/7] Reading script...")

    script = read_docx(input_doc)

    print(f"Loaded: {script['filename']}")
    print(f"Paragraphs: {len(script['paragraphs'])}")

    print("\n[2/7] Cleaning script...")

    cleaned_script = clean_script(script, cleaned_script_path)

    print("OK: Script cleaned")


    print("\n[3/7] Segmenting into beats...")

    beats = segment_beats(
        cleaned_script_path,
        beats_path
    )

    print(f"OK: Generated {len(beats['beats'])} beats")

    print("\n[4/7] Retrieving storyboard examples...")

    retrieved = retrieve_examples(
        beats_path,
        retrieved_examples_path
    )

    print("OK: Retrieval complete")


    print("\n[5/7] Generating storyboard...")

    storyboard = generate_storyboard(
        retrieved_examples_path,
        generated_storyboard_path
    )

    print(
        f"OK: Generated {len(storyboard['beats'])} storyboard beats"
    )


    print("\n[6/7] Validating storyboard...")

    validated = validate_storyboard(storyboard)


    if len(beats["beats"]) != len(validated.beats):
        raise ValueError(
            f"Beat count mismatch.\n"
            f"Segmented: {len(beats['beats'])}\n"
            f"Generated: {len(validated.beats)}"
        )

    print("OK: Storyboard validation successful")

    print("\n[7/7] Rendering storyboard to DOCX...")

    render_storyboard(
        generated_storyboard_path,
        generated_storyboard_docx
    )

    print("OK: Storyboard rendering successful")

    print("\n" + "=" * 80)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 80)

    return validated