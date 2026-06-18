import time
import requests
import feedparser
from bs4 import BeautifulSoup

from config.settings import RSS_URL, NOD, DELAY_TIME


def clean_text(text):
    if text is None:
        return ""

    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text(" ", strip=True)

    return text


def get_nvidia_rss_news():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(RSS_URL, headers=headers, timeout=15)

    print("Status Code:", response.status_code)

    if response.status_code != 200:
        print("NVIDIA RSS request failed")
        return []

    feed = feedparser.parse(response.text)

    articles = []

    for entry in feed.entries[:NOD]:
        title = clean_text(entry.get("title", ""))
        summary = clean_text(entry.get("summary", ""))
        url = entry.get("link", "")
        published = entry.get("published", "")

        article = {
            "title": title,
            "source": "NVIDIA Official RSS",
            "published_at": published,
            "url": url,
            "description": summary,
            "text": summary
        }

        articles.append(article)

        time.sleep(DELAY_TIME)

    return articles




if __name__ == "__main__":

    articles = get_nvidia_rss_news()

    print("Total NVIDIA official articles:", len(articles))

    
    for i,article in enumerate(articles, start = 1):
        print("\n-------------------------")
        print("count:",i)
        print("Title:", article["title"])
        print("Source:", article["source"])
        print("Published At:", article["published_at"])
        print("URL:", article["url"])
        print("Description:", article["description"])
        print("Text:", article["text"][:1000])
