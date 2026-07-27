from pathlib import Path
from tqdm import tqdm

from process_script import process_script
from utils.folder_picker import select_folder


def run_batch():
    """
    Run the storyboard generation pipeline for all DOCX files
    in a user-selected folder.
    """

    try:
        print("\n📂 Select the folder containing the scripts...\n")
        scripts_dir = select_folder("Select Folder Containing Scripts")

        print("\n📂 Select the folder where generated storyboards will be saved...\n")
        output_dir = select_folder("Select Output Folder")

    except ValueError:
        print("\n❌ Folder selection cancelled.")
        return

    # Find all DOCX files
    docx_files = sorted(scripts_dir.glob("*.docx"))

    if not docx_files:
        print(f"\n❌ No DOCX files found in:\n{scripts_dir}")
        return

    print(f"\n✅ Found {len(docx_files)} script(s) in:\n{scripts_dir}\n")

    progress = tqdm(
        docx_files,
        desc="Processing Modules",
        unit="module"
    )

    for script_path in progress:
        progress.set_postfix(module=script_path.stem)

        # Create a separate output folder for each script
        script_output_dir = output_dir / script_path.stem

        try:
            process_script(script_path, script_output_dir)

        except Exception as e:
            print(f"\n❌ FAILED to process {script_path.name}")
            print(f"Reason: {e}")

    progress.close()

    print("\n" + "=" * 80)
    print("✅ BATCH PROCESSING COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    run_batch()