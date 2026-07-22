"""
PDF Reader

Reads an educational PDF and extracts all text along with
basic metadata.

Returns:
{
    "filename": "...",
    "num_pages": ...,
    "text": "..."
}
"""

import fitz
from pathlib import Path


def read_pdf(pdf_path: str) -> dict:
    """
    Extract text and metadata from a PDF.

    Args:
        pdf_path (str): Path to PDF.

    Returns:
        dict
    """

    pdf_path = Path(pdf_path)

    doc = fitz.open(pdf_path)

    pages = []

    for page in doc:
        pages.append(page.get_text())

    text = "\n".join(pages)

    return {
        "filename": pdf_path.name,
        "num_pages": len(doc),
        "text": text
    }


if __name__ == "__main__":

    pdf = read_pdf("sample.pdf")

    print("=" * 50)
    print(pdf["filename"])
    print(pdf["num_pages"])
    print("=" * 50)

    print(pdf["text"][:1500])