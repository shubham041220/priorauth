from pydantic import BaseModel
from typing import Optional

class ClinicalInformation(BaseModel):
    diagnosis: Optional[str] = None
    icd_10_code: Optional[str] = None
    prior_treatments_and_results: Optional[str] = None
    symptom_severity_and_impact: Optional[str] = None
    prognosis_and_risk_if_not_approved: Optional[str] = None
    clinical_rationale_for_urgency: Optional[str] = None

class NotesData(BaseModel):
    clinical_information: Optional[ClinicalInformation] = None