import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from config.paths import (
    FAISS_INDEX_FILE,
    CHUNK_METADATA_FILE
)

from config.settings import (
    EMBEDDING_MODEL_NAME,
    TOP_K
)


def load_faiss_index():
    if not FAISS_INDEX_FILE.exists():
        print("FAISS index not found:", FAISS_INDEX_FILE)
        return None

    index = faiss.read_index(str(FAISS_INDEX_FILE))
    return index


def load_chunk_metadata():
    if not CHUNK_METADATA_FILE.exists():
        print("Chunk metadata file not found:", CHUNK_METADATA_FILE)
        return []

    with open(CHUNK_METADATA_FILE, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    return metadata


def load_embedding_model():
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return model


def search_faiss(query, index, metadata, model, top_k=TOP_K):
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    query_embedding = query_embedding.astype("float32")

    scores, vector_ids = index.search(query_embedding, top_k)

    results = []

    for score, vector_id in zip(scores[0], vector_ids[0]):
        if vector_id == -1:
            continue

        chunk_data = metadata[vector_id]

        result = {
            "score": float(score),
            "vector_id": int(vector_id),
            "chunk_id": chunk_data.get("chunk_id"),
            "clean_document_id": chunk_data.get("clean_document_id"),
            "chunk_number": chunk_data.get("chunk_number"),

            "company": chunk_data.get("company", ""),
            "source": chunk_data.get("source", ""),
            "source_type": chunk_data.get("source_type", ""),
            "publisher": chunk_data.get("publisher", ""),

            "title": chunk_data.get("title", ""),
            "published_at": chunk_data.get("published_at", ""),
            "url": chunk_data.get("url", ""),

            "chunk_text": chunk_data.get("chunk_text", "")
        }

        results.append(result)

    return results


def print_results(results):
    if not results:
        print("No results found.")
        return

    for index, result in enumerate(results, start=1):
        print("\n" + "=" * 80)
        print("Result:", index)
        print("Score:", result["score"])
        print("Vector ID:", result["vector_id"])
        print("Chunk ID:", result["chunk_id"])
        print("Clean Document ID:", result["clean_document_id"])
        print("Chunk Number:", result["chunk_number"])
        print("Source:", result["source"])
        print("Publisher:", result["publisher"])
        print("Title:", result["title"])
        print("Published At:", result["published_at"])
        print("URL:", result["url"])
        print("\nText Preview:")
        print(result["chunk_text"][:1000])


def main():
    print("Loading FAISS index...")
    index = load_faiss_index()

    if index is None:
        print("Run build_faiss_index.py first.")
        return

    print("Loading chunk metadata...")
    metadata = load_chunk_metadata()

    if not metadata:
        print("Run build_faiss_index.py first.")
        return

    print("Loading embedding model...")
    model = load_embedding_model()

    query = "What are NVIDIA's biggest opportunities in artificial intelligence and data centers?"

    print("\nQuery:", query)

    results = search_faiss(
        query=query,
        index=index,
        metadata=metadata,
        model=model,
        top_k=TOP_K
    )

    print_results(results)


if __name__ == "__main__":
    main()