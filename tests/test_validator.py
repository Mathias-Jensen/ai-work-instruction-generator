import json
import pytest

from src.validator import OutputValidator


def valid_work_instruction_payload():
    return {
        "title": "Work Instruction: Sensor Replacement",
        "purpose": "Safely replace a defective sensor.",
        "scope": "Applies to maintenance technicians.",
        "equipment_or_system": "Conveyor system",
        "target_user": "Maintenance technician",
        "experience_level": "intermediate",
        "required_tools": ["Screwdriver"],
        "required_materials": ["Replacement sensor"],
        "safety_precautions": [
            {
                "precaution": "Apply lockout/tagout before work.",
                "reason": "Prevents accidental startup.",
                "risk_level": "high",
            }
        ],
        "procedure_steps": [
            {
                "step_number": 1,
                "instruction": "Stop the conveyor.",
                "expected_result": "Conveyor is stopped.",
                "safety_note": None,
            },
            {
                "step_number": 2,
                "instruction": "Replace the sensor.",
                "expected_result": "Sensor is installed.",
                "safety_note": None,
            },
            {
                "step_number": 3,
                "instruction": "Run a test cycle.",
                "expected_result": "System operates correctly.",
                "safety_note": "Keep clear of moving parts.",
            },
        ],
        "quality_checks": [
            {
                "check": "Verify signal in HMI.",
                "acceptance_criteria": "Sensor changes state correctly.",
            }
        ],
        "risks_and_mitigations": [
            {
                "risk": "Incorrect alignment.",
                "mitigation": "Adjust and verify signal.",
                "risk_level": "medium",
            }
        ],
        "missing_information": [],
        "assumptions": [],
        "human_review_required": True,
    }


def test_validator_accepts_valid_json():
    raw_response = json.dumps(valid_work_instruction_payload())

    result = OutputValidator.validate(raw_response)

    assert result.title == "Work Instruction: Sensor Replacement"
    assert len(result.procedure_steps) == 3
    assert result.human_review_required is True


def test_validator_rejects_invalid_json():
    raw_response = "{not valid json}"

    with pytest.raises(ValueError, match="invalid JSON"):
        OutputValidator.validate(raw_response)


def test_validator_rejects_invalid_risk_level():
    payload = valid_work_instruction_payload()
    payload["safety_precautions"][0]["risk_level"] = "critical"

    raw_response = json.dumps(payload)

    with pytest.raises(ValueError, match="validation failed"):
        OutputValidator.validate(raw_response)