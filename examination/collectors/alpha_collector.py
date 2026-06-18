import time
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
from config.settings import (
    COMPANY_NAME,
    TICKER,
    ALPHA_URL,
    NOD,
    DELAY_TIME
)


def collect_alpha_vantage_news():
    if API_KEY is None:
        print("Alpha Vantage API key is missing.")
        return []

    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": TICKER,
        "topics": "technology",
        "sort": "LATEST",
        "limit": NOD,
        "apikey": API_KEY
    }

    response = requests.get(ALPHA_URL, params=params, timeout=20)

    print("Alpha Vantage Status Code:", response.status_code)

    if response.status_code != 200:
        print("Alpha Vantage request failed.")
        print(response.text[:500])
        return []

    data = response.json()

    if "Note" in data:
        print("Alpha Vantage API limit message:")
        print(data["Note"])
        return []

    if "Information" in data:
        print("Alpha Vantage information message:")
        print(data["Information"])
        return []

    articles = data.get("feed", [])

    documents = []

    for article in articles[:NOD]:
        title = article.get("title", "")
        url = article.get("url", "")
        summary = article.get("summary", "")
        source = article.get("source", "")
        published_at = article.get("time_published", "")

        overall_sentiment_score = article.get("overall_sentiment_score", "")
        overall_sentiment_label = article.get("overall_sentiment_label", "")

        text = f"{title}. {summary}"

        document = {
            "company": COMPANY_NAME,
            "source": "Alpha Vantage",
            "source_type": "financial_news_sentiment",
            "publisher": source,
            "title": title,
            "published_at": published_at,
            "url": url,
            "summary": summary,
            "overall_sentiment_score": overall_sentiment_score,
            "overall_sentiment_label": overall_sentiment_label,
            "text": text,
            "collected_at": datetime.now().isoformat()
        }

        documents.append(document)

        time.sleep(DELAY_TIME)

    return documents


if __name__ == "__main__":
    documents = collect_alpha_vantage_news()

    print("\nTotal Alpha Vantage documents collected:", len(documents))

    for document in documents:
        print("\n-------------------------")
        print("Title:", document["title"])
        print("Source:", document["source"])
        print("Publisher:", document["publisher"])
        print("Published At:", document["published_at"])
        print("URL:", document["url"])
        print("Sentiment Score:", document["overall_sentiment_score"])
        print("Sentiment Label:", document["overall_sentiment_label"])
        print("Text Preview:", document["text"][:1000])