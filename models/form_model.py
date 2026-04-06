from pydantic import BaseModel
from typing import Optional

class PhysicianContact(BaseModel):
    office_phone: Optional[str] = None
    fax: Optional[str] = None
    office_address: Optional[str] = None

class PatientInformation(BaseModel):
    patient_name: Optional[str] = None
    patient_date_of_birth: Optional[str] = None
    patient_id: Optional[str] = None
    patient_address: Optional[str] = None
    patient_phone_number: Optional[str] = None

class PhysicianInformation(BaseModel):
    physician_name: Optional[str] = None
    specialty: Optional[str] = None
    physician_contact: Optional[PhysicianContact] = None

class TreatmentRequest(BaseModel):
    name_of_medication_or_procedure: Optional[str] = None
    code_of_medication_or_procedure: Optional[str] = None
    dosage: Optional[str] = None
    duration: Optional[str] = None
    rationale: Optional[str] = None
    presumed_eligibility: Optional[str] = None

class ClinicalInformation(BaseModel):
    treatment_request: Optional[TreatmentRequest] = None 

class FormData(BaseModel):
    patient_information: Optional[PatientInformation] = None
    physician_information: Optional[PhysicianInformation] = None
    clinical_information: Optional[ClinicalInformation] = None  