import time
import requests
import feedparser
from concurrent.futures import ThreadPoolExecutor

FEEDS = {
    "TechCrunch": "https://techcrunch.com/feed/",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",
    "Wired": "https://www.wired.com/feed/rss",
    "Engadget": "https://www.engadget.com/rss.xml",
    "MIT Tech Review": "https://www.technologyreview.com/feed/",
    "VentureBeat": "https://venturebeat.com/feed/",
    "ZDNet": "https://www.zdnet.com/news/rss.xml",
    "The Register": "https://www.theregister.com/headlines.atom",
    "Gizmodo": "https://gizmodo.com/feed",
    "CNET": "https://www.cnet.com/rss/news/",
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
    "Hacker News": "https://hnrss.org/frontpage",
    "Inc42": "https://inc42.com/feed/",
}

HEADERS = {"User-Agent": "Mozilla/5.0 (tech-news-app)"}

def fetch_one(source, url, limit):
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        feed = feedparser.parse(r.content)
    except Exception as e:
        print(f"[skip] {source}: {e}")
        return []
    items = []
    for e in feed.entries[:limit]:
        items.append({
            "source": source,
            "title": e.get("title", "").strip(),
            "link": e.get("link", ""),
            "published": e.get("published_parsed") or e.get("updated_parsed"),
        })
    if not items:
        print(f"[empty] {source}: check its URL")
    return items

def fetch_news(per_source=5):
    with ThreadPoolExecutor(max_workers=10) as pool:
        results = pool.map(lambda kv: fetch_one(kv[0], kv[1], per_source), FEEDS.items())
    items = [i for group in results for i in group]

    # remove duplicate titles
    seen, unique = set(), []
    for i in items:
        key = i["title"].lower()
        if key and key not in seen:
            seen.add(key)
            unique.append(i)

    unique.sort(key=lambda x: x["published"] or time.gmtime(0), reverse=True)
    for i in unique:
        i["published"] = time.strftime("%d %b %H:%M", i["published"]) if i["published"] else ""
    return unique

if __name__ == "__main__":
    news = fetch_news()
    print(len(news), "articles")
    for n in news[:30]:
        print(n["source"], "|", n["title"])