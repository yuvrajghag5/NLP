import json
from datetime import datetime

from config.paths import RAW_DOCUMENTS_FILE, create_project_folders

from collectors.alpha_collector import collect_alpha_vantage_news
from collectors.newsorg_collector import collect_newsorg_news
from collectors.nvidia_rss_collector import get_nvidia_rss_news


def add_document_id(documents):
    final_documents = []

    for index, document in enumerate(documents, start=1):
        document["document_id"] = index
        final_documents.append(document)

    return final_documents


def save_documents_jsonl(documents, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        for document in documents:
            file.write(json.dumps(document, ensure_ascii=False) + "\n")


def run_all_collectors():
    create_project_folders()

    all_documents = []

    print("\nCollecting Alpha Vantage news...")
    alpha_documents = collect_alpha_vantage_news()
    all_documents.extend(alpha_documents)

    print("\nCollecting News.org articles...")
    newsorg_documents = collect_newsorg_news()
    all_documents.extend(newsorg_documents)

    print("\nCollecting NVIDIA official RSS articles...")
    nvidia_documents = get_nvidia_rss_news()
    all_documents.extend(nvidia_documents)

    all_documents = add_document_id(all_documents)

    save_documents_jsonl(all_documents, RAW_DOCUMENTS_FILE)

    print("\nData collection completed.")
    print("Total documents collected:", len(all_documents))
    print("Saved to:", RAW_DOCUMENTS_FILE)
    print("Timestamp:", datetime.now().isoformat())


if __name__ == "__main__":
    run_all_collectors()