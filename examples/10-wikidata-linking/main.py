"""Link an ambiguous mention using Wikidata's public search API.

Setup: uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
Run:   python main.py
Targeting Python 3.10-3.12. Requires network; obey Wikidata API guidance.
"""
import json
import re
import requests

API = "https://www.wikidata.org/w/api.php"


def main() -> None:
    mention = "Jordan"
    context = "Basketball legend Jordan won championships with the Chicago Bulls."
    try:
        response = requests.get(
            API,
            params={"action": "wbsearchentities", "search": mention,
                    "language": "en", "format": "json", "limit": 10},
            headers={"User-Agent": "awesome-entity-extraction-example/1.0 (educational)"},
            timeout=20,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise SystemExit(
            f"Wikidata request failed ({exc}). Check network access and retry."
        ) from exc
    candidates = response.json().get("search", [])
    stop_words = {"the", "with", "for", "and", "in", "a", "an", "of"}
    keywords = {word.lower() for word in re.findall(r"[A-Za-z]+", context)}
    keywords -= stop_words | {mention.lower()}

    def context_score(item: dict) -> int:
        candidate_text = (item.get("label", "") + " " +
                          item.get("description", "")).lower()
        return sum(bool(re.search(r"\\b" + re.escape(word) + r"\\b", candidate_text))
                   for word in keywords)

    ranked = sorted(candidates, key=context_score, reverse=True)
    result = [{"id": item["id"], "label": item.get("label", ""),
               "description": item.get("description", ""),
               "context_score": context_score(item)}
              for item in ranked[:5]]
    selected = result[0] if result and result[0]["context_score"] else None
    print(json.dumps({"mention": mention, "context": context,
                      "selected": selected, "candidates": result}, indent=2))
    assert selected is None or selected["id"].startswith("Q")


if __name__ == "__main__":
    main()
