from pathlib import Path

from process_script import process_script

INPUT_DOC = Path("data/raw/scripts/Umed_2.1.1_Script.docx")
OUTPUT_DIR = Path("output/Umed_2.1.1_Script")


def main():

    process_script(INPUT_DOC, OUTPUT_DIR)


if __name__ == "__main__":
    main()