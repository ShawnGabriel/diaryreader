"""Thin wrapper so the rest of the pipeline doesn't care which
OpenAI-compatible backend (OpenRouter, self-hosted vLLM, DashScope, a
different provider entirely) is actually serving the model."""
import base64
import json
import os

from openai import OpenAI


def _image_to_data_url(image_path: str) -> str:
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{b64}"


class VLMClient:
    def __init__(self, base_url: str, api_key: str, model: str):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    def extract_page(self, image_path: str, prompt: str) -> list[dict]:
        """Send one page image + prompt, return the parsed JSON array.
        Raises ValueError with the raw text if the model didn't return
        valid JSON, so the caller can log/retry instead of silently
        losing a page."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": _image_to_data_url(image_path)}},
                    ],
                }
            ],
            temperature=0,
        )
        raw = response.choices[0].message.content.strip()
        # tolerate ```json ... ``` fences some models add despite instructions
        if raw.startswith("```"):
            raw = raw.strip("`")
            if raw.startswith("json"):
                raw = raw[4:]
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"Model did not return valid JSON for {image_path}: {e}\nRaw output:\n{raw}")
