# models/labs_model.py

from pydantic import BaseModel
from typing import Optional

class LabResults(BaseModel):
    CBC: Optional[str] = None
    CMP: Optional[str] = None
    ESR: Optional[str] = None
    CRP: Optional[str] = None
    fecal_markers: Optional[str] = None
    abnormal_values: Optional[str] = None

class ClinicalInformation(BaseModel):
    lab_results: Optional[LabResults] = None

class LabsData(BaseModel):
    clinical_information: Optional[ClinicalInformation] = None