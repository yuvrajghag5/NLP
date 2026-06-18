import json
import re
import html
import hashlib

from config.paths import (
    RAW_DOCUMENTS_FILE,
    CLEAN_DOCUMENTS_FILE,
    create_project_folders
)


def load_jsonl(file_path):
    documents = []

    if not file_path.exists():
        print("Raw file not found:", file_path)
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


def save_jsonl(documents, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for document in documents:
            file.write(json.dumps(document, ensure_ascii=False) + "\n")


def clean_text(text):
    if text is None:
        return ""

    text = str(text)

    # Convert HTML entities like &amp; into normal text
    text = html.unescape(text)

    # Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)

    # Remove NewsAPI-style truncated markers like [+123 chars]
    text = re.sub(r"\[\+\d+\schars\]", " ", text)

    # Remove extra spaces, tabs, and newlines
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def create_duplicate_key(document):
    url = str(document.get("url", "")).strip().lower()
    title = str(document.get("title", "")).strip().lower()
    text = clean_text(document.get("text", "")).lower()

    if url:
        return "url_" + url

    if title:
        return "title_" + title

    text_hash = hashlib.md5(text.encode("utf-8")).hexdigest()
    return "text_" + text_hash


def is_valid_document(document):
    title = str(document.get("title", "")).strip()
    text = clean_text(document.get("text", ""))

    if not title and not text:
        return False

    if len(text.split()) < 20:
        return False

    return True


def remove_unwanted_fields(document):
    unwanted_fields = [
        "overall_sentiment_score",
        "overall_sentiment_label",
        "sentiment_score",
        "sentiment_label",
        "news_sentiment",
        "public_sentiment",
        "text_word_count",
        "text_character_count"
    ]

    for field in unwanted_fields:
        document.pop(field, None)

    return document


def clean_documents(raw_documents):
    cleaned_documents = []
    seen_keys = set()

    total_documents = len(raw_documents)
    invalid_count = 0
    duplicate_count = 0

    for document in raw_documents:
        if not is_valid_document(document):
            invalid_count += 1
            continue

        duplicate_key = create_duplicate_key(document)

        if duplicate_key in seen_keys:
            duplicate_count += 1
            continue

        seen_keys.add(duplicate_key)

        clean_id = len(cleaned_documents) + 1

        # Keep original metadata
        cleaned_document = document.copy()

        # Remove sentiment and extra analysis fields
        cleaned_document = remove_unwanted_fields(cleaned_document)

        # Clean only the main text field
        cleaned_document["text"] = clean_text(cleaned_document.get("text", ""))

        # Add unique clean document ID
        final_document = {
            "clean_document_id": clean_id,
            **cleaned_document
        }

        cleaned_documents.append(final_document)

    print("\nCleaning Summary")
    print("-------------------------")
    print("Raw documents:", total_documents)
    print("Invalid documents removed:", invalid_count)
    print("Duplicate documents removed:", duplicate_count)
    print("Clean documents saved:", len(cleaned_documents))

    return cleaned_documents


def main():
    create_project_folders()

    print("Loading raw documents from:", RAW_DOCUMENTS_FILE)

    raw_documents = load_jsonl(RAW_DOCUMENTS_FILE)

    if not raw_documents:
        print("No raw documents found. Run collectors first.")
        return

    cleaned_documents = clean_documents(raw_documents)

    save_jsonl(cleaned_documents, CLEAN_DOCUMENTS_FILE)

    print("\nCleaned data saved to:", CLEAN_DOCUMENTS_FILE)


if __name__ == "__main__":
    main()