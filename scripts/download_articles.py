"""Download 10 English articles (~300-1000 words) for the intro exercise."""

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "01_Intro-to-LLMs"
OUT.mkdir(parents=True, exist_ok=True)

ARTICLES = [
    ("en", "Artificial intelligence", "Tech: Artificial Intelligence"),
    ("en", "Quantum computing", "Tech: Quantum Computing"),
    ("en", "Large language model", "Tech: Large Language Models"),
    ("en", "CRISPR", "Tech: CRISPR Gene Editing"),
    ("en", "Renewable energy", "Tech: Renewable Energy"),
    ("simple", "Robot", "Tech: Robots"),
    ("en", "Space exploration", "Tech: Space Exploration"),
    ("en", "Science fiction", "Sci-Fi: Science Fiction"),
    ("en", "Cyberpunk", "Sci-Fi: Cyberpunk"),
    ("en", "Mars", "Tech/Science: Mars"),
]


def fetch_wikipedia(title: str, lang: str = "en") -> str:
    base = f"https://{lang}.wikipedia.org/w/api.php"
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "prop": "extracts",
            "explaintext": "true",
            "titles": title,
            "format": "json",
        }
    )
    req = urllib.request.Request(
        base + "?" + params,
        headers={"User-Agent": "LLM-Basics/1.0 (education)"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.load(response)
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    return page.get("extract", "")


def trim_words(text: str, max_words: int = 1000) -> tuple[str, int]:
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    words = text.split()
    if len(words) > max_words:
        words = words[:max_words]
    text = " ".join(words)
    return text, len(words)


def main() -> None:
    for i, (lang, title, label) in enumerate(ARTICLES, 1):
        raw = fetch_wikipedia(title, lang)
        trimmed, word_count = trim_words(raw)
        slug = title.replace(" ", "_")
        header = (
            f"Title: {label}\n"
            f"Source: https://{lang}.wikipedia.org/wiki/{slug}\n"
            f"Word count: {word_count}\n\n"
        )
        path = OUT / f"article_{i:02d}.txt"
        path.write_text(header + trimmed, encoding="utf-8")
        print(f"{path.name}: {word_count} words - {label}")


if __name__ == "__main__":
    main()
