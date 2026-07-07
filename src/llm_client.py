# src/llm_client.py

import os
from pathlib import Path


class LLMClient:
    def __init__(self, mock_mode: bool = False):
        self.mock_mode = mock_mode
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.mock_mode and not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY is missing. Set it in your environment or use mock_mode=True."
            )

    def generate(self, prompt: str) -> str:
        if self.mock_mode:
            return self._mock_response()

        return self._openai_response(prompt)

    def _openai_response(self, prompt: str) -> str:
        from openai import OpenAI

        client = OpenAI(api_key=self.api_key)

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.2,
        )

        return response.output_text

    def _mock_response(self) -> str:
        mock_path = Path("examples/mock_work_instruction_response.json")

        if not mock_path.exists():
            raise FileNotFoundError(
                "Mock response file not found: examples/mock_work_instruction_response.json"
            )

        return mock_path.read_text(encoding="utf-8")