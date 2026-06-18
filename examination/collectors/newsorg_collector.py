import requests
import os
import time
from datetime import datetime
from config.settings import TOPIC, NEWS_ORG_URL, DELAY_TIME, NOD
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

API_KEY = os.getenv("NEWS_ORG_API_KEY")


def get_full_article_text(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        paragraphs = soup.find_all("p")

        text_parts = []

        for paragraph in paragraphs:
            text = paragraph.get_text(" ", strip=True)

            if len(text.split()) > 8:
                text_parts.append(text)

        full_text = "\n".join(text_parts)

        return full_text

    except Exception as error:
        print("Article text extraction failed:", error)
        return ""


def collect_newsorg_news():
    if API_KEY is None:
        print("News.org API key is missing.")
        return []

    params = {
        "q": TOPIC,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": NOD,
        "apiKey": API_KEY
    }

    response = requests.get(NEWS_ORG_URL, params=params, timeout=20)

    print("News.org Status Code:", response.status_code)

    if response.status_code != 200:
        print("News.org request failed.")
        print(response.text[:500])
        return []

    data = response.json()

    articles = data.get("articles", [])

    documents = []

    for article in articles:
        title = article.get("title", "")
        source = article.get("source", {}).get("name", "")
        published_at = article.get("publishedAt", "")
        url = article.get("url", "")
        description = article.get("description", "")
        content = article.get("content", "")

        full_text = get_full_article_text(url)

        if full_text:
            text = full_text
        else:
            text = f"{title}. {description}. {content}"

        document = {
            "company": "NVIDIA",
            "source": "News.org",
            "source_type": "general_news",
            "publisher": source,
            "title": title,
            "published_at": published_at,
            "url": url,
            "description": description,
            "content": content,
            "text": text,
            "topic": TOPIC,
            "collected_at": datetime.now().isoformat()
        }

        documents.append(document)

        time.sleep(DELAY_TIME)

    return documents


if __name__ == "__main__":
    documents = collect_newsorg_news()

    print("Total News.org documents collected:", len(documents))

    for i, document in enumerate(documents, start=1):
        print("\n-------------------------")
        print("count:", i)
        print("Title:", document["title"])
        print("Source:", document["source"])
        print("Publisher:", document["publisher"])
        print("Published At:", document["published_at"])
        print("URL:", document["url"])
        print("Text Preview:", document["text"][:1000])





    # params = {
#     "q": TOPIC,
#     "language": "en",
#     "sortBy": "publishedAt",
#     "pageSize": 10,
#     "apiKey": API_KEY
# }

# response = requests.get(NEWS_ORG_URL, params=params)

# print("Status Code:", response.status_code)

# data = response.json()

# articles = data.get("articles", [])

# print("Total articles received:", len(articles))


# for article in articles:
#     print("\n-------------------------")
#     print("Title:", article.get("title"))
#     print("Source:", article.get("source", {}).get("name"))
#     print("Published At:", article.get("publishedAt"))
#     print("URL:", article.get("url"))
#     print("Description:", article.get("description"))
