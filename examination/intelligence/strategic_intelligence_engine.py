import json
from datetime import datetime

from config.paths import (
    STRATEGIC_EVIDENCE_FILE,
    create_project_folders
)

from config.settings import (
    COMPANY_NAME,
    STRATEGIC_QUERIES,
    EVIDENCE_TOP_K
)

from vector_db.faiss_retriever import (
    load_faiss_index,
    load_chunk_metadata,
    load_embedding_model,
    search_faiss
)


def create_evidence_item(result, category, query):
    evidence = {
        "category": category,
        "query_used": query,

        "score": result.get("score"),
        "chunk_id": result.get("chunk_id"),
        "clean_document_id": result.get("clean_document_id"),
        "chunk_number": result.get("chunk_number"),

        "company": result.get("company", ""),
        "source": result.get("source", ""),
        "source_type": result.get("source_type", ""),
        "publisher": result.get("publisher", ""),

        "title": result.get("title", ""),
        "published_at": result.get("published_at", ""),
        "url": result.get("url", ""),

        "evidence_text": result.get("chunk_text", "")
    }

    return evidence


def remove_duplicate_evidence(evidence_items):
    unique_evidence = []
    seen_chunk_ids = set()

    for item in evidence_items:
        chunk_id = item.get("chunk_id")

        if chunk_id in seen_chunk_ids:
            continue

        seen_chunk_ids.add(chunk_id)
        unique_evidence.append(item)

    return unique_evidence


def collect_evidence_for_category(category, queries, index, metadata, model):
    category_evidence = []

    print(f"\nCollecting evidence for category: {category}")

    for query in queries:
        print("Query:", query)

        results = search_faiss(
            query=query,
            index=index,
            metadata=metadata,
            model=model,
            top_k=EVIDENCE_TOP_K
        )

        for result in results:
            evidence_item = create_evidence_item(
                result=result,
                category=category,
                query=query
            )

            category_evidence.append(evidence_item)

    category_evidence = remove_duplicate_evidence(category_evidence)

    print("Evidence found:", len(category_evidence))

    return category_evidence


def create_strategic_evidence():
    print("Loading FAISS index...")
    index = load_faiss_index()

    if index is None:
        print("FAISS index not found. Run build_faiss_index.py first.")
        return None

    print("Loading chunk metadata...")
    metadata = load_chunk_metadata()

    if not metadata:
        print("Chunk metadata not found. Run build_faiss_index.py first.")
        return None

    print("Loading embedding model...")
    model = load_embedding_model()

    strategic_evidence = {
        "company": COMPANY_NAME,
        "generated_at": datetime.now().isoformat(),
        "description": "Evidence collected using FAISS retrieval. No LLM reasoning is used in this file.",
        "categories": {}
    }

    total_evidence_count = 0

    for category, queries in STRATEGIC_QUERIES.items():
        evidence = collect_evidence_for_category(
            category=category,
            queries=queries,
            index=index,
            metadata=metadata,
            model=model
        )

        strategic_evidence["categories"][category] = evidence
        total_evidence_count += len(evidence)

    strategic_evidence["total_evidence_items"] = total_evidence_count

    return strategic_evidence


def save_strategic_evidence(strategic_evidence):
    with open(STRATEGIC_EVIDENCE_FILE, "w", encoding="utf-8") as file:
        json.dump(strategic_evidence, file, indent=4, ensure_ascii=False)


def main():
    create_project_folders()

    strategic_evidence = create_strategic_evidence()

    if strategic_evidence is None:
        return

    save_strategic_evidence(strategic_evidence)

    print("\nStrategic evidence created successfully.")
    print("-------------------------")
    print("Company:", strategic_evidence["company"])
    print("Total evidence items:", strategic_evidence["total_evidence_items"])
    print("Saved to:", STRATEGIC_EVIDENCE_FILE)


if __name__ == "__main__":
    main()