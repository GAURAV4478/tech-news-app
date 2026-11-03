import time
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from news import fetch_news
from ai import digest

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CACHE_SECONDS = 900  # 15 minutes
cache = {"time": 0, "data": None}


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/api/news")
def news():
    if cache["data"] and time.time() - cache["time"] < CACHE_SECONDS:
        return cache["data"]
    items = fetch_news()
    data = {"digest": digest(items), "articles": items}
    cache.update(time=time.time(), data=data)
    return data


# must stay LAST: serves frontend/index.html at "/"
FRONTEND = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=FRONTEND, html=True), name="frontend")