"""
embedding.py

Generates vector embeddings using OpenAI's embedding models.
"""

import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        raise RuntimeError(
            "OPENAI_API_KEY not found in environment variables or Streamlit Secrets."
        )

client = OpenAI(api_key=api_key)

# ==========================================================
# Configuration
# ==========================================================

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "text-embedding-3-small"
)

# ==========================================================
# Embedding Generation
# ==========================================================

def get_embedding(text: str) -> list[float]:
    """
    Generate an embedding for a single text.

    Args:
        text:
            Input text.

    Returns:
        Embedding vector.

    Raises:
        RuntimeError:
            If embedding generation fails.
    """

    try:

        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text.strip()
        )

        return response.data[0].embedding

    except Exception as e:

        raise RuntimeError(
            f"Failed to generate embedding: {e}"
        ) from e


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    sample_text = (
        "UMED म्हणजे Unique Mindful Education Development."
    )

    embedding = get_embedding(sample_text)

    print("=" * 80)
    print("EMBEDDING GENERATED")
    print("=" * 80)

    print(f"Dimensions : {len(embedding)}")
    print()

    print("First 10 values:")
    print(embedding[:10])