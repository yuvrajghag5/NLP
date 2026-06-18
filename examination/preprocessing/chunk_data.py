import json

from config.paths import (
    CLEAN_DOCUMENTS_FILE,
    CHUNKS_FILE,
    create_project_folders
)

from config.settings import CHUNK_SIZE, CHUNK_OVERLAP


def load_jsonl(file_path):
    documents = []

    if not file_path.exists():
        print("Clean file not found:", file_path)
        return documents

    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                document = json.loads(line)
                documents.append(document)

            except json.JSONDecodeError:
                print(f"Skipping invalid JSON at line {line_number}")

    return documents


def save_jsonl(chunks, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(json.dumps(chunk, ensure_ascii=False) + "\n")


def split_text_into_chunks(text, chunk_size, chunk_overlap):
    words = text.split()

    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)

        if chunk_text.strip():
            chunks.append(chunk_text)

        start = end - chunk_overlap

        if start < 0:
            start = 0

        if start >= len(words):
            break

    return chunks


def create_chunks(clean_documents):
    all_chunks = []
    chunk_id = 1

    for document in clean_documents:
        text = document.get("text", "")

        if not text:
            continue

        document_chunks = split_text_into_chunks(
            text=text,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        for chunk_number, chunk_text in enumerate(document_chunks, start=1):

            chunk = {
                "chunk_id": chunk_id,
                "clean_document_id": document.get("clean_document_id"),
                "chunk_number": chunk_number,

                "company": document.get("company", ""),
                "source": document.get("source", ""),
                "source_type": document.get("source_type", ""),
                "publisher": document.get("publisher", ""),

                "title": document.get("title", ""),
                "published_at": document.get("published_at", ""),
                "url": document.get("url", ""),

                "chunk_text": chunk_text
            }

            all_chunks.append(chunk)
            chunk_id += 1

    return all_chunks


def main():
    create_project_folders()

    print("Loading clean documents from:", CLEAN_DOCUMENTS_FILE)

    clean_documents = load_jsonl(CLEAN_DOCUMENTS_FILE)

    if not clean_documents:
        print("No clean documents found. Run clean_data.py first.")
        return

    chunks = create_chunks(clean_documents)

    save_jsonl(chunks, CHUNKS_FILE)

    print("\nChunking completed.")
    print("-------------------------")
    print("Clean documents:", len(clean_documents))
    print("Total chunks created:", len(chunks))
    print("Chunks saved to:", CHUNKS_FILE)


if __name__ == "__main__":
    main()