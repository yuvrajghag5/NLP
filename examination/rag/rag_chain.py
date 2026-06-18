# import json
# from datetime import datetime

# from langchain_core.output_parsers import StrOutputParser

# from config.paths import (
#     STRATEGIC_EVIDENCE_FILE,
#     CEO_BRIEFING_FILE,
#     create_project_folders
# )

# from config.settings import (
#     COMPANY_NAME,
#     DEFAULT_CEO_QUESTION,
#     RAG_TOP_K,
#     STRATEGIC_EVIDENCE_PER_CATEGORY_IN_PROMPT,
#     MAX_CHARS_PER_EVIDENCE
# )

# from rag.prompt import get_ceo_prompt
# from rag.llm import load_llm

# from vector_db.faiss_retriever import (
#     load_faiss_index,
#     load_chunk_metadata,
#     load_embedding_model,
#     search_faiss
# )


# def load_json(file_path):
#     if not file_path.exists():
#         print("File not found:", file_path)
#         return None

#     with open(file_path, "r", encoding="utf-8") as file:
#         return json.load(file)


# def save_json(data, file_path):
#     with open(file_path, "w", encoding="utf-8") as file:
#         json.dump(data, file, indent=4, ensure_ascii=False)


# def shorten_text(text, max_chars=900):
#     if text is None:
#         return ""

#     text = str(text).strip()

#     if len(text) <= max_chars:
#         return text

#     return text[:max_chars] + "..."


# def format_strategic_evidence(strategic_evidence):
#     categories = strategic_evidence.get("categories", {})

#     formatted_sections = []
#     source_records = []

#     source_number = 1

#     for category, evidence_items in categories.items():
#         formatted_sections.append(f"\n## {category.upper()}")

#         sorted_items = sorted(
#             evidence_items,
#             key=lambda item: item.get("score", 0),
#             reverse=True
#         )

#         selected_items = sorted_items[:STRATEGIC_EVIDENCE_PER_CATEGORY_IN_PROMPT]

#         for item in selected_items:
#             source_id = f"S{source_number}"

#             title = item.get("title", "")
#             source = item.get("source", "")
#             publisher = item.get("publisher", "")
#             url = item.get("url", "")
#             score = item.get("score", "")
#             evidence_text = shorten_text(
#                 item.get("evidence_text", ""),
#                 MAX_CHARS_PER_EVIDENCE
#             )

#             formatted_sections.append(
#                 f"""
# [{source_id}]
# Category: {category}
# Title: {title}
# Source: {source}
# Publisher: {publisher}
# Score: {score}
# URL: {url}
# Evidence:
# {evidence_text}
# """
#             )

#             source_records.append({
#                 "source_id": source_id,
#                 "type": "strategic_evidence",
#                 "category": category,
#                 "title": title,
#                 "source": source,
#                 "publisher": publisher,
#                 "url": url,
#                 "score": score
#             })

#             source_number += 1

#     return "\n".join(formatted_sections), source_records


# def retrieve_additional_context(question):
#     print("Loading FAISS index...")
#     index = load_faiss_index()

#     if index is None:
#         return "", []

#     print("Loading chunk metadata...")
#     metadata = load_chunk_metadata()

#     if not metadata:
#         return "", []

#     print("Loading embedding model...")
#     model = load_embedding_model()

#     print("Retrieving additional FAISS context...")

#     results = search_faiss(
#         query=question,
#         index=index,
#         metadata=metadata,
#         model=model,
#         top_k=RAG_TOP_K
#     )

#     formatted_results = []
#     source_records = []

#     for index_number, result in enumerate(results, start=1):
#         source_id = f"R{index_number}"

#         title = result.get("title", "")
#         source = result.get("source", "")
#         publisher = result.get("publisher", "")
#         url = result.get("url", "")
#         score = result.get("score", "")
#         chunk_text = shorten_text(
#             result.get("chunk_text", ""),
#             MAX_CHARS_PER_EVIDENCE
#         )

#         formatted_results.append(
#             f"""
# [{source_id}]
# Title: {title}
# Source: {source}
# Publisher: {publisher}
# Score: {score}
# URL: {url}
# Retrieved Context:
# {chunk_text}
# """
#         )

#         source_records.append({
#             "source_id": source_id,
#             "type": "faiss_retrieval",
#             "title": title,
#             "source": source,
#             "publisher": publisher,
#             "url": url,
#             "score": score
#         })

#     return "\n".join(formatted_results), source_records


# def generate_ceo_briefing(question=DEFAULT_CEO_QUESTION):
#     create_project_folders()

#     print("Loading strategic evidence from:", STRATEGIC_EVIDENCE_FILE)

#     strategic_evidence = load_json(STRATEGIC_EVIDENCE_FILE)

#     if strategic_evidence is None:
#         print("Strategic evidence not found. Run strategic_intelligence_engine.py first.")
#         return None

#     strategic_context, strategic_sources = format_strategic_evidence(strategic_evidence)

#     retrieved_context, retrieved_sources = retrieve_additional_context(question)

#     print("Loading CEO prompt...")
#     prompt = get_ceo_prompt()

#     print("Loading LLM...")
#     llm = load_llm()

#     output_parser = StrOutputParser()

#     rag_chain = prompt | llm | output_parser

#     print("Generating CEO briefing...")

#     response = rag_chain.invoke({
#         "company": COMPANY_NAME,
#         "question": question,
#         "strategic_evidence": strategic_context,
#         "retrieved_context": retrieved_context
#     })

#     # response = clean_llm_response(response)

#     ceo_briefing = {
#         "company": COMPANY_NAME,
#         "question": question,
#         "generated_at": datetime.now().isoformat(),
#         "answer": response,
#         "sources_used": strategic_sources + retrieved_sources
#     }

#     save_json(ceo_briefing, CEO_BRIEFING_FILE)

#     print("\nCEO briefing generated successfully.")
#     print("-------------------------")
#     print("Saved to:", CEO_BRIEFING_FILE)

#     return ceo_briefing



# # def clean_llm_response(response):
# #     if response is None:
# #         return ""

# #     response = str(response).strip()

# #     stop_phrases = [
# #         "End of CEO Briefing.",
# #         "===================================================",
# #         "EXECUTIVE SUMMARY:",
# #         "Executive Summary:"
# #     ]

# #     for phrase in stop_phrases:
# #         if phrase in response:
# #             if phrase == "End of CEO Briefing.":
# #                 response = response.split(phrase)[0].strip() + "\n\nEnd of CEO Briefing."
# #             else:
# #                 response = response.split(phrase)[0].strip()

# #     return response



# # def remove_duplicate_sources(sources):
# #     unique_sources = []
# #     seen_urls = set()
# #     seen_titles = set()

# #     for source in sources:
# #         url = source.get("url", "").strip()
# #         title = source.get("title", "").strip().lower()

# #         if url and url in seen_urls:
# #             continue

# #         if not url and title in seen_titles:
# #             continue

# #         if url:
# #             seen_urls.add(url)

# #         if title:
# #             seen_titles.add(title)

# #         unique_sources.append(source)

# #     return unique_sources



# def main():
#     briefing = generate_ceo_briefing()

#     if briefing is None:
#         return

#     print("\nCEO Briefing Preview")
#     print("-------------------------")
#     print(briefing["answer"][:3000])


# if __name__ == "__main__":
#     main()





import json
from datetime import datetime

from langchain_core.output_parsers import StrOutputParser

from config.paths import (
    STRATEGIC_EVIDENCE_FILE,
    CEO_BRIEFING_FILE,
    create_project_folders
)

from config.settings import (
    COMPANY_NAME,
    DEFAULT_CEO_QUESTION,
    RAG_TOP_K,
    STRATEGIC_EVIDENCE_PER_CATEGORY_IN_PROMPT,
    MAX_CHARS_PER_EVIDENCE
)

from rag.prompt import get_ceo_prompt
from rag.llm import load_llm

from vector_db.faiss_retriever import (
    load_faiss_index,
    load_chunk_metadata,
    load_embedding_model,
    search_faiss
)


def load_json(file_path):
    if not file_path.exists():
        print("File not found:", file_path)
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def shorten_text(text, max_chars=900):
    if text is None:
        return ""

    text = str(text).strip()

    if len(text) <= max_chars:
        return text

    return text[:max_chars] + "..."


