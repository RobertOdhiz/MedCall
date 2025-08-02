from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.schemas.triage import PatientRequest, AIResponse
from app.models.patient import PatientInput, PatientLog, Physician
from app.services.db import get_db
from app.services.orchestrator import WatsonXOrchestrator
import re

router = APIRouter()

def strip_mentions(text: str) -> str:
    return re.sub(r"<@[\w\d]+>", "", text).strip()

@router.post("/analyze", response_model=AIResponse)
def analyze_input(data: PatientRequest, db: Session = Depends(get_db)):

    # Step 1: Fetch and prepare message history from DB
    history_records = (
        db.query(PatientInput)
        .filter(PatientInput.slack_user_id == data.slack_user_id)
        .order_by(desc(PatientInput.created_at))
        .limit(10)
        .all()
    )
    history_records.reverse()

    # Step 2: Build initial message history
    message_history = []
    for record in history_records:
        message_history.append({"role": "user", "content": strip_mentions(record.input_text)})
        message_history.append({"role": "assistant", "content": record.ai_response})

    # Step 3: Add new input messages
    for m in data.input_text:
        message_history.append({
            "role": m.role,
            "content": strip_mentions(m.content)
        })

    # Step 4: Run the orchestrated workflow
    orchestrator = WatsonXOrchestrator()
    result = orchestrator.run_orchestration(message_history)
    print(f"Final AI response: {result}")

    # Step 5: Save the interaction
    last_user_msg = next((m for m in reversed(data.input_text) if m.role == "user"), None)
    if last_user_msg:
        record = PatientInput(
            slack_user_id=data.slack_user_id,
            input_text=strip_mentions(last_user_msg.content),
            ai_response=result
        )
        db.add(record)
        db.commit()
        db.refresh(record)

    return {"ai_response": result}

@router.post('/loguser', response_model=AIResponse)
def log_user(data: PatientRequest, db: Session = Depends(get_db)):
    """ """
    patient_logs = (
        db.query(PatientLog)
        .filter(PatientLog.slack_user_id == data.slack_user_id)
        .order_by(desc(PatientLog.created_at))
        .limit(10)
        .all()
    )
    patient_logs.reverse()
    logs_history = []
    for log in patient_logs:
        logs_history.append({"role": "user", "content": strip_mentions(log.input_text)})
        logs_history.append({"role": "assistant", "content": log.ai_response})
    
    for m in data.input_text:
        logs_history.append({
            "role": m.role,
            "content": strip_mentions(m.content)
        })