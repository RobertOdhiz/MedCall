from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict, Any

class PatientLogBase(BaseModel):
    patient_input_id: int
    symptoms: Optional[Dict[str, Any]] = None
    severity: Optional[str] = None
    triage_notes: Optional[str] = None

class PatientLogCreate(PatientLogBase):
    processed_by: Optional[str] = None

class PatientLog(PatientLogBase):
    id: int
    processed_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True