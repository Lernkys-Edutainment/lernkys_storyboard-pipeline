from pathlib import Path

from process_script import process_script

INPUT_DOC = Path("sample.docx")
OUTPUT_DIR = Path("output/sample")


def main():

    process_script(INPUT_DOC, OUTPUT_DIR)


if __name__ == "__main__":
    main()