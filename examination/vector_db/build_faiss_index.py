import json
import numpy as np
import faiss

from config.paths import (
    EMBEDDINGS_FILE,
    EMBEDDING_METADATA_FILE,
    FAISS_INDEX_FILE,
    CHUNK_METADATA_FILE,
    create_project_folders
)


def load_embeddings(file_path):
    if not file_path.exists():
        print("Embeddings file not found:", file_path)
        return None

    embeddings = np.load(file_path)

    return embeddings


def load_metadata(file_path):
    if not file_path.exists():
        print("Embedding metadata file not found:", file_path)
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    return metadata


def save_chunk_metadata(metadata, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4, ensure_ascii=False)


def build_faiss_index(embeddings):
    embeddings = embeddings.astype("float32")

    embedding_dimension = embeddings.shape[1]

    # Because embeddings are already normalized,
    # IndexFlatIP works like cosine similarity.
    index = faiss.IndexFlatIP(embedding_dimension)

    index.add(embeddings)

    return index


def main():
    create_project_folders()

    print("Loading embeddings from:", EMBEDDINGS_FILE)
    embeddings = load_embeddings(EMBEDDINGS_FILE)

    if embeddings is None:
        print("No embeddings found. Run create_embeddings.py first.")
        return

    print("Loading metadata from:", EMBEDDING_METADATA_FILE)
    metadata = load_metadata(EMBEDDING_METADATA_FILE)

    if not metadata:
        print("No metadata found. Run create_embeddings.py first.")
        return

    if len(embeddings) != len(metadata):
        print("Mismatch found.")
        print("Total embeddings:", len(embeddings))
        print("Total metadata records:", len(metadata))
        return

    print("Building FAISS index...")

    index = build_faiss_index(embeddings)

    faiss.write_index(index, str(FAISS_INDEX_FILE))

    save_chunk_metadata(metadata, CHUNK_METADATA_FILE)

    print("\nFAISS index created successfully.")
    print("-------------------------")
    print("Total vectors indexed:", index.ntotal)
    print("Embedding dimension:", embeddings.shape[1])
    print("FAISS index saved to:", FAISS_INDEX_FILE)
    print("Chunk metadata saved to:", CHUNK_METADATA_FILE)


if __name__ == "__main__":
    main()