from pathlib import Path
from docx import Document


# Different ways headings may appear
SCRIPT_MARKERS = [
    "script",
    "script -",
    "script:",
]

POST_TEST_MARKERS = [
    "post test",
    "post-test",
    "posttest",
]

PRE_TEST_MARKERS = [
    "pre test",
    "pre-test",
    "pretest",
]


def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())


def read_docx(docx_path: str) -> dict:

    docx_path = Path(docx_path)
    document = Document(docx_path)

    paragraphs = [
        p.text.strip()
        for p in document.paragraphs
        if p.text.strip()
    ]

    has_pretest = False
    has_posttest = False
    has_script_section = False

    extracted_script = []

    collecting = False

    for para in paragraphs:

        normalized = normalize(para)

        if any(marker == normalized for marker in PRE_TEST_MARKERS):
            has_pretest = True

        if any(marker == normalized for marker in SCRIPT_MARKERS):
            has_script_section = True
            collecting = True
            continue

        if any(marker == normalized for marker in POST_TEST_MARKERS):
            has_posttest = True
            collecting = False
            break

        if collecting:
            extracted_script.append(para)

    if not has_script_section:
        extracted_script = paragraphs

    return {
        "filename": docx_path.name,
        "num_paragraphs": len(paragraphs),
        "has_script_section": has_script_section,
        "has_pretest": has_pretest,
        "has_posttest": has_posttest,
        "paragraphs": extracted_script,
        "text": "\n".join(extracted_script),
    }


if __name__ == "__main__":

    script = read_docx("sample.docx")

    print("=" * 60)
    print(f"File               : {script['filename']}")
    print(f"Paragraphs         : {script['num_paragraphs']}")
    print(f"Script Section     : {script['has_script_section']}")
    print(f"Pre Test Found     : {script['has_pretest']}")
    print(f"Post Test Found    : {script['has_posttest']}")
    print(f"Script Paragraphs  : {len(script['paragraphs'])}")
    print("=" * 60)

    print("\nFirst Paragraph:")
    print(script["paragraphs"][0])

    print("\nLast Paragraph:")
    print(script["paragraphs"][-1])
    