# src/pipeline.py

from dataclasses import dataclass
from pathlib import Path

from src.llm_client import LLMClient
from src.markdown_generator import MarkdownGenerator
from src.models import WorkInstructionInput, WorkInstructionOutput
from src.prompt_builder import PromptBuilder
from src.rule_checker import RuleChecker, RuleCheckResult
from src.validator import OutputValidator


@dataclass
class PipelineResult:
    work_instruction: WorkInstructionOutput
    markdown: str
    rule_check: RuleCheckResult


class WorkInstructionPipeline:
    def __init__(self, mock_mode: bool = False):
        self.prompt_builder = PromptBuilder()
        self.llm_client = LLMClient(mock_mode=mock_mode)
        self.validator = OutputValidator()
        self.rule_checker = RuleChecker()
        self.markdown_generator = MarkdownGenerator()

    def run(self, input_data: WorkInstructionInput) -> PipelineResult:
        prompt = self.prompt_builder.build_work_instruction_prompt(input_data)

        raw_response = self.llm_client.generate(prompt)

        work_instruction = self.validator.validate(raw_response)

        rule_check = self.rule_checker.check(work_instruction)

        markdown = self.markdown_generator.generate(work_instruction)

        return PipelineResult(
            work_instruction=work_instruction,
            markdown=markdown,
            rule_check=rule_check,
        )

    @staticmethod
    def save_outputs(
        result: PipelineResult,
        output_dir: str = "outputs",
    ) -> None:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        json_path = output_path / "work_instruction.json"
        markdown_path = output_path / "work_instruction.md"

        json_path.write_text(
            result.work_instruction.model_dump_json(indent=2),
            encoding="utf-8",
        )

        markdown_path.write_text(
            result.markdown,
            encoding="utf-8",
        )