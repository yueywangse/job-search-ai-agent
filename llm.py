from typing import Type
from pydantic import BaseModel
from ollama import chat
from config import OLLAMA_MODEL

class LLM:
    def __init__(self, model=OLLAMA_MODEL):
        self.model = model

    def generate(
        self,
        prompt: str,
        schema: Type[BaseModel] | None = None
    ) -> str:
        kwargs = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        if schema is not None:
            kwargs["format"] = schema.model_json_schema()
        response = chat(**kwargs)

        return response.message.content