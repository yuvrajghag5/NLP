import json
import numpy as np

from sentence_transformers import SentenceTransformer

from config.paths import (
    CHUNKS_FILE,
    EMBEDDINGS_FILE,
    EMBEDDING_METADATA_FILE,
    create_project_folders
)

from config.settings import EMBEDDING_MODEL_NAME


def load_jsonl(file_path):
    chunks = []

    if not file_path.exists():
        print("Chunks file not found:", file_path)
        return chunks

    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                chunk = json.loads(line)
                chunks.append(chunk)

            except json.JSONDecodeError:
                print(f"Skipping invalid JSON at line {line_number}")

    return chunks


def save_metadata(metadata, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4, ensure_ascii=False)


def create_embeddings(chunks):
    texts = []
    metadata = []

    for vector_id, chunk in enumerate(chunks):
        chunk_text = chunk.get("chunk_text", "")

        if not chunk_text:
            continue

        texts.append(chunk_text)

        metadata.append({
            "vector_id": vector_id,
            "chunk_id": chunk.get("chunk_id"),
            "clean_document_id": chunk.get("clean_document_id"),
            "chunk_number": chunk.get("chunk_number"),

            "company": chunk.get("company", ""),
            "source": chunk.get("source", ""),
            "source_type": chunk.get("source_type", ""),
            "publisher": chunk.get("publisher", ""),

            "title": chunk.get("title", ""),
            "published_at": chunk.get("published_at", ""),
            "url": chunk.get("url", ""),

            "chunk_text": chunk_text
        })

    print("Loading embedding model:", EMBEDDING_MODEL_NAME)

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    print("Creating embeddings...")

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings, metadata


def main():
    create_project_folders()

    print("Loading chunks from:", CHUNKS_FILE)

    chunks = load_jsonl(CHUNKS_FILE)

    if not chunks:
        print("No chunks found. Run chunk_data.py first.")
        return

    embeddings, metadata = create_embeddings(chunks)

    np.save(EMBEDDINGS_FILE, embeddings)

    save_metadata(metadata, EMBEDDING_METADATA_FILE)

    print("\nEmbedding creation completed.")
    print("-------------------------")
    print("Total chunks:", len(chunks))
    print("Embedding shape:", embeddings.shape)
    print("Embeddings saved to:", EMBEDDINGS_FILE)
    print("Metadata saved to:", EMBEDDING_METADATA_FILE)


if __name__ == "__main__":
    main()