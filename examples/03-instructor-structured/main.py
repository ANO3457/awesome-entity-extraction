"""Typed structured extraction with Instructor and an OpenAI API.

Setup: uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
       export OPENAI_API_KEY=...  (PowerShell: $env:OPENAI_API_KEY="...")
Run:   python main.py
Targeting Python 3.10-3.12. Network/API key required; API usage may cost money.
"""
import json
import os
from typing import Optional

import instructor
from openai import OpenAI
from pydantic import BaseModel, ConfigDict


class BusinessNote(BaseModel):
    model_config = ConfigDict(extra="forbid")
    person: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    investment_usd: Optional[int] = None


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY before running this API example.")
    text = "Tim Cook said Apple will invest $2 billion in Paris."
    client = instructor.from_openai(OpenAI())
    result = client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=BusinessNote,
        messages=[{"role": "user", "content":
                   "Extract only facts stated in this note.\n" + text}],
    )
    assert result.person and result.company and result.location
    assert isinstance(result.investment_usd, int)
    print(json.dumps({"source": text, "extracted": result.model_dump()}, indent=2))


if __name__ == "__main__":
    main()
