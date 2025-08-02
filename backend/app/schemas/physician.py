from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class PhysicianBase(BaseModel):
    slack_user_id: str
    name: str
    email: str
    specialty: str = "general"

class PhysicianCreate(PhysicianBase):
    pass

class PhysicianUpdate(BaseModel):
    is_active: Optional[bool] = None
    current_patient_count: Optional[int] = None
    last_assigned_at: Optional[datetime] = None

class Physician(PhysicianBase):
    id: int
    is_active: bool
    current_patient_count: int
    last_assigned_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
