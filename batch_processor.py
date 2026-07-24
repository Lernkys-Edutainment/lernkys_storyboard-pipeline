from pathlib import Path
from config import SCRIPTS_DIR, OUTPUT_DIR
from process_script import process_script


def run_batch():
    """
    Iterate through all DOCX files inside the scripts directory,
    create an output folder for each script, and run the pipeline.
    """
    if not SCRIPTS_DIR.exists():
        print(f"Scripts directory does not exist: {SCRIPTS_DIR}")
        return

    # Locate all DOCX files in the configured SCRIPTS_DIR
    docx_files = sorted(list(SCRIPTS_DIR.glob("*.docx")))

    if not docx_files:
        print(f"No DOCX files found in {SCRIPTS_DIR}")
        return

    print(f"Found {len(docx_files)} scripts in {SCRIPTS_DIR}.")

    for index, script_path in enumerate(docx_files, start=1):
        # Determine the unique output directory: output/<script_name>/
        script_output_dir = OUTPUT_DIR / script_path.stem
        
        print("\n" + "=" * 80)
        print(f"Batch Processing [{index}/{len(docx_files)}]: {script_path.name}")
        print("=" * 80)
        
        try:
            process_script(script_path, script_output_dir)
        except Exception as e:
            print(f"FAILED to process {script_path.name}: {e}")


if __name__ == "__main__":
    run_batch()
