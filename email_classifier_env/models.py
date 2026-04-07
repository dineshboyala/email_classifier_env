from openenv.core.env_server.types import Action, Observation
from pydantic import BaseModel
from typing import Optional


class Email(BaseModel):
    id: int
    subject: str
    body: str
    category: Optional[str] = None


# ✅ IMPORTANT: MUST MATCH app.py imports
class EmailAction(Action):
    action_type: str
    email_id: int
    value: Optional[str] = None


class EmailObservation(Observation):
    goal: str
    current_email: Optional[Email]
    step: int