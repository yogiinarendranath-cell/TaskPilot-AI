from __future__ import annotations

import json
import os

from openai import OpenAI

_CLIENT = None


def _get_client() -> OpenAI:
    global _CLIENT
    if _CLIENT is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable is not set")
        base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        _CLIENT = OpenAI(api_key=api_key, base_url=base_url)
    return _CLIENT


def ask(prompt: str, model: str) -> str:
    """Single-turn completion. Returns text."""
    resp = _get_client().chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return resp.choices[0].message.content or ""


def ask_json(prompt: str, model: str) -> dict:
    """Ask for JSON. Strips code fences. Raises if invalid JSON."""
    text = ask(
        prompt + "\n\nRespond ONLY with a valid JSON object. No prose, no markdown.",
        model,
    )
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        text = text.rsplit("```", 1)[0]
    return json.loads(text.strip())
