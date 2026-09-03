import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse


INDEX = Path(__file__).resolve().parents[1] / "index.html"
PREFIX = "<script>window.PULS_SNAPSHOT="
SUFFIX = ";</script>"
MAX_SUMMARY = 280
RUNTIME_MARKER = "function publicSafeArticles(articles)"


def clean_text(value: object, limit: int) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", " ", str(value or "")))
    return re.sub(r"\s+", " ", text).strip()[:limit]


def safe_url(value: object) -> str:
    url = str(value or "").strip()
    parsed = urlparse(url)
    return url if parsed.scheme == "https" and parsed.netloc else ""


def safe_article(article: dict) -> dict:
    summary = clean_text(article.get("summary") or article.get("readerText"), MAX_SUMMARY)
    return {
        "id": clean_text(article.get("id"), 120),
        "title": clean_text(article.get("title"), 400),
        "url": safe_url(article.get("url")),
        "source": clean_text(article.get("source"), 120),
        "sourceId": clean_text(article.get("sourceId"), 120),
        "sourceUrl": safe_url(article.get("sourceUrl")),
        "sourceColor": clean_text(article.get("sourceColor"), 20),
        "published": clean_text(article.get("published"), 60),
        "category": clean_text(article.get("category"), 120),
        "author": clean_text(article.get("author"), 160),
        "summary": summary,
        "readerText": summary,
        "image": "",
        "framable": article.get("framable") is not False,
    }


def main() -> None:
    source = INDEX.read_text(encoding="utf-8")
    start = source.index(PREFIX) + len(PREFIX)
    end = source.index(SUFFIX, start)
    payload = json.loads(source[start:end])
    payload["articles"] = [
        safe_article(article)
        for article in payload.get("articles", [])
        if safe_url(article.get("url")) and clean_text(article.get("title"), 400)
    ]
    snapshot = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    source = source[:start] + snapshot + source[end:]

    if RUNTIME_MARKER not in source:
        save_marker = "  function saveStoredPayload(payload) {"
        helper = """  function publicSafeArticles(articles) {
    return articles.map((article) => {
      const summary = String(article.summary || article.readerText || "")
        .replace(/<[^>]+>/g, " ")
        .replace(/\\s+/g, " ")
        .trim()
        .slice(0, 280);
      return { ...article, summary, readerText: summary, image: "" };
    });
  }

"""
        if save_marker not in source:
            raise RuntimeError("PULS storage function was not found")
        source = source.replace(save_marker, helper + save_marker, 1)

    if source.count(RUNTIME_MARKER) < 2:
        main_marker = '<script>\n"use strict";\n\n'
        main_helper = """function publicSafeArticles(articles) {
  return articles.map((article) => {
    const summary = String(article.summary || article.readerText || "")
      .replace(/<[^>]+>/g, " ")
      .replace(/\\s+/g, " ")
      .trim()
      .slice(0, 280);
    return { ...article, summary, readerText: summary, image: "" };
  });
}

"""
        if main_marker not in source:
            raise RuntimeError("PULS main script was not found")
        source = source.replace(main_marker, main_marker + main_helper, 1)

    if "const safePayload = {" not in source:
        original_store = """  function saveStoredPayload(payload) {
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify(payload));
    } catch {
      // The embedded snapshot remains available if private browsing blocks storage.
    }
    storedPayload = payload;
    storedGroups = sourceSnapshot(payload);"""
        safe_store = """  function saveStoredPayload(payload) {
    const safePayload = {
      ...payload,
      articles: publicSafeArticles(payload.articles || []),
    };
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify(safePayload));
    } catch {
      // The embedded snapshot remains available if private browsing blocks storage.
    }
    storedPayload = safePayload;
    storedGroups = sourceSnapshot(safePayload);"""
        if original_store not in source:
            raise RuntimeError("PULS cache assignment was not found")
        source = source.replace(original_store, safe_store, 1)

    original = "    state.articles = payload.articles;"
    safe_assignment = "    state.articles = publicSafeArticles(payload.articles);"
    if original in source:
        source = source.replace(original, safe_assignment, 1)
    elif safe_assignment not in source:
        raise RuntimeError("PULS article assignment was not found")

    INDEX.write_text(source, encoding="utf-8", newline="\n")
    print(f"Sanitized {len(payload['articles'])} source-linked articles")


if __name__ == "__main__":
    main()
