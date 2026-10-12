#!/usr/bin/env python3
"""Offline checks for the machine-readable catalog and model-origin policy.

* catalog/entries.json matches catalog/schema.json.
* Every catalog entry corresponds to a link under the same README heading,
  so the sidecar cannot drift away from the hand-written list.
* No README link or catalog entry names a model family barred by
  scripts/model_policy.py.
* Freshness: entries whose last_checked is older than --max-age days are
  reported. This is a warning by default and fails only with --strict, so a
  calendar rollover never breaks an unrelated PR.

Usage: python3 scripts/check-catalog.py [--strict] [--max-age DAYS]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _schema import validate as validate_schema  # noqa: E402
from model_policy import violations  # noqa: E402

CATALOG = ROOT / "catalog"
README = ROOT / "README.md"
LINK_RE = re.compile(r"^- \[([^\]]+)\]\((https?://[^)\s]+)\)", re.MULTILINE)


def readme_sections() -> dict[str, set[str]]:
    """Map each '## ' heading (emoji stripped) to the URLs listed under it."""
    sections: dict[str, set[str]] = {}
    current = None
    for line in README.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            current = re.sub(r"^[^\w(]+", "", line[3:]).strip()
            sections[current] = set()
        elif current:
            match = LINK_RE.match(line)
            if match:
                sections[current].add(match.group(2))
    return sections


def check_policy() -> list[str]:
    errors = []
    for name, url in LINK_RE.findall(README.read_text(encoding="utf-8")):
        for family in violations(f"{name} {url}"):
            errors.append(f"README entry {name!r} violates model-origin policy ({family})")
    return errors


def check_catalog(today: dt.date, max_age: int) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    stale: list[str] = []
    data = json.loads((CATALOG / "entries.json").read_text(encoding="utf-8"))
    schema = json.loads((CATALOG / "schema.json").read_text(encoding="utf-8"))
    errors.extend(f"catalog/entries.json {e}" for e in validate_schema(data, schema))
    if errors:
        return errors, stale
    sections = readme_sections()
    seen_urls: set[str] = set()
    for section in data["sections"]:
        heading = section["heading"]
        if heading not in sections:
            errors.append(f"catalog section {heading!r} has no matching README heading")
            continue
        for entry in section["entries"]:
            label = f"{heading} / {entry['name']}"
            if entry["url"] in seen_urls:
                errors.append(f"{label}: duplicate URL {entry['url']}")
            seen_urls.add(entry["url"])
            if entry["url"] not in sections[heading]:
                errors.append(f"{label}: URL not listed under that README heading")
            errors.extend(f"{label}: violates model-origin policy ({v})"
                          for v in violations(f"{entry['name']} {entry['url']}"))
            checked = dt.date.fromisoformat(entry["last_checked"])
            if checked > today:
                errors.append(f"{label}: last_checked is in the future")
            elif (today - checked).days > max_age:
                stale.append(f"{label}: last checked {entry['last_checked']}")
    return errors, stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--strict", action="store_true", help="fail on stale entries")
    parser.add_argument("--max-age", type=int, default=180, help="freshness window in days")
    args = parser.parse_args()

    errors = check_policy()
    catalog_errors, stale = check_catalog(dt.date.today(), args.max_age)
    errors.extend(catalog_errors)
    for item in stale:
        print(f"stale: {item}")
    if args.strict and stale:
        errors.append(f"{len(stale)} catalog entr{'y is' if len(stale) == 1 else 'ies are'} older than {args.max_age} days")
    if errors:
        print("Catalog checks failed:")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    count = sum(len(s["entries"]) for s in json.loads((CATALOG / "entries.json").read_text())["sections"])
    print(f"OK: {count} catalog entries valid and linked; README passes the model-origin policy.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
