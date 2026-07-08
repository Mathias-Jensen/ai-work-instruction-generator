from tests.test_validator import valid_work_instruction_payload
from src.models import WorkInstructionOutput
from src.rule_checker import RuleChecker


def make_work_instruction(**overrides):
    payload = valid_work_instruction_payload()
    payload.update(overrides)
    return WorkInstructionOutput.model_validate(payload)


def test_rule_checker_passes_valid_instruction():
    instruction = make_work_instruction()

    result = RuleChecker.check(instruction)

    assert result.passed is True
    assert result.warnings == []


def test_rule_checker_warns_when_too_few_steps():
    instruction = make_work_instruction(
        procedure_steps=[
            {
                "step_number": 1,
                "instruction": "Stop machine.",
                "expected_result": "Machine stopped.",
                "safety_note": None,
            }
        ]
    )

    result = RuleChecker.check(instruction)

    assert result.passed is False
    assert any("at least 3 procedure steps" in warning for warning in result.warnings)


def test_rule_checker_warns_when_no_safety_precautions():
    instruction = make_work_instruction(safety_precautions=[])

    result = RuleChecker.check(instruction)

    assert result.passed is False
    assert any("safety precaution" in warning for warning in result.warnings)


def test_rule_checker_warns_when_human_review_disabled():
    instruction = make_work_instruction(human_review_required=False)

    result = RuleChecker.check(instruction)

    assert result.passed is False
    assert any("Human review" in warning for warning in result.warnings)