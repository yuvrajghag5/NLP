from pathlib import Path

# Root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Main folders
DATA_DIR = BASE_DIR / "data"

RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
CHUNKS_DIR = DATA_DIR / "chunks"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
VECTOR_INDEX_DIR = DATA_DIR / "vector_index"
INTELLIGENCE_DIR = DATA_DIR / "intelligence"

# Files
RAW_DOCUMENTS_FILE = RAW_DIR / "collected_documents.jsonl"

CLEAN_DOCUMENTS_FILE = PROCESSED_DIR / "clean_documents.jsonl"

CHUNKS_FILE = CHUNKS_DIR / "chunks.jsonl"

EMBEDDINGS_FILE = EMBEDDINGS_DIR / "chunk_embeddings.npy"
EMBEDDING_METADATA_FILE = EMBEDDINGS_DIR / "embedding_metadata.json"

FAISS_INDEX_FILE = VECTOR_INDEX_DIR / "faiss.index"
CHUNK_METADATA_FILE = VECTOR_INDEX_DIR / "chunk_metadata.json"

STRATEGIC_EVIDENCE_FILE = INTELLIGENCE_DIR / "strategic_evidence.json"
CEO_BRIEFING_FILE = INTELLIGENCE_DIR / "ceo_briefing.json"


def create_project_folders():
    folders = [
        RAW_DIR,
        PROCESSED_DIR,
        CHUNKS_DIR,
        EMBEDDINGS_DIR,
        VECTOR_INDEX_DIR,
        INTELLIGENCE_DIR,
    ]

    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)