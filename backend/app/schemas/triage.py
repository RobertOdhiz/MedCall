from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class PatientRequest(BaseModel):
    slack_user_id: str
    input_text: List[Message]
    channel_id: Optional[str] = None

class AIResponse(BaseModel):
    ai_response: str
    requires_physician: bool = False
    physician_slack_id: Optional[str] = None
    is_emergency: bool = False