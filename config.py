from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

DATA_DIR = PROJECT_ROOT / "data"

SCRIPTS_DIR = DATA_DIR / "scripts"

APPROVED_STORYBOARDS_DIR = DATA_DIR / "approved_storyboards"

OUTPUT_DIR = PROJECT_ROOT / "output"

CHROMA_DB_DIR = PROJECT_ROOT / "chroma_db"

COLLECTION_NAME = "storyboard_examples"

TOP_K = 3

MODEL_NAME = "gpt-5.5"

TEMPERATURE = 0.3

SUPPORTED_EXTENSIONS = [".docx"]