from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from datetime import datetime
from app.services.db import Base

class Physician(Base):
    __tablename__ = "physicians"

    id = Column(Integer, primary_key=True, index=True)
    slack_user_id = Column(String, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    specialty = Column(String, index=True, default="general")
    is_active = Column(Boolean, default=True)

    last_assigned_at = Column(DateTime, default=datetime.utcnow)
    current_patient_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PatientInput(Base):
    __tablename__ = "patient_inputs"

    id = Column(Integer, primary_key=True, index=True)
    slack_user_id = Column(String, index=True)
    input_text = Column(String)
    ai_response = Column(String)

    is_emergency = Column(Boolean, default=False)
    is_escalated = Column(Boolean, default=False)
    escalated_to = Column(Integer, ForeignKey('physicians.id'), nullable=True)
    escalation_reason =  Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PatientLog(Base):
    __tablename__ = 'patient_logs'

    id = Column(Integer, primary_key=True, index=True)
    patient_input_id = Column(Integer, ForeignKey('patient_inputs.id'), nullable=False, index=True)

    slack_user_id = Column(String, index=True)

    syptoms = Column(JSON)
    severity = Column(String, nullable=True)
    triage_notes = Column(String, nullable=True)

    processed_by =  Column(String, nullable=True)
    processed_at = Column(DateTime, default=datetime.utcnow)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)