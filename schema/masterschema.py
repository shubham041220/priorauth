
from pydantic import BaseModel
from typing import Optional


class PatientInformation(BaseModel):
    patient_name: Optional[str] = None
    patient_date_of_birth: Optional[str] = None
    patient_id: Optional[str] = None
    patient_address: Optional[str] = None
    patient_phone_number: Optional[str] = None


class PhysicianContact(BaseModel):
    office_phone: Optional[str] = None
    fax: Optional[str] = None
    office_address: Optional[str] = None


class PhysicianInformation(BaseModel):
    physician_name: Optional[str] = None
    specialty: Optional[str] = None
    physician_contact: PhysicianContact = PhysicianContact()


class TreatmentRequest(BaseModel):
    name_of_medication_or_procedure: Optional[str] = None
    code_of_medication_or_procedure: Optional[str] = None
    dosage: Optional[str] = None
    duration: Optional[str] = None
    rationale: Optional[str] = None
    presumed_eligibility: Optional[str] = None


class ClinicalInformation(BaseModel):
    diagnosis: Optional[str] = None
    icd_10_code: Optional[str] = None
    prior_treatments_and_results: Optional[str] = None
    specific_drugs_taken_and_failures: Optional[str] = None
    alternative_drugs_required: Optional[str] = None
    lab_results: Optional[dict] = None
    lab_summary: Optional[str] = None
    imaging_results: Optional[str] = None
    symptom_severity_and_impact: Optional[str] = None
    prognosis_and_risk_if_not_approved: Optional[str] = None
    clinical_rationale_for_urgency: Optional[str] = None
    treatment_request: TreatmentRequest = TreatmentRequest()


class PriorAuthMasterSchema(BaseModel):
    patient_information: PatientInformation = PatientInformation()
    physician_information: PhysicianInformation = PhysicianInformation()
    clinical_information: ClinicalInformation = ClinicalInformation()