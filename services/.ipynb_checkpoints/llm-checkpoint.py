import json
from typing import Type

from ollama import chat
from pydantic import BaseModel

from config import OLLAMA_MODEL


class LLM:
    """Wrapper around the Ollama chat API."""

    def __init__(self, model: str = OLLAMA_MODEL):
        """Initialize the LLM client."""

        self.model = model

    def generate(
        self, prompt: str, schema: Type[BaseModel] | None = None
    ) -> str | BaseModel:
        """Generate a response from the language model."""

        kwargs = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "think": False,
            "options": {
                "temperature": 0,
            },
        }

        if schema is not None:
            kwargs["format"] = schema.model_json_schema()

        print(f"Prompt length: {len(prompt)} characters")

        response = chat(**kwargs)
        content = response.message.content

        if schema is None:
            return content

        return schema.model_validate(json.loads(content))