def format_strategic_evidence(strategic_evidence):
    categories = strategic_evidence.get("categories", {})

    formatted_sections = []
    source_records = []

    source_number = 1

    for category, evidence_items in categories.items():
        formatted_sections.append(f"\n## {category.upper()}")

        sorted_items = sorted(
            evidence_items,
            key=lambda item: item.get("score", 0),
            reverse=True
        )

        selected_items = sorted_items[:STRATEGIC_EVIDENCE_PER_CATEGORY_IN_PROMPT]

        for item in selected_items:
            source_id = f"S{source_number}"

            title = item.get("title", "")
            source = item.get("source", "")
            publisher = item.get("publisher", "")
            url = item.get("url", "")
            score = item.get("score", "")
            evidence_text = shorten_text(
                item.get("evidence_text", ""),
                MAX_CHARS_PER_EVIDENCE
            )

            formatted_sections.append(
                f"""
[{source_id}]
Category: {category}
Title: {title}
Source: {source}
Publisher: {publisher}
Score: {score}
URL: {url}
Evidence:
{evidence_text}
"""
            )

            source_records.append({
                "source_id": source_id,
                "type": "strategic_evidence",
                "category": category,
                "title": title,
                "source": source,
                "publisher": publisher,
                "url": url,
                "score": score
            })

            source_number += 1

    return "\n".join(formatted_sections), source_records


def retrieve_additional_context(question):
    print("Loading FAISS index...")
    index = load_faiss_index()

    if index is None:
        return "", []

    print("Loading chunk metadata...")
    metadata = load_chunk_metadata()

    if not metadata:
        return "", []

    print("Loading embedding model...")
    model = load_embedding_model()

    print("Retrieving additional FAISS context...")

    results = search_faiss(
        query=question,
        index=index,
        metadata=metadata,
        model=model,
        top_k=RAG_TOP_K
    )

    formatted_results = []
    source_records = []

    for index_number, result in enumerate(results, start=1):
        source_id = f"R{index_number}"

        title = result.get("title", "")
        source = result.get("source", "")
        publisher = result.get("publisher", "")
        url = result.get("url", "")
        score = result.get("score", "")
        chunk_text = shorten_text(
            result.get("chunk_text", ""),
            MAX_CHARS_PER_EVIDENCE
        )

        formatted_results.append(
            f"""
[{source_id}]
Title: {title}
Source: {source}
Publisher: {publisher}
Score: {score}
URL: {url}
Retrieved Context:
{chunk_text}
"""
        )

        source_records.append({
            "source_id": source_id,
            "type": "faiss_retrieval",
            "title": title,
            "source": source,
            "publisher": publisher,
            "url": url,
            "score": score
        })

    return "\n".join(formatted_results), source_records


def generate_ceo_briefing(question=DEFAULT_CEO_QUESTION):
    create_project_folders()

    print("Loading strategic evidence from:", STRATEGIC_EVIDENCE_FILE)

    strategic_evidence = load_json(STRATEGIC_EVIDENCE_FILE)

    if strategic_evidence is None:
        print("Strategic evidence not found. Run strategic_intelligence_engine.py first.")
        return None

    strategic_context, strategic_sources = format_strategic_evidence(strategic_evidence)

    retrieved_context, retrieved_sources = retrieve_additional_context(question)

    print("Loading CEO prompt...")
    prompt = get_ceo_prompt()

    print("Loading LLM...")
    llm = load_llm()

    output_parser = StrOutputParser()

    rag_chain = prompt | llm | output_parser

    print("Generating CEO briefing...")

    response = rag_chain.invoke({
        "company": COMPANY_NAME,
        "question": question,
        "strategic_evidence": strategic_context,
        "retrieved_context": retrieved_context
    })

    ceo_briefing = {
        "company": COMPANY_NAME,
        "question": question,
        "generated_at": datetime.now().isoformat(),
        "answer": response,
        "sources_used": strategic_sources + retrieved_sources
    }

    save_json(ceo_briefing, CEO_BRIEFING_FILE)

    print("\nCEO briefing generated successfully.")
    print("-------------------------")
    print("Saved to:", CEO_BRIEFING_FILE)

    return ceo_briefing


def main():
    briefing = generate_ceo_briefing()

    if briefing is None:
        return

    print("\nCEO Briefing Preview")
    print("-------------------------")
    print(briefing["answer"][:3000])


if __name__ == "__main__":
    main()