import re


def clean_script(script_data: dict) -> dict:

    cleaned_paragraphs = []

    for paragraph in script_data["paragraphs"]:

        paragraph = paragraph.strip()

        paragraph = re.sub(r"[ \t]+", " ", paragraph)

        paragraph = re.sub(r"\n+", "\n", paragraph)

        if paragraph:
            cleaned_paragraphs.append(paragraph)

    cleaned_text = "\n".join(cleaned_paragraphs)

    return {
        **script_data,
        "paragraphs": cleaned_paragraphs,
        "text": cleaned_text,
    }


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