# src/rule_checker.py

from src.models import WorkInstructionOutput


class RuleCheckResult:
    def __init__(self, warnings: list[str]):
        self.warnings = warnings

    @property
    def passed(self) -> bool:
        return len(self.warnings) == 0


class RuleChecker:
    """
    Applies deterministic business rules to a validated WorkInstructionOutput.
    """

    @staticmethod
    def check(work_instruction: WorkInstructionOutput) -> RuleCheckResult:
        warnings = []

        if not work_instruction.human_review_required:
            warnings.append("Human review must always be required.")

        if len(work_instruction.procedure_steps) < 3:
            warnings.append("Work instruction should contain at least 3 procedure steps.")

        if len(work_instruction.safety_precautions) < 1:
            warnings.append("At least one safety precaution should be included.")

        if len(work_instruction.quality_checks) < 1:
            warnings.append("At least one quality check should be included.")

        if len(work_instruction.missing_information) > 0:
            warnings.append(
                "The generated document contains missing information that must be reviewed."
            )

        if len(work_instruction.assumptions) > 0:
            warnings.append(
                "The generated document contains AI assumptions that must be reviewed."
            )

        return RuleCheckResult(warnings)