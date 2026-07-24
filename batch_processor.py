from pathlib import Path
from tqdm import tqdm

from config import SCRIPTS_DIR, OUTPUT_DIR
from process_script import process_script


def run_batch():
    if not SCRIPTS_DIR.exists():
        print(f"Scripts directory does not exist: {SCRIPTS_DIR}")
        return

    docx_files = sorted(SCRIPTS_DIR.glob("*.docx"))

    if not docx_files:
        print(f"No DOCX files found in {SCRIPTS_DIR}")
        return

    print(f"\nFound {len(docx_files)} scripts in {SCRIPTS_DIR}.\n")

    progress = tqdm(
        docx_files,
        desc="Processing Modules",
        unit="module"
    )

    for script_path in progress:
        progress.set_postfix(module=script_path.stem)

        script_output_dir = OUTPUT_DIR / script_path.stem

        try:
            process_script(script_path, script_output_dir)

        except Exception as e:
            print(f"\n❌ FAILED to process {script_path.name}")
            print(f"Reason: {e}")

    progress.close()

    print("\n" + "=" * 80)
    print("BATCH PROCESSING COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    run_batch()