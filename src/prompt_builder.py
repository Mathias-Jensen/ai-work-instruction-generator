# src/prompt_builder.py

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.models import WorkInstructionInput


class PromptBuilder:
    def __init__(self, template_dir: str = "prompts"):
        self.template_dir = Path(template_dir)

        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(disabled_extensions=("j2",)),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def build_work_instruction_prompt(
        self,
        input_data: WorkInstructionInput,
    ) -> str:
        template = self.env.get_template("work_instruction_prompt.j2")

        return template.render(
            document_title=input_data.document_title,
            equipment_or_system=input_data.equipment_or_system,
            target_user=input_data.target_user,
            experience_level=input_data.experience_level.value,
            raw_notes=input_data.raw_notes,
        )