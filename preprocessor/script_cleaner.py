import re
import json
from pathlib import Path


def clean_script(script_data_or_path, output_path: Path = None) -> dict:
    if isinstance(script_data_or_path, (str, Path)):
        path = Path(script_data_or_path)
        if path.suffix == ".docx":
            from preprocessor.docx_reader import read_docx
            script_data = read_docx(path)
        else:
            with open(path, "r", encoding="utf-8") as f:
                script_data = json.load(f)
    else:
        script_data = script_data_or_path

    cleaned_paragraphs = []

    for paragraph in script_data["paragraphs"]:

        paragraph = paragraph.strip()

        paragraph = re.sub(r"[ \t]+", " ", paragraph)

        paragraph = re.sub(r"\n+", "\n", paragraph)

        if paragraph:
            cleaned_paragraphs.append(paragraph)

    cleaned_text = "\n".join(cleaned_paragraphs)

    cleaned_data = {
        **script_data,
        "paragraphs": cleaned_paragraphs,
        "text": cleaned_text,
    }

    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

    return cleaned_data


if __name__ == "__main__":

    from preprocessor.docx_reader import read_docx

    script = read_docx("sample.docx")

    cleaned = clean_script(script)

    print("=" * 60)
    print(f"Original Paragraphs : {len(script['paragraphs'])}")
    print(f"Cleaned Paragraphs  : {len(cleaned['paragraphs'])}")
    print("=" * 60)

    print("\nFirst Paragraph:")
    print(cleaned["paragraphs"][0])

    print("\nLast Paragraph:")
    print(cleaned["paragraphs"][-1])