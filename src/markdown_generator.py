# src/markdown_generator.py

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.models import WorkInstructionOutput


class MarkdownGenerator:
    def __init__(self, template_dir: str = "templates"):
        self.template_dir = Path(template_dir)

        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(disabled_extensions=("j2",)),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate(self, work_instruction: WorkInstructionOutput) -> str:
        template = self.env.get_template("work_instruction_template.md.j2")

        return template.render(
            work_instruction=work_instruction
        )