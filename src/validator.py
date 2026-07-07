# src/validator.py

import json
from pydantic import ValidationError

from src.models import WorkInstructionOutput


class OutputValidator:
    """
    Validates and parses LLM JSON output into a strongly typed
    WorkInstructionOutput object.
    """

    @staticmethod
    def validate(raw_response: str) -> WorkInstructionOutput:
        try:
            data = json.loads(raw_response)

        except json.JSONDecodeError as e:
            raise ValueError(
                f"LLM returned invalid JSON:\n{e}"
            )

        try:
            return WorkInstructionOutput.model_validate(data)

        except ValidationError as e:
            raise ValueError(
                f"Pydantic validation failed:\n{e}"
            )