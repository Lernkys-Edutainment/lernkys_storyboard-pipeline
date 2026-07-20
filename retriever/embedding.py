from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI()

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "text-embedding-3-small" 
)

def get_embedding(text: str) -> list[float]:
    """
    Generate an embedding for a single text.
    """

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text.strip()
    )

    return response.data[0].embedding