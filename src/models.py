# src/models.py

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ExperienceLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    experienced = "experienced"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class WorkInstructionInput(BaseModel):
    document_title: str = Field(..., description="Title of the work instruction")
    equipment_or_system: str = Field(..., description="Machine, equipment or system involved")
    target_user: str = Field(..., description="Intended user group")
    experience_level: ExperienceLevel = Field(..., description="Expected experience level of the user")
    raw_notes: str = Field(..., description="Unstructured technical notes from the user")


class ProcedureStep(BaseModel):
    step_number: int
    instruction: str
    expected_result: Optional[str] = None
    safety_note: Optional[str] = None


class SafetyPrecaution(BaseModel):
    precaution: str
    reason: Optional[str] = None
    risk_level: RiskLevel = RiskLevel.medium


class QualityCheck(BaseModel):
    check: str
    acceptance_criteria: str


class RiskMitigation(BaseModel):
    risk: str
    mitigation: str
    risk_level: RiskLevel = RiskLevel.medium


class MissingInformation(BaseModel):
    item: str
    why_it_matters: str


class WorkInstructionOutput(BaseModel):
    title: str
    purpose: str
    scope: str
    equipment_or_system: str
    target_user: str
    experience_level: ExperienceLevel

    required_tools: List[str] = Field(default_factory=list)
    required_materials: List[str] = Field(default_factory=list)

    safety_precautions: List[SafetyPrecaution] = Field(default_factory=list)
    procedure_steps: List[ProcedureStep] = Field(default_factory=list)
    quality_checks: List[QualityCheck] = Field(default_factory=list)
    risks_and_mitigations: List[RiskMitigation] = Field(default_factory=list)

    missing_information: List[MissingInformation] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)

    human_review_required: bool = True