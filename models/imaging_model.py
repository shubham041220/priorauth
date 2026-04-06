from pydantic import BaseModel
from typing import Optional

class ClinicalInformation(BaseModel):
    imaging_results: Optional[str] = None

class ImagingData(BaseModel):
    clinical_information: Optional[ClinicalInformation] = None